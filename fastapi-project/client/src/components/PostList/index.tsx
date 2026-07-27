import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import type { PostListItem } from '../../types/api'
import { formatRelative } from '../../utils/date'
import './index.less'

type PostListProps = {
  items: PostListItem[]
  /** 入场动画起始延迟步进序号，可选 */
  staggerFrom?: number
}

export function PostList({ items, staggerFrom = 0 }: PostListProps) {
  return (
    <ul className="post-list">
      {items.map((post, index) => (
        <li
          key={post.id}
          className="post-list__item post-list__reveal"
          style={{
            animationDelay: `calc(var(--stagger-step) * ${staggerFrom + index})`,
          }}
        >
          <Link className="post-list__link" to={`/posts/${post.id}`}>
            <h2 className="post-list__title">{post.title}</h2>
            <div className="post-list__meta">
              <span className="post-list__author">@{post.author.username}</span>
              <span className="post-list__dot" aria-hidden="true">
                ·
              </span>
              <time dateTime={post.created_at}>
                {formatRelative(post.created_at) || post.created_at}
              </time>
            </div>
            <div className="post-list__stats">
              <span>{post.like_count} 赞</span>
              <span>{post.favorite_count} 收藏</span>
            </div>
          </Link>
        </li>
      ))}
    </ul>
  )
}

type PaginationProps = {
  page: number
  pageSize: number
  total: number
  onChange: (page: number) => void
  disabled?: boolean
}

export function Pagination({
  page,
  pageSize,
  total,
  onChange,
  disabled = false,
}: PaginationProps) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  if (totalPages <= 1) return null

  return (
    <div className="pagination" role="navigation" aria-label="分页">
      <button
        type="button"
        className="pagination__btn"
        disabled={disabled || page <= 1}
        onClick={() => onChange(page - 1)}
      >
        上一页
      </button>
      <span className="pagination__info">
        {page} / {totalPages}
      </span>
      <button
        type="button"
        className="pagination__btn"
        disabled={disabled || page >= totalPages}
        onClick={() => onChange(page + 1)}
      >
        下一页
      </button>
    </div>
  )
}

export function PageShell({
  eyebrow,
  title,
  lead,
  actions,
  children,
}: {
  eyebrow?: string
  title: string
  lead?: string
  actions?: ReactNode
  children: ReactNode
}) {
  return (
    <div className="page-shell">
      <header className="page-shell__header page-shell__reveal">
        {eyebrow ? <p className="page-shell__eyebrow">{eyebrow}</p> : null}
        <div className="page-shell__title-row">
          <h1 className="page-shell__title">{title}</h1>
          {actions ? <div className="page-shell__actions">{actions}</div> : null}
        </div>
        {lead ? <p className="page-shell__lead">{lead}</p> : null}
      </header>
      <div className="page-shell__body">{children}</div>
    </div>
  )
}
