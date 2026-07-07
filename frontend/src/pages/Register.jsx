import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../hooks/useAuth.jsx'

export default function Register() {
  const { t } = useTranslation()
  const [role, setRole] = useState('user')
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '' })
  const { register, loading, authError, setAuthError } = useAuth()
  const navigate = useNavigate()

  const ROLES = [
    { key: 'user',   labelKey: 'auth.role_user',   icon: '👤' },
    { key: 'doctor', labelKey: 'auth.role_doctor', icon: '🩺' },
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.confirm) {
      setAuthError(t('auth.error_password_match'))
      return
    }
    setAuthError(null)
    try {
      await register({ name: form.name, email: form.email, password: form.password, role })
      navigate('/')
    } catch { /* error shown via authError */ }
  }

  const field = (key, label, type = 'text', placeholder = '') => (
    <div>
      <label className="block text-sm font-medium text-olive-700 mb-1.5">{label}</label>
      <input type={type} value={form[key]}
        onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
        placeholder={placeholder} className="input-field" required />
    </div>
  )

  return (
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
          <h1 className="font-serif text-2xl font-bold text-olive-800">{t('auth.create_account')}</h1>
          <p className="text-olive-500 text-sm mt-1">{t('auth.register_subtitle')}</p>
        </div>

        <div className="card shadow-card">
          {/* Role selector */}
          <div className="flex gap-2 mb-6 p-1 bg-cream-100 rounded-2xl">
            {ROLES.map(r => (
              <button key={r.key} onClick={() => setRole(r.key)}
                className={`flex-1 flex flex-col items-center py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  role === r.key ? 'bg-white text-olive-700 shadow-soft' : 'text-olive-500 hover:text-olive-700'}`}>
                <span className="text-lg mb-0.5">{r.icon}</span>
                {t(r.labelKey)}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {field('name',    t('auth.full_name'),         'text',     t('auth.placeholder_name'))}
            {field('email',   t('auth.email'),             'email',    t('auth.placeholder_email'))}
            {field('password',t('auth.password'),          'password', t('auth.placeholder_password'))}
            {field('confirm', t('auth.confirm_password'),  'password', t('auth.placeholder_password'))}

            {authError && (
              <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-4 py-3 rounded-2xl">{authError}</div>
            )}

            <button type="submit" disabled={loading} className="btn-primary w-full py-3.5 mt-2">
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                  {t('auth.creating')}
                </span>
              ) : t('auth.create_btn')}
            </button>
          </form>

          <p className="text-center text-sm text-olive-500 mt-5">
            {t('auth.have_account')}{' '}
            <Link to="/login" className="text-olive-700 font-semibold hover:underline">{t('auth.sign_in_link')}</Link>
          </p>
        </div>
        <p className="text-center text-xs text-olive-400 mt-6">{t('auth.register_privacy')}</p>
      </div>
    </div>
  )
}
