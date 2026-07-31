"""Plan-and-Execute 示例：先规划完整步骤，再逐步执行，必要时重规划。

对比 02/03 的 ReAct（每步边想边调工具）：
- ReAct：思考 → 行动 → 观察 → 再思考……（计划与执行交织）
- Plan-and-Execute：Planner 先产出多步计划 → Executor 逐步执行 →
  Replanner 根据结果决定「继续 / 改计划 / 收工」

本示例用 LangGraph 把三个角色串成状态机。
"""

from __future__ import annotations

import operator
import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

load_dotenv()


# ---------- 模拟工具（Executor 专用） ----------
@tool
def search_web(query: str) -> str:
    """搜索公开信息（天气、景点、交通等）。

    Args:
        query: 搜索关键词
    """
    print(f"[tool] search_web({query!r})")
    q = query.lower()
    if "东京" in query or "tokyo" in q:
        return (
            "东京：春季（3-5 月）温暖，赏樱季；地铁发达；"
            "热门：浅草寺、涩谷、台场。人均日消费约 150-250 USD。"
        )
    if "大阪" in query or "osaka" in q:
        return (
            "大阪：美食之都，道顿堀、环球影城；"
            "与京都新干线约 15 分钟。人均日消费约 120-200 USD。"
        )
    if "京都" in query or "kyoto" in q:
        return (
            "京都：寺庙神社众多（清水寺、伏见稻荷）；"
            "春秋最宜，夏季湿热。建议预留 2 天。"
        )
    if "汇率" in query or "日元" in query:
        return "参考汇率：1 USD ≈ 150 JPY；1 CNY ≈ 21 JPY。"
    return f"未找到与「{query}」高度相关的结果，请换关键词。"


@tool
def get_weather(city: str, month: str) -> str:
    """查询某城市某月的典型天气。

    Args:
        city: 城市名
        month: 月份，如 4 或 April
    """
    print(f"[tool] get_weather(city={city!r}, month={month!r})")
    data = {
        ("东京", "4"): "平均 15°C，偶有小雨，适合赏樱，带薄外套",
        ("大阪", "4"): "平均 16°C，晴间多云，适合步行观光",
        ("京都", "4"): "平均 14°C，早晚凉，寺庙区可能湿润",
    }
    key = (city.replace("市", ""), month.replace("月", ""))
    return data.get(key, f"{city} {month} 月：温和，建议查询当地预报。")


@tool
def estimate_budget(days: int, daily_usd: float, people: int = 1) -> str:
    """估算旅行总预算（美元）。

    Args:
        days: 天数
        daily_usd: 人均每日花费（USD）
        people: 人数
    """
    print(f"[tool] estimate_budget(days={days}, daily_usd={daily_usd}, people={people})")
    total = days * daily_usd * people
    return f"估算：{people} 人 × {days} 天 × ${daily_usd}/天 = ${total:.0f} USD"


TOOLS = [search_web, get_weather, estimate_budget]


# ---------- 结构化输出 ----------
class Plan(BaseModel):
    """多步执行计划。"""

    steps: list[str] = Field(description="按顺序排列的具体步骤，每步可独立执行")


class FinalAnswer(BaseModel):
    """任务已完成时的最终答复。"""

    response: str = Field(description="给用户的完整中文答复")


class ReplanResult(BaseModel):
    """重规划结果：要么继续执行剩余步骤，要么给出最终答复。"""

    done: bool = Field(description="True 表示已有足够信息可回答用户")
    steps: list[str] = Field(
        default_factory=list,
        description="若未完成：剩余待执行步骤；若已完成可为空",
    )
    response: str = Field(
        default="",
        description="若 done=True：最终中文答复；否则为空",
    )


# ---------- 图状态 ----------
class PlanExecuteState(TypedDict):
    input: str
    plan: list[str]
    past_steps: Annotated[list[tuple[str, str]], operator.add]
    response: str


# ---------- 模型 ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2,
)

# DeepSeek 不支持 response_format/json_schema，用 function_calling 拿结构化结果
planner_llm = llm.with_structured_output(Plan, method="function_calling")
replanner_llm = llm.with_structured_output(ReplanResult, method="function_calling")

# Executor：每一步用带工具的 agent 完成（局部 ReAct）
executor = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=(
        "你是执行助手。只完成用户给出的「当前步骤」，"
        "必要时调用工具获取事实，最后用简洁中文汇报本步结果。"
        "不要擅自做后续步骤。"
    ),
)


