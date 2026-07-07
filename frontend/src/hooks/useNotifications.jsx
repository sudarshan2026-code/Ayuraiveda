import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { notificationService } from '../services/pocketbase.js'
import pb from '../services/pocketbase.js'

const NotificationContext = createContext(null)

export function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([])
  const [pbReady, setPbReady] = useState(false)

  const userId = pb.authStore.isValid ? pb.authStore.model?.id : null

  // Load notifications from PocketBase when user is logged in
  const loadNotifications = useCallback(async () => {
    if (!userId) { setNotifications([]); return }
    try {
      const records = await notificationService.getByUser(userId)
      setNotifications(records.map(r => ({
        id: r.id,
        title: r.title,
        body: r.message,
        time: formatTime(r.created),
        read: r.is_read,
      })))
      setPbReady(true)
    } catch {
      // PocketBase not running — use local state silently
      setPbReady(false)
    }
  }, [userId])

  useEffect(() => {
    loadNotifications()
  }, [loadNotifications])

  // Real-time subscription
  useEffect(() => {
    if (!userId || !pbReady) return
    notificationService.subscribe(userId, () => loadNotifications())
    return () => notificationService.unsubscribe()
  }, [userId, pbReady, loadNotifications])

  // Sync when auth changes
  useEffect(() => {
    const unsub = pb.authStore.onChange(() => loadNotifications())
    return () => unsub()
  }, [loadNotifications])

  const unreadCount = notifications.filter(n => !n.read).length

  const markAllRead = async () => {
    if (userId && pbReady) {
      await notificationService.markAllRead(userId).catch(() => {})
    }
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
  }

  const addNotification = async ({ title, body }) => {
    const local = { id: Date.now(), title, body, time: 'Just now', read: false }
    setNotifications(prev => [local, ...prev])
    if (userId && pbReady) {
      try {
        await notificationService.create({ userId, title, message: body })
        await loadNotifications()
      } catch { /* offline — local only */ }
    }
  }

  return (
    <NotificationContext.Provider value={{ notifications, unreadCount, markAllRead, addNotification }}>
      {children}
    </NotificationContext.Provider>
  )
}

export const useNotifications = () => useContext(NotificationContext)

function formatTime(isoString) {
  if (!isoString) return 'Just now'
  const diff = (Date.now() - new Date(isoString).getTime()) / 1000
  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}
