import { type FormEvent, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register as registerRequest } from '../../apis/auth'
import { AuthLayout } from '../../layout/AuthLayout'
import { useUserStore } from '../../store/user-store'
import { getApiErrorMessage } from '../../utils/api-error'
import './index.less'

const USERNAME_RE = /^[a-zA-Z0-9_]{3,32}$/

export function Register() {
  const navigate = useNavigate()
  const { hydrated, hydrate, token, login } = useUserStore()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    if (hydrated && token) {
      navigate('/', { replace: true })
    }
  }, [hydrated, token, navigate])

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    const trimmed = username.trim()
    if (!trimmed || !password) {
      setError('请填写用户名和密码')
      return
    }
    if (!USERNAME_RE.test(trimmed)) {
      setError('用户名需为 3–32 位字母、数字或下划线')
      return
    }
    if (password.length < 6 || password.length > 64) {
      setError('密码长度为 6–64 位')
      return
    }
    if (password !== confirm) {
      setError('两次输入的密码不一致')
      return
    }

    setSubmitting(true)
    try {
      await registerRequest({ username: trimmed, password })
      await login({ username: trimmed, password })
      navigate('/', { replace: true })
    } catch (err: unknown) {
      setError(getApiErrorMessage(err, '注册失败，请稍后重试'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthLayout>
      <div className="auth">
        <p className="auth__eyebrow">新账户</p>
        <h1 className="auth__title">注册</h1>
        <p className="auth__lead">创建账号后即可发帖、点赞与收藏</p>

        <form className="auth__form" onSubmit={handleSubmit} noValidate>
          {error ? <p className="auth__error">{error}</p> : null}

          <div className="auth__field">
            <label className="auth__label" htmlFor="register-username">
              用户名
            </label>
            <input
              id="register-username"
              className="auth__input"
              type="text"
              name="username"
              autoComplete="username"
              placeholder="3–32 位字母数字下划线"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="auth__field">
            <label className="auth__label" htmlFor="register-password">
              密码
            </label>
            <input
              id="register-password"
              className="auth__input"
              type="password"
              name="password"
              autoComplete="new-password"
              placeholder="至少 6 位"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="auth__field">
            <label className="auth__label" htmlFor="register-confirm">
              确认密码
            </label>
            <input
              id="register-confirm"
              className="auth__input"
              type="password"
              name="confirm"
              autoComplete="new-password"
              placeholder="再次输入密码"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
            />
          </div>

          <button className="auth__submit" type="submit" disabled={submitting}>
            {submitting ? '注册中…' : '注册'}
          </button>
        </form>

        <div className="auth__footer">
          已有账号？{' '}
          <Link className="auth__link" to="/login">
            登录
          </Link>
        </div>
      </div>
    </AuthLayout>
  )
}
