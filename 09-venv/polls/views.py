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