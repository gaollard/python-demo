from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.response import ok
from ..database import get_db
from ..schemas import TokenOut, UserLogin, UserOut, UserRegister
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    user: UserOut = await auth_service.register_user(db, payload)
    return ok(user.model_dump(mode="json"))


@router.post("/login")
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    token: TokenOut = await auth_service.login_user(db, payload.username, payload.password)
    return ok(token.model_dump(mode="json"))
