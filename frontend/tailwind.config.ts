import type { Config } from 'tailwindcss'

export default {
  content: [
    "./components/**/*.{ts,tsx}",
		"./src/**/*.{ts,tsx}",
  ],
  prefix: "",
  theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
    extend: {
      fontFamily: {
        sansation: ['Sansation', 'sans-serif'],
        manrope: ['Manrope', 'sans-serif'],
        'lisu-bosa': ['"Lisu Bosa"', 'serif']
      },
      colors: {
        background: "#2775A7",
        foreground: "#EAF7FF",
        text: {
          DEFAULT: "#002169",
          warning_low: "#685000",
          warning_high: "#680000",
          accent: "#7053C8",
          secondary: "#484848"
        },
        warning_low: {
          DEFAULT: "#E3D87E",
          border: "#8F8427",
        },
        warning_high: {
          DEFAULT: "#E37E7E",
          border: "#8F2727",
        }
      }
    }
  },
  plugins: [],
} satisfies Config