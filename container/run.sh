# 进入container目录
cd container

# 构建镜像
podman build -t python-http-server .

# 运行容器
podman run -p 8000:8000 python-http-server

# 或者使用Docker Compose
docker-compose up -d