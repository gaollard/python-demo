import { isAxiosError } from 'axios'
import { BizApiError } from '../apis/request'

/** 从接口异常中提取可读错误文案 */
export function getApiErrorMessage(
  err: unknown,
  fallback = '请求失败，请稍后重试'
): string {
  if (err instanceof BizApiError) {
    return err.message || fallback
  }
  if (isAxiosError(err)) {
    const data = err.response?.data as
      | { message?: string; msg?: string }
      | undefined
    if (data?.message) return data.message
    if (data?.msg) return data.msg
    if (err.code === 'ECONNABORTED') return '请求超时，请稍后重试'
    if (!err.response) return '网络异常，请检查连接后重试'
  }
  if (err instanceof Error && err.message) return err.message
  return fallback
}
