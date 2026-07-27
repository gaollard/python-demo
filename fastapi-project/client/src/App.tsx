import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.less'
import { Link, Route, Routes } from 'react-router-dom'
import { Login } from './pages/login'
import { Profile } from './pages/profile'
import { Register } from './pages/register'
import { CopyButton } from './components/CopyButton'
import { Empty } from './components/Empty'

function Home() {
  const [count, setCount] = useState(0)

  return (
    <div className="home">
      <header className="home__masthead">
        <span className="home__brand" aria-hidden="true">
          ◆
        </span>
        <nav className="home__nav" aria-label="快捷导航">
          <Link className="home__nav-link" to="/login">
            登录
          </Link>
          <Link className="home__nav-link" to="/register">
            注册
          </Link>
          <Link className="home__nav-link home__nav-link--accent" to="/profile">
            资料
          </Link>
        </nav>
      </header>

      <section className="home__intro">
        <div>
        <p className="home__eyebrow home__reveal" style={{ animationDelay: '0ms' }}>
          Vite · React · 本地脚手架
        </p>
        <div className="home__hero home__reveal" style={{ animationDelay: 'var(--stagger-step)' }}>
          <img src={heroImg} className="home__hero-base" width="170" height="179" alt="" />
          <img src={reactLogo} className="home__hero-framework" alt="React logo" />
          <img src={viteLogo} className="home__hero-vite" alt="Vite logo" />
        </div>
        <div className="home__intro-copy">
          <h1 className="home__title home__reveal" style={{ animationDelay: 'calc(var(--stagger-step) * 2)' }}>
            快速开始
          </h1>
          <p className="home__intro-desc home__reveal" style={{ animationDelay: 'calc(var(--stagger-step) * 3)' }}>
            编辑 <code>src/App.tsx</code> 并保存以体验 <code>HMR</code>
          </p>
        </div>
        </div>

        <div className="home__actions home__reveal" style={{ animationDelay: 'calc(var(--stagger-step) * 4)' }}>
          <button type="button" className="home__counter" onClick={() => setCount((c) => c + 1)}>
            Count is {count}
          </button>
          <CopyButton text="Hello, world!" onCopy={() => console.log('Copied!')} />
          <Empty className="home__empty home__reveal" compact description="占位组件演示" style={{ animationDelay: 'calc(var(--stagger-step) * 5)' }} />
        </div>
      </section>

      <section className="home__panels" aria-label="文档与社区">
        <div className="home__column home__column--docs">
          <div className="home__column-head">
            <svg className="home__panel-icon" role="presentation" aria-hidden="true">
              <use href="/icons.svg#documentation-icon"></use>
            </svg>
            <h2>文档</h2>
          </div>
          <p className="home__column-lead">常用参考与深入学习</p>
          <ul className="home__links">
            <li>
              <a className="home__link" href="https://vite.dev/" target="_blank" rel="noreferrer">
                <img className="home__logo" src={viteLogo} alt="" />
                Explore Vite
              </a>
            </li>
            <li>
              <a className="home__link" href="https://react.dev/" target="_blank" rel="noreferrer">
                <img className="home__link-icon" src={reactLogo} alt="" />
                Learn more
              </a>
            </li>
          </ul>
        </div>
        <div className="home__column home__column--social">
          <div className="home__column-head">
            <svg className="home__panel-icon" role="presentation" aria-hidden="true">
              <use href="/icons.svg#social-icon"></use>
            </svg>
            <h2>社区</h2>
          </div>
          <p className="home__column-lead">加入 Vite 开源社区</p>
          <ul className="home__links">
            <li>
              <a className="home__link" href="https://github.com/vitejs/vite" target="_blank" rel="noreferrer">
                <svg className="home__link-icon" role="presentation" aria-hidden="true">
                  <use href="/icons.svg#github-icon"></use>
                </svg>
                GitHub
              </a>
            </li>
            <li>
              <a className="home__link" href="https://chat.vite.dev/" target="_blank" rel="noreferrer">
                <svg className="home__link-icon" role="presentation" aria-hidden="true">
                  <use href="/icons.svg#discord-icon"></use>
                </svg>
                Discord
              </a>
            </li>
            <li>
              <a className="home__link" href="https://x.com/vite_js" target="_blank" rel="noreferrer">
                <svg className="home__link-icon" role="presentation" aria-hidden="true">
                  <use href="/icons.svg#x-icon"></use>
                </svg>
                X.com
              </a>
            </li>
            <li>
              <a className="home__link" href="https://bsky.app/profile/vite.dev" target="_blank" rel="noreferrer">
                <svg className="home__link-icon" role="presentation" aria-hidden="true">
                  <use href="/icons.svg#bluesky-icon"></use>
                </svg>
                Bluesky
              </a>
            </li>
          </ul>
        </div>
      </section>

      <footer className="home__foot" aria-hidden="true" />
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<Profile />} />
    </Routes>
  )
}

export default App
