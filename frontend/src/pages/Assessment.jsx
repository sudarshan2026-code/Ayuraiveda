import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { QUESTION_BANK } from '../prakriti/questionBank'
import { getTranslatedQuestion, getTranslatedOption } from '../prakriti/questionsTranslations'
import { DOSHAS } from '../prakriti/doshaMapping'
import { calculatePrakriti } from '../prakriti/prakritiCalculator'
import { interpretResult } from '../prakriti/resultInterpreter'
import DoshaCard from '../components/DoshaCard'
import { useNotifications } from '../hooks/useNotifications.jsx'
import { useAuth } from '../hooks/useAuth.jsx'
import { submitAssessment } from '../services/api'
import { assessmentService } from '../services/pocketbase.js'
import { printReport } from '../utils/printReport.js'
import { canTakeAssessment, isMembershipActive, incrementUsage } from '../utils/membership.js'

const PERSONAL_FIELDS = [
  { key: 'name',   label: 'Full Name',   type: 'text',   placeholder: 'Your full name' },
  { key: 'age',    label: 'Age',         type: 'number', placeholder: 'Your age' },
  { key: 'gender', label: 'Gender',      type: 'select',
    options: [{ value: 'male', label: 'Male' }, { value: 'female', label: 'Female' }, { value: 'other', label: 'Other' }] },
  { key: 'weight', label: 'Weight (kg)', type: 'number', placeholder: 'e.g. 65' },
  { key: 'height', label: 'Height (cm)', type: 'number', placeholder: 'e.g. 170' },
]

