import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'

export default function TeacherDashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-8 text-center">
        <div className="text-6xl mb-4">🏫</div>
        <h1 className="text-3xl font-bold text-white mb-3">Teacher Dashboard</h1>
        <p className="text-slate-400 mb-6">
          Clinical simulator features have been removed from this version.
        </p>
        <div className="space-y-3">
          <button 
            onClick={() => navigate('/')}
            className="w-full px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-white rounded-xl font-medium transition-all"
          >
            ← Back to Home
          </button>
          <button 
            onClick={() => navigate('/assessment')}
            className="w-full px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-xl font-medium transition-all"
          >
            Go to Ayurveda Assessment
          </button>
        </div>
      </div>
    </div>
  )
}

// ── Tab button ────────────────────────────────────────────────────────────────
function Tab({ label, active, onClick, count }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
        active ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40' : 'text-slate-400 hover:text-white'
      }`}
    >
      {label}
      {count !== undefined && (
        <span className={`text-xs px-1.5 py-0.5 rounded-full ${active ? 'bg-cyan-500/30' : 'bg-slate-700'}`}>
          {count}
        </span>
      )}
    </button>
  )
}

// ── Case form ─────────────────────────────────────────────────────────────────
function CreateCaseForm({ onSave, onCancel }) {
  const [form, setForm] = useState({
    patientName: '', age: '', gender: 'Male', occupation: '',
    complaint: '', hiddenDiagnosis: '', severity: 'moderate',
    emotion: 'anxious', history: '', lifestyle: '',
    doshaImbalance: 'Pitta', difficulty: 'medium',
    redFlags: '', clues: '',
  })
  const [saving, setSaving] = useState(false)

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await simulatorDB.savePatientCase({
        ...form,
        age: parseInt(form.age),
        redFlags: form.redFlags.split(',').map(s => s.trim()).filter(Boolean),
        clues: form.clues,
        created_by: 'teacher',
      })
      onSave()
    } catch (err) {
      console.error(err)
    } finally {
      setSaving(false)
    }
  }

  const Field = ({ label, name, type = 'text', options, rows }) => (
    <div>
      <label className="block text-xs text-slate-400 mb-1">{label}</label>
      {options ? (
        <select value={form[name]} onChange={e => set(name, e.target.value)}
          className="sim-input w-full">
          {options.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
      ) : rows ? (
        <textarea value={form[name]} onChange={e => set(name, e.target.value)}
          rows={rows} className="sim-input w-full resize-none" />
      ) : (
        <input type={type} value={form[name]} onChange={e => set(name, e.target.value)}
          className="sim-input w-full" />
      )}
    </div>
  )

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <Field label="Patient Name *" name="patientName" />
        <Field label="Age *" name="age" type="number" />
        <Field label="Gender" name="gender" options={['Male', 'Female', 'Other']} />
        <Field label="Occupation" name="occupation" />
        <Field label="Severity" name="severity" options={['mild', 'moderate', 'high']} />
        <Field label="Difficulty" name="difficulty" options={['easy', 'medium', 'hard']} />
        <Field label="Emotional State" name="emotion" options={['anxious', 'worried', 'nervous', 'calm', 'calm but confused']} />
        <Field label="Dosha Imbalance" name="doshaImbalance" options={['Vata', 'Pitta', 'Kapha', 'Vata-Pitta', 'Pitta-Kapha', 'Vata-Kapha']} />
      </div>
      <Field label="Chief Complaint *" name="complaint" rows={2} />
      <Field label="Hidden Diagnosis *" name="hiddenDiagnosis" />
      <Field label="Medical History" name="history" rows={2} />
      <Field label="Lifestyle Notes" name="lifestyle" rows={2} />
      <Field label="Red Flags (comma separated)" name="redFlags" />
      <Field label="Clinical Clues (JSON or text)" name="clues" rows={2} />

      <div className="flex gap-3 pt-2">
        <button type="button" onClick={onCancel} className="sim-btn-secondary flex-1">Cancel</button>
        <button type="submit" disabled={saving || !form.patientName || !form.complaint || !form.hiddenDiagnosis}
          className="sim-btn-primary flex-1 disabled:opacity-50">
          {saving ? 'Saving...' : '💾 Save Case'}
        </button>
      </div>
    </form>
  )
}

// ── Student row ───────────────────────────────────────────────────────────────
function StudentRow({ sim }) {
  const ev = (() => { try { return JSON.parse(sim.evaluation) } catch { return null } })()
  const patient = (() => { try { return JSON.parse(sim.patient_data) } catch { return null } })()
  const score = ev?.scores?.overall ?? sim.overall_score ?? 0

  return (
    <div className="flex items-center gap-4 p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-cyan-500/30 transition-all">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-sm font-bold shrink-0 ${
        score >= 75 ? 'bg-emerald-500/20 text-emerald-400' :
        score >= 50 ? 'bg-amber-500/20 text-amber-400' :
        'bg-red-500/20 text-red-400'
      }`}>
        {score}%
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-white text-sm font-medium truncate">{sim.diagnosis || 'Unknown'}</div>
        <div className="text-slate-500 text-xs">
          {patient?.name} · {new Date(sim.created).toLocaleDateString('en-IN')}
          {ev?.questionCount ? ` · ${ev.questionCount}Q` : ''}
        </div>
      </div>
      <div className="hidden sm:flex gap-3 text-xs text-slate-500">
        <span>Comm: <span className="text-slate-300">{ev?.scores?.communication ?? '-'}%</span></span>
        <span>Reason: <span className="text-slate-300">{ev?.scores?.clinicalReasoning ?? '-'}%</span></span>
      </div>
    </div>
  )
}

