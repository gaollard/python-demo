import { create } from 'zustand'
import { login } from '../apis/auth'
import type { IUserInfo, LoginPayload } from '../types/api'

interface IUserStore {
  user: IUserInfo | null
  loadingLoading: boolean;
  setUser: (user: IUserInfo) => void
  clearUser: () => void
}

export const useUserStore = create<IUserStore>((set, get) => ({
  user: {
    id: 1,
    name: 'hello',
    email: 'hello@gmail'
  },
  loadingLoading: false,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
  async login (params: LoginPayload) {
    set({ loadingLoading: true })
      try {
        const res = await login(params);
        set({ user: res.data.user, loadingLoading: false })
      } catch (error) {
        set({ loadingLoading: false })
        throw error
      }
    }
  }
));
