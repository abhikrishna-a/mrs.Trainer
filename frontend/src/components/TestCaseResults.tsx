import { AlertTriangle, CheckCircle2, XCircle, Clock, Ban } from 'lucide-react'
import { TestCaseResult } from '../types/api'

interface TestCaseResultsProps {
  results?: TestCaseResult[]
  verdict?: string
  error?: string
}

const verdictConfig: Record<string, { icon: typeof CheckCircle2; label: string; bg: string; text: string }> = {
  accepted: { icon: CheckCircle2, label: 'Accepted', bg: 'bg-correct-bg', text: 'text-correct' },
  wrong_answer: { icon: XCircle, label: 'Wrong Answer', bg: 'bg-wrong-bg', text: 'text-wrong' },
  time_limit_exceeded: { icon: Clock, label: 'Time Limit Exceeded', bg: 'bg-wrong-bg', text: 'text-wrong' },
  runtime_error: { icon: AlertTriangle, label: 'Runtime Error', bg: 'bg-wrong-bg', text: 'text-wrong' },
  quota_exceeded: { icon: Ban, label: 'Quota Exceeded', bg: 'bg-wrong-bg', text: 'text-wrong' },
}

export default function TestCaseResults({ results, verdict, error }: TestCaseResultsProps) {
  if (error) {
    return (
      <div className="bg-wrong-bg border border-wrong-border rounded-xl p-4 flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-wrong shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-semibold text-wrong">Execution Error</p>
          <p className="text-sm text-text-secondary mt-1">{error}</p>
        </div>
      </div>
    )
  }

  if (!results || results.length === 0) return null

  const config = verdictConfig[verdict || '']
  const VerdictIcon = config?.icon || CheckCircle2

  return (
    <div className="space-y-3 animate-fade-in-up">
      {verdict && (
        <div className={`${config?.bg} rounded-xl p-4 flex items-center gap-3 border ${config?.bg.replace('bg-', 'border-').replace('-bg', '') || 'border-glass-border'}`}>
          <VerdictIcon className={`w-5 h-5 ${config?.text || 'text-text-primary'} shrink-0`} />
          <span className={`text-sm font-bold ${config?.text || 'text-text-primary'}`}>
            {config?.label || verdict}
          </span>
          <span className="text-xs text-text-muted ml-auto">
            {results.filter((r) => r.passed).length}/{results.length} passed
          </span>
        </div>
      )}

      <div className="space-y-2">
        {results.map((r, i) => (
          <div
            key={i}
            className={`rounded-xl p-4 border transition-all ${
              r.passed
                ? 'bg-correct-bg border-correct-border'
                : 'bg-wrong-bg border-wrong-border'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-text-primary">Test Case {i + 1}</span>
              {r.passed ? (
                <CheckCircle2 className="w-4 h-4 text-correct" />
              ) : (
                <XCircle className="w-4 h-4 text-wrong" />
              )}
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              {[
                { label: 'Input', value: r.output || '(empty)' },
                { label: 'Expected', value: r.expected || '(empty)' },
              ].map((field) => (
                <div key={field.label}>
                  <p className="text-text-muted mb-1">{field.label}</p>
                  <pre className="bg-bg-primary/50 rounded-lg p-2 text-text-primary font-mono overflow-x-auto max-h-20">
                    {field.value}
                  </pre>
                </div>
              ))}
            </div>
            {r.error && (
              <p className="text-xs text-wrong mt-2">{r.error}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
