import { useState, useRef, useEffect } from 'react'
import { useNotifications } from '../hooks/useNotifications.jsx'

export default function NotificationBell() {
  const [open, setOpen] = useState(false)
  const { notifications, unreadCount, markAllRead } = useNotifications()
  const ref = useRef(null)

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => { setOpen(o => !o); if (!open) markAllRead() }}
        className="relative p-2 rounded-xl hover:bg-cream-100 transition-colors"
        aria-label="Notifications"
      >
        <svg className="w-5 h-5 text-olive-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <>
          {/* Mobile: full-width fixed panel */}
          <div className="fixed inset-x-0 top-14 z-50 px-3 sm:hidden">
            <div className="card shadow-card overflow-hidden">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-olive-800 text-sm">Notifications</h3>
                <button onClick={() => setOpen(false)} className="text-olive-400 hover:text-olive-600 text-lg leading-none">&times;</button>
              </div>
              <div className="space-y-2 max-h-64 overflow-y-auto scrollbar-hide">
                {notifications.length === 0 ? (
                  <p className="text-xs text-olive-400 text-center py-4">No notifications yet</p>
                ) : notifications.map(n => (
                  <div key={n.id} className={`p-3 rounded-2xl ${n.read ? 'bg-cream-50' : 'bg-olive-50 border border-olive-100'}`}>
                    <p className="text-sm font-medium text-olive-800">{n.title}</p>
                    <p className="text-xs text-olive-500 mt-0.5">{n.body}</p>
                    <p className="text-[10px] text-olive-400 mt-1">{n.time}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Desktop: dropdown */}
          <div className="hidden sm:block absolute right-0 top-12 w-80 card shadow-card z-50 overflow-hidden">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-olive-800 text-sm">Notifications</h3>
              <span className="text-xs text-olive-400">All caught up</span>
            </div>
            <div className="space-y-2 max-h-72 overflow-y-auto scrollbar-hide">
              {notifications.length === 0 ? (
                <p className="text-xs text-olive-400 text-center py-4">No notifications yet</p>
              ) : notifications.map(n => (
                <div key={n.id} className={`p-3 rounded-2xl ${n.read ? 'bg-cream-50' : 'bg-olive-50 border border-olive-100'}`}>
                  <p className="text-sm font-medium text-olive-800">{n.title}</p>
                  <p className="text-xs text-olive-500 mt-0.5">{n.body}</p>
                  <p className="text-[10px] text-olive-400 mt-1">{n.time}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
