"""HTTP 请求对象：解析请求行、请求头、查询参数与请求体。

一次完整请求在 TCP 字节流中的大致形态：

    GET /api/hello?name=Py HTTP/1.1\\r\\n
    Host: 127.0.0.1:8000\\r\\n
    Content-Length: 0\\r\\n
    \\r\\n
    <可选 body>
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


class Request:
    """封装一次 HTTP 请求的解析结果，供路由处理函数使用。"""

    def __init__(
        self,
        method: str,
        path: str,
        query_string: str,
        headers: dict[str, str],
        body: bytes,
        client_addr: tuple[str, int] | None = None,
    ) -> None:
        self.method = method.upper()  # GET / POST / ...
        self.path = path  # 不含 query 的路径，如 /users/1
        self.query_string = query_string  # name=Py&tag=a
        self.headers = headers  # Header 名保持原始大小写（教学简化）
        self.body = body  # 原始请求体字节
        self.client_addr = client_addr  # (ip, port)
        # 由 Router 匹配动态段后填入，如 {"user_id": "42"}
        self.path_params: dict[str, str] = {}
        # 懒解析缓存，避免同一请求多次 json()/form() 重复解码
        self._json_cache: Any | None = None
        self._form_cache: dict[str, str] | None = None

    @property
    def args(self) -> dict[str, list[str]]:
        """查询参数，如 /users?id=1&tag=a&tag=b → {"id":["1"], "tag":["a","b"]}"""
        return parse_qs(self.query_string, keep_blank_values=True)

    def get_arg(self, name: str, default: str | None = None) -> str | None:
        """取某个查询参数的第一个值（多值时常用这种简化接口）。"""
        values = self.args.get(name)
        return values[0] if values else default

    @property
    def content_type(self) -> str:
        return self.headers.get("Content-Type", "")

    @property
    def content_length(self) -> int:
        try:
            return int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return 0

    def json(self) -> Any:
        """将请求体解析为 JSON（application/json）。"""
        if self._json_cache is not None:
            return self._json_cache
        if not self.body:
            self._json_cache = None
            return None
        self._json_cache = json.loads(self.body.decode("utf-8"))
        return self._json_cache

    def form(self) -> dict[str, str]:
        """解析 application/x-www-form-urlencoded 表单（每个字段取首值）。"""
        if self._form_cache is not None:
            return self._form_cache
        parsed = parse_qs(self.body.decode("utf-8"), keep_blank_values=True)
        self._form_cache = {k: v[0] if v else "" for k, v in parsed.items()}
        return self._form_cache

    def text(self) -> str:
        """请求体按 UTF-8 解码为字符串。"""
        return self.body.decode("utf-8")

    @classmethod
    def from_raw(
        cls,
        raw: bytes,
        client_addr: tuple[str, int] | None = None,
    ) -> Request:
        """从原始 TCP 字节流解析一个完整 HTTP 请求。

        步骤：
        1. 用空行 \\r\\n\\r\\n 切开 header / body
        2. 第一行是请求行：METHOD TARGET VERSION
        3. 其余行是 Header: Value
        4. TARGET 可能是 /path?query，用 urlparse 拆开
        """
        # HTTP 报文：头部与正文之间固定以空行分隔
        header_part, _, body = raw.partition(b"\r\n\r\n")
        # 头部使用 latin-1（iso-8859-1）解码，与 HTTP 规范一致
        lines = header_part.decode("iso-8859-1").split("\r\n")
        if not lines or not lines[0]:
            raise ValueError("空的 HTTP 请求")

        # 请求行示例：GET /api/hello?name=Py HTTP/1.1
        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) < 2:
            raise ValueError(f"非法请求行: {request_line!r}")

        method, target = parts[0], parts[1]
        parsed = urlparse(target)
        # unquote：把 %20 之类还原成字符；空 path 归一成 /
        path = unquote(parsed.path) or "/"
        query_string = parsed.query

        headers: dict[str, str] = {}
        for line in lines[1:]:
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

        content_length = 0
        try:
            content_length = int(headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0

        # 若首次读入的 body 超过 Content-Length，截断多余字节；
        # 不足时由 server._recv_request 先补齐再调用本方法。
        if content_length and len(body) > content_length:
            body = body[:content_length]

        return cls(
            method=method,
            path=path,
            query_string=query_string,
            headers=headers,
            body=body,
            client_addr=client_addr,
        )
