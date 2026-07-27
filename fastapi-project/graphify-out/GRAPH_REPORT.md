# Graph Report - fastapi-project  (2026-07-27)

## Corpus Check
- 66 files · ~38,764 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 318 nodes · 533 edges · 22 communities (21 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `14e0f776`
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
1. `useUserStore` - 15 edges
2. `ok()` - 13 edges
3. `论坛系统 PRD` - 10 edges
4. `3. 功能需求` - 9 edges
5. `FastAPI 目录结构最佳实践` - 8 edges
6. `PyMySQL vs aiomysql` - 8 edges
7. `getApiErrorMessage()` - 7 edges
8. `5. 实践建议` - 7 edges
9. `init_redis()` - 6 edges
10. `Post` - 6 edges

## Surprising Connections (you probably didn't know these)
- `register_user()` --calls--> `User`  [INFERRED]
  server/src/services/auth_service.py → server/src/models/user.py
- `get_current_user()` --calls--> `decode_access_token()`  [EXTRACTED]
  server/src/dependencies.py → server/src/core/security.py
- `register()` --calls--> `ok()`  [EXTRACTED]
  server/src/routers/auth.py → server/src/core/response.py
- `login()` --calls--> `ok()`  [EXTRACTED]
  server/src/routers/auth.py → server/src/core/response.py
- `my_posts()` --calls--> `ok()`  [EXTRACTED]
  server/src/routers/me.py → server/src/core/response.py

## Communities (22 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (41): register(), fetchMyFavorites(), fetchMyPosts(), createPost(), favoritePost(), fetchPostDetail(), fetchPosts(), likePost() (+33 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (28): BaseSettings, get_settings(), Settings, Configure root logging once for the application., setup_logging(), fail(), create_access_token(), decode_access_token() (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (25): BaseModel, ApiResponse, ok(), PageData, login(), register(), my_favorites(), my_posts() (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (31): 1.1 背景, 1.2 目标, 1.3 非目标（本期不做）, 1. 背景与目标, 2.1 角色, 2.2 核心用户旅程, 2. 用户与场景, 3.1 用户注册 (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (23): login(), attachAuthHeader(), BIZ_SUCCESS_CODES, envelopeMessage(), httpClient, IBaseRes, IRequestOptions, isBizSuccess() (+15 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (27): 1. 从最小到规范：按规模演进, 2. 官方推荐的多文件结构（起步版）, 3. 中型项目推荐结构（业务分层）, 4. 关键文件示例, 5. 实践建议, 6. 常见反模式, 7. 与本仓库 `fastapi-demo` 的关系, `app/dependencies.py`：共享依赖 (+19 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (22): Base, DeclarativeBase, Base, TimestampMixin, Post, PostFavorite, PostLike, User (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (18): 1. 一句话区别, 2. 为什么 FastAPI 更推荐 aiomysql, 3.1 同步：PyMySQL, 3.2 异步：aiomysql（本项目）, 3. 与 SQLAlchemy 的对接方式, 4. 对比一览, 5. 选型建议, 6. 常见踩坑 (+10 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (10): code:bash (cd fastapi-demo), code:bash (uvicorn src.main:app --reload --app-dir .), code:json ({ "code": 0, "message": "ok", "data": {} }), code:text (src/), code:python (from fastapi import Depends), Forum API (FastAPI Demo), 主要接口, 快速开始 (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.31
Nodes (5): copyTextToClipboard(), CheckGlyph(), CopyGlyph(), iconProps, CopyButtonProps

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (7): code:shell (./.venv/bin/python3 -m pip install "fastapi[standard]" uvico), code:shell (fastapi dev), Linux/macOS, 创建虚拟环境, 启动项目, 安装依赖, 激活虚拟环境

### Community 11 - "Community 11"
Cohesion: 0.33
Nodes (5): code:bash (pnpm install), 功能, 开发, 脚本, 鱼泡论坛 Client

## Knowledge Gaps
- **86 isolated node(s):** `Create the shared async Redis client (call once on app startup).`, `Close Redis client and connection pool on app shutdown.`, `FastAPI dependency that yields the shared Redis client.`, `Configure root logging once for the application.`, `env` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `register_user()` connect `Community 1` to `Community 6`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `InteractionOut` connect `Community 6` to `Community 2`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **What connects `Create the shared async Redis client (call once on app startup).`, `Close Redis client and connection pool on app shutdown.`, `FastAPI dependency that yields the shared Redis client.` to the rest of the system?**
  _86 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._