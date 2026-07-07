export default function MsmeBadge({ className = '' }) {
  return (
    <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-olive-50 border border-olive-200 ${className}`}>
      <span className="text-olive-600 text-lg">🏛️</span>
      <div>
        <p className="text-[10px] text-olive-500 font-medium uppercase tracking-wider">Govt. Registered</p>
        <p className="text-xs text-olive-700 font-semibold">MSME · Ananta Labs India</p>
      </div>
    </div>
  )
}
