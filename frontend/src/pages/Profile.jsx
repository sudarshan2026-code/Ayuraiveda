import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'
import { doctorService, assessmentService } from '../services/pocketbase.js'
import { DOSHAS, RISK_COLORS } from '../utils/doshaUtils.js'
import DoshaCard from '../components/DoshaCard.jsx'
import { printReport } from '../utils/printReport.js'

// ── Field definitions ────────────────────────────────────────────────────────
const USER_FIELDS = [
  { key: 'name',        label: 'Full Name',      type: 'text',     placeholder: 'Your full name' },
  { key: 'email',       label: 'Email',          type: 'email',    placeholder: 'you@example.com' },
  { key: 'age',         label: 'Age',            type: 'number',   placeholder: 'Your age' },
  { key: 'gender',      label: 'Gender',         type: 'select',   options: ['Male', 'Female', 'Other'] },
  { key: 'city',        label: 'City',           type: 'text',     placeholder: 'Your city' },
  { key: 'blood_group', label: 'Blood Group',    type: 'select',   options: ['A+','A-','B+','B-','AB+','AB-','O+','O-'] },
  { key: 'phone',       label: 'Phone Number',   type: 'tel',      placeholder: '+91 XXXXX XXXXX' },
  { key: 'bio',         label: 'About Me',       type: 'textarea', placeholder: 'A short bio...' },
]

const DOCTOR_FIELDS = [
  { key: 'name',           label: 'Full Name',           type: 'text',     placeholder: 'Dr. Full Name' },
  { key: 'email',          label: 'Email',               type: 'email',    placeholder: 'doctor@example.com' },
  { key: 'phone',          label: 'Phone Number',        type: 'tel',      placeholder: '+91 XXXXX XXXXX' },
  { key: 'qualification',  label: 'Qualification',       type: 'text',     placeholder: 'e.g. BAMS, MD (Ayurveda)' },
  { key: 'specialization', label: 'Specialization',      type: 'text',     placeholder: 'e.g. Panchakarma' },
  { key: 'experience',     label: 'Years of Experience', type: 'number',   placeholder: 'e.g. 10' },
  { key: 'hospital',       label: 'Hospital / Clinic',   type: 'text',     placeholder: 'Clinic or hospital name' },
  { key: 'city',           label: 'City',                type: 'text',     placeholder: 'Your city' },
  { key: 'reg_number',     label: 'Registration Number', type: 'text',     placeholder: 'Medical council reg. no.' },
  { key: 'bio',            label: 'Professional Bio',    type: 'textarea', placeholder: 'Brief professional summary...' },
]

// ── Avatar ───────────────────────────────────────────────────────────────────
function Avatar({ user, size = 'lg' }) {
  const initials = (user?.name || 'U').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
  const isDoctor = user?.role === 'doctor'
  const sz = size === 'lg' ? 'w-20 h-20 text-2xl' : size === 'md' ? 'w-12 h-12 text-base' : 'w-9 h-9 text-sm'
  return (
    <div className={`${sz} rounded-full flex items-center justify-center font-bold text-white shadow-soft shrink-0
      ${isDoctor ? 'bg-gradient-to-br from-blue-500 to-blue-700' : 'bg-gradient-to-br from-olive-500 to-olive-700'}`}>
      {initials}
    </div>
  )
}
export { Avatar }

