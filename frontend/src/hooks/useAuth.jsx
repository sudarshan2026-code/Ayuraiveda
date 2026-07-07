import { createContext, useContext, useState, useEffect } from 'react'
import pb, { authService } from '../services/pocketbase.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    // Support local admin session
    const local = (() => { try { return JSON.parse(localStorage.getItem('ayur_user')) } catch { return null } })()
    if (local?.role === 'admin') return local
    return authService.currentUser
  })
  const [loading, setLoading] = useState(false)
  const [authError, setAuthError] = useState(null)

  // Sync user state whenever PocketBase auth store changes
  useEffect(() => {
    const unsub = pb.authStore.onChange(() => {
      setUser(authService.currentUser)
    })
    return () => unsub()
  }, [])

  const login = async ({ email, password }) => {
    setLoading(true)
    setAuthError(null)
    try {
      const record = await authService.login({ email, password })
      setUser(record)
      return record
    } catch (err) {
      const msg = err?.response?.message || 'Invalid credentials. Please try again.'
      setAuthError(msg)
      throw new Error(msg)
    } finally {
      setLoading(false)
    }
  }

  const register = async ({ name, email, password, role }) => {
    setLoading(true)
    setAuthError(null)
    try {
      const record = await authService.register({ name, email, password, role })
      setUser(authService.currentUser)
      return record
    } catch (err) {
      const msg = err?.response?.message || 'Registration failed. Please try again.'
      setAuthError(msg)
      throw new Error(msg)
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    authService.logout()
    localStorage.removeItem('ayur_user')
    setUser(null)
  }

  const updateProfile = async (updates) => {
    if (!user?.id) return
    try {
      const updated = await authService.updateProfile(user.id, updates)
      setUser(updated)
      return updated
    } catch (err) {
      throw new Error(err?.response?.message || 'Profile update failed.')
    }
  }

  const forgotPassword = async (email) => {
    await authService.forgotPassword(email)
  }

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      authError,
      setAuthError,
      login,
      register,
      logout,
      updateProfile,
      forgotPassword,
      isLoggedIn: !!user,
      isDoctor: user?.role === 'doctor',
      isAdmin: user?.role === 'admin',
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
