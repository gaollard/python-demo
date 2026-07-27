from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.response import ok
from ..database import get_db
from ..dependencies import get_current_user, get_optional_user
from ..models import User
from ..schemas import PostCreate
from ..services import post_service

router = APIRouter(prefix="/posts", tags=["posts"])

Page = Annotated[int, Query(ge=1)]
PageSize = Annotated[int, Query(ge=1, le=50)]


@router.get("")
async def list_posts(
    page: Page = 1,
    page_size: PageSize = 20,
    db: AsyncSession = Depends(get_db),
):
    items, total = await post_service.list_posts(db, page=page, page_size=page_size)
    return ok(
        {
            "items": [item.model_dump(mode="json") for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    detail = await post_service.get_post_detail(db, post_id, current_user)
    return ok(detail.model_dump(mode="json"))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = await post_service.create_post(db, current_user, payload)
    return ok(detail.model_dump(mode="json"))


@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await post_service.like_post(db, current_user, post_id)
    return ok(result.model_dump(mode="json", exclude_none=True))


@router.delete("/{post_id}/like")
async def unlike_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await post_service.unlike_post(db, current_user, post_id)
    return ok(result.model_dump(mode="json", exclude_none=True))


@router.post("/{post_id}/favorite")
async def favorite_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await post_service.favorite_post(db, current_user, post_id)
    return ok(result.model_dump(mode="json", exclude_none=True))


@router.delete("/{post_id}/favorite")
async def unfavorite_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await post_service.unfavorite_post(db, current_user, post_id)
    return ok(result.model_dump(mode="json", exclude_none=True))
