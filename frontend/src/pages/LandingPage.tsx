import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const features = [
  {
    title: 'Coding Problems',
    description: 'Hands-on Python challenges with real-time code execution via Monaco Editor. Write, run, and submit solutions instantly.',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
      </svg>
    ),
  },
  {
    title: 'MCQ Practice',
    description: 'Topic-wise multiple-choice questions with instant feedback and detailed explanations for every answer.',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    title: 'Mock Exams',
    description: 'Timed full-length mock exams simulating real assessment conditions. Track your accuracy and score over time.',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    title: 'Progress Dashboard',
    description: 'Visual analytics of your performance — accuracy trends, topic breakdowns, and session history at a glance.',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
      </svg>
    ),
  },
]

const stats = [
  { label: 'Coding Problems', value: '50+' },
  { label: 'MCQ Questions', value: '200+' },
  { label: 'Practice Exams', value: 'Unlimited' },
]

export default function LandingPage() {
  const navigate = useNavigate()
  const { user } = useAuth()

  return (
    <div className="animate-fade-in-up space-y-20 pb-16">
      {/* Hero */}
      <section className="pt-16 md:pt-24 text-center">
        <div className="inline-block px-4 py-1.5 rounded-full bg-bg-surface border border-glass-border text-xs font-mono text-text-muted mb-6">
          Python &bull; Django &bull; OnlineCompiler.io
        </div>
        <h1 className="font-display font-black text-4xl md:text-5xl lg:text-6xl text-text-primary leading-tight mb-5">
          Master Python
          <br />
          <span className="bg-gradient-to-r from-accent-red to-accent-gold bg-clip-text text-transparent">
            One Problem at a Time
          </span>
        </h1>
        <p className="text-text-secondary text-base md:text-lg max-w-lg mx-auto mb-8 leading-relaxed">
          Practice coding problems, tackle multiple-choice questions, and take mock exams — all powered by real code execution.
        </p>
        <div className="flex items-center justify-center gap-3">
          {user ? (
            <button
              onClick={() => navigate('/topics')}
              className="px-7 py-3 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_20px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
            >
              Start Practicing
            </button>
          ) : (
            <>
              <button
                onClick={() => navigate('/register')}
                className="px-7 py-3 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_20px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
              >
                Get Started Free
              </button>
              <button
                onClick={() => navigate('/login')}
                className="px-6 py-3 rounded-xl font-semibold text-sm bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover transition-all duration-150 cursor-pointer"
              >
                Sign In
              </button>
            </>
          )}
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-3 gap-4 md:gap-8 max-w-lg mx-auto">
        {stats.map((s) => (
          <div key={s.label} className="text-center p-4 rounded-xl bg-bg-surface border border-glass-border">
            <p className="font-mono font-bold text-lg md:text-xl text-accent-gold">{s.value}</p>
            <p className="font-mono text-[10px] text-text-muted uppercase tracking-wider mt-1">{s.label}</p>
          </div>
        ))}
      </section>

      {/* Features */}
      <section className="grid md:grid-cols-2 gap-4">
        {features.map((f) => (
          <div
            key={f.title}
            className="p-6 rounded-2xl bg-bg-surface border border-glass-border hover:bg-bg-surface-hover transition-all"
          >
            <div className="w-10 h-10 rounded-lg bg-accent-red/10 flex items-center justify-center text-accent-red mb-4">
              {f.icon}
            </div>
            <h3 className="font-display font-bold text-base text-text-primary mb-2">{f.title}</h3>
            <p className="text-text-secondary text-sm leading-relaxed">{f.description}</p>
          </div>
        ))}
      </section>

      {/* CTA */}
      {!user && (
        <section className="text-center p-8 rounded-2xl bg-bg-surface border border-glass-border">
          <h2 className="font-display font-black text-xl md:text-2xl text-text-primary mb-3">
            Ready to level up?
          </h2>
          <p className="text-text-secondary text-sm mb-6 max-w-md mx-auto">
            Create a free account and start your Python mastery journey today.
          </p>
          <button
            onClick={() => navigate('/register')}
            className="px-7 py-3 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_20px_rgba(192,57,43,0.3)] hover:-translate-y-0.5 transition-all duration-150 cursor-pointer"
          >
            Create Free Account
          </button>
        </section>
      )}
    </div>
  )
}
