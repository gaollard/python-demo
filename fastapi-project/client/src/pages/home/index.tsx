import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchPosts } from '../../apis/posts'
import { Empty } from '../../components/Empty'
import { PageShell, Pagination, PostList } from '../../components/PostList'
import { BasicLayout } from '../../layout/BasicLayout'
import { useUserStore } from '../../store/user-store'
import type { PostListItem } from '../../types/api'
import { getApiErrorMessage } from '../../utils/api-error'
import './index.less'

const PAGE_SIZE = 20

export function Home() {
  const { hydrated, hydrate, token } = useUserStore()
  const [items, setItems] = useState<PostListItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    let cancelled = false

    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetchPosts({ page, page_size: PAGE_SIZE })
        if (cancelled) return
        setItems(res.data.items)
        setTotal(res.data.total)
      } catch (err) {
        if (!cancelled) {
          setError(getApiErrorMessage(err, '加载帖子失败'))
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
  }, [page])

  const authed = Boolean(token)

  return (
    <BasicLayout>
      <PageShell
        eyebrow="鱼泡论坛"
        title="最新帖子"
        lead="浏览公开讨论，登录后可发帖、点赞与收藏。"
        actions={
          authed ? (
            <Link className="home-page__cta" to="/posts/new">
              发布新帖
            </Link>
          ) : (
            <Link className="home-page__cta home-page__cta--ghost" to="/login">
              登录后发帖
            </Link>
          )
        }
      >
        {error ? <p className="home-page__error">{error}</p> : null}

        {loading ? (
          <p className="home-page__status">加载中…</p>
        ) : items.length === 0 ? (
          <Empty
            title="还没有帖子"
            description={authed ? '来发布第一篇讨论吧' : '登录后即可发帖'}
            extra={
              <Link className="home-page__cta" to={authed ? '/posts/new' : '/login'}>
                {authed ? '去发帖' : '去登录'}
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
