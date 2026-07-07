// Membership management — localStorage-first, PocketBase-synced
// Membership stored as: { userId, name, email, role, active, expiry, activatedAt, activatedBy }

const STORE_KEY = 'ayur_memberships'
const USAGE_KEY = 'ayur_usage'
const MEMBERSHIP_PRICE = 999 // INR per 3 months

export function getMemberships() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY) || '[]') } catch { return [] }
}

export function saveMemberships(list) {
  localStorage.setItem(STORE_KEY, JSON.stringify(list))
}

export function getMembership(userId) {
  return getMemberships().find(m => m.userId === userId) || null
}

export function isMembershipActive(userId) {
  const m = getMembership(userId)
  if (!m || !m.active) return false
  return new Date(m.expiry) > new Date()
}

export function activateMembership(userId, userName, userEmail, userRole) {
  const list = getMemberships()
  const now = new Date()
  const expiry = new Date(now)
  expiry.setMonth(expiry.getMonth() + 3)

  const existing = list.findIndex(m => m.userId === userId)
  const record = {
    userId, name: userName, email: userEmail, role: userRole,
    active: true,
    activatedAt: now.toISOString(),
    expiry: expiry.toISOString(),
    revenue: MEMBERSHIP_PRICE,
  }
  if (existing >= 0) list[existing] = record
  else list.push(record)
  saveMemberships(list)
  return record
}

export function deactivateMembership(userId) {
  const list = getMemberships().map(m =>
    m.userId === userId ? { ...m, active: false } : m
  )
  saveMemberships(list)
}

// ── Usage tracking (free trial) ──────────────────────────────────────────────
export function getUsage(userId) {
  try {
    const all = JSON.parse(localStorage.getItem(USAGE_KEY) || '{}')
    return all[userId] || { assessments: 0 }
  } catch { return { assessments: 0 } }
}

export function incrementUsage(userId) {
  const all = JSON.parse(localStorage.getItem(USAGE_KEY) || '{}')
  all[userId] = { assessments: (all[userId]?.assessments || 0) + 1 }
  localStorage.setItem(USAGE_KEY, JSON.stringify(all))
}

export function canTakeAssessment(userId) {
  if (!userId) return { allowed: true, isFree: true } // guest — allow 1
  if (isMembershipActive(userId)) return { allowed: true, isFree: false }
  const usage = getUsage(userId)
  return { allowed: usage.assessments < 1, isFree: true }
}

export function getTotalRevenue() {
  return getMemberships()
    .filter(m => m.active && new Date(m.expiry) > new Date())
    .reduce((sum, m) => sum + (m.revenue || MEMBERSHIP_PRICE), 0)
}

export { MEMBERSHIP_PRICE }
