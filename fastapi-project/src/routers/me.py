from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.response import ok
from ..database import get_db
from ..dependencies import get_current_user
from ..models import User
from ..services import post_service

router = APIRouter(prefix="/me", tags=["me"])

Page = Annotated[int, Query(ge=1)]
PageSize = Annotated[int, Query(ge=1, le=50)]


@router.get("/posts")
async def my_posts(
    page: Page = 1,
    page_size: PageSize = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = await post_service.list_posts(
        db,
        page=page,
        page_size=page_size,
        user_id=current_user.id,
    )
    return ok(
        {
            "items": [item.model_dump(mode="json") for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.get("/favorites")
async def my_favorites(
    page: Page = 1,
    page_size: PageSize = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = await post_service.list_my_favorites(
        db,
        current_user,
        page=page,
        page_size=page_size,
    )
    return ok(
        {
            "items": [item.model_dump(mode="json") for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )
