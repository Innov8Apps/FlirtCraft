# NativeBase Theme Configuration

---
title: FlirtCraft NativeBase Theme Configuration
description: Complete theme configuration for NativeBase with FlirtCraft design tokens
last-updated: 2025-08-30
version: 2.0.0
related-files:
  - ../style-guide.md
  - ./colors.md
  - ./typography.md
  - ./spacing.md
dependencies:
  - native-base
status: approved
---

## Overview

This document provides the complete NativeBase theme configuration for FlirtCraft, integrating all design tokens and ensuring consistency across components. NativeBase is a battle-tested, mature component library that provides comprehensive UI components with excellent cross-platform support.

## Base Theme Configuration

### Core Theme Setup

```javascript
// theme/nativebase-theme.js
import { extendTheme } from 'native-base';

const theme = extendTheme({
  colors: {
    // Primary Colors - FlirtCraft Orange
    primary: {
      50: '#FFF7ED',
      100: '#FFEDD5',
      200: '#FED7AA',
      300: '#FDBA74',
      400: '#FB923C',
      500: '#F97316', // Main Primary
      600: '#EA580C',
      700: '#C2410C',
      800: '#9A3412',
      900: '#7C2D12',
    },
    
    // Secondary Colors - Teal
    secondary: {
      50: '#F0FDFA',
      100: '#CCFBF1',
      200: '#99F6E4',
      300: '#5EEAD4',
      400: '#2DD4BF',
      500: '#E65100', // Main Secondary
      600: '#0D9488',
      700: '#0F766E',
      800: '#115E59',
      900: '#134E4A',
    },
    
    // Success Colors - Green (for Green difficulty)
    success: {
      50: '#F0FDF4',
      100: '#DCFCE7',
      200: '#BBF7D0',
      300: '#86EFAC',
      400: '#4ADE80',
      500: '#10B981', // Main Success
      600: '#059669',
      700: '#047857',
      800: '#065F46',
      900: '#064E3B',
    },
    
    // Warning Colors - Amber (for Yellow difficulty)
    warning: {
      50: '#FFFBEB',
      100: '#FEF3C7',
      200: '#FDE68A',
      300: '#FCD34D',
      400: '#FBBF24',
      500: '#F59E0B', // Main Warning
      600: '#D97706',
      700: '#B45309',
      800: '#92400E',
      900: '#78350F',
    },
    
    // Error Colors - Red (for Red difficulty)
    error: {
      50: '#FEF2F2',
      100: '#FECACA',
      200: '#FCA5A5',
      300: '#F87171',
      400: '#EF4444', // Main Error
      500: '#DC2626',
      600: '#B91C1C',
      700: '#991B1B',
      800: '#7F1D1D',
      900: '#450A0A',
    },
    
    // Info Colors - Blue
    info: {
      50: '#EFF6FF',
      100: '#DBEAFE',
      200: '#BFDBFE',
      300: '#93C5FD',
      400: '#60A5FA',
      500: '#3B82F6', // Main Info
      600: '#2563EB',
      700: '#1D4ED8',
      800: '#1E40AF',
      900: '#1E3A8A',
    },
    
    // Gray Scale - Neutral
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
    
    // Semantic Colors
    white: '#FFFFFF',
    black: '#000000',
    transparent: 'transparent',
    
    // Custom FlirtCraft Colors
    flirtcraft: {
      gradient: {
        start: '#F97316',
        end: '#EA580C',
      },
      difficulty: {
        green: '#10B981',
        yellow: '#F59E0B',
        red: '#EF4444',
      },
    },
  },
  
  fontConfig: {
    Inter: {
      100: {
        normal: 'Inter-Thin',
      },
      200: {
        normal: 'Inter-ExtraLight',
      },
      300: {
        normal: 'Inter-Light',
      },
      400: {
        normal: 'Inter-Regular',
      },
      500: {
        normal: 'Inter-Medium',
      },
      600: {
        normal: 'Inter-SemiBold',
      },
      700: {
        normal: 'Inter-Bold',
      },
      800: {
        normal: 'Inter-ExtraBold',
      },
      900: {
        normal: 'Inter-Black',
      },
    },
  },
  
  fonts: {
    heading: 'Inter',
    body: 'Inter',
    mono: 'SF Mono, Consolas, Liberation Mono, Menlo',
  },
  
  fontSizes: {
    '2xs': 10,
    'xs': 12,     // Caption
    'sm': 14,     // Body Small, Button Small
    'md': 16,     // Body, Button
    'lg': 18,     // Body Large, Button Large
    'xl': 20,     // H4
    '2xl': 24,    // H3
    '3xl': 28,    // H2, H1 (mobile)
    '4xl': 32,    // H1 (tablet)
    '5xl': 36,    // H1 (desktop)
    '6xl': 48,
  },
  
  lineHeights: {
    '2xs': 12,
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
  
  fontWeights: {
    hairline: '100',
    thin: '200',
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
    black: '900',
  },
  
  space: {
    px: 1,
    0: 0,
    0.5: 2,   // xs
    1: 4,     // sm
    1.5: 6,
    2: 8,     // md
    2.5: 10,
    3: 12,    // lg
    3.5: 14,
    4: 16,    // xl
    5: 20,
    6: 24,    // 2xl
    7: 28,
    8: 32,    // 3xl
    9: 36,
    10: 40,
    12: 48,   // 4xl
    16: 64,   // 5xl
    20: 80,
    24: 96,
    32: 128,
    40: 160,
    48: 192,
    56: 224,
    64: 256,
  },
  
  sizes: {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
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
    px: 1,
    full: '100%',
    '3xs': 224,
    '2xs': 256,
    xs: 320,
    sm: 384,
    md: 448,
    lg: 512,
    xl: 576,
    '2xl': 672,
  },
  
  radii: {
    none: 0,
    xs: 2,
    sm: 4,
    md: 6,
    lg: 8,
    xl: 12,
    '2xl': 16,
    '3xl': 20,
    full: 9999,
  },
  
  shadows: {
    none: {
      shadowColor: 'transparent',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0,
      shadowRadius: 0,
      elevation: 0,
    },
    sm: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.1,
      shadowRadius: 2,
      elevation: 2,
    },
    base: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    },
    md: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.1,
      shadowRadius: 6,
      elevation: 4,
    },
    lg: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 10 },
      shadowOpacity: 0.1,
      shadowRadius: 15,
      elevation: 6,
    },
    xl: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 20 },
      shadowOpacity: 0.1,
      shadowRadius: 25,
      elevation: 8,
    },
  },
  
  components: {
    Button: {
      baseStyle: {
        rounded: 'xl',
        _text: {
          fontWeight: 'semibold',
        },
      },
      defaultProps: {
        size: 'md',
        colorScheme: 'primary',
      },
      sizes: {
        sm: {
          px: 4,
          py: 2,
          _text: {
            fontSize: 'sm',
          },
        },
        md: {
          px: 5,
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
          _light: {
            bg: 'primary.500',
            _pressed: {
              bg: 'primary.600',
            },
            _text: {
              color: 'white',
            },
          },
          _dark: {
            bg: 'primary.500',
            _pressed: {
              bg: 'primary.600',
            },
            _text: {
              color: 'white',
            },
          },
        },
        outline: {
          borderWidth: 2,
          _light: {
            borderColor: 'primary.500',
            _text: {
              color: 'primary.500',
            },
            _pressed: {
              bg: 'primary.50',
            },
          },
          _dark: {
            borderColor: 'primary.400',
            _text: {
              color: 'primary.400',
            },
            _pressed: {
              bg: 'primary.900:alpha.20',
            },
          },
        },
        ghost: {
          _light: {
            _text: {
              color: 'primary.500',
            },
            _pressed: {
              bg: 'primary.50',
            },
          },
          _dark: {
            _text: {
              color: 'primary.400',
            },
            _pressed: {
              bg: 'primary.900:alpha.20',
            },
          },
        },
      },
    },
    
    Input: {
      baseStyle: {
        rounded: 'lg',
        borderWidth: 2,
        fontSize: 'md',
        py: 3,
        px: 4,
        _light: {
          borderColor: 'gray.200',
          bg: 'white',
          _focus: {
            borderColor: 'primary.500',
            bg: 'white',
          },
        },
        _dark: {
          borderColor: 'gray.700',
          bg: 'gray.800',
          color: 'gray.50',
          _focus: {
            borderColor: 'primary.400',
            bg: 'gray.800',
          },
        },
      },
      defaultProps: {
        size: 'md',
      },
      sizes: {
        sm: {
          fontSize: 'sm',
          py: 2,
          px: 3,
        },
        md: {
          fontSize: 'md',
          py: 3,
          px: 4,
        },
        lg: {
          fontSize: 'lg',
          py: 4,
          px: 4,
        },
      },
    },
    
    Text: {
      baseStyle: {
        _light: {
          color: 'gray.800',
        },
        _dark: {
          color: 'gray.100',
        },
      },
      variants: {
        heading: {
          fontWeight: 'bold',
          _light: {
            color: 'gray.900',
          },
          _dark: {
            color: 'white',
          },
        },
        body: {
          fontWeight: 'normal',
        },
        caption: {
          fontSize: 'xs',
          _light: {
            color: 'gray.500',
          },
          _dark: {
            color: 'gray.400',
          },
        },
      },
    },
    
    Box: {
      baseStyle: {
        _light: {
          bg: 'white',
        },
        _dark: {
          bg: 'gray.800',
        },
      },
      variants: {
        card: {
          p: 5,
          rounded: '2xl',
          shadow: 'base',
          _light: {
            bg: 'white',
          },
          _dark: {
            bg: 'gray.800',
            borderColor: 'gray.700',
            borderWidth: 1,
          },
        },
      },
    },
    
    Badge: {
      baseStyle: {
        rounded: 'full',
        px: 2,
        py: 0.5,
        _text: {
          fontSize: 'xs',
          fontWeight: 'semibold',
        },
      },
      variants: {
        solid: {
          _light: {
            bg: 'primary.500',
            _text: {
              color: 'white',
            },
          },
        },
        subtle: {
          _light: {
            bg: 'primary.100',
            _text: {
              color: 'primary.700',
            },
          },
        },
        outline: {
          borderWidth: 1,
          _light: {
            borderColor: 'primary.500',
            _text: {
              color: 'primary.500',
            },
          },
        },
      },
    },
  },
  
  config: {
    useSystemColorMode: false,
    initialColorMode: 'light',
  },
});

export default theme;
```

