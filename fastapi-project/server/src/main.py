import time
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.config import get_settings
from .core.logging import get_logger, set_request_id, setup_logging
from .core.response import fail
from .database import engine
from .models import Base
from .redis_client import close_redis, get_redis, init_redis
from .routers import auth, me, posts, uploads
from .services.upload_service import resolve_upload_dir

REQUEST_ID_HEADER = "X-Request-ID"

settings = get_settings()
setup_logging(settings.log_level)
logger = get_logger(__name__)


# lifespan: 生命周期管理
@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(
        "Starting %s v%s (log_level=%s)",
        settings.app_title,
        settings.app_version,
        settings.log_level,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured")

    upload_path = resolve_upload_dir(settings)
    logger.info("Upload directory ready: %s", upload_path)

    await init_redis()
    logger.info(
        "Redis connected: %s:%s/%s",
        settings.redis_host,
        settings.redis_port,
        settings.redis_db,
    )
    try:
        yield
    finally:
        await close_redis()
        logger.info("Redis closed; shutting down")


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(me.router, prefix="/api/v1")
app.include_router(uploads.router, prefix="/api/v1")

upload_dir = resolve_upload_dir(settings)
app.mount(
    f"{settings.media_url_prefix.rstrip('/')}/uploads",
    StaticFiles(directory=str(upload_dir)),
    name="media",
)


@app.middleware("http")
async def request_id_and_log(request: Request, call_next):
    incoming = request.headers.get(REQUEST_ID_HEADER, "").strip()
    request_id = incoming or uuid.uuid4().hex
    set_request_id(request_id)
    request.state.request_id = request_id

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers[REQUEST_ID_HEADER] = request_id
    logger.info(
        "%s %s -> %s %.1fms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/")
async def health(redis: Redis = Depends(get_redis)):
    redis_ok = False
    try:
        redis_ok = bool(await redis.ping())
    except Exception:
        logger.exception("Health check Redis ping failed")
        redis_ok = False
    status = "ok" if redis_ok else "degraded"
    logger.debug("Health check status=%s redis=%s", status, redis_ok)
    return {
        "status": status,
        "service": settings.app_title,
        "version": settings.app_version,
        "redis": "ok" if redis_ok else "unavailable",
    }


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    message = detail if isinstance(detail, str) else str(detail)
    logger.warning(
        "HTTP %s %s %s: %s",
        exc.status_code,
        request.method,
        request.url.path,
        message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=fail(code=exc.status_code, message=message),
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "Validation error %s %s: %s",
        request.method,
        request.url.path,
        exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content=fail(code=422, message="Validation error", data=exc.errors()),
    )
