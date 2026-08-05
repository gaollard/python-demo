# Code Wiki — AI Technical Design

## 1. 背景与目标

### 1.1 产品目标

Code Wiki 是一个**代码分析 Agent**：用户提供工作空间路径与自然语言问题后，Agent 自主检索、阅读相关代码，并给出带引用的回答。

### 1.2 成功标准（MVP）

| 场景 | 期望行为 |
|------|----------|
| 「XXX 在哪里实现？」 | 定位到文件/函数，给出路径与关键片段 |
| 「YYY 流程怎么走？」 | 沿调用链说明步骤，引用关键代码 |
| 「这个仓库大致结构？」 | 概述目录与核心模块 |
| 「这段是谁改的 / 何时引入？」 | 用只读 git 工具（blame/log）给出提交与作者线索 |

验收：CLI 可运行；可见 tool 调用轨迹；回答含 `path:line` 引用。

### 1.3 非目标（MVP 不做）

- 修改/提交代码（`commit` / `push` / `checkout` 写操作等）
- 任意 shell（`run_shell`）；git 仅以**白名单只读子命令**提供（见 §5.3）
- 多用户 SaaS、权限体系
- 完整 IDE 插件
- 自动生成并持久化全库 Wiki 页面（可作为后续增强）

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│  Interface                                                   │
│  CLI (typer)  /  后续: HTTP API                              │
└───────────────────────────┬─────────────────────────────────┘
                            │ workspace + question
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Agent Orchestrator                                          │
│  - System Prompt                                             │
│  - ReAct / Tool-calling Loop                                 │
│  - max_steps / token 预算                                    │
└───────────────────────────┬─────────────────────────────────┘
                            │ tool_calls
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Tool Layer                                                  │
│  list_dir │ glob │ grep │ read_file │ find_def/refs │ git_* │ (+语义) │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Safety & IO / Index                                         │
│  路径沙箱 │ 忽略 │ 截断 │ rg │ git 只读白名单 │ 符号索引        │
└─────────────────────────────────────────────────────────────┘
```

设计原则：

1. **不整库塞入上下文** — 靠多轮工具调用缩小范围。
2. **工具最小可用** — MVP 文件系统 + grep + **只读 git**；**符号导航优先于全文**（P1+）；图谱/语义为增强。
3. **路径沙箱** — 所有路径必须解析到 workspace 内；git 在 repo 根执行且禁止写操作。

---

## 3. 核心流程

```
1. 校验 workspace 存在且为目录
2. 构造 messages = [system, user(question + workspace)]
3. for step in 1..max_steps:
     a. 调用 LLM（带 tools schema）
     b. 若有 tool_calls → 执行 → append tool results → continue
     c. 若无 tool_calls → 将 content 作为最终回答返回
4. 若耗尽 max_steps → 基于已有上下文强制总结或返回超时提示
```

### 3.1 Agent 策略（写入 System Prompt）

1. 先用 `list_dir` / `glob` 了解结构  
2. **符号优先**：已知/可推断符号名时，优先 `find_definition` / `find_references`；全文 `grep` 作兜底（见 §5.2）  
3. 用 `read_file` **分层阅读**：大文件先 `outline`，再 `symbol` / 区间 `body`（见 §5.1）  
4. 涉及「谁改的 / 何时引入 / 近期变更」时用只读 **git 工具**（见 §5.3），勿臆造提交历史  
5. 必要时沿调用链 / 引用继续搜索  
6. 用清晰结构回答，并给出 `文件路径:行号`（及可选 commit）引用  

### 3.2 并行 Tool Calls

模型在**同一轮**可能返回多个 `tool_calls`（例如同时 `grep` 两个关键词、或并行 `read_file` 多个候选文件）。这些调用彼此**无依赖**时，应并行执行以降低端到端延迟。

#### 行为约定

| 项 | 约定 |
|----|------|
| 触发条件 | 单次 `LLMResponse.tool_calls` 长度 > 1 |
| 执行方式 | `concurrent.futures.ThreadPoolExecutor`（或 `asyncio.gather`）并行跑各 tool |
| 结果顺序 | **按原始 `tool_calls` 顺序**写回 messages（OpenAI 要求 `tool` 消息与 `tool_call_id` 对应，顺序建议保持稳定） |
| 失败隔离 | 单个 tool 异常 → 该 call 返回错误字符串，不影响同轮其他 call |
| 并发上限 | 默认 `max_workers=min(8, len(tool_calls))`，可配置 |
| 超时 | 单 call 可选 `tool_timeout`（如 30s），超时记为错误结果 |

#### 伪代码

```python
def execute_tool_calls(tool_calls: list[ToolCall], workspace: Path) -> list[ToolResult]:
    if len(tool_calls) == 1:
        return [run_one(tool_calls[0], workspace)]

    with ThreadPoolExecutor(max_workers=min(8, len(tool_calls))) as pool:
        futures = [pool.submit(run_one, tc, workspace) for tc in tool_calls]
        # 按提交顺序取回，保持与 tool_calls 对齐
        return [f.result() for f in futures]
