import { Link } from 'react-router-dom'
import { BasicLayout } from '../../layout/BasicLayout'
import './index.less'

export function Profile() {
  return (
    <BasicLayout>
      <div className="profile">
        <div className="profile__ribbon" aria-hidden="true" />
        <header className="profile__header">
          <p className="profile__eyebrow">账户</p>
          <h1 className="profile__title">个人资料</h1>
          <p className="profile__lead">账户信息与偏好（演示）</p>
          <nav className="profile__toolbar" aria-label="页面操作">
            <Link className="profile__toolbar-link" to="/">
              返回首页
            </Link>
          </nav>
        </header>

        <section className="profile__card" aria-labelledby="profile-meta-heading">
          <h2 id="profile-meta-heading" className="profile__card-title">
            元数据
          </h2>
          <dl className="profile__meta">
            <div className="profile__meta-row">
              <dt className="profile__meta-label">用户 ID</dt>
              <dd>
                <code className="profile__mono">—</code>
              </dd>
            </div>
            <div className="profile__meta-row">
              <dt className="profile__meta-label">会话</dt>
              <dd className="profile__meta-value">登录后展示</dd>
            </div>
          </dl>
        </section>
      </div>
    </BasicLayout>
  )
}
