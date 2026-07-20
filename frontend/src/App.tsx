import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { ProblemProvider } from './context/ProblemContext'
import { ExamProvider } from './context/ExamContext'
import ErrorBoundary from './components/ErrorBoundary'
import ProtectedRoute from './components/ProtectedRoute'
import Header from './components/Header'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import TopicsPage from './pages/TopicsPage'
import ProblemsPage from './pages/ProblemsPage'
import ProblemDetailPage from './pages/ProblemDetailPage'
import ExamSelectPage from './pages/ExamSelectPage'
import ExamPage from './pages/ExamPage'
import ExamResultsPage from './pages/ExamResultsPage'
import ExamHistoryPage from './pages/ExamHistoryPage'
import DashboardPage from './pages/DashboardPage'
import ProfilePage from './pages/ProfilePage'

function ProblemDetailWrapper() {
  return (
    <ProblemProvider>
      <ProblemDetailPage />
    </ProblemProvider>
  )
}

function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return <ProtectedRoute>{children}</ProtectedRoute>
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <ExamProvider>
          <BrowserRouter>
            <ErrorBoundary>
              <div className="min-h-screen bg-bg-primary text-text-primary font-display">
                <div className="max-w-[1080px] mx-auto px-4 md:px-6 pb-16">
                  <Header />
                  <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/topics" element={<TopicsPage />} />
                    <Route path="/problems" element={<ProblemsPage />} />
                    <Route path="/problems/:slug" element={<ProblemDetailWrapper />} />
                    <Route path="/exams" element={<ProtectedLayout><ExamSelectPage /></ProtectedLayout>} />
                    <Route path="/exam/:examId" element={<ProtectedLayout><ExamPage /></ProtectedLayout>} />
                    <Route path="/exam/:examId/results" element={<ProtectedLayout><ExamResultsPage /></ProtectedLayout>} />
                    <Route path="/exams/history" element={<ProtectedLayout><ExamHistoryPage /></ProtectedLayout>} />
                    <Route path="/dashboard" element={<ProtectedLayout><DashboardPage /></ProtectedLayout>} />
                    <Route path="/profile" element={<ProtectedLayout><ProfilePage /></ProtectedLayout>} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </div>
              </div>
            </ErrorBoundary>
          </BrowserRouter>
        </ExamProvider>
      </AuthProvider>
    </ThemeProvider>
  )
}
