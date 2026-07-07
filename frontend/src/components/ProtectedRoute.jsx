import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'

/**
 * Wraps a route and redirects to /login if not authenticated.
 * Optionally restricts to specific roles: <ProtectedRoute roles={['doctor']} />
 */
export default function ProtectedRoute({ children, roles }) {
  const { user, isLoggedIn } = useAuth()
  const location = useLocation()

  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (roles && !roles.includes(user?.role)) {
    return <Navigate to="/" replace />
  }

  return children
}
