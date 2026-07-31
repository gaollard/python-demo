# Plan-and-Execute vs ReAct

核心区别：**节奏不同**——ReAct 是「边想边做」，Plan-and-Execute 是「先整份计划，再按步执行」。

## 对比表

| | ReAct（02 / 03） | Plan-and-Execute（本 demo） |
|--|------------------|----------------------------|
| 节奏 | 每轮：想一步 → 调工具 → 观察 → 再想 | 先出完整 `steps[]`，再逐步执行，必要时重规划 |
| 计划与执行 | 交织在一起 | 分离：Planner / Executor / Replanner |
| 适合 | 路径不确定、需要边探边走 | 目标清晰、可拆成多步流水线 |
| 成本 | 步数多时反复「想」 | Planner / Replanner 调用少，Executor 可专注执行 |
| 风险 | 容易绕路或漏步骤 | 初始计划错了，要靠 Replanner 纠正 |

## 流程对比

```
ReAct:
  想 → 做 → 看 → 想 → 做 → 看 → … → 答

Plan-and-Execute:
  Planner 出整份计划
       ↓
  Executor 执行当前步（内部可再做局部 ReAct）
       ↓
  Replanner：够了就答 / 不够就改剩余 steps，再回 Executor
```

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

## Plan-and-Execute 三个角色

1. **Planner**：只规划，不调工具；输出结构化 `steps[]`
2. **Executor**：对本步做局部 ReAct（可调 `search_web` / `get_weather` / `estimate_budget`）
3. **Replanner**：看已完成结果，决定 `done` + 最终答复，或改写剩余计划

状态在 `PlanExecuteState`：`input` / `plan` / `past_steps` / `response`，用 LangGraph `StateGraph` 串起来。

## 哪种更好？

没有绝对更好，取决于任务形态：

- **选 ReAct**：目标模糊、要边查边决策、步骤事先不好拆（排障、开放式搜索）
- **选 Plan-and-Execute**：目标清楚、步骤可预估（行程、调研报告、多工具流水线），能少绕路、结构更稳

实操建议：路径不清先用 ReAct；能一眼拆成 3～5 步再用 Plan-and-Execute，并保留 Replanner。

## 两种能混合吗？

能，而且本 demo 已经在混用：**外层 Plan-and-Execute，内层 ReAct**。

1. **Planner** 先定整份步骤
2. **Executor** 对每一步用带工具的 agent（局部 ReAct：想 → 调工具 → 观察）
3. **Replanner** 再决定继续、改计划或收工

`main.py` 里 Executor 就是 `create_agent(...)`，每步内部可多次调 `search_web` / `get_weather` / `estimate_budget`。

| 层级 | 模式 | 管什么 |
|------|------|--------|
| 外层 | Plan-and-Execute | 目标拆解、进度、是否收工 |
| 内层 | ReAct | 单步里怎么调工具、应对不确定信息 |

也可以反过来：整体 ReAct 跑，中间某几步再嵌套「先规划再执行」——较少见，适合特别重的子任务。

混合很常见：外层规划控大局，内层 ReAct 处理单步细节。

## 一句话

ReAct 像边走边问路；Plan-and-Execute 像先画路线图再走，走偏了再改图；生产里常两者叠用。
