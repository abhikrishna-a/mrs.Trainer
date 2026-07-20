interface CardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
  hover?: boolean
}

export default function Card({ children, className = '', onClick, hover = false }: CardProps) {
  return (
    <div
      onClick={onClick}
      className={`rounded-2xl bg-bg-surface backdrop-blur-[14px] border border-glass-border shadow-[0_8px_32px_rgba(0,0,0,0.25)] ${
        hover ? 'hover:bg-bg-surface-hover hover:-translate-y-0.5 transition-all duration-200 cursor-pointer' : ''
      } ${className}`}
    >
      {children}
    </div>
  )
}
