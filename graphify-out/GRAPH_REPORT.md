# Graph Report - pythons  (2026-07-24)

## Corpus Check
- 180 files · ~24,953 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1118 nodes · 814 edges · 376 communities (337 shown, 39 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `72490912`
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
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 132|Community 132]]
- [[_COMMUNITY_Community 194|Community 194]]
- [[_COMMUNITY_Community 195|Community 195]]
- [[_COMMUNITY_Community 334|Community 334]]
- [[_COMMUNITY_Community 335|Community 335]]

## God Nodes (most connected - your core abstractions)
1. `MiniHTTP` - 18 edges
2. `Python HTTP Server Docker 部署指南` - 13 edges
3. `集合（Set）` - 13 edges
4. `集合（Set）` - 13 edges
5. `Response` - 11 edges
6. `元组的组包和解包` - 10 edges
7. `常用内置模块（按用途）` - 10 edges
8. `元组的组包和解包` - 10 edges
9. `元组的组包和解包` - 10 edges
10. `Request` - 9 edges

## Surprising Connections (you probably didn't know these)
- `AppProtocol` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/server.py → 03-http框架/minihttp/request.py
- `AppProtocol` --uses--> `Response`  [INFERRED]
  03-http框架/minihttp/server.py → 03-http框架/minihttp/response.py
- `MiniHTTP` --uses--> `Request`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/request.py
- `MiniHTTP` --uses--> `Response`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/response.py
- `MiniHTTP` --uses--> `MethodNotAllowed`  [INFERRED]
  03-http框架/minihttp/app.py → 03-http框架/minihttp/router.py