```

Agent Loop 中：

```python
if resp.tool_calls:
    results = execute_tool_calls(resp.tool_calls, workspace)  # 自动并行
    for tc, result in zip(resp.tool_calls, results):
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    continue
```

#### Prompt 侧引导（可选）

在 System Prompt 中加一句，鼓励模型在信息独立时合并调用：

> 若需要同时搜索多个关键词或阅读多个互不依赖的文件，请在同一轮发起多个 tool_calls，勿串行拆成多轮。

#### 注意事项

1. **MVP 工具均为只读、无共享可变状态**，并行安全；后续若加写操作或索引更新，需排除或加锁。  
2. **不要做跨轮依赖分析**：并行范围仅限「同一 LLM 响应内的多个 tool_calls」；跨轮天然串行。  
3. **verbose 输出**应标注本轮为 parallel，并打印各 call 耗时，便于对比串行收益。  
4. I/O 密集（`rg` / 读盘）适合线程池；若未来 tool 含重 CPU（大规模 AST），再考虑进程池。

#### 配置

| 变量 | 含义 | 默认 |
|------|------|------|
| `CODE_WIKI_TOOL_MAX_WORKERS` | 单轮并行上限 | `8` |
| `CODE_WIKI_TOOL_TIMEOUT` | 单 tool 超时（秒） | `30` |

---

## 4. 模块设计

### 4.1 建议目录结构

```
code-wiki/
├── README.md
├── tech-design.md
├── pyproject.toml
├── src/code_wiki/
│   ├── __init__.py
│   ├── cli.py              # CLI 入口
│   ├── agent.py            # Agent Loop
│   ├── llm.py              # LLM Client 抽象
│   ├── prompts.py          # System / 策略文案
│   ├── config.py           # 环境变量与默认配置
│   ├── safety.py           # 路径校验、截断、忽略
│   └── tools/
│       ├── __init__.py     # Tool registry + OpenAI-compatible schemas
│       ├── base.py         # Tool 协议
│       ├── filesystem.py   # list_dir / glob / read_file
│       ├── outline.py      # 分层读：启发式/AST 大纲与符号切片
│       ├── symbols.py      # find_definition / find_references（tree-sitter / LSP）
│       ├── grep.py         # 内容搜索（优先 rg；符号工具不可用时的兜底）
│       ├── git_tools.py    # 只读 git 白名单（log/blame/show/…）
│       └── search.py       # 可选：语义检索
└── tests/
    ├── test_safety.py
    ├── test_tools.py
    └── test_agent_loop.py  # mock LLM
