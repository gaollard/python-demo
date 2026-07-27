/** 认证 */

export type LoginPayload = {
  username: string
  password: string
}

export type RegisterPayload = {
  username: string
  password: string
}

export type IUserInfo = {
  id: number
  username: string
  created_at?: string
}

export type LoginResData = {
  access_token: string
  token_type: string
  user: IUserInfo
}

/** 帖子 */

export type AuthorInfo = {
  id: number
  username: string
}

export type PostListItem = {
  id: number
  title: string
  author: AuthorInfo
  images?: string[]
  like_count: number
  favorite_count: number
  created_at: string
}

export type PostDetail = PostListItem & {
  content: string
  liked?: boolean | null
  favorited?: boolean | null
}

export type PostCreatePayload = {
  title: string
  content: string
  images?: string[]
}

export type ImageUploadResult = {
  urls: string[]
}

export type InteractionResult = {
  post_id: number
  liked?: boolean | null
  favorited?: boolean | null
  like_count?: number | null
  favorite_count?: number | null
}

export type PageParams = {
  page?: number
  page_size?: number
}

export type PageData<T> = {
  items: T[]
  total: number
  page: number
  page_size: number
}
