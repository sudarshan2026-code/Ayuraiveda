/**
 * Opens a new window with only the report content formatted for print/PDF.
 * Works from both Assessment results and Profile report history.
 */
export function printReport({ result, userName, date }) {
  const dom = result.dominant?.split('-')[0].toLowerCase() || 'vata'

  const DOSHA_COLORS = {
    vata:  { bg: '#e0f2fe', bar: '#0ea5e9', label: 'Vata',  emoji: '🌬️' },
    pitta: { bg: '#fef3c7', bar: '#f59e0b', label: 'Pitta', emoji: '🔥' },
    kapha: { bg: '#d1fae5', bar: '#10b981', label: 'Kapha', emoji: '🌿' },
  }

  const RISK_COLORS = {
    High:     { bg: '#fee2e2', text: '#dc2626', border: '#fca5a5' },
    Moderate: { bg: '#fef3c7', text: '#d97706', border: '#fcd34d' },
    Low:      { bg: '#d1fae5', text: '#059669', border: '#6ee7b7' },
  }

  const risk = RISK_COLORS[result.risk] || RISK_COLORS.Low
  const dateStr = date
    ? new Date(date).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    : new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })

  // Dosha score bars HTML
  const doshaRows = ['vata', 'pitta', 'kapha'].map(d => {
    const score = result.scores?.[d] ?? 0
    const c = DOSHA_COLORS[d]
    return `
      <div style="margin-bottom:12px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
          <span style="font-weight:600;color:#3d4a1a;">${c.emoji} ${c.label}</span>
          <span style="font-weight:700;color:${c.bar};">${score}%</span>
        </div>
        <div style="background:#f0f0e8;border-radius:99px;height:10px;overflow:hidden;">
          <div style="width:${score}%;background:${c.bar};height:100%;border-radius:99px;"></div>
        </div>
      </div>`
  }).join('')

  // Agni / Ama / Vikriti
  const indicators = [
    { label: 'Agni', val: result.agni_state },
    { label: 'Ama',  val: result.ama_status },
    { label: 'Vikriti', val: result.vikriti },
  ].filter(i => i.val)

  const indicatorsHTML = indicators.length ? `
    <div style="display:grid;grid-template-columns:repeat(${indicators.length},1fr);gap:12px;margin-bottom:20px;">
      ${indicators.map(i => `
        <div style="background:#f7f5ec;border-radius:12px;padding:12px;text-align:center;">
          <div style="font-size:10px;color:#8a9a4a;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">${i.label}</div>
          <div style="font-weight:700;color:#3d4a1a;font-size:13px;">${i.val}</div>
        </div>`).join('')}
    </div>` : ''

  // Recommendations
  const recsHTML = result.recommendations?.length ? `
    <div style="margin-bottom:20px;">
      <div style="font-size:11px;font-weight:700;color:#8a9a4a;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">🌱 Recommendations</div>
      <ul style="margin:0;padding-left:18px;">
        ${result.recommendations.map(r => `<li style="color:#4a5a1a;font-size:13px;margin-bottom:5px;">${r}</li>`).join('')}
      </ul>
    </div>` : ''

  // Diet
  const dietHTML = result.diet_suggestions ? `
    <div style="margin-bottom:20px;">
      <div style="font-size:11px;font-weight:700;color:#8a9a4a;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">🥗 Diet Guidelines</div>
      ${result.diet_suggestions.foods_to_favor?.length ? `
        <p style="font-size:13px;color:#4a5a1a;margin-bottom:6px;">
          <strong style="color:#059669;">✅ Favor:</strong> ${result.diet_suggestions.foods_to_favor.join(' · ')}
        </p>` : ''}
      ${result.diet_suggestions.foods_to_avoid?.length ? `
        <p style="font-size:13px;color:#4a5a1a;">
          <strong style="color:#dc2626;">❌ Avoid:</strong> ${result.diet_suggestions.foods_to_avoid.join(' · ')}
        </p>` : ''}
    </div>` : ''

  // Justification
  const justHTML = result.justification ? `
    <div style="background:#f7f5ec;border-radius:12px;padding:16px;margin-bottom:20px;">
      <div style="font-size:11px;font-weight:700;color:#8a9a4a;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">🔬 Clinical Reasoning</div>
      <p style="font-size:13px;color:#4a5a1a;line-height:1.6;margin:0;">${result.justification}</p>
    </div>` : ''

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>AyurAI Veda — Prakriti Report</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #fff;
      color: #3d4a1a;
      padding: 32px;
      max-width: 720px;
      margin: 0 auto;
    }
    @media print {
      body { padding: 16px; }
      .no-print { display: none !important; }
    }
  </style>
