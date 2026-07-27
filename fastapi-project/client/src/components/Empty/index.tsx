import { type HTMLAttributes, type ReactNode } from 'react'
import { EmptyIllustration } from './icons'
import './index.less'

export type EmptyProps = Omit<HTMLAttributes<HTMLDivElement>, 'title'> & {
  /** 主标题，默认「暂无数据」 */
  title?: ReactNode
  /** 辅助说明 */
  description?: ReactNode
  /** 替换默认插画 */
  illustration?: ReactNode
  /** 是否隐藏插画 */
  hideIllustration?: boolean
  /** 底部操作区（按钮、链接等） */
  extra?: ReactNode
  /** 紧凑布局，更少内边距 */
  compact?: boolean
}

export function Empty({
  title = '暂无数据',
  description,
  illustration,
  hideIllustration = false,
  extra,
  compact = false,
  className,
  ...rest
}: EmptyProps) {
  const mergedClass = ['empty', compact ? 'empty--compact' : '', className ?? '']
    .filter(Boolean)
    .join(' ')

  return (
    <div {...rest} className={mergedClass} role="status">
      {!hideIllustration ? illustration ?? <EmptyIllustration /> : null}
      <div className="empty__title">{title}</div>
      {description != null && description !== '' ? (
        <div className="empty__desc">{description}</div>
      ) : null}
      {extra != null ? <div className="empty__extra">{extra}</div> : null}
    </div>
  )
}
