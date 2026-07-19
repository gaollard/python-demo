# Graph Report - pythons  (2026-07-19)

## Corpus Check
- 117 files · ~16,551 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 357 nodes · 202 edges · 171 communities (156 shown, 15 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1852cdb4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
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
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 46|Community 46]]

## God Nodes (most connected - your core abstractions)
1. `Python HTTP Server Docker 部署指南` - 13 edges
2. `RequestLoggingMiddleware` - 7 edges
3. `RateLimitMiddleware` - 7 edges
4. `Dog` - 5 edges
5. `test_middlewares()` - 5 edges
6. `SecurityHeadersMiddleware` - 5 edges
7. `Dog` - 5 edges
8. `CustomHTTPRequestHandler` - 4 edges
9. `MyApp` - 4 edges
10. `CustomHTTPRequestHandler` - 4 edges

## Surprising Connections (you probably didn't know these)
- `test_middlewares()` --calls--> `RequestLoggingMiddleware`  [INFERRED]
  project/django-demo/test_middleware.py → project/django-demo/polls/middleware.py
- `test_middlewares()` --calls--> `SecurityHeadersMiddleware`  [INFERRED]
  project/django-demo/test_middleware.py → project/django-demo/polls/middleware.py
- `test_middlewares()` --calls--> `RateLimitMiddleware`  [INFERRED]
  project/django-demo/test_middleware.py → project/django-demo/polls/middleware.py
- `test_middlewares()` --calls--> `CustomErrorMiddleware`  [INFERRED]
  project/django-demo/test_middleware.py → project/django-demo/polls/middleware.py

## Communities (171 total, 15 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (24): code:bash (# 查看详细错误信息), code:bash (# 手动测试连接), code:yaml (services:), code:yaml (services:), code:bash (# 自定义端口映射), code:block4 (container/), code:bash (# 访问主页), code:bash (# 检查端口占用) (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (8): test_middlewares(), MiddlewareMixin, CustomErrorMiddleware, RateLimitMiddleware, 请求日志中间件 - 记录每个请求的详细信息, 安全头中间件 - 添加安全相关的HTTP头, RequestLoggingMiddleware, SecurityHeadersMiddleware

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (7): code:sh (pip freeze > requirements.txt), code:block2 (python your_script.py &), code:block3 (nohup python your_script.py &), code:python (import subprocess), 作用域, 依赖生成, 后台运行

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (7): code:bash (# 查看运行中的容器), code:bash (# 实时查看日志), code:bash (# 查看健康状态), 健康检查, 查看容器状态, 查看日志, 🔍 监控和日志

### Community 10 - "Community 10"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (5): code:shell (./ll_env/bin/python -m pip install Django), code:shell (./ll_env/bin/django-admin startproject hello_world .), code:shell (./ll_env/bin/python manage.py runserver), code:shell (python manage.py startapp polls), code:block5 (app_name/)

### Community 17 - "Community 17"
Cohesion: 0.4
Nodes (5): code:bash (# 构建镜像), code:bash (# 启动服务), 🛠️ 快速开始, 方法1: 使用Docker命令, 方法2: 使用Docker Compose (推荐)

## Knowledge Gaps
- **53 isolated node(s):** `Config`, `计算表达式，格式: 'a operator b`, `Run administrative tasks.`, `ASGI config for hello_world project.  It exposes the ASGI callable as a module-l`, `Django settings for hello_world project.  Generated by 'django-admin startprojec` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Python HTTP Server Docker 部署指南` connect `Community 0` to `Community 17`, `Community 9`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `🔍 监控和日志` connect `Community 9` to `Community 0`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `🛠️ 快速开始` connect `Community 17` to `Community 0`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `test_middlewares()` (e.g. with `RequestLoggingMiddleware` and `SecurityHeadersMiddleware`) actually correct?**
  _`test_middlewares()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `计算表达式，格式: 'a operator b`, `Run administrative tasks.` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._