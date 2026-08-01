# 10 · 多轮记忆 / Checkpoint 持久化

用 **SqliteSaver** 把 checkpoint 落到本地 `.db`，进程退出后仍能按 `thread_id` 续聊。

## 和 09 的区别

| | 09 `MemorySaver` | 本示例 `SqliteSaver` |
|--|------------------|----------------------|
| 存储 | 进程内存 | 本地 SQLite 文件 |
| 进程退出 | 历史丢失 | 历史仍在 |
| 适用 | 快速 demo / 单测 | 本地工具、单机原型 |

```
阶段 A（进程 1）                阶段 B（进程 2 / 重开连接）
  用户自我介绍                      只发「我叫什么？」
        │                                 │
        ▼                                 ▼
┌──────────────┐   写入        ┌──────────────────┐
│ create_agent │ ───────────► │ checkpoints.sqlite│
│ + SqliteSaver│ ◄─────────── │ （落盘，可重启）   │
└──────────────┘   按 thread 读 └──────────────────┘
```

## 两个概念（承接 09）

1. **checkpointer**：存图状态；实现可换（内存 / SQLite / Postgres）
2. **thread_id**：会话主键；相同 = 续聊，不同 = 隔离

本示例额外证明：**换 checkpointer 实现，API 不变**——仍是 `create_agent(checkpointer=...)` + `config.configurable.thread_id`。

## 依赖

```bash
pip install langgraph-checkpoint-sqlite
```

## 运行

```bash
# 需已配置 DEEPSEEK_API_KEY
cd llm-demo
./.venv/bin/python3 10-多伦记忆-checkpoint持久化/main.py
```

预期：

1. 阶段 A：记下「小明 / ORD-1001」，关闭连接
2. 阶段 B：重开同一 `.db`，同 `thread_id` 仍答出姓名/订单并调 `lookup_order`
3. 阶段 C：换 `thread_id`，不知道小明

运行后同目录会生成 `checkpoints.sqlite`（可删；再跑会重新写入）。
