import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import client from '../api/client'
import { UserProfile } from '../types/api'
import Button from '../components/Button'
import Card from '../components/Card'
import ErrorState from '../components/ErrorState'

export default function ProfilePage() {
  const { user } = useAuth()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const { data } = await client.get<UserProfile>('/auth/profile/')
        setProfile(data)
      } catch {
        setError('Failed to load profile')
      } finally {
        setLoading(false)
      }
    }
    fetchProfile()
  }, [])

  if (loading) {
    return (
      <div className="animate-fade-in-up max-w-md mx-auto">
        <div className="p-8 bg-bg-surface rounded-2xl animate-pulse" />
      </div>
    )
  }

  if (error) {
    return <ErrorState message={error} onRetry={() => window.location.reload()} />
  }

  const display = profile || user
  const initial = display?.username?.charAt(0)?.toUpperCase() || '?'

  return (
    <div className="animate-fade-in-up space-y-6 max-w-md mx-auto">
      <Card className="p-8 text-center">
        <div className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold text-white mx-auto mb-4"
          style={{ background: 'linear-gradient(135deg, #c0392b, #d4a017)' }}>
          {initial}
        </div>
        <h2 className="font-display font-bold text-xl text-text-primary mb-1">{display?.username}</h2>
        <p className="text-text-muted text-sm mb-6">{display?.email || 'No email set'}</p>

        {profile && (
          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-glass-border">
            <div>
              <div className="font-mono font-bold text-lg text-correct">{profile.questions_solved}</div>
              <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest">Solved</div>
            </div>
            <div>
              <div className="font-mono font-bold text-lg text-accent-gold">{profile.questions_attempted}</div>
              <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest">Attempted</div>
            </div>
            <div>
              <div className="font-mono font-bold text-lg text-accent-red-soft">
                {profile.questions_attempted > 0
                  ? Math.round((profile.questions_solved / profile.questions_attempted) * 100)
                  : 0}%
              </div>
              <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest">Accuracy</div>
            </div>
          </div>
        )}
      </Card>

      <div className="flex justify-center">
        <Button variant="secondary" to="/dashboard">
          View Dashboard
        </Button>
      </div>
    </div>
  )
}
