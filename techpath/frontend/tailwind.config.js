/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#EEEDFE',
          100: '#CECBF6',
          200: '#AFA9EC',
          500: '#7F77DD',
          600: '#534AB7',
          700: '#3C3489',
          900: '#26215C',
        },
        ink: {
          900: '#0b0b12',
          800: '#151521',
          700: '#1d1d2b',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
};
