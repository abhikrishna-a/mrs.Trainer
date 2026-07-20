import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import client from '../api/client'
import { useProblem } from '../context/ProblemContext'
import CodeEditor from '../components/CodeEditor'
import TestCaseResults from '../components/TestCaseResults'
import { ProblemDetail, ExamAnswerResponse } from '../types/api'

const LANGUAGE_LABELS: Record<string, string> = { python: 'Python' }

export default function ProblemDetailPage() {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const { language, setLanguage, code, setCode, startPolling, taskStatus, taskResult, reset } = useProblem()
  const [languages, setLanguages] = useState<{ id: string; label: string }[]>([{ id: 'python', label: 'Python' }])

  useEffect(() => {
    client.get<{ enabled_languages: string[] }>('/config/').then(({ data }) => {
      setLanguages(data.enabled_languages.map((l: string) => ({ id: l, label: LANGUAGE_LABELS[l] || l })))
    }).catch(() => {})
  }, [])

  const [problem, setProblem] = useState<ProblemDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [mcqResult, setMcqResult] = useState<ExamAnswerResponse | null>(null)
  const [mcqChecking, setMcqChecking] = useState(false)

  useEffect(() => {
    if (!slug) return
    const fetchProblem = async () => {
      try {
        const { data } = await client.get<ProblemDetail>(`/problems/${slug}/`)
        setProblem(data)
        const starter = data.starter_code
        if (starter) {
          setCode(starter.python_code || '')
        }
      } catch {
        setError('Failed to load problem')
      } finally {
        setLoading(false)
      }
    }
    fetchProblem()
    return () => reset()
  }, [slug])

  useEffect(() => {
    if (problem?.starter_code) {
      const codeKey = `${language}_code` as keyof typeof problem.starter_code
      setCode((problem.starter_code[codeKey] as string) || '')
    }
  }, [language, problem?.starter_code, setCode])

  const handleMcqCheck = useCallback(async () => {
    if (!selectedOption || !slug) return
    setMcqChecking(true)
    setMcqResult(null)
    try {
      const { data } = await client.post<ExamAnswerResponse>(`/problems/${slug}/answer/`, {
        selected_option_id: selectedOption,
      })
      setMcqResult(data)
    } catch {
      setMcqResult({ is_correct: false })
    } finally {
      setMcqChecking(false)
    }
  }, [slug, selectedOption])

  const handleRun = useCallback(async () => {
    if (!slug) return
    reset()
    try {
      const { data } = await client.post<{ task_id: string }>('/run/', { slug, language, code })
      startPolling(data.task_id, false)
    } catch {
      setError('Failed to submit code')
    }
  }, [slug, language, code, reset, startPolling])

  const handleSubmit = useCallback(async () => {
    if (!slug) return
    reset()
    try {
      const { data } = await client.post<{ task_id: string }>(`/problems/${slug}/submit/`, { language, code })
      startPolling(data.task_id, true)
    } catch {
      setError('Failed to submit solution')
    }
  }, [slug, language, code, reset, startPolling])

  if (loading) {
    return (
      <div className="animate-fade-in-up grid grid-cols-1 lg:grid-cols-2 gap-4 min-h-[70vh]">
        <div className="bg-bg-surface rounded-2xl animate-pulse" />
        <div className="bg-bg-surface rounded-2xl animate-pulse" />
      </div>
    )
  }

  if (error || !problem) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-secondary font-mono mb-4">{error || 'Problem not found'}</p>
          <button onClick={() => navigate('/problems')} className="px-4 py-2 rounded-lg bg-gradient-to-r from-accent-red to-accent-gold text-white font-bold cursor-pointer">
            Back to Problems
          </button>
        </div>
      </div>
    )
  }

  const visibleTestCases = problem.test_cases?.filter((tc) => !tc.is_hidden) || []

  return (
    <div className="animate-fade-in-up grid grid-cols-1 lg:grid-cols-2 gap-4 min-h-[70vh]">
      <div className="bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl p-6 overflow-y-auto">
        <div className="flex items-center gap-2 mb-4 flex-wrap">
          <span className={`font-mono text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded border ${
            problem.difficulty === 'easy' ? 'text-correct bg-correct-bg border-correct-border' :
            problem.difficulty === 'medium' ? 'text-accent-gold bg-accent-gold/10 border-accent-gold/30' :
            'text-accent-red-soft bg-wrong-bg border-wrong-border'
          }`}>
            {problem.difficulty}
          </span>
          <span className="font-mono text-[10px] text-text-muted uppercase">
            {problem.question_type === 'mcq' ? 'MCQ' : 'Coding'}
          </span>
        </div>
        <h2 className="font-display font-bold text-xl text-text-primary mb-4">{problem.title}</h2>
        <p className="text-text-secondary text-sm leading-relaxed whitespace-pre-line mb-6">{problem.text}</p>

        {problem.question_type === 'mcq' && (
          <div className="space-y-3">
            {problem.options?.map((opt, i) => {
              const correctOptionId = mcqResult?.correct_option_id
              const isCorrectOption = mcqResult && opt.id === correctOptionId
              const isWrongSelected = mcqResult && !mcqResult.is_correct && selectedOption === opt.id
              return (
                <button
                  key={opt.id}
                  onClick={() => { if (!mcqResult) { setSelectedOption(opt.id); setMcqResult(null) } }}
                  disabled={!!mcqResult}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-left text-sm transition-all cursor-pointer ${
                    isCorrectOption
                      ? 'bg-correct-bg border-correct text-correct'
                      : isWrongSelected
                        ? 'bg-wrong-bg border-wrong text-wrong'
                        : selectedOption === opt.id
                          ? 'bg-accent-gold/10 border-accent-gold'
                          : 'bg-bg-surface-hover border-glass-border hover:border-accent-gold/30'
                  } ${mcqResult ? 'cursor-default' : ''}`}
                >
                  <span className={`shrink-0 w-7 h-7 rounded-full flex items-center justify-center font-mono text-xs font-bold border ${
                    isCorrectOption
                      ? 'bg-correct text-white border-correct'
                      : isWrongSelected
                        ? 'bg-wrong text-white border-wrong'
                        : selectedOption === opt.id
                          ? 'bg-accent-gold text-white border-accent-gold'
                          : 'bg-white/6 border-glass-border text-text-muted'
                  }`}>
                    {String.fromCharCode(65 + i)}
                  </span>
                  {opt.text}
                  {isCorrectOption && <span className="ml-auto font-mono text-[10px] font-bold">Correct</span>}
                  {isWrongSelected && <span className="ml-auto font-mono text-[10px] font-bold">Your answer</span>}
                </button>
              )
            })}
            <button
              onClick={handleMcqCheck}
              disabled={!selectedOption || mcqChecking || !!mcqResult}
              className="px-6 py-2.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {mcqChecking ? 'Checking...' : mcqResult ? (mcqResult.is_correct ? 'Correct!' : 'Incorrect') : 'Check Answer'}
            </button>
            {mcqResult?.explanation && (
              <div className="p-4 rounded-xl border bg-bg-secondary border-glass-border">
                <p className="font-mono text-[10px] font-bold text-text-muted uppercase tracking-widest mb-2">Explanation</p>
                <p className="text-sm text-text-secondary">{mcqResult.explanation}</p>
              </div>
            )}
          </div>
        )}

        {problem.question_type === 'coding' && visibleTestCases.length > 0 && (
          <div className="mt-6">
            <p className="font-mono text-[10px] font-bold text-text-muted uppercase tracking-widest mb-3">Sample Test Cases</p>
            <div className="space-y-2">
              {visibleTestCases.map((tc, i) => (
                <div key={tc.id || i} className="p-3 rounded-xl bg-bg-secondary border border-glass-border">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-[10px] font-bold text-text-muted">Case {i + 1}</span>
                  </div>
                  {tc.stdin && (
                    <div className="mb-1">
                      <span className="font-mono text-[10px] text-text-muted">Input: </span>
                      <code className="font-mono text-xs text-text-primary">{tc.stdin}</code>
                    </div>
                  )}
                  <div>
                    <span className="font-mono text-[10px] text-text-muted">Expected: </span>
                    <code className="font-mono text-xs text-text-primary">{tc.expected_output}</code>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {problem.question_type === 'coding' ? (
        <div className="flex flex-col bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl overflow-hidden">
          <div className="flex items-center gap-1 px-4 py-2 border-b border-glass-border bg-bg-secondary">
            {languages.map((lang) => (
              <button
                key={lang.id}
                onClick={() => setLanguage(lang.id)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  language === lang.id
                    ? 'bg-accent-gold/20 text-accent-gold'
                    : 'text-text-muted hover:text-text-secondary'
                }`}
              >
                {lang.label}
              </button>
            ))}
            <div className="flex-1" />
            <button
              onClick={handleRun}
              className="px-4 py-1.5 rounded-lg text-xs font-bold bg-bg-surface-hover border border-glass-border text-text-secondary hover:text-text-primary transition-all cursor-pointer"
            >
              Run
            </button>
            <button
              onClick={handleSubmit}
              className="px-4 py-1.5 rounded-lg text-xs font-bold text-white bg-gradient-to-r from-accent-red to-accent-gold hover:-translate-y-0.5 transition-all cursor-pointer"
            >
              Submit
            </button>
          </div>

          <div className="flex-1 min-h-[400px]">
            <CodeEditor
              language={language}
              value={code}
              onChange={(val) => setCode(val || '')}
              height="400px"
            />
          </div>

          {(taskStatus || taskResult) && (
            <div className="border-t border-glass-border p-4 bg-bg-secondary space-y-3">
              {taskStatus === 'PENDING' || taskStatus === 'STARTED' ? (
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 rounded-full border-2 border-accent-gold border-t-transparent animate-spin" />
                  <p className="font-mono text-xs text-text-muted animate-pulse">
                    {taskStatus === 'PENDING' ? 'Queued...' : 'Running...'}
                  </p>
                </div>
              ) : taskResult ? (
                <div>
                  {'results' in taskResult && taskResult.results ? (
                    <TestCaseResults
                      results={taskResult.results}
                      verdict={taskResult.verdict}
                      error={taskResult.error}
                    />
                  ) : taskResult.error ? (
                    <pre className="font-mono text-xs text-wrong whitespace-pre-wrap">{taskResult.error}</pre>
                  ) : (
                    <pre className="font-mono text-xs text-text-secondary whitespace-pre-wrap">
                      {JSON.stringify(taskResult, null, 2)}
                    </pre>
                  )}
                </div>
              ) : null}
            </div>
          )}
        </div>
      ) : null}
    </div>
  )
}
