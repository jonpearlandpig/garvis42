/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        tt: {
          blue: '#3B82F6',
          dark: '#0F172A',
          card: '#1E293B',
          border: '#334155',
          muted: '#94A3B8',
        },
      },
    },
  },
  plugins: [],
}
