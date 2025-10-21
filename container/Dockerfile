# ===========================================
# Python HTTP Server Dockerfile
# ===========================================
# 这是一个用于容器化Python HTTP服务器的Dockerfile
# 支持多种API端点和文件浏览功能

# 使用官方Python 3.13 slim镜像作为基础镜像
# slim版本更小，只包含运行时必需的文件
FROM python:3.13-slim

# 设置标签信息
LABEL maintainer="Python Demo" \
      version="1.0" \
      description="Python HTTP Server with API endpoints and file browsing"

# 设置工作目录
WORKDIR /app

# 设置环境变量
# PYTHONUNBUFFERED: 确保Python输出直接发送到终端，不缓冲
# PYTHONDONTWRITEBYTECODE: 防止Python生成.pyc文件
# PORT: 默认端口号
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# 更新包管理器并安装必要的系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

# 创建非root用户以提高安全性
# 这是Docker最佳实践，避免以root用户运行应用
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /bin/bash appuser

# 复制应用文件到容器
COPY main.py /app/

# 创建日志目录并设置适当的权限
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app && \
    chmod 755 /app

# 切换到非root用户
USER appuser

# 暴露端口8000
# 这个端口与main.py中的默认端口一致
EXPOSE 8000

# 添加健康检查
# 每30秒检查一次服务器是否响应
HEALTHCHECK --interval=30s \
            --timeout=10s \
            --start-period=5s \
            --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8000)); s.close()" || exit 1

# 设置启动命令
# 使用exec形式确保信号处理正确
CMD ["python", "main.py"]

# ===========================================
# 构建和运行说明:
# ===========================================
# 构建镜像:
#   docker build -t python-http-server .
#
# 运行容器:
#   docker run -p 8000:8000 python-http-server
#
# 运行容器(自定义端口):
#   docker run -p 8080:8000 -e PORT=8080 python-http-server
#
# 后台运行:
#   docker run -d -p 8000:8000 --name http-server python-http-server
#
# 查看日志:
#   docker logs http-server
#
# 停止容器:
#   docker stop http-server
# ===========================================