```

### 4.2 模块职责

| 模块 | 职责 |
|------|------|
| `cli.py` | 解析参数：`workspace`、`question`、`--max-steps`、`--verbose` |
| `agent.py` | 维护 messages、调度 tool（含同轮并行，见 §3.2）、控制循环退出 |
| `llm.py` | 统一 chat + tool_calls 接口（OpenAI 兼容优先） |
| `tools/*` | 实现具体工具；返回结构化文本给模型 |
| `outline.py` | `read_file` 分层读：签名大纲、按符号切片（启发式 → AST） |
| `symbols.py` | `find_definition` / `find_references`（见 §5.2） |
| `git_tools.py` | 只读 git 白名单封装（见 §5.3）；禁止任意 shell |
| `safety.py` | `resolve_under_root`、忽略 glob、`truncate` |
| `config.py` | `DEEPSEEK_API_KEY`、默认 DeepSeek base_url/model、`max_steps` 等 |

---

## 5. Tool 规格

### 5.1 MVP 工具集

#### `list_dir`

| 字段 | 说明 |
|------|------|
| 入参 | `path`（相对 workspace，默认 `.`） |
| 出参 | 子目录/文件名列表（已应用忽略规则） |
| 限制 | 单目录最多返回 N 项（如 200） |

#### `glob`

| 字段 | 说明 |
|------|------|
| 入参 | `pattern`（如 `**/*auth*.py`） |
| 出参 | 匹配路径列表 |
| 限制 | 最多返回 M 条（如 100） |

#### `grep`

| 字段 | 说明 |
|------|------|
| 入参 | `pattern`，可选 `glob`、`path`、`case_insensitive` |
| 出参 | `file:line:content` 列表 |
| 限制 | 最多 K 条匹配（如 50）；单行截断 |
| 实现 | 优先调用 `rg`；无则 Python 回退 |

#### `read_file`

| 字段 | 说明 |
|------|------|
| 入参 | `path`；可选 `mode`、`symbol`、`start_line`、`end_line` |
| 出参 | 见下方 `mode` |
| 限制 | `body` / 区间读：单次最多 L 行（如 200）或约 20KB；`outline` 最多 S 个符号（如 80） |

##### 分层读（`mode`）

目标：先廉价看结构，再按需读实现，避免整文件灌进上下文。

| `mode` | 行为 | 典型用途 |
|--------|------|----------|
| `outline`（默认推荐） | 只返回文件大纲：imports 摘要 + 顶层/类成员**签名**与起止行号，不含函数体 | 判断文件是否相关、选下钻目标 |
| `body` | 读完整区间或整文件（受行数/字节上限约束） | 已确认相关，需要实现细节 |
| `symbol` | 按符号名只返回该函数/方法/类的完整定义（含 body） | 已知符号名时的精读 |

入参补充：

| 参数 | 说明 |
|------|------|
| `mode` | `outline` \| `body` \| `symbol`；缺省建议 `outline`（短文件可直接 `body`） |
| `symbol` | `mode=symbol` 时必填，如 `AuthService.login` 或 `login` |
| `start_line` / `end_line` | 仅 `mode=body` 时生效；用于分段精读 |

##### `outline` 输出示例

```
# src/auth/service.py  (342 lines)
imports: fastapi, jose, .models, .repo  (4)

L12  class AuthService
L18    def __init__(self, repo: UserRepo) -> None
L24    def login(self, username: str, password: str) -> Token
L56    def refresh(self, token: str) -> Token
L80  def hash_password(raw: str) -> str
L95  def verify_password(raw: str, hashed: str) -> bool
```

Agent 看到 `login` 在 L24 后，再调用：

```
read_file(path="src/auth/service.py", mode="symbol", symbol="AuthService.login")
# 或
read_file(path="src/auth/service.py", mode="body", start_line=24, end_line=55)
```

##### 解析实现策略

| 阶段 | 做法 |
|------|------|
| **P0（启发式）** | 正则/缩进识别 `def`/`class`/`function`/`func` 等行作为签名；不保证全语言正确，但零依赖可用 |
| **P1（结构化）** | tree-sitter（或语言官方 AST）提取符号名、种类、起止行；`symbol` 模式按节点切片 |
| 语言覆盖 | P0：Python / TS / Go / Java 常见模式；P1：按仓库实际语言扩展 grammar |

启发式失败时：回退为「文件头 N 行 + 所有疑似签名行」，并提示模型改用 `body` + 行号区间。

##### Prompt 侧策略（写入 System Prompt）

1. 对未知大文件（如 >80 行）**先 `outline`**，确认相关后再 `symbol` / `body`。  
2. 小文件或已由 `grep` 精确定位到窄行号时，可直接 `body`。  
3. 禁止对同一大文件反复 `body` 整读；应基于 outline 行号分段。

##### 与其它工具的关系

| 能力 | 归属 |
|------|------|
| 文件级大纲 / 按符号读 body | `read_file` 的 `mode`（本节） |
| 跨文件定位定义 / 引用 | `find_definition` / `find_references`（§5.2） |

### 5.2 符号导航（优先于全文 grep）

有 tree-sitter 索引或 LSP 时，**按符号图导航比盲目全文 grep 更稳**：少噪声（字符串/注释误命中）、能区分定义与引用、便于沿调用链下钻。

#### 工具规格

##### `find_definition`

| 字段 | 说明 |
|------|------|
| 入参 | `symbol`（必填）；可选 `path`（提示作用域，如当前文件/包）、`lang` |
| 出参 | 定义位置列表：`path:start_line-end_line` + 符号种类（function/class/method/…）+ 签名一行 |
| 限制 | 最多返回 D 条（如 20）；重名时全部列出并标注文件路径 |

##### `find_references`

| 字段 | 说明 |
|------|------|
| 入参 | `symbol`（必填）；可选 `path`、`include_declaration`（默认 false） |
| 出参 | 引用位置列表：`path:line:snippet`；可按文件聚合计数 |
| 限制 | 最多 R 条（如 50）；超出时注明 truncated，建议收窄 `path` |

典型链路：

```
find_definition("login") 
  → src/auth/service.py:L24 AuthService.login
