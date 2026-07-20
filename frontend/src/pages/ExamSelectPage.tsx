import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useExam } from '../context/ExamContext'
import client from '../api/client'
import { Role, ExamMode } from '../types/api'

export default function ExamSelectPage() {
  const [roles, setRoles] = useState<Role[]>([])
  const [rolesLoading, setRolesLoading] = useState(true)
  const [rolesError, setRolesError] = useState<string | null>(null)
  const [starting, setStarting] = useState(false)
  const { startExam, loading: examLoading, error } = useExam()
  const navigate = useNavigate()

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const { data } = await client.get<Role[]>('/roles/')
        setRoles(data)
      } catch {
        setRolesError('Failed to load categories')
      } finally {
        setRolesLoading(false)
      }
    }
    fetchRoles()
  }, [])

  const handleStart = async (mode: ExamMode, roleSlug?: string | null) => {
    setStarting(true)
    const result = await startExam(mode, roleSlug)
    setStarting(false)
    if (result?.id) navigate(`/exam/${result.id}`)
  }

  const isBusy = examLoading || starting

  return (
    <div className="animate-fade-in-up space-y-8 max-w-3xl mx-auto">
      <div className="text-center">
        <h2 className="font-display font-black text-2xl md:text-3xl text-text-primary mb-2">Mock Exams</h2>
        <p className="text-text-secondary text-sm">Choose your exam format and begin</p>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-wrong-bg border border-wrong-border text-wrong text-sm font-mono">
          {error}
        </div>
      )}

      {rolesError && (
        <div className="p-3 rounded-lg bg-wrong-bg border border-wrong-border text-wrong text-sm font-mono">
          {rolesError}
        </div>
      )}

      <button
        onClick={() => handleStart('full_mock')}
        disabled={isBusy}
        className="w-full group relative overflow-hidden rounded-2xl border border-glass-border bg-bg-surface backdrop-blur-[14px] p-8 text-left transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_20px_60px_rgba(0,0,0,0.4)] hover:border-accent-gold/30 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
      >
        <div className="flex items-start gap-4">
          <div className="shrink-0 w-14 h-14 rounded-xl flex items-center justify-center bg-accent-gold/10 border border-accent-gold/20">
            <svg className="w-7 h-7 text-accent-gold" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className="font-display font-bold text-lg text-text-primary mb-1">Full Mock Exam</h3>
            <p className="text-text-muted text-sm mb-2">30 questions across all roles · 45 minutes · Interleaved format</p>
            <span className="font-mono text-xs font-bold text-accent-gold uppercase tracking-widest">45 min</span>
          </div>
        </div>
      </button>

      <div>
        <h3 className="font-display font-bold text-sm text-text-secondary mb-3 uppercase tracking-wider">Category Drills</h3>
        {rolesLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-32 bg-bg-surface rounded-xl animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {roles.map((role) => (
              <button
                key={role.id}
                onClick={() => handleStart('category_drill', role.slug)}
                disabled={isBusy}
                className="group rounded-xl border border-glass-border bg-bg-surface backdrop-blur-[14px] p-5 text-left transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_12px_40px_rgba(0,0,0,0.3)] hover:border-accent-gold/20 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                <h4 className="font-display font-bold text-sm text-text-primary mb-1">{role.name}</h4>
                <p className="text-text-muted text-xs mb-2">20 questions · 20 minutes</p>
                <span className="font-mono text-[10px] font-bold text-accent-gold uppercase tracking-widest">20 min</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
