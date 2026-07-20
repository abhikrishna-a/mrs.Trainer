import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import { AuthTokens } from '../types/api'

const API_BASE = '/api'

interface FailedRequest extends InternalAxiosRequestConfig {
  _retry?: boolean
}

const getTokens = (): AuthTokens | null => {
  try {
    const raw = localStorage.getItem('tokens')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const tokens = getTokens()
  if (tokens?.access && config.headers) {
    config.headers.Authorization = `Bearer ${tokens.access}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as FailedRequest | undefined
    if (!originalRequest || error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }
    originalRequest._retry = true
    try {
      const tokens = getTokens()
      if (!tokens?.refresh) {
        throw new Error('No refresh token')
      }
      const { data } = await axios.post<{ access: string; refresh?: string }>(
        `${API_BASE}/auth/refresh/`,
        { refresh: tokens.refresh },
      )
      const newTokens: AuthTokens = { ...tokens, access: data.access }
      if (data.refresh) newTokens.refresh = data.refresh
      localStorage.setItem('tokens', JSON.stringify(newTokens))
      if (originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${data.access}`
      }
      return client(originalRequest)
    } catch {
      localStorage.removeItem('tokens')
      localStorage.removeItem('user')
      window.location.href = '/login'
      return Promise.reject(error)
    }
  },
)

export default client