</head>
<body>

  <!-- Header -->
  <div style="display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #c8d87a;padding-bottom:16px;margin-bottom:24px;">
    <div>
      <div style="font-size:22px;font-weight:800;color:#3d4a1a;font-family:Georgia,serif;">
        AyurAI<span style="color:#7d8c3a;">Veda</span>
      </div>
      <div style="font-size:11px;color:#8a9a4a;margin-top:2px;">Tridosha Intelligence Engine · Clinical Prakriti Report</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:11px;color:#8a9a4a;">Generated on</div>
      <div style="font-size:12px;font-weight:600;color:#3d4a1a;">${dateStr}</div>
    </div>
  </div>

  <!-- Patient info -->
  ${userName ? `
  <div style="background:#f7f5ec;border-radius:12px;padding:14px 18px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div style="font-size:11px;color:#8a9a4a;text-transform:uppercase;letter-spacing:1px;">Patient</div>
      <div style="font-size:16px;font-weight:700;color:#3d4a1a;margin-top:2px;">${userName}</div>
    </div>
    <div style="font-size:28px;">${DOSHA_COLORS[dom]?.emoji || '🌿'}</div>
  </div>` : ''}

  <!-- Prakriti result -->
  <div style="text-align:center;margin-bottom:24px;padding:20px;border-radius:16px;background:linear-gradient(135deg,#f4f7f2,#eef0dc);">
    <div style="font-size:13px;color:#8a9a4a;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;">Dominant Prakriti</div>
    <div style="font-size:32px;font-weight:800;color:#3d4a1a;font-family:Georgia,serif;">${result.dominant || 'Unknown'}</div>
    <div style="display:inline-block;margin-top:10px;padding:6px 18px;border-radius:99px;font-size:13px;font-weight:700;
      background:${risk.bg};color:${risk.text};border:1.5px solid ${risk.border};">
      ${result.risk || '—'} Imbalance Risk
    </div>
  </div>

  <!-- Dosha scores -->
  <div style="margin-bottom:20px;">
    <div style="font-size:11px;font-weight:700;color:#8a9a4a;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">Dosha Balance</div>
    ${doshaRows}
  </div>

  <!-- Indicators -->
  ${indicatorsHTML}

  <!-- Justification -->
  ${justHTML}

  <!-- Recommendations -->
  ${recsHTML}

  <!-- Diet -->
  ${dietHTML}

  <!-- Footer -->
  <div style="border-top:1px solid #e8edcc;padding-top:14px;margin-top:24px;display:flex;justify-content:space-between;align-items:center;">
    <div style="font-size:10px;color:#aab87a;">
      ⚠️ Educational &amp; preventive insights only. Not a substitute for medical advice.
    </div>
    <div style="font-size:10px;color:#aab87a;">AyurAI Veda · Ananta Labs India</div>
  </div>

  <!-- Print button (hidden when printing) -->
  <div class="no-print" style="text-align:center;margin-top:24px;">
    <button onclick="window.print()" style="background:#5f6b2a;color:#fff;border:none;padding:12px 32px;border-radius:12px;font-size:14px;font-weight:600;cursor:pointer;">
      🖨️ Save as PDF / Print
    </button>
  </div>

</body>
</html>`

  const win = window.open('', '_blank', 'width=800,height=900')
  win.document.write(html)
  win.document.close()
  win.focus()
}
