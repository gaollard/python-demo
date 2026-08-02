"""LangSmith Tracing + Eval：观测 Agent 调用链，并用小数据集打分。

对比此前 demo（终端 print / 肉眼看结果）：
- 之前：本地日志看 tool / messages，对不对靠人判断
- 本示例：LANGSMITH_TRACING 自动上报整条 run tree（LLM / tool / agent）；
  evaluate() 对同一批题批量跑，用规则打分看正确率

流程：
  阶段 A：开启 tracing，跑一次带工具的 Agent → 提示去 Smith UI 看 trace
  阶段 B：3 道题 evaluate（答案是否包含期望关键词）→ 打印正确率
         其中第 1 题 num_repetitions=2，演示「同一问题跑多次」
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langsmith import Client, evaluate, tracing_context
from langsmith.schemas import Example

load_dotenv()

PROJECT = os.getenv("LANGSMITH_PROJECT") or "llm-demo-12-langsmith"
DATASET_NAME = "llm-demo-12-order-lookup"


@tool
def lookup_order(order_id: str) -> str:
    """查询订单状态。

    Args:
        order_id: 订单号，如 ORD-1001
    """
    print(f"[tool] lookup_order({order_id!r})")
    catalog = {
        "ORD-1001": "已发货，预计明天送达",
        "ORD-1002": "处理中，尚未出库",
        "ORD-1003": "已取消",
    }
    return catalog.get(order_id.upper(), f"未找到订单 {order_id}")


def _build_agent():
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0,
    )
    return create_agent(
        model=llm,
        tools=[lookup_order],
        system_prompt=(
            "你是客服助手。查订单必须调用 lookup_order，不要编造状态。"
            "用简洁中文回答，并明确写出订单号与状态关键词。"
        ),
    )


def _print_reply(label: str, result: dict) -> None:
    print(f"\n--- {label} ---")
    print(result["messages"][-1].content)


def _require_deepseek() -> None:
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("缺少 DEEPSEEK_API_KEY，无法调用模型。", file=sys.stderr)
        sys.exit(1)


def _configure_langsmith() -> bool:
    """配置 tracing 环境变量。返回是否具备上传到 LangSmith 的条件。"""
    api_key = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGSMITH_PROJECT"] = PROJECT

    if not api_key:
        # 无 key 时关掉自动上传，避免 Client 报错刷屏
        os.environ["LANGSMITH_TRACING"] = "false"
        print(
            "[warn] 未设置 LANGSMITH_API_KEY：阶段 A 不上传 trace；"
            "阶段 B 走本地评估循环。\n"
            "      获取 key: https://smith.langchain.com/settings → API Keys\n"
            "      然后: export LANGSMITH_API_KEY=lsv2_...\n"
            f"           export LANGSMITH_TRACING=true\n"
            f"           export LANGSMITH_PROJECT={PROJECT}\n"
        )
        return False

    os.environ.setdefault("LANGSMITH_TRACING", "true")
    print(f"[langsmith] tracing=on  project={PROJECT}")
    return True


def _run_tracing_demo(agent, upload: bool) -> None:
    print("=" * 60)
    print("阶段 A：Tracing —— 跑一次 Agent，观察 LLM / tool 调用链")
    print("=" * 60)

    # tracing_context：即使全局未开 tracing，也可按块启用（有 key 时）
    with tracing_context(project_name=PROJECT, enabled=upload):
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "请查询订单 ORD-1001 的状态。",
                    }
                ]
            }
        )
    _print_reply("阶段A · 查 ORD-1001", result)

    if upload:
        print(
            f"\n[langsmith] 打开 https://smith.langchain.com → Projects → "
            f"「{PROJECT}」查看本次 run tree（agent / chat / tool）"
        )
    else:
        print("\n[langsmith] 跳过上传（无 API key）；本地仍完成了一次 Agent 调用")


def _answer_contains_keywords(
    inputs: dict,
    outputs: dict,
    reference_outputs: dict,
) -> dict:
    """规则评估器：助手回复是否包含全部期望关键词。"""
    answer = (outputs or {}).get("answer") or ""
    keywords = (reference_outputs or {}).get("must_contain") or []
    missing = [k for k in keywords if k not in answer]
    ok = not missing
    return {
        "key": "contains_keywords",
        "score": ok,
        "comment": "ok" if ok else f"missing={missing}",
    }


def _build_examples() -> list[Example]:
    """本地 Example 列表；evaluate(data=...) 需要 Example，不能只传裸 dict。"""
    now = datetime.now(timezone.utc)
    rows = [
        (
            {"question": "请查询订单 ORD-1001 的状态。"},
            {"must_contain": ["ORD-1001", "已发货"]},
        ),
        (
            {"question": "ORD-1002 现在怎样了？"},
            {"must_contain": ["ORD-1002", "处理中"]},
        ),
        (
            {"question": "帮我看一下 ORD-1003。"},
            {"must_contain": ["ORD-1003", "已取消"]},
        ),
    ]
    return [
        Example(id=uuid4(), inputs=inp, outputs=out, created_at=now)
        for inp, out in rows
    ]


def _ensure_remote_dataset(client: Client, examples: list[Example]) -> str:
    """有 API key 时：没有同名 dataset 就创建，便于在 UI 里复跑。"""
    existing = list(client.list_datasets(dataset_name=DATASET_NAME))
    if existing:
        print(f"[langsmith] 复用 dataset: {DATASET_NAME}")
        return DATASET_NAME

    ds = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="订单查询 Agent 评估集（llm-demo 12）",
    )
    client.create_examples(
        dataset_id=ds.id,
        examples=[
            {"inputs": e.inputs, "outputs": e.outputs} for e in examples
        ],
    )
    print(f"[langsmith] 已创建 dataset: {DATASET_NAME}")
    return DATASET_NAME


def _run_target(agent, inputs: dict) -> dict:
    """每道题独立会话，避免记忆串题。"""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": inputs["question"]}]}
    )
    return {"answer": result["messages"][-1].content}


def _print_eval_row(i: int, question: str, answer: str, score: bool, comment: str) -> None:
    flag = "PASS" if score else "FAIL"
    print(f"  [{flag}] #{i}  Q={question}")
    print(f"         A={answer[:80]}{'...' if len(answer) > 80 else ''}")
    if comment and comment != "ok":
        print(f"         {comment}")


def _local_eval(agent, examples: list[Example], repetitions: int) -> list[bool]:
    """无 API key 时：同一套 evaluator，本地循环（避免 evaluate 仍去上报 401）。"""
    scores: list[bool] = []
    print("\n[eval] 逐条结果（本地）:")
    i = 0
    for _ in range(repetitions):
        for example in examples:
            outputs = _run_target(agent, example.inputs or {})
            er = _answer_contains_keywords(
                example.inputs or {},
                outputs,
                example.outputs or {},
            )
            score = bool(er["score"])
            scores.append(score)
            _print_eval_row(
                i,
                (example.inputs or {}).get("question", "?"),
                outputs.get("answer", ""),
                score,
                er.get("comment", ""),
            )
            i += 1
    return scores


def _langsmith_eval(agent, examples: list[Example], repetitions: int) -> list[bool]:
    """有 API key：创建/复用 dataset + evaluate 上传 experiment。"""
    client = Client()
    data = _ensure_remote_dataset(client, examples)

    def target(inputs: dict) -> dict:
        return _run_target(agent, inputs)

    results = evaluate(
        target,
        data=data,
        evaluators=[_answer_contains_keywords],
        experiment_prefix="llm-demo-12-order-lookup",
        description="订单查询 Agent：关键词命中率",
        max_concurrency=0,
        num_repetitions=repetitions,
        client=client,
    )

    scores: list[bool] = []
    print("\n[eval] 逐条结果（LangSmith experiment）:")
    for i, row in enumerate(results):
        example = row.get("example")
        run = row.get("run")
        eval_results = (row.get("evaluation_results") or {}).get("results") or []
        q = "?"
        if example is not None and getattr(example, "inputs", None):
            q = (example.inputs or {}).get("question", "?")
        answer = ""
        if run is not None and getattr(run, "outputs", None):
            answer = (run.outputs or {}).get("answer", "")
        score = False
        comment = ""
        for er in eval_results:
            if getattr(er, "key", None) == "contains_keywords":
                score = bool(er.score)
                comment = getattr(er, "comment", "") or ""
                break
        scores.append(score)
        _print_eval_row(i, q, answer, score, comment)

    print(
        f"\n[langsmith] dataset「{DATASET_NAME}」→ Experiments 前缀 "
        f"「llm-demo-12-order-lookup」"
    )
    return scores


def _run_eval_demo(agent, upload: bool) -> None:
    print("\n" + "=" * 60)
    print("阶段 B：Eval —— 小数据集打分（含同一题重复跑）")
    print("=" * 60)

    examples = _build_examples()
    repetitions = 2  # 每题跑两遍，观察「同一问题多次」稳定性

    if upload:
        scores = _langsmith_eval(agent, examples, repetitions)
    else:
        scores = _local_eval(agent, examples, repetitions)
        print("\n[langsmith] 本地评估完成；配置 LANGSMITH_API_KEY 后会上传 experiment")

    if scores:
        hit = sum(scores)
        print(f"\n[eval] 正确率: {hit}/{len(scores)} = {hit / len(scores):.0%}")
        print(
            f"       （num_repetitions={repetitions} → "
            f"{len(examples)} 题 × {repetitions} = 最多 {len(examples) * repetitions} 条）"
        )


def main() -> None:
    _require_deepseek()
    upload = _configure_langsmith()
    agent = _build_agent()

    _run_tracing_demo(agent, upload=upload)
    _run_eval_demo(agent, upload=upload)

    print("\n" + "=" * 60)
    print("要点: LANGSMITH_TRACING + LANGSMITH_API_KEY → 自动上报 run tree")
    print("      LANGSMITH_PROJECT 决定落在哪个项目")
    print("      evaluate(target, data=examples, evaluators=[...]) → 批量打分")
    print("      num_repetitions 可对同一题多跑，观察稳定性")
    print("=" * 60)


if __name__ == "__main__":
    main()
