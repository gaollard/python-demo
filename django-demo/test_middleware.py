#!/usr/bin/env python
"""
测试中间件功能的脚本
"""
import os
import sys
import django
from django.conf import settings
from django.test import RequestFactory
from django.http import HttpResponse

# 添加项目路径
sys.path.append('/Users/xiong.gao/code/python-demo/09-venv')

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from polls.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware, RateLimitMiddleware, CustomErrorMiddleware
from polls.views import test_middleware, trigger_error

def test_middlewares():
    """测试中间件功能"""
    print("开始测试中间件功能...")
    
    # 创建请求工厂
    factory = RequestFactory()
    
    # 创建测试请求
    request = factory.get('/polls/test_middleware')
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    request.META['HTTP_USER_AGENT'] = 'Test Browser'
    
    # 测试RequestLoggingMiddleware
    print("\n1. 测试RequestLoggingMiddleware...")
    logging_middleware = RequestLoggingMiddleware(lambda req: HttpResponse("Test Response"))
    response = logging_middleware(request)
    print(f"响应状态码: {response.status_code}")
    
    # 测试SecurityHeadersMiddleware
    print("\n2. 测试SecurityHeadersMiddleware...")
    security_middleware = SecurityHeadersMiddleware(lambda req: HttpResponse("Test Response"))
    response = security_middleware(request)
    print(f"安全头: {dict(response.items())}")
    
    # 测试RateLimitMiddleware
    print("\n3. 测试RateLimitMiddleware...")
    rate_limit_middleware = RateLimitMiddleware(lambda req: HttpResponse("Test Response"))
    response = rate_limit_middleware(request)
    print(f"频率限制响应状态码: {response.status_code}")
    
    # 测试CustomErrorMiddleware
    print("\n4. 测试CustomErrorMiddleware...")
    error_middleware = CustomErrorMiddleware(lambda req: HttpResponse("Test Response"))
    
    # 创建一个会引发异常的请求
    def error_view(req):
        raise Exception("测试异常")
    
    error_middleware_with_error = CustomErrorMiddleware(error_view)
    try:
        response = error_middleware_with_error(request)
        print(f"错误处理响应状态码: {response.status_code}")
    except Exception as e:
        print(f"捕获到异常: {e}")
    
    print("\n中间件测试完成！")

if __name__ == '__main__':
    test_middlewares()
