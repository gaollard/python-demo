import type { ReactNode } from 'react'
import './BasicLayout.less'

export function BasicLayout({ children }: { children: ReactNode }) {
  return <div className="layout-basic">{children}</div>
}
