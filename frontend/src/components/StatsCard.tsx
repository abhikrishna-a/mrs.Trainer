import { ElementType } from 'react'

interface StatsCardProps {
  label: string
  value: string | number
  Icon?: ElementType
}

export default function StatsCard({ label, value, Icon }: StatsCardProps) {
  return (
    <div className="bg-bg-surface backdrop-blur-xl border border-glass-border rounded-xl p-5 flex items-center gap-4 transition-colors hover:bg-bg-surface-hover">
      {Icon && (
        <div className="w-10 h-10 rounded-lg bg-accent-red-soft/10 flex items-center justify-center shrink-0">
          <Icon className="w-5 h-5 text-accent-red-soft" />
        </div>
      )}
      <div>
        <p className="text-2xl font-bold text-text-primary tabular-nums">{value}</p>
        <p className="text-sm text-text-secondary">{label}</p>
      </div>
    </div>
  )
}
