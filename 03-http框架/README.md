# 03 · 纯 Python 实现 HTTP 框架

只使用 Python **标准库**（`socket` / `threading` / `json` / `urllib` 等），不依赖 Flask、Django、FastAPI。

## 目录

```
03-http框架/
├── README.md
├── example.py          # 可运行示例
└── minihttp/           # 框架核心
    ├── __init__.py
    ├── app.py          # MiniHTTP：路由装饰器、中间件、分发
    ├── request.py      # Request：解析请求行 / Header / Query / Body
    ├── response.py     # Response：组装 HTTP/1.1 响应
    ├── router.py       # 路由表：支持 /users/<id> 动态参数
    └── server.py       # 基于 socket 的多线程 TCP 服务器
```

## 快速开始

```sh
cd 03-http框架
python example.py
```

另开终端：

```sh
curl http://127.0.0.1:8000/
curl 'http://127.0.0.1:8000/api/hello?name=Python'
curl http://127.0.0.1:8000/users/42
curl -X POST http://127.0.0.1:8000/api/echo \
  -H 'Content-Type: application/json' \
  -d '{"msg":"hi"}'
```

## 最小用法

```python
from minihttp import MiniHTTP

app = MiniHTTP("demo")

@app.get("/")
def index(request):
    return {"ok": True}

@app.get("/users/<int:user_id>")
def user(request, user_id):
    return {"id": int(user_id)}

@app.post("/api/echo")
def echo(request):
    return {"echo": request.json()}

@app.middleware
def log(request, call_next):
    resp = call_next(request)
    print(request.method, request.path, resp.status)
    return resp

app.run(port=8000)
```

## 设计要点

| 模块 | 做什么 |
|------|--------|
| `server` | `accept` 连接 → 读完整请求字节 → 调 `app.handle` → 写回响应 |
| `request` | 按 HTTP/1.1 解析 Method / Path / Query / Headers / Body |
| `router` | 正则编译路由；`<name>` / `<int:name>` / `<path:name>` |
| `app` | Flask 风格装饰器；中间件洋葱模型；返回值自动转 Response |
| `response` | 拼 `HTTP/1.1 status` + headers + body |

返回值约定：

- `dict` / `list` → JSON
- `str` → text/plain
- `Response` → 原样返回
- `(body, status)` → 带状态码
- `None` → 204

## 路由装饰器原理

`app.get` **本身不是装饰器**，而是**装饰器工厂**（decorator factory）。

### 调用链

`get` 只做一件事：调用 `route`，并固定 `methods=["GET"]`：

```python
def get(self, path: str):
    return self.route(path, methods=["GET"])
```

真正的装饰逻辑在 `route` 里：

```python
def route(self, path: str, methods: list[str] | None = None):
    methods = methods or ["GET"]

    def decorator(func: Handler) -> Handler:
        self.router.add(methods, path, func)
        return func

    return decorator
```

### 使用时发生了什么

```python
@app.get("/")
def index(request):
    return {"hello": "world"}
```

等价于：

```python
def index(request):
    return {"hello": "world"}

index = app.get("/")(index)
# 展开后：
# decorator = app.route("/", methods=["GET"])  ← get 返回这个
# index = decorator(index)                      ← 这里才注册路由
```

| 函数 | 角色 |
|------|------|
| `get(path)` | 装饰器工厂：接收路径，返回装饰器 |
| `route` 内部的 `decorator(func)` | 真正的装饰器：注册 handler 并返回原函数 |
| `middleware(func)` | 直接就是装饰器（不需要额外参数） |

### 为什么要分两层？

因为 `@app.get("/")` 需要**先传路径**，再**装饰函数**。Python 的 `@` 语法只能写一层，所以常见写法是：

1. 外层函数（`get` / `route`）接收配置参数（`path`）
2. 返回内层函数（`decorator`），内层才是接收被装饰函数的那个

对比一下 `middleware`——它不需要额外参数，所以可以直接写成装饰器：

```python
def middleware(self, func: Middleware) -> Middleware:
    self.middlewares.append(func)
    return func
```

`post`、`put`、`delete` 与 `get` 是同一模式，都是 `route` 的语法糖。

## 与 `02-basic/14-网络` 的关系

- `02-basic` 里用的是标准库 `http.server`，适合快速起静态/简单 API。
- 本目录从 **原始 socket** 自己解析协议，目的是理解「框架」在 `http.server` 下面做了什么。
