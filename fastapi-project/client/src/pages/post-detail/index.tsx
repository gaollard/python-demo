import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  favoritePost,
  fetchPostDetail,
  likePost,
  unfavoritePost,
  unlikePost,
} from '../../apis/posts'
import { Empty } from '../../components/Empty'
import { BasicLayout } from '../../layout/BasicLayout'
import { useUserStore } from '../../store/user-store'
import type { PostDetail } from '../../types/api'
import { getApiErrorMessage } from '../../utils/api-error'
import { formatDateTime, formatRelative } from '../../utils/date'
import './index.less'

export function PostDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { hydrated, hydrate, token } = useUserStore()
  const [post, setPost] = useState<PostDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [acting, setActing] = useState<'like' | 'favorite' | null>(null)

  const postId = Number(id)

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    if (!Number.isFinite(postId) || postId <= 0) {
      setError('无效的帖子 ID')
      setLoading(false)
      return
    }

    let cancelled = false

    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetchPostDetail(postId)
        if (!cancelled) setPost(res.data)
      } catch (err) {
        if (!cancelled) {
          setPost(null)
          setError(getApiErrorMessage(err, '加载帖子失败'))
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void load()
    return () => {
      cancelled = true
    }
  }, [postId, token])

  const authed = Boolean(token)

  function requireAuth() {
    navigate('/login', { state: { from: `/posts/${postId}` } })
  }

  async function toggleLike() {
    if (!post) return
    if (!authed) {
      requireAuth()
      return
    }
    setActing('like')
    try {
      const res = post.liked
        ? await unlikePost(post.id)
        : await likePost(post.id)
      setPost((prev) =>
        prev
          ? {
              ...prev,
              liked: res.data.liked ?? !prev.liked,
              like_count: res.data.like_count ?? prev.like_count,
            }
          : prev
      )
    } catch (err) {
      setError(getApiErrorMessage(err, '操作失败'))
    } finally {
      setActing(null)
    }
  }

  async function toggleFavorite() {
    if (!post) return
    if (!authed) {
      requireAuth()
      return
    }
    setActing('favorite')
    try {
      const res = post.favorited
        ? await unfavoritePost(post.id)
        : await favoritePost(post.id)
      setPost((prev) =>
        prev
          ? {
              ...prev,
              favorited: res.data.favorited ?? !prev.favorited,
              favorite_count: res.data.favorite_count ?? prev.favorite_count,
            }
          : prev
      )
    } catch (err) {
      setError(getApiErrorMessage(err, '操作失败'))
    } finally {
      setActing(null)
    }
  }

  return (
    <BasicLayout>
      <article className="post-detail">
        <Link className="post-detail__back" to="/">
          返回列表
        </Link>

        {loading ? (
          <p className="post-detail__status">加载中…</p>
        ) : error && !post ? (
          <Empty
            title="无法打开帖子"
            description={error}
            extra={
              <Link className="post-detail__cta" to="/">
                回到首页
              </Link>
            }
          />
        ) : post ? (
          <>
            <header className="post-detail__header post-detail__reveal">
              <h1 className="post-detail__title">{post.title}</h1>
              <div className="post-detail__meta">
                <span className="post-detail__author">@{post.author.username}</span>
                <span aria-hidden="true">·</span>
                <time dateTime={post.created_at} title={formatDateTime(post.created_at)}>
                  {formatRelative(post.created_at) || formatDateTime(post.created_at)}
                </time>
              </div>
            </header>

            {error ? <p className="post-detail__error">{error}</p> : null}

            <div className="post-detail__content post-detail__reveal" style={{ animationDelay: 'var(--stagger-step)' }}>
              {post.content.split('\n').map((line, i) => (
                <p key={i}>{line || '\u00A0'}</p>
              ))}
            </div>

            {post.images && post.images.length > 0 ? (
              <div
                className="post-detail__images post-detail__reveal"
                style={{ animationDelay: 'calc(var(--stagger-step) * 1.5)' }}
              >
                {post.images.map((src) => (
                  <a
                    key={src}
                    className="post-detail__image"
                    href={src}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <img src={src} alt="" loading="lazy" />
                  </a>
                ))}
              </div>
            ) : null}

            <footer
              className="post-detail__actions post-detail__reveal"
              style={{ animationDelay: 'calc(var(--stagger-step) * 2)' }}
            >
              <button
                type="button"
                className={`post-detail__action${post.liked ? ' post-detail__action--on' : ''}`}
                disabled={acting !== null}
                onClick={() => void toggleLike()}
              >
                {post.liked ? '已赞' : '点赞'} · {post.like_count}
              </button>
              <button
                type="button"
                className={`post-detail__action${post.favorited ? ' post-detail__action--on' : ''}`}
                disabled={acting !== null}
                onClick={() => void toggleFavorite()}
              >
                {post.favorited ? '已收藏' : '收藏'} · {post.favorite_count}
              </button>
            </footer>
          </>
        ) : null}
      </article>
    </BasicLayout>
  )
}
