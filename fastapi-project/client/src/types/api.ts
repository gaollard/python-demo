export type LoginPayload = {
  email: string
  password: string
}

export type LoginResData = {
  token?: string
  user?: Record<string, unknown>
}

/** 常见字段名；后端可只返回其中一部分 */
export type IUserInfo = {
  id?: string | number
  email?: string
  name?: string
  nickname?: string
  avatar?: string
}