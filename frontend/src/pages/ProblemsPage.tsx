import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import client from '../api/client'
import { ProblemSummary } from '../types/api'

const difficulties = ['all', 'easy', 'medium', 'hard']
const types = ['all', 'mcq', 'coding']

export default function ProblemsPage() {
  const [problems, setProblems] = useState<ProblemSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchParams, setSearchParams] = useSearchParams()
  const navigate = useNavigate()

  const activeTopic = searchParams.get('topic') || ''
  const activeDifficulty = searchParams.get('difficulty') || 'all'
  const activeType = searchParams.get('type') || 'all'

  useEffect(() => {
    const fetchProblems = async () => {
      setLoading(true)
      try {
        const params: Record<string, string> = {}
        if (activeTopic) params.topic = activeTopic
        if (activeDifficulty !== 'all') params.difficulty = activeDifficulty
        if (activeType !== 'all') params.type = activeType
        const qs = new URLSearchParams(params).toString()
        const { data } = await client.get<ProblemSummary[]>(`/problems/${qs ? `?${qs}` : ''}`)
        setProblems(Array.isArray(data) ? data : [])
      } catch {
        setError('Failed to load problems')
      } finally {
        setLoading(false)
      }
    }
    fetchProblems()
  }, [activeTopic, activeDifficulty, activeType])

  const updateFilter = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams)
    if (value === 'all' || (key === 'topic' && !value)) next.delete(key)
    else next.set(key, value)
    setSearchParams(next)
  }

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-4">
        <div className="h-10 bg-bg-surface rounded-xl animate-pulse" />
        <div className="space-y-3">
          {Array.from({ length: 8 }).map((_, i) => (
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

  return (
    <div className="animate-fade-in-up space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="font-display font-black text-xl md:text-2xl text-text-primary">Problems</h2>
        <span className="font-mono text-xs text-text-muted">{problems.length} problems</span>
      </div>

      <div className="flex flex-wrap gap-3">
        {activeTopic && (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-accent-gold/20 border border-accent-gold/30">
            <span className="font-mono text-[10px] font-bold text-accent-gold uppercase tracking-widest">
              Topic: {activeTopic.toUpperCase()}
            </span>
            <button
              onClick={() => updateFilter('topic', '')}
              className="text-text-muted hover:text-text-primary transition-colors cursor-pointer text-xs"
            >
              ✕
            </button>
          </div>
        )}
        <FilterTabs
          label="Difficulty"
          items={difficulties.map((d) => ({ slug: d, name: d.charAt(0).toUpperCase() + d.slice(1) }))}
          active={activeDifficulty}
          onChange={(v) => updateFilter('difficulty', v)}
        />
        <FilterTabs
          label="Type"
          items={types.map((t) => ({ slug: t, name: t === 'all' ? 'All' : t === 'mcq' ? 'MCQ' : 'Coding' }))}
          active={activeType}
          onChange={(v) => updateFilter('type', v)}
        />
      </div>

      <div className="space-y-2">
        {problems.length === 0 ? (
          <p className="text-center text-text-muted py-12 font-mono">No problems match your filters</p>
        ) : (
          problems.map((problem) => (
            <ProblemRow key={problem.id} problem={problem} onClick={() => navigate(`/problems/${problem.slug}`)} />
          ))
        )}
      </div>
    </div>
  )
}

function FilterTabs({
  label, items, active, onChange,
}: {
  label: string
  items: { slug: string; name: string }[]
  active: string
  onChange: (slug: string) => void
}) {
  return (
    <div className="flex items-center gap-1.5 flex-wrap">
      <span className="font-mono text-[10px] font-bold text-text-muted uppercase tracking-widest mr-1">{label}</span>
      {items.map((item) => (
        <button
          key={item.slug}
          onClick={() => onChange(item.slug)}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            active === item.slug
              ? 'bg-accent-gold/20 text-accent-gold border border-accent-gold/30'
              : 'bg-bg-surface border border-glass-border text-text-secondary hover:bg-bg-surface-hover'
          }`}
        >
          {item.name}
        </button>
      ))}
    </div>
  )
}

function ProblemRow({ problem, onClick }: { problem: ProblemSummary; onClick: () => void }) {
  const diffColor: Record<string, string> = {
    easy: 'text-correct bg-correct-bg border-correct-border',
    medium: 'text-accent-gold bg-accent-gold/10 border-accent-gold/30',
    hard: 'text-accent-red-soft bg-wrong-bg border-wrong-border',
  }

  return (
    <div
      onClick={onClick}
      className="flex items-center gap-4 px-5 py-3.5 rounded-xl bg-bg-surface border border-glass-border hover:bg-bg-surface-hover transition-all cursor-pointer"
    >
      <span className="flex-1 font-display font-medium text-sm text-text-primary truncate">{problem.title}</span>
      {problem.topic_name && (
        <span className="font-mono text-[10px] text-text-muted">{problem.topic_name}</span>
      )}
      <span className={`font-mono text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded border ${diffColor[problem.difficulty] || 'text-text-muted'}`}>
        {problem.difficulty}
      </span>
      <span className="font-mono text-[10px] text-text-muted uppercase">
        {problem.question_type === 'mcq' ? 'MCQ' : 'Coding'}
      </span>
      <svg className="w-4 h-4 text-text-muted shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  )
}
