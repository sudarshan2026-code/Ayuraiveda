import { useTranslation } from 'react-i18next'
import MsmeBadge from '../components/MsmeBadge'

const TIMELINE_YEARS = ['2024', '2024', '2025', '2025+']

export default function About() {
  const { t } = useTranslation()

  const PILLARS = [
    { icon: '🧬', titleKey: 'about.pillar1_title', descKey: 'about.pillar1_desc' },
    { icon: '📚', titleKey: 'about.pillar2_title', descKey: 'about.pillar2_desc' },
    { icon: '🎓', titleKey: 'about.pillar3_title', descKey: 'about.pillar3_desc' },
    { icon: '🔬', titleKey: 'about.pillar4_title', descKey: 'about.pillar4_desc' },
  ]

  const TIMELINE = TIMELINE_YEARS.map((year, i) => ({
    year,
    eventKey: `about.timeline_${i + 1}`,
  }))

  const FUTURE = [1, 2, 3, 4, 5, 6].map(i => `about.future_${i}`)

  return (
    <div className="max-w-4xl mx-auto px-4 md:px-8 py-8 md:py-10">

      {/* Header */}
      <div className="text-center mb-10 md:mb-14 page-enter">
        <MsmeBadge className="mb-4 md:mb-5 mx-auto" />
        <h1 className="section-title mb-3 md:mb-4">{t('about.title')}</h1>
        <p className="text-olive-600 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
          {t('about.subtitle')}
        </p>
      </div>

      {/* Mission */}
      <div className="gradient-olive rounded-3xl p-6 md:p-8 lg:p-12 text-white mb-10 md:mb-12 shadow-glow">
        <p className="text-olive-300 text-xs font-semibold uppercase tracking-widest mb-3">
          {t('about.mission_label')}
        </p>
        <h2 className="font-serif text-xl md:text-2xl lg:text-3xl font-bold mb-3 md:mb-4 leading-snug">
          {t('about.mission_quote')}
        </h2>
        <p className="text-olive-200 leading-relaxed text-sm md:text-base">
          {t('about.mission_desc')}
        </p>
      </div>

      {/* Pillars */}
      <section className="mb-10 md:mb-14">
        <h2 className="section-title text-center mb-8 md:mb-10">{t('about.pillars_title')}</h2>
        <div className="grid sm:grid-cols-2 gap-4 md:gap-6">
          {PILLARS.map(p => (
            <div key={p.titleKey} className="card-hover">
              <span className="text-2xl md:text-3xl">{p.icon}</span>
              <h3 className="font-semibold text-olive-800 text-base md:text-lg mt-3 mb-2">{t(p.titleKey)}</h3>
              <p className="text-olive-500 text-sm leading-relaxed">{t(p.descKey)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Engine */}
      <section className="mb-10 md:mb-14">
        <div className="card">
          <h2 className="font-serif text-xl md:text-2xl font-bold text-olive-800 mb-4">
            {t('about.engine_title')}
          </h2>
          <p className="text-olive-600 text-sm leading-relaxed mb-5">
            {t('about.engine_desc')}
          </p>
          <div className="bg-olive-900 rounded-2xl p-4 md:p-5 font-mono text-xs md:text-sm text-olive-200 overflow-x-auto">
            <pre className="whitespace-pre-wrap break-words">{`# Tridosha Scoring Logic
if sleep == 'poor':      vata_score  += 3
if digestion == 'acidity': pitta_score += 4
if skin == 'oily':       kapha_score += 3

total = vata + pitta + kapha
vata_pct = (vata / total) * 100

# Risk Classification
if dominant >= 50%: risk = 'High'
elif dominant >= 35%: risk = 'Moderate'
else: risk = 'Low'`}</pre>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="mb-10 md:mb-14">
        <h2 className="section-title text-center mb-8 md:mb-10">{t('about.journey_title')}</h2>
        <div className="relative pl-7 md:pl-8 border-l-2 border-olive-200 space-y-6 md:space-y-8">
          {TIMELINE.map((item, i) => (
            <div key={i} className="relative">
              <div className="absolute -left-[2.1rem] md:-left-[2.35rem] w-4 h-4 rounded-full bg-olive-500 border-4 border-cream-50" />
              <p className="text-xs font-bold text-olive-500 uppercase tracking-wider mb-1">{item.year}</p>
              <p className="text-olive-800 font-medium text-sm md:text-base">{t(item.eventKey)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Future */}
      <section className="mb-8 md:mb-10">
        <div className="card bg-cream-50 border border-cream-200">
          <h2 className="font-serif text-xl md:text-2xl font-bold text-olive-800 mb-4">{t('about.future_title')}</h2>
          <div className="grid sm:grid-cols-2 gap-2 md:gap-3">
            {FUTURE.map(key => (
              <div key={key} className="flex items-start gap-2 text-sm text-olive-700">
                <span className="text-olive-400 mt-0.5 shrink-0">→</span>
                {t(key)}
              </div>
            ))}
          </div>
        </div>
      </section>

      <p className="text-center text-xs text-olive-400">{t('about.footer')}</p>
    </div>
  )
}
