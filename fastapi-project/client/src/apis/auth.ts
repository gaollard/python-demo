import type { LoginPayload, LoginResData, RegisterPayload, IUserInfo } from '../types/api'
import { request, type IBaseRes } from './request'

export async function login(payload: LoginPayload) {
  const response = await request<LoginResData>('/auth/login', {
    method: 'POST',
    data: payload,
  })
  return response as IBaseRes<LoginResData>
}

export async function register(payload: RegisterPayload) {
  const response = await request<IUserInfo>('/auth/register', {
    method: 'POST',
    data: payload,
  })
  return response as IBaseRes<IUserInfo>
}
