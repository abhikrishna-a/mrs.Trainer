import { createContext, useContext, useState, useCallback, useRef, ReactNode } from 'react'
import client from '../api/client'
import { TaskResultData, TaskResultResponse } from '../types/api'

interface ProblemContextValue {
  language: string
  setLanguage: (lang: string) => void
  code: string
  setCode: (code: string) => void
  taskId: string | null
  taskStatus: string | null
  taskResult: TaskResultData | null
  startPolling: (id: string, isSubmit?: boolean) => void
  reset: () => void
}

const ProblemContext = createContext<ProblemContextValue | null>(null)

export function ProblemProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState('python')
  const [code, setCode] = useState('')
  const [taskId, setTaskId] = useState<string | null>(null)
  const [taskStatus, setTaskStatus] = useState<string | null>(null)
  const [taskResult, setTaskResult] = useState<TaskResultData | null>(null)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const startPolling = useCallback((id: string, isSubmit = false) => {
    setTaskId(id)
    setTaskStatus('PENDING')
    setTaskResult(null)

    const initial = isSubmit ? 1000 : 300
    const interval = isSubmit ? 2000 : 500
    const maxPolls = isSubmit ? 90 : 20

    let polls = 0
    if (pollRef.current) clearInterval(pollRef.current)

    setTimeout(() => {
      pollRef.current = setInterval(async () => {
        polls++
        try {
          const { data } = await client.get<TaskResultResponse>(`/tasks/${id}/`)
          setTaskStatus(data.status)
          if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
            const result = typeof data.result === 'string' ? JSON.parse(data.result) : data.result
            setTaskResult(result)
            clearInterval(pollRef.current!)
            pollRef.current = null
          } else if (polls >= maxPolls) {
            setTaskStatus('TIMEOUT')
            setTaskResult({ error: 'Polling timed out' })
            clearInterval(pollRef.current!)
            pollRef.current = null
          }
        } catch {
          if (polls >= maxPolls) {
            setTaskStatus('TIMEOUT')
            clearInterval(pollRef.current!)
            pollRef.current = null
          }
        }
      }, interval)
    }, initial)
  }, [])

  const reset = useCallback(() => {
    setTaskId(null)
    setTaskStatus(null)
    setTaskResult(null)
    setCode('')
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }, [])

  return (
    <ProblemContext.Provider value={{
      language, setLanguage, code, setCode,
      taskId, taskStatus, taskResult,
      startPolling, reset,
    }}>
      {children}
    </ProblemContext.Provider>
  )
}

export function useProblem(): ProblemContextValue {
  const ctx = useContext(ProblemContext)
  if (!ctx) throw new Error('useProblem must be used within ProblemProvider')
  return ctx
}