read_file(mode="symbol", symbol="AuthService.login")
find_references("AuthService.login")
  → src/api/routes.py:L88  … await auth.login(...)
  → tests/test_auth.py:L12 …
```

#### 检索优先级（写入 System Prompt）

| 优先级 | 何时用 | 工具 |
|--------|--------|------|
| 1 | 问题里已出现/可推断出符号、类名、函数名 | `find_definition` → `read_file(mode=symbol)` |
| 2 | 需要调用方 / 影响面 / 「谁用了 X」 | `find_references` |
| 3 | 符号未知，只有自然语言概念（如「鉴权」） | `grep` / 可选 `semantic_search`，命中后再升到符号工具 |
| 4 | 符号工具不可用或 0 结果 | **回退 `grep`**，并在 tool 结果中注明 fallback |

禁止：在已能 `find_definition` 时，对同一标识符做无 glob 收窄的全仓库 `grep`（浪费步数与上下文）。

#### 后端实现分层

| 层 | 能力 | 阶段 |
|----|------|------|
| **A. tree-sitter 符号表** | 扫仓库建 `(name, kind, file, range)` 索引；`find_definition` 查表；`find_references` 做同名 identifier 匹配（可先文件内/包内） | P1 |
| **B. LSP** | 对已配置语言起 language server，走 `textDocument/definition` / `references`（精度最高，含跨文件真实引用） | P2 |
| **C. GitNexus / 图谱** | `query` / `context` 补执行流与社区结构；与 LSP 互补而非替代 | P2 可选 |
| **回退** | 无索引/无 LSP → 工具返回明确错误码，Agent 改用 `grep` + `read_file(outline)` | P0 即约定 |

索引策略（层 A）：

- 首次提问或检测到 workspace 变更时懒建索引；结果缓存在 `{workspace}/.code-wiki/symbols.json`（或内存 + mtime 校验）
- 遵守与 §6 相同的忽略规则；大仓可先索引入口目录（`--focus`）
- 索引失败不阻断 Agent，仅禁用符号工具并回退 grep

#### 输出示例

```
# find_definition("AuthService.login")
DEFINITIONS (1)
- src/auth/service.py:24-55  method  AuthService.login(self, username: str, password: str) -> Token

