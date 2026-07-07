import PocketBase from 'pocketbase'
import { POCKETBASE_URL } from '../config'

// ── Singleton PocketBase client ──────────────────────────────────────────────
const pb = new PocketBase(POCKETBASE_URL)

// Keep auth store in sync with localStorage automatically (PocketBase does this)
pb.autoCancellation(false)

export default pb

// ── Auth ─────────────────────────────────────────────────────────────────────
export const authService = {
  /** Register a new user */
  async register({ name, email, password, role = 'user' }) {
    const record = await pb.collection('users').create({
      name,
      email,
      password,
      passwordConfirm: password,
      role,
    })
    // Auto-login after register
    await pb.collection('users').authWithPassword(email, password)
    return record
  },

  /** Login with email + password */
  async login({ email, password }) {
    const auth = await pb.collection('users').authWithPassword(email, password)
    return auth.record
  },

  /** Logout */
  logout() {
    pb.authStore.clear()
  },

  /** Current logged-in user record */
  get currentUser() {
    return pb.authStore.isValid ? pb.authStore.model : null
  },

  /** Is authenticated */
  get isLoggedIn() {
    return pb.authStore.isValid
  },

  /** Update profile fields */
  async updateProfile(userId, data) {
    return pb.collection('users').update(userId, data)
  },

  /** Send password reset email */
  async forgotPassword(email) {
    return pb.collection('users').requestPasswordReset(email)
  },
}

// ── Clinical Assessments ─────────────────────────────────────────────────────
export const assessmentService = {
  /** Save a completed assessment */
  async save({ userId, answers, result }) {
    return pb.collection('clinical_assessments').create({
      user_id: userId,
      assessment_answers: answers,
      dosha_result: result.dominant,
      ai_analysis: JSON.stringify(result),
      report_status: 'completed',
    })
  },

  /** Get all assessments for a user */
  async getByUser(userId) {
    return pb.collection('clinical_assessments').getFullList({
      filter: `user_id = "${userId}"`,
      sort: '-created',
    })
  },

  /** Get single assessment */
  async getById(id) {
    return pb.collection('clinical_assessments').getOne(id)
  },
}

// ── Notifications ─────────────────────────────────────────────────────────────
export const notificationService = {
  /** Get notifications for a user */
  async getByUser(userId) {
    return pb.collection('notifications').getFullList({
      filter: `user_id = "${userId}"`,
      sort: '-created',
    })
  },

  /** Create a notification */
  async create({ userId, title, message }) {
    return pb.collection('notifications').create({
      user_id: userId,
      title,
      message,
      is_read: false,
    })
  },

  /** Mark a notification as read */
  async markRead(id) {
    return pb.collection('notifications').update(id, { is_read: true })
  },

  /** Mark all as read for a user */
  async markAllRead(userId) {
    const unread = await pb.collection('notifications').getFullList({
      filter: `user_id = "${userId}" && is_read = false`,
    })
    return Promise.all(unread.map(n => pb.collection('notifications').update(n.id, { is_read: true })))
  },

  /** Subscribe to real-time notifications */
  subscribe(userId, callback) {
    pb.collection('notifications').subscribe('*', (e) => {
      if (e.record.user_id === userId) callback(e)
    })
  },

  unsubscribe() {
    pb.collection('notifications').unsubscribe('*')
  },
}

// ── Doctors ───────────────────────────────────────────────────────────────────
export const doctorService = {
  async getAll() {
    return pb.collection('doctors').getFullList({ sort: 'doctor_name' })
  },

  async getById(id) {
    return pb.collection('doctors').getOne(id)
  },

  async upsert(userId, data) {
    // Check if doctor profile exists
    try {
      const existing = await pb.collection('doctors').getFirstListItem(`user_id = "${userId}"`)
      return pb.collection('doctors').update(existing.id, data)
    } catch {
      return pb.collection('doctors').create({ ...data, user_id: userId })
    }
  },
}
