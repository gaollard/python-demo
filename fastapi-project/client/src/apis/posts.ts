import type {
  InteractionResult,
  PageData,
  PageParams,
  PostCreatePayload,
  PostDetail,
  PostListItem,
} from '../types/api'
import { request, type IBaseRes } from './request'

export async function fetchPosts(params: PageParams = {}) {
  const response = await request<PageData<PostListItem>>('/posts', {
    method: 'GET',
    params: {
      page: params.page ?? 1,
      page_size: params.page_size ?? 20,
    },
  })
  return response as IBaseRes<PageData<PostListItem>>
}

export async function fetchPostDetail(id: number) {
  const response = await request<PostDetail>(`/posts/${id}`, {
    method: 'GET',
  })
  return response as IBaseRes<PostDetail>
}

export async function createPost(payload: PostCreatePayload) {
  const response = await request<PostDetail>('/posts', {
    method: 'POST',
    data: payload,
  })
  return response as IBaseRes<PostDetail>
}

export async function likePost(id: number) {
  const response = await request<InteractionResult>(`/posts/${id}/like`, {
    method: 'POST',
  })
  return response as IBaseRes<InteractionResult>
}

export async function unlikePost(id: number) {
  const response = await request<InteractionResult>(`/posts/${id}/like`, {
    method: 'DELETE',
  })
  return response as IBaseRes<InteractionResult>
}

export async function favoritePost(id: number) {
  const response = await request<InteractionResult>(`/posts/${id}/favorite`, {
    method: 'POST',
  })
  return response as IBaseRes<InteractionResult>
}

export async function unfavoritePost(id: number) {
  const response = await request<InteractionResult>(`/posts/${id}/favorite`, {
    method: 'DELETE',
  })
  return response as IBaseRes<InteractionResult>
}
