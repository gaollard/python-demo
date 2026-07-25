"""基于 socket 的 HTTP/1.1 服务器（仅标准库）。

职责很窄：accept 连接 → 读完整请求 → 调 app.handle → 写回响应。
协议解析与业务分发分别交给 Request / MiniHTTP。
"""

from __future__ import annotations

import socket
import threading
from typing import TYPE_CHECKING, Protocol

from .request import Request
from .response import Response, text_response

if TYPE_CHECKING:
    pass


class AppProtocol(Protocol):
    """server 只依赖 handle 方法，便于解耦（不必硬绑 MiniHTTP 类）。"""

    def handle(self, request: Request) -> Response: ...


BUFFER_SIZE = 65536  # 单次 recv 缓冲
MAX_HEADER_SIZE = 64 * 1024  # 防止恶意超大请求头撑爆内存


def _recv_request(conn: socket.socket) -> bytes:
    """读取一个完整 HTTP 请求（含 body）。

    TCP 是流式协议，一次 recv 不一定拿到完整报文，因此：
    1. 先循环读到出现头部结束标记 \\r\\n\\r\\n
    2. 解析 Content-Length
    3. 再继续读，直到 body 字节数够
    """
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            break  # 对端关闭
        data += chunk
        if len(data) > MAX_HEADER_SIZE:
            raise ValueError("请求头过大")

    if b"\r\n\r\n" not in data:
        return data  # 不完整，上层会当空/非法请求处理

    header_part, sep, body = data.partition(b"\r\n\r\n")
    content_length = 0
    # 只扫头部行，找 Content-Length（大小写不敏感）
    for line in header_part.decode("iso-8859-1").split("\r\n")[1:]:
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":", 1)[1].strip())
            except ValueError:
                content_length = 0
            break

    # POST/PUT 等可能有 body；GET 通常 Content-Length=0，循环不进入
    while len(body) < content_length:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            break
        body += chunk

    return header_part + sep + body[:content_length]


def _handle_connection(conn: socket.socket, addr: tuple[str, int], app: AppProtocol) -> None:
    """处理单个客户端连接（在独立线程中运行）。"""
    try:
        raw = _recv_request(conn)
        if not raw:
            return
        try:
            request = Request.from_raw(raw, client_addr=addr)
            response = app.handle(request)
        except ValueError as exc:
            # 请求行/头部非法 → 400
            response = text_response(f"Bad Request: {exc}", status=400)
        conn.sendall(response.to_bytes())
    except Exception as exc:  # noqa: BLE001
        # 读/写或未预期错误：尽量回一条 500，再关连接
        try:
            err = text_response(f"Internal Server Error: {exc}", status=500)
            conn.sendall(err.to_bytes())
        except OSError:
            pass
    finally:
        # 半关闭后再 close，避免对端仍在写时收到 RST
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        conn.close()


def serve(app: AppProtocol, host: str = "127.0.0.1", port: int = 8000) -> None:
    """阻塞式启动 TCP 服务器；每个连接在独立线程中处理。

    SO_REUSEADDR：进程退出后端口可立即再绑定（开发时常用）。
    daemon 线程：主线程 Ctrl+C 退出时，子线程随进程结束。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(128)  # 半连接/已连接队列长度
        print(f"Listening on {host}:{port} (Ctrl+C to stop)")
        try:
            while True:
                conn, addr = sock.accept()
                thread = threading.Thread(
                    target=_handle_connection,
                    args=(conn, addr, app),
                    daemon=True,
                )
                thread.start()
        except KeyboardInterrupt:
            print("\nServer stopped.")
