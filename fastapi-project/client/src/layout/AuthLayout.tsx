import type { ReactNode } from 'react'
import './AuthLayout.less'

export function AuthLayout({ children }: { children: ReactNode }) {
  return <div className="layout-auth">{children}</div>
}
