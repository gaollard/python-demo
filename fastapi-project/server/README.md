# Forum API (FastAPI Demo)

轻量论坛后端，按 `prd/README.md` 实现：注册 / 登录 / 看帖 / 发帖 / 点赞 / 收藏。

## 快速开始

```bash
cd fastapi-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 填写数据库、Redis 与 JWT 配置
```

启动：

```bash
uvicorn src.main:app --reload --app-dir .
# 或在项目根目录：
fastapi dev src/main.py
```

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/

首次启动会通过 SQLAlchemy `create_all` 自动建表；也可手动执行 `sql/schema.sql`。
启动时会连接 Redis（`init_redis`），关闭时释放连接池。

> 若库中已有旧版 `user_tab(id, name)`，需先按新结构重建表（见 `sql/schema.sql`），否则字段不匹配。

## 主要接口

| 方法 | 路径 | 鉴权 |
|------|------|------|
| POST | `/api/v1/auth/register` | 否 |
| POST | `/api/v1/auth/login` | 否 |
| GET | `/api/v1/posts` | 否 |
| GET | `/api/v1/posts/{id}` | 可选 |
| POST | `/api/v1/posts` | 是 |
| POST/DELETE | `/api/v1/posts/{id}/like` | 是 |
| POST/DELETE | `/api/v1/posts/{id}/favorite` | 是 |
| GET | `/api/v1/me/posts` | 是 |
| GET | `/api/v1/me/favorites` | 是 |

统一响应：

```json
{ "code": 0, "message": "ok", "data": {} }
```

写接口请求头：`Authorization: Bearer <access_token>`

## 目录结构

```text
src/
  main.py            # 应用入口、异常处理、挂载路由
  database.py        # 异步引擎 / Session
  redis_client.py    # 异步 Redis 客户端 / 连接池
  dependencies.py    # JWT 鉴权依赖
  core/              # 配置、安全、统一响应
  models/            # SQLAlchemy ORM
  schemas/           # Pydantic 入参/出参
  services/          # 业务逻辑
  routers/           # HTTP 路由
prd/README.md        # 产品需求
sql/schema.sql       # MySQL 建表脚本
```

## 环境变量

见 `.env.example`：`DB_*`、`REDIS_*` 与 `JWT_*`。

业务代码中注入 Redis：

```python
from fastapi import Depends
from redis.asyncio import Redis

from src.redis_client import get_redis

@router.get("/example")
async def example(redis: Redis = Depends(get_redis)):
    await redis.set("key", "value", ex=60)
    return await redis.get("key")
```
