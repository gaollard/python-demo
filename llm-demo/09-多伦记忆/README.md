# 09 · 多轮记忆 / Checkpoint

用 **Checkpointer** 让 Agent 在同一会话里跨轮记住对话；不同 `thread_id` 互不干扰。

## 和 02 的区别

| | 02 单次 Agent | 本示例 |
|--|---------------|--------|
| 状态 | 无；每次只看当次 `messages` | `MemorySaver` 持久化图状态 |
| 多轮 | 需自己把历史拼进 `messages` | 同一 `thread_id` 自动加载历史 |
| 隔离 | — | 换 `thread_id` = 新会话 |

```
轮次 N 的 messages（仅新用户话）
        │
        ▼
┌─────────────────┐   thread_id=alice    ┌──────────────┐
│ create_agent    │ ◄─────────────────── │ MemorySaver  │
│ + checkpointer  │  加载历史 / 写回新状态 │ （内存）      │
└────────┬────────┘                      └──────────────┘
         ▼
   模型看到：历史 + 本轮 → 回复
```

## 两个概念

1. **checkpointer**：存「这个图跑到哪、messages 有哪些」
2. **thread_id**：会话主键；相同 = 续聊，不同 = 隔离

`MemorySaver` 只在进程内存里；进程退出即丢。生产可换 `SqliteSaver` / `PostgresSaver`。

## 运行

```bash
# 需已配置 DEEPSEEK_API_KEY
cd llm-demo
./.venv/bin/python3 09-多伦记忆/main.py
```

预期：

1. 轮次 1：记下「小明 / ORD-1001」
2. 轮次 2（同 thread）：答出姓名与订单，并调用 `lookup_order`
3. 轮次 3（新 thread）：不知道小明是谁