## Communities (376 total, 39 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (36): code:bash (# 构建镜像), code:bash (# 查看详细错误信息), code:bash (# 手动测试连接), code:yaml (services:), code:yaml (services:), code:bash (# 启动服务), code:bash (# 自定义端口映射), code:block4 (container/) (+28 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (12): Exception, MethodNotAllowed, 路由表：支持精确路径与 /users/<id> 动态参数。  路由规则在注册时编译成正则，匹配时抽出命名捕获组作为 path_params。, 路径存在、但当前 HTTP 方法未注册时抛出。, 单条路由：HTTP 方法集合 + 路径模板 + 处理函数。, /users/<id>      -> ^/users/(?P<id>[^/]+)$         /files/<path:p>  -> ^/files/(, 把路径模板编译成正则。          示例：             /users/<id>       -> ^/users/(?P<id>[^/]+)$, 方法与路径都匹配时返回参数字典，否则 None。 (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (27): code:python (# 花括号字面量), code:python (nums = [1, 2, 2, 3, 3, 3]), code:python (allowed = {"admin", "editor", "viewer"}), code:python (users_a = ["Alice", "Bob", "Carol"]), code:python (squares = {x * x for x in range(6)}), code:python (lst = [1, 2, 2, 3]), code:python (ok = {1, "a", (1, 2)}), code:python (s = {1, 2, 3}) (+19 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (27): code:python (# 花括号字面量), code:python (nums = [1, 2, 2, 3, 3, 3]), code:python (allowed = {"admin", "editor", "viewer"}), code:python (users_a = ["Alice", "Bob", "Carol"]), code:python (squares = {x * x for x in range(6)}), code:python (lst = [1, 2, 2, 3]), code:python (ok = {1, "a", (1, 2)}), code:python (s = {1, 2, 3}) (+19 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (22): 1. 系统与运行环境, 2. 时间与日期, 3. 数学与随机, 4. 字符串与数据格式, 5. 数据结构与迭代工具, 6. 文件、压缩与序列化, 7. 网络与并发, 8. 日志、调试与测试 (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (22): code:python (# 显式括号), code:python (points = [(0, 0), (1, 2), (3, 4)]), code:python (# 1. 数量不匹配), code:python (a, *rest = (1, 2, 3, 4)), code:python (def get_size():), code:python (point = (10, 20)), code:python (def get_user():), code:python (a, b = 1, 2) (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.1
Nodes (19): 03 · 纯 Python 实现 HTTP 框架, code:block1 (03-http框架/), code:sh (cd 03-http框架), code:sh (curl http://127.0.0.1:8000/), code:python (from minihttp import MiniHTTP), code:python (def get(self, path: str):), code:python (def route(self, path: str, methods: list[str] | None = None)), code:python (@app.get("/")) (+11 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (8): test_middlewares(), MiddlewareMixin, CustomErrorMiddleware, RateLimitMiddleware, 请求日志中间件 - 记录每个请求的详细信息, 安全头中间件 - 添加安全相关的HTTP头, RequestLoggingMiddleware, SecurityHeadersMiddleware

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (18): code:text (01module1/), code:python (from core import *), code:python (# core/__init__.py), code:python (import core), code:python (from core.logger import log), code:python (# 1. 导入包内模块，起别名), code:python (# core/app.py), code:bash (# 在项目根（能找到包的那一层）执行) (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (16): code:python (# 列表可以就地修改), code:python (t = ([1, 2], 3)), code:python (a = (1, 2, 3)), code:python (dimensions = (200, 50)), code:python (# 做字典的键), code:python (t = (10, 20, 30, 40)), code:python (lst = [1, 2, 3]), 何时用元组 (+8 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (12): code:python (from my import NAME          # 可以，即使 NAME 不在 __all__ 里), code:python (# my.py), code:python (# test.py), code:python (# utils.py（没有 __all__）), code:python (from utils import *), code:python (# mypkg/__init__.py), 作用, 包里的 `__all__` (+4 more)

### Community 15 - "Community 15"
Cohesion: 0.15
Nodes (12): code:python (# demo.py), code:bash (python demo.py          # 输出：__main__), code:python (# 在任意 .py 文件中), code:python (import math), code:python (# m.py), code:python (import m), `__dict__`：模块的命名空间, `__name__` 最常用 (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (11): access_log(), boom(), echo(), get_user(), hello(), 迷你 HTTP 框架示例。  运行：     cd 03-http框架     python example.py  测试：     curl http://1, 访问日志中间件：先放行到内层，再根据响应状态打印一行。, 演示查询参数：dict 返回值会自动转成 JSON。 (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.23
Nodes (6): MiniHTTP, 迷你 HTTP 框架，风格类似 Flask：          app = MiniHTTP("demo")          @app.get("/"), 迷你 HTTP 框架，风格类似 Flask：          app = MiniHTTP("demo")          @app.get("/"), 通用路由装饰器；get/post/... 都是它的语法糖。, 注册中间件：middleware(request, call_next) -> Response, 注册中间件：middleware(request, call_next) -> Response。          先注册的中间件在最外层（先看到请求、最后看

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (8): index(), 首页：直接返回 HTML Response。, html_response(), HTTP 响应对象与常用响应构造函数。  组装后的字节流形态：      HTTP/1.1 200 OK\\r\\n     Content-Type: app, 封装状态码、响应头与响应体，最终通过 to_bytes() 写出到 socket。, 设置或覆盖单个响应头（如 405 时的 Allow）。, 拼成符合 HTTP/1.1 的完整响应字节：状态行 + 头部 + 空行 + body。, Response

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (8): plain(), 演示显式构造 text Response。, 路由匹配 → 调 handler → 规范化返回值。, 把 handler 的多种返回值约定转成统一的 Response。          - Response          → 原样         - (b, 入口：包一层中间件链，再交给 _dispatch；未捕获异常统一 500。, json_response(), JSON 响应；ensure_ascii=False 保留中文可读性。, text_response()

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (6): 封装一次 HTTP 请求的解析结果，供路由处理函数使用。, 取某个查询参数的第一个值（多值时常用这种简化接口）。, 解析 application/x-www-form-urlencoded 表单。, 将请求体解析为 JSON（application/json）。, 解析 application/x-www-form-urlencoded 表单（每个字段取首值）。, Request

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (6): Calculator, call_math_function(), create_function_from_string(), create_function_with_exec(), create_partial_function(), 计算表达式，格式: 'a operator b

### Community 22 - "Community 22"
Cohesion: 0.24
Nodes (8): AppProtocol, _handle_connection(), 基于 socket 的 HTTP/1.1 服务器（仅标准库）。  职责很窄：accept 连接 → 读完整请求 → 调 app.handle → 写回响应。 协, server 只依赖 handle 方法，便于解耦（不必硬绑 MiniHTTP 类）。, 读取一个完整 HTTP 请求（含 body）。, 读取一个完整 HTTP 请求（含 body）。      TCP 是流式协议，一次 recv 不一定拿到完整报文，因此：     1. 先循环读到出现头部结束标, _recv_request(), Protocol

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (3): 应用入口：路由装饰器、中间件、请求分发。  调用链（自外向内）：      socket 收到字节       → Request.from_raw, 纯 Python 原生实现的迷你 HTTP 框架（仅依赖标准库）。  对外只暴露应用入口与请求/响应类型，内部模块拆分见同目录各文件。, HTTP 请求对象：解析请求行、请求头、查询参数与请求体。  一次完整请求在 TCP 字节流中的大致形态：      GET /api/hello?name=P

### Community 24 - "Community 24"
Cohesion: 0.2
Nodes (9): del t[0]      # TypeError, print(u.name)  # AttributeError, print(x)  # NameError: name 'x' is not defined, 但可以删整个名字, 元组不能删元素（不可变）, 删切片、步长切片, 多目标一起删, 正确写法 (+1 more)

### Community 28 - "Community 28"
Cohesion: 0.25
Nodes (7): code:sh (pip freeze > requirements.txt), code:block2 (python your_script.py &), code:block3 (nohup python your_script.py &), code:python (import subprocess), 作用域, 依赖生成, 后台运行

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (6): count_alpha(), count_score(), count_vowel(), 统计文本中字母的个数和字母的组合     :param text: 文本     :return: 字母的个数和字母的组合, 统计文本中元音字母的个数     :param text: 文本     :return: 元音字母的个数, 统计分数列表中最高分 最低分 和平均分     :param scores: 分数列表     :return: 最高分 最低分 和平均分

### Community 31 - "Community 31"
Cohesion: 0.48
Nodes (5): circle_area(), circle_diameter(), circle_perimeter(), define_val(), update_val()

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 36 - "Community 36"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 38 - "Community 38"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): count_alpha(), count_score(), count_vowel(), 统计文本中字母的个数和字母的组合     :param text: 文本     :return: 字母的个数和字母的组合, 统计文本中元音字母的个数     :param text: 文本     :return: 元音字母的个数, 统计分数列表中最高分 最低分 和平均分     :param scores: 分数列表     :return: 最高分 最低分 和平均分

### Community 40 - "Community 40"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (3): CustomHTTPRequestHandler, get_local_ip(), start_server()

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (6): code:python (match 表达式:), code:python (status = 404), code:python (day = "Sat"), code:python (point = (3, 5)), code:python (age = 20), code:python (# 序列)

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (4): getProductPrice(), getProductPrice3(), 返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2", :param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (5): code:shell (./ll_env/bin/python -m pip install Django), code:shell (./ll_env/bin/django-admin startproject hello_world .), code:shell (./ll_env/bin/python manage.py runserver), code:shell (python manage.py startapp polls), code:block5 (app_name/)

### Community 51 - "Community 51"
Cohesion: 0.33
Nodes (4): getProductPrice(), getProductPrice3(), 返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2", :param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量

### Community 55 - "Community 55"
Cohesion: 0.6
Nodes (3): add(), greet(), multiply()

### Community 58 - "Community 58"
Cohesion: 0.4
Nodes (4): 阻塞启动内置 socket 服务器（Ctrl+C 结束）。, 阻塞式启动 TCP 服务器；每个连接在独立线程中处理。      SO_REUSEADDR：进程退出后端口可立即再绑定（开发时常用）。     daemon 线, 阻塞式启动 TCP 服务器；每个连接在独立线程中处理。, serve()

### Community 59 - "Community 59"
Cohesion: 0.4
Nodes (4): 内置模块有哪些, 模块的定义, 模块的导入, 软件包 package

### Community 60 - "Community 60"
Cohesion: 0.4
Nodes (4): 修改已有全局变量, 可变对象：改内容不需要 global, 在函数里「创建」全局变量（模块里原先没有也可以）, 正确：

## Knowledge Gaps
- **281 isolated node(s):** `Config`, `:param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量`, `返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2"`, `计算圆的面积     :param radius: 圆的半径     :return: 圆的面积`, `统计文本中字母的个数和字母的组合     :param text: 文本     :return: 字母的个数和字母的组合` (+276 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MiniHTTP` connect `Community 17` to `Community 1`, `Community 18`, `Community 19`, `Community 20`, `Community 23`, `Community 58`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `MethodNotAllowed` connect `Community 1` to `Community 17`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MiniHTTP` (e.g. with `Request` and `Response`) actually correct?**
  _`MiniHTTP` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Response` (e.g. with `AppProtocol` and `MiniHTTP`) actually correct?**
  _`Response` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `:param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量`, `返回姓名、朋友列表和其他信息      :param name: 姓名     :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2"` to the rest of the system?**
  _281 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._