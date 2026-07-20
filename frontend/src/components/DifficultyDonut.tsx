interface DifficultyDonutProps {
  easy: number
  medium: number
  hard: number
  total: number
  loading: boolean
}

const S = 160
const SW = 22
const R = (S - SW) / 2
const C = 2 * Math.PI * R
const CX = S / 2

export default function DifficultyDonut({ easy, medium, hard, total, loading }: DifficultyDonutProps) {
  if (loading) {
    return (
      <div className="rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border p-5">
        <div className="w-[160px] h-[160px] mx-auto bg-bg-primary/30 rounded-full animate-pulse" />
        <div className="flex justify-center gap-6 mt-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-4 w-16 bg-bg-primary/30 rounded animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  if (total === 0) {
    return (
      <div className="rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border p-5">
        <p className="text-text-muted font-mono text-xs text-center py-8">No data yet</p>
      </div>
    )
  }

  const aE = (easy / total) * C
  const aM = (medium / total) * C
  const aH = (hard / total) * C

  const arcs: { deg: number; offset: number; color: string; label: string }[] = [
    { deg: aE, offset: 0, color: '#27ae60', label: 'Easy' },
    { deg: aM, offset: -aE, color: '#f39c12', label: 'Medium' },
    { deg: aH, offset: -(aE + aM), color: '#e74c3c', label: 'Hard' },
  ]

  return (
    <div className="rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border p-5 flex flex-col items-center">
      <svg width={S} height={S} viewBox={`0 0 ${S} ${S}`}>
        <circle cx={CX} cy={CX} r={R} fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth={SW} />
        {arcs.map(
          (arc) =>
            arc.deg > 0 && (
              <circle
                key={arc.label}
                cx={CX}
                cy={CX}
                r={R}
                fill="none"
                stroke={arc.color}
                strokeWidth={SW}
                strokeDasharray={`${arc.deg} ${C - arc.deg}`}
                strokeDashoffset={arc.offset}
                transform={`rotate(-90 ${CX} ${CX})`}
                strokeLinecap="round"
                className="transition-all duration-700"
              />
            ),
        )}
        <text x={CX} y={CX - 4} textAnchor="middle" className="fill-text-primary font-display font-bold text-2xl">
          {total}
        </text>
        <text x={CX} y={CX + 14} textAnchor="middle" className="fill-text-muted font-mono text-[9px] uppercase tracking-widest">
          Total
        </text>
      </svg>

      <div className="flex flex-col gap-2 w-full mt-4">
        {[
          { color: '#27ae60', label: 'Easy', value: easy },
          { color: '#f39c12', label: 'Medium', value: medium },
          { color: '#e74c3c', label: 'Hard', value: hard },
        ].map((item) => (
          <div key={item.label} className="flex items-center gap-2.5 text-xs">
            <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: item.color }} />
            <span className="flex-1 font-mono text-text-muted">{item.label}</span>
            <span className="font-mono font-bold text-text-primary">
              {item.value}
              <span className="text-text-muted font-normal ml-0.5">
                ({total > 0 ? Math.round((item.value / total) * 100) : 0}%)
              </span>
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
