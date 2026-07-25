"""应用入口：路由装饰器、中间件、请求分发。

调用链（自外向内）：

    socket 收到字节
      → Request.from_raw
      → MiniHTTP.handle（中间件洋葱）
          → _dispatch（路由匹配 + 调 handler）
          → _normalize（把返回值转成 Response）
      → Response.to_bytes 写回客户端
"""

from __future__ import annotations

from typing import Any, Callable

from .request import Request
from .response import Response, json_response, text_response
from .router import MethodNotAllowed, Router
from .server import serve


Handler = Callable[..., Any]
# 中间件签名：接收 request 与 call_next，必须返回 Response
Middleware = Callable[[Request, Callable[[Request], Response]], Response]


class MiniHTTP:
    """
    迷你 HTTP 框架，风格类似 Flask：

        app = MiniHTTP("demo")

        @app.get("/")
        def index(request):
            return {"hello": "world"}

        app.run(host="127.0.0.1", port=8000)
    """

    def __init__(self, name: str = "minihttp") -> None:
        self.name = name
        self.router = Router()
        self.middlewares: list[Middleware] = []

    # ---------- 路由装饰器 ----------

    def route(self, path: str, methods: list[str] | None = None):
        """通用路由装饰器；get/post/... 都是它的语法糖。"""
        methods = methods or ["GET"]

        def decorator(func: Handler) -> Handler:
            self.router.add(methods, path, func)
            return func

        return decorator

    def get(self, path: str):
        return self.route(path, methods=["GET"])

    def post(self, path: str):
        return self.route(path, methods=["POST"])

    def put(self, path: str):
        return self.route(path, methods=["PUT"])

    def delete(self, path: str):
        return self.route(path, methods=["DELETE"])

    # ---------- 中间件 ----------

    def middleware(self, func: Middleware) -> Middleware:
        """注册中间件：middleware(request, call_next) -> Response。

        先注册的中间件在最外层（先看到请求、最后看到响应）。
        """
        self.middlewares.append(func)
        return func

    # ---------- 请求处理 ----------

    def handle(self, request: Request) -> Response:
        """入口：包一层中间件链，再交给 _dispatch；未捕获异常统一 500。"""

        def dispatch(req: Request) -> Response:
            return self._dispatch(req)

        # 洋葱模型：从内到外包装。
        # 假设中间件注册顺序为 [A, B]，最终调用顺序为：
        #   A 进入 → B 进入 → dispatch → B 返回 → A 返回
        call_next: Callable[[Request], Response] = dispatch
        for mw in reversed(self.middlewares):
            next_fn = call_next

            # 用闭包工厂固定 mw / next_fn，避免循环变量被后续迭代覆盖
            def make_wrapper(middleware: Middleware, nxt: Callable[[Request], Response]):
                def wrapper(req: Request) -> Response:
                    return middleware(req, nxt)

                return wrapper

            call_next = make_wrapper(mw, next_fn)

        try:
            return call_next(request)
        except Exception as exc:  # noqa: BLE001 - 教学框架统一兜底
            return json_response(
                {"error": "Internal Server Error", "detail": str(exc)},
                status=500,
            )

    def _dispatch(self, request: Request) -> Response:
        """路由匹配 → 调 handler → 规范化返回值。"""
        try:
            resolved = self.router.resolve(request.method, request.path)
        except MethodNotAllowed as exc:
            # 405：路径存在但方法不对，并带上 Allow 头
            resp = text_response("Method Not Allowed", status=405)
            resp.set_header("Allow", ", ".join(exc.allowed))
            return resp

        if resolved is None:
            return json_response({"error": "Not Found", "path": request.path}, status=404)

        handler, params = resolved
        request.path_params = params  # 挂到 request 上，也作为 **kwargs 传入
        result = handler(request, **params)
        return self._normalize(result)

    def _normalize(self, result: Any) -> Response:
        """把 handler 的多种返回值约定转成统一的 Response。

        - Response          → 原样
        - (body, status)    → 带状态码
        - dict / list       → JSON
        - None              → 204
        - 其它              → text/plain
        """
        if isinstance(result, Response):
            return result
        if isinstance(result, tuple) and len(result) == 2:
            body, status = result
            if isinstance(body, (dict, list)):
                return json_response(body, status=status)
            return text_response(str(body), status=status)
        if isinstance(result, (dict, list)):
            return json_response(result)
        if result is None:
            return Response(b"", status=204)
        return text_response(str(result))

    # ---------- 启动 ----------

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """阻塞启动内置 socket 服务器（Ctrl+C 结束）。"""
        print(f"[{self.name}] http://{host}:{port}")
        serve(self, host=host, port=port)
