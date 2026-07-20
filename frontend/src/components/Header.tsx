import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { Sun, Moon, LogOut, User } from 'lucide-react'
import { useEffect } from 'react'

export default function Header() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const location = useLocation()

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'T') {
        e.preventDefault()
        toggleTheme()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [toggleTheme])

  const isActive = (path: string) => location.pathname.startsWith(path)

  return (
    <header className="sticky top-0 z-50 bg-bg-primary/80 backdrop-blur-xl border-b border-glass-border">
      <div className="max-w-[1080px] mx-auto px-4 md:px-6 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-lg font-bold text-text-primary group">
          <span className="w-7 h-7 rounded-lg bg-accent-red-soft flex items-center justify-center text-white text-sm font-bold group-hover:scale-105 transition-transform">
            P
          </span>
          <span className="hidden sm:inline">Python Dev Trials</span>
        </Link>

        <nav className="flex items-center gap-1">
          <NavLink to="/topics" active={isActive('/topics') || (isActive('/problems') && !isActive('/problems/'))}>
            Problems
          </NavLink>
          <NavLink to="/exams" active={isActive('/exams')}>
            Exams
          </NavLink>
          {user && (
            <NavLink to="/dashboard" active={isActive('/dashboard')}>
              Dashboard
            </NavLink>
          )}

          <div className="w-px h-6 bg-glass-border mx-2" />

          <button
            onClick={toggleTheme}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-text-secondary hover:text-text-primary hover:bg-bg-surface transition-colors cursor-pointer"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {user ? (
            <div className="flex items-center gap-2">
              <Link
                to="/profile"
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-surface transition-colors"
              >
                <User className="w-4 h-4" />
                <span className="hidden sm:inline">{user.username}</span>
              </Link>
              <button
                onClick={logout}
                className="w-8 h-8 rounded-lg flex items-center justify-center text-text-secondary hover:text-wrong hover:bg-wrong-bg transition-colors cursor-pointer"
                aria-label="Log out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link
              to="/login"
              className="px-4 py-1.5 rounded-lg bg-accent-red-soft hover:bg-accent-red text-white text-sm font-semibold transition-colors"
            >
              Sign In
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}

function NavLink({ to, active, children }: { to: string; active: boolean; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      className={`px-3 py-1.5 rounded-lg text-sm font-semibold transition-colors ${
        active
          ? 'bg-bg-surface text-text-primary'
          : 'text-text-secondary hover:text-text-primary hover:bg-bg-surface'
      }`}
    >
      {children}
    </Link>
  )
}
