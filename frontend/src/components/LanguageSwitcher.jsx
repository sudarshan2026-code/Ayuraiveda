import { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'

const LANGUAGES = [
  { code: 'en', label: 'English',  native: 'English',   flag: '🇬🇧' },
  { code: 'hi', label: 'Hindi',    native: 'हिन्दी',    flag: '🇮🇳' },
  { code: 'gu', label: 'Gujarati', native: 'ગુજરાતી',  flag: '🪔' },
]

export default function LanguageSwitcher({ mobile = false }) {
  const { i18n } = useTranslation()
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  const current = LANGUAGES.find(l => l.code === i18n.language) || LANGUAGES[0]

  // Close on outside click
  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const switchLang = (code) => {
    i18n.changeLanguage(code)
    // Update html lang attribute for CSS font stacks
    document.documentElement.lang = code
    setOpen(false)
  }

  // Sync html lang on mount
  useEffect(() => {
    document.documentElement.lang = i18n.language
  }, [i18n.language])

  if (mobile) {
    // Horizontal pill row for mobile bottom sheet or inline use
    return (
      <div className="flex items-center gap-1.5">
        {LANGUAGES.map(l => (
          <button
            key={l.code}
            onClick={() => switchLang(l.code)}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200
              ${i18n.language === l.code
                ? 'bg-olive-600 text-white shadow-soft'
                : 'bg-cream-100 text-olive-600 hover:bg-olive-100'}`}
          >
            <span>{l.flag}</span>
            <span>{l.native}</span>
          </button>
        ))}
      </div>
    )
  }

  return (
    <div ref={ref} className="relative">
      {/* Trigger button */}
      <button
        onClick={() => setOpen(o => !o)}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-sm font-medium transition-all duration-200 border
          ${open
            ? 'bg-olive-50 border-olive-300 text-olive-700'
            : 'bg-white/60 border-cream-200 text-olive-600 hover:bg-olive-50 hover:border-olive-300'}`}
        aria-label="Select language"
        aria-expanded={open}
      >
        <span className="text-base leading-none">🌐</span>
        <span className="hidden sm:inline">{current.native}</span>
        <svg
          className={`w-3.5 h-3.5 text-olive-400 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 top-full mt-2 w-44 glass rounded-2xl shadow-card border border-white/60 overflow-hidden z-[100] animate-dropdown">
          {LANGUAGES.map((l, idx) => (
            <button
              key={l.code}
              onClick={() => switchLang(l.code)}
              className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors duration-150
                ${i18n.language === l.code
                  ? 'bg-olive-50 text-olive-700 font-semibold'
                  : 'text-olive-600 hover:bg-cream-50'}
                ${idx !== LANGUAGES.length - 1 ? 'border-b border-cream-100' : ''}`}
            >
              <span className="text-lg leading-none">{l.flag}</span>
              <div className="text-left">
                <p className="font-medium leading-tight">{l.native}</p>
                <p className="text-[10px] text-olive-400 leading-tight">{l.label}</p>
              </div>
              {i18n.language === l.code && (
                <span className="ml-auto text-olive-500 text-xs">✓</span>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
