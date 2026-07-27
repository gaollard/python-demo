import { type FormEvent, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { createPost } from '../../apis/posts'
import { PageShell } from '../../components/PostList'
import { BasicLayout } from '../../layout/BasicLayout'
import { useUserStore } from '../../store/user-store'
import { getApiErrorMessage } from '../../utils/api-error'
import './index.less'

export function PostCreatePage() {
  const navigate = useNavigate()
  const { hydrated, hydrate, token } = useUserStore()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    if (hydrated && !token) {
      navigate('/login', { replace: true, state: { from: '/posts/new' } })
    }
  }, [hydrated, token, navigate])

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    const trimmedTitle = title.trim()
    const trimmedContent = content.trim()

    if (!trimmedTitle || !trimmedContent) {
      setError('请填写标题和正文')
      return
    }
    if (trimmedTitle.length > 100) {
      setError('标题不能超过 100 字')
      return
    }
    if (trimmedContent.length > 10000) {
      setError('正文不能超过 10000 字')
      return
    }

    setSubmitting(true)
    try {
      const res = await createPost({
        title: trimmedTitle,
        content: trimmedContent,
      })
      navigate(`/posts/${res.data.id}`, { replace: true })
    } catch (err) {
      setError(getApiErrorMessage(err, '发帖失败'))
    } finally {
      setSubmitting(false)
    }
  }

  if (!hydrated || !token) {
    return (
      <BasicLayout>
        <p className="post-create__status">正在跳转登录…</p>
      </BasicLayout>
    )
  }

  return (
    <BasicLayout>
      <PageShell
        eyebrow="写作"
        title="发布新帖"
        lead="标题简洁有力，正文把话说清楚。"
        actions={
          <Link className="post-create__cancel" to="/">
            取消
          </Link>
        }
      >
        <form className="post-create__form" onSubmit={handleSubmit} noValidate>
          {error ? <p className="post-create__error">{error}</p> : null}

          <div className="post-create__field">
            <label className="post-create__label" htmlFor="post-title">
              标题
            </label>
            <input
              id="post-title"
              className="post-create__input"
              type="text"
              maxLength={100}
              placeholder="一句话概括话题"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <span className="post-create__hint">{title.trim().length}/100</span>
          </div>

          <div className="post-create__field">
            <label className="post-create__label" htmlFor="post-content">
              正文
            </label>
            <textarea
              id="post-content"
              className="post-create__textarea"
              rows={12}
              maxLength={10000}
              placeholder="写下你的想法…"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
            <span className="post-create__hint">{content.trim().length}/10000</span>
          </div>

          <button className="post-create__submit" type="submit" disabled={submitting}>
            {submitting ? '发布中…' : '发布'}
          </button>
        </form>
      </PageShell>
    </BasicLayout>
  )
}
