from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.config import get_settings
from .core.response import fail
from .database import engine
from .models import Base
from .redis_client import close_redis, get_redis, init_redis
from .routers import auth, me, posts, uploads
from .services.upload_service import resolve_upload_dir


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    resolve_upload_dir(settings)
    await init_redis()
    try:
        yield
    finally:
        await close_redis()


settings = get_settings()
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


@app.get("/")
async def health(redis: Redis = Depends(get_redis)):
    redis_ok = False
    try:
        redis_ok = bool(await redis.ping())
    except Exception:
        redis_ok = False
    return {
        "status": "ok" if redis_ok else "degraded",
        "service": settings.app_title,
        "version": settings.app_version,
        "redis": "ok" if redis_ok else "unavailable",
    }


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    detail = exc.detail
    message = detail if isinstance(detail, str) else str(detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=fail(code=exc.status_code, message=message),
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=fail(code=422, message="Validation error", data=exc.errors()),
    )
