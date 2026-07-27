from redis.asyncio import ConnectionPool, Redis

from .core.config import get_settings

_pool: ConnectionPool | None = None
_client: Redis | None = None


async def init_redis() -> Redis:
    """Create the shared async Redis client (call once on app startup)."""
    global _pool, _client
    if _client is not None:
        return _client

    settings = get_settings()
    password = settings.redis_password or None
    _pool = ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        password=password,
        db=settings.redis_db,
        max_connections=settings.redis_max_connections,
        decode_responses=True,
    )
    _client = Redis(connection_pool=_pool)
    await _client.ping()
    return _client


async def close_redis() -> None:
    """Close Redis client and connection pool on app shutdown."""
    global _pool, _client
    if _client is not None:
        await _client.aclose()
        _client = None
    if _pool is not None:
        await _pool.aclose()
        _pool = None


def get_redis_client() -> Redis:
    if _client is None:
        raise RuntimeError("Redis is not initialized; call init_redis() first")
    return _client


async def get_redis():
    """FastAPI dependency that yields the shared Redis client."""
    yield get_redis_client()