# find_references("AuthService.login")
REFERENCES (3)  include_declaration=false
- src/api/routes.py:88  return await auth_service.login(form.username, form.password)
- src/cli/main.py:40    token = svc.login(user, pw)
- tests/test_auth.py:12 tok = service.login("u", "p")
```

#### 配置

| 变量 | 含义 | 默认 |
|------|------|------|
| `CODE_WIKI_SYMBOL_BACKEND` | `auto` \| `treesitter` \| `lsp` \| `off` | `auto` |
| `CODE_WIKI_SYMBOL_INDEX` | 是否启用懒索引缓存 | `true` |

`auto`：LSP 可用则 LSP，否则 tree-sitter，再否则 off（仅 grep）。

### 5.3 只读 Git 工具（白名单，非任意 shell）

支持 git，但**不暴露通用 `sh`**：用结构化 tool 封装只读子命令，由进程调用 `git -C <repo> …`，参数经白名单校验。

#### 何时使用

| 用户意图 | 推荐工具 |
|----------|----------|
| 某行/某段是谁改的 | `git_blame` |
| 文件或符号近期提交 | `git_log` |
| 看某次提交改了什么 | `git_show` |
| 当前分支 / 脏文件概览 | `git_status` |
| 两版本差异（只读） | `git_diff` |

纯「代码怎么工作」的问题**不必先调 git**；定位到文件后再按需用 blame/log。

#### 工具规格

##### `git_status`

| 字段 | 说明 |
|------|------|
| 入参 | 无（或可选 `porcelain=true`） |
| 出参 | 分支名、ahead/behind（若有）、变更文件列表摘要 |
| 等价 | `git status -sb`（可加 `--porcelain=v1`） |

##### `git_log`

| 字段 | 说明 |
|------|------|
| 入参 | 可选 `path`、`max_count`（默认 10，上限 30）、`since`、`until`、`grep`（提交说明关键词） |
| 出参 | `hash`、`author`、`date`、`subject` 列表 |
| 等价 | `git log --format=… -n N [-- path]` |

##### `git_blame`

| 字段 | 说明 |
|------|------|
| 入参 | `path`（必填）；可选 `start_line`、`end_line` |
| 出参 | 按行：`line | short_hash | author | date | content` |
| 限制 | 单次最多 blame L 行（如 200）；大范围先收窄 |
| 等价 | `git blame -L S,E -- path` |

##### `git_show`

| 字段 | 说明 |
|------|------|
| 入参 | `revision`（必填，如 commit hash / `HEAD~1`）；可选 `path` |
| 出参 | commit metadata + patch（截断） |
| 限制 | patch 最多约 20KB；超出截断并提示用 `path` 收窄 |
| 等价 | `git show --stat --format=… rev[:path]` |

##### `git_diff`

| 字段 | 说明 |
|------|------|
| 入参 | 可选 `base`、`head`（默认 `HEAD`）、`path` |
| 出参 | unified diff 摘要（截断） |
| 限制 | 同上字节上限；拒绝包含 `..` 且指向 sandbox 外的 path |
| 等价 | `git diff base...head -- path` |

#### 安全约定（强制）

| 规则 | 说明 |
|------|------|
| 只读白名单 | 仅允许上表子命令；**禁止** `commit` / `push` / `pull` / `fetch` / `checkout` / `reset` / `rebase` / `merge` / `add` / `stash` / `clean` / `config` 等 |
| 无任意参数透传 | 禁止把用户/模型拼的原始 argv 直接交给 shell；每个字段映射到固定 flag |
| 工作目录 | `git -C <git_root>`；`git_root` = workspace 内 `git rev-parse --show-toplevel`，必须仍在 sandbox |
| 非 git 仓库 | 工具返回明确错误：`not a git repository`，Agent 改用文件系统工具 |
| 超时 | 复用 `CODE_WIKI_TOOL_TIMEOUT`；blame/log 过大时先截断 |
| 环境 | `GIT_TERMINAL_PROMPT=0`；不传网络凭证；不执行 `git` 别名危险配置时可加 `-c alias.*=` 清理（实现阶段细化） |
| 并行 | 只读，可与其它 tool 同轮并行（§3.2） |

#### 实现要点

```python
# 伪代码：禁止 shell=True，禁止字符串拼接整条命令
subprocess.run(
    ["git", "-C", str(git_root), "blame", f"-L{start},{end}", "--", rel_path],
    capture_output=True,
    text=True,
    timeout=timeout,
    env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
)
```

- `.git` 对 `list_dir`/`grep` 仍默认忽略；git 工具通过 git 协议读对象，不把 `.git` 当普通目录扫。
- 无 `git` 可执行文件：注册 tool 但调用时返回安装提示；或启动时探测并禁用 schema。

#### Prompt 侧

- 历史/作者类问题优先 `git_blame` / `git_log`，再 `git_show` 看具体 diff。  
- 不要编造 hash；只引用工具返回的提交。  
- 分析现行代码逻辑时以工作区文件为准；git 用于补充「演变/责任」上下文。

#### 配置

| 变量 | 含义 | 默认 |
|------|------|------|
| `CODE_WIKI_GIT_ENABLED` | 是否注册 git 工具 | `true` |
| `CODE_WIKI_GIT_LOG_MAX` | `git_log` 默认条数上限 | `30` |

### 5.4 其它增强工具（Phase 2+）

| Tool | 说明 |
|------|------|
| `semantic_search` | embedding 检索代码块；适合作「概念 → 候选符号」的入口，命中后仍走 §5.2 |
| `gitnexus_query` / `context` | 若已索引，走图谱查执行流与社区；可与 `find_references` 结果交叉验证 |

### 5.5 Tool Schema 约定

对外暴露 OpenAI-compatible `tools` JSON Schema，便于切换兼容网关。每个工具执行结果统一为 **字符串**（必要时 JSON 序列化），并在过长时截断并附提示。符号 / git 等可选能力未启用时，**不要注册**对应 schema，避免模型误调。

---

## 6. 安全与边界

| 规则 | 说明 |
|------|------|
| 路径沙箱 | `Path.resolve()` 后必须 `is_relative_to(workspace)` |
| 默认忽略 | `.git`, `node_modules`, `dist`, `build`, `.venv`, `venv`, `__pycache__`, `.idea`, `.cursor` 等（git **工具**除外，见 §5.3） |
| 输出截断 | 防止单次 tool 结果撑爆上下文 |
| 步数上限 | 默认 `max_steps=20`（可配置） |
| 只读 | 禁止写文件；**禁止任意 shell**；git 仅白名单只读子命令（§5.3） |

二进制/超大文件：`read_file` 拒绝或只读文本 MIME/扩展名白名单。

---

## 7. LLM 与配置

### 7.1 接口抽象

```python
class LLMClient(Protocol):
    def chat(self, messages: list[dict], tools: list[dict]) -> LLMResponse: ...

