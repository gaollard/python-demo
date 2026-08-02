"""Human-in-the-loop：敏感工具执行前 interrupt，人工确认后再继续。

对比 06（middleware 管沙箱）/ 09（checkpointer 管记忆）：
- 06：ShellToolMiddleware 管「怎么执行」
- 09：MemorySaver 管「会话状态」
- 本示例：HumanInTheLoopMiddleware 在工具真正执行前调用 interrupt，
  图状态靠 checkpointer 挂起；人工通过 Command(resume=...) 决定
  approve / edit / reject 后继续

流程：
  阶段 A：查订单（安全工具）→ 不中断
  阶段 B：退款（敏感工具）→ interrupt → 人工 approve → 执行
  阶段 C：退款 → interrupt → 人工 reject → 不执行并反馈模型
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, Interrupt

load_dotenv()


@tool
def lookup_order(order_id: str) -> str:
    """查询订单状态（安全操作，无需人工确认）。

    Args:
        order_id: 订单号，如 ORD-1001
    """
    print(f"[tool] lookup_order({order_id!r})")
    catalog = {
        "ORD-1001": "已发货，金额 128.00 元",
        "ORD-1002": "处理中，金额 56.00 元",
    }
    return catalog.get(order_id.upper(), f"未找到订单 {order_id}")


@tool
def refund_order(order_id: str, amount: float) -> str:
    """发起退款（敏感操作：会改动资金，需人工确认后才执行）。

    Args:
        order_id: 订单号，如 ORD-1001
        amount: 退款金额（元）
    """
    print(f"[tool] refund_order({order_id!r}, {amount})")
    return f"已退款成功：订单 {order_id.upper()}，金额 {amount:.2f} 元"


def _print_reply(label: str, result: dict) -> None:
    print(f"\n--- {label} ---")
    print(result["messages"][-1].content)


def _get_interrupts(result: dict[str, Any]) -> list[Interrupt]:
    """v1 invoke：中断挂在结果的 __interrupt__ 上。"""
    return list(result.get("__interrupt__") or [])


def _print_hitl(interrupts: list[Interrupt]) -> None:
    print("\n[HITL] 执行已暂停，等待人工决策：")
    for i, intr in enumerate(interrupts):
        value = intr.value
        print(f"  interrupt[{i}] id={intr.id}")
        for j, action in enumerate(value.get("action_requests", [])):
            print(f"    action[{j}] name={action['name']}")
            print(f"              args={action['args']}")
            print(f"              desc={action.get('description', '')}")
        for cfg in value.get("review_configs", []):
            print(
                f"    review  action={cfg['action_name']} "
                f"allowed={cfg['allowed_decisions']}"
            )


def _invoke_until_refund_interrupt(agent, config: dict, first_user: str) -> dict:
    """催模型调用 refund_order，直到 HITL interrupt（最多再追问一轮）。"""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": first_user}]},
        config=config,
    )
    if _get_interrupts(result):
        return result

    # 有的模型会先查单就结束；再明确要求立刻调退款工具
    print("[demo] 尚未 interrupt，追加催促：立刻调用 refund_order")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "请立刻调用 refund_order 完成退款，"
                        "金额用刚才查到的订单金额，不要只口头确认。"
                    ),
                }
            ]
        },
        config=config,
    )
    return result


def _build_agent():
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0,
    )
    # HITL 必须挂 checkpointer：interrupt 把状态存起来，resume 才能续跑
    checkpointer = MemorySaver()
    return create_agent(
        model=llm,
        tools=[lookup_order, refund_order],
        checkpointer=checkpointer,
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    # False = 自动放行；未列出的工具默认也自动放行
                    "lookup_order": False,
                    "refund_order": {
                        "allowed_decisions": ["approve", "edit", "reject"],
                        "description": (
                            "敏感操作：退款会改动资金，请确认订单号与金额后再批准。"
                        ),
                    },
                },
                description_prefix="工具待人工确认",
            )
        ],
        system_prompt=(
            "你是客服助手。查订单必须调用 lookup_order；"
            "用户要退款时必须调用 refund_order（不要只口头答应）。"
            "退款金额按查到的订单金额填写。用简洁中文回答。"
        ),
    )


def main() -> None:
    agent = _build_agent()

    # ---------- 阶段 A：安全工具，不中断 ----------
    print("=" * 60)
    print("阶段 A：查订单（lookup_order）→ 应直接执行，无 interrupt")
    print("=" * 60)

    thread_safe = {"configurable": {"thread_id": "hitl-safe"}}
    r_safe = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "请查一下订单 ORD-1001 的状态。",
                }
            ]
        },
        config=thread_safe,
    )
    assert not _get_interrupts(r_safe), "安全工具不应触发 interrupt"
    _print_reply("阶段A · 查订单", r_safe)

    # ---------- 阶段 B：敏感工具 → approve ----------
    print("\n" + "=" * 60)
    print("阶段 B：退款（refund_order）→ interrupt → 人工 approve")
    print("=" * 60)

    thread_approve = {"configurable": {"thread_id": "hitl-approve"}}
    r_pause = _invoke_until_refund_interrupt(
        agent,
        thread_approve,
        "订单 ORD-1001 我要全额退款。请先查状态，再调用 refund_order。",
    )
    interrupts = _get_interrupts(r_pause)
    assert interrupts, "退款工具应触发 interrupt"
    _print_hitl(interrupts)

    # 模拟人工：批准原参数执行（生产里这里接审批 UI / 工单）
    print("\n[HITL] 人工决策: approve")
    r_ok = agent.invoke(
        Command(resume={"decisions": [{"type": "approve"}]}),
        config=thread_approve,
    )
    assert not _get_interrupts(r_ok), "approve 后续应跑完"
    _print_reply("阶段B · 批准后退款完成", r_ok)

    # ---------- 阶段 C：敏感工具 → reject ----------
    print("\n" + "=" * 60)
    print("阶段 C：退款 → interrupt → 人工 reject（不执行工具）")
    print("=" * 60)

    thread_reject = {"configurable": {"thread_id": "hitl-reject"}}
    r_pause2 = _invoke_until_refund_interrupt(
        agent,
        thread_reject,
        "订单 ORD-1002 请退款 56 元。请先查状态，再调用 refund_order。",
    )
    interrupts2 = _get_interrupts(r_pause2)
    assert interrupts2, "退款工具应触发 interrupt"
    _print_hitl(interrupts2)

    print("\n[HITL] 人工决策: reject")
    r_no = agent.invoke(
        Command(
            resume={
                "decisions": [
                    {
                        "type": "reject",
                        "message": (
                            "人工拒绝：该订单仍在处理中，暂不退款。"
                            "请告知用户稍后再试，不要再次调用 refund_order。"
                        ),
                    }
                ]
            }
        ),
        config=thread_reject,
    )
    assert not _get_interrupts(r_no), "reject 后续应跑完（模型用反馈作答）"
    _print_reply("阶段C · 拒绝后的助手回复", r_no)

    print("\n" + "=" * 60)
    print("要点: HumanInTheLoopMiddleware + interrupt_on 控制哪些工具要审批")
    print("      checkpointer + thread_id 保存挂起状态；Command(resume=) 续跑")
    print("      approve 执行原工具 / reject 不执行并回灌反馈 / edit 可改参数")
    print("=" * 60)


if __name__ == "__main__":
    main()
