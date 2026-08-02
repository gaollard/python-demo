# 11 · Agent Human-in-the-loop

敏感工具执行前用 LangGraph `interrupt` 暂停，人工 `approve` / `reject` 后再继续。

## 和 06 / 09 的关系

| | 06 middleware | 09 checkpointer | 本示例 HITL |
|--|---------------|-----------------|-------------|
| 管什么 | 沙箱里怎么跑 shell | 多轮会话状态 | 工具执行前要不要人批 |
| 关键节点 | `ShellToolMiddleware` | `MemorySaver` | `HumanInTheLoopMiddleware` |
| 续跑方式 | 一次 `invoke` 跑完 | 同 `thread_id` 再 `invoke` | `Command(resume=...)` |

HITL **依赖 checkpointer**：`interrupt` 把图状态存住，审批后才能按同一 `thread_id` 恢复。

```
模型提出 tool_call
        │
        ▼
┌──────────────────────────┐
│ HumanInTheLoopMiddleware │  after_model：对照 interrupt_on
└────────────┬─────────────┘
             │ 敏感工具？
      否     │     是
      ▼      │      ▼
   直接执行  │   interrupt ──► 人工决策
             │      │
             │      ▼
             │  Command(resume={decisions:[...]})
             │      │
             └──────┴──► 继续跑图（执行 / 跳过 / 改参）
```

## 决策类型（本示例用到的）

| 决策 | 效果 |
|------|------|
| `approve` | 按模型原参数执行工具 |
| `reject` | 不执行；把 `message` 当 ToolMessage 反馈给模型 |
| `edit` | 改 `name` / `args` 后再执行（本示例未演示） |

## 运行

```bash
# 需已配置 DEEPSEEK_API_KEY
cd llm-demo
./.venv/bin/python3 11-agent-human-in-the-loop/main.py
```

预期：

1. 阶段 A：`lookup_order` 直接执行，无 `__interrupt__`
2. 阶段 B：`refund_order` 暂停 → 脚本模拟 `approve` → 打印 `[tool] refund_order...` → 成功答复
3. 阶段 C：再次退款暂停 → `reject` → 不出现退款 tool 日志 → 助手说明被拒原因
