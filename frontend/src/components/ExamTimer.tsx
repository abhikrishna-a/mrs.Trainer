interface ExamTimerProps {
  secondsLeft: number
  total: number
}

export default function ExamTimer({ secondsLeft, total }: ExamTimerProps) {
  const minutes = Math.floor(secondsLeft / 60)
  const seconds = secondsLeft % 60
  const pct = total > 0 ? (secondsLeft / total) * 100 : 0
  const isWarning = secondsLeft < 300
  const isDanger = secondsLeft < 60

  return (
    <div className="bg-bg-surface backdrop-blur-xl border border-glass-border rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-text-secondary font-semibold">Time Remaining</span>
        <span
          className={`text-xl font-bold font-mono tabular-nums transition-colors ${
            isDanger ? 'text-timer-danger' : isWarning ? 'text-timer-warning' : 'text-text-primary'
          }`}
        >
          {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
        </span>
      </div>
      <div className="h-1.5 rounded-full bg-bg-surface-active overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-linear ${
            isDanger ? 'bg-timer-danger' : isWarning ? 'bg-timer-warning' : 'bg-accent-red-soft'
          }`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
