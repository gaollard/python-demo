"""多轮记忆示例：用 Checkpointer 让 Agent 跨轮记住对话。

对比 02（单次 invoke，无状态）：
- 02：每次 invoke 只带当前 messages，上一轮内容不会自动回来
- 本示例：create_agent(checkpointer=MemorySaver())，同一 thread_id
  下历史消息由 checkpointer 自动拼接；换 thread_id 则互不干扰

流程：
  轮次 1（thread=A）→ 自我介绍
  轮次 2（thread=A）→ 「我叫什么？」应能答出
  轮次 3（thread=B）→ 同样问法，新会话无记忆
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


class PrintPromptHandler(BaseCallbackHandler):
    """打印每次真正发给 LLM 的完整 messages（含 system + 历史）。"""

    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("\n===== LLM input messages =====")
        for batch in messages:
            for m in batch:
                print(f"[{m.type}] {m.content}")
        print("===== end =====\n")


@tool
def lookup_order(order_id: str) -> str:
    """查询订单状态（演示：记忆与工具可同时使用）。

    Args:
        order_id: 订单号，如 ORD-1001
    """
    print(f"[tool] lookup_order({order_id!r})")
    catalog = {
        "ORD-1001": "已发货，预计明天送达",
        "ORD-1002": "处理中，尚未出库",
    }
    return catalog.get(order_id.upper(), f"未找到订单 {order_id}")


def _print_reply(label: str, result: dict) -> None:
    print(f"\n--- {label} ---")
    print(result["messages"][-1].content)


def _with_prompt_logger(thread_config: dict) -> dict:
    return {**thread_config, "callbacks": [PrintPromptHandler()]}


def main() -> None:
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.2,
    )

    # MemorySaver：进程内内存 checkpoint；进程退出即丢。
    # 生产可换成 SqliteSaver / PostgresSaver 做持久化。
    checkpointer = MemorySaver()

    agent = create_agent(
        model=llm,
        tools=[lookup_order],
        checkpointer=checkpointer,
        system_prompt=(
            "你是客服助手。记住用户在本会话中说过的信息；"
            "查订单请用 lookup_order 工具。用简洁中文回答。"
        ),
    )

    # 同一 thread_id = 同一会话；config 必须带 configurable.thread_id
    thread_a = {"configurable": {"thread_id": "user-alice"}}
    thread_b = {"configurable": {"thread_id": "user-bob"}}

    print("=" * 60)
    print("同一 thread_id：多轮应能记住上下文")
    print("=" * 60)

    r1 = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "你好，我叫小明，我的订单号是 ORD-1001。",
                }
            ]
        },
        config=_with_prompt_logger(thread_a),
    )
    _print_reply("轮次1 · thread=alice", r1)

    # 本轮只发新消息；历史由 checkpointer 按 thread_id 自动加载
    r2 = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "我叫什么？订单号又是多少？请查一下订单状态。",
                }
            ]
        },
        config=_with_prompt_logger(thread_a),
    )
    _print_reply("轮次2 · thread=alice（应记住姓名/订单并调工具）", r2)

    print("\n" + "=" * 60)
    print("换 thread_id：新会话，不应知道小明的信息")
    print("=" * 60)

    r3 = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "我叫什么？我的订单号是多少？",
                }
            ]
        },
        config=_with_prompt_logger(thread_b),
    )
    _print_reply("轮次3 · thread=bob（应表示不知道）", r3)

    print("\n" + "=" * 60)
    print("要点: checkpointer + 相同 thread_id → 多轮记忆")
    print("      换 thread_id → 会话隔离")
    print("=" * 60)


if __name__ == "__main__":
    main()
