import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://127.0.0.1:5000',
      '/clinical-analyze': 'http://127.0.0.1:5000',
      '/analyze-clinical-image': 'http://127.0.0.1:5000',
      '/download-report': 'http://127.0.0.1:5000',
      '/contact-email': 'http://127.0.0.1:5000'
    }
  }
})
