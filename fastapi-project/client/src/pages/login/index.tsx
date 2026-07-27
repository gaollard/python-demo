import { type FormEvent, useState } from 'react'
import { isAxiosError } from 'axios'
import { Link, useNavigate } from 'react-router-dom'
import { setAuthToken } from '../../utils/auth'
import { AuthLayout } from '../../layout/AuthLayout'
import { login as loginRequest } from '../../apis/auth'
import './index.less'

function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim())
}

export function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    const trimmed = email.trim()
    if (!trimmed || !password) {
      setError('请填写邮箱和密码')
      return
    }
    if (!isValidEmail(trimmed)) {
      setError('请输入有效的邮箱地址')
      return
    }

    setSubmitting(true)
    try {
      const res = await loginRequest({ email: trimmed, password })
      const token = res.data?.token
      if (token) {
        setAuthToken(token)
      }
      navigate('/', { replace: true })
    } catch (err: unknown) {
      let msg = '登录失败，请检查账号密码或稍后重试'
      if (isAxiosError(err)) {
        const data = err.response?.data as { message?: string } | undefined
        if (data?.message) msg = data.message
        else if (err.code === 'ECONNABORTED') msg = '请求超时，请稍后重试'
        else if (!err.response) msg = '网络异常，请检查连接后重试'
      }
      setError(msg)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthLayout>
      <div className="auth">
        <p className="auth__eyebrow">欢迎回来</p>
        <h1 className="auth__title">登录</h1>
        <p className="auth__lead">使用邮箱与密码登录你的账户</p>

        <form className="auth__form" onSubmit={handleSubmit} noValidate>
          {error ? <p className="auth__error">{error}</p> : null}

          <div className="auth__field">
            <label className="auth__label" htmlFor="login-email">
              邮箱
            </label>
            <input
              id="login-email"
              className="auth__input"
              type="email"
              name="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="auth__field">
            <label className="auth__label" htmlFor="login-password">
              密码
            </label>
            <input
              id="login-password"
              className="auth__input"
              type="password"
              name="password"
              autoComplete="current-password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="auth__row">
            <label className="auth__remember">
              <input
                type="checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
              />
              在此设备保持登录
            </label>
          </div>

          <button className="auth__submit" type="submit" disabled={submitting}>
            {submitting ? '登录中…' : '登录'}
          </button>
        </form>

        <div className="auth__footer">
          还没有账号？{' '}
          <Link className="auth__link" to="/register">
            注册
          </Link>
        </div>
      </div>
    </AuthLayout>
  )
}
