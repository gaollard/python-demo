# Python HTTP Server Docker 部署指南

这是一个基于Python内置HTTP服务器模块的容器化应用，提供多种API端点和文件浏览功能。

## 🚀 功能特性

- **RESTful API端点**:
  - `GET /` - 主页，显示服务器信息和可用端点
  - `GET /api/info` - 获取服务器信息(JSON格式)
  - `GET /api/time` - 获取当前时间
  - `POST /api/echo` - 数据回显功能
  - `GET /files/` - 文件浏览功能

- **Docker特性**:
  - 基于Python 3.13 slim镜像
  - 非root用户运行，提高安全性
  - 内置健康检查
  - 支持环境变量配置
  - 优化的构建过程

## 📋 前置要求

- Docker Engine 20.10+
- Docker Compose 2.0+ (可选)

## 🛠️ 快速开始

### 方法1: 使用Docker命令

```bash
# 构建镜像
docker build -t python-http-server .

# 运行容器
docker run -p 8000:8000 python-http-server
```

### 方法2: 使用Docker Compose (推荐)

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🔧 配置选项

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 8000 | 服务器监听端口 |

### 端口映射

```bash
# 自定义端口映射
docker run -p 8080:8000 python-http-server

# 使用环境变量
docker run -p 8080:8000 -e PORT=8080 python-http-server
```

## 📁 文件结构

```
container/
├── Dockerfile              # Docker镜像构建文件
├── docker-compose.yml      # Docker Compose配置
├── .dockerignore          # Docker构建忽略文件
├── main.py                # Python HTTP服务器源码
└── README.md              # 本文档
```

## 🧪 测试API

启动服务后，可以通过以下方式测试API:

```bash
# 访问主页
curl http://localhost:8000/

# 获取服务器信息
curl http://localhost:8000/api/info

# 获取当前时间
curl http://localhost:8000/api/time

# 测试POST回显
curl -X POST -d "Hello World" http://localhost:8000/api/echo

# 浏览文件
curl http://localhost:8000/files/
```

## 🔍 监控和日志

### 查看容器状态

```bash
# 查看运行中的容器
docker ps

# 查看容器详细信息
docker inspect python-http-server
```

### 查看日志

```bash
# 实时查看日志
docker logs -f python-http-server

# 查看最近100行日志
docker logs --tail 100 python-http-server
```

### 健康检查

```bash
# 查看健康状态
docker inspect --format='{{.State.Health.Status}}' python-http-server
```

## 🛡️ 安全特性

- **非root用户**: 应用以`appuser`用户运行，提高安全性
- **最小权限**: 只安装必要的系统依赖
- **健康检查**: 自动监控服务状态
- **资源限制**: 可通过Docker Compose设置资源限制

## 🔧 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口占用
   lsof -i :8000
   
   # 使用其他端口
   docker run -p 8080:8000 python-http-server
   ```

2. **容器无法启动**
   ```bash
   # 查看详细错误信息
   docker logs python-http-server
   
   # 检查镜像构建
   docker build --no-cache -t python-http-server .
   ```

3. **健康检查失败**
   ```bash
   # 手动测试连接
   docker exec python-http-server python -c "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"
   ```

## 📈 性能优化

### 资源限制

在`docker-compose.yml`中添加资源限制:

```yaml
services:
  python-http-server:
    # ... 其他配置
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 多实例部署

```yaml
services:
  python-http-server:
    # ... 其他配置
    deploy:
      replicas: 3
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

本项目采用MIT许可证。
