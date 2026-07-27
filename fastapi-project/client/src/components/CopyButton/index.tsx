import {
  type ButtonHTMLAttributes,
  type ReactNode,
  useCallback,
  useEffect,
  useRef,
  useState,
} from 'react'
import { copyTextToClipboard } from './copy'
import { CheckGlyph, CopyGlyph } from './icons'
import './index.less'

export type CopyButtonProps = Omit<
  ButtonHTMLAttributes<HTMLButtonElement>,
  'children' | 'onClick' | 'type'
> & {
  /** 要复制到剪贴板的文本 */
  text: string
  /** 按钮文案，默认「复制」 */
  children?: ReactNode
  /** 复制成功后的短暂提示，默认「已复制」 */
  successText?: string
  /** 复制结束回调 */
  onCopy?: (success: boolean) => void
  /** 成功提示显示的毫秒数，默认 2000 */
  successDurationMs?: number
}

export function CopyButton({
  text,
  children = '复制',
  successText = '已复制',
  className,
  disabled,
  onCopy,
  successDurationMs = 2000,
  ...rest
}: CopyButtonProps) {
  const [copied, setCopied] = useState(false)
  const timerRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)

  useEffect(() => {
    return () => {
      if (timerRef.current !== undefined) clearTimeout(timerRef.current)
    }
  }, [])

  const handleClick = useCallback(async () => {
    if (disabled) return
    const ok = await copyTextToClipboard(text)
    onCopy?.(ok)
    if (!ok) return
    setCopied(true)
    if (timerRef.current !== undefined) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => {
      setCopied(false)
      timerRef.current = undefined
    }, successDurationMs)
  }, [disabled, onCopy, successDurationMs, text])

  const mergedClass = ['copy-btn', copied ? 'copy-btn--copied' : '', className ?? '']
    .filter(Boolean)
    .join(' ')

  return (
    <button
      {...rest}
      type="button"
      className={mergedClass}
      disabled={disabled}
      onClick={handleClick}
      aria-live="polite"
      title={copied ? successText : '复制到剪贴板'}
    >
      <span className="copy-btn__icon" aria-hidden={true}>
        {copied ? <CheckGlyph /> : <CopyGlyph />}
      </span>
      <span className="copy-btn__label">{copied ? successText : children}</span>
    </button>
  )
}