// ── Report Card ──────────────────────────────────────────────────────────────
function ReportCard({ report, index }) {
  const [expanded, setExpanded] = useState(false)
  const result = report.result || {}
  const dom = result.dominant?.split('-')[0].toLowerCase() || 'vata'
  const doshaInfo = DOSHAS[dom] || DOSHAS.vata
  const riskClass = RISK_COLORS[result.risk] || RISK_COLORS.Low
  const date = new Date(report.date || report.created)
  const dateStr = isNaN(date) ? 'Unknown date' : date.toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })

  return (
    <div className="card border border-cream-200 overflow-hidden">
      {/* Header row */}
      <button
        onClick={() => setExpanded(e => !e)}
        className="w-full flex items-center gap-4 text-left"
      >
        <div className="w-10 h-10 rounded-2xl bg-olive-50 flex items-center justify-center text-xl shrink-0">
          {doshaInfo.emoji}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold text-olive-800 text-sm">
              {result.dominant || 'Unknown'} Prakriti
            </span>
            <span className={`badge text-xs px-2 py-0.5 border ${riskClass}`}>
              {result.risk || '—'} Risk
            </span>
          </div>
          <p className="text-xs text-olive-400 mt-0.5">{dateStr}</p>
        </div>
        <span className={`text-olive-400 text-lg transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}>
          ⌄
        </span>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="mt-4 pt-4 border-t border-cream-100 space-y-4 page-enter">

          {/* Dosha bars */}
          <div className="space-y-2">
            {['vata', 'pitta', 'kapha'].map(d => (
              <DoshaCard key={d} type={d} score={result.scores?.[d] ?? 0} showBar />
            ))}
          </div>

          {/* Agni / Ama / Vikriti */}
          {(result.agni_state || result.ama_status || result.vikriti) && (
            <div className="grid grid-cols-3 gap-3 text-center">
              {[
                { label: 'Agni',    val: result.agni_state },
                { label: 'Ama',     val: result.ama_status },
                { label: 'Vikriti', val: result.vikriti },
              ].filter(i => i.val).map(item => (
                <div key={item.label} className="bg-olive-50 rounded-2xl p-3">
                  <p className="text-xs text-olive-400 uppercase tracking-wider">{item.label}</p>
                  <p className="text-sm font-semibold text-olive-800 mt-1">{item.val}</p>
                </div>
              ))}
            </div>
          )}

          {/* Reasoning */}
          {result.justification && (
            <div className="bg-olive-50 rounded-2xl p-4">
              <p className="text-xs font-semibold text-olive-500 uppercase tracking-wider mb-1">🔬 Clinical Reasoning</p>
              <p className="text-sm text-olive-700 leading-relaxed">{result.justification}</p>
            </div>
          )}

          {/* Recommendations */}
          {result.recommendations?.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-olive-500 uppercase tracking-wider mb-2">🌱 Recommendations</p>
              <ul className="space-y-1">
                {result.recommendations.map((r, i) => (
                  <li key={i} className="flex gap-2 text-sm text-olive-700">
                    <span className="text-olive-400 shrink-0">•</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Diet */}
          {result.diet_suggestions && (
            <div>
              <p className="text-xs font-semibold text-olive-500 uppercase tracking-wider mb-2">🥗 Diet Guidelines</p>
              {result.diet_suggestions.foods_to_favor?.length > 0 && (
                <p className="text-sm text-olive-700 mb-1">
                  <span className="font-medium text-emerald-600">✅ Favor: </span>
                  {result.diet_suggestions.foods_to_favor.join(' · ')}
                </p>
              )}
              {result.diet_suggestions.foods_to_avoid?.length > 0 && (
                <p className="text-sm text-olive-700">
                  <span className="font-medium text-red-500">❌ Avoid: </span>
                  {result.diet_suggestions.foods_to_avoid.join(' · ')}
                </p>
              )}
            </div>
          )}

          <button
            onClick={() => printReport({ result, userName: report.userName, date: report.date || report.created })}
            className="btn-secondary w-full py-2.5 text-sm"
          >
            🖨️ Print / Download Report
          </button>
        </div>
      )}
    </div>
  )
}

// ── Main Profile Page ────────────────────────────────────────────────────────
export default function Profile() {
  const { user, updateProfile, logout } = useAuth()
  const navigate = useNavigate()
  const [tab, setTab] = useState('profile')
  const [form, setForm] = useState({ ...user })
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [saveError, setSaveError] = useState(null)
  const [reports, setReports] = useState([])
  const [reportsLoading, setReportsLoading] = useState(false)

  if (!user) { navigate('/login'); return null }

  const isDoctor = user.role === 'doctor'
  const fields = isDoctor ? DOCTOR_FIELDS : USER_FIELDS

  // Load reports when Reports tab is opened
  useEffect(() => {
    if (tab !== 'reports') return
    setReportsLoading(true)

    // Always load from localStorage first (instant, works offline)
    const local = JSON.parse(localStorage.getItem('ayur_reports') || '[]')
    setReports(local)

    // Then try PocketBase for richer data
    if (user?.id) {
      assessmentService.getByUser(user.id)
        .then(pbRecords => {
          if (pbRecords.length === 0) return
          const pbReports = pbRecords.map(r => ({
            id: r.id,
            date: r.created,
            result: (() => { try { return JSON.parse(r.ai_analysis) } catch { return { dominant: r.dosha_result } } })(),
            source: 'pb',
          }))
          // Merge: PocketBase records take priority, fill rest from local
          const pbIds = new Set(pbReports.map(r => r.id))
          const localOnly = local.filter(r => !pbIds.has(r.id))
          setReports([...pbReports, ...localOnly])
        })
        .catch(() => {}) // PocketBase offline — local data already shown
        .finally(() => setReportsLoading(false))
    } else {
      setReportsLoading(false)
    }
  }, [tab, user?.id])

  const handleChange = (key, val) => setForm(f => ({ ...f, [key]: val }))

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true); setSaveError(null)
    try {
      await updateProfile(form)
      if (isDoctor) {
        await doctorService.upsert(user.id, {
          doctor_name: form.name,
          specialization: form.specialization || '',
          availability: form.availability || '',
          contact_info: form.phone || '',
        }).catch(() => {})
      }
      setSaved(true)
      setTimeout(() => setSaved(false), 2500)
    } catch (err) {
      setSaveError(err.message || 'Save failed.')
    } finally {
      setSaving(false)
    }
  }

  const handleLogout = () => { logout(); navigate('/login') }

  const TABS = [
    { key: 'profile', label: isDoctor ? '🩺 Profile' : '👤 Profile' },
    { key: 'reports', label: `📋 Reports${reports.length ? ` (${reports.length})` : ''}` },
  ]

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">

      {/* ── Header card ── */}
      <div className="card mb-5 flex items-center gap-4">
        <Avatar user={form} size="lg" />
        <div className="flex-1 min-w-0">
          <h1 className="font-serif text-xl font-bold text-olive-800 truncate">
            {form.name || 'Your Name'}
          </h1>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className={`badge text-xs px-2.5 py-1 ${isDoctor
              ? 'bg-blue-50 text-blue-700 border border-blue-200'
              : 'bg-olive-50 text-olive-700 border border-olive-200'}`}>
              {isDoctor ? '🩺 Doctor' : '👤 User'}
            </span>
            {isDoctor && form.specialization && (
              <span className="text-xs text-olive-500 truncate">{form.specialization}</span>
            )}
            {!isDoctor && form.city && (
              <span className="text-xs text-olive-500">📍 {form.city}</span>
            )}
          </div>
          {isDoctor && form.qualification && (
            <p className="text-xs text-olive-400 mt-1">{form.qualification}</p>
          )}
        </div>
      </div>

      {/* ── Doctor stats strip ── */}
      {isDoctor && (
        <div className="grid grid-cols-3 gap-3 mb-5">
          {[
            { label: 'Experience', value: form.experience ? `${form.experience} yrs` : '—' },
            { label: 'Hospital',   value: form.hospital || '—' },
            { label: 'Reg. No.',   value: form.reg_number || '—' },
          ].map(item => (
            <div key={item.label} className="card text-center py-3">
              <p className="text-xs text-olive-400 mb-1">{item.label}</p>
              <p className="text-sm font-semibold text-olive-800 truncate">{item.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* ── Tabs ── */}
      <div className="flex gap-2 p-1 bg-cream-100 rounded-2xl mb-5">
        {TABS.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`flex-1 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
              tab === t.key ? 'bg-white text-olive-700 shadow-soft' : 'text-olive-500 hover:text-olive-700'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── Profile Tab ── */}
      {tab === 'profile' && (
        <form onSubmit={handleSave} className="card space-y-4">
          <h2 className="font-semibold text-olive-800 text-base">
            {isDoctor ? '🩺 Doctor Details' : '👤 Personal Details'}
          </h2>
          {fields.map(f => (
            <div key={f.key}>
              <label className="block text-sm font-medium text-olive-700 mb-1.5">{f.label}</label>
              {f.type === 'select' ? (
                <select value={form[f.key] || ''} onChange={e => handleChange(f.key, e.target.value)} className="input-field">
                  <option value="">Select…</option>
                  {f.options.map(o => <option key={o} value={o}>{o}</option>)}
                </select>
              ) : f.type === 'textarea' ? (
                <textarea rows={3} value={form[f.key] || ''} onChange={e => handleChange(f.key, e.target.value)}
                  placeholder={f.placeholder} className="input-field resize-none" />
              ) : (
                <input type={f.type} value={form[f.key] || ''} onChange={e => handleChange(f.key, e.target.value)}
                  placeholder={f.placeholder} className="input-field" />
              )}
            </div>
          ))}
          <button type="submit" disabled={saving} className="btn-primary w-full py-3 mt-2">
            {saving
              ? <span className="flex items-center justify-center gap-2"><span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />Saving…</span>
              : saved ? '✓ Profile Saved!' : 'Save Profile'}
          </button>
          {saveError && <p className="text-red-500 text-sm text-center">{saveError}</p>}
        </form>
      )}

      {/* ── Reports Tab ── */}
      {tab === 'reports' && (
        <div className="space-y-3">
          <div className="flex items-center justify-between mb-1">
            <h2 className="font-semibold text-olive-800">Assessment History</h2>
            {reports.length > 0 && (
              <span className="text-xs text-olive-400">{reports.length} report{reports.length !== 1 ? 's' : ''}</span>
            )}
          </div>

          {reportsLoading ? (
            <div className="text-center py-12">
              <div className="w-10 h-10 border-4 border-olive-200 border-t-olive-600 rounded-full animate-spin mx-auto mb-3" />
              <p className="text-sm text-olive-400">Loading reports…</p>
            </div>
          ) : reports.length === 0 ? (
            <div className="card text-center py-12">
              <span className="text-4xl">📋</span>
              <h3 className="font-semibold text-olive-700 mt-3 mb-1">No Reports Yet</h3>
              <p className="text-sm text-olive-400 mb-5">Complete an assessment to see your Prakriti report here.</p>
              <button onClick={() => navigate('/assessment')} className="btn-primary px-6 py-2.5 text-sm">
                Take Assessment →
              </button>
            </div>
          ) : (
            reports.map((report, i) => (
              <ReportCard key={report.id || i} report={report} index={i} />
            ))
          )}
        </div>
      )}

      {/* ── Sign Out ── */}
      <button onClick={handleLogout}
        className="btn-secondary w-full py-3 mt-5 text-red-600 border-red-200 hover:bg-red-50">
        Sign Out
      </button>
    </div>
  )
}
