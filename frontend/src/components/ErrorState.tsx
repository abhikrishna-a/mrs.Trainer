import Button from './Button'

interface ErrorStateProps {
  message?: string
  onRetry?: () => void
  backTo?: string
  backLabel?: string
}

export default function ErrorState({
  message = 'Something went wrong',
  onRetry,
  backTo,
  backLabel = 'Go Back',
}: ErrorStateProps) {
  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="text-center p-10 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-3xl max-w-md">
        <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-wrong-bg flex items-center justify-center">
          <span className="text-wrong text-2xl font-bold">!</span>
        </div>
        <p className="text-text-secondary font-mono text-sm mb-6">{message}</p>
        <div className="flex items-center justify-center gap-3">
          {onRetry && (
            <Button variant="primary" size="md" onClick={onRetry}>
              Retry
            </Button>
          )}
          {backTo && (
            <Button variant="secondary" size="md" to={backTo}>
              {backLabel}
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
