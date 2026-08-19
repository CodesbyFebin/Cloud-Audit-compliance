/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@tremor/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        brand: {
          50: '#eef5ff',
          100: '#d9e8ff',
          200: '#bcd8ff',
          300: '#8ec0ff',
          400: '#599eff',
          500: '#3378ff',
          600: '#1b57f5',
          700: '#1443e1',
          800: '#1736b6',
          900: '#19338f',
          950: '#142057',
        },
        surface: {
          0: '#0a0b0f',
          1: '#12131a',
          2: '#1a1b24',
          3: '#22232e',
          4: '#2a2c3a',
        },
      },
    },
  },
  plugins: [],
}