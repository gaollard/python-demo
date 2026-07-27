import type { PageData, PageParams, PostListItem } from '../types/api'
import { request, type IBaseRes } from './request'

export async function fetchMyPosts(params: PageParams = {}) {
  const response = await request<PageData<PostListItem>>('/me/posts', {
    method: 'GET',
    params: {
      page: params.page ?? 1,
      page_size: params.page_size ?? 20,
    },
  })
  return response as IBaseRes<PageData<PostListItem>>
}

export async function fetchMyFavorites(params: PageParams = {}) {
  const response = await request<PageData<PostListItem>>('/me/favorites', {
    method: 'GET',
    params: {
      page: params.page ?? 1,
      page_size: params.page_size ?? 20,
    },
  })
  return response as IBaseRes<PageData<PostListItem>>
}
