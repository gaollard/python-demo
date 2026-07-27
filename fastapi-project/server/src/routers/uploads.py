from fastapi import APIRouter, Depends, File, UploadFile

from ..core.config import Settings, get_settings
from ..core.response import ok
from ..dependencies import get_current_user
from ..models import User
from ..schemas import ImageUploadOut
from ..services import upload_service

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/images")
async def upload_images(
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    _ = current_user
    urls = await upload_service.save_images(files, settings)
    return ok(ImageUploadOut(urls=urls).model_dump())
