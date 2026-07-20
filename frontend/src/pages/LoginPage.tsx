import { useState, FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'
import { Link, useNavigate } from 'react-router-dom'
import { LogIn } from 'lucide-react'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login, loading } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    if (!username || !password) {
      setError('Please fill in all fields')
      return
    }
    const result = await login(username, password)
    if (result.success) navigate('/dashboard')
    else setError(result.error || '')
  }

  return (
    <div className="min-h-[70vh] flex items-center justify-center animate-fade-in-up">
      <div className="relative w-full max-w-md">
        {/* Background glow */}
        <div className="pointer-events-none absolute -top-20 -right-20 w-48 h-48 rounded-full bg-accent-red/5 blur-[80px]" />
        <div className="pointer-events-none absolute -bottom-20 -left-20 w-48 h-48 rounded-full bg-accent-gold/5 blur-[80px]" />

        <div className="relative p-8 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.25)]">
          <div className="text-center mb-6">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-red/20 to-accent-gold/20 flex items-center justify-center mx-auto mb-4">
              <LogIn className="w-5 h-5 text-accent-gold-soft" />
            </div>
            <h2 className="text-2xl font-black font-display bg-gradient-to-r from-accent-red to-accent-gold bg-clip-text text-transparent">
              Welcome Back
            </h2>
            <p className="text-text-muted text-sm mt-1">Sign in to your account</p>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-wrong-bg border border-wrong-border text-wrong text-sm font-mono animate-scale-in" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold mb-1.5 text-text-secondary">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold/40 focus:border-accent-gold/50 transition-all"
                placeholder="Enter your username"
                autoComplete="username"
                autoFocus
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1.5 text-text-secondary">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold/40 focus:border-accent-gold/50 transition-all"
                placeholder="Enter your password"
                autoComplete="current-password"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl font-bold text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:shadow-[0_6px_20px_rgba(192,57,43,0.4)] hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-text-secondary text-sm mt-6">
            No account?{' '}
            <Link to="/register" className="text-accent-gold font-semibold hover:underline transition-all">
              Create one
            </Link>
          </p>

          <p className="text-center mt-3">
            <Link to="/" className="text-text-muted text-xs hover:text-text-secondary transition-all">
              or continue without login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