@dataclass
class LLMResponse:
    content: str | None
    tool_calls: list[ToolCall]  # id, name, arguments
```

### 7.2 配置项

| 变量 | 含义 | 默认 |
|------|------|------|
| `CODE_WIKI_API_KEY` / `DEEPSEEK_API_KEY` | DeepSeek API Key | 必填 |
| `CODE_WIKI_BASE_URL` | API Base URL | 默认 `https://api.deepseek.com` |
| `CODE_WIKI_MODEL` | 模型名 | 默认 `deepseek-v4-flash` |
| `CODE_WIKI_MAX_STEPS` | 最大工具轮次 | `20` |
| `CODE_WIKI_TOOL_MAX_WORKERS` | 单轮 tool 并行上限（见 §3.2） | `8` |
| `CODE_WIKI_TOOL_TIMEOUT` | 单 tool 超时秒数 | `30` |
| `CODE_WIKI_SYMBOL_BACKEND` | 符号导航后端（见 §5.2） | `auto` |
| `CODE_WIKI_SYMBOL_INDEX` | tree-sitter 懒索引缓存 | `true` |
| `CODE_WIKI_GIT_ENABLED` | 是否启用只读 git 工具（§5.3） | `true` |
| `CODE_WIKI_GIT_LOG_MAX` | git_log 条数上限 | `30` |

需选用支持 **tool / function calling** 的模型。

---

## 8. 接口设计

### 8.1 CLI（MVP）

```bash
code-wiki /path/to/repo "登录鉴权是怎么做的？"
code-wiki /path/to/repo "Who implements payment?" --max-steps 30 -v
```

| 参数 | 说明 |
|------|------|
| `workspace` | 工作空间绝对/相对路径 |
| `question` | 自然语言问题 |
| `--max-steps` | 覆盖默认步数 |
| `-v / --verbose` | 打印 tool 调用与结果摘要 |

退出码：`0` 成功；`1` 参数/路径错误；`2` LLM/运行失败。

### 8.2 程序 API（内部）

```python
def run_agent(
    workspace: Path,
    question: str,
    *,
    max_steps: int = 20,
    verbose: bool = False,
) -> str:
    """返回最终回答文本。"""
```

### 8.3 后续 HTTP（非 MVP）

