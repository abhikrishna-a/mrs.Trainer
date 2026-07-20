import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import { Role, Topic } from '../types/api'
import { BookOpen, GraduationCap, ArrowRight } from 'lucide-react'

const ROLE_ICONS: Record<string, typeof BookOpen> = {
  quantitative: GraduationCap,
  'logical-reasoning': BookOpen,
  dsa: BookOpen,
  python: BookOpen,
}

const ROLE_COLORS: Record<string, string> = {
  quantitative: 'from-blue-500/20 to-blue-600/10 border-blue-500/20 text-blue-400',
  'logical-reasoning': 'from-purple-500/20 to-purple-600/10 border-purple-500/20 text-purple-400',
  dsa: 'from-orange-500/20 to-orange-600/10 border-orange-500/20 text-orange-400',
  python: 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/20 text-emerald-400',
}

export default function TopicsPage() {
  const [roles, setRoles] = useState<Role[]>([])
  const [topics, setTopics] = useState<Topic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data: rolesData } = await client.get<Role[]>('/roles/')
        setRoles(rolesData)
        const { data: topicsData } = await client.get<Topic[]>('/topics/')
        setTopics(topicsData)
      } catch {
        setError('Failed to load data')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-44 bg-bg-surface rounded-2xl animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center p-10 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-3xl">
          <p className="text-text-secondary font-mono text-sm mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 rounded-xl font-bold text-white bg-gradient-to-r from-accent-red to-accent-gold cursor-pointer hover:-translate-y-0.5 transition-all"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="animate-fade-in-up space-y-10 pb-8">
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Roles</h2>
          <span className="font-mono text-[10px] text-text-muted uppercase tracking-wider">{roles.length} tracks</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {roles.map((role) => {
            const Icon = ROLE_ICONS[role.slug] || BookOpen
            const colors = ROLE_COLORS[role.slug] || 'from-accent-red/10 to-accent-gold/10 border-glass-border text-accent-gold'
            return (
              <button
                key={role.id}
                onClick={() => navigate(`/exams?role=${role.slug}`)}
                className={`group relative overflow-hidden rounded-2xl border p-6 bg-gradient-to-br ${colors} backdrop-blur-[14px] hover:-translate-y-1 transition-all duration-300 text-left cursor-pointer`}
              >
                <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-display font-bold text-lg text-text-primary mb-1.5">{role.name}</h3>
                <p className="text-text-muted text-sm mb-4">{role.description || 'Practice for this role'}</p>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-text-muted">
                    {role.topic_count || 0} topics
                  </span>
                  <span className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <ArrowRight className="w-4 h-4 text-text-muted" />
                  </span>
                </div>
              </button>
            )
          })}
        </div>
      </section>

      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Topics</h2>
          <span className="font-mono text-[10px] text-text-muted uppercase tracking-wider">{topics.length} available</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics.map((topic) => (
            <button
              key={topic.id}
              onClick={() => navigate(`/problems?topic=${topic.short_name.toLowerCase()}`)}
              className="group relative overflow-hidden rounded-2xl border border-glass-border p-5 bg-bg-surface backdrop-blur-[14px] hover:bg-bg-surface-hover hover:-translate-y-0.5 transition-all duration-300 text-left cursor-pointer"
            >
              <div className="flex items-start justify-between">
                <h3 className="font-display font-bold text-base text-text-primary mb-2">{topic.name}</h3>
                <ArrowRight className="w-4 h-4 text-text-muted opacity-0 group-hover:opacity-100 transition-all duration-300 -translate-x-1 group-hover:translate-x-0" />
              </div>
              <span className="font-mono text-xs text-text-muted">
                {topic.question_count || 0} questions
              </span>
            </button>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative overflow-hidden rounded-3xl border border-glass-border p-8 md:p-12 text-center"
        style={{ background: 'linear-gradient(135deg, rgba(192,57,43,0.06), rgba(212,160,23,0.06))' }}>
        <div className="pointer-events-none absolute inset-0 -z-10">
          <div className="absolute -top-16 -right-16 w-48 h-48 rounded-full bg-accent-red/5 blur-[80px]" />
          <div className="absolute -bottom-16 -left-16 w-48 h-48 rounded-full bg-accent-gold/5 blur-[80px]" />
        </div>
        <h2 className="font-display font-black text-2xl md:text-3xl text-text-primary mb-3">
          Ready to test your skills?
        </h2>
        <p className="text-text-secondary text-sm md:text-base max-w-md mx-auto mb-6">
          Take a timed exam and measure your progress across all topics.
        </p>
        <button
          onClick={() => navigate('/exams')}
          className="group px-8 py-3.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_20px_rgba(192,57,43,0.3)] hover:shadow-[0_8px_32px_rgba(192,57,43,0.4)] hover:-translate-y-0.5 transition-all duration-300 cursor-pointer inline-flex items-center gap-2"
        >
          Start Exam
          <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
        </button>
      </section>
    </div>
  )
}
