interface ExamQuestionNavProps {
  total: number
  currentIndex: number
  answers: Record<number, { selectedOptionId: number; isCorrect: boolean }>
  questions: { id: number }[]
  onSelect: (index: number) => void
}

export default function ExamQuestionNav({ total, currentIndex, answers, questions, onSelect }: ExamQuestionNavProps) {
  return (
    <div className="bg-bg-surface backdrop-blur-xl border border-glass-border rounded-xl p-4">
      <p className="text-sm font-semibold text-text-secondary mb-3">Questions</p>
      <div className="grid grid-cols-6 gap-1.5">
        {questions.map((q, i) => {
          const isAnswered = answers[q.id] !== undefined
          const isCurrent = i === currentIndex
          return (
            <button
              key={q.id}
              onClick={() => onSelect(i)}
              className={`w-8 h-8 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                isCurrent
                  ? 'bg-accent-red-soft text-white ring-2 ring-accent-red-soft/50'
                  : isAnswered
                    ? 'bg-correct-bg text-correct border border-correct-border'
                    : 'bg-bg-surface-active text-text-secondary hover:bg-bg-surface-hover'
              }`}
            >
              {i + 1}
            </button>
          )
        })}
      </div>
      <p className="text-xs text-text-muted mt-3 text-center">
        {Object.keys(answers).length} of {total} answered
      </p>
    </div>
  )
}
