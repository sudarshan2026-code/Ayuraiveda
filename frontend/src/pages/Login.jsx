import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../hooks/useAuth.jsx'

export default function Login() {
  const { t } = useTranslation()
  const [role, setRole] = useState('user')
  const [form, setForm] = useState({ email: '', password: '' })
  const [forgotMode, setForgotMode] = useState(false)
  const [forgotSent, setForgotSent] = useState(false)
  const [forgotEmail, setForgotEmail] = useState('')
  const { login, forgotPassword, loading, authError, setAuthError } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname || '/'

  const ROLES = [
    { key: 'user',   labelKey: 'auth.role_user',   icon: '👤', descKey: 'auth.role_user_desc' },
    { key: 'doctor', labelKey: 'auth.role_doctor', icon: '🩺', descKey: 'auth.role_doctor_desc' },
  ]
  const currentRole = ROLES.find(r => r.key === role)

  const ADMIN_EMAIL = 'ayuraiveda@gmail.com'
  const ADMIN_PASSWORD = 'Zala@0007'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setAuthError(null)
    // Admin shortcut — bypass PocketBase, use hardcoded credentials
    if (role === 'doctor' && form.email === ADMIN_EMAIL && form.password === ADMIN_PASSWORD) {
      // Store a local admin session
      const adminUser = { id: 'admin', name: 'Admin', email: ADMIN_EMAIL, role: 'admin' }
      localStorage.setItem('ayur_user', JSON.stringify(adminUser))
      window.location.href = '/admin'
      return
    }
    try {
      await login({ email: form.email, password: form.password })
      navigate(from, { replace: true })
    } catch { /* error shown via authError */ }
  }

  const handleForgot = async (e) => {
    e.preventDefault()
    try {
      await forgotPassword(forgotEmail)
      setForgotSent(true)
    } catch {
      setAuthError('Could not send reset email. Please check the address.')
    }
  }

  // ── Forgot password view ──
  if (forgotMode) return (
    <div className="min-h-screen gradient-hero flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-olive-500 hover:text-olive-700 mb-6 transition-colors">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </Link>
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 rounded-2xl gradient-olive flex items-center justify-center text-white font-bold text-lg shadow-soft">ॐ</div>
            <span className="font-serif font-bold text-olive-800 text-xl">AyurAI<span className="text-olive-500">Veda</span></span>
          </Link>
          <h1 className="font-serif text-2xl font-bold text-olive-800">Reset Password</h1>
          <p className="text-olive-500 text-sm mt-1">We'll send a reset link to your email</p>
        </div>
        <div className="card shadow-card">
          {forgotSent ? (
            <div className="text-center py-6">
              <span className="text-4xl">📧</span>
              <h3 className="font-semibold text-olive-800 mt-3 mb-2">Check your inbox</h3>
              <p className="text-sm text-olive-500 mb-5">Reset link sent to <strong>{forgotEmail}</strong></p>
              <button onClick={() => { setForgotMode(false); setForgotSent(false) }} className="btn-primary w-full py-3">
                Back to Login
              </button>
            </div>
          ) : (
            <form onSubmit={handleForgot} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-olive-700 mb-1.5">Email Address</label>
                <input type="email" value={forgotEmail} onChange={e => setForgotEmail(e.target.value)}
                  placeholder="you@example.com" className="input-field" required />
              </div>
              {authError && <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-4 py-3 rounded-2xl">{authError}</div>}
              <button type="submit" disabled={loading} className="btn-primary w-full py-3.5">
                {loading ? <Spinner text="Sending…" /> : 'Send Reset Link →'}
              </button>
              <button type="button" onClick={() => setForgotMode(false)} className="w-full text-sm text-olive-500 hover:text-olive-700 mt-1">
                ← Back to Login
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  )

  // ── Main login view ──
  return (
    <div className="min-h-screen gradient-hero flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Back to Home */}
        <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-olive-500 hover:text-olive-700 mb-6 transition-colors">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </Link>
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 rounded-2xl gradient-olive flex items-center justify-center text-white font-bold text-lg shadow-soft">ॐ</div>
            <span className="font-serif font-bold text-olive-800 text-xl">AyurAI<span className="text-olive-500">Veda</span></span>
          </Link>
          <h1 className="font-serif text-2xl font-bold text-olive-800">{t('auth.welcome_back')}</h1>
          <p className="text-olive-500 text-sm mt-1">{t('auth.sign_in_subtitle')}</p>
        </div>

        <div className="card shadow-card">
          {/* Role tabs */}
          <div className="flex gap-2 mb-6 p-1 bg-cream-100 rounded-2xl">
            {ROLES.map(r => (
              <button key={r.key} onClick={() => setRole(r.key)}
                className={`flex-1 flex flex-col items-center py-2.5 px-2 rounded-xl text-xs font-medium transition-all duration-200 ${
                  role === r.key ? 'bg-white text-olive-700 shadow-soft' : 'text-olive-500 hover:text-olive-700'}`}>
                <span className="text-lg mb-0.5">{r.icon}</span>
                {t(r.labelKey)}
              </button>
            ))}
          </div>
          <p className="text-xs text-olive-400 text-center mb-5">{currentRole && t(currentRole.descKey)}</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-olive-700 mb-1.5">{t('auth.email')}</label>
              <input type="email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
                placeholder={t('auth.placeholder_email')} className="input-field" required />
            </div>
            <div>
              <div className="flex justify-between mb-1.5">
                <label className="text-sm font-medium text-olive-700">{t('auth.password')}</label>
                <button type="button" onClick={() => setForgotMode(true)}
                  className="text-xs text-olive-500 hover:text-olive-700">{t('auth.forgot_password')}</button>
              </div>
              <input type="password" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
                placeholder={t('auth.placeholder_password')} className="input-field" required />
            </div>

            {authError && <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-4 py-3 rounded-2xl">{authError}</div>}

            <button type="submit" disabled={loading} className="btn-primary w-full py-3.5 mt-2">
              {loading ? <Spinner text={t('auth.signing_in')} /> : t('auth.sign_in_btn', { role: currentRole ? t(currentRole.labelKey) : '' })}
            </button>
          </form>

          <p className="text-center text-sm text-olive-500 mt-5">
            {t('auth.no_account')}{' '}
            <Link to="/register" className="text-olive-700 font-semibold hover:underline">{t('auth.create_link')}</Link>
          </p>
        </div>
        <p className="text-center text-xs text-olive-400 mt-6">{t('auth.privacy_note')}</p>
      </div>
    </div>
  )
}

function Spinner({ text }) {
  return (
    <span className="flex items-center justify-center gap-2">
      <span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
      {text}
    </span>
  )
}
