# 08 · Agent 调用 MCP

Agent 的工具不再用进程内 `@tool`，而是来自独立的 **MCP Server**。

## 和 02 / 03 的区别

| | 02 / 03 `@tool` | 本示例 MCP |
|--|------------------|------------|
| 工具位置 | 与 Agent 同一进程 | 独立子进程（stdio MCP Server） |
| 暴露方式 | LangChain `tool` 装饰器 | MCP `FastMCP` + `@mcp.tool()` |
| 接入方式 | 直接传给 `create_agent` | `MultiServerMCPClient.get_tools()` 再传入 |
| 好处 | 简单 | 工具可复用、可替换实现、可跨语言 |

```
用户问题
   │
   ▼
┌─────────┐   get_tools()    ┌──────────────────┐
│  Agent  │ ◄─────────────── │ MultiServerMCP   │
│(DeepSeek│  call tool       │ Client           │
└────┬────┘ ───────────────► └────────┬─────────┘
     │                                │ stdio
     │                     ┌──────────┴──────────┐
     │                     ▼                     ▼
     │              math_server.py        weather_server.py
     │              add/multiply/divide   get_weather/convert_currency
     ▼
  中文最终答复
```

## 目录

- `main.py` — Agent 客户端：连 MCP、建 Agent、提问
- `servers/math_server.py` — 数学 MCP Server
- `servers/weather_server.py` — 天气 / 汇率 MCP Server

## 依赖

已在 `llm-demo/.venv` 中安装：

```bash
pip install langchain-mcp-adapters 'mcp>=1.24,<2'
```

> 注意：当前 `langchain-mcp-adapters` 与 `mcp 2.x` 不兼容，请使用 `mcp 1.x`。

## 运行

```bash
# 需已配置 DEEPSEEK_API_KEY
cd llm-demo
./.venv/bin/python3 08-agent-call-mcp/main.py
```

预期日志：先打印「已从 MCP 加载 N 个工具」，再出现 `[mcp:math]` / `[mcp:weather]` 调用痕迹，最后给出中文答复。
