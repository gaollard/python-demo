import dayjs, { type ConfigType } from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

/** 常用：年月日 */
export const DISPLAY_DATE = 'YYYY-MM-DD'

/** 常用：年月日 + 时分 */
export const DISPLAY_DATETIME = 'YYYY-MM-DD HH:mm'

/** 常用：年月日 + 时分秒 */
export const DISPLAY_DATETIME_FULL = 'YYYY-MM-DD HH:mm:ss'

function toDayjs(input: ConfigType) {
  return dayjs(input)
}

/**
 * 格式化为本地展示字符串；无效日期返回空字符串。
 */
export function formatDate(input: ConfigType, formatStr = DISPLAY_DATE): string {
  const d = toDayjs(input)
  return d.isValid() ? d.format(formatStr) : ''
}

/**
 * 日期时间展示，默认 `DISPLAY_DATETIME`。
 */
export function formatDateTime(
  input: ConfigType,
  formatStr = DISPLAY_DATETIME
): string {
  return formatDate(input, formatStr)
}

/**
 * 相对时间（如「3小时前」），无效日期返回空字符串。
 */
export function formatRelative(input: ConfigType): string {
  const d = toDayjs(input)
  return d.isValid() ? d.fromNow() : ''
}
