from django.shortcuts import render
from django.http import HttpResponse

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