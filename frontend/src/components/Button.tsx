import { Link } from 'react-router-dom'

interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  to?: string
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  className?: string
  type?: 'button' | 'submit'
}

const variantStyles: Record<string, string> = {
  primary:
    'text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5',
  secondary:
    'bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover',
  ghost:
    'text-text-secondary hover:text-text-primary hover:bg-bg-surface',
}

const sizeStyles: Record<string, string> = {
  sm: 'px-3 py-1.5 text-xs rounded-lg',
  md: 'px-5 py-2.5 text-sm rounded-xl',
  lg: 'px-7 py-3 text-sm rounded-xl',
}

export default function Button({
  children, onClick, to, variant = 'primary', size = 'md',
  disabled, className = '', type = 'button',
}: ButtonProps) {
  const base = `font-bold transition-all duration-150 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2 ${variantStyles[variant]} ${sizeStyles[size]} ${className}`

  if (to) {
    return <Link to={to} className={base}>{children}</Link>
  }

  return (
    <button type={type} onClick={onClick} disabled={disabled} className={base}>
      {children}
    </button>
  )
}
