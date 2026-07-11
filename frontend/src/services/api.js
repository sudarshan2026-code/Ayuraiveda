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

// Analyze clinical image — calls Flask AI computer vision backend
export async function analyzeClinicalImage(imageData) {
  const res = await fetch(`${API_BASE_URL}/analyze-clinical-image`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageData }),
  })
  if (!res.ok) throw new Error('Image analysis failed')
  return res.json()
}
