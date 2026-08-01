"""Checkpoint 持久化：用 SqliteSaver 让多轮记忆跨进程存活。

对比 09（MemorySaver，进程内）：
- 09：checkpointer 在内存；进程退出 → 历史全丢
- 本示例：SqliteSaver 写入本地 .db；关掉连接 / 重启进程后，
  同一 thread_id 仍能加载历史

流程：
  阶段 A：写入自我介绍 → 关闭 SQLite 连接（模拟进程退出）
  阶段 B：重新打开同一 .db → 同 thread_id 追问「我叫什么？」
  阶段 C：换 thread_id → 新会话无记忆
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

# 与脚本同目录，方便观察 / 删除
DB_PATH = Path(__file__).resolve().parent / "checkpoints.sqlite"


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
    """查询订单状态（演示：持久化记忆与工具可同时使用）。

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


def _build_agent(checkpointer: SqliteSaver):
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.2,
    )
    return create_agent(
        model=llm,
        tools=[lookup_order],
        checkpointer=checkpointer,
        system_prompt=(
            "你是客服助手。记住用户在本会话中说过的信息；"
            "查订单请用 lookup_order 工具。用简洁中文回答。"
        ),
    )


def main() -> None:
    thread_a = {"configurable": {"thread_id": "user-alice"}}
    thread_b = {"configurable": {"thread_id": "user-bob"}}

    print("=" * 60)
    print(f"阶段 A：写入记忆 → 落盘 {DB_PATH.name}")
    print("=" * 60)

    # from_conn_string 是 contextmanager：退出 with 即关闭连接（≈ 进程退出）
    with SqliteSaver.from_conn_string(str(DB_PATH)) as checkpointer:
        agent = _build_agent(checkpointer)
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
        _print_reply("阶段A · 写入（thread=alice）", r1)

    print(f"\n[persist] 已关闭 SQLite 连接；文件仍在: {DB_PATH}")
    print("[persist] 若用 MemorySaver，此刻历史已丢；SqliteSaver 仍可读回\n")

    print("=" * 60)
    print("阶段 B：重新打开同一 .db（模拟进程重启）")
    print("=" * 60)

    with SqliteSaver.from_conn_string(str(DB_PATH)) as checkpointer:
        agent = _build_agent(checkpointer)

        # 新进程 / 新 agent 实例，但同 thread_id → 应从 .db 加载历史
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
        _print_reply("阶段B · 重启后续聊（应记住姓名/订单并调工具）", r2)

        print("\n" + "=" * 60)
        print("阶段 C：换 thread_id → 新会话，不应知道小明")
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
        _print_reply("阶段C · thread=bob（应表示不知道）", r3)

    print("\n" + "=" * 60)
    print("要点: SqliteSaver + 相同 thread_id → 跨进程多轮记忆")
    print("      MemorySaver 只活在进程内；生产可再换 PostgresSaver")
    print(f"      本地库文件: {DB_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
