import type { ExamSession } from '../types/api'

interface ExamHistoryRowProps {
  exam: ExamSession
}

export default function ExamHistoryRow({ exam }: ExamHistoryRowProps) {
  const correct = exam.score || 0
  const total = exam.total_questions || 0
  const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0

  const date = exam.finished_at || exam.started_at
  const formattedDate = date ? new Date(date).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  }) : 'N/A'

  return (
    <div className="flex items-center gap-4 px-5 py-4 rounded-xl bg-bg-surface border border-glass-border hover:bg-bg-surface-hover transition-all">
      <div className="flex-1 min-w-0">
        <p className="font-display font-semibold text-sm text-text-primary mb-0.5">
          {exam.mode === 'full_mock' ? 'Full Mock Exam' : 'Quick Practice'}
        </p>
        <p className="font-mono text-xs text-text-muted">{formattedDate}</p>
      </div>
      <div className="text-center">
        <span className="block font-mono font-bold text-sm text-accent-gold">{accuracy}%</span>
        <span className="block font-mono text-[10px] text-text-muted">Accuracy</span>
      </div>
      <div className="text-center">
        <span className="block font-mono font-bold text-sm text-text-primary">{correct}/{total}</span>
        <span className="block font-mono text-[10px] text-text-muted">Score</span>
      </div>
      <svg className="w-4 h-4 text-text-muted shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  )
}
