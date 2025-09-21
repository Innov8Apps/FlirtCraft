# Button Components

---
title: FlirtCraft Button Component Specifications
description: Complete button system with variants, states, and accessibility requirements
last-updated: 2025-08-30
version: 2.0.0
related-files:
  - ../style-guide.md
  - ./README.md
dependencies:
  - NativeBase Button components
  - React Native Reanimated 3
  - NativeWind 4.1 utilities
  - Design system color tokens
status: approved
---

## Button System Overview

FlirtCraft's button system creates confidence through clear visual hierarchy, encouraging feedback, and accessible interaction patterns. All buttons follow consistent sizing, color application, and animation standards while adapting to specific use case requirements.

## Primary Button

### Purpose
Main actions that move users forward in their confidence-building journey: starting conversations, completing setup, confirming choices.

### Visual Specifications

#### Large Size (Default)
- **Height**: 48px - Optimal touch target for mobile
- **Width**: Full-width on mobile, content-width on tablet/desktop
- **Padding**: 16px horizontal, 12px vertical
- **Border Radius**: 12px - Friendly, approachable corners
- **Typography**: Button Large (18px/24px, 600) - Clear, readable text
- **Background**: Primary gradient (`linear-gradient(135deg, #F97316 0%, #EA580C 100%)`)
- **Text Color**: White (`#FFFFFF`) for maximum contrast
- **Shadow**: `0 4px 14px rgba(99, 102, 241, 0.25)` - Subtle elevation

#### Medium Size
- **Height**: 40px - Compact option for secondary areas
- **Padding**: 20px horizontal, 8px vertical
- **Typography**: Button (16px/20px, 600)
- **Other specs**: Same as Large with proportional adjustments

#### Small Size
- **Height**: 32px - Tight spaces, inline actions
- **Padding**: 16px horizontal, 6px vertical  
- **Typography**: Button Small (14px/18px, 500)
- **Shadow**: Reduced to `0 2px 8px rgba(99, 102, 241, 0.2)`

### Interactive States

#### Default State

**NativeBase Implementation:**
```jsx
import { Button } from 'native-base';

<Button 
  size="lg"
  variant="solid"
  colorScheme="primary"
  borderRadius="12"
  shadow={3}
  _pressed={{
    bg: 'primary.700'
  }}
  _hover={{
    bg: 'primary.600'
  }}
>
  Start Practicing
</Button>
```

**NativeWind 4.1 Alternative:**
```jsx
import { Pressable, Text } from 'react-native';

<Pressable 
  className="h-12 px-6 bg-primary rounded-xl shadow-lg items-center justify-center active:scale-95 transition-transform duration-100"
>
  <Text className="text-white font-semibold text-lg">
    Start Practicing
  </Text>
</Pressable>
```

#### Hover State (Web/Cursor Devices)
- **Background**: Slightly deeper gradient with 10% increased saturation
- **Shadow**: Increased to `0 6px 20px rgba(99, 102, 241, 0.3)`
- **Transition**: `200ms ease-out` for smooth color and shadow changes
- **Cursor**: Pointer cursor indicates interactivity

#### Active/Press State
- **Scale**: 98% (transform: scale(0.98)) for tactile feedback
- **Duration**: 100ms ease-in for press, 200ms ease-out for release
- **Background**: Maintains gradient, no color change on press
- **Shadow**: Slightly reduced during press for "pressed down" effect

#### Focus State (Keyboard Navigation)
- **Outline**: 2px solid Primary (`#F97316`) with 2px offset
- **Background**: Unchanged from default state
- **Animation**: Focus ring fades in over 150ms
- **Accessibility**: Clearly visible on all background colors

#### Disabled State
- **Opacity**: 40% overall component opacity
- **Background**: Maintains gradient but heavily muted
- **Interaction**: No touch events, no animations
- **Cursor**: Default cursor (not pointer) on web
- **Accessibility**: `aria-disabled="true"` attribute