export default function TeacherDashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [tab, setTab] = useState('overview')
  const [cases, setCases] = useState([])
  const [allSims, setAllSims] = useState([])
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      simulatorDB.getPatientCases(),
      // Fetch all simulations (teacher view)
      pb.collection('simulations').getFullList({ sort: '-created', $autoCancel: false }).catch(() => []),
    ]).then(([c, s]) => {
      setCases(c)
      setAllSims(s)
    }).finally(() => setLoading(false))
  }, [])

  const handleCaseSaved = async () => {
    setShowCreateForm(false)
    const c = await simulatorDB.getPatientCases()
    setCases(c)
  }

  // Analytics aggregation
  const totalStudents = new Set(allSims.map(s => s.user_id)).size
  const avgScore = allSims.length
    ? Math.round(allSims.reduce((a, s) => a + (s.overall_score || 0), 0) / allSims.length)
    : 0

  if (loading) return (
    <div className="sim-bg min-h-screen flex items-center justify-center">
      <div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div className="sim-bg min-h-screen pb-8">
      {/* Header */}
      <div className="sim-header px-4 lg:px-8 py-6">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="text-xs text-cyan-400 font-mono uppercase tracking-widest mb-1">Teacher / Admin Panel</div>
            <h1 className="text-2xl font-bold text-white">Clinical Training Management</h1>
            <p className="text-slate-400 text-sm mt-1">
              {totalStudents} students · {allSims.length} simulations · {cases.length} custom cases
            </p>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            className="sim-btn-primary flex items-center gap-2 text-sm"
          >
            <span>➕</span> Create Patient Case
          </button>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 lg:px-8 mt-6">

        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[
            { icon: '👥', label: 'Active Students', value: totalStudents },
            { icon: '🏥', label: 'Total Simulations', value: allSims.length },
            { icon: '📋', label: 'Custom Cases', value: cases.length },
            { icon: '🎯', label: 'Avg Student Score', value: `${avgScore}%` },
          ].map(s => (
            <div key={s.label} className="sim-card text-center">
              <div className="text-2xl mb-1">{s.icon}</div>
              <div className="text-xl font-bold text-white">{s.value}</div>
              <div className="text-xs text-slate-400">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto scrollbar-hide">
          <Tab label="Overview" active={tab === 'overview'} onClick={() => setTab('overview')} />
          <Tab label="Student Performance" active={tab === 'students'} onClick={() => setTab('students')} count={allSims.length} />
          <Tab label="Patient Cases" active={tab === 'cases'} onClick={() => setTab('cases')} count={cases.length} />
        </div>

        {/* Create case form modal */}
        {showCreateForm && (
          <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4" onClick={() => setShowCreateForm(false)}>
            <div className="sim-card w-full max-w-2xl max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
              <h3 className="text-white font-bold text-lg mb-4">Create Custom Patient Case</h3>
              <CreateCaseForm onSave={handleCaseSaved} onCancel={() => setShowCreateForm(false)} />
            </div>
          </div>
        )}

        {/* Tab: Overview */}
        {tab === 'overview' && (
          <div className="space-y-4">
            <div className="sim-card">
              <h3 className="text-white font-semibold mb-4">Recent Simulations</h3>
              {allSims.length === 0 ? (
                <p className="text-slate-500 text-sm text-center py-6">No simulations yet.</p>
              ) : (
                <div className="space-y-3">
                  {allSims.slice(0, 8).map((sim, i) => <StudentRow key={sim.id || i} sim={sim} />)}
                </div>
              )}
            </div>

            {/* Score distribution */}
            <div className="sim-card">
              <h3 className="text-white font-semibold mb-4">Score Distribution</h3>
              <div className="space-y-3">
                {[
                  { label: 'Excellent (75-100%)', count: allSims.filter(s => (s.overall_score || 0) >= 75).length, color: 'bg-emerald-400' },
                  { label: 'Good (50-74%)', count: allSims.filter(s => (s.overall_score || 0) >= 50 && (s.overall_score || 0) < 75).length, color: 'bg-amber-400' },
                  { label: 'Needs Work (0-49%)', count: allSims.filter(s => (s.overall_score || 0) < 50).length, color: 'bg-red-400' },
                ].map(d => (
                  <div key={d.label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-300">{d.label}</span>
                      <span className="text-slate-400">{d.count} students</span>
                    </div>
                    <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${d.color}`}
                        style={{ width: allSims.length ? `${(d.count / allSims.length) * 100}%` : '0%' }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Tab: Students */}
        {tab === 'students' && (
          <div className="sim-card">
            <h3 className="text-white font-semibold mb-4">All Student Simulations</h3>
            {allSims.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-6">No simulations yet.</p>
            ) : (
              <div className="space-y-3">
                {allSims.map((sim, i) => <StudentRow key={sim.id || i} sim={sim} />)}
              </div>
            )}
          </div>
        )}

        {/* Tab: Cases */}
        {tab === 'cases' && (
          <div className="space-y-4">
            {cases.length === 0 ? (
              <div className="sim-card text-center py-10">
                <div className="text-4xl mb-3">📋</div>
                <p className="text-slate-400 text-sm mb-4">No custom cases yet.</p>
                <button onClick={() => setShowCreateForm(true)} className="sim-btn-primary text-sm">
                  Create First Case
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {cases.map((c, i) => (
                  <div key={c.id || i} className="sim-card hover:border-cyan-500/40 transition-all">
                    <div className="flex items-start justify-between mb-2">
                      <div className="text-white font-semibold text-sm">{c.patientName || 'Patient'}</div>
                      <span className={`text-xs px-2 py-0.5 rounded-full border ${
                        c.difficulty === 'hard' ? 'bg-red-500/20 text-red-400 border-red-500/30' :
                        c.difficulty === 'easy' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' :
                        'bg-amber-500/20 text-amber-400 border-amber-500/30'
                      }`}>{c.difficulty || 'medium'}</span>
                    </div>
                    <p className="text-slate-400 text-xs mb-2 line-clamp-2">{c.complaint}</p>
                    <div className="text-xs text-cyan-400 font-medium">{c.hiddenDiagnosis}</div>
                    <div className="flex items-center gap-2 mt-3">
                      <span className="text-xs text-slate-500">{c.doshaImbalance} · {c.severity}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  )
}
