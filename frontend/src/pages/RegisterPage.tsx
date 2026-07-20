import { useState, FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'
import { Link, useNavigate } from 'react-router-dom'

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
      <div className="w-full max-w-md p-8 bg-bg-surface backdrop-blur-[14px] border border-glass-border rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.25)]">
        <h2 className="text-2xl font-black text-center mb-6 font-display"
          style={{
            background: 'linear-gradient(135deg, #c0392b, #d4a017)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>
          Create Account
        </h2>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-wrong-bg border border-wrong-border text-wrong text-sm font-mono" role="alert">
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
              className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold focus:border-transparent transition-all"
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
              className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold focus:border-transparent transition-all"
              autoComplete="email"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold mb-1.5 text-text-secondary">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-bg-surface-hover border border-glass-border text-text-primary font-display text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold focus:border-transparent transition-all"
              autoComplete="new-password"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl font-bold text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_16px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <p className="text-center text-text-secondary text-sm mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-accent-gold font-semibold hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
