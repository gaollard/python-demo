import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios'
import { getAuthToken } from '../utils/auth'

/** 与后端约定的统一响应壳 */
export interface IBaseRes<T> {
  code: string
  msg: string
  data: T
}

/** HTTP 成功但业务码失败时抛出，便于与 Axios 错误区分 */
export class BizApiError extends Error {
  readonly code: string
  readonly payload: unknown
  constructor(code: string, message: string, payload?: unknown) {
    super(message)
    this.name = 'BizApiError'
    this.code = code
    this.payload = payload ?? undefined
    Object.setPrototypeOf(this, BizApiError.prototype)
  }
}

/** 视为成功的业务码，可按后端约定增删 */
const BIZ_SUCCESS_CODES = new Set(['0', '200', '00000'])

export function isBizSuccess(code: string): boolean {
  return BIZ_SUCCESS_CODES.has(code)
}

function isEnvelope(x: unknown): x is IBaseRes<unknown> {
  if (typeof x !== 'object' || x === null) return false
  const o = x as Record<string, unknown>
  return (
    typeof o.code === 'string' &&
    typeof o.msg === 'string' &&
    'data' in o
  )
}

function rejectIfBizFailed(body: unknown): void {
  if (isEnvelope(body) && !isBizSuccess(body.code)) {
    throw new BizApiError(body.code, body.msg, body.data)
  }
}

const BASE_URL = '/api'
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
  showGlobalError?: boolean;
}

export const request = async <T>(url: string, options?: IRequestOptions): Promise<IBaseRes<T>> => {
  const opts = options ?? {};
  const method = opts.method || 'POST';
  const showGlobalError = opts.showGlobalError || false;
  const data = opts.data || {};
  try {
    const response = await httpClient.request({
      ...opts,
      url,
      method,
      data,
    });
    return response.data as IBaseRes<T>;
  } catch (error: unknown) {
    if (showGlobalError) {
      const msg = error instanceof Error ? error.message : '请求失败';
      notifyGlobalError(msg);
    }
    throw error;
  }
}

function notifyGlobalError(message: string) {
  throw new Error(message);
}