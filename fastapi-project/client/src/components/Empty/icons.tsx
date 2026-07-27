/** 列表/搜索结果为空时的默认插画 */
export function EmptyIllustration() {
  return (
    <svg
      className="empty__svg"
      viewBox="0 0 120 96"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden={true}
    >
      <rect
        x="12"
        y="24"
        width="96"
        height="56"
        rx="8"
        fill="var(--accent-bg)"
        stroke="var(--border)"
        strokeWidth="1.5"
      />
      <path
        d="M36 44h48M36 56h32"
        stroke="var(--border)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle cx="76" cy="41" r="10" fill="var(--accent-bg)" stroke="var(--accent-border)" strokeWidth="1.5" />
      <path
        d="M72 41l4 4 8-9"
        stroke="var(--accent)"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  )
}
