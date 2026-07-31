# 07 · Plan-and-Execute

先**规划**完整步骤，再**逐步执行**，必要时**重规划**。

## 和 ReAct（02 / 03）的区别

| | ReAct | Plan-and-Execute |
|--|--------|------------------|
| 节奏 | 每轮：想一步 → 调工具 → 观察 | 先出整份计划，再按步执行 |
| 适合 | 路径不确定、需要边探边走 | 目标清晰、可拆成多步流水线 |
| 成本 | 步数多时反复「想」 | Planner / Replanner 调用少，Executor 可专注执行 |
| 风险 | 容易绕路或漏步骤 | 初始计划错了要靠 Replanner 纠正 |

```
用户目标
   │
   ▼
┌─────────┐
│ Planner │  →  steps = [步1, 步2, 步3, ...]
└────┬────┘
     ▼
┌──────────┐     ┌───────────┐
│ Executor │ ──► │ Replanner │──► 有最终答复？──是──► END
└──────────┘     └─────┬─────┘
     ▲                 │ 否：更新剩余 steps
     └─────────────────┘
```

## 三个角色

1. **Planner**：只规划，不调工具；输出结构化 `steps[]`
2. **Executor**：对本步做局部 ReAct（可调 `search_web` / `get_weather` / `estimate_budget`）
3. **Replanner**：看已完成结果，决定 `done` + 最终答复，或改写剩余计划

状态在 `PlanExecuteState`：`input` / `plan` / `past_steps` / `response`，用 LangGraph `StateGraph` 串起来。

## 运行

```bash
# 需已配置 DEEPSEEK_API_KEY（见仓库根或 llm-demo 的 .env）
cd llm-demo
./.venv/bin/python3 07-plan-and-excute/main.py
```

预期日志顺序：`[planner]` → 多次 `[executor]` + `[tool]` → `[replanner]` → 最终中文行程/预算答复。