# ---------- 节点 ----------
def plan_node(state: PlanExecuteState) -> dict:
    """Planner：根据用户目标生成完整步骤列表。"""
    prompt = (
        "为下面的目标制定清晰、可执行的分步计划。\n"
        "要求：\n"
        "1. 一共 3～5 步，不要拆得过细\n"
        "2. 每一步应具体到可调用搜索/天气/预算工具完成\n"
        "3. 可把「查天气」「查景点」「估预算」等合并进同一步\n"
        "4. 不要执行，只规划\n\n"
        f"目标：{state['input']}"
    )
    plan: Plan = planner_llm.invoke([HumanMessage(content=prompt)])
    print("\n[planner] 计划步骤:")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. {step}")
    return {"plan": plan.steps}


def execute_node(state: PlanExecuteState) -> dict:
    """Executor：执行计划中的第一步。"""
    plan = state["plan"]
    if not plan:
        return {"past_steps": []}

    task = plan[0]
    print(f"\n[executor] 执行: {task}")

    # 把已完成步骤摘要塞进上下文，便于本步引用
    history = ""
    if state.get("past_steps"):
        history = "\n已完成步骤:\n" + "\n".join(
            f"- {s}: {r}" for s, r in state["past_steps"]
        )

    result = executor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"原始目标：{state['input']}\n"
                        f"{history}\n\n"
                        f"请只完成当前步骤：{task}"
                    ),
                }
            ]
        }
    )
    observation = result["messages"][-1].content
    print(f"[executor] 结果: {observation[:200]}...")

    # 弹出已执行的第一步，剩余步骤留给 replanner 决定是否保留
    return {
        "past_steps": [(task, observation)],
        "plan": plan[1:],
    }


def replan_node(state: PlanExecuteState) -> dict:
    """Replanner：根据已执行结果决定继续、改计划或结束。"""
    past = "\n".join(f"- {s}: {r}" for s, r in state["past_steps"])
    remaining = "\n".join(f"- {s}" for s in state["plan"]) or "（无）"
    prompt = (
        "你是重规划器。根据目标与已完成步骤，判断是否已能回答用户。\n"
        "- 若已足够：done=true，填写 response（完整中文答复），steps 置空。\n"
        "- 若还需继续：done=false，给出更新后的剩余 steps"
        "（可改写/增删，不要重复已完成的工作）。\n\n"
        f"目标：{state['input']}\n\n"
        f"已完成：\n{past}\n\n"
        f"原剩余计划：\n{remaining}"
    )
    result: ReplanResult = replanner_llm.invoke([HumanMessage(content=prompt)])
    if result.done:
        print("\n[replanner] 完成，生成最终答复")
        return {"response": result.response, "plan": []}
    print("\n[replanner] 更新剩余计划:")
    for i, step in enumerate(result.steps, 1):
        print(f"  {i}. {step}")
    return {"plan": result.steps}


MAX_STEPS = 6  # 防止重规划死循环


def should_end(state: PlanExecuteState) -> Literal["execute", "__end__"]:
    if state.get("response"):
        return "__end__"
    if not state.get("plan"):
        return "__end__"
    if len(state.get("past_steps", [])) >= MAX_STEPS:
        return "__end__"
    return "execute"


# ---------- 组装图 ----------
graph = StateGraph(PlanExecuteState)
graph.add_node("planner", plan_node)
graph.add_node("execute", execute_node)
graph.add_node("replan", replan_node)

graph.add_edge(START, "planner")
graph.add_edge("planner", "execute")
graph.add_edge("execute", "replan")
graph.add_conditional_edges("replan", should_end, {"execute": "execute", "__end__": END})

app = graph.compile()


# ---------- 运行 ----------
USER_QUERY = (
    "我想 4 月去日本玩 5 天，主要看东京和京都。"
    "请帮我查两地 4 月天气、大致行程要点，并估算 2 人总预算（美元）。"
)

if __name__ == "__main__":
    print("=" * 60)
    print("用户目标:", USER_QUERY)
    print("=" * 60)

    final = app.invoke(
        {
            "input": USER_QUERY,
            "plan": [],
            "past_steps": [],
            "response": "",
        }
    )

    print("\n" + "=" * 60)
    print("最终答复:")
    response = final.get("response")
    if not response and final.get("past_steps"):
        # 触达步数上限时，用已完成步骤拼一份简报
        response = "（达到最大步数，以下为已收集信息）\n" + "\n".join(
            f"### {s}\n{r}" for s, r in final["past_steps"]
        )
    print(response or "(无最终答复)")
    print("=" * 60)
    print(f"共执行步骤数: {len(final.get('past_steps', []))}")
