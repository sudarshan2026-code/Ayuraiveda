/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        olive: {
          50:  '#f7f8f0',
          100: '#eef0dc',
          200: '#d8ddb4',
          300: '#bcc585',
          400: '#a0ad5a',
          500: '#7d8c3a',
          600: '#5f6b2a',
          700: '#475120',
          800: '#333a18',
          900: '#1e2210',
        },
        sage: {
          50:  '#f4f7f2',
          100: '#e4ede0',
          200: '#c5d9be',
          300: '#9dbe93',
          400: '#74a068',
          500: '#537d48',
          600: '#3e6135',
          700: '#2f4a28',
          800: '#21341c',
          900: '#131f10',
        },
        cream: {
          50:  '#fdfcf8',
          100: '#faf7ee',
          200: '#f4edd6',
          300: '#ecdfb8',
          400: '#e0cc90',
          500: '#d0b468',
          600: '#b8944a',
          700: '#8f7038',
          800: '#644f28',
          900: '#3a2e17',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '2rem',
      },
      boxShadow: {
        soft: '0 2px 20px rgba(0,0,0,0.06)',
        card: '0 4px 30px rgba(0,0,0,0.08)',
        glow: '0 0 30px rgba(125,140,58,0.15)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
