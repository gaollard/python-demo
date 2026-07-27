import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios'
import { getAuthToken } from '../utils/auth'

/** 与后端约定的统一响应壳：`{ code, message, data }` */
export interface IBaseRes<T> {
  code: number | string
  message: string
  data: T
}

/** HTTP 成功但业务码失败时抛出，便于与 Axios 错误区分 */
export class BizApiError extends Error {
  readonly code: string
  readonly payload: unknown
  constructor(code: string | number, message: string, payload?: unknown) {
    super(message)
    this.name = 'BizApiError'
    this.code = String(code)
    this.payload = payload ?? undefined
    Object.setPrototypeOf(this, BizApiError.prototype)
  }
}

/** 视为成功的业务码，可按后端约定增删 */
const BIZ_SUCCESS_CODES = new Set(['0', '200', '00000'])

export function isBizSuccess(code: number | string): boolean {
  return BIZ_SUCCESS_CODES.has(String(code))
}

function isEnvelope(x: unknown): x is IBaseRes<unknown> {
  if (typeof x !== 'object' || x === null) return false
  const o = x as Record<string, unknown>
  const hasCode = typeof o.code === 'string' || typeof o.code === 'number'
  const hasMessage = typeof o.message === 'string' || typeof o.msg === 'string'
  return hasCode && hasMessage && 'data' in o
}

function envelopeMessage(body: IBaseRes<unknown> & { msg?: string }): string {
  return body.message || body.msg || '请求失败'
}

function rejectIfBizFailed(body: unknown): void {
  if (isEnvelope(body) && !isBizSuccess(body.code)) {
    throw new BizApiError(body.code, envelopeMessage(body), body.data)
  }
}

const BASE_URL = '/api/v1'
const TIMEOUT_MS = 15_000

function attachAuthHeader(config: InternalAxiosRequestConfig) {
  const token = getAuthToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}

/**
 * 全局 Axios 实例：JSON、超时、Bearer、`IBaseRes` 业务码校验
 */
const httpClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT_MS,
  headers: {
    'Content-Type': 'application/json',
  },
  validateStatus: (status) => status >= 200 && status < 300,
})

httpClient.interceptors.request.use(attachAuthHeader, (error) =>
  Promise.reject(error)
)

httpClient.interceptors.response.use(
  (response: AxiosResponse) => {
    rejectIfBizFailed(response.data)
    return response
  },
  (error: AxiosError) => {
    const body = error.response?.data
    try {
      rejectIfBizFailed(body)
    } catch (e) {
      return Promise.reject(e)
    }
    return Promise.reject(error)
  }
)

interface IRequestOptions extends AxiosRequestConfig {
  showGlobalError?: boolean
}

export const request = async <T>(
  url: string,
  options?: IRequestOptions
): Promise<IBaseRes<T>> => {
  const opts = options ?? {}
  const method = (opts.method || 'POST').toUpperCase()
  const showGlobalError = opts.showGlobalError || false

  const config: AxiosRequestConfig = {
    ...opts,
    url,
    method,
  }

  // GET/DELETE 默认不带 body，避免空对象干扰查询参数
  if (method === 'GET' || method === 'DELETE') {
    if (opts.data === undefined) {
      delete config.data
    }
  } else if (opts.data === undefined) {
    config.data = {}
  }

  // FormData 需由浏览器设置 multipart boundary，去掉默认 JSON Content-Type
  if (typeof FormData !== 'undefined' && config.data instanceof FormData) {
    config.headers = {
      ...config.headers,
      'Content-Type': undefined,
    }
  }

  try {
    const response = await httpClient.request(config)
    return response.data as IBaseRes<T>
  } catch (error: unknown) {
    if (showGlobalError) {
      const msg = error instanceof Error ? error.message : '请求失败'
      notifyGlobalError(msg)
    }
    throw error
  }
}

function notifyGlobalError(message: string) {
  throw new Error(message)
}
