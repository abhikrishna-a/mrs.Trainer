import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import ExamHistoryRow from '../components/ExamHistoryRow'
import type { ExamSession } from '../types/api'

export default function ExamHistoryPage() {
  const [exams, setExams] = useState<ExamSession[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const { data } = await client.get<ExamSession[]>('/exams/history/')
        setExams(Array.isArray(data) ? data : [])
      } catch {
        setError('Failed to load exam history')
      } finally {
        setLoading(false)
      }
    }
    fetchHistory()
  }, [])

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-3 max-w-2xl mx-auto">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="h-20 bg-bg-surface rounded-xl animate-pulse" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <p className="text-text-secondary font-mono">{error}</p>
      </div>
    )
  }

  return (
    <div className="animate-fade-in-up space-y-6 max-w-2xl mx-auto">
      <div className="flex items-center justify-between">
        <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Exam History</h2>
        <span className="font-mono text-xs text-text-muted">{exams.length} exams</span>
      </div>

      <div className="space-y-3">
        {exams.length === 0 ? (
          <p className="text-center text-text-muted py-12 font-mono">No exams taken yet</p>
        ) : (
          exams.map((exam) => (
            <div key={exam.id} onClick={() => navigate(`/exam/${exam.id}/results`)} className="cursor-pointer">
              <ExamHistoryRow exam={exam} />
            </div>
          ))
        )}
      </div>
    </div>
  )
}
