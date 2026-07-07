import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'
import {
  getMemberships, activateMembership, deactivateMembership,
  isMembershipActive, getTotalRevenue, MEMBERSHIP_PRICE
} from '../utils/membership.js'
import pb from '../services/pocketbase.js'

const ADMIN_EMAIL = 'ayuraiveda@gmail.com'
const ADMIN_PIN   = '909909'

// ── PIN Gate ─────────────────────────────────────────────────────────────────
function PinGate({ onSuccess }) {
  const [pin, setPin] = useState('')
  const [error, setError] = useState('')
  const [shake, setShake] = useState(false)
  const navigate = useNavigate()

  const handleDigit = (d) => {
    if (pin.length >= 6) return
    const next = pin + d
    setPin(next)
    if (next.length === 6) {
      if (next === ADMIN_PIN) {
        onSuccess()
      } else {
        setShake(true)
        setError('Incorrect PIN')
        setTimeout(() => { setPin(''); setShake(false); setError('') }, 900)
      }
    }
  }

  return (
    <div className="min-h-screen gradient-hero flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-3xl gradient-olive flex items-center justify-center text-white text-3xl font-bold shadow-soft mx-auto mb-4">
            🔐
          </div>
          <h1 className="font-serif text-2xl font-bold text-olive-800">Admin Access</h1>
          <p className="text-olive-500 text-sm mt-1">Enter your 6-digit security PIN</p>
        </div>

        <div className="card shadow-card">
          {/* PIN dots */}
          <div className={`flex justify-center gap-3 mb-6 ${shake ? 'animate-bounce' : ''}`}>
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className={`w-4 h-4 rounded-full border-2 transition-all duration-150 ${
                i < pin.length
                  ? error ? 'bg-red-500 border-red-500' : 'bg-olive-600 border-olive-600'
                  : 'border-cream-300 bg-cream-50'
              }`} />
            ))}
          </div>

          {error && <p className="text-center text-red-500 text-sm mb-4">{error}</p>}

          {/* Numpad */}
          <div className="grid grid-cols-3 gap-3">
            {[1,2,3,4,5,6,7,8,9,'',0,'⌫'].map((d, i) => (
              <button key={i}
                onClick={() => {
                  if (d === '⌫') setPin(p => p.slice(0, -1))
                  else if (d !== '') handleDigit(String(d))
                }}
                disabled={d === ''}
                className={`h-14 rounded-2xl text-lg font-semibold transition-all duration-150 active:scale-95
                  ${d === '' ? 'invisible' : d === '⌫'
                    ? 'bg-cream-100 text-olive-600 hover:bg-cream-200'
                    : 'bg-cream-50 text-olive-800 hover:bg-olive-50 border border-cream-200'}`}
              >
                {d}
              </button>
            ))}
          </div>

          <button onClick={() => navigate('/')}
            className="w-full text-sm text-olive-400 hover:text-olive-600 mt-5 text-center">
            ← Back to App
          </button>
        </div>
      </div>
    </div>
  )
}

