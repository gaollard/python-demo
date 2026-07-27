import type { ImageUploadResult } from '../types/api'
import { request, type IBaseRes } from './request'

export async function uploadImages(files: File[]) {
  const form = new FormData()
  for (const file of files) {
    form.append('files', file)
  }
  const response = await request<ImageUploadResult>('/uploads/images', {
    method: 'POST',
    data: form,
  })
  return response as IBaseRes<ImageUploadResult>
}
