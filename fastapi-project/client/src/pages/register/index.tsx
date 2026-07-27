import { Link } from 'react-router-dom'
import { AuthLayout } from '../../layout/AuthLayout'
import './index.less'

export function Register() {
  return (
    <AuthLayout>
      <div className="auth">
        <p className="auth__eyebrow">新账户</p>
        <h1 className="auth__title">注册</h1>
        <p className="auth__lead">
          注册接口对接后，可在此完成账号创建。请先使用登录页。
        </p>
        <div className="auth__footer auth__footer--bare">
          <Link className="auth__link" to="/login">
            返回登录
          </Link>
        </div>
      </div>
    </AuthLayout>
  )
}
