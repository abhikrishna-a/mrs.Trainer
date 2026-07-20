import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import { Role, Topic } from '../types/api'

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
        <div className="relative overflow-hidden rounded-3xl h-72 bg-bg-surface animate-pulse" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-40 bg-bg-surface rounded-2xl animate-pulse" />
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
    <div className="animate-fade-in-up space-y-8">
      <section>
        <h2 className="font-display font-black text-xl md:text-2xl text-text-primary mb-6">Roles</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {roles.map((role) => (
            <div
              key={role.id}
              className="group relative overflow-hidden rounded-2xl border border-glass-border p-6 bg-bg-surface backdrop-blur-[14px] hover:bg-bg-surface-hover transition-all duration-300 cursor-pointer hover:-translate-y-1"
              onClick={() => navigate(`/exams?role=${role.slug}`)}
            >
              <h3 className="font-display font-bold text-lg text-text-primary mb-2">{role.name}</h3>
              <p className="text-text-muted text-sm mb-4">{role.description || 'Practice for this role'}</p>
              <span className="font-mono text-xs text-text-muted">
                {role.topic_count || 0} topics
              </span>
            </div>
          ))}
        </div>
      </section>

      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Topics</h2>
          <span className="font-mono text-xs text-text-muted">{topics.length} topics</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics.map((topic) => (
            <div
              key={topic.id}
              className="group relative overflow-hidden rounded-2xl border border-glass-border p-6 bg-bg-surface backdrop-blur-[14px] hover:bg-bg-surface-hover transition-all duration-300 cursor-pointer hover:-translate-y-1"
              onClick={() => navigate(`/problems?topic=${topic.short_name.toLowerCase()}`)}
            >
              <h3 className="font-display font-bold text-base text-text-primary mb-2">{topic.name}</h3>
              <span className="font-mono text-xs text-text-muted">
                {topic.question_count || 0} questions
              </span>
            </div>
          ))}
        </div>
      </section>

      <section className="relative overflow-hidden rounded-3xl border border-glass-border p-8 md:p-12 text-center"
        style={{ background: 'rgba(26,26,38,0.4)' }}>
        <h2 className="font-display font-black text-2xl md:text-3xl mb-3">
          Ready to test your skills?
        </h2>
        <p className="text-text-secondary text-sm md:text-base max-w-md mx-auto mb-6">
          Take a timed exam and measure your progress across all topics.
        </p>
        <button
          onClick={() => navigate('/exams')}
          className="group px-8 py-3.5 rounded-2xl font-bold text-white cursor-pointer transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_8px_32px_rgba(192,57,43,0.35)]"
          style={{ background: 'linear-gradient(135deg, #c0392b, #d4a017)' }}
        >
          <span className="flex items-center gap-2">
            Start Exam
            <svg className="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </span>
        </button>
      </section>
    </div>
  )
}
