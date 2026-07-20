import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import { DashboardData } from '../types/api'

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const { data } = await client.get<DashboardData>('/dashboard/')
        setDashboard(data)
      } catch {
        setError('Failed to load dashboard')
      } finally {
        setLoading(false)
      }
    }
    fetchDashboard()
  }, [])

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-28 bg-bg-surface rounded-2xl animate-pulse" />
          ))}
        </div>
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-16 bg-bg-surface rounded-xl animate-pulse" />
          ))}
        </div>
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

  const accuracy = dashboard?.questions_attempted && dashboard.questions_attempted > 0
    ? Math.round((dashboard.questions_solved / dashboard.questions_attempted) * 100)
    : 0

  const stats: { label: string; value: string | number; color: string }[] = [
    { label: 'Problems Solved', value: dashboard?.questions_solved || 0, color: 'text-correct' },
    { label: 'Problems Attempted', value: dashboard?.questions_attempted || 0, color: 'text-accent-gold' },
    { label: 'Accuracy', value: `${accuracy}%`, color: 'text-accent-red-soft' },
    { label: 'Streak', value: `${dashboard?.current_streak || 0} days`, color: 'text-text-primary' },
  ]

  return (
    <div className="animate-fade-in-up space-y-8">
      <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Dashboard</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <DashboardStatCard key={stat.label} label={stat.label} value={stat.value} color={stat.color} />
        ))}
      </div>

      {dashboard?.last_practice_date && (
        <section>
          <h3 className="font-mono text-xs font-bold text-text-muted uppercase tracking-widest mb-4">Last Practice</h3>
          <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-bg-surface border border-glass-border">
            <div className="w-2 h-2 rounded-full bg-correct" />
            <p className="flex-1 text-sm text-text-primary">
              {new Date(dashboard.last_practice_date).toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
          </div>
        </section>
      )}

      <div className="flex justify-center gap-3">
        <button
          onClick={() => navigate('/problems')}
          className="px-6 py-2.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
        >
          Practice Problems
        </button>
        <button
          onClick={() => navigate('/exams')}
          className="px-5 py-2.5 rounded-xl font-semibold text-sm bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover transition-all duration-150 cursor-pointer"
        >
          Take Exam
        </button>
      </div>
    </div>
  )
}

function DashboardStatCard({ label, value, color }: { label: string; value: string | number; color: string }) {
  return (
    <div className="p-5 rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border">
      <div className={`font-display font-bold text-2xl md:text-3xl mb-1 ${color}`}>{value}</div>
      <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest">{label}</div>
    </div>
  )
}
