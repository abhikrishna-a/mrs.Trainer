import { useState, FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'
import { Link, useNavigate } from 'react-router-dom'
import { UserPlus } from 'lucide-react'

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { register, loading } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    if (!username || !password) {
      setError('Username and password are required')
      return
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }
    const result = await register(username, email, password)
    if (result.success) navigate('/dashboard')
    else setError(result.error || '')
  }

  return (
    <div className="min-h-[70vh] flex items-center justify-center animate-fade-in-up">
      <div className="relative w-full max-w-md">
        <div className="pointer-events-none absolute -top-20 -right-20 w-48 h-48 rounded-full bg-accent-gold/5 blur-[80px]" />
        <div className="pointer-events-none absolute -bottom-20 -left-20 w-48 h-48 rounded-full bg-accent-red/5 blur-[80px]" />

        <div className="relative p-8 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.25)]">
          <div className="text-center mb-6">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-gold/20 to-accent-red/20 flex items-center justify-center mx-auto mb-4">
              <UserPlus className="w-5 h-5 text-accent-gold-soft" />
            </div>
            <h2 className="text-2xl font-black font-display bg-gradient-to-r from-accent-gold to-accent-red bg-clip-text text-transparent">
              Create Account
            </h2>
            <p className="text-text-muted text-sm mt-1">Start your practice journey</p>
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
                placeholder="Choose a username"
                autoComplete="username"
                autoFocus
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1.5 text-text-secondary">Email (optional)</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold/40 focus:border-accent-gold/50 transition-all"
                placeholder="you@example.com"
                autoComplete="email"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1.5 text-text-secondary">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold/40 focus:border-accent-gold/50 transition-all"
                placeholder="Min. 8 characters"
                autoComplete="new-password"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl font-bold text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:shadow-[0_6px_20px_rgba(192,57,43,0.4)] hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <p className="text-center text-text-secondary text-sm mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-accent-gold font-semibold hover:underline transition-all">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
