import type { LoginPayload, LoginResData, IUserInfo } from '../types/api'
import { request, type IBaseRes } from './request'

export async function login(payload: LoginPayload) {
  const response = await request<LoginResData>('/auth/login', {
    method: 'POST',
    data: payload,
  })
  return response as IBaseRes<LoginResData>
}

export async function fetchProfile() {
  const response = await request<IUserInfo | null>('/auth/me', {
    method: 'GET',
  })
  return response as IBaseRes<IUserInfo | null>
}
