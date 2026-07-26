import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 在读取环境变量之前加载 .env（相对项目根目录，不依赖 cwd）
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_user = os.getenv("DB_USERNAME")
_password = quote_plus(os.getenv("DB_PASSWORD") or "")
_host = os.getenv("DB_HOST")
_port = os.getenv("DB_PORT")
_database = os.getenv("DB_DATABASE")

# 使用 aiomysql 驱动的异步连接字符串
DATABASE_URL = f"mysql+aiomysql://{_user}:{_password}@{_host}:{_port}/{_database}"

# 创建异步引擎，并配置连接池
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,        # 常驻连接数
    max_overflow=10,     # 峰值时额外连接数
    pool_recycle=3600,   # 连接回收时间(秒)，避免超时断开
    echo=False           # 生产环境关闭SQL日志
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 依赖注入：为每个请求提供独立的数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
