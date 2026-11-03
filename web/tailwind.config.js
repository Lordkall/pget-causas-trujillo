/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        vinotinto: {
          DEFAULT: '#6B1226',
          dark: '#4A0C1A',
          light: '#8B1832',
        },
        oro: {
          DEFAULT: '#D4AF37',
          light: '#F4D068',
          dark: '#AA8822',
        },
      },
    },
  },
  plugins: [],
};

