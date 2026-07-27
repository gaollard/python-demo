import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { fetchMyFavorites, fetchMyPosts } from '../../apis/me'
import { Empty } from '../../components/Empty'
import { PageShell, Pagination, PostList } from '../../components/PostList'
import { BasicLayout } from '../../layout/BasicLayout'
import { useUserStore } from '../../store/user-store'
import type { PostListItem } from '../../types/api'
import { getApiErrorMessage } from '../../utils/api-error'
import { formatDateTime } from '../../utils/date'
import './index.less'

type TabKey = 'posts' | 'favorites'

const PAGE_SIZE = 20

export function Profile() {
  const navigate = useNavigate()
  const { user, hydrated, hydrate, token, logout } = useUserStore()
  const [tab, setTab] = useState<TabKey>('posts')
  const [items, setItems] = useState<PostListItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    if (hydrated && !token) {
      navigate('/login', { replace: true, state: { from: '/profile' } })
    }
  }, [hydrated, token, navigate])

  useEffect(() => {
    setPage(1)
  }, [tab])

  useEffect(() => {
    if (!hydrated || !token) return

    let cancelled = false

    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res =
          tab === 'posts'
            ? await fetchMyPosts({ page, page_size: PAGE_SIZE })
            : await fetchMyFavorites({ page, page_size: PAGE_SIZE })
        if (cancelled) return
        setItems(res.data.items)
        setTotal(res.data.total)
      } catch (err) {
        if (!cancelled) {
          setError(getApiErrorMessage(err, '加载失败'))
          setItems([])
          setTotal(0)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void load()
    return () => {
      cancelled = true
    }
  }, [hydrated, token, tab, page])

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  if (!hydrated || !token) {
    return (
      <BasicLayout>
        <p className="profile__status">正在跳转登录…</p>
      </BasicLayout>
    )
  }

  return (
    <BasicLayout>
      <PageShell
        eyebrow="账户"
        title={user?.username ? `@${user.username}` : '我的'}
        lead="查看你发布的帖子与收藏。"
        actions={
          <button type="button" className="profile__logout" onClick={handleLogout}>
            退出登录
          </button>
        }
      >
        <section className="profile__card" aria-labelledby="profile-meta-heading">
          <h2 id="profile-meta-heading" className="profile__card-title">
            账户信息
          </h2>
          <dl className="profile__meta">
            <div className="profile__meta-row">
              <dt className="profile__meta-label">用户 ID</dt>
              <dd>
                <code className="profile__mono">{user?.id ?? '—'}</code>
              </dd>
            </div>
            <div className="profile__meta-row">
              <dt className="profile__meta-label">用户名</dt>
              <dd className="profile__meta-value">{user?.username ?? '—'}</dd>
            </div>
            <div className="profile__meta-row">
              <dt className="profile__meta-label">注册时间</dt>
              <dd className="profile__meta-value">
                {user?.created_at ? formatDateTime(user.created_at) : '—'}
              </dd>
            </div>
          </dl>
        </section>

        <div className="profile__tabs" role="tablist" aria-label="我的内容">
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'posts'}
            className={`profile__tab${tab === 'posts' ? ' profile__tab--active' : ''}`}
            onClick={() => setTab('posts')}
          >
            我的帖子
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'favorites'}
            className={`profile__tab${tab === 'favorites' ? ' profile__tab--active' : ''}`}
            onClick={() => setTab('favorites')}
          >
            我的收藏
          </button>
        </div>

        {error ? <p className="profile__error">{error}</p> : null}

        {loading ? (
          <p className="profile__status">加载中…</p>
        ) : items.length === 0 ? (
          <Empty
            title={tab === 'posts' ? '还没有发过帖' : '还没有收藏'}
            description={
              tab === 'posts' ? '去写一篇新帖吧' : '浏览帖子时可以收藏感兴趣的内容'
            }
            extra={
              <Link className="profile__cta" to={tab === 'posts' ? '/posts/new' : '/'}>
                {tab === 'posts' ? '去发帖' : '去逛逛'}
              </Link>
            }
          />
        ) : (
          <>
            <PostList items={items} />
            <Pagination
              page={page}
              pageSize={PAGE_SIZE}
              total={total}
              disabled={loading}
              onChange={setPage}
            />
          </>
        )}
      </PageShell>
    </BasicLayout>
  )
}
