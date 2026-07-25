# Graph Report - 01-streamlit  (2026-07-25)

## Corpus Check
- 3 files · ~1,199 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 47 nodes · 44 edges · 14 communities (10 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `caa1d732`
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

## God Nodes (most connected - your core abstractions)
1. `Streamlit` - 18 edges
2. `为什么需要 Streamlit` - 3 edges
3. `安装与启动` - 3 edges
4. `最小应用` - 3 edges
5. `布局` - 3 edges
6. `session_state：跨次重跑的状态` - 3 edges
7. `缓存：别在每次 rerun 里重算` - 3 edges
8. `最小可运行看板骨架` - 3 edges
9. `list_models()` - 2 edges
10. `核心概念` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (14 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.18
Nodes (10): code:block1 (浏览器操作（改控件 / 点按钮）), code:python (import streamlit as st), code:python (import streamlit as st), Streamlit, 和「普通 Web 框架」差在哪, 常用展示, 常见坑, 延伸阅读 (+2 more)

### Community 1 - "Community 1"
Cohesion: 0.4
Nodes (5): code:python (import streamlit as st), code:python (import streamlit as st), `@st.cache_data` —— 缓存「数据」, `@st.cache_resource` —— 缓存「资源 / 连接」, 缓存：别在每次 rerun 里重算

### Community 2 - "Community 2"
Cohesion: 0.5
Nodes (3): list_models(), 本地 Ollama 聊天 Demo（Streamlit）。  说明： - 通过 Ollama 的 OpenAI 兼容接口调用本地模型 - Streamlit 每, 从 Ollama 拉取本地模型；过滤掉 embedding 模型。失败则用默认列表。

### Community 3 - "Community 3"
Cohesion: 0.67
Nodes (3): code:python (# 终端脚本：只能改参数再跑), code:python (# Streamlit：浏览器里拖滑块，立刻看到结果), 为什么需要 Streamlit

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (3): code:bash (python -m pip install streamlit), code:bash (streamlit run app.py --server.port 8501), 安装与启动

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (3): code:python (# app.py), code:bash (streamlit run app.py), 最小应用

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (3): code:python (import streamlit as st), code:python (import streamlit as st), 布局

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): code:python (import streamlit as st), code:python (import streamlit as st), session_state：跨次重跑的状态

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (3): code:python (# app.py), code:bash (streamlit run app.py), 最小可运行看板骨架

## Knowledge Gaps
- **26 isolated node(s):** `本地 Ollama 聊天 Demo（Streamlit）。  说明： - 通过 Ollama 的 OpenAI 兼容接口调用本地模型 - Streamlit 每`, `从 Ollama 拉取本地模型；过滤掉 embedding 模型。失败则用默认列表。`, `code:block1 (浏览器操作（改控件 / 点按钮）)`, `code:python (# 终端脚本：只能改参数再跑)`, `code:python (# Streamlit：浏览器里拖滑块，立刻看到结果)` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Streamlit` connect `Community 0` to `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 12`?**
  _High betweenness centrality (0.758) - this node is a cross-community bridge._
- **Why does `缓存：别在每次 rerun 里重算` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `为什么需要 Streamlit` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **What connects `本地 Ollama 聊天 Demo（Streamlit）。  说明： - 通过 Ollama 的 OpenAI 兼容接口调用本地模型 - Streamlit 每`, `从 Ollama 拉取本地模型；过滤掉 embedding 模型。失败则用默认列表。`, `code:block1 (浏览器操作（改控件 / 点按钮）)` to the rest of the system?**
  _26 weakly-connected nodes found - possible documentation gaps or missing edges._