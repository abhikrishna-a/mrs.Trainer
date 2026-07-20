import { Link, useLocation, NavLink as RRNavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { Sun, Moon, LogOut, User, ChevronDown } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

const NAV_ITEMS = [
  { to: '/topics', label: 'Problems' },
  { to: '/exams', label: 'Exams' },
]

const AUTH_NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard' },
]

export default function Header() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const [profileOpen, setProfileOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

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

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setProfileOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <header className="sticky top-0 z-50 bg-bg-primary/80 backdrop-blur-xl border-b border-glass-border">
      <div className="max-w-[1080px] mx-auto px-4 md:px-6 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5 group shrink-0">
          <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-red to-accent-gold flex items-center justify-center text-white text-sm font-bold shadow-[0_2px_8px_rgba(192,57,43,0.3)] group-hover:shadow-[0_4px_16px_rgba(192,57,43,0.45)] transition-all duration-300 group-hover:scale-105">
            A
          </span>
          <span className="hidden sm:inline font-display font-bold text-text-primary tracking-tight">
            AlgoForge
          </span>
        </Link>

        <nav className="flex items-center gap-1">
          {NAV_ITEMS.map(({ to, label }) => (
            <NavItem key={to} to={to} label={label} />
          ))}
          {user && AUTH_NAV_ITEMS.map(({ to, label }) => (
            <NavItem key={to} to={to} label={label} />
          ))}

          <div className="w-px h-5 bg-glass-border mx-2" />

          <button
            onClick={toggleTheme}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-text-secondary hover:text-text-primary hover:bg-bg-surface transition-all duration-200 cursor-pointer"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {user ? (
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setProfileOpen((p) => !p)}
                className="flex items-center gap-2 pl-2.5 pr-2 py-1.5 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-surface transition-all duration-200 cursor-pointer"
              >
                <User className="w-4 h-4" />
                <span className="hidden sm:inline text-sm font-medium max-w-[100px] truncate">{user.username}</span>
                <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${profileOpen ? 'rotate-180' : ''}`} />
              </button>
              {profileOpen && (
                <div className="absolute right-0 top-full mt-1 w-44 p-1.5 rounded-xl bg-bg-elevated border border-glass-border backdrop-blur-xl shadow-[0_8px_32px_rgba(0,0,0,0.4)] animate-scale-in origin-top-right">
                  <Link
                    to="/profile"
                    onClick={() => setProfileOpen(false)}
                    className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-surface transition-all cursor-pointer"
                  >
                    <User className="w-4 h-4" />
                    Profile
                  </Link>
                  <button
                    onClick={() => { logout(); setProfileOpen(false) }}
                    className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-wrong hover:bg-wrong-bg transition-all cursor-pointer"
                  >
                    <LogOut className="w-4 h-4" />
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-3.5 py-1.5 rounded-lg text-sm font-semibold text-text-secondary hover:text-text-primary hover:bg-bg-surface transition-all duration-200"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-1.5 rounded-lg text-sm font-bold text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_2px_8px_rgba(192,57,43,0.25)] hover:shadow-[0_4px_16px_rgba(192,57,43,0.35)] hover:-translate-y-0.5 transition-all duration-200"
              >
                Get Started
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  )
}

function NavItem({ to, label }: { to: string; label: string }) {
  const location = useLocation()
  const active = location.pathname === to || location.pathname.startsWith(to + '/') ||
    (to === '/topics' && (location.pathname === '/problems' || location.pathname.startsWith('/problems/')))
  return (
    <RRNavLink
      to={to}
      className={`relative px-3 py-1.5 rounded-lg text-sm font-semibold transition-all duration-200 ${
        active
          ? 'text-text-primary'
          : 'text-text-secondary hover:text-text-primary hover:bg-bg-surface'
      }`}
    >
      {label}
      {active && (
        <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-5 h-0.5 rounded-full bg-gradient-to-r from-accent-red to-accent-gold" />
      )}
    </RRNavLink>
  )
}