## Component Usage Examples

### Basic Component Usage

```jsx
import { 
  Button, 
  Input, 
  Box, 
  VStack, 
  HStack, 
  Text,
  FormControl,
  Badge
} from 'native-base';

// Primary button
<Button colorScheme="primary" size="lg">
  Start Practicing
</Button>

// Secondary outline button
<Button variant="outline" colorScheme="secondary">
  View Profile
</Button>

// Input field with form control
<FormControl>
  <FormControl.Label>Your Message</FormControl.Label>
  <Input 
    placeholder="Type your message..." 
    size="md"
  />
</FormControl>

// Difficulty badges
<HStack space={2}>
  <Badge colorScheme="success">Green - Friendly</Badge>
  <Badge colorScheme="warning">Yellow - Real Talk</Badge>
  <Badge colorScheme="error">Red - A-Game</Badge>
</HStack>
```

### Custom Card Component

```jsx
import { Box, VStack, HStack, Text, Badge, Pressable } from 'native-base';

const ScenarioCard = ({ scenario, difficulty, onPress }) => {
  const difficultyColors = {
    green: 'success',
    yellow: 'warning',
    red: 'error'
  };
  
  return (
    <Pressable onPress={onPress}>
      {({ isPressed }) => (
        <Box
          variant="card"
          opacity={isPressed ? 0.8 : 1}
          transform={[{ scale: isPressed ? 0.98 : 1 }]}
        >
          <VStack space={3}>
            <HStack justifyContent="space-between" alignItems="center">
              <Text fontSize="xl" fontWeight="bold">
                {scenario.title}
              </Text>
              <Badge colorScheme={difficultyColors[difficulty]}>
                {difficulty.toUpperCase()}
              </Badge>
            </HStack>
            <Text color="gray.500">
              {scenario.description}
            </Text>
          </VStack>
        </Box>
      )}
    </Pressable>
  );
};
```

