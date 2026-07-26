# 实现文件上传功能
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

@require_POST
def upload_file(request):
    """实现文件上传功能"""
    # d
    file = request.FILES['file']
    # 获取文件名
    file_name = file.name
    # 获取文件内容
    file_content = file.read()
    print(file_name)
    print(file_content)
    # 返回文件内容
    return HttpResponse(file_content)