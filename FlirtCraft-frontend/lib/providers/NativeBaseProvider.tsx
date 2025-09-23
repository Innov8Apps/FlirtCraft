import React, { ReactNode } from 'react';
import { NativeBaseProvider, extendTheme } from 'native-base';
import { Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

// FlirtCraft custom theme
const theme = extendTheme({
  colors: {
    primary: {
      50: '#fef5e7',
      100: '#fde6c1',
      200: '#fbcf8a',
      300: '#f9b653',
      400: '#f7a41c',
      500: '#f59e0b', // Main brand color
      600: '#d97706',
      700: '#b45309',
      800: '#92400e',
      900: '#78350f',
    },
    secondary: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a',
    },
    success: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d',
    },
    warning: {
      50: '#fffbeb',
      100: '#fef3c7',
      200: '#fde68a',
      300: '#fcd34d',
      400: '#fbbf24',
      500: '#f59e0b',
      600: '#d97706',
      700: '#b45309',
      800: '#92400e',
      900: '#78350f',
    },
    error: {
      50: '#fef2f2',
      100: '#fee2e2',
      200: '#fecaca',
      300: '#fca5a5',
      400: '#f87171',
      500: '#ef4444',
      600: '#dc2626',
      700: '#b91c1c',
      800: '#991b1b',
      900: '#7f1d1d',
    },
  },
  fonts: {
    heading: 'Inter_600SemiBold',
    body: 'Inter_400Regular',
    mono: 'Courier',
  },
  fontSizes: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
    '5xl': 48,
    '6xl': 60,
  },
  space: {
    px: 1,
    0.5: 2,
    1: 4,
    1.5: 6,
    2: 8,
    2.5: 10,
    3: 12,
    3.5: 14,
    4: 16,
    5: 20,
    6: 24,
    7: 28,
    8: 32,
    9: 36,
    10: 40,
    12: 48,
    16: 64,
    20: 80,
    24: 96,
    32: 128,
    40: 160,
    48: 192,
    56: 224,
    64: 256,
  },
  radii: {
    none: 0,
    sm: 2,
    base: 4,
    md: 6,
    lg: 8,
    xl: 12,
    '2xl': 16,
    '3xl': 24,
    full: 9999,
  },
  shadows: {
    sm: {
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: 1,
      },
      shadowOpacity: 0.18,
      shadowRadius: 1.0,
      elevation: 1,
    },
    base: {
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: 1,
      },
      shadowOpacity: 0.2,
      shadowRadius: 1.41,
      elevation: 2,
    },
    md: {
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: 2,
      },
      shadowOpacity: 0.23,
      shadowRadius: 2.62,
      elevation: 4,
    },
    lg: {
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: 4,
      },
      shadowOpacity: 0.25,
      shadowRadius: 3.84,
      elevation: 5,
    },
    xl: {
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: 6,
      },
      shadowOpacity: 0.27,
      shadowRadius: 4.65,
      elevation: 6,
    },
  },
  components: {
    Button: {
      baseStyle: {
        rounded: 'xl',
        _text: {
          fontWeight: '600',
        },
      },
      sizes: {
        sm: {
          px: 3,
          py: 2,
          _text: {
            fontSize: 'sm',
          },
        },
        md: {
          px: 4,
          py: 3,
          _text: {
            fontSize: 'md',
          },
        },
        lg: {
          px: 6,
          py: 4,
          _text: {
            fontSize: 'lg',
          },
        },
      },
      variants: {
        solid: {
          bg: 'primary.500',
          _pressed: {
            bg: 'primary.600',
          },
          _text: {
            color: 'white',
          },
        },
        outline: {
          borderWidth: 2,
          borderColor: 'primary.500',
          _pressed: {
            bg: 'primary.50',
          },
          _text: {
            color: 'primary.500',
          },
        },
        ghost: {
          _pressed: {
            bg: 'primary.50',
          },
          _text: {
            color: 'primary.500',
          },
        },
      },
      defaultProps: {
        size: 'md',
        variant: 'solid',
      },
    },
    Input: {
      baseStyle: {
        rounded: 'lg',
        borderWidth: 1,
        borderColor: 'secondary.200',
        _focus: {
          borderColor: 'primary.500',
          bg: 'white',
        },
        _invalid: {
          borderColor: 'error.500',
        },
      },
      sizes: {
        sm: {
          px: 3,
          py: 2,
          _text: {
            fontSize: 'sm',
          },
        },
        md: {
          px: 4,
          py: 3,
          _text: {
            fontSize: 'md',
          },
        },
        lg: {
          px: 4,
          py: 4,
          _text: {
            fontSize: 'lg',
          },
        },
      },
      defaultProps: {
        size: 'md',
      },
    },
    Card: {
      baseStyle: {
        rounded: 'xl',
        bg: 'white',
        shadow: 'md',
        p: 4,
      },
    },
  },
  config: {
    // Changing initialColorMode to 'light'
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
});

interface NativeBaseAppProviderProps {
  children: ReactNode;
}

export const NativeBaseAppProvider: React.FC<NativeBaseAppProviderProps> = ({ children }) => {
  return (
    <NativeBaseProvider theme={theme}>
      {children}
    </NativeBaseProvider>
  );
};

export { theme };