from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.logging import get_logger
from ..models import Post, PostFavorite, PostLike, User
from ..schemas import AuthorOut, InteractionOut, PostCreate, PostDetail, PostListItem

logger = get_logger(__name__)


def _to_list_item(post: Post) -> PostListItem:
    return PostListItem(
        id=post.id,
        title=post.title,
        author=AuthorOut(id=post.author.id, username=post.author.username),
        images=list(post.images or []),
        like_count=post.like_count,
        favorite_count=post.favorite_count,
        created_at=post.created_at,
    )


def _to_detail(
    post: Post,
    *,
    liked: bool | None = None,
    favorited: bool | None = None,
) -> PostDetail:
    return PostDetail(
        id=post.id,
        title=post.title,
        content=post.content,
        images=list(post.images or []),
        author=AuthorOut(id=post.author.id, username=post.author.username),
        like_count=post.like_count,
        favorite_count=post.favorite_count,
        created_at=post.created_at,
        liked=liked,
        favorited=favorited,
    )


async def create_post(db: AsyncSession, user: User, payload: PostCreate) -> PostDetail:
    post = Post(
        user_id=user.id,
        title=payload.title,
        content=payload.content,
        images=payload.images,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    post.author = user
    logger.info("Post created id=%s user_id=%s title=%s", post.id, user.id, post.title)
    return _to_detail(post, liked=False, favorited=False)


async def list_posts(
    db: AsyncSession,
    *,
    page: int,
    page_size: int,
    user_id: int | None = None,
) -> tuple[list[PostListItem], int]:
    filters = []
    if user_id is not None:
        filters.append(Post.user_id == user_id)

    total = await db.scalar(select(func.count()).select_from(Post).where(*filters)) or 0
    result = await db.scalars(
        select(Post)
        .where(*filters)
        .order_by(Post.created_at.desc(), Post.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    items = [_to_list_item(post) for post in result.all()]
    return items, total


async def get_post_detail(
    db: AsyncSession,
    post_id: int,
    current_user: User | None = None,
) -> PostDetail:
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        logger.warning("Post not found id=%s", post_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    liked: bool | None = None
    favorited: bool | None = None
    if current_user is not None:
        liked = (
            await db.scalar(
                select(PostLike.id).where(
                    PostLike.user_id == current_user.id,
                    PostLike.post_id == post_id,
                )
            )
            is not None
        )
        favorited = (
            await db.scalar(
                select(PostFavorite.id).where(
                    PostFavorite.user_id == current_user.id,
                    PostFavorite.post_id == post_id,
                )
            )
            is not None
        )
    return _to_detail(post, liked=liked, favorited=favorited)


async def _get_post_or_404(db: AsyncSession, post_id: int) -> Post:
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


async def like_post(db: AsyncSession, user: User, post_id: int) -> InteractionOut:
    post = await _get_post_or_404(db, post_id)
    existing = await db.scalar(
        select(PostLike).where(PostLike.user_id == user.id, PostLike.post_id == post_id)
    )
    if existing is None:
        db.add(PostLike(user_id=user.id, post_id=post_id))
        post.like_count += 1
        await db.commit()
        await db.refresh(post)
        logger.info("Post liked post_id=%s user_id=%s", post_id, user.id)

    return InteractionOut(
        post_id=post_id,
        liked=True,
        like_count=post.like_count,
    )


async def unlike_post(db: AsyncSession, user: User, post_id: int) -> InteractionOut:
    post = await _get_post_or_404(db, post_id)
    existing = await db.scalar(
        select(PostLike).where(PostLike.user_id == user.id, PostLike.post_id == post_id)
    )
    if existing is not None:
        await db.delete(existing)
        post.like_count = max(post.like_count - 1, 0)
        await db.commit()
        await db.refresh(post)
        logger.info("Post unliked post_id=%s user_id=%s", post_id, user.id)

    return InteractionOut(
        post_id=post_id,
        liked=False,
        like_count=post.like_count,
    )


async def favorite_post(db: AsyncSession, user: User, post_id: int) -> InteractionOut:
    post = await _get_post_or_404(db, post_id)
    existing = await db.scalar(
        select(PostFavorite).where(
            PostFavorite.user_id == user.id,
            PostFavorite.post_id == post_id,
        )
    )
    if existing is None:
        db.add(PostFavorite(user_id=user.id, post_id=post_id))
        post.favorite_count += 1
        await db.commit()
        await db.refresh(post)
        logger.info("Post favorited post_id=%s user_id=%s", post_id, user.id)

    return InteractionOut(
        post_id=post_id,
        favorited=True,
        favorite_count=post.favorite_count,
    )


async def unfavorite_post(db: AsyncSession, user: User, post_id: int) -> InteractionOut:
    post = await _get_post_or_404(db, post_id)
    existing = await db.scalar(
        select(PostFavorite).where(
            PostFavorite.user_id == user.id,
            PostFavorite.post_id == post_id,
        )
    )
    if existing is not None:
        await db.delete(existing)
        post.favorite_count = max(post.favorite_count - 1, 0)
        await db.commit()
        await db.refresh(post)
        logger.info("Post unfavorited post_id=%s user_id=%s", post_id, user.id)

    return InteractionOut(
        post_id=post_id,
        favorited=False,
        favorite_count=post.favorite_count,
    )


async def list_my_favorites(
    db: AsyncSession,
    user: User,
    *,
    page: int,
    page_size: int,
) -> tuple[list[PostListItem], int]:
    total = (
        await db.scalar(
            select(func.count())
            .select_from(PostFavorite)
            .where(PostFavorite.user_id == user.id)
        )
        or 0
    )
    result = await db.scalars(
        select(Post)
        .join(PostFavorite, PostFavorite.post_id == Post.id)
        .where(PostFavorite.user_id == user.id)
        .order_by(PostFavorite.created_at.desc(), PostFavorite.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    items = [_to_list_item(post) for post in result.all()]
    return items, total
