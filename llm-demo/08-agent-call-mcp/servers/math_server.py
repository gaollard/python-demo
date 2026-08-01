"""本地 MCP Server：数学工具（stdio 传输）。

注意：stdio 模式下 stdout 专供 JSON-RPC，调试日志必须打到 stderr。
"""

import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


@mcp.tool()
def add(a: float, b: float) -> float:
    """两数相加。

    Args:
        a: 第一个数
        b: 第二个数
    """
    _log(f"[mcp:math] add({a}, {b})")
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """两数相乘。

    Args:
        a: 第一个数
        b: 第二个数
    """
    _log(f"[mcp:math] multiply({a}, {b})")
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """两数相除。

    Args:
        a: 被除数
        b: 除数（不能为 0）
    """
    _log(f"[mcp:math] divide({a}, {b})")
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b


if __name__ == "__main__":
    mcp.run(transport="stdio")
