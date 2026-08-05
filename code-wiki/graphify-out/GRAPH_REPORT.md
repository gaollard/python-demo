# Graph Report - code-wiki  (2026-08-06)

## Corpus Check
- 19 files · ~8,273 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 202 nodes · 292 edges · 15 communities (14 shown, 1 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2050ea16`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]

## God Nodes (most connected - your core abstractions)
1. `Code Wiki — AI Technical Design` - 16 edges
2. `extract_symbols()` - 12 edges
3. `resolve_under_root()` - 12 edges
4. `run_agent()` - 9 edges
5. `read_file()` - 9 edges
6. `ToolSpec` - 9 edges
7. `truncate()` - 8 edges
8. `_run_git()` - 8 edges
9. `ToolRegistry` - 8 edges
10. `test_agent_uses_tools_then_answers()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `test_resolve_under_root_ok()` --calls--> `resolve_under_root()`  [INFERRED]
  tests/test_safety.py → src/code_wiki/safety.py
- `test_resolve_blocks_escape()` --calls--> `resolve_under_root()`  [INFERRED]
  tests/test_safety.py → src/code_wiki/safety.py
- `test_truncate()` --calls--> `truncate()`  [INFERRED]
  tests/test_safety.py → src/code_wiki/safety.py
- `test_agent_uses_tools_then_answers()` --calls--> `run_agent()`  [INFERRED]
  tests/test_agent_loop.py → src/code_wiki/agent.py
- `test_agent_prints_assistant_content_with_tool_calls()` --calls--> `run_agent()`  [INFERRED]
  tests/test_agent_loop.py → src/code_wiki/agent.py

## Communities (15 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (24): is_probably_text_file(), PathEscapeError, Resolve path and ensure it stays inside root., resolve_under_root(), should_skip_dir(), truncate(), truncate_lines(), test_resolve_blocks_escape() (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (25): 10. 分阶段计划, 11. 测试策略, 12. 风险与对策, 13. 依赖（MVP）, 14. 开放问题, 15. 附录：与 README 的对应关系, 1.1 产品目标, 1.2 成功标准（MVP） (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.18
Nodes (11): Settings, LLMClient, LLMResponse, MockLLMClient, OpenAICompatibleClient, Deterministic client for tests: scripted responses., _settings(), test_agent_prints_assistant_content_with_tool_calls() (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (10): Protocol, ToolContext, ToolSpec, filesystem_tools(), git_tools(), grep_tools(), from_settings(), ToolRegistry (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (15): 5.1 MVP 工具集, 5.4 其它增强工具（Phase 2+）, 5.5 Tool Schema 约定, 5. Tool 规格, code:block6 (# src/auth/service.py  (342 lines)), code:block7 (read_file(path="src/auth/service.py", mode="symbol", symbol=), `glob`, `grep` (+7 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (13): 5.3 只读 Git 工具（白名单，非任意 shell）, code:python (# 伪代码：禁止 shell=True，禁止字符串拼接整条命令), `git_blame`, `git_diff`, `git_log`, `git_show`, `git_status`, Prompt 侧 (+5 more)

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (11): extract_imports(), extract_symbols(), find_symbol_span(), _fix_end_lines(), format_outline(), format_symbol_body(), _kind_from_sig(), _name_from_sig() (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (8): Run the analysis agent and return the final answer text., run_agent(), main(), Code Wiki — analyze a workspace with an LLM agent., bootstrap_context(), Cheap first-turn context: top-level listing + README snippet., system_prompt(), user_prompt()

### Community 8 - "Community 8"
Cohesion: 0.49
Nodes (10): _find_git_root(), _format_blame_porcelain(), git_blame(), git_diff(), _git_env(), git_log(), git_show(), git_status() (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (11): 3.1 Agent 策略（写入 System Prompt）, 3.2 并行 Tool Calls, 3. 核心流程, code:block2 (1. 校验 workspace 存在且为目录), code:python (def execute_tool_calls(tool_calls: list[ToolCall], workspace), code:python (if resp.tool_calls:), Prompt 侧引导（可选）, 伪代码 (+3 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (10): Code Wiki, code:bash (cd code-wiki), code:bash (export DEEPSEEK_API_KEY=sk-...), code:bash (pytest), 使用, 关注维度, 安装, 开发 (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.2
Nodes (10): 5.2 符号导航（优先于全文 grep）, code:block8 (find_definition("login")), code:block9 (# find_definition("AuthService.login")), `find_definition`, `find_references`, 后端实现分层, 工具规格, 检索优先级（写入 System Prompt） (+2 more)

### Community 12 - "Community 12"
Cohesion: 0.29
Nodes (6): 8.1 CLI（MVP）, 8.2 程序 API（内部）, 8.3 后续 HTTP（非 MVP）, 8. 接口设计, code:bash (code-wiki /path/to/repo "登录鉴权是怎么做的？"), code:block14 (POST /v1/ask)

### Community 13 - "Community 13"
Cohesion: 0.83
Nodes (3): _env_bool(), _env_int(), from_env()

## Knowledge Gaps
- **66 isolated node(s):** `Code Wiki — read-only code analysis agent.`, `Deterministic client for tests: scripted responses.`, `Cheap first-turn context: top-level listing + README snippet.`, `Extract top-level / nested signatures via indent heuristics.`, `Code Wiki — analyze a workspace with an LLM agent.` (+61 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolSpec` connect `Community 3` to `Community 2`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `Code Wiki — AI Technical Design` connect `Community 1` to `Community 9`, `Community 4`, `Community 12`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `5. Tool 规格` connect `Community 4` to `Community 1`, `Community 11`, `Community 5`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `extract_symbols()` (e.g. with `test_outline_and_symbol()` and `find_definition()`) actually correct?**
  _`extract_symbols()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `resolve_under_root()` (e.g. with `test_resolve_under_root_ok()` and `test_resolve_blocks_escape()`) actually correct?**
  _`resolve_under_root()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `run_agent()` (e.g. with `test_agent_uses_tools_then_answers()` and `test_agent_prints_assistant_content_with_tool_calls()`) actually correct?**
  _`run_agent()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `read_file()` (e.g. with `test_outline_and_symbol()` and `resolve_under_root()`) actually correct?**
  _`read_file()` has 6 INFERRED edges - model-reasoned connections that need verification._