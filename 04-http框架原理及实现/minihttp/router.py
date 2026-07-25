"""路由表：支持精确路径与 /users/<id> 动态参数。

路由规则在注册时编译成正则，匹配时抽出命名捕获组作为 path_params。
"""

from __future__ import annotations

import re
from typing import Callable


Handler = Callable[..., object]


class Route:
    """单条路由：HTTP 方法集合 + 路径模板 + 处理函数。"""

    def __init__(self, methods: set[str], path: str, handler: Handler) -> None:
        self.methods = {m.upper() for m in methods}
        self.path = path
        self.handler = handler
        self._param_names: list[str] = []
        self._regex = self._compile(path)

    def _compile(self, path: str) -> re.Pattern[str]:
        """把路径模板编译成正则。

        示例：
            /users/<id>       -> ^/users/(?P<id>[^/]+)$
            /users/<int:id>   -> ^/users/(?P<id>\\d+)$
            /files/<path:p>   -> ^/files/(?P<p>.+)$
        """
        pattern_parts: list[str] = []
        # "/" 单独处理；其它路径按 / 切段再拼接
        for part in path.strip("/").split("/") if path != "/" else []:
            if part.startswith("<") and part.endswith(">"):
                # <name> 或 <type:name>
                inner = part[1:-1]
                if ":" in inner:
                    type_name, name = inner.split(":", 1)
                else:
                    type_name, name = "str", inner
                self._param_names.append(name)
                # path：可含斜杠；int：纯数字；默认 str：单段非斜杠
                if type_name == "path":
                    pattern_parts.append(f"(?P<{name}>.+)")
                elif type_name == "int":
                    pattern_parts.append(f"(?P<{name}>\\d+)")
                else:
                    pattern_parts.append(f"(?P<{name}>[^/]+)")
            else:
                # 静态段做 re.escape，避免特殊字符被当成正则语法
                pattern_parts.append(re.escape(part))

        if path == "/":
            regex = r"^/$"
        else:
            regex = "^/" + "/".join(pattern_parts) + "$"
        return re.compile(regex)

    def match(self, method: str, path: str) -> dict[str, str] | None:
        """方法与路径都匹配时返回参数字典，否则 None。"""
        if method.upper() not in self.methods:
            return None
        m = self._regex.match(path)
        if not m:
            return None
        return m.groupdict()


class Router:
    """路由表：按注册顺序匹配，先命中者优先。"""

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def add(self, methods: set[str] | list[str], path: str, handler: Handler) -> None:
        """注册一条路由。"""
        self.routes.append(Route(set(methods), path, handler))

    def resolve(self, method: str, path: str) -> tuple[Handler, dict[str, str]] | None:
        """解析 (method, path) → (handler, path_params)。

        - 路径与方法都匹配：返回处理函数与参数
        - 路径匹配但方法不对：抛 MethodNotAllowed（上层转 405）
        - 都不匹配：返回 None（上层转 404）
        """
        allowed_methods: set[str] = set()
        for route in self.routes:
            # 先看路径是否匹配，再判断方法（便于收集 Allow 列表）
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
            # 路径能匹配但方法不对时，记下允许的方法
            if route._regex.match(path):
                allowed_methods |= route.methods

        if allowed_methods:
            # 路径存在但方法不对：交给 app 返回 405 + Allow
            raise MethodNotAllowed(sorted(allowed_methods))
        return None


class MethodNotAllowed(Exception):
    """路径存在、但当前 HTTP 方法未注册时抛出。"""

    def __init__(self, allowed: list[str]) -> None:
        self.allowed = allowed  # 用于写响应头 Allow
        super().__init__(f"Allowed: {', '.join(allowed)}")
