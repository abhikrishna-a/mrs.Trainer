import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Code2, CheckCircle2, Clock, BarChart3, ArrowRight, Sparkles, Layers, Zap } from 'lucide-react'

const features = [
  {
    title: 'Coding Problems',
    description: 'Hands-on Python challenges with real-time code execution. Write, run, and submit solutions in a full Monaco editor.',
    icon: Code2,
  },
  {
    title: 'MCQ Practice',
    description: 'Topic-wise multiple-choice questions with instant feedback and detailed trap-based explanations for every answer.',
    icon: CheckCircle2,
  },
  {
    title: 'Mock Exams',
    description: 'Timed full-length exams simulating real assessments. Track accuracy and score with detailed post-exam breakdowns.',
    icon: Clock,
  },
  {
    title: 'Progress Analytics',
    description: 'Visual performance dashboard — accuracy trends, topic-wise breakdowns, and session history at a glance.',
    icon: BarChart3,
  },
]

const stats = [
  { label: 'Coding Problems', value: '50+' },
  { label: 'MCQ Questions', value: '200+' },
  { label: 'Topics Covered', value: '20' },
  { label: 'Practice Exams', value: '∞' },
]

export default function LandingPage() {
  const navigate = useNavigate()
  const { user } = useAuth()

  return (
    <div className="animate-fade-in-up">
      {/* Hero */}
      <section className="relative pt-20 md:pt-28 pb-16 text-center overflow-hidden">
        {/* Animated mesh background */}
        <div className="pointer-events-none absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-accent-red/5 blur-[120px] animate-pulse" style={{ animationDuration: '8s' }} />
          <div className="absolute top-1/3 left-1/2 -translate-x-1/2 translate-y-20 w-[400px] h-[400px] rounded-full bg-accent-gold/5 blur-[100px] animate-pulse" style={{ animationDuration: '6s' }} />
        </div>

        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-accent-gold/10 border border-accent-gold/20 text-xs font-mono text-accent-gold-soft mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          Python practice platform — built for placements
        </div>

        <h1 className="font-display font-black text-4xl md:text-5xl lg:text-6xl text-text-primary leading-[1.1] mb-5">
          Master Python
          <br />
          <span className="bg-gradient-to-r from-accent-red via-accent-gold to-accent-gold-soft bg-clip-text text-transparent">
            One Problem at a Time
          </span>
        </h1>

        <p className="text-text-secondary text-base md:text-lg max-w-xl mx-auto mb-8 leading-relaxed">
          Practice coding problems, tackle multiple-choice questions, and take timed mock exams — all powered by real code execution with instant feedback.
        </p>

        <div className="flex items-center justify-center gap-3 flex-wrap">
          {user ? (
            <button
              onClick={() => navigate('/topics')}
              className="group px-7 py-3 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_24px_rgba(192,57,43,0.35)] hover:shadow-[0_8px_32px_rgba(192,57,43,0.45)] hover:-translate-y-0.5 transition-all duration-300 cursor-pointer inline-flex items-center gap-2"
            >
              Start Practicing
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </button>
          ) : (
            <>
              <button
                onClick={() => navigate('/register')}
                className="group px-7 py-3 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_24px_rgba(192,57,43,0.35)] hover:shadow-[0_8px_32px_rgba(192,57,43,0.45)] hover:-translate-y-0.5 transition-all duration-300 cursor-pointer inline-flex items-center gap-2"
              >
                Get Started Free
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </button>
              <button
                onClick={() => navigate('/login')}
                className="px-6 py-3 rounded-xl font-semibold text-sm bg-bg-surface border border-glass-border text-text-primary hover:bg-bg-surface-hover hover:-translate-y-0.5 transition-all duration-300 cursor-pointer"
              >
                Sign In
              </button>
            </>
          )}
        </div>
      </section>

      {/* Stats bar */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 mb-20">
        {stats.map((s) => (
          <div key={s.label} className="text-center p-4 md:p-5 rounded-2xl bg-bg-surface border border-glass-border backdrop-blur-[14px] hover:bg-bg-surface-hover transition-all duration-300">
            <p className="font-display font-bold text-xl md:text-2xl text-accent-gold">{s.value}</p>
            <p className="font-mono text-[10px] text-text-muted uppercase tracking-wider mt-1.5">{s.label}</p>
          </div>
        ))}
      </section>

      {/* Features grid */}
      <section className="mb-20">
        <div className="text-center mb-10">
          <h2 className="font-display font-black text-2xl md:text-3xl text-text-primary mb-3">
            Everything you need to crack the interview
          </h2>
          <p className="text-text-secondary text-sm md:text-base max-w-lg mx-auto">
            From fundamentals to advanced topics, structured practice that builds real confidence.
          </p>
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          {features.map((f, i) => (
            <div
              key={f.title}
              className="group p-6 rounded-2xl bg-bg-surface border border-glass-border backdrop-blur-[14px] hover:bg-bg-surface-hover hover:border-accent-gold/20 transition-all duration-300 hover:-translate-y-0.5"
              style={{ animationDelay: `${i * 80}ms` }}
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-red/20 to-accent-gold/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <f.icon className="w-5 h-5 text-accent-gold-soft" />
              </div>
              <h3 className="font-display font-bold text-base text-text-primary mb-2">{f.title}</h3>
              <p className="text-text-secondary text-sm leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mb-20">
        <div className="text-center mb-10">
          <h2 className="font-display font-black text-2xl md:text-3xl text-text-primary mb-3">
            How it works
          </h2>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { step: '01', icon: Layers, title: 'Pick a Topic', desc: 'Choose from 20 topics across Quantitative Aptitude, Logical Reasoning, DSA, and Python.' },
            { step: '02', icon: Zap, title: 'Practice & Learn', desc: 'Solve coding problems with real-time execution or answer MCQs with detailed explanations.' },
            { step: '03', icon: BarChart3, title: 'Track Progress', desc: 'Monitor accuracy trends, topic mastery, and take timed mock exams to simulate the real thing.' },
          ].map(({ step, icon: Icon, title, desc }) => (
            <div key={step} className="p-6 rounded-2xl bg-bg-surface border border-glass-border backdrop-blur-[14px] text-center">
              <div className="w-12 h-12 rounded-xl bg-accent-gold/10 flex items-center justify-center mx-auto mb-4">
                <Icon className="w-6 h-6 text-accent-gold-soft" />
              </div>
              <p className="font-mono text-xs font-bold text-accent-gold mb-2">{step}</p>
              <h3 className="font-display font-bold text-base text-text-primary mb-2">{title}</h3>
              <p className="text-text-secondary text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      {!user && (
        <section className="relative overflow-hidden rounded-3xl border border-glass-border p-8 md:p-14 text-center mb-8"
          style={{ background: 'linear-gradient(135deg, rgba(192,57,43,0.08), rgba(212,160,23,0.08))' }}>
          <div className="pointer-events-none absolute inset-0 -z-10">
            <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full bg-accent-red/5 blur-[80px]" />
            <div className="absolute -bottom-20 -left-20 w-60 h-60 rounded-full bg-accent-gold/5 blur-[80px]" />
          </div>
          <h2 className="font-display font-black text-2xl md:text-3xl text-text-primary mb-3">
            Ready to level up?
          </h2>
          <p className="text-text-secondary text-sm md:text-base max-w-md mx-auto mb-6">
            Create a free account and start your Python mastery journey today. No credit card required.
          </p>
          <button
            onClick={() => navigate('/register')}
            className="group px-8 py-3.5 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-accent-red to-accent-gold shadow-[0_4px_24px_rgba(192,57,43,0.35)] hover:shadow-[0_8px_32px_rgba(192,57,43,0.45)] hover:-translate-y-0.5 transition-all duration-300 cursor-pointer inline-flex items-center gap-2"
          >
            Create Free Account
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </section>
      )}

      {/* Footer */}
      <footer className="text-center py-8 border-t border-glass-border">
        <p className="font-mono text-[10px] text-text-muted">
          &copy; {new Date().getFullYear()} AlgoForge. Built for practice.
        </p>
      </footer>
    </div>
  )
}
