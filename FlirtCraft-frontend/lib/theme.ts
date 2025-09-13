import { extendTheme } from 'native-base';

// Orange-based color system as specified in design documentation
export const colors = {
  primary: {
    50: '#FFF5E6',
    100: '#FFE4B8',
    200: '#FFD38A',
    300: '#FDBA74', // Primary Light
    400: '#FB923C',
    500: '#F97316', // Primary
    600: '#EA580C',
    700: '#C2410C', // Primary Dark
    800: '#9A3412',
    900: '#7C2D12',
  },
  secondary: {
    50: '#FEF7F0',
    100: '#FEEEE0',
    200: '#FEDCC7',
    300: '#F9A8D4', // Secondary Light
    400: '#FB9A3C',
    500: '#E65100', // Secondary
    600: '#D84315',
    700: '#BF360C',
    800: '#A5300A',
    900: '#8B2508',
  },
  success: {
    500: '#10B981', // Green difficulty
  },
  warning: {
    500: '#F59E0B', // Yellow difficulty
  },
  error: {
    500: '#EF4444', // Red difficulty
  },
  info: {
    500: '#3B82F6',
  },
  // Neutral palette
  gray: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827',
  },
};

// Custom theme extending NativeBase
const theme = extendTheme({
  colors,
  space: {
    '0.5': 2,  // xs
    '1': 4,    // sm
    '2': 8,    // md
    '3': 12,   // lg
    '4': 16,   // xl
    '6': 24,   // 2xl
    '8': 32,   // 3xl
    '12': 48,  // 4xl
    '16': 64,  // 5xl
  },
  fontSizes: {
    '2xs': 10,
    'xs': 12,
    'sm': 14,
    'md': 16,
    'lg': 18,
    'xl': 20,
    '2xl': 24,
    '3xl': 28,
    '4xl': 32,
    '5xl': 36,
  },
  fontWeights: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeights: {
    '2xs': 14,
    'xs': 16,
    'sm': 20,
    'md': 22,
    'lg': 26,
    'xl': 28,
    '2xl': 32,
    '3xl': 36,
    '4xl': 40,
    '5xl': 44,
  },
  components: {
    Button: {
      defaultProps: {
        size: 'md',
        colorScheme: 'primary',
      },
      sizes: {
        lg: {
          px: 6,
          py: 4,
          fontSize: 'lg',
          _text: {
            fontSize: 'lg',
            fontWeight: 'semibold',
          },
        },
        md: {
          px: 5,
          py: 3,
          fontSize: 'md',
          _text: {
            fontSize: 'md',
            fontWeight: 'semibold',
          },
        },
        sm: {
          px: 4,
          py: 2,
          fontSize: 'sm',
          _text: {
            fontSize: 'sm',
            fontWeight: 'medium',
          },
        },
      },
      variants: {
        solid: {
          borderRadius: 12,
          shadow: 1,
          _pressed: {
            opacity: 0.8,
            transform: [{ scale: 0.98 }],
          },
        },
        outline: {
          borderRadius: 12,
          borderWidth: 2,
          _pressed: {
            opacity: 0.8,
            transform: [{ scale: 0.98 }],
          },
        },
        ghost: {
          borderRadius: 12,
          _pressed: {
            opacity: 0.8,
            bg: 'primary.100',
          },
        },
      },
    },
    Input: {
      defaultProps: {
        size: 'md',
        borderRadius: 8,
        borderWidth: 2,
        borderColor: 'gray.200',
        _focus: {
          borderColor: 'primary.500',
          shadow: 1,
        },
        _invalid: {
          borderColor: 'error.500',
        },
      },
      sizes: {
        md: {
          fontSize: 'md',
          py: 3,
          px: 4,
          h: 12,
        },
      },
    },
    FormControl: {
      defaultProps: {},
    },
    Text: {
      baseStyle: {
        color: 'gray.900',
      },
      variants: {
        heading1: {
          fontSize: '3xl',
          fontWeight: 'bold',
          lineHeight: '4xl',
          color: 'gray.900',
        },
        heading2: {
          fontSize: '2xl',
          fontWeight: 'semibold',
          lineHeight: '3xl',
          color: 'gray.900',
        },
        heading3: {
          fontSize: 'xl',
          fontWeight: 'semibold',
          lineHeight: '2xl',
          color: 'gray.900',
        },
        body: {
          fontSize: 'md',
          lineHeight: 'md',
          color: 'gray.700',
        },
        caption: {
          fontSize: 'sm',
          lineHeight: 'sm',
          color: 'gray.500',
        },
      },
    },
    Box: {
      defaultProps: {},
    },
  },
});

export default theme;