#### Loading State
- **Background**: Maintains full gradient and styling
- **Content**: Text replaced with loading spinner
- **Spinner**: White color, 20px diameter, smooth rotation
- **Interaction**: Touch events disabled during loading
- **Duration**: Supports indefinite loading with smooth spinner animation

### Accessibility Implementation

#### NativeBase Screen Reader Support
```jsx
import { Button } from 'native-base';

<Button
  accessibilityRole="button"
  accessibilityLabel="Start your first practice conversation"
  accessibilityHint="Opens scenario selection screen"
  accessibilityState={{
    disabled: isDisabled,
    busy: isLoading
  }}
  isDisabled={isDisabled}
  _focus={{
    borderColor: 'primary.500',
    borderWidth: 2
  }}
>
  {buttonText}
</Button>
```

#### NativeWind 4.1 Focus States
```jsx
// Enhanced focus support with NativeWind 4.1
<Pressable 
  className="focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-gray-900"
  accessibilityRole="button"
  accessibilityLabel="Start your first practice conversation"
>
  <Text className="text-white font-semibold">
    {buttonText}
  </Text>
</Pressable>
```

#### Keyboard Support
- **Tab Navigation**: Included in logical tab order
- **Enter/Space**: Activates button action
- **Focus Indicator**: Clearly visible focus ring
- **Focus Management**: Maintains focus after activation unless navigation occurs

---

## Secondary Button

### Purpose
Alternative actions, secondary paths, or actions that support the primary flow without competing for attention.

### Visual Specifications

#### Standard Design
- **Height**: Same as Primary (48px/40px/32px)
- **Border**: 2px solid Primary (`#F97316`) 
- **Background**: White (`#FFFFFF`) or transparent
- **Text Color**: Primary (`#F97316`)
- **Typography**: Same scale as Primary buttons
- **Border Radius**: 12px matching Primary
- **Shadow**: None (relies on border for definition)

### Interactive States

#### Default State

**NativeBase Implementation:**
```jsx
import { Button } from 'native-base';

<Button 
  size="lg"
  variant="outline"
  colorScheme="primary"
  borderRadius="12"
  borderWidth="2"
  _pressed={{
    bg: 'primary.100'
  }}
  _hover={{
    bg: 'primary.50'
  }}
>
  Maybe Later
</Button>
```

**NativeWind 4.1 Alternative:**
```jsx
import { Pressable, Text } from 'react-native';

<Pressable 
  className="h-12 px-6 bg-white border-2 border-primary rounded-xl items-center justify-center active:scale-95 active:bg-primary/10 transition-all duration-100"
>
  <Text className="text-primary font-semibold text-lg">
    Maybe Later
  </Text>
</Pressable>
```

#### Hover State
- **Background**: Light primary tint (`rgba(99, 102, 241, 0.1)`)
- **Border**: Unchanged primary color
- **Text**: Unchanged primary color
- **Transition**: 200ms ease-out for smooth background change

#### Active/Press State
- **Scale**: 98% matching Primary button feedback
- **Background**: Slightly deeper tint (`rgba(99, 102, 241, 0.15)`)
- **Animation**: Same timing as Primary (100ms in, 200ms out)

#### Focus State
- **Outline**: 2px solid Primary with 2px offset (same as Primary)
- **Background**: Unchanged from default
- **Border**: Remains primary color

#### Disabled State
- **Border Color**: Neutral-300 (`#D1D5DB`)
- **Text Color**: Neutral-300 (`#D1D5DB`)
- **Background**: White (unchanged)
- **Opacity**: No overall opacity change (individual element colors change)

---

## Ghost Button

### Purpose
Tertiary actions, navigation elements, subtle interactions that don't compete with primary and secondary actions.

### Visual Specifications

#### Standard Design
- **Height**: Same sizing scale (48px/40px/32px)
- **Background**: Transparent
- **Border**: None
- **Text Color**: Primary (`#F97316`)
- **Typography**: Same scale, potentially lighter weight (500 instead of 600)
- **Padding**: Smaller horizontal padding (12px instead of 16px)
- **Touch Target**: Maintains 44×44px minimum despite smaller visual appearance

