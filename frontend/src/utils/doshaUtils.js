export const DOSHAS = {
  vata:  { label: 'Vata',  color: 'bg-sky-400',    text: 'text-sky-700',    desc: 'Air + Space · Movement & Creativity',   emoji: '🌬️' },
  pitta: { label: 'Pitta', color: 'bg-amber-400',  text: 'text-amber-700',  desc: 'Fire + Water · Metabolism & Digestion',  emoji: '🔥' },
  kapha: { label: 'Kapha', color: 'bg-emerald-400',text: 'text-emerald-700',desc: 'Water + Earth · Stability & Immunity',    emoji: '🌿' },
}

export function calculateDoshas(answers) {
  let v = 0, p = 0, k = 0

  const map = {
    sleep:     { poor: ['vata',3], deep: ['kapha',3], light: ['pitta',2] },
    digestion: { irregular: ['vata',3], acidity: ['pitta',4], slow: ['kapha',3] },
    skin:      { dry: ['vata',3], oily: ['kapha',3], sensitive: ['pitta',3] },
    energy:    { variable: ['vata',2], intense: ['pitta',3], steady: ['kapha',2] },
    stress:    { anxiety: ['vata',4], anger: ['pitta',4], withdrawal: ['kapha',3] },
    appetite:  { irregular: ['vata',3], strong: ['pitta',3], low: ['kapha',3] },
    body:      { thin: ['vata',3], medium: ['pitta',2], heavy: ['kapha',3] },
    mind:      { creative: ['vata',2], analytical: ['pitta',2], calm: ['kapha',2] },
    weather:   { cold: ['vata',2], heat: ['pitta',3], damp: ['kapha',2] },
  }

  Object.entries(answers).forEach(([key, val]) => {
    const entry = map[key]?.[val]
    if (!entry) return
    const [dosha, score] = entry
    if (dosha === 'vata')  v += score
    if (dosha === 'pitta') p += score
    if (dosha === 'kapha') k += score
  })

  const total = v + p + k || 1
  const scores = { vata: Math.round((v/total)*100), pitta: Math.round((p/total)*100), kapha: Math.round((k/total)*100) }
  const dominant = Object.entries(scores).sort((a,b) => b[1]-a[1])[0][0]
  const risk = scores[dominant] >= 50 ? 'High' : scores[dominant] >= 35 ? 'Moderate' : 'Low'

  return { scores, dominant, risk }
}

export const RISK_COLORS = {
  High:     'text-red-600 bg-red-50 border-red-200',
  Moderate: 'text-amber-600 bg-amber-50 border-amber-200',
  Low:      'text-emerald-600 bg-emerald-50 border-emerald-200',
}
