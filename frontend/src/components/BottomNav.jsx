import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

const ICONS = {
  home:       'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  assessment: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01',
  scan:       'M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z M15 13a3 3 0 11-6 0 3 3 0 016 0z',
  chat:       'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
  simulator:  'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
  about:      'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  contact:    'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
}

export default function BottomNav() {
  const { t } = useTranslation()

  const TABS = [
    { to: '/',           labelKey: 'nav.home',       icon: ICONS.home },
    { to: '/assessment', labelKey: 'nav.assessment', icon: ICONS.assessment },
    { to: '/scan',       labelKey: 'nav.scan',       icon: ICONS.scan },
    { to: '/chat',       labelKey: 'nav.chat',       icon: ICONS.chat },
  ]

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-50 safe-bottom">
      <div className="glass border-t border-white/50 px-2 py-1.5">
        <div className="flex justify-around max-w-lg mx-auto">
          {TABS.map(tab => (
            <NavLink
              key={tab.to}
              to={tab.to}
              end={tab.to === '/'}
              className={({ isActive }) =>
                `flex flex-col items-center gap-0.5 px-4 py-2 rounded-2xl transition-all duration-200 min-w-[64px] ${
                  isActive
                    ? 'bg-olive-100 text-olive-700'
                    : 'text-olive-400 hover:text-olive-600'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <svg className={`w-5 h-5 transition-transform duration-200 ${isActive ? 'scale-110' : ''}`}
                    fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={isActive ? 2.5 : 1.8} d={tab.icon} />
                  </svg>
                  <span className={`text-[10px] font-medium ${isActive ? 'text-olive-700' : ''}`}>
                    {t(tab.labelKey)}
                  </span>
                </>
              )}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  )
}