// ── Member Row ────────────────────────────────────────────────────────────────
function MemberRow({ member, onActivate, onDeactivate }) {
  const active = member.active && new Date(member.expiry) > new Date()
  const expiry = member.expiry ? new Date(member.expiry).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric'
  }) : '—'
  const daysLeft = member.expiry
    ? Math.max(0, Math.ceil((new Date(member.expiry) - new Date()) / 86400000))
    : 0

  return (
    <div className="card border border-cream-200 flex flex-col sm:flex-row sm:items-center gap-4">
      {/* Avatar */}
      <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm shrink-0
        ${member.role === 'doctor' ? 'bg-gradient-to-br from-blue-500 to-blue-700' : 'bg-gradient-to-br from-olive-500 to-olive-700'}`}>
        {(member.name || 'U').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-semibold text-olive-800 text-sm truncate">{member.name || 'Unknown'}</span>
          <span className={`badge text-xs px-2 py-0.5 ${member.role === 'doctor'
            ? 'bg-blue-50 text-blue-700 border border-blue-200'
            : 'bg-olive-50 text-olive-700 border border-olive-200'}`}>
            {member.role === 'doctor' ? '🩺 Doctor' : '👤 User'}
          </span>
          {active && (
            <span className="badge text-xs px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200">
              ✓ Active · {daysLeft}d left
            </span>
          )}
          {!active && member.expiry && (
            <span className="badge text-xs px-2 py-0.5 bg-red-50 text-red-600 border border-red-200">
              Expired
            </span>
          )}
        </div>
        <p className="text-xs text-olive-400 mt-0.5 truncate">{member.email}</p>
        {active && <p className="text-xs text-olive-400">Expires: {expiry}</p>}
      </div>

      {/* Actions */}
      <div className="flex gap-2 shrink-0">
        {active ? (
          <button onClick={() => onDeactivate(member.userId)}
            className="text-xs px-3 py-2 rounded-xl bg-red-50 text-red-600 border border-red-200 hover:bg-red-100 transition-colors">
            Deactivate
          </button>
        ) : (
          <button onClick={() => onActivate(member)}
            className="text-xs px-3 py-2 rounded-xl bg-olive-600 text-white hover:bg-olive-700 transition-colors font-semibold">
            + Activate 3 Months
          </button>
        )}
      </div>
    </div>
  )
}

// ── Main Admin Panel ──────────────────────────────────────────────────────────
export default function AdminPanel() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [pinPassed, setPinPassed] = useState(
    () => sessionStorage.getItem('admin_pin_ok') === '1'
  )
  const [members, setMembers] = useState([])
  const [pbUsers, setPbUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState('members')
  const [search, setSearch] = useState('')
  const [toast, setToast] = useState(null)

  // Guard — only admin email allowed
  useEffect(() => {
    if (!user || user.email !== ADMIN_EMAIL) navigate('/', { replace: true })
  }, [user, navigate])

  // Load users from PocketBase + merge with membership data
  useEffect(() => {
    if (!pinPassed) return
    setLoading(true)
    pb.collection('users').getFullList({ sort: '-created' })
      .then(records => {
        setPbUsers(records)
        // Merge with membership data
        const memberships = getMemberships()
        const merged = records.map(r => {
          const m = memberships.find(m => m.userId === r.id)
          return {
            userId: r.id,
            name: r.name || r.email?.split('@')[0],
            email: r.email,
            role: r.role || 'user',
            active: m?.active && new Date(m.expiry) > new Date(),
            expiry: m?.expiry || null,
            activatedAt: m?.activatedAt || null,
            revenue: m?.revenue || 0,
          }
        })
        setMembers(merged)
      })
      .catch(() => {
        // PocketBase offline — show from localStorage only
        setMembers(getMemberships())
      })
      .finally(() => setLoading(false))
  }, [pinPassed])

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type })
    setTimeout(() => setToast(null), 3000)
  }

  const handleActivate = (member) => {
    activateMembership(member.userId, member.name, member.email, member.role)
    setMembers(prev => prev.map(m => m.userId === member.userId ? {
      ...m, active: true,
      expiry: new Date(Date.now() + 90 * 86400000).toISOString(),
      revenue: MEMBERSHIP_PRICE,
    } : m))
    showToast(`Membership activated for ${member.name}`)
  }

  const handleDeactivate = (userId) => {
    deactivateMembership(userId)
    setMembers(prev => prev.map(m => m.userId === userId ? { ...m, active: false } : m))
    showToast('Membership deactivated', 'warn')
  }

  const handlePinSuccess = () => {
    sessionStorage.setItem('admin_pin_ok', '1')
    setPinPassed(true)
  }

  if (!user || user.email !== ADMIN_EMAIL) return null
  if (!pinPassed) return <PinGate onSuccess={handlePinSuccess} />

  const activeCount  = members.filter(m => m.active && new Date(m.expiry) > new Date()).length
  const totalRevenue = members.reduce((s, m) => s + (m.active ? (m.revenue || MEMBERSHIP_PRICE) : 0), 0)
  const filtered     = members.filter(m =>
    !search || m.name?.toLowerCase().includes(search.toLowerCase()) ||
    m.email?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(135deg,#1a1f0a 0%,#2d3a10 100%)' }}>
      {/* Toast */}
      {toast && (
        <div className={`fixed top-4 right-4 z-50 px-5 py-3 rounded-2xl text-sm font-semibold shadow-lg transition-all
          ${toast.type === 'warn' ? 'bg-amber-500 text-white' : 'bg-emerald-500 text-white'}`}>
          {toast.msg}
        </div>
      )}

      {/* Header */}
      <div className="border-b border-white/10 px-4 md:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl gradient-olive flex items-center justify-center text-white font-bold text-sm">
            ॐ
          </div>
          <div>
            <h1 className="font-serif font-bold text-white text-lg leading-tight">AyurAI Veda</h1>
            <p className="text-olive-400 text-xs">Admin Panel</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-olive-400 hidden sm:block">{user.email}</span>
          <button onClick={() => { sessionStorage.removeItem('admin_pin_ok'); logout(); navigate('/login') }}
            className="text-xs px-3 py-2 rounded-xl bg-white/10 text-white hover:bg-white/20 transition-colors">
            Sign Out
          </button>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 md:px-8 py-8">

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total Users',    value: members.length,  icon: '👥', color: 'from-blue-500 to-blue-700' },
            { label: 'Active Members', value: activeCount,     icon: '✅', color: 'from-emerald-500 to-emerald-700' },
            { label: 'Revenue (INR)',  value: `₹${totalRevenue.toLocaleString()}`, icon: '💰', color: 'from-amber-500 to-amber-700' },
            { label: 'Free Trial',     value: members.length - activeCount, icon: '🆓', color: 'from-olive-500 to-olive-700' },
          ].map(s => (
            <div key={s.label} className="rounded-2xl p-4 text-white" style={{ background: 'rgba(255,255,255,0.08)' }}>
              <div className="text-2xl mb-1">{s.icon}</div>
              <div className="text-2xl font-bold">{s.value}</div>
              <div className="text-xs text-white/60 mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex gap-2 p-1 rounded-2xl mb-6" style={{ background: 'rgba(255,255,255,0.06)' }}>
          {[
            { key: 'members', label: '👥 Members' },
            { key: 'revenue', label: '💰 Revenue' },
          ].map(t => (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`flex-1 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                tab === t.key ? 'bg-olive-600 text-white shadow-soft' : 'text-white/60 hover:text-white'
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        {/* Members Tab */}
        {tab === 'members' && (
          <div>
            <div className="flex items-center gap-3 mb-4">
              <input
                value={search} onChange={e => setSearch(e.target.value)}
                placeholder="Search by name or email…"
                className="flex-1 bg-white/10 border border-white/20 rounded-2xl px-4 py-2.5 text-white placeholder-white/40 text-sm focus:outline-none focus:border-olive-400"
              />
              <span className="text-white/50 text-sm shrink-0">{filtered.length} users</span>
            </div>

            {loading ? (
              <div className="text-center py-16">
                <div className="w-10 h-10 border-4 border-olive-400/30 border-t-olive-400 rounded-full animate-spin mx-auto mb-3" />
                <p className="text-white/50 text-sm">Loading users…</p>
              </div>
            ) : filtered.length === 0 ? (
              <div className="text-center py-16 text-white/40">
                <div className="text-4xl mb-3">👥</div>
                <p>No users found</p>
                <p className="text-xs mt-1">Users appear here after they register in the app</p>
              </div>
            ) : (
              <div className="space-y-3">
                {filtered.map(m => (
                  <MemberRow key={m.userId} member={m}
                    onActivate={handleActivate}
                    onDeactivate={handleDeactivate}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Revenue Tab */}
        {tab === 'revenue' && (
          <div className="space-y-4">
            <div className="card">
              <h2 className="font-semibold text-olive-800 mb-4">Revenue Summary</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                {[
                  { label: 'Total Revenue',    value: `₹${totalRevenue.toLocaleString()}` },
                  { label: 'Active Members',   value: activeCount },
                  { label: 'Per Membership',   value: `₹${MEMBERSHIP_PRICE}` },
                ].map(s => (
                  <div key={s.label} className="bg-olive-50 rounded-2xl p-4 text-center">
                    <p className="text-2xl font-bold text-olive-800">{s.value}</p>
                    <p className="text-xs text-olive-500 mt-1">{s.label}</p>
                  </div>
                ))}
              </div>

              <h3 className="font-semibold text-olive-700 text-sm mb-3">Active Memberships</h3>
              {members.filter(m => m.active && new Date(m.expiry) > new Date()).length === 0 ? (
                <p className="text-olive-400 text-sm text-center py-6">No active memberships yet</p>
              ) : (
                <div className="space-y-2">
                  {members.filter(m => m.active && new Date(m.expiry) > new Date()).map(m => (
                    <div key={m.userId} className="flex items-center justify-between py-2 border-b border-cream-100 last:border-0">
                      <div>
                        <p className="text-sm font-medium text-olive-800">{m.name}</p>
                        <p className="text-xs text-olive-400">{m.email}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-bold text-emerald-600">₹{MEMBERSHIP_PRICE}</p>
                        <p className="text-xs text-olive-400">
                          Exp: {new Date(m.expiry).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
