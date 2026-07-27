import { type ReactNode, useEffect } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useUserStore } from '../store/user-store'
import './BasicLayout.less'

export function BasicLayout({ children }: { children: ReactNode }) {
  const navigate = useNavigate()
  const { user, hydrated, hydrate, logout, token } = useUserStore()

  useEffect(() => {
    if (!hydrated) hydrate()
  }, [hydrated, hydrate])

  const authed = Boolean(token)

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="layout-basic">
      <header className="layout-basic__header">
        <div className="layout-basic__header-inner">
          <Link className="layout-basic__brand" to="/">
            <span className="layout-basic__brand-mark" aria-hidden="true">
              ◆
            </span>
            <span className="layout-basic__brand-text">鱼泡论坛</span>
          </Link>

          <nav className="layout-basic__nav" aria-label="主导航">
            <NavLink
              className={({ isActive }) =>
                `layout-basic__nav-link${isActive ? ' layout-basic__nav-link--active' : ''}`
              }
              to="/"
              end
            >
              帖子
            </NavLink>
            {authed ? (
              <>
                <NavLink
                  className={({ isActive }) =>
                    `layout-basic__nav-link${isActive ? ' layout-basic__nav-link--active' : ''}`
                  }
                  to="/posts/new"
                >
                  发帖
                </NavLink>
                <NavLink
                  className={({ isActive }) =>
                    `layout-basic__nav-link${isActive ? ' layout-basic__nav-link--active' : ''}`
                  }
                  to="/profile"
                >
                  {user?.username ?? '我的'}
                </NavLink>
                <button
                  type="button"
                  className="layout-basic__nav-btn"
                  onClick={handleLogout}
                >
                  退出
                </button>
              </>
            ) : (
              <>
                <NavLink
                  className={({ isActive }) =>
                    `layout-basic__nav-link${isActive ? ' layout-basic__nav-link--active' : ''}`
                  }
                  to="/login"
                >
                  登录
                </NavLink>
                <NavLink
                  className={({ isActive }) =>
                    `layout-basic__nav-link layout-basic__nav-link--accent${isActive ? ' layout-basic__nav-link--active' : ''}`
                  }
                  to="/register"
                >
                  注册
                </NavLink>
              </>
            )}
          </nav>
        </div>
      </header>

      <main className="layout-basic__main">{children}</main>
    </div>
  )
}
