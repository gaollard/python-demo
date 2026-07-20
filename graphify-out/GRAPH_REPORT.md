# Graph Report - pythons  (2026-07-20)

## Corpus Check
- 130 files · ~19,857 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 527 nodes · 396 edges · 184 communities (164 shown, 20 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06bbf0ce`
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
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 120|Community 120]]
- [[_COMMUNITY_Community 121|Community 121]]
- [[_COMMUNITY_Community 142|Community 142]]
- [[_COMMUNITY_Community 143|Community 143]]

## God Nodes (most connected - your core abstractions)
1. `MiniHTTP` - 18 edges
2. `Python HTTP Server Docker 部署指南` - 13 edges
3. `Response` - 11 edges
4. `元组的组包和解包` - 10 edges
5. `Request` - 9 edges
6. `元组和列表的区别` - 9 edges
7. `RequestLoggingMiddleware` - 7 edges
8. `RateLimitMiddleware` - 7 edges
9. `03 · 纯 Python 实现 HTTP 框架` - 7 edges
10. `AppProtocol` - 6 edges

## Surprising Connections (you probably didn't know these)
- `AppProtocol` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/server.py → 03-http框架/minihttp/request.py
- `AppProtocol` --uses--> `Response`  [INFERRED]
  03-http框架/minihttp/server.py → 03-http框架/minihttp/response.py
- `MiniHTTP` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/request.py
- `MiniHTTP` --uses--> `MethodNotAllowed`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py
- `MiniHTTP` --uses--> `Router`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py

## Communities (184 total, 20 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (36): code:bash (# 构建镜像), code:bash (# 查看详细错误信息), code:bash (# 手动测试连接), code:yaml (services:), code:yaml (services:), code:bash (# 启动服务), code:bash (# 自定义端口映射), code:block4 (container/) (+28 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (22): index(), plain(), 首页：直接返回 HTML Response。, 演示显式构造 text Response。, MiniHTTP, 路由匹配 → 调 handler → 规范化返回值。, 把 handler 的多种返回值约定转成统一的 Response。          - Response          → 原样         - (b, 迷你 HTTP 框架，风格类似 Flask：          app = MiniHTTP("demo")          @app.get("/") (+14 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (15): 应用入口：路由装饰器、中间件、请求分发。  调用链（自外向内）：      socket 收到字节       → Request.from_raw, 阻塞启动内置 socket 服务器（Ctrl+C 结束）。, 纯 Python 原生实现的迷你 HTTP 框架（仅依赖标准库）。  对外只暴露应用入口与请求/响应类型，内部模块拆分见同目录各文件。, HTTP 请求对象：解析请求行、请求头、查询参数与请求体。  一次完整请求在 TCP 字节流中的大致形态：      GET /api/hello?name=P, AppProtocol, _handle_connection(), 基于 socket 的 HTTP/1.1 服务器（仅标准库）。  职责很窄：accept 连接 → 读完整请求 → 调 app.handle → 写回响应。 协, 阻塞式启动 TCP 服务器；每个连接在独立线程中处理。      SO_REUSEADDR：进程退出后端口可立即再绑定（开发时常用）。     daemon 线 (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (19): 03 · 纯 Python 实现 HTTP 框架, code:block1 (03-http框架/), code:sh (cd 03-http框架), code:sh (curl http://127.0.0.1:8000/), code:python (from minihttp import MiniHTTP), code:python (def get(self, path: str):), code:python (def route(self, path: str, methods: list[str] | None = None)), code:python (@app.get("/")) (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (10): MethodNotAllowed, 路由表：支持精确路径与 /users/<id> 动态参数。  路由规则在注册时编译成正则，匹配时抽出命名捕获组作为 path_params。, 路径存在、但当前 HTTP 方法未注册时抛出。, 单条路由：HTTP 方法集合 + 路径模板 + 处理函数。, /users/<id>      -> ^/users/(?P<id>[^/]+)$         /files/<path:p>  -> ^/files/(, 把路径模板编译成正则。          示例：             /users/<id>       -> ^/users/(?P<id>[^/]+)$, 方法与路径都匹配时返回参数字典，否则 None。, 解析 (method, path) → (handler, path_params)。          - 路径与方法都匹配：返回处理函数与参数 (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (8): test_middlewares(), MiddlewareMixin, CustomErrorMiddleware, RateLimitMiddleware, 请求日志中间件 - 记录每个请求的详细信息, 安全头中间件 - 添加安全相关的HTTP头, RequestLoggingMiddleware, SecurityHeadersMiddleware

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.17
Nodes (11): access_log(), boom(), echo(), get_user(), hello(), 迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1, 访问日志中间件：先放行到内层，再根据响应状态打印一行。, 演示查询参数：dict 返回值会自动转成 JSON。 (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (6): 封装一次 HTTP 请求的解析结果，供路由处理函数使用。, 取某个查询参数的第一个值（多值时常用这种简化接口）。, 解析 application/x-www-form-urlencoded 表单。, 将请求体解析为 JSON（application/json）。, 解析 application/x-www-form-urlencoded 表单（每个字段取首值）。, Request

### Community 13 - "Community 13"
Cohesion: 0.25
Nodes (7): code:sh (pip freeze > requirements.txt), code:block2 (python your_script.py &), code:block3 (nohup python your_script.py &), code:python (import subprocess), 作用域, 依赖生成, 后台运行

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (5): code:shell (./ll_env/bin/python -m pip install Django), code:shell (./ll_env/bin/django-admin startproject hello_world .), code:shell (./ll_env/bin/python manage.py runserver), code:shell (python manage.py startapp polls), code:block5 (app_name/)

## Knowledge Gaps
- **133 isolated node(s):** `Config`, `计算表达式，格式: 'a operator b`, `迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1`, `访问日志中间件：先放行到内层，再根据响应状态打印一行。`, `首页：直接返回 HTML Response。` (+128 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MiniHTTP` connect `Community 1` to `Community 9`, `Community 2`, `Community 5`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `MethodNotAllowed` connect `Community 5` to `Community 1`, `Community 10`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `Response` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MiniHTTP` (e.g. with `Request` and `Response`) actually correct?**
  _`MiniHTTP` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Response` (e.g. with `AppProtocol` and `MiniHTTP`) actually correct?**
  _`Response` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Request` (e.g. with `AppProtocol` and `MiniHTTP`) actually correct?**
  _`Request` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `计算表达式，格式: 'a operator b`, `迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1` to the rest of the system?**
  _133 weakly-connected nodes found - possible documentation gaps or missing edges._