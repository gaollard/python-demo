# PyMySQL vs aiomysql

在 FastAPI + SQLAlchemy 项目中连接 MySQL，常见两种驱动：

| 驱动 | 类型 | SQLAlchemy URL 前缀 | 典型场景 |
|------|------|---------------------|----------|
| **PyMySQL** | 同步 | `mysql+pymysql://` | 脚本、同步 Web、后台任务 |
| **aiomysql** | 异步 | `mysql+aiomysql://` | FastAPI / 高并发 IO 型 API |

本项目的 `src/database.py` 使用的是 **aiomysql**。

---

## 1. 一句话区别

- **PyMySQL**：纯 Python 的同步 MySQL 客户端。调用时会**阻塞当前线程**，等数据库返回后才继续。
- **aiomysql**：基于 asyncio 的异步 MySQL 客户端（API 风格接近 PyMySQL）。用 `await` 发起查询，等待期间**不占用事件循环**，可处理其他请求。

两者协议层都是 MySQL，语法、参数、结果集概念基本一致；差别主要在**是否异步**以及如何与 FastAPI / SQLAlchemy 配合。

---

## 2. 为什么 FastAPI 更推荐 aiomysql

FastAPI 跑在 **ASGI + asyncio** 上：一个进程里用事件循环并发处理大量请求。

若在 `async def` 路由里用 **同步** PyMySQL / `create_engine`：

```python
# 反例：在 async 路由里跑同步 DB，会卡住事件循环
@app.get("/users")
async def get_users():
    conn = pymysql.connect(...)   # 阻塞
    cursor.execute("SELECT ...")  # 阻塞
    ...
```

数据库慢时，整个事件循环被堵住，其他请求也会变慢。

正确做法二选一：

1. **全程异步**（本项目采用）：`aiomysql` + `create_async_engine` + `AsyncSession` + `async def` 路由。
2. **同步路由 / 线程池**：用 PyMySQL，路由写成普通 `def`（FastAPI 会丢到线程池），或自己用 `run_in_executor`。适合迁移期或低并发。

高并发、IO 密集的 API，优先 **方案 1（aiomysql）**。

---

## 3. 与 SQLAlchemy 的对接方式

### 3.1 同步：PyMySQL

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://user:password@host:3306/dbname"
engine = create_engine(DATABASE_URL, pool_size=20, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)
```

依赖注入示例：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

路由用同步 `def`：

```python
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).limit(10).all()
```

安装：

```shell
pip install sqlalchemy pymysql
```

### 3.2 异步：aiomysql（本项目）

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+aiomysql://user:password@host:3306/dbname"
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,
    echo=False,
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

路由必须用 `async def`，并用 `await`：

```python
from sqlalchemy import select

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).limit(10))
    users = result.scalars().all()
    return {"users": [{"id": u.id, "name": u.name} for u in users]}
```

安装（见 `docs/02-安装.md`）：

```shell
pip install sqlalchemy aiomysql
```

要点：

- URL 必须是 `mysql+aiomysql://`，不能写成 `mysql+pymysql://` 再配异步引擎。
- 查询用 `await db.execute(...)`，不要用同步的 `db.query(...)`。
- `expire_on_commit=False` 可避免 commit 后访问属性时再触发懒加载（异步下懒加载容易踩坑）。

---

## 4. 对比一览

| 维度 | PyMySQL | aiomysql |
|------|---------|----------|
| 执行模型 | 同步，阻塞线程 | 异步，配合 asyncio |
| FastAPI 路由 | 适合 `def` | 适合 `async def` |
| SQLAlchemy | `create_engine` / `Session` | `create_async_engine` / `AsyncSession` |
| 连接串 | `mysql+pymysql://` | `mysql+aiomysql://` |
| 高并发 IO | 依赖多线程/多进程 | 单进程事件循环更高效 |
| API 熟悉度 | 文档多、生态成熟 | 与 PyMySQL 类似，异步写法需适应 |
| 适用场景 | 脚本、管理工具、同步服务 | FastAPI、异步微服务 |

---

## 5. 选型建议

| 场景 | 建议 |
|------|------|
| 新建 FastAPI + MySQL | **aiomysql** + SQLAlchemy 异步 |
| 已有大量同步 ORM / 脚本 | 继续 **PyMySQL**，或逐步拆出异步读写路径 |
| 简单 CRUD、QPS 很低 | 两者都行；团队更熟同步可先用 PyMySQL |
| 连接池、超时、回收 | 两边都要配 `pool_size` / `pool_recycle` 等，与驱动无关 |

本仓库选择 aiomysql，是为了和 FastAPI 的异步模型一致，避免在请求路径上阻塞事件循环。

---

## 6. 常见踩坑

1. **混用同步/异步**  
   `async def` 里直接调 PyMySQL，或对 `AsyncSession` 用同步 `query()`，都会出问题（卡死或运行时报错）。

2. **驱动装错 / URL 写错**  
   用了 `create_async_engine` 却写 `mysql+pymysql://`，或只装了 pymysql 没装 aiomysql，启动或首次查询会失败。

3. **密码特殊字符**  
   密码里有 `@`、`#` 等时要用 URL 编码（本项目用 `urllib.parse.quote_plus`）。

4. **懒加载（lazy load）**  
   异步 Session 下，离开 `await` 上下文后再访问未加载关系，容易触发 `MissingGreenlet`。应在查询时 `selectinload` / 一次查出需要的字段。

5. **连接被服务端断开**  
   MySQL 的 `wait_timeout` 可能导致空闲连接失效，设置 `pool_recycle`（本项目为 3600 秒）可缓解。

---

## 7. 和本项目代码的对应关系

| 文件 | 作用 |
|------|------|
| `src/database.py` | `mysql+aiomysql://`、异步引擎、连接池、`get_db` |
| `src/models/user.py` | ORM 模型（同步/异步共用同一套模型定义） |
| `src/main.py` | `/users` 使用 `AsyncSession` + `await db.execute` |

模型层（`DeclarativeBase` / `Mapped`）与驱动无关；换成 PyMySQL 时主要改的是 **引擎、Session、依赖注入和路由的 async/await**，而不是改表结构定义。
