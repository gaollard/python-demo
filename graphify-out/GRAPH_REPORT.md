# Graph Report - pythons  (2026-07-22)

## Corpus Check
- 154 files · ~22,383 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 756 nodes · 548 edges · 262 communities (236 shown, 26 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ecd961da`
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
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 136|Community 136]]
- [[_COMMUNITY_Community 137|Community 137]]
- [[_COMMUNITY_Community 220|Community 220]]
- [[_COMMUNITY_Community 221|Community 221]]

## God Nodes (most connected - your core abstractions)
1. `MiniHTTP` - 18 edges
2. `Python HTTP Server Docker 部署指南` - 13 edges
3. `集合（Set）` - 13 edges
4. `Response` - 11 edges
5. `元组的组包和解包` - 10 edges
6. `元组的组包和解包` - 10 edges
7. `Request` - 9 edges
8. `元组和列表的区别` - 9 edges
9. `元组和列表的区别` - 9 edges
10. `RequestLoggingMiddleware` - 7 edges

## Surprising Connections (you probably didn't know these)
- `AppProtocol` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/server.py → 03-http框架/minihttp/request.py
- `MiniHTTP` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/request.py
- `MiniHTTP` --uses--> `MethodNotAllowed`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py
- `MiniHTTP` --uses--> `Router`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py
- `index()` --calls--> `html_response()`  [INFERRED]
  03-http框架/example.py → 03-http框架/minihttp/response.py

## Communities (262 total, 26 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (37): index(), plain(), 首页：直接返回 HTML Response。, 演示显式构造 text Response。, MiniHTTP, 应用入口：路由装饰器、中间件、请求分发。  调用链（自外向内）：      socket 收到字节       → Request.from_raw, 路由匹配 → 调 handler → 规范化返回值。, 把 handler 的多种返回值约定转成统一的 Response。          - Response          → 原样         - (b (+29 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (36): code:bash (# 构建镜像), code:bash (# 查看详细错误信息), code:bash (# 手动测试连接), code:yaml (services:), code:yaml (services:), code:bash (# 启动服务), code:bash (# 自定义端口映射), code:block4 (container/) (+28 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (12): Exception, MethodNotAllowed, 路由表：支持精确路径与 /users/<id> 动态参数。  路由规则在注册时编译成正则，匹配时抽出命名捕获组作为 path_params。, 路径存在、但当前 HTTP 方法未注册时抛出。, 单条路由：HTTP 方法集合 + 路径模板 + 处理函数。, /users/<id>      -> ^/users/(?P<id>[^/]+)$         /files/<path:p>  -> ^/files/(, 把路径模板编译成正则。          示例：             /users/<id>       -> ^/users/(?P<id>[^/]+)$, 方法与路径都匹配时返回参数字典，否则 None。 (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (27): code:python (# 花括号字面量), code:python (nums = [1, 2, 2, 3, 3, 3]), code:python (allowed = {"admin", "editor", "viewer"}), code:python (users_a = ["Alice", "Bob", "Carol"]), code:python (squares = {x * x for x in range(6)}), code:python (lst = [1, 2, 2, 3]), code:python (ok = {1, "a", (1, 2)}), code:python (s = {1, 2, 3}) (+19 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (19): 03 · 纯 Python 实现 HTTP 框架, code:block1 (03-http框架/), code:sh (cd 03-http框架), code:sh (curl http://127.0.0.1:8000/), code:python (from minihttp import MiniHTTP), code:python (def get(self, path: str):), code:python (def route(self, path: str, methods: list[str] | None = None)), code:python (@app.get("/")) (+11 more)

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (8): test_middlewares(), MiddlewareMixin, CustomErrorMiddleware, RateLimitMiddleware, 请求日志中间件 - 记录每个请求的详细信息, 安全头中间件 - 添加安全相关的HTTP头, RequestLoggingMiddleware, SecurityHeadersMiddleware

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.17
Nodes (11): access_log(), boom(), echo(), get_user(), hello(), 迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1, 访问日志中间件：先放行到内层，再根据响应状态打印一行。, 演示查询参数：dict 返回值会自动转成 JSON。 (+3 more)

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (6): 封装一次 HTTP 请求的解析结果，供路由处理函数使用。, 取某个查询参数的第一个值（多值时常用这种简化接口）。, 解析 application/x-www-form-urlencoded 表单。, 将请求体解析为 JSON（application/json）。, 解析 application/x-www-form-urlencoded 表单（每个字段取首值）。, Request

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (9): del t[0]      # TypeError, print(u.name)  # AttributeError, print(x)  # NameError: name 'x' is not defined, 但可以删整个名字, 元组不能删元素（不可变）, 删切片、步长切片, 多目标一起删, 正确写法 (+1 more)

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (7): code:sh (pip freeze > requirements.txt), code:block2 (python your_script.py &), code:block3 (nohup python your_script.py &), code:python (import subprocess), 作用域, 依赖生成, 后台运行

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (6): count_alpha(), count_score(), count_vowel(), 统计文本中字母的个数和字母的组合     :param text: 文本     :return: 字母的个数和字母的组合, 统计文本中元音字母的个数     :param text: 文本     :return: 元音字母的个数, 统计分数列表中最高分 最低分 和平均分     :param scores: 分数列表     :return: 最高分 最低分 和平均分

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (4): getProductPrice(), getProductPrice3(), 返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2", :param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (5): code:shell (./ll_env/bin/python -m pip install Django), code:shell (./ll_env/bin/django-admin startproject hello_world .), code:shell (./ll_env/bin/python manage.py runserver), code:shell (python manage.py startapp polls), code:block5 (app_name/)

### Community 32 - "Community 32"
Cohesion: 0.4
Nodes (4): 修改已有全局变量, 可变对象：改内容不需要 global, 在函数里「创建」全局变量（模块里原先没有也可以）, 正确：

## Knowledge Gaps
- **192 isolated node(s):** `:param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量`, `返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2"`, `Config`, `计算圆的面积     :param radius: 圆的半径     :return: 圆的面积`, `统计文本中字母的个数和字母的组合     :param text: 文本     :return: 字母的个数和字母的组合` (+187 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MiniHTTP` connect `Community 0` to `Community 2`, `Community 11`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `MethodNotAllowed` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MiniHTTP` (e.g. with `Request` and `Response`) actually correct?**
  _`MiniHTTP` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Response` (e.g. with `AppProtocol` and `MiniHTTP`) actually correct?**
  _`Response` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `:param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量`, `返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2"`, `Config` to the rest of the system?**
  _192 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._