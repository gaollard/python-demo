"""
迷你 HTTP 框架示例。

运行：
    cd 03-http框架
    python example.py

测试：
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/api/hello?name=Python
    curl http://127.0.0.1:8000/users/42
    curl -X POST http://127.0.0.1:8000/api/echo -H 'Content-Type: application/json' -d '{"msg":"hi"}'
"""

from minihttp import MiniHTTP, html_response, json_response, text_response

app = MiniHTTP("demo")


@app.middleware
def access_log(request, call_next):
    """访问日志中间件：先放行到内层，再根据响应状态打印一行。"""
    response = call_next(request)
    client = request.client_addr[0] if request.client_addr else "-"
    print(f"{client} {request.method} {request.path} -> {response.status}")
    return response


@app.get("/")
def index(request):
    """首页：直接返回 HTML Response。"""
    return html_response(
        """
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>MiniHTTP</title></head>
        <body>
            <h1>MiniHTTP Demo</h1>
            <ul>
                <li><a href="/api/hello?name=Python">GET /api/hello</a></li>
                <li><a href="/users/1">GET /users/&lt;id&gt;</a></li>
                <li>POST /api/echo （JSON body）</li>
            </ul>
        </body>
        </html>
        """
    )


@app.get("/api/hello")
def hello(request):
    """演示查询参数：dict 返回值会自动转成 JSON。"""
    name = request.get_arg("name", "World")
    return {"message": f"Hello, {name}!"}


@app.get("/users/<int:user_id>")
def get_user(request, user_id: str):
    """演示动态路由：<int:user_id> 匹配数字并作为关键字参数传入。"""
    return {"id": int(user_id), "name": f"user-{user_id}"}


@app.post("/api/echo")
def echo(request):
    """演示 JSON body：request.json() 解析请求体。"""
    data = request.json()
    return {"echo": data}


@app.get("/plain")
def plain(request):
    """演示显式构造 text Response。"""
    return text_response("just plain text")


@app.get("/error")
def boom(request):
    """演示未捕获异常 → 框架统一返回 500 JSON。"""
    raise RuntimeError("demo error")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
