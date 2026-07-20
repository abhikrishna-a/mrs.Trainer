import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import { DashboardData, ProblemSummary } from '../types/api'
import { CheckCircle2, Target, TrendingUp, Flame, ArrowRight, Calendar } from 'lucide-react'
import ActivityHeatmap from '../components/ActivityHeatmap'
import DifficultyDonut from '../components/DifficultyDonut'

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [activity, setActivity] = useState<{ date: string; count: number }[]>([])
  const [heatmapLoading, setHeatmapLoading] = useState(true)

  const [solvedEasy, setSolvedEasy] = useState(0)
  const [solvedMedium, setSolvedMedium] = useState(0)
  const [solvedHard, setSolvedHard] = useState(0)
  const [donutLoading, setDonutLoading] = useState(true)

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

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const { data } = await client.get<{ activity: { date: string; count: number }[] }>('/dashboard/activity/')
        setActivity(data.activity)
      } catch {
        // silently fail
      } finally {
        setHeatmapLoading(false)
      }
    }
    fetchActivity()
  }, [])

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const { data } = await client.get<ProblemSummary[]>('/problems/')
        const solved = data.filter((p) => p.user_solved)
        setSolvedEasy(solved.filter((p) => p.difficulty === 'easy').length)
        setSolvedMedium(solved.filter((p) => p.difficulty === 'medium').length)
        setSolvedHard(solved.filter((p) => p.difficulty === 'hard').length)
      } catch {
        // silently fail
      } finally {
        setDonutLoading(false)
      }
    }
    fetchProblems()
  }, [])

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-32 bg-bg-surface rounded-2xl animate-pulse" />
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

  const stats: { label: string; value: string | number; icon: typeof CheckCircle2; color: string; bg: string }[] = [
    { label: 'Problems Solved', value: dashboard?.questions_solved || 0, icon: CheckCircle2, color: 'text-correct', bg: 'bg-correct-bg' },
    { label: 'Attempted', value: dashboard?.questions_attempted || 0, icon: Target, color: 'text-accent-gold', bg: 'bg-accent-gold/10' },
    { label: 'Accuracy', value: `${accuracy}%`, icon: TrendingUp, color: 'text-accent-red-soft', bg: 'bg-wrong-bg' },
    { label: 'Streak', value: `${dashboard?.current_streak || 0}d`, icon: Flame, color: 'text-accent-gold-soft', bg: 'bg-accent-gold/10' },
  ]

  return (
    <div className="animate-fade-in-up space-y-8 pb-8">
      <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Dashboard</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="p-5 rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border hover:bg-bg-surface-hover transition-all duration-300">
            <div className={`w-9 h-9 rounded-xl ${stat.bg} flex items-center justify-center mb-3`}>
              <stat.icon className={`w-4.5 h-4.5 ${stat.color}`} />
            </div>
            <div className={`font-display font-bold text-2xl md:text-3xl mb-1 ${stat.color}`}>{stat.value}</div>
            <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest">{stat.label}</div>
          </div>
        ))}
      </div>

      <section>
        <h3 className="font-mono text-xs font-bold text-text-muted uppercase tracking-widest mb-4 flex items-center gap-2">
          <Calendar className="w-3.5 h-3.5" />
          Activity
        </h3>
        <div className="flex flex-col 2xl:flex-row gap-4">
          <div className="flex-1 min-w-0">
            <ActivityHeatmap data={activity} loading={heatmapLoading} />
          </div>
          <div className="2xl:w-64 shrink-0">
            <DifficultyDonut
              easy={solvedEasy}
              medium={solvedMedium}
              hard={solvedHard}
              total={solvedEasy + solvedMedium + solvedHard}
              loading={donutLoading}
            />
          </div>
        </div>
      </section>

      {dashboard?.last_practice_date && (
        <section>
          <h3 className="font-mono text-xs font-bold text-text-muted uppercase tracking-widest mb-4 flex items-center gap-2">
            <Calendar className="w-3.5 h-3.5" />
            Last Practice
          </h3>
          <div className="flex items-center gap-3 px-5 py-3.5 rounded-xl bg-bg-surface border border-glass-border">
            <div className="w-2.5 h-2.5 rounded-full bg-correct animate-pulse" />
            <p className="flex-1 text-sm text-text-primary">
              {new Date(dashboard.last_practice_date).toLocaleDateString(undefined, {
                weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
              })}
            </p>
          </div>
        </section>
      )}

      <div className="flex items-center justify-center gap-3 pt-2">
        <button
          onClick={() => navigate('/problems')}
          className="group px-6 py-2.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:shadow-[0_8px_24px_rgba(192,57,43,0.4)] hover:-translate-y-0.5 transition-all duration-300 cursor-pointer inline-flex items-center gap-2"
        >
          Practice Problems
          <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
        </button>
        <button
          onClick={() => navigate('/exams')}
          className="px-5 py-2.5 rounded-xl font-semibold text-sm bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover hover:-translate-y-0.5 transition-all duration-300 cursor-pointer"
        >
          Take Exam
        </button>
      </div>
    </div>
  )
}
