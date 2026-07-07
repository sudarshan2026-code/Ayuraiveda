import { useTranslation } from 'react-i18next'
import { DOSHAS } from '../utils/doshaUtils'

export default function DoshaCard({ type, score, showBar = false }) {
  const { t } = useTranslation()
  const d = DOSHAS[type]

  return (
    <div className="card-hover">
      <div className="flex items-start justify-between mb-3">
        <div>
          <span className="text-2xl">{d.emoji}</span>
          <h3 className={`font-serif font-bold text-xl mt-1 ${d.text}`}>{d.label}</h3>
          <p className="text-xs text-olive-500 mt-0.5">{t(`dosha.${type}_desc`, d.desc)}</p>
        </div>
        {score !== undefined && (
          <span className={`text-2xl font-bold ${d.text}`}>{score}%</span>
        )}
      </div>
      {showBar && score !== undefined && (
        <div className="h-2 bg-cream-100 rounded-full overflow-hidden mt-3">
          <div
            className={`h-full rounded-full dosha-bar ${d.color}`}
            style={{ '--target-width': `${score}%`, width: `${score}%` }}
          />
        </div>
      )}
    </div>
  )
}
