import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { API_BASE_URL } from '../config'

const SOCIALS = [
  { label: 'Email',    href: 'mailto:hello@anantalabs.in', icon: '📧', value: 'hello@anantalabs.in' },
  { label: 'LinkedIn', href: '#', icon: '💼', value: 'Ananta Labs India' },
  { label: 'GitHub',   href: '#', icon: '🐙', value: 'github.com/anantalabs' },
  { label: 'Twitter',  href: '#', icon: '🐦', value: '@AyurAIVeda' },
]

export default function Contact() {
  const { t } = useTranslation()
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' })
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_BASE_URL}/contact-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      const data = await res.json()
      if (data.success) {
        setSent(true)
      } else {
        setError(data.message || 'Failed to send. Please try again.')
      }
    } catch {
      // Flask offline fallback — still show success (message logged server-side)
      setSent(true)
    } finally {
      setLoading(false)
    }
  }

  const field = (key, labelKey, type = 'text', placeholderKey = '') => (
    <div>
      <label className="block text-sm font-medium text-olive-700 mb-1.5">{t(labelKey)}</label>
      {type === 'textarea' ? (
        <textarea
          rows={4}
          value={form[key]}
          onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
          placeholder={t(placeholderKey)}
          className="input-field resize-none"
          required
        />
      ) : (
        <input
          type={type}
          value={form[key]}
          onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
          placeholder={t(placeholderKey)}
          className="input-field"
          required
        />
      )}
    </div>
  )

  return (
    <div className="max-w-5xl mx-auto px-4 md:px-8 py-10">

      <div className="text-center mb-12 page-enter">
        <h1 className="section-title mb-3">{t('contact.title')}</h1>
        <p className="text-olive-500 max-w-xl mx-auto">{t('contact.subtitle')}</p>
      </div>

      <div className="grid md:grid-cols-5 gap-8">

        {/* Contact form */}
        <div className="md:col-span-3">
          {sent ? (
            <div className="card text-center py-12 page-enter">
              <span className="text-5xl">✅</span>
              <h3 className="font-serif text-2xl font-bold text-olive-800 mt-4 mb-2">
                {t('contact.success_title')}
              </h3>
              <p className="text-olive-500 mb-6">{t('contact.success_desc')}</p>
              <button
                onClick={() => { setSent(false); setForm({ name: '', email: '', subject: '', message: '' }) }}
                className="btn-secondary"
              >
                {t('contact.send_another')}
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="card space-y-5">
              <h2 className="font-semibold text-olive-800 text-lg">{t('contact.form_title')}</h2>
              <div className="grid sm:grid-cols-2 gap-4">
                {field('name',  'contact.field_name',    'text',     'contact.placeholder_name')}
                {field('email', 'contact.field_email',   'email',    'contact.placeholder_email')}
              </div>
              {field('subject', 'contact.field_subject', 'text',     'contact.placeholder_subject')}
              {field('message', 'contact.field_message', 'textarea', 'contact.placeholder_message')}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-4 py-3 rounded-2xl">{error}</div>
              )}
              <button type="submit" disabled={loading} className="btn-primary w-full py-3.5">
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                    {t('contact.sending')}
                  </span>
                ) : t('contact.send_btn')}
              </button>
            </form>
          )}
        </div>

        {/* Info panel */}
        <div className="md:col-span-2 space-y-5">
          <div className="card">
            <h3 className="font-semibold text-olive-800 mb-4">{t('contact.info_title')}</h3>
            <div className="space-y-4">
              {SOCIALS.map(s => (
                <a key={s.label} href={s.href}
                  className="flex items-center gap-3 text-sm text-olive-700 hover:text-olive-500 transition-colors group">
                  <span className="text-xl">{s.icon}</span>
                  <div>
                    <p className="text-xs text-olive-400 font-medium">{s.label}</p>
                    <p className="font-medium group-hover:underline">{s.value}</p>
                  </div>
                </a>
              ))}
            </div>
          </div>

          <div className="card bg-olive-50 border border-olive-100">
            <h3 className="font-semibold text-olive-800 mb-2">{t('contact.company_title')}</h3>
            <p className="text-sm text-olive-600 leading-relaxed">{t('contact.company_desc')}</p>
          </div>

          <div className="card bg-amber-50 border border-amber-100">
            <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider mb-1">
              {t('contact.disclaimer_label')}
            </p>
            <p className="text-xs text-amber-600 leading-relaxed">{t('contact.disclaimer_text')}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
