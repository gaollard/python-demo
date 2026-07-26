from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def hello_world(request):
    print(request)
    # 打印请求方法
    print(request.method)
    # 打印请求头
    print(request.headers)
    # 打印请求体
    print(request.body)
    # 打印请求参数
    print(request.GET)
    # 打印请求路径
    print(request.path)
    # 打印 url 所有参数
    print(request.GET.items())
    return HttpResponse("Hello, World!")

def query_params(request):
    return HttpResponse("query_params")

def submit_form(request):
    if request.method == 'GET':
        # 处理GET请求 - 显示表单
        return HttpResponse("显示表单页面")
    elif request.method == 'POST':
        # 处理POST请求 - 处理表单提交
        return HttpResponse("处理表单提交")
    else:
        # 其他HTTP方法
        return HttpResponse("不支持的请求方法")

# 使用装饰器限制只允许GET请求
@require_GET
def get_only_view(request):
    return HttpResponse("这个视图只接受GET请求")

# 使用装饰器限制只允许POST请求
@require_POST
def post_only_view(request):
    return HttpResponse("这个视图只接受POST请求")

# 使用装饰器限制允许GET和POST请求
@require_http_methods(["GET"])
def preview_view(request):
    """预览表单页面"""
    # 渲染表单页面
    return render(request, 'form.html')

@require_http_methods(["POST"])
def submit_form_view(request):
    """处理表单提交"""
    # 获取表单数据
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    age = request.POST.get('age', '')
    gender = request.POST.get('gender', '')
    city = request.POST.get('city', '')
    hobbies = request.POST.getlist('hobbies')  # 获取多选框的值
    message = request.POST.get('message', '')
    agree_terms = request.POST.get('agree_terms', '')

    file_upload = request.FILES.get('file_upload', None)
    
    if file_upload:
        file_name = file_upload.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb') as f:
            for chunk in file_upload.chunks():
                f.write(chunk)
        # file_content = file_upload.read()
        print( "文件路径: " + file_path) 
        logger.info("文件路径" + file_path)
        
        # print(file_content)
    
    # 构建响应内容
    hobbies_str = ', '.join(hobbies) if hobbies else '无'
    message_str = message if message else '无'
    agree_str = '是' if agree_terms else '否'
    
    response_content = f"""
    <html>
    <head>
        <title>表单提交结果</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
            .result {{ background-color: #f0f8ff; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; }}
            .field {{ margin-bottom: 10px; }}
            .label {{ font-weight: bold; }}
            .back-link {{ margin-top: 20px; }}
            .back-link a {{ color: #007bff; text-decoration: none; }}
            .back-link a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="result">
            <h1>表单提交成功！</h1>
            <div class="field">
                <span class="label">姓名:</span> {name}
            </div>
            <div class="field">
                <span class="label">邮箱:</span> {email}
            </div>
            <div class="field">
                <span class="label">年龄:</span> {age}
            </div>
            <div class="field">
                <span class="label">性别:</span> {gender}
            </div>
            <div class="field">
                <span class="label">城市:</span> {city}
            </div>
            <div class="field">
                <span class="label">兴趣爱好:</span> {hobbies_str}
            </div>
            <div class="field">
                <span class="label">留言:</span> {message_str}
            </div>
            <div class="field">
                <span class="label">同意条款:</span> {agree_str}
            </div>
            <div class="back-link">
                <a href="/polls/preview">返回表单</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(response_content)

def test_middleware(request):
    """测试中间件功能的视图"""
    logger.info("测试中间件视图被调用")
    
    # 获取请求信息
    client_ip = request.META.get('REMOTE_ADDR', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    response_content = f"""
    <html>
    <head>
        <title>中间件测试</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            .info {{ background-color: #f0f8ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .header {{ background-color: #e8f5e8; padding: 15px; border-radius: 8px; }}
            h1 {{ color: #333; }}
            .field {{ margin-bottom: 10px; }}
            .label {{ font-weight: bold; }}
            .value {{ color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>中间件功能测试</h1>
            <p>这个页面用于测试我们添加的自定义中间件功能</p>
        </div>
        
        <div class="info">
            <h2>请求信息</h2>
            <div class="field">
                <span class="label">请求方法:</span> <span class="value">{request.method}</span>
            </div>
            <div class="field">
                <span class="label">请求路径:</span> <span class="value">{request.path}</span>
            </div>
            <div class="field">
                <span class="label">客户端IP:</span> <span class="value">{client_ip}</span>
            </div>
            <div class="field">
                <span class="label">用户代理:</span> <span class="value">{user_agent}</span>
            </div>
            <div class="field">
                <span class="label">请求时间:</span> <span class="value">{request.META.get('REQUEST_TIME', 'Unknown')}</span>
            </div>
        </div>
        
        <div class="info">
            <h2>中间件功能说明</h2>
            <ul>
                <li><strong>RequestLoggingMiddleware:</strong> 记录每个请求的详细信息，包括处理时间</li>
                <li><strong>SecurityHeadersMiddleware:</strong> 添加安全相关的HTTP头</li>
                <li><strong>RateLimitMiddleware:</strong> 限制请求频率（每分钟最多100次）</li>
                <li><strong>CustomErrorMiddleware:</strong> 自定义错误处理</li>
            </ul>
        </div>
        
        <div class="info">
            <h2>测试链接</h2>
            <p><a href="/polls/hello">Hello World</a> - 测试基本功能</p>
            <p><a href="/polls/preview">表单预览</a> - 测试表单功能</p>
            <p><a href="/polls/test_middleware">刷新此页面</a> - 查看中间件日志</p>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(response_content)

def trigger_error(request):
    """触发错误的视图，用于测试错误处理中间件"""
    logger.info("触发错误视图被调用")
    
    # 故意引发一个异常来测试错误处理中间件
    raise Exception("这是一个测试异常，用于测试CustomErrorMiddleware")