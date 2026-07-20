export function formatTime(ms: number): string {
  const totalSec = Math.floor(ms / 1000)
  const m = Math.floor(totalSec / 60)
  const s = totalSec % 60
  return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`
}

export function safeLocalStorage<T = unknown>(key: string, value?: T): T | null {
  try {
    if (value !== undefined) {
      localStorage.setItem(key, JSON.stringify(value))
    }
    const item = localStorage.getItem(key)
    return item ? JSON.parse(item) as T : null
  } catch {
    return null
  }
}
