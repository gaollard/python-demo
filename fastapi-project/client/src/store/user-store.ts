import { create } from 'zustand'
import { login as loginRequest } from '../apis/auth'
import type { IUserInfo, LoginPayload } from '../types/api'
import { getAuthToken, removeAuthToken, setAuthToken } from '../utils/auth'

const USER_KEY = 'forum_user'

function readStoredUser(): IUserInfo | null {
  try {
    const raw = localStorage.getItem(USER_KEY)
    if (!raw) return null
    return JSON.parse(raw) as IUserInfo
  } catch {
    return null
  }
}

function writeStoredUser(user: IUserInfo | null) {
  if (!user) {
    localStorage.removeItem(USER_KEY)
    return
  }
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

interface IUserStore {
  user: IUserInfo | null
  token: string | null
  loggingIn: boolean
  hydrated: boolean
  hydrate: () => void
  setUser: (user: IUserInfo | null) => void
  login: (params: LoginPayload) => Promise<void>
  logout: () => void
}

export const useUserStore = create<IUserStore>((set) => ({
  user: null,
  token: null,
  loggingIn: false,
  hydrated: false,

  hydrate: () => {
    const token = getAuthToken()
    const user = token ? readStoredUser() : null
    if (!token) writeStoredUser(null)
    set({ token, user, hydrated: true })
  },

  setUser: (user) => {
    writeStoredUser(user)
    set({ user })
  },

  login: async (params) => {
    set({ loggingIn: true })
    try {
      const res = await loginRequest(params)
      const { access_token, user } = res.data
      setAuthToken(access_token)
      writeStoredUser(user)
      set({ token: access_token, user, loggingIn: false })
    } catch (error) {
      set({ loggingIn: false })
      throw error
    }
  },

  logout: () => {
    removeAuthToken()
    writeStoredUser(null)
    set({ token: null, user: null })
  },
}))