```
POST /v1/ask
{ "workspace": "...", "question": "...", "max_steps": 20 }
→ { "answer": "...", "steps": [...] }
```

---

## 9. Prompt 设计要点

System Prompt 应包含：

- 角色：只读代码分析助手  
- 工作空间根路径  
- 工具使用策略（见 §3.1）：符号优先（§5.2）、分层读（§5.1）、历史用只读 git（§5.3）  
- 回答格式：结论 → 关键步骤/模块 → 引用列表  
- 不确定时说明假设，勿编造不存在的文件  

User Message 模板：

```
工作空间: {workspace}
问题: {question}
```

---

## 10. 分阶段计划

| 阶段 | 内容 | 产出 |
|------|------|------|
| **P0 MVP** | CLI + 文件系统/grep + **只读 git 白名单** + Agent Loop；`read_file` 启发式分层读 | 可本地问答 + 历史追溯 |
| **P1 可用** | verbose、忽略规则、tree-sitter 大纲 + **符号表 `find_definition`/`find_references`**、单测 | 符号优先检索 |
| **P2 增强** | LSP 高精度引用、语义检索、GitNexus 可选集成 | 复杂链路更准 |
| **P3 产品化** | HTTP API、流式输出、索引缓存、简单 Web UI | 可分享使用 |

---

## 11. 测试策略

| 类型 | 覆盖 |
|------|------|
| 单元 | `safety.resolve_under_root`（含 `..` 穿越）、截断、忽略规则 |
| 工具 | 临时目录 fixture：`list_dir` / `grep` / `read_file`；git 临时 repo 测 `log`/`blame`；符号工具样例 |
| Agent | mock LLM 固定 tool_calls 序列，断言最终答案与调用次数 |
| 手工 | 用小型样例仓库跑 2～3 个真实问题 |

---

## 12. 风险与对策

| 风险 | 对策 |
|------|------|
| 大仓库搜索过慢/结果过多 | 符号优先（§5.2）+ 忽略规则 + 结果上限 + 收窄 path/glob |
| grep 噪声（注释/同名字符串） | 有符号后端时禁用盲目全库 grep；重名靠定义列表消歧 |
| 模型幻觉文件路径 | Prompt 强制「只引用读过的路径」；verbose 可审计 |
| Tool 循环无效 | `max_steps`；可选检测重复相同 tool 调用 |
| 无 `rg` 环境 | Python 回退实现，并在文档说明推荐安装 ripgrep |
| 上下文爆掉 | 截断 tool 输出；`read_file` 先 outline 再分段/按符号读（§5.1） |
| outline 解析不准 | P0 启发式 + 失败回退；P1 换 tree-sitter；Prompt 允许改 body |
| 符号索引陈旧 / LSP 未就绪 | mtime 校验重建；`auto` 降级 grep；tool 结果明示 backend |
| git 写操作误暴露 | 子命令白名单 + 参数结构映射 + 禁止 `shell=True`；单测覆盖拒绝 `push`/`reset` |
| 非 git 目录 / 无 git 二进制 | 明确错误并降级；启动探测可禁用 schema |

---

## 13. 依赖（MVP）

```
# 运行时
openai          # 或兼容 SDK
typer           # CLI
rich            # 可选：美化 verbose 输出

# 开发
pytest
ruff
```

系统推荐：`ripgrep`（`rg`）。

---

## 14. 开放问题

1. 默认模型与网关是否固定为内部兼容 API？  
2. 符号后端默认：P1 只做 tree-sitter 表，还是尽早接 LSP？GitNexus 与 LSP 如何分工？  
3. 回答语言：跟随用户问题，还是固定中文？  

---

## 15. 附录：与 README 的对应关系

| README 描述 | 设计落点 |
|-------------|----------|
| 输入工作空间 + 问题 | CLI / `run_agent` |
| Agent 自己分析 | Tool-calling Loop（§3） |
| 找到相关代码 | 符号工具优先（§5.2）+ `grep` / `glob` / `read_file`（§5） |
| 变更/作者追溯 | 只读 git 白名单（§5.3）：`git_log` / `git_blame` / `git_show` 等 |
| 给出回复 | 最终无 tool_calls 的 LLM content（§3） |
