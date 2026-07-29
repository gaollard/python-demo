# Graph Report - llm-demo  (2026-07-29)

## Corpus Check
- 4 files · ~413 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 13 nodes · 9 edges · 5 communities (4 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `96867b42`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]

## God Nodes (most connected - your core abstractions)
1. `llm-demo` - 3 edges
2. `依赖说明` - 3 edges
3. `search_database()` - 2 edges
4. ``langchain_openai`` - 2 edges
5. `二者关系` - 2 edges
6. `Search the customer database for records matching the query.      Args:` - 1 edges
7. ``langchain_core`` - 1 edges
8. `code:block2 (langchain_core          →  抽象：Prompt / Parser / Chain)` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (5 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.5
Nodes (3): `langchain_core`, `langchain_openai`, 依赖说明

### Community 1 - "Community 1"
Cohesion: 0.5
Nodes (3): code:block2 (langchain_core          →  抽象：Prompt / Parser / Chain), llm-demo, 二者关系

## Knowledge Gaps
- **3 isolated node(s):** `Search the customer database for records matching the query.      Args:`, ``langchain_core``, `code:block2 (langchain_core          →  抽象：Prompt / Parser / Chain)`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `llm-demo` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.212) - this node is a cross-community bridge._
- **Why does `依赖说明` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.212) - this node is a cross-community bridge._
- **What connects `Search the customer database for records matching the query.      Args:`, ``langchain_core``, `code:block2 (langchain_core          →  抽象：Prompt / Parser / Chain)` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._