import { useMemo } from 'react'

interface DayData {
  date: string
  count: number
}

interface ActivityHeatmapProps {
  data: DayData[]
  loading: boolean
}

const CELL = 12
const GAP = 2
const STEP = CELL + GAP
const PX = STEP
const PY = 20
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const LEVELS = ['#1e1e2e', '#0e4429', '#006d32', '#26a641', '#39d353']

function level(count: number): number {
  if (count === 0) return 0
  if (count <= 3) return 1
  if (count <= 7) return 2
  if (count <= 15) return 3
  return 4
}

export default function ActivityHeatmap({ data, loading }: ActivityHeatmapProps) {
  const grid = useMemo(() => {
    if (data.length === 0) return null
    const lookup = new Map(data.map((d) => [d.date, d.count]))

    const today = new Date()
    const cursor = new Date(today)
    cursor.setDate(cursor.getDate() - 364)

    const dow = cursor.getDay()
    cursor.setDate(cursor.getDate() + (dow === 0 ? -6 : 1 - dow))

    const weeks: { date: string; count: number }[][] = []
    for (let w = 0; w < 53; w++) {
      const week: { date: string; count: number }[] = []
      for (let d = 0; d < 7; d++) {
        const iso = cursor.toISOString().slice(0, 10)
        week.push({ date: iso, count: lookup.get(iso) ?? 0 })
        cursor.setDate(cursor.getDate() + 1)
      }
      weeks.push(week)
    }

    const monthLabels: { label: string; col: number }[] = []
    let prev = -1
    for (let w = 0; w < weeks.length; w++) {
      const mid = new Date(weeks[w][3].date).getMonth()
      if (mid !== prev) {
        monthLabels.push({ label: MONTHS[mid], col: w })
        prev = mid
      }
    }

    return { weeks, monthLabels }
  }, [data])

  if (loading) {
    return (
      <div className="rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border p-5">
        <div className="h-[124px] bg-bg-primary/30 rounded-xl animate-pulse" />
      </div>
    )
  }

  if (!grid) {
    return (
      <div className="rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border p-5">
        <p className="text-text-muted font-mono text-xs text-center py-8">No activity data yet</p>
      </div>
    )
  }

  const w = PX + grid.weeks.length * STEP + 4
  const h = PY + 7 * STEP + 4

  return (
    <div className="rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border p-5 overflow-x-auto">
      <svg width={w} height={h} className="font-mono">
        {grid.monthLabels.map(({ label, col }) => (
          <text key={label} x={PX + col * STEP} y={12} className="fill-text-muted text-[9px]">
            {label}
          </text>
        ))}

        {['Mon', 'Wed', 'Fri'].map((label, i) => (
          <text
            key={label}
            x={PX - 4}
            y={PY + [0, 2, 4][i] * STEP + 9}
            textAnchor="end"
            className="fill-text-muted text-[8px]"
          >
            {label}
          </text>
        ))}

        {grid.weeks.map((week, w) =>
          week.map((day, d) => (
            <rect
              key={`${w}-${d}`}
              x={PX + w * STEP}
              y={PY + d * STEP}
              width={CELL}
              height={CELL}
              rx={3}
              style={{ fill: LEVELS[level(day.count)] }}
            >
              <title>
                {new Date(day.date).toLocaleDateString('en-US', {
                  weekday: 'short',
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric',
                })} — {day.count} {day.count === 1 ? 'attempt' : 'attempts'}
              </title>
            </rect>
          )),
        )}
      </svg>
    </div>
  )
}
