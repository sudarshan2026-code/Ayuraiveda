import { API_BASE_URL } from '../config'

// Clinical assessment — calls Flask AI backend
export async function submitAssessment(formData) {
  const res = await fetch(`${API_BASE_URL}/clinical-analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  })
  if (!res.ok) throw new Error('Assessment failed')
  return res.json()
}