export default function Assessment() {
  const { t, i18n } = useTranslation()
  const [phase, setPhase] = useState('intro') // 'intro' | 'form' | 'processing' | 'results'
  const [step, setStep] = useState(0) // 0 = Personal Info, 1 to 22 = Q1 to Q22
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [activeTab, setActiveTab] = useState('overview') // 'overview' | 'characteristics' | 'lifestyle' | 'diet' | 'seasonal'
  const [error, setError] = useState(null)
  const { addNotification } = useNotifications()
  const { user } = useAuth()
  const navigate = useNavigate()

  const membershipActive = isMembershipActive(user?.id)
  const { allowed: canAssess, isFree } = canTakeAssessment(user?.id)

  // Calculate questionnaire progress (only for Q1 to Q22)
  const totalQuestions = QUESTION_BANK.length // 22
  const answeredQuestionsCount = QUESTION_BANK.filter(q => answers[`q${q.id}`]).length
  const progress = Math.round((answeredQuestionsCount / totalQuestions) * 100)

  const handlePersonalField = (key, value) => {
    setAnswers(prev => ({ ...prev, [key]: value }))
  }

  const handleAnswerSelection = (questionId, optionText) => {
    setAnswers(prev => ({ ...prev, [`q${questionId}`]: optionText }))
  }

  const isPersonalFormValid = () => {
    return PERSONAL_FIELDS.every(field => answers[field.key] && String(answers[field.key]).trim() !== '')
  }

  const isCurrentQuestionAnswered = () => {
    if (step === 0) return isPersonalFormValid()
    return !!answers[`q${step}`]
  }

  const handleNext = () => {
    if (isCurrentQuestionAnswered()) {
      setStep(prev => prev + 1)
    }
  }

  const handleBack = () => {
    if (step > 0) {
      setStep(prev => prev - 1)
    } else {
      setPhase('intro')
    }
  }

  const handleSubmit = async () => {
    setPhase('processing')
    setError(null)
    try {
      // 1. Tally locally first using our modular engines
      const localPrakriti = calculatePrakriti(answers)
      const localInterpretation = interpretResult(localPrakriti)

      // 2. Submit to backend API to align and save on database/AI reports
      let finalResult = localInterpretation
      try {
        const backendRes = await submitAssessment(answers)
        // Merge backend result, prioritizing detailed local fields for richer display
        finalResult = {
          ...localInterpretation,
          ...backendRes,
          // Guarantee new premium categories are preserved
          personality_traits: localInterpretation.personality_traits,
          physical_characteristics: localInterpretation.physical_characteristics,
          exercise_recommendations: localInterpretation.exercise_recommendations,
          sleep_recommendations: localInterpretation.sleep_recommendations,
          seasonal_precautions: localInterpretation.seasonal_precautions,
          strengths: localInterpretation.strengths,
          possible_health_tendencies: localInterpretation.possible_health_tendencies
        }
      } catch (err) {
        console.warn("Backend API calculation failed, falling back to local client-side calculation:", err)
      }

      setResult(finalResult)
      setPhase('results')

      // Save report locally
      const report = {
        id: Date.now().toString(),
        date: new Date().toISOString(),
        answers,
        result: finalResult,
        userName: answers.name || user?.name || 'Anonymous',
      }
      const existing = JSON.parse(localStorage.getItem('ayur_reports') || '[]')
      localStorage.setItem('ayur_reports', JSON.stringify([report, ...existing].slice(0, 20)))

      // Track usage
      if (user?.id) incrementUsage(user.id)

      // Save to PocketBase
      if (user?.id) {
        assessmentService.save({ userId: user.id, answers, result: finalResult }).catch((e) => {
          console.error("PocketBase save failed:", e)
        })
      }

      addNotification({
        title: t('notifications.assessment_complete'),
        body: `${t('assessment.result_prakriti')} ${finalResult.dominant}. ${finalResult.risk} Imbalance Risk.`,
      })
    } catch (e) {
      console.error(e)
      setError(t('assessment.error'))
      setPhase('form')
    }
  }

  const reset = () => {
    setPhase('intro')
    setStep(0)
    setAnswers({})
    setResult(null)
    setError(null)
    setActiveTab('overview')
  }

  // ── INTRO PAGE ─────────────────────────────────────────────────────────────
  if (phase === 'intro') {
    if (!canAssess) {
      return (
        <div className="max-w-md mx-auto px-4 py-16 text-center page-enter">
          <span className="text-5xl">🔒</span>
          <h2 className="font-serif text-2xl font-bold text-olive-800 mt-4 mb-2">{t('assessment.membership_required')}</h2>
          <p className="text-olive-500 mb-2">{t('assessment.free_trial_used')}</p>
          <p className="text-olive-500 mb-6">{t('assessment.contact_admin_membership')}</p>
          <div className="card mb-6 text-left space-y-2">
            <p className="text-sm font-semibold text-olive-700">{t('assessment.membership_includes')}</p>
            {[
              t('assessment.unlimited_assessments'),
              t('assessment.full_pdf_download'),
              t('assessment.complete_ai_analysis'),
              t('assessment.diet_lifestyle_plan')
            ].map(f => (
              <div key={f} className="flex items-center gap-2 text-sm text-olive-600">
                <span className="text-emerald-500">✓</span> {f}
              </div>
            ))}
          </div>
          <button onClick={() => navigate('/')} className="btn-secondary w-full py-3">{t('assessment.back_to_home')}</button>
        </div>
      )
    }

    return (
      <div className="max-w-2xl mx-auto px-4 py-10 text-center page-enter">
        <span className="text-5xl">🌿</span>
        <h1 className="section-title mt-4 mb-3">{t('assessment.title')}</h1>
        <p className="text-olive-500 mb-8 leading-relaxed">
          {t('assessment.desc_22')}
        </p>
        {isFree && (
          <div className="mb-5 px-4 py-3 bg-amber-50 border border-amber-200 rounded-2xl text-sm text-amber-700">
            <strong>Free Trial:</strong> You have 1 free assessment. Activate membership for unlimited access.
          </div>
        )}
        <div className="card mb-8 text-left space-y-3">
          <p className="text-sm font-semibold text-olive-800 mb-2">{t('assessment.details_title')}</p>
          {[
            t('assessment.bullet_1'),
            t('assessment.bullet_2'),
            t('assessment.bullet_3'),
            t('assessment.bullet_4'),
            t('assessment.bullet_5')
          ].map((text, idx) => (
            <div key={idx} className="flex items-start gap-3 text-sm text-olive-700">
              <span className="w-5 h-5 rounded-full bg-olive-100 text-olive-600 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">✓</span>
              <span>{text}</span>
            </div>
          ))}
        </div>
        <button onClick={() => setPhase('form')} className="btn-primary w-full py-4 text-base">
          {t('assessment.begin_btn')}
        </button>
      </div>
    )
  }

  // ── PROCESSING PAGE ────────────────────────────────────────────────────────
  if (phase === 'processing') {
    return (
      <div className="text-center py-20 page-enter">
        <div className="w-16 h-16 border-4 border-olive-200 border-t-olive-600 rounded-full animate-spin mx-auto mb-6" />
        <h2 className="font-serif text-2xl font-bold text-olive-800 mb-2">{t('assessment.processing_title')}</h2>
        <p className="text-olive-500">{t('assessment.processing_desc')}</p>
      </div>
    )
  }

  // ── RESULTS DASHBOARD ──────────────────────────────────────────────────────
  if (phase === 'results' && result) {
    const dom = result.dominant?.split('-')[0].split(' ')[0].toLowerCase() || 'vata'
    const doshaInfo = DOSHAS[dom] || DOSHAS.vata
    const riskColors = {
      High: 'text-red-700 bg-red-50 border-red-200',
      Moderate: 'text-amber-700 bg-amber-50 border-amber-200',
      Low: 'text-emerald-700 bg-emerald-50 border-emerald-200'
    }

    return (
      <div className="max-w-3xl mx-auto px-4 py-10 page-enter">
        {/* Header summary */}
        <div className="text-center mb-8">
          <span className="text-5xl">{doshaInfo.emoji}</span>
          <h2 className="font-serif text-3xl md:text-4xl font-bold text-olive-800 mt-4 mb-2">
            Prakriti: <span className={doshaInfo.text}>{result.dominant}</span>
          </h2>
          <span className={`badge border text-sm px-4 py-1.5 ${riskColors[result.risk] || riskColors.Low}`}>
            {result.risk} Imbalance Risk
          </span>
        </div>

        {/* Dosha Progress Bars */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {['vata', 'pitta', 'kapha'].map(d => (
            <DoshaCard key={d} type={d} score={result.scores?.[d] ?? 0} showBar />
          ))}
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 p-1 bg-cream-100 rounded-2xl mb-6">
          {[
            { id: 'overview', label: '📋 Overview' },
            { id: 'characteristics', label: '👤 Traits & Body' },
            { id: 'lifestyle', label: '🧘 Routine' },
            { id: 'diet', label: '🥗 Diet Plan' },
            { id: 'seasonal', label: '❄️ Seasons' }
          ].map(t => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex-1 py-2 px-3 rounded-xl text-xs md:text-sm font-medium transition-all duration-200 ${
                activeTab === t.id ? 'bg-white text-olive-800 shadow-soft' : 'text-olive-500 hover:text-olive-700'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Tab Contents */}
        <div className="space-y-6 mb-8">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Clinical Interpretation */}
              <div className="card">
                <h3 className="font-serif text-lg font-bold text-olive-800 mb-3">Ayurvedic Interpretation</h3>
                <p className="text-sm text-olive-700 leading-relaxed">{result.justification}</p>
              </div>

              {/* Agni & Ama */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="card text-center py-4 bg-olive-50/50">
                  <p className="text-xs text-olive-400 uppercase tracking-wider">Digestive Agni</p>
                  <p className="text-sm font-bold text-olive-800 mt-1">{result.agni_state}</p>
                </div>
                <div className="card text-center py-4 bg-olive-50/50">
                  <p className="text-xs text-olive-400 uppercase tracking-wider">Ama (Toxin Level)</p>
                  <p className="text-sm font-bold text-olive-800 mt-1">{result.ama_status}</p>
                </div>
                <div className="card text-center py-4 bg-olive-50/50">
                  <p className="text-xs text-olive-400 uppercase tracking-wider">Current Vikriti</p>
                  <p className="text-sm font-bold text-olive-800 mt-1">{result.vikriti}</p>
                </div>
              </div>

              {/* Strengths & Health Tendencies */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="card border border-emerald-100 bg-emerald-50/20">
                  <h4 className="font-bold text-emerald-800 text-sm mb-3 flex items-center gap-1.5">
                    <span>🌟</span> Core Strengths
                  </h4>
                  <ul className="space-y-2">
                    {result.strengths?.map((str, i) => (
                      <li key={i} className="text-sm text-emerald-950 flex items-start gap-2">
                        <span className="text-emerald-500">•</span>
                        <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="card border border-amber-100 bg-amber-50/20">
                  <h4 className="font-bold text-amber-800 text-sm mb-3 flex items-center gap-1.5">
                    <span>⚠️</span> Health Tendencies
                  </h4>
                  <ul className="space-y-2">
                    {result.possible_health_tendencies?.map((ten, i) => (
                      <li key={i} className="text-sm text-amber-950 flex items-start gap-2">
                        <span className="text-amber-500">•</span>
                        <span>{ten}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'characteristics' && (
            <div className="space-y-6">
              {/* Personality traits */}
              <div className="card">
                <h3 className="font-serif text-lg font-bold text-olive-800 mb-4 flex items-center gap-2">
                  <span>🧠</span> Personality Traits
                </h3>
                <ul className="space-y-2.5">
                  {result.personality_traits?.map((t, i) => (
                    <li key={i} className="text-sm text-olive-700 flex items-start gap-2.5">
                      <span className="w-5 h-5 rounded-full bg-olive-50 text-olive-500 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">{i+1}</span>
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Physical characteristics */}
              <div className="card">
                <h3 className="font-serif text-lg font-bold text-olive-800 mb-4 flex items-center gap-2">
                  <span>📐</span> Physical Characteristics
                </h3>
                <ul className="space-y-2.5">
                  {result.physical_characteristics?.map((c, i) => (
                    <li key={i} className="text-sm text-olive-700 flex items-start gap-2.5">
                      <span className="w-5 h-5 rounded-full bg-olive-50 text-olive-500 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">{i+1}</span>
                      <span>{c}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'lifestyle' && (
            <div className="space-y-6">
              {/* Lifestyle recs */}
              <div className="card">
                <h3 className="font-serif text-lg font-bold text-olive-800 mb-4 flex items-center gap-2">
                  <span>🧘</span> Lifestyle & Routine (Dinacharya)
                </h3>
                <ul className="space-y-3">
                  {result.lifestyle_recommendations?.map((r, i) => (
                    <li key={i} className="text-sm text-olive-700 flex gap-2">
                      <span className="text-olive-400 shrink-0 mt-0.5">•</span>
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Exercise and sleep side by side */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="card">
                  <h4 className="font-serif text-base font-bold text-olive-800 mb-3 flex items-center gap-2">
                    <span>🏃</span> Exercise Guidelines
                  </h4>
                  <ul className="space-y-2">
                    {result.exercise_recommendations?.map((r, i) => (
                      <li key={i} className="text-xs md:text-sm text-olive-700 flex gap-2">
                        <span className="text-olive-400 shrink-0 mt-0.5">•</span>
                        <span>{r}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="card">
                  <h4 className="font-serif text-base font-bold text-olive-800 mb-3 flex items-center gap-2">
                    <span>🛌</span> Sleep Recommendations
                  </h4>
                  <ul className="space-y-2">
                    {result.sleep_recommendations?.map((r, i) => (
                      <li key={i} className="text-xs md:text-sm text-olive-700 flex gap-2">
                        <span className="text-olive-400 shrink-0 mt-0.5">•</span>
                        <span>{r}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'diet' && (
            <div className="card">
              <h3 className="font-serif text-lg font-bold text-olive-800 mb-4 flex items-center gap-2">
                <span>🥗</span> Dietary Recommendations
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-4 rounded-2xl bg-emerald-50/30 border border-emerald-100">
                  <p className="font-bold text-emerald-800 text-sm mb-3 flex items-center gap-1.5">
                    <span>✅</span> Foods to Favor
                  </p>
                  <p className="text-sm text-emerald-950 leading-relaxed">
                    {result.diet_suggestions?.foods_to_favor?.join(' · ')}
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-red-50/30 border border-red-100">
                  <p className="font-bold text-red-800 text-sm mb-3 flex items-center gap-1.5">
                    <span>❌</span> Foods to Avoid
                  </p>
                  <p className="text-sm text-red-950 leading-relaxed">
                    {result.diet_suggestions?.foods_to_avoid?.join(' · ')}
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'seasonal' && (
            <div className="card">
              <h3 className="font-serif text-lg font-bold text-olive-800 mb-4 flex items-center gap-2">
                <span>❄️</span> Seasonal Precautions (Ritucharya)
              </h3>
              <ul className="space-y-3">
                {result.seasonal_precautions?.map((r, i) => (
                  <li key={i} className="text-sm text-olive-700 flex gap-2">
                    <span className="text-olive-400 shrink-0 mt-0.5">•</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Buttons / Actions */}
        <div className="flex flex-col sm:flex-row gap-3">
          <button onClick={reset} className="btn-secondary flex-1">
            {t('assessment.retake_btn')}
          </button>
          {membershipActive ? (
            <button
              onClick={() => printReport({
                result,
                userName: answers.name || user?.name || 'Anonymous',
                date: new Date().toISOString(),
              })}
              className="btn-primary flex-1"
            >
              {t('assessment.download_btn')}
            </button>
          ) : (
            <div className="flex-1 text-center">
              <div className="btn-secondary w-full opacity-50 cursor-not-allowed py-3 text-sm">
                {t('assessment.locked_download')}
              </div>
              <p className="text-xs text-olive-400 mt-1">{t('assessment.locked_download_desc')}</p>
            </div>
          )}
        </div>
        <p className="text-center text-xs text-olive-400 mt-4 leading-relaxed">
          Disclaimer: This assessment provides holistic educational recommendations based on classic Ayurvedic science. It is not intended to diagnose, treat, or cure any medical condition.
        </p>
      </div>
    )
  }

  // ── QUESTIONNAIRE FORM STEPS ──────────────────────────────────────────────
  const currentQuestion = step > 0 ? QUESTION_BANK[step - 1] : null

  return (
    <div className="max-w-2xl mx-auto px-4 py-10 page-enter">
      {/* Progress header & bar */}
      <div className="mb-8">
        <div className="flex justify-between text-xs text-olive-500 mb-2">
          <span>
            {step === 0 
              ? t('assessment.personal_info') 
              : t('assessment.q_step_label', { step: step, total: totalQuestions, name: getTranslatedQuestion(currentQuestion.id, i18n.language) })
            }
          </span>
          {step > 0 && (
            <span>{t('assessment.q_progress', { percent: progress })}</span>
          )}
        </div>
        <div className="h-2 bg-cream-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-olive-500 rounded-full transition-all duration-300" 
            style={{ width: `${step === 0 ? 5 : progress}%` }} 
          />
        </div>
      </div>

      {error && (
        <div className="mb-5 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
          {error}
        </div>
      )}

      {/* ── STEP 0: Personal Info Form ── */}
      {step === 0 && (
        <div className="page-enter">
          <div className="flex items-center gap-3 mb-6">
            <span className="text-3xl">👤</span>
            <h2 className="font-serif text-2xl font-bold text-olive-800">{t('assessment.personal_info')}</h2>
          </div>
          
          <div className="card space-y-4 mb-6">
            {PERSONAL_FIELDS.map(f => (
              <div key={f.key}>
                <label className="block text-sm font-medium text-olive-700 mb-1.5">
                  {t(`assessment.field_${f.key}`)}
                </label>
                {f.type === 'select' ? (
                  <select
                    value={answers[f.key] || ''}
                    onChange={e => handlePersonalField(f.key, e.target.value)}
                    className="input-field"
                  >
                    <option value="">{t('assessment.gender_placeholder')}</option>
                    {f.options?.map(o => (
                      <option key={o.value} value={o.value}>
                        {t(`assessment.gender_${o.value}`)}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type={f.type}
                    placeholder={t(`assessment.placeholder_${f.key}`)}
                    value={answers[f.key] || ''}
                    onChange={e => handlePersonalField(f.key, e.target.value)}
                    className="input-field"
                  />
                )}
              </div>
            ))}
          </div>

          <div className="flex gap-3">
            <button onClick={handleBack} className="btn-secondary flex-1">
              {t('assessment.back_btn')}
            </button>
            <button
              onClick={handleNext}
              disabled={!isPersonalFormValid()}
              className="btn-primary flex-1 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {t('assessment.start_questionnaire')}
            </button>
          </div>
        </div>
      )}

      {/* ── STEPS 1 to 22: Question Options selection ── */}
      {step > 0 && currentQuestion && (
        <div className="page-enter" key={currentQuestion.id}>
          <div className="flex items-center gap-3 mb-6">
            <span className="w-10 h-10 rounded-full bg-olive-100 text-olive-700 flex items-center justify-center text-sm font-bold shrink-0">
              {currentQuestion.id}
            </span>
            <h2 className="font-serif text-xl md:text-2xl font-bold text-olive-800">
              {getTranslatedQuestion(currentQuestion.id, i18n.language)}
            </h2>
          </div>

          <p className="text-xs text-olive-400 uppercase tracking-wider mb-3">{t('assessment.q_select_statement')}</p>

          <div className="space-y-2.5 mb-8">
            {currentQuestion.options.map((opt, idx) => {
              const isSelected = answers[`q${currentQuestion.id}`] === opt.text
              return (
                <button
                  key={idx}
                  onClick={() => handleAnswerSelection(currentQuestion.id, opt.text)}
                  className={`w-full text-left flex items-start gap-3.5 px-4 py-3.5 rounded-xl border transition-all duration-150 active:scale-[0.99]
                    ${isSelected
                      ? 'border-olive-500 bg-olive-50/70 text-olive-800 font-semibold shadow-soft'
                      : 'border-cream-200 bg-white text-olive-700 hover:border-olive-300 hover:bg-olive-50/30'}`}
                >
                  <span className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 text-[10px] mt-0.5
                    ${isSelected 
                      ? 'border-olive-500 bg-olive-600 text-white font-bold' 
                      : 'border-cream-300 bg-cream-50 text-olive-300'}`}
                  >
                    {isSelected ? '✓' : ''}
                  </span>
                  <span className="text-sm md:text-base leading-relaxed">
                    {getTranslatedOption(currentQuestion.id, idx, i18n.language)}
                  </span>
                </button>
              )
            })}
          </div>

          <div className="flex gap-3">
            <button onClick={handleBack} className="btn-secondary flex-1">
              {t('assessment.back_btn')}
            </button>
            {step === totalQuestions ? (
              <button
                onClick={handleSubmit}
                disabled={!isCurrentQuestionAnswered()}
                className="btn-primary flex-1 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Analyze Prakriti 🌿
              </button>
            ) : (
              <button
                onClick={handleNext}
                disabled={!isCurrentQuestionAnswered()}
                className="btn-primary flex-1 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {t('assessment.next_btn')}
              </button>
            )}
          </div>

          {!isCurrentQuestionAnswered() && (
            <p className="text-center text-xs text-olive-400 mt-4">
              {t('assessment.q_select_at_least_one')}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