### Chat Message Component (Custom, not Gifted Chat)

```jsx
import { Box, HStack, Avatar, VStack, Text } from 'native-base';

const ChatMessage = ({ message, isUser }) => {
  return (
    <HStack 
      space={2} 
      alignSelf={isUser ? 'flex-end' : 'flex-start'}
      maxW="80%"
    >
      {!isUser && (
        <Avatar 
          size="sm" 
          source={{ uri: message.avatar }}
          bg="secondary.500"
        >
          AI
        </Avatar>
      )}
      <Box
        bg={isUser ? 'primary.500' : 'gray.100'}
        rounded="xl"
        roundedBottomRight={isUser ? 'sm' : 'xl'}
        roundedBottomLeft={!isUser ? 'sm' : 'xl'}
        px={4}
        py={2}
      >
        <Text color={isUser ? 'white' : 'gray.800'}>
          {message.text}
        </Text>
      </Box>
      {isUser && (
        <Avatar 
          size="sm" 
          bg="primary.600"
        >
          U
        </Avatar>
      )}
    </HStack>
  );
};
```

### Dark Mode Support

```jsx
import { useColorMode, useColorModeValue, Box, Text, Switch } from 'native-base';

const ThemeToggle = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const bg = useColorModeValue('gray.50', 'gray.900');
  const textColor = useColorModeValue('gray.800', 'gray.100');
  
  return (
    <Box bg={bg} p={4} rounded="lg">
      <HStack justifyContent="space-between" alignItems="center">
        <Text color={textColor}>Dark Mode</Text>
        <Switch
          isChecked={colorMode === 'dark'}
          onToggle={toggleColorMode}
          colorScheme="primary"
        />
      </HStack>
    </Box>
  );
};
```

