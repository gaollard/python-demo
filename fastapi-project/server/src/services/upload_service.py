import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from ..core.config import Settings
from ..core.logging import get_logger

logger = get_logger(__name__)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


def resolve_upload_dir(settings: Settings) -> Path:
    path = Path(settings.upload_dir)
    if not path.is_absolute():
        # server/src/services -> server/
        path = Path(__file__).resolve().parent.parent.parent / path
    path.mkdir(parents=True, exist_ok=True)
    return path


async def save_images(files: list[UploadFile], settings: Settings) -> list[str]:
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one image is required",
        )
    if len(files) > settings.upload_max_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"At most {settings.upload_max_files} images per request",
        )

    upload_dir = resolve_upload_dir(settings)
    urls: list[str] = []

    for file in files:
        content_type = (file.content_type or "").lower()
        ext = ALLOWED_CONTENT_TYPES.get(content_type)
        if ext is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only jpeg/png/gif/webp images are allowed",
            )

        data = await file.read()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file is not allowed",
            )
        if len(data) > settings.upload_max_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Each image must be <= {settings.upload_max_bytes // (1024 * 1024)}MB",
            )

        filename = f"{uuid.uuid4().hex}{ext}"
        dest = upload_dir / filename
        dest.write_bytes(data)
        urls.append(f"{settings.media_url_prefix.rstrip('/')}/uploads/{filename}")
        logger.info("Image saved file=%s size=%s", filename, len(data))

    logger.info("Uploaded %s image(s)", len(urls))
    return urls
