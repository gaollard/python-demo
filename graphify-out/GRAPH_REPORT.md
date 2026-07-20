# Graph Report - pythons  (2026-07-20)

## Corpus Check
- 130 files · ~19,296 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 484 nodes · 355 edges · 181 communities (163 shown, 18 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `00428df6`
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
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 119|Community 119]]
- [[_COMMUNITY_Community 120|Community 120]]

## God Nodes (most connected - your core abstractions)
1. `MiniHTTP` - 17 edges
2. `Python HTTP Server Docker 部署指南` - 13 edges
3. `Response` - 10 edges
4. `元组的组包和解包` - 10 edges
5. `元组和列表的区别` - 9 edges
6. `Request` - 8 edges
7. `RequestLoggingMiddleware` - 7 edges
8. `RateLimitMiddleware` - 7 edges
9. `text_response()` - 6 edges
10. `Router` - 6 edges

## Surprising Connections (you probably didn't know these)
- `plain()` --calls--> `text_response()`  [INFERRED]
  03-http框架/example.py → 03-http框架/minihttp/response.py
- `AppProtocol` --uses--> `Response`  [INFERRED]
  03-http框架/minihttp/server.py → 03-http框架/minihttp/response.py
- `MiniHTTP` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/request.py
- `MiniHTTP` --uses--> `MethodNotAllowed`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py
- `MiniHTTP` --uses--> `Router`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py

## Communities (181 total, 18 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (29): code:bash (# 构建镜像), code:bash (# 查看详细错误信息), code:bash (# 手动测试连接), code:yaml (services:), code:yaml (services:), code:bash (# 启动服务), code:bash (# 自定义端口映射), code:block4 (container/) (+21 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (10): index(), plain(), 迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1, MiniHTTP, 迷你 HTTP 框架，风格类似 Flask：          app = MiniHTTP("demo")          @app.get("/"), 注册中间件：middleware(request, call_next) -> Response, html_response(), json_response() (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (12): 纯 Python 原生实现的迷你 HTTP 框架（仅依赖标准库）。, HTTP 请求对象：解析请求行、请求头、查询参数与请求体。, 解析 application/x-www-form-urlencoded 表单。, Request, AppProtocol, _handle_connection(), 基于 socket 的 HTTP/1.1 服务器（仅标准库）。, 读取一个完整 HTTP 请求（含 body）。 (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (8): test_middlewares(), MiddlewareMixin, CustomErrorMiddleware, RateLimitMiddleware, 请求日志中间件 - 记录每个请求的详细信息, 安全头中间件 - 添加安全相关的HTTP头, RequestLoggingMiddleware, SecurityHeadersMiddleware

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (5): MethodNotAllowed, 路由表：支持精确路径与 /users/<id> 动态参数。, /users/<id>      -> ^/users/(?P<id>[^/]+)$         /files/<path:p>  -> ^/files/(, Route, Router

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (10): 03 · 纯 Python 实现 HTTP 框架, code:block1 (03-http框架/), code:sh (cd 03-http框架), code:sh (curl http://127.0.0.1:8000/), code:python (from minihttp import MiniHTTP), 与 `02-basic/14-网络` 的关系, 快速开始, 最小用法 (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (7): code:sh (pip freeze > requirements.txt), code:block2 (python your_script.py &), code:block3 (nohup python your_script.py &), code:python (import subprocess), 作用域, 依赖生成, 后台运行

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (7): code:bash (# 查看运行中的容器), code:bash (# 实时查看日志), code:bash (# 查看健康状态), 健康检查, 查看容器状态, 查看日志, 🔍 监控和日志

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 21 - "Community 21"
Cohesion: 0.33
Nodes (5): code:shell (./ll_env/bin/python -m pip install Django), code:shell (./ll_env/bin/django-admin startproject hello_world .), code:shell (./ll_env/bin/python manage.py runserver), code:shell (python manage.py startapp polls), code:block5 (app_name/)

## Knowledge Gaps
- **94 isolated node(s):** `Config`, `计算表达式，格式: 'a operator b`, `迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1`, `基于 socket 的 HTTP/1.1 服务器（仅标准库）。`, `读取一个完整 HTTP 请求（含 body）。` (+89 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MiniHTTP` connect `Community 1` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `MethodNotAllowed` connect `Community 6` to `Community 1`, `Community 7`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MiniHTTP` (e.g. with `Request` and `Response`) actually correct?**
  _`MiniHTTP` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Response` (e.g. with `AppProtocol` and `MiniHTTP`) actually correct?**
  _`Response` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `计算表达式，格式: 'a operator b`, `迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1` to the rest of the system?**
  _94 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._