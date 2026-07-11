import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Home from './pages/Home'
import Assessment from './pages/Assessment'
import VisualScan from './pages/VisualScan'
import Chat from './pages/Chat'
import About from './pages/About'
import Contact from './pages/Contact'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import AdminPanel from './pages/AdminPanel'
import ProtectedRoute from './components/ProtectedRoute'
import { AuthProvider } from './hooks/useAuth.jsx'
import { NotificationProvider } from './hooks/useNotifications.jsx'

export default function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        <BrowserRouter>
          <Routes>
            {/* ── Main app layout (Ayurveda pages) ── */}
            <Route element={<MainLayout />}>
              <Route index element={<Home />} />
              <Route path="assessment" element={<Assessment />} />
              <Route path="scan" element={<VisualScan />} />
              <Route path="chat" element={<Chat />} />
              <Route path="about" element={<About />} />
              <Route path="contact" element={<Contact />} />
              <Route path="profile" element={
                <ProtectedRoute><Profile /></ProtectedRoute>
              } />
            </Route>

            {/* ── Auth ── */}
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="admin" element={<AdminPanel />} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </NotificationProvider>
    </AuthProvider>
  )
}
