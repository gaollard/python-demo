import { type FormEvent, useEffect, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { AuthLayout } from '../../layout/AuthLayout'
import { useUserStore } from '../../store/user-store'
import { getApiErrorMessage } from '../../utils/api-error'
import './index.less'

const USERNAME_RE = /^[a-zA-Z0-9_]{3,32}$/

export function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login, loggingIn, hydrated, hydrate, token } = useUserStore()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const from =
    (location.state as { from?: string } | null)?.from &&
    typeof (location.state as { from?: string }).from === 'string'
      ? (location.state as { from: string }).from
      : '/'

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  useEffect(() => {
    if (hydrated && token) {
      navigate(from, { replace: true })
    }
  }, [hydrated, token, navigate, from])

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

    try {
      await login({ username: trimmed, password })
      navigate(from, { replace: true })
    } catch (err: unknown) {
      setError(getApiErrorMessage(err, '登录失败，请检查账号密码或稍后重试'))
    }
  }

  return (
    <AuthLayout>
      <div className="auth">
        <p className="auth__eyebrow">欢迎回来</p>
        <h1 className="auth__title">登录</h1>
        <p className="auth__lead">使用用户名与密码登录论坛</p>

        <form className="auth__form" onSubmit={handleSubmit} noValidate>
          {error ? <p className="auth__error">{error}</p> : null}

          <div className="auth__field">
            <label className="auth__label" htmlFor="login-username">
              用户名
            </label>
            <input
              id="login-username"
              className="auth__input"
              type="text"
              name="username"
              autoComplete="username"
              placeholder="your_name"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
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

          <button className="auth__submit" type="submit" disabled={loggingIn}>
            {loggingIn ? '登录中…' : '登录'}
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
