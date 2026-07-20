import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import ProtectedRoute from '../components/ProtectedRoute'

const mockUser = { id: 1, username: 'testuser', email: 'test@test.com' }

vi.mock('../context/AuthContext', () => ({
  useAuth: vi.fn(),
}))

import { useAuth } from '../context/AuthContext'

function ProtectedPage() {
  return <div data-testid="protected-content">Secret Dashboard</div>
}

function LoginPage() {
  return <div data-testid="login-page">Login</div>
}

function renderRoute(user: typeof mockUser | null) {
  vi.mocked(useAuth).mockReturnValue({
    user,
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
    loading: false,
  })

  return render(
    <MemoryRouter initialEntries={['/dashboard']}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={<ProtectedRoute><ProtectedPage /></ProtectedRoute>}
        />
      </Routes>
    </MemoryRouter>
  )
}

describe('ProtectedRoute', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders children when user is authenticated', () => {
    renderRoute(mockUser)
    expect(screen.getByTestId('protected-content')).toBeInTheDocument()
    expect(screen.queryByTestId('login-page')).not.toBeInTheDocument()
  })

  it('redirects to /login when user is not authenticated', () => {
    renderRoute(null)
    expect(screen.getByTestId('login-page')).toBeInTheDocument()
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument()
  })
})