### Interactive States

#### Default State

**NativeBase Implementation:**
```jsx
import { Button } from 'native-base';

<Button 
  size="lg"
  variant="ghost"
  colorScheme="primary"
  borderRadius="12"
  minW="11"
  _pressed={{
    bg: 'primary.100'
  }}
  _hover={{
    bg: 'primary.50'
  }}
>
  Skip
</Button>
```

**NativeWind 4.1 Alternative:**
```jsx
import { Pressable, Text } from 'react-native';

<Pressable 
  className="h-12 px-3 bg-transparent min-w-11 items-center justify-center active:scale-95 active:bg-primary/5 rounded-xl transition-all duration-100"
>
  <Text className="text-primary font-medium text-lg">
    Skip
  </Text>
</Pressable>
```

#### Hover State
- **Background**: Very light primary tint (`rgba(99, 102, 241, 0.05)`)
- **Text Color**: Slightly darker primary (`#C2410C`)
- **Transition**: 200ms ease-out

#### Active/Press State
- **Background**: Light primary tint (`rgba(99, 102, 241, 0.1)`)
- **Scale**: 95% (slightly more pronounced than solid buttons)
- **Animation**: Same timing pattern (100ms in, 200ms out)

#### Focus State
- **Outline**: 2px solid Primary with 2px offset
- **Background**: Transparent (unchanged)
- **Text**: Unchanged primary color

---

## Specialized Button Variants

### Difficulty Selector Buttons

#### Visual Design
- **Layout**: Horizontal pill buttons for Green/Yellow/Red selection
- **Background**: Semantic colors (Success/Warning/Error)
- **Border Radius**: 24px for full pill shape
- **Typography**: Button (16px/20px, 500) with emoji and text
- **Spacing**: 8px between buttons in group

#### Implementation Example
```jsx
const DifficultyButton = ({ difficulty, isSelected, onSelect }) => {
  const colors = {
    green: { bg: '#10B981', text: '#FFFFFF' },
    yellow: { bg: '#F59E0B', text: '#374151' },
    red: { bg: '#EF4444', text: '#FFFFFF' }
  }
  
  return (
    <TouchableOpacity
      style={{
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderRadius: 24,
        backgroundColor: colors[difficulty].bg,
        opacity: isSelected ? 1 : 0.7,
        transform: [{ scale: isSelected ? 1 : 0.95 }]
      }}
      onPress={() => onSelect(difficulty)}
    >
      <Text style={{ 
        color: colors[difficulty].text,
        fontWeight: '500' 
      }}>
        {difficulty === 'green' && '🟢 Green (Friendly)'}
        {difficulty === 'yellow' && '🟡 Yellow (Real Talk)'}
        {difficulty === 'red' && '🔴 Red (A-Game)'}
      </Text>
    </TouchableOpacity>
  )
}
```

### Floating Action Button (FAB)

#### Use Cases
- Start new conversation from main screen
- Add custom scenario (future feature)
- Quick access to help or settings

#### Visual Specifications
- **Size**: 56×56px circle (Material Design standard)
- **Background**: Primary gradient matching primary buttons
- **Icon**: 24×24px white icon, centered
- **Shadow**: Enhanced elevation (`0 6px 20px rgba(99, 102, 241, 0.3)`)
- **Position**: Fixed bottom-right with 16px margins

---

## Implementation Guidelines

### NativeBase Theme Integration

#### Theme Configuration
```javascript
// NativeBase theme configuration
import { extendTheme } from 'native-base';

const theme = extendTheme({
  colors: {
    primary: {
      50: '#FFF7ED',
      100: '#FFEDD5',
      500: '#F97316',
      600: '#EA580C',
      700: '#C2410C',
    },
  },
  components: {
    Button: {
      variants: {
        solid: {
          bg: 'primary.500',
          _pressed: {
            bg: 'primary.700',
          },
          _hover: {
            bg: 'primary.600',
          },
          _text: {
            color: 'white',
            fontWeight: 'semibold'
          }
        },
        outline: {
          borderColor: 'primary.500',
          borderWidth: 2,
          bg: 'transparent',
          _pressed: {
            bg: 'primary.100',
          },
          _hover: {
            bg: 'primary.50',
          },
          _text: {
            color: 'primary.500',
            fontWeight: 'semibold'
          }
        },
        ghost: {
          bg: 'transparent',
          _pressed: {
            bg: 'primary.100',
          },
          _hover: {
            bg: 'primary.50',
          },
          _text: {
            color: 'primary.500',
            fontWeight: 'medium'
          }
        }
      }
    }
  }
});

export default theme;
```

