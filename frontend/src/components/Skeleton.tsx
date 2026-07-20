interface SkeletonProps {
  className?: string
  count?: number
}

export default function Skeleton({ className = 'h-16 rounded-xl', count = 1 }: SkeletonProps) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className={`bg-bg-surface animate-pulse ${className}`} />
      ))}
    </>
  )
}
