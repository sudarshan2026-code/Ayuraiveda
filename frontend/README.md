# AyurAI Veda™ — React Frontend

Modern React frontend for the AyurAI Veda™ platform.

## Tech Stack
- **React 18** + **Vite 5**
- **Tailwind CSS 3** — custom Ayurvedic color palette
- **React Router 6** — client-side routing

## Folder Structure
```
src/
├── components/       # Reusable UI components
│   ├── Navbar.jsx
│   ├── BottomNav.jsx
│   ├── NotificationBell.jsx
│   ├── DoshaCard.jsx
│   └── MsmeBadge.jsx
├── pages/            # Route-level pages
│   ├── Home.jsx
│   ├── Assessment.jsx
│   ├── About.jsx
│   ├── Contact.jsx
│   ├── Login.jsx
│   └── Register.jsx
├── layouts/
│   └── MainLayout.jsx
├── hooks/
│   ├── useAuth.js
│   └── useNotifications.js
├── services/
│   └── api.js        # Flask backend API calls
├── utils/
│   └── doshaUtils.js # Dosha scoring logic
└── assets/
```

## Setup

### Prerequisites
- Node.js 18+ and npm

### Install & Run
```bash
cd frontend
npm install
npm run dev
```

App runs at: http://localhost:3000

### Build for Production
```bash
npm run build
```

### APK Conversion (Capacitor)
```bash
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init
npm run build
npx cap add android
npx cap sync
npx cap open android
```

## Backend Proxy
Vite proxies `/api/*` requests to `http://127.0.0.1:5000` (Flask backend).
Make sure the Flask server is running before using assessment features.

## Pages
| Route | Page |
|-------|------|
| `/` | Home |
| `/assessment` | Clinical Assessment |
| `/about` | About |
| `/contact` | Contact |
| `/login` | Login (User / Doctor / College) |
| `/register` | Register |
