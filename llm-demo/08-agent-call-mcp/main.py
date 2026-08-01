"""Agent 调用 MCP 工具示例。

对比 02/03（工具写在进程内 @tool）：
- 本示例工具跑在独立 MCP Server 进程里（stdio）
- Agent 通过 langchain-mcp-adapters 把 MCP tools 转成 LangChain tools
- 模型仍用 create_agent + DeepSeek，只是工具来源换成 MCP

流程：
  main.py
    → MultiServerMCPClient 拉起 math / weather 两个 MCP Server
    → get_tools() 拿到工具列表
    → create_agent(tools=...) 让模型按需调用
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()

DIR = Path(__file__).resolve().parent
PYTHON = sys.executable  # 用当前 venv 的 python 拉起 MCP Server


async def main() -> None:
    # 两个本地 MCP Server，均走 stdio；client 会按需启动子进程
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": PYTHON,
                "args": [str(DIR / "servers" / "math_server.py")],
            },
            "weather": {
                "transport": "stdio",
                "command": PYTHON,
                "args": [str(DIR / "servers" / "weather_server.py")],
            },
        }
    )

    tools = await client.get_tools()
    print("=" * 60)
    print(f"已从 MCP 加载 {len(tools)} 个工具:")
    for t in tools:
        print(f"  - {t.name}: {t.description.splitlines()[0] if t.description else ''}")
    print("=" * 60)

    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.2,
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "你是助手。计算请用 math 工具（add / multiply / divide），"
            "查天气用 get_weather，换汇用 convert_currency。"
            "不要心算或编造汇率/天气；最后用简洁中文回答。"
        ),
    )

    user_query = (
        "请依次完成：\n"
        "1. 用工具计算 (120 + 80) × 1.5\n"
        "2. 查询东京天气\n"
        "3. 把第 1 步算出的金额按 USD 换成 CNY\n"
        "最后汇总三步结果。"
    )
    print("用户:", user_query)

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_query}]}
    )

    print("\n" + "=" * 60)
    print("最终回复:")
    print(result["messages"][-1].content)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
