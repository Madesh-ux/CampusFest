import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export function getApiError(error, fallback = 'Something went wrong. Please try again.') {
  const data = error.response?.data
  if (typeof data === 'string') return data
  if (data?.error || data?.detail || data?.message) return data.error || data.detail || data.message
  if (data && typeof data === 'object') {
    const first = Object.values(data)[0]
    if (Array.isArray(first)) return first[0]
    if (typeof first === 'string') return first
  }
  return fallback
}

export default api
