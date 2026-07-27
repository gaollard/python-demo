from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = "post_tab"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_tab.id"), index=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    images: Mapped[list[Any]] = mapped_column(JSON, default=list, server_default="[]")
    like_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    favorite_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    author = relationship("User", lazy="joined")


class PostLike(Base):
    __tablename__ = "post_like_tab"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uk_like_user_post"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_tab.id"), index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post_tab.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )


class PostFavorite(Base):
    __tablename__ = "post_favorite_tab"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uk_favorite_user_post"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_tab.id"), index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post_tab.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )
