import { useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useExam } from '../context/ExamContext'
import ExamQuestionNav from '../components/ExamQuestionNav'
import ExamTimer from '../components/ExamTimer'
import type { AnswerOption } from '../types/api'

export default function ExamPage() {
  const { examId } = useParams<{ examId: string }>()
  const navigate = useNavigate()
  const {
    session, questions, currentIndex, currentQuestion, answers, timeLeft,
    loading, error, finishExam, answerQuestion, goToQuestion,
  } = useExam()

  useEffect(() => {
    if (timeLeft <= 0 && session && !session.is_completed) {
      finishExam().then(() => navigate(`/exam/${examId}/results`))
    }
  }, [timeLeft, session, finishExam, navigate, examId])

  useEffect(() => {
    if (session?.is_completed) {
      navigate(`/exam/${examId}/results`)
    }
  }, [session?.is_completed, navigate, examId])

  const handleSelectOption = useCallback(async (questionId: number, optionId: number) => {
    try {
      await answerQuestion(questionId, optionId)
    } catch {}
  }, [answerQuestion])

  const handleFinish = useCallback(async () => {
    const unanswered = questions.length - Object.keys(answers).length
    if (unanswered > 0) {
      if (!window.confirm(`You have ${unanswered} unanswered question(s). Submit anyway?`)) return
    }
    await finishExam()
    navigate(`/exam/${examId}/results`)
  }, [questions, answers, finishExam, navigate, examId])

  if (loading) {
    return (
      <div className="animate-fade-in-up space-y-4">
        <div className="h-10 bg-bg-surface rounded-lg animate-pulse" />
        <div className="h-48 bg-bg-surface rounded-2xl animate-pulse" />
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-14 bg-bg-surface rounded-xl animate-pulse" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center p-8 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl">
          <p className="text-wrong font-mono text-sm mb-4">{error}</p>
          <button onClick={() => navigate('/exams')} className="px-4 py-2 rounded-lg bg-gradient-to-r from-accent-red to-accent-gold text-white font-bold cursor-pointer">
            Back to Exams
          </button>
        </div>
      </div>
    )
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <p className="text-text-muted font-mono">No questions available</p>
      </div>
    )
  }

  const question = currentQuestion.question
  const questionText = question?.text || ''
  const qId = question?.id || 0
  const options = question?.options || []

  return (
    <div className="flex gap-4 animate-fade-in-up">
      <div className="hidden lg:block w-48 shrink-0 self-start sticky top-4">
        <ExamQuestionNav
          total={questions.length}
          currentIndex={currentIndex}
          answers={answers}
          questions={questions}
          onSelect={goToQuestion}
        />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-6">
          <span className="font-mono text-sm text-text-secondary">
            Question {currentIndex + 1} of {questions.length}
          </span>
          <div className="flex items-center gap-3">
            <ExamTimer secondsLeft={timeLeft} total={session?.mode === 'full_mock' ? 2700 : 1200} />
            <button
              onClick={handleFinish}
              className="px-4 py-2 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
            >
              Finish Exam
            </button>
          </div>
        </div>

        <div className="p-6 md:p-7 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.25)] mb-4">
          <p className="text-base md:text-lg font-semibold leading-relaxed whitespace-pre-line">
            {questionText}
          </p>
        </div>

        <div className="flex flex-col gap-2.5 mb-4" role="radiogroup" aria-label="Answer options">
          {options.map((opt: AnswerOption, i: number) => {
            const isSelected = answers[qId]?.selectedOptionId === opt.id
            return (
              <button
                key={opt.id}
                role="radio"
                aria-checked={isSelected}
                onClick={() => handleSelectOption(qId, opt.id)}
                className={`flex items-center gap-3.5 px-5 py-3.5 rounded-xl border text-left font-display text-sm transition-all duration-150 cursor-pointer ${
                  isSelected
                    ? 'bg-accent-gold/10 border-accent-gold'
                    : 'bg-bg-surface hover:bg-bg-surface-hover hover:border-accent-gold/20'
                } ${isSelected ? '' : ''}`}
              >
                <span className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-mono font-bold text-xs border ${
                  isSelected
                    ? 'bg-accent-gold text-white border-accent-gold'
                    : 'bg-white/6 border-glass-border text-text-secondary'
                }`}>
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="flex-1 leading-relaxed">{opt.text}</span>
              </button>
            )
          })}
        </div>

        <div className="flex items-center justify-between">
          <button
            onClick={() => goToQuestion(currentIndex - 1)}
            disabled={currentIndex === 0}
            className="px-4 py-2.5 rounded-xl font-semibold text-sm bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer"
          >
            Previous
          </button>
          {currentIndex < questions.length - 1 ? (
            <button
              onClick={() => goToQuestion(currentIndex + 1)}
              className="px-6 py-2.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleFinish}
              className="px-6 py-2.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
            >
              Submit Exam
            </button>
          )}
        </div>

        <div className="lg:hidden mt-6">
          <ExamQuestionNav
            total={questions.length}
            currentIndex={currentIndex}
            answers={answers}
            questions={questions}
            onSelect={goToQuestion}
          />
        </div>
      </div>
    </div>
  )
}
