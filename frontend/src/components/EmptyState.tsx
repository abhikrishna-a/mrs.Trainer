import Button from './Button'

interface EmptyStateProps {
  message?: string
  actionLabel?: string
  actionTo?: string
}

export default function EmptyState({
  message = 'Nothing here yet',
  actionLabel,
  actionTo,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-16 h-16 rounded-full bg-bg-surface border border-glass-border flex items-center justify-center mb-4">
        <svg className="w-6 h-6 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m8.25 3v6.75m0 0l-3-3m3 3l3-3M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
        </svg>
      </div>
      <p className="font-mono text-sm text-text-muted mb-6">{message}</p>
      {actionLabel && actionTo && (
        <Button variant="primary" size="md" to={actionTo}>
          {actionLabel}
        </Button>
      )}
    </div>
  )
}
