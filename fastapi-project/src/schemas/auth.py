from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

UsernameStr = Annotated[str, Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")]
PasswordStr = Annotated[str, Field(min_length=6, max_length=64)]


class UserRegister(BaseModel):
    username: UsernameStr
    password: PasswordStr


class UserLogin(BaseModel):
    username: UsernameStr
    password: PasswordStr


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class PostCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    content: Annotated[str, Field(min_length=1, max_length=10000)]

    @field_validator("title", "content")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("cannot be blank")
        return value


class AuthorOut(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}


class PostListItem(BaseModel):
    id: int
    title: str
    author: AuthorOut
    like_count: int
    favorite_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PostDetail(PostListItem):
    content: str
    liked: bool | None = None
    favorited: bool | None = None


class InteractionOut(BaseModel):
    post_id: int
    liked: bool | None = None
    favorited: bool | None = None
    like_count: int | None = None
    favorite_count: int | None = None
