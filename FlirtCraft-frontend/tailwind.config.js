/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
    './features/**/*.{js,jsx,ts,tsx}',
    './hooks/**/*.{js,jsx,ts,tsx}',
    './stores/**/*.{js,jsx,ts,tsx}',
    './utils/**/*.{js,jsx,ts,tsx}',
  ],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        // Primary Colors (Orange-based brand palette)
        primary: {
          50: '#FFF7ED',
          100: '#FFEDD5',
          200: '#FED7AA',
          300: '#FDBA74',
          400: '#FB923C',
          500: '#F97316', // Main brand color
          600: '#EA580C',
          700: '#C2410C', // Primary dark
          800: '#9A3412',
          900: '#7C2D12',
        },
        // Secondary Colors (Orange Complements)
        secondary: {
          50: '#FEF7F0',   // Warm cream
          100: '#FEEEE0',  // Light peach
          200: '#FEDCC7',  // Soft peach
          300: '#FDBA8C',  // Warm peach
          400: '#FB9A3C',  // Rich orange
          500: '#E65100',  // Deep orange secondary
          600: '#D84315',  // Dark orange
          700: '#BF360C',  // Deep rust
          800: '#A5300A',  // Dark rust
          900: '#8B2508'   // Darkest rust
        },
        // Semantic Colors
        success: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          500: '#10B981',
          600: '#059669',
          700: '#047857',
        },
        warning: {
          50: '#FFFBEB',
          100: '#FEF3C7',
          500: '#F59E0B',
          600: '#D97706',
          700: '#B45309',
        },
        error: {
          50: '#FEF2F2',
          100: '#FEE2E2',
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
        },
        info: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
        },
        // Warm Neutral System
        neutral: {
          50: '#FEFAF8',   // Warm white
          100: '#FDF7F3',  // Cream white
          200: '#F9F0EA',  // Light cream
          300: '#F1E5DA',  // Soft beige
          400: '#E6D3C4',  // Warm beige
          500: '#D4BBA6',  // Medium warm grey
          600: '#B8956F',  // Warm brown
          700: '#8E6B47',  // Deep warm brown
          800: '#6B4423',  // Dark brown
          900: '#4A2818'   // Darkest brown
        },
        // Difficulty Level Colors
        difficulty: {
          green: '#10B981',
          yellow: '#F59E0B',
          red: '#EF4444',
        },
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      spacing: {
        '0.5': '2px',
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '6': '24px',
        '8': '32px',
        '12': '48px',
        '16': '64px',
      },
      fontSize: {
        '2xs': ['10px', { lineHeight: '14px' }],
        'xs': ['12px', { lineHeight: '16px' }],
        'sm': ['14px', { lineHeight: '20px' }],
        'base': ['16px', { lineHeight: '22px' }],
        'lg': ['18px', { lineHeight: '26px' }],
        'xl': ['20px', { lineHeight: '28px' }],
        '2xl': ['24px', { lineHeight: '32px' }],
        '3xl': ['28px', { lineHeight: '36px' }],
        '4xl': ['32px', { lineHeight: '40px' }],
        '5xl': ['36px', { lineHeight: '44px' }],
      },
      borderRadius: {
        'xs': '4px',
        'sm': '6px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        '2xl': '20px',
      },
      boxShadow: {
        'sm': '0 1px 2px rgba(0, 0, 0, 0.05)',
        'md': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'lg': '0 4px 14px rgba(99, 102, 241, 0.25)',
        'xl': '0 8px 24px rgba(0, 0, 0, 0.15)',
      },
      animation: {
        'fade-in': 'fadeIn 300ms ease-out',
        'slide-in-right': 'slideInRight 300ms ease-out',
        'slide-in-left': 'slideInLeft 300ms ease-out',
        'scale-in': 'scaleIn 200ms ease-out',
        'bounce-gentle': 'bounceGentle 400ms ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },
    },
  },
  plugins: [],
};