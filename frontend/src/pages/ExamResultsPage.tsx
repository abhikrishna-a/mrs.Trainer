import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import client from '../api/client'
import type { ExamSession } from '../types/api'

interface ExamResult {
  question_id?: number
  question_text?: string
  explanation?: string
  is_correct: boolean
}

interface ExamResultsResponse {
  session: ExamSession
  results: ExamResult[]
}

export default function ExamResultsPage() {
  const { examId } = useParams<{ examId: string }>()
  const navigate = useNavigate()
  const [results, setResults] = useState<ExamResultsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const { data } = await client.get<ExamResultsResponse>(`/exams/${examId}/results/`)
        setResults(data)
      } catch {
        setError('Failed to load exam results')
      } finally {
        setLoading(false)
      }
    }
    fetchResults()
  }, [examId])

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-4 max-w-2xl mx-auto">
        <div className="h-48 bg-bg-surface rounded-2xl animate-pulse" />
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-16 bg-bg-surface rounded-xl animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  if (error || !results) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-secondary font-mono mb-4">{error || 'Results not found'}</p>
          <button onClick={() => navigate('/exams')} className="px-4 py-2 rounded-lg bg-gradient-to-r from-accent-red to-accent-gold text-white font-bold cursor-pointer">
            Back to Exams
          </button>
        </div>
      </div>
    )
  }

  const resultList = results.results || []
  const correct = resultList.filter((r) => r.is_correct).length
  const total = resultList.length
  const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0

  return (
    <div className="animate-fade-in-up space-y-6 max-w-2xl mx-auto">
      <div className="p-8 text-center bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.25)]">
        <h2 className="sr-only">Exam Results</h2>
        <div className="mb-4">
          <span className="text-5xl md:text-7xl font-mono font-bold"
            style={{
              background: 'linear-gradient(135deg, #c0392b, #d4a017)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
            {correct}
          </span>
          <span className="text-3xl md:text-5xl text-text-muted mx-1">/</span>
          <span className="text-3xl md:text-5xl text-text-muted">{total}</span>
        </div>
        <div className="flex justify-center gap-8">
          <div className="text-center">
            <span className="block font-mono text-[10px] font-bold text-text-muted uppercase tracking-widest mb-1">Accuracy</span>
            <span className="font-display font-bold text-lg">{accuracy}%</span>
          </div>
          <div className="text-center">
            <span className="block font-mono text-[10px] font-bold text-text-muted uppercase tracking-widest mb-1">Score</span>
            <span className="font-display font-bold text-lg">{results.session.score || 0}</span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        <h3 className="font-mono text-xs font-bold text-text-muted uppercase tracking-widest">Question Breakdown</h3>
        {resultList.map((r, i) => (
          <div key={r.question_id || i}
            className={`flex items-center gap-3 p-4 rounded-xl border ${
              r.is_correct
                ? 'bg-correct-bg border-correct-border'
                : 'bg-wrong-bg border-wrong-border'
            }`}
          >
            <span className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-mono text-xs font-bold border ${
              r.is_correct
                ? 'bg-correct text-white border-correct'
                : 'bg-wrong text-white border-wrong'
            }`}>
              {i + 1}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{r.question_text || `Question ${i + 1}`}</p>
              {r.explanation && (
                <p className="text-xs text-text-muted mt-1">{r.explanation}</p>
              )}
            </div>
            <span className={`shrink-0 font-mono text-[10px] font-bold uppercase ${
              r.is_correct ? 'text-correct' : 'text-wrong'
            }`}>
              {r.is_correct ? 'Correct' : 'Wrong'}
            </span>
          </div>
        ))}
      </div>

      <div className="flex justify-center gap-3">
        <button
          onClick={() => navigate('/exams')}
          className="px-6 py-2.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
        >
          Back to Exams
        </button>
        <button
          onClick={() => navigate('/exams/history')}
          className="px-5 py-2.5 rounded-xl font-semibold text-sm bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover transition-all duration-150 cursor-pointer"
        >
          View History
        </button>
      </div>
    </div>
  )
}
