import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    请求日志中间件 - 记录每个请求的详细信息
    """
    
    def process_request(self, request):
        """处理请求前的逻辑"""
        # 记录请求开始时间
        request.start_time = time.time()
        
        # 记录请求信息
        logger.info(f"请求开始: {request.method} {request.path}")
        logger.info(f"用户代理: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        logger.info(f"客户端IP: {self.get_client_ip(request)}")
        
        return None
    
    def process_response(self, request, response):
        """处理响应后的逻辑"""
        # 计算请求处理时间
        if hasattr(request, 'start_time'):
            process_time = time.time() - request.start_time
            logger.info(f"请求完成: {request.method} {request.path} - 耗时: {process_time:.3f}秒")
            logger.info(f"响应状态码: {response.status_code}")

        # 返回 JSON 响应
        # return JsonResponse({
        #     "status": "success",
        #     "message": "请求完成",
        #     "data": {
        #         "request_method": request.method,
        #         "request_path": request.path,
        #         "process_time": process_time,
        #         "status_code": response.status_code,
        #     },
        # })
        
        return response
    
    def get_client_ip(self, request):
        """获取客户端真实IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    安全头中间件 - 添加安全相关的HTTP头
    """
    
    def process_response(self, request, response):
        """为响应添加安全头"""
        # 防止XSS攻击
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # 内容安全策略
        response['Content-Security-Policy'] = "default-src 'self'"
        
        # 严格传输安全（仅在HTTPS下使用）
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class CustomErrorMiddleware(MiddlewareMixin):
    """
    自定义错误处理中间件
    """
    
    def process_exception(self, request, exception):
        """处理异常"""
        logger.error(f"异常发生: {request.path} - {str(exception)}")
        
        # 返回自定义错误页面
        return HttpResponse(
            f"""
            <html>
            <head>
                <title>服务器错误</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }}
                    .error {{ color: #d32f2f; }}
                </style>
            </head>
            <body>
                <h1 class="error">服务器内部错误</h1>
                <p>抱歉，服务器遇到了一个错误。请稍后重试。</p>
                <p><a href="/polls/hello">返回首页</a></p>
            </body>
            </html>
            """,
            status=500
        )


class RateLimitMiddleware(MiddlewareMixin):
    """
    简单的请求频率限制中间件
    """
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.request_counts = {}
        self.max_requests = 100  # 每分钟最大请求数
        self.time_window = 60    # 时间窗口（秒）
    
    def process_request(self, request):
        """检查请求频率"""
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # 清理过期的记录
        self.cleanup_old_records(current_time)
        
        # 检查当前IP的请求频率
        if client_ip in self.request_counts:
            if len(self.request_counts[client_ip]) >= self.max_requests:
                logger.warning(f"IP {client_ip} 请求过于频繁，被限制")
                return HttpResponse(
                    """
                    <html>
                    <head><title>请求过于频繁</title></head>
                    <body>
                        <h1>请求过于频繁</h1>
                        <p>您的请求过于频繁，请稍后再试。</p>
                    </body>
                    </html>
                    """,
                    status=429
                )
        
        # 记录当前请求
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        self.request_counts[client_ip].append(current_time)
        
        return None
    
    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def cleanup_old_records(self, current_time):
        """清理过期的请求记录"""
        for ip in list(self.request_counts.keys()):
            # 移除时间窗口外的记录
            self.request_counts[ip] = [
                timestamp for timestamp in self.request_counts[ip]
                if current_time - timestamp < self.time_window
            ]
            # 如果列表为空，删除该IP的记录
            if not self.request_counts[ip]:
                del self.request_counts[ip]
