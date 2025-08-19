/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.{html,js}",
    "./*/templates/**/*.{html,js}", 
    "./static/js/**/*.js",
    "./*.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        lexend: ['Lexend', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}