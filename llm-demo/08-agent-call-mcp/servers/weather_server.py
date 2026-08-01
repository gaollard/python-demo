"""本地 MCP Server：天气 / 汇率工具（stdio 传输）。

注意：stdio 模式下 stdout 专供 JSON-RPC，调试日志必须打到 stderr。
"""

import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)

# 模拟数据，便于演示 Agent 调用 MCP 工具
_WEATHER = {
    "tokyo": "东京：晴，24°C，湿度 55%，东南风 2 级",
    "东京": "东京：晴，24°C，湿度 55%，东南风 2 级",
    "singapore": "新加坡：多云，31°C，湿度 78%，阵雨概率 40%",
    "新加坡": "新加坡：多云，31°C，湿度 78%，阵雨概率 40%",
    "shanghai": "上海：阴，22°C，湿度 70%，东北风 3 级",
    "上海": "上海：阴，22°C，湿度 70%，东北风 3 级",
}

_FX = {
    ("USD", "CNY"): 7.24,
    ("CNY", "USD"): 0.138,
    ("USD", "JPY"): 150.2,
    ("JPY", "USD"): 0.00666,
}


@mcp.tool()
def get_weather(city: str) -> str:
    """查询城市当前天气（模拟数据）。

    Args:
        city: 城市名，如 东京 / Tokyo / 新加坡
    """
    _log(f"[mcp:weather] get_weather({city!r})")
    key = city.strip()
    if key in _WEATHER:
        return _WEATHER[key]
    lower = key.lower()
    for k, v in _WEATHER.items():
        if k.lower() == lower:
            return v
    return f"暂无「{city}」的天气数据，请换一个城市试试。"


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """按模拟汇率兑换货币。

    Args:
        amount: 金额
        from_currency: 源币种，如 USD / CNY / JPY
        to_currency: 目标币种，如 USD / CNY / JPY
    """
    _log(
        f"[mcp:weather] convert_currency({amount}, {from_currency!r}, {to_currency!r})"
    )
    src = from_currency.strip().upper()
    dst = to_currency.strip().upper()
    if src == dst:
        return f"{amount} {src} = {amount} {dst}"
    rate = _FX.get((src, dst))
    if rate is None:
        return f"不支持 {src} → {dst} 的汇率"
    result = round(amount * rate, 2)
    return f"{amount} {src} = {result} {dst}（汇率 {rate}）"


if __name__ == "__main__":
    mcp.run(transport="stdio")
