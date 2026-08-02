# llm-demo 待实践知识点

已完成：`01` LCEL → `02/03` ReAct → `04/05` Skill → `06` Sandbox → `07` Plan-and-Execute → `08` MCP → `09` 多轮记忆 → `10` Checkpoint 持久化 → `11` HITL → `12` LangSmith。

## 优先（承接现有 demo）

| 序号 | 主题 | 练什么 | 为什么接得上 | 状态 |
|------|------|--------|--------------|------|
| 09 | 多轮记忆 / Checkpoint | `MemorySaver`，同一 `thread_id` 多轮对话 | 02–08 基本都是单次 `invoke`，缺状态 | ✅ `09-多伦记忆/` |
| 10 | Checkpoint 持久化 | `SqliteSaver` 落盘；关连接 / 重启后同 `thread_id` 仍能续聊 | 接 09：换 checkpointer 实现，API 不变 | ✅ `10-多伦记忆-checkpoint持久化/` |
| 11 | Human-in-the-loop | LangGraph `interrupt`：敏感操作前人工确认再继续 | 接 06 middleware、07 状态机 | ✅ `11-agent-human-in-the-loop/` |
| 12 | LangSmith Tracing / Eval | `LANGSMITH_TRACING` 上报 run tree；`evaluate` + 规则打分 | 此前只靠终端肉眼看，缺观测与批量评估 | ✅ `12-LangSmith/` |
| 13 | 结构化输出 | `with_structured_output` / Pydantic，强制 JSON Schema | 07 已有 Planner schema，可单独拆成最小 demo | 待做 |
| 14 | Streaming | `astream` / token 流 / 工具调用事件流 | 生产里几乎必备，现有 demo 都是整包返回 | 待做 |
| 15 | RAG + Agent | 本地文档切块 → 向量检索 tool → Agent 问答 | 和 03 多工具、04 Skill 互补 | 待做 |

## 进阶（系统感更强）

| 主题 | 练什么 |
|------|--------|
| Multi-Agent | Supervisor / 路由：调研员 + 写手 + 审核，用 LangGraph 拼 |
| MCP 进阶 | SSE/HTTP transport、Resources、Prompts（08 只做了 stdio Tools） |
| Tool 容错 | 超时、重试、错误回传模型再试 |
| 路由链 | 分类器决定走「闲聊 / 查库 / 写代码」，不用每次上完整 Agent |

## 建议顺序

`09 记忆` → `10 持久化` → `11 HITL` → `12 LangSmith` → `14 Streaming` → `13 结构化输出` → `15 RAG` → `Multi-Agent`
