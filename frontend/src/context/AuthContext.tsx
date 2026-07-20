import { createContext, useContext, useState, ReactNode } from 'react'
import client from '../api/client'
import { UserInfo, LoginResponse, RegisterResponse, ApiError } from '../types/api'
import { AxiosError } from 'axios'

interface AuthContextValue {
  user: UserInfo | null
  login: (username: string, password: string) => Promise<{ success: boolean; error?: string }>
  register: (username: string, email: string, password: string) => Promise<{ success: boolean; error?: string }>
  logout: () => Promise<void>
  loading: boolean
}

const AuthContext = createContext<AuthContextValue | null>(null)

function extractError(err: unknown): string {
  const axiosErr = err as AxiosError<ApiError>
  const detail = axiosErr.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail && typeof detail === 'object') return Object.values(detail).flat().join(', ')
  return 'An unexpected error occurred'
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserInfo | null>(() => {
    try {
      const saved = localStorage.getItem('user')
      return saved ? JSON.parse(saved) : null
    } catch {
      return null
    }
  })
  const [loading, setLoading] = useState(false)

  const login = async (username: string, password: string) => {
    setLoading(true)
    try {
      const { data } = await client.post<LoginResponse>('/auth/login/', { username, password })
      localStorage.setItem('tokens', JSON.stringify(data.tokens))
      localStorage.setItem('user', JSON.stringify(data.user))
      setUser(data.user)
      return { success: true }
    } catch (err) {
      return { success: false, error: extractError(err) }
    } finally {
      setLoading(false)
    }
  }

  const register = async (username: string, email: string, password: string) => {
    setLoading(true)
    try {
      const { data } = await client.post<RegisterResponse>('/auth/register/', { username, email, password })
      localStorage.setItem('tokens', JSON.stringify(data.tokens))
      localStorage.setItem('user', JSON.stringify(data.user))
      setUser(data.user)
      return { success: true }
    } catch (err) {
      return { success: false, error: extractError(err) }
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      const raw = localStorage.getItem('tokens')
      if (raw) {
        const tokens = JSON.parse(raw)
        if (tokens?.refresh) {
          await client.post('/auth/logout/', { refresh: tokens.refresh })
        }
      }
    } catch {}
    localStorage.removeItem('tokens')
    localStorage.removeItem('user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
