import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import DoshaCard from '../components/DoshaCard'
import MsmeBadge from '../components/MsmeBadge'

export default function Home() {
  const { t } = useTranslation()

  const FEATURES = [
    { icon: '🧬', titleKey: 'home.feat1_title', descKey: 'home.feat1_desc' },
    { icon: '🌿', titleKey: 'home.feat2_title', descKey: 'home.feat2_desc' },
    { icon: '📊', titleKey: 'home.feat3_title', descKey: 'home.feat3_desc' },
    { icon: '🔒', titleKey: 'home.feat4_title', descKey: 'home.feat4_desc' },
  ]

  const STEPS = [
    { step: '01', titleKey: 'home.step1_title', descKey: 'home.step1_desc' },
    { step: '02', titleKey: 'home.step2_title', descKey: 'home.step2_desc' },
    { step: '03', titleKey: 'home.step3_title', descKey: 'home.step3_desc' },
  ]

  const TAGS = [
    { key: 'home.tag_nep' },
    { key: 'home.tag_iks' },
    { key: 'home.tag_ai' },
    { key: 'home.tag_msme' },
    { key: 'home.tag_privacy' },
  ]

  return (
    <div className="max-w-6xl mx-auto px-4 md:px-8">

      {/* Hero */}
      <section className="pt-10 pb-14 md:pt-16 md:pb-20 text-center">
        <MsmeBadge className="mb-5 mx-auto" />

        <h1 className="font-serif text-3xl md:text-5xl lg:text-6xl font-bold text-olive-900 leading-tight mb-4">
          {t('home.hero_title_1')}<br />
          <span className="text-gradient">{t('home.hero_title_2')}</span>
        </h1>

        <p className="text-olive-600 text-base md:text-lg lg:text-xl max-w-2xl mx-auto leading-relaxed mb-7 px-2">
          {t('home.hero_desc')}
        </p>

        <div className="flex flex-col sm:flex-row gap-3 justify-center px-2">
          <Link to="/assessment" className="btn-primary text-base px-7 py-3.5">
            {t('home.cta_primary')}
          </Link>
          <Link to="/about" className="btn-secondary text-base px-7 py-3.5">
            {t('home.cta_secondary')}
          </Link>
        </div>

        {/* Hero visual */}
        <div className="mt-10 md:mt-14 relative">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-cream-50 z-10 pointer-events-none rounded-3xl" />
          <div className="glass rounded-3xl p-5 md:p-8 lg:p-12 shadow-card max-w-3xl mx-auto">
            <div className="grid grid-cols-3 gap-3 md:gap-4">
              {['vata', 'pitta', 'kapha'].map(d => (
                <DoshaCard key={d} type={d} />
              ))}
            </div>
            <div className="mt-4 md:mt-6 pt-4 md:pt-6 border-t border-cream-200 flex items-center justify-center gap-2">
              <div className="w-2 h-2 rounded-full bg-olive-400 animate-pulse" />
              <span className="text-xs md:text-sm text-olive-600 font-medium text-center">{t('home.engine_active')}</span>
            </div>
          </div>
        </div>
      </section>

      <section className="py-12 md:py-16">
        <p className="text-xs font-semibold text-olive-500 uppercase tracking-widest text-center mb-2">
          {t('home.how_title')}
        </p>
        <h2 className="section-title text-center mb-8 md:mb-12">{t('home.how_subtitle')}</h2>
        <div className="grid md:grid-cols-3 gap-4 md:gap-6">
          {STEPS.map(s => (
            <div key={s.step} className="card text-center">
              <span className="text-4xl md:text-5xl font-serif font-bold text-olive-100">{s.step}</span>
              <h3 className="font-semibold text-olive-800 text-base md:text-lg mt-2 mb-2">{t(s.titleKey)}</h3>
              <p className="text-olive-500 text-sm leading-relaxed">{t(s.descKey)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="py-12 md:py-16">
        <p className="text-xs font-semibold text-olive-500 uppercase tracking-widest text-center mb-2">
          {t('home.features_label')}
        </p>
        <h2 className="section-title text-center mb-8 md:mb-12">{t('home.features_title')}</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
          {FEATURES.map(f => (
            <div key={f.titleKey} className="card-hover text-center">
              <span className="text-2xl md:text-3xl">{f.icon}</span>
              <h3 className="font-semibold text-olive-800 text-sm md:text-base mt-3 mb-2">{t(f.titleKey)}</h3>
              <p className="text-olive-500 text-xs md:text-sm leading-relaxed">{t(f.descKey)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Banner */}
      <section className="py-12 md:py-16">
        <div className="gradient-olive rounded-3xl p-8 md:p-10 lg:p-14 text-center text-white shadow-glow">
          <h2 className="font-serif text-2xl md:text-3xl lg:text-4xl font-bold mb-3 md:mb-4">
            {t('home.cta_banner_title')}
          </h2>
          <p className="text-olive-200 text-base md:text-lg mb-6 md:mb-8 max-w-xl mx-auto">
            {t('home.cta_banner_desc')}
          </p>
          <Link to="/assessment" className="inline-block bg-white text-olive-700 font-bold px-7 py-3.5 rounded-2xl hover:bg-cream-50 transition-colors shadow-soft">
            {t('home.cta_banner_btn')}
          </Link>
        </div>
      </section>

      {/* Tags */}
      <section className="py-10 text-center">
        <div className="inline-flex flex-wrap justify-center gap-3">
          {TAGS.map(tag => (
            <span key={tag.key} className="badge bg-olive-50 text-olive-700 border border-olive-200">
              ✓ {t(tag.key)}
            </span>
          ))}
        </div>
        <p className="text-olive-400 text-xs mt-4">
          {t('home.footer_copy', { year: new Date().getFullYear() })}
        </p>
      </section>

    </div>
  )
}
