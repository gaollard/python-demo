"""HTTP 响应对象与常用响应构造函数。

组装后的字节流形态：

    HTTP/1.1 200 OK\\r\\n
    Content-Type: application/json; charset=utf-8\\r\\n
    Content-Length: 17\\r\\n
    Connection: close\\r\\n
    \\r\\n
    {"hello":"world"}
"""

from __future__ import annotations

import json
from typing import Any


# 常见状态码对应的 reason phrase（状态行第三段）
STATUS_TEXT = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}


class Response:
    """封装状态码、响应头与响应体，最终通过 to_bytes() 写出到 socket。"""

    def __init__(
        self,
        body: bytes | str = b"",
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        # 统一成 bytes，方便计算 Content-Length 与 sendall
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.body = body
        self.status = status
        # 默认头：短连接（Connection: close），每次请求后关闭 TCP
        self.headers: dict[str, str] = {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": str(len(self.body)),
            "Connection": "close",
        }
        if headers:
            self.headers.update(headers)
            # 外部若未显式给 Content-Length，按最终 body 长度回写，避免不一致
            if "Content-Length" not in (headers or {}):
                self.headers["Content-Length"] = str(len(self.body))

    def set_header(self, key: str, value: str) -> None:
        """设置或覆盖单个响应头（如 405 时的 Allow）。"""
        self.headers[key] = value

    def to_bytes(self) -> bytes:
        """拼成符合 HTTP/1.1 的完整响应字节：状态行 + 头部 + 空行 + body。"""
        reason = STATUS_TEXT.get(self.status, "Unknown")
        status_line = f"HTTP/1.1 {self.status} {reason}\r\n"
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        # 头部用 iso-8859-1；body 保持原样（可能是 UTF-8 JSON）
        return (status_line + header_lines + "\r\n").encode("iso-8859-1") + self.body


def text_response(text: str, status: int = 200) -> Response:
    """纯文本响应。"""
    return Response(
        body=text,
        status=status,
        headers={"Content-Type": "text/plain; charset=utf-8"},
    )


def html_response(html: str, status: int = 200) -> Response:
    """HTML 页面响应。"""
    return Response(
        body=html,
        status=status,
        headers={"Content-Type": "text/html; charset=utf-8"},
    )


def json_response(data: Any, status: int = 200) -> Response:
    """JSON 响应；ensure_ascii=False 保留中文可读性。"""
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    return Response(
        body=payload,
        status=status,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