## Provider Setup

### App Configuration

```jsx
// App.js
import React from 'react';
import { NativeBaseProvider } from 'native-base';
import theme from './theme/nativebase-theme';

export default function App() {
  return (
    <NativeBaseProvider theme={theme}>
      {/* Your app components */}
    </NativeBaseProvider>
  );
}
```

### TypeScript Support

```typescript
// types/theme.d.ts
import { Theme } from 'native-base';

declare module 'native-base' {
  interface ICustomTheme extends Theme {
    colors: Theme['colors'] & {
      flirtcraft: {
        gradient: {
          start: string;
          end: string;
        };
        difficulty: {
          green: string;
          yellow: string;
          red: string;
        };
      };
    };
  }
}
```

## Integration with NativeWind

NativeBase works seamlessly with NativeWind for utility styling:

```jsx
import { Box, Text } from 'native-base';

// Combine NativeBase props with NativeWind classes
<Box 
  bg="primary.500" 
  className="rounded-lg shadow-md"
>
  <Text 
    fontSize="lg" 
    className="font-semibold text-white"
  >
    Hybrid Styling Approach
  </Text>
</Box>
```

## Benefits of NativeBase

- **Battle-tested**: Mature library with years of production use
- **Comprehensive**: 40+ pre-built components out of the box
- **Customizable**: Powerful theming system with design tokens
- **Cross-platform**: Consistent behavior across iOS, Android, and Web
- **Accessible**: Built-in accessibility features and ARIA support
- **Community**: Large, active community with extensive documentation
- **TypeScript**: Full TypeScript support with type definitions
- **Performance**: Optimized for React Native with minimal overhead

---

*This theme configuration provides the foundation for consistent styling across all FlirtCraft components using NativeBase, a proven and reliable component library.*