import { NavLink, Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import NotificationBell from './NotificationBell'
import LanguageSwitcher from './LanguageSwitcher'
import { useAuth } from '../hooks/useAuth.jsx'
import { Avatar } from '../pages/Profile.jsx'

export default function Navbar() {
  const { user } = useAuth()
  const { t } = useTranslation()
  const navigate = useNavigate()

  const NAV = [
    { to: '/',           label: t('nav.home') },
    { to: '/assessment', label: t('nav.assessment') },
    { to: '/scan',       label: t('nav.scan') },
    { to: '/chat',       label: t('nav.chat') },
    { to: '/about',      label: t('nav.about') },
    { to: '/contact',    label: t('nav.contact') },
  ]

  const linkClass = ({ isActive }) =>
    `text-sm font-medium transition-colors duration-200 ${
      isActive ? 'text-olive-600' : 'text-olive-700 hover:text-olive-500'
    }`

  return (
    <header className="sticky top-0 z-50 safe-top">
      <nav className="glass border-b border-white/50 px-4 lg:px-8">
        <div className="max-w-6xl mx-auto flex items-center justify-between h-14 md:h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 shrink-0">
            <div className="w-8 h-8 rounded-xl gradient-olive flex items-center justify-center text-white text-sm font-bold shadow-soft">
              ॐ
            </div>
            <span className="font-serif font-bold text-olive-800 text-lg leading-tight">
              AyurAI<span className="text-olive-500">Veda</span>
            </span>
          </Link>

          {/* Desktop nav — only on large screens */}
          <div className="hidden lg:flex items-center gap-7">
            {NAV.map(n => (
              <NavLink key={n.to} to={n.to} end={n.to === '/'} className={linkClass}>
                {n.label}
              </NavLink>
            ))}
          </div>

          {/* Right actions */}
          <div className="flex items-center gap-2">
            <LanguageSwitcher />
            <NotificationBell />
            {user ? (
              <button
                onClick={() => navigate('/profile')}
                className="flex items-center gap-2 rounded-full focus:outline-none focus:ring-2 focus:ring-olive-400 focus:ring-offset-2"
                aria-label="Profile"
              >
                <Avatar user={user} size="sm" />
              </button>
            ) : (
              <Link to="/login" className="btn-primary text-sm px-4 py-2">
                {t('nav.login')}
              </Link>
            )}
          </div>
        </div>
      </nav>
    </header>
  )
}
