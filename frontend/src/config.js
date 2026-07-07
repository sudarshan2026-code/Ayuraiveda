// Dynamic configuration resolving correct API and DB URLs for web vs native mobile APK environments
const isNative = window.location.protocol === 'file:' || 
                 (window.location.hostname === 'localhost' && !window.location.port) || 
                 !!window.Capacitor;

// Flask backend base URL
export const API_BASE_URL = isNative
  ? (import.meta.env.VITE_API_BASE_URL || 'https://ayuraiveda.vercel.app')
  : '';

// PocketBase database base URL
export const POCKETBASE_URL = isNative
  ? (import.meta.env.VITE_POCKETBASE_URL || 'https://ayuraiveda-pocketbase.up.railway.app')
  : (import.meta.env.VITE_POCKETBASE_URL || 'http://127.0.0.1:8090');
