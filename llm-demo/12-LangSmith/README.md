# 12 · LangSmith Tracing + Eval

把 Agent 的调用链上报到 LangSmith，并用小数据集做规则评估。

## 和此前 demo 的关系

| | 02–11 本地观察 | 本示例 LangSmith |
|--|----------------|------------------|
| 看什么 | 终端 `print` / assert | UI 里的 run tree + Experiment 表 |
| 对不对 | 肉眼看回复 | `evaluate` + evaluator 打分 |
| 稳定性 | 跑一遍就算 | `num_repetitions` 同一题多跑 |

```
Agent.invoke / evaluate(target)
        │
        ▼  LANGSMITH_TRACING=true
┌─────────────────┐
│ LangSmith Cloud │  Projects → 单次 trace（LLM / tool / agent）
│                 │  Experiments → 批量打分对比
└─────────────────┘
```

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `DEEPSEEK_API_KEY` | 是 | 调模型 |
| `LANGSMITH_API_KEY` | 建议 | 有则上传 trace / experiment；无则本地跑通 |
| `LANGSMITH_TRACING` | 建议 `true` | 开启自动追踪（脚本在有 key 时会 `setdefault`） |
| `LANGSMITH_PROJECT` | 可选 | 默认 `llm-demo-12-langsmith` |

API Key：[smith.langchain.com/settings](https://smith.langchain.com/settings) → **API Keys**。

```bash
export LANGSMITH_API_KEY=lsv2_...
export LANGSMITH_TRACING=true
export LANGSMITH_PROJECT=llm-demo-12-langsmith
```

## 两个阶段

1. **Tracing**：查 `ORD-1001` 一次。有 key 时到 UI 的 Projects 里看完整调用树。
2. **Eval**：3 道订单题 × `num_repetitions=2`，规则评估器检查回复是否包含订单号 + 状态关键词，终端打印正确率。

## 运行

```bash
cd llm-demo
./.venv/bin/python3 12-LangSmith/main.py
```

预期：

1. 阶段 A：打印 `[tool] lookup_order('ORD-1001')` 与助手回复
2. 阶段 B：多条 `PASS`/`FAIL`，最后一行正确率（理想 6/6）
3. 配置了 key 时：Smith UI 出现对应 Project / Experiment
