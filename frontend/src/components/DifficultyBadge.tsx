import { Difficulty } from '../types/api'

const difficultyConfig: Record<string, { border: string; text: string }> = {
  Easy: { border: 'border-difficulty-easy', text: 'text-difficulty-easy' },
  Medium: { border: 'border-difficulty-medium', text: 'text-difficulty-medium' },
  Hard: { border: 'border-difficulty-hard', text: 'text-difficulty-hard' },
}

interface DifficultyBadgeProps {
  difficulty: Difficulty
}

export default function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  const label = difficulty.charAt(0).toUpperCase() + difficulty.slice(1)
  const config = difficultyConfig[label] || { border: 'border-text-muted', text: 'text-text-muted' }

  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded border ${config.border} ${config.text}`}>
      {label}
    </span>
  )
}
