from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

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
@require_http_methods(["GET", "POST"])
def get_post_view(request):
    if request.method == 'GET':
        return HttpResponse("GET请求处理")
    else:  # POST
        return HttpResponse("POST请求处理")