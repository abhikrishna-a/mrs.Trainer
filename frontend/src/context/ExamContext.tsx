import { createContext, useContext, useState, useCallback, useRef, useEffect, ReactNode } from 'react'
import client from '../api/client'
import { ExamSession, ExamDetail, ExamQuestion, ExamAnswerResponse, ExamFinishResponse, ExamMode } from '../types/api'

interface ExamContextValue {
  session: ExamSession | null
  questions: ExamQuestion[]
  currentIndex: number
  answers: Record<number, { selectedOptionId: number; isCorrect: boolean }>
  timeLeft: number
  loading: boolean
  error: string | null
  currentQuestion: ExamQuestion | null
  startExam: (mode: ExamMode, roleSlug?: string | null) => Promise<ExamSession | undefined>
  answerQuestion: (questionId: number, selectedOptionId: number) => Promise<ExamAnswerResponse | undefined>
  finishExam: () => Promise<ExamFinishResponse | undefined>
  goToQuestion: (index: number) => void
  reset: () => void
}

const ExamContext = createContext<ExamContextValue | null>(null)

export function ExamProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<ExamSession | null>(null)
  const [questions, setQuestions] = useState<ExamQuestion[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, { selectedOptionId: number; isCorrect: boolean }>>({})
  const [timeLeft, setTimeLeft] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const startExam = useCallback(async (mode: ExamMode, roleSlug: string | null = null) => {
    setLoading(true)
    setError(null)
    try {
      const { data: sessionData } = await client.post<ExamSession>('/exams/start/', { mode, role: roleSlug })
      setSession(sessionData)
      setCurrentIndex(0)
      setAnswers({})

      const duration = mode === 'full_mock' ? 2700 : 1200
      const elapsed = Math.floor((Date.now() - new Date(sessionData.started_at).getTime()) / 1000)
      setTimeLeft(Math.max(0, duration - elapsed))

      const { data: detail } = await client.get<ExamDetail>(`/exams/${sessionData.id}/`)
      setQuestions(detail.questions || [])
      return sessionData
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to start exam'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (timeLeft <= 0 || !session || session.is_completed) return
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current!)
          return 0
        }
        return prev - 1
      })
    }, 1000)
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [session?.id, session?.is_completed])

  const answerQuestion = useCallback(async (questionId: number, selectedOptionId: number) => {
    if (!session) return
    try {
      const { data } = await client.post<ExamAnswerResponse>(`/exams/${session.id}/answer/`, {
        question_id: questionId,
        selected_option_id: selectedOptionId,
      })
      setAnswers((prev) => ({ ...prev, [questionId]: { selectedOptionId, isCorrect: data.is_correct } }))
      return data
    } catch (err) {
      throw err
    }
  }, [session])

  const finishExam = useCallback(async () => {
    if (!session) return
    if (timerRef.current) clearInterval(timerRef.current)
    try {
      const { data } = await client.post<ExamFinishResponse>(`/exams/${session.id}/finish/`)
      setSession(data as unknown as ExamSession)
      return data
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to finish exam'
      setError(msg)
    }
  }, [session])

  const goToQuestion = useCallback((index: number) => {
    if (index >= 0 && index < questions.length) setCurrentIndex(index)
  }, [questions.length])

  const currentQuestion = questions[currentIndex] || null

  const reset = useCallback(() => {
    setSession(null)
    setQuestions([])
    setCurrentIndex(0)
    setAnswers({})
    setTimeLeft(0)
    setError(null)
    if (timerRef.current) clearInterval(timerRef.current)
  }, [])

  return (
    <ExamContext.Provider value={{
      session, questions, currentIndex, answers, timeLeft,
      loading, error, currentQuestion,
      startExam, answerQuestion, finishExam, goToQuestion, reset,
    }}>
      {children}
    </ExamContext.Provider>
  )
}

export function useExam(): ExamContextValue {
  const ctx = useContext(ExamContext)
  if (!ctx) throw new Error('useExam must be used within ExamProvider')
  return ctx
}
