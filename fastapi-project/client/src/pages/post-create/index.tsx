import { type ChangeEvent, type FormEvent, useEffect, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { createPost } from '../../apis/posts'
import { uploadImages } from '../../apis/uploads'
import { PageShell } from '../../components/PostList'
import { BasicLayout } from '../../layout/BasicLayout'
import { useUserStore } from '../../store/user-store'
import { getApiErrorMessage } from '../../utils/api-error'
import './index.less'

const MAX_IMAGES = 9
const ACCEPT = 'image/jpeg,image/png,image/gif,image/webp'

type PreviewItem = {
  id: string
  file: File
  url: string
}

export function PostCreatePage() {
  const navigate = useNavigate()
  const { hydrated, hydrate, token } = useUserStore()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [previews, setPreviews] = useState<PreviewItem[]>([])
  const previewsRef = useRef(previews)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  previewsRef.current = previews

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    if (hydrated && !token) {
      navigate('/login', { replace: true, state: { from: '/posts/new' } })
    }
  }, [hydrated, token, navigate])

  useEffect(() => {
    return () => {
      for (const item of previewsRef.current) URL.revokeObjectURL(item.url)
    }
  }, [])

  function handlePickImages(e: ChangeEvent<HTMLInputElement>) {
    const picked = Array.from(e.target.files ?? [])
    e.target.value = ''
    if (!picked.length) return

    setError(null)
    setPreviews((prev) => {
      const room = MAX_IMAGES - prev.length
      if (room <= 0) {
        setError(`最多上传 ${MAX_IMAGES} 张图片`)
        return prev
      }
      const nextFiles = picked.slice(0, room)
      if (picked.length > room) {
        setError(`最多上传 ${MAX_IMAGES} 张图片，已截取前 ${room} 张`)
      }
      return [
        ...prev,
        ...nextFiles.map((file) => ({
          id: `${file.name}-${file.size}-${file.lastModified}-${Math.random()}`,
          file,
          url: URL.createObjectURL(file),
        })),
      ]
    })
  }

  function removePreview(id: string) {
    setPreviews((prev) => {
      const target = prev.find((p) => p.id === id)
      if (target) URL.revokeObjectURL(target.url)
      return prev.filter((p) => p.id !== id)
    })
  }

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
      let images: string[] = []
      if (previews.length > 0) {
        const uploaded = await uploadImages(previews.map((p) => p.file))
        images = uploaded.data.urls
      }
      const res = await createPost({
        title: trimmedTitle,
        content: trimmedContent,
        images,
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
        lead="标题简洁有力，正文把话说清楚，可附带图片。"
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

          <div className="post-create__field">
            <span className="post-create__label">图片（可选）</span>
            <div className="post-create__images">
              {previews.map((item) => (
                <div key={item.id} className="post-create__thumb">
                  <img src={item.url} alt="" />
                  <button
                    type="button"
                    className="post-create__thumb-remove"
                    aria-label="移除图片"
                    onClick={() => removePreview(item.id)}
                  >
                    ×
                  </button>
                </div>
              ))}
              {previews.length < MAX_IMAGES ? (
                <label className="post-create__add-image">
                  <input
                    type="file"
                    accept={ACCEPT}
                    multiple
                    onChange={handlePickImages}
                  />
                  <span>+</span>
                </label>
              ) : null}
            </div>
            <span className="post-create__hint">
              {previews.length}/{MAX_IMAGES} · jpeg/png/gif/webp · ≤5MB
            </span>
          </div>

          <button className="post-create__submit" type="submit" disabled={submitting}>
            {submitting ? '发布中…' : '发布'}
          </button>
        </form>
      </PageShell>
    </BasicLayout>
  )
}