#### NativeWind 4.1 Utilities
```javascript
// Custom button utilities in tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'press': 'press 100ms ease-in-out',
        'release': 'release 200ms ease-in-out',
      },
      keyframes: {
        press: {
          '0%': { transform: 'scale(1)' },
          '100%': { transform: 'scale(0.98)' }
        },
        release: {
          '0%': { transform: 'scale(0.98)' },
          '100%': { transform: 'scale(1)' }
        }
      },
      colors: {
        primary: {
          DEFAULT: '#F97316',
          50: '#FFF7ED',
          100: '#FFEDD5',
          500: '#F97316',
          600: '#EA580C',
          700: '#C2410C',
        }
      }
    }
  }
}
```

### Animation Performance

#### Optimized Press Animation with Reanimated 3
```jsx
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring,
  runOnJS,
  useAnimatedGestureHandler
} from 'react-native-reanimated';
import { TapGestureHandler } from 'react-native-gesture-handler';

const AnimatedButton = ({ children, onPress, ...props }) => {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value
  }));
  
  const gestureHandler = useAnimatedGestureHandler({
    onStart: () => {
      scale.value = withSpring(0.98, { 
        damping: 15,
        stiffness: 400 
      });
    },
    onEnd: () => {
      scale.value = withSpring(1, { 
        damping: 15,
        stiffness: 400 
      });
      if (onPress) {
        runOnJS(onPress)();
      }
    },
    onFail: () => {
      scale.value = withSpring(1, { 
        damping: 15,
        stiffness: 400 
      });
    }
  });
  
  return (
    <TapGestureHandler onGestureEvent={gestureHandler}>
      <Animated.View style={animatedStyle}>
        {children}
      </Animated.View>
    </TapGestureHandler>
  );
};
```

#### NativeWind 4.1 CSS Animations
```jsx
// Using NativeWind 4.1 built-in animation utilities
const PressableButton = ({ children, onPress, className = '' }) => {
  return (
    <Pressable 
      onPress={onPress}
      className={`active:scale-95 transition-transform duration-100 ${className}`}
    >
      {children}
    </Pressable>
  );
};

// Dark mode support with NativeBase + NativeWind 4.1
<Button 
  colorScheme="primary" 
  className="active:scale-95"
  _dark={{
    bg: 'primary.400'
  }}
>
  Press Me
</Button>
```

## Quality Assurance Checklist

### Visual Consistency
- [ ] Colors match design system tokens exactly
- [ ] Typography uses established scale
- [ ] Spacing follows systematic measurements
- [ ] Border radius consistent within button family
- [ ] Shadows appropriate for elevation level

### Accessibility Compliance
- [ ] Touch targets meet 44×44px minimum
- [ ] Focus indicators clearly visible
- [ ] Screen reader labels descriptive and helpful
- [ ] Keyboard navigation fully functional
- [ ] Color contrast meets WCAG AA standards (4.5:1 minimum)

### Performance Validation
- [ ] Animations maintain 60fps on target devices
- [ ] Press feedback responsive (<100ms)
- [ ] No memory leaks from animation timers
- [ ] Smooth transitions between all states

### Cross-Platform Testing
- [ ] iOS appearance matches specifications
- [ ] Android appearance consistent with iOS
- [ ] Haptic feedback works appropriately on iOS
- [ ] Material Design principles respected on Android

---

*Button components serve as the primary interaction points in FlirtCraft, designed to build user confidence through clear, accessible, and encouraging interface patterns.*