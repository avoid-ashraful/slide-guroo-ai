import { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Header from './components/Header'

// Page components
import Home from './pages/Home'
import LessonView from './pages/LessonView'
import TopicGenerator from './pages/TopicGenerator'
import Login from './pages/Login'
import Signup from './pages/Signup'
import VerifyEmail from './pages/VerifyEmail'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import Dashboard from './pages/Dashboard'

function App() {
  const [currentLanguage, setCurrentLanguage] = useState('en')

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Header currentLanguage={currentLanguage} setCurrentLanguage={setCurrentLanguage} />

        <main className="container mx-auto px-4 py-8">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/verify-email" element={<VerifyEmail />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />

            {/* Protected routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute requireVerified={true}>
                  <Home currentLanguage={currentLanguage} />
                </ProtectedRoute>
              }
            />
            <Route
              path="/topic"
              element={
                <ProtectedRoute requireVerified={true}>
                  <TopicGenerator currentLanguage={currentLanguage} />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lesson/:lessonId"
              element={
                <ProtectedRoute requireVerified={true}>
                  <LessonView currentLanguage={currentLanguage} />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <footer className="bg-white border-t mt-16 py-8">
          <div className="container mx-auto px-4 text-center text-gray-600">
            <p className="mb-2">SlideGuroo - AI-Powered Student Learning Assistant</p>
            <p className="text-sm">Transforming education for students (Class 6-12 & University)</p>
          </div>
        </footer>
      </div>
    </AuthProvider>
  )
}

export default App
