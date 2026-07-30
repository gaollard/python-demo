# Graph Report - llm-demo  (2026-07-30)

## Corpus Check
- 15 files · ~3,244 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 80 nodes · 75 edges · 14 communities (10 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `01aeb9c0`
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

## God Nodes (most connected - your core abstractions)
1. `Refund Policy Skill` - 6 edges
2. `Support Reply Skill` - 6 edges
3. `discover_skills()` - 5 edges
4. `discover_skills()` - 4 edges
5. `_parse_frontmatter()` - 3 edges
6. `load_skill()` - 3 edges
7. `_parse_frontmatter()` - 3 edges
8. `llm-demo` - 3 edges
9. `依赖说明` - 3 edges
10. `read_readme()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (14 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (12): _discover_scripts(), discover_skills(), load_skill(), _parse_frontmatter(), Agent Skills + Scripts 示例：每个 skill 自带 scripts/， load_skill 按需加载指令，run_skill_scri, Load a specialized skill's full instructions and list its scripts.      Call thi, Run a Python script bundled under skills/<skill>/scripts/.      Only scripts dis, Parse YAML-ish frontmatter without requiring a full YAML dependency. (+4 more)

### Community 1 - "Community 1"
Cohesion: 0.17
Nodes (11): calculate_refund(), check_inventory(), create_support_ticket(), get_orders(), lookup_customer(), 多工具 Agent 示例：客服场景，需要串联查客户 → 查订单 → 查库存 → 算退款 → 建工单。, 查询商品库存与所在仓库。      Args:         product_id: 商品 SKU，例如 SKU-WATCH, 根据单价、数量、会员等级和退款原因计算应退金额。      规则：     - defect / wrong_item: 全额退款 + 会员加成     - c (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.24
Nodes (8): discover_skills(), load_skill(), _parse_frontmatter(), Agent Skills 示例：扫描 skills/*/SKILL.md，把 name/description 注入 system prompt， 需要时通过, Parse YAML-ish frontmatter without requiring a full YAML dependency., Scan skills/*/SKILL.md and return skills keyed by name., Load a specialized skill's full instructions by name.      Call this when the us, Skill

### Community 3 - "Community 3"
Cohesion: 0.25
Nodes (6): code:block2 (langchain_core          →  抽象：Prompt / Parser / Chain), `langchain_core`, `langchain_openai`, llm-demo, 二者关系, 依赖说明

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (6): Allowed values, code:bash (python scripts/calculate_refund.py \), Output format, Refund Policy Skill, Rules, Workflow

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (6): code:block1 (尊敬的 {name}：), Constraints, Support Reply Skill, Template, Tone, Workflow

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (3): Sandbox 示例：用 ShellToolMiddleware 给 agent 提供受控 shell 执行环境。  对比 05：05 用 subprocess, 读取本示例目录下的 README.md（位于沙箱工作区之外）。      shell 只能访问 workspace；要用此工具读取沙箱外的 README。, read_readme()

## Knowledge Gaps
- **27 isolated node(s):** `Sandbox 示例：用 ShellToolMiddleware 给 agent 提供受控 shell 执行环境。  对比 05：05 用 subprocess`, `读取本示例目录下的 README.md（位于沙箱工作区之外）。      shell 只能访问 workspace；要用此工具读取沙箱外的 README。`, `多工具 Agent 示例：客服场景，需要串联查客户 → 查订单 → 查库存 → 算退款 → 建工单。`, `按客户姓名查找客户档案（id / email / 会员等级 / 城市）。      Args:         name: 客户姓名，支持模糊匹配，如 Alic`, `按客户 ID 拉取历史订单列表。      Args:         customer_id: 客户 ID，例如 C001` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Sandbox 示例：用 ShellToolMiddleware 给 agent 提供受控 shell 执行环境。  对比 05：05 用 subprocess`, `读取本示例目录下的 README.md（位于沙箱工作区之外）。      shell 只能访问 workspace；要用此工具读取沙箱外的 README。`, `多工具 Agent 示例：客服场景，需要串联查客户 → 查订单 → 查库存 → 算退款 → 建工单。` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._