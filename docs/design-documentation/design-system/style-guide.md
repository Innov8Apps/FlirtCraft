# FlirtCraft Design System Style Guide

---
title: FlirtCraft Complete Style Guide
description: Comprehensive design system for AI-powered dating conversation training app
last-updated: 2025-08-30
version: 2.0.0
status: approved
technology-stack:
  - NativeBase
  - React Native Gifted Chat
  - NativeWind 4.1
  - React Native Reanimated 3
---

## Design Philosophy

FlirtCraft's design system creates a supportive, confidence-building experience through:

- **Psychological Safety**: Warm, non-judgmental visual language that reduces anxiety
- **Progressive Disclosure**: Information revealed gradually to prevent overwhelm
- **Accessible Excellence**: WCAG 2.1 AA compliance as minimum standard
- **Gamified Encouragement**: Motivation through positive reinforcement, not pressure
- **Mobile-First Excellence**: Touch-optimized interactions for seamless mobile experience

## Color System

### Primary Colors
- **Primary**: `#F97316` (Indigo-500) – Main CTAs, brand elements, progress indicators
- **Primary Dark**: `#C2410C` (Indigo-700) – Hover states, emphasis, active elements
- **Primary Light**: `#FDBA74` (Indigo-300) – Subtle backgrounds, highlights, disabled states

### Secondary Colors
- **Secondary**: `#E65100` (Deep Orange-500) – Supporting elements, warm accent
- **Secondary Light**: `#F9A8D4` (Pink-300) – Backgrounds, subtle accents, selected states
- **Secondary Pale**: `#FCE7F3` (Pink-50) – Selected states, highlights, soft backgrounds

### Accent Colors
- **Accent Primary**: `#10B981` (Emerald-500) – Success states, Green difficulty, positive feedback
- **Accent Secondary**: `#F59E0B` (Amber-500) – Warnings, Yellow difficulty, caution states
- **Gradient Start**: `#F97316` – Primary gradient starting point
- **Gradient End**: `#EA580C` – Primary gradient ending point

### Semantic Colors
- **Success**: `#10B981` (Emerald-500) – Positive actions, achievements, completed goals
- **Warning**: `#F59E0B` (Amber-500) – Caution states, Yellow difficulty, attention needed
- **Error**: `#EF4444` (Red-500) – Errors, Red difficulty, destructive actions, critical feedback
- **Info**: `#3B82F6` (Blue-500) – Informational messages, tips, neutral feedback

### Difficulty Color System
- **Green (Friendly)**: `#10B981` (Emerald-500) – Easy scenarios, welcoming contexts
- **Yellow (Real Talk)**: `#F59E0B` (Amber-500) – Intermediate difficulty, realistic scenarios
- **Red (A-Game)**: `#EF4444` (Red-500) – Advanced difficulty, challenging contexts

### Neutral Palette
- **Neutral-50**: `#F9FAFB` – Page backgrounds, card backgrounds
- **Neutral-100**: `#F3F4F6` – Subtle borders, dividers
- **Neutral-200**: `#E5E7EB` – Input borders, inactive elements
- **Neutral-300**: `#D1D5DB` – Placeholder text, disabled text
- **Neutral-400**: `#9CA3AF` – Secondary text, icons
- **Neutral-500**: `#6B7280` – Body text, standard content
- **Neutral-600**: `#4B5563` – Emphasis text, headings
- **Neutral-700**: `#374151` – Strong emphasis, important headings
- **Neutral-800**: `#1F2937` – High contrast text, titles
- **Neutral-900**: `#111827` – Maximum contrast, primary headings

### Accessibility Notes
- All color combinations meet WCAG AA standards (minimum 4.5:1 for normal text, 3:1 for large text)
- Critical interactions maintain 7:1 contrast ratio for AAA compliance
- Color-blind friendly palette tested with Stark and Colour Oracle
- Never relies on color alone to convey information

## Typography System

### Font Stack
- **Primary**: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Monospace**: `'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace`

### Font Weights
- **Light**: 300 – Decorative text, large display elements
- **Regular**: 400 – Body text, standard interface elements
- **Medium**: 500 – Emphasized text, secondary headings
- **Semibold**: 600 – Button text, important labels
- **Bold**: 700 – Primary headings, strong emphasis

### Mobile Type Scale (Primary)
- **H1**: `28px/36px, 700, -0.02em` – Screen titles, major sections
- **H2**: `24px/32px, 600, -0.01em` – Section headers, card titles
- **H3**: `20px/28px, 600, 0em` – Subsection headers, feature titles  
- **H4**: `18px/24px, 500, 0em` – Minor headers, component titles
- **H5**: `16px/22px, 500, 0em` – List headers, metadata labels
- **Body Large**: `18px/26px, 400` – Primary reading text, important descriptions
- **Body**: `16px/22px, 400` – Standard UI text, form fields
- **Body Small**: `14px/20px, 400` – Secondary information, captions
- **Caption**: `12px/16px, 400, 0.01em` – Metadata, timestamps, fine print
- **Label**: `14px/20px, 500, 0.02em, uppercase` – Form labels, categories
- **Button Large**: `18px/24px, 600` – Primary action buttons
- **Button**: `16px/20px, 600` – Standard buttons, CTAs
- **Button Small**: `14px/18px, 500` – Minor actions, secondary buttons

### Tablet Type Scale (768px+)
- **H1**: `32px/40px` – Increased screen real estate scaling
- **H2**: `28px/36px` – Proportional scaling for medium screens
- **Body Large**: `20px/28px` – Enhanced readability for tablet viewing

### Desktop Type Scale (1024px+)
- **H1**: `36px/44px` – Desktop-optimized hierarchy
- **H2**: `32px/40px` – Clear section distinction
- **Body Large**: `20px/28px` – Optimal reading length maintenance

### Typography Usage Guidelines
- **Line Length**: 45-75 characters for optimal readability
- **Paragraph Spacing**: 1.5x line height minimum
- **Letter Spacing**: Tight for large text, slightly loose for small caps
- **Text Contrast**: Minimum 4.5:1 ratio, prefer 7:1 for body text

## Spacing & Layout System

### Base Unit
**4px** – All spacing values derive from this fundamental unit for mathematical consistency

### Spacing Scale
- **xs**: `2px` – Micro spacing between tightly related elements (borders, tiny gaps)
- **sm**: `4px` – Small spacing, internal component padding
- **md**: `8px` – Default spacing, standard margins between elements
- **lg**: `12px` – Medium spacing between component groups
- **xl**: `16px` – Large spacing, major section separation
- **2xl**: `24px` – Extra large spacing, screen padding and major layout gaps
- **3xl**: `32px` – Huge spacing, hero sections, major content separation
- **4xl**: `48px` – Screen-level spacing, major layout sections
- **5xl**: `64px` – Maximum spacing for special layouts

### Grid System
- **Mobile Columns**: 4 columns with 16px gutters
- **Tablet Columns**: 8 columns with 20px gutters  
- **Desktop Columns**: 12 columns with 24px gutters
- **Container Max-width**: 1200px with responsive padding

### Breakpoints
- **Mobile**: 320px – 767px (primary target)
- **Tablet**: 768px – 1023px (secondary support)
- **Desktop**: 1024px – 1439px (web version consideration)
- **Wide**: 1440px+ (large screen optimization)

### Layout Principles
- **Touch Targets**: Minimum 44×44px for all interactive elements
- **Safe Areas**: 16px minimum margins on mobile, 24px on tablet+
- **Content Width**: Maximum 600px for text blocks to maintain readability
- **Vertical Rhythm**: Consistent spacing using the 4px base unit

## Component Specifications

### Buttons

#### Primary Button
**Purpose**: Main actions, primary CTAs, conversation starters

**Visual Specifications**:
- **Height**: `48px` (large), `40px` (medium), `32px` (small)
- **Padding**: `16px 24px` (large), `12px 20px` (medium), `8px 16px` (small)
- **Border Radius**: `12px` – Friendly, approachable feel
- **Background**: Primary gradient (`#F97316` to `#EA580C`)
- **Text Color**: `#FFFFFF` (White)
- **Typography**: Button scale matching size
- **Shadow**: `0 4px 14px rgba(99, 102, 241, 0.25)`

**States**:
- **Default**: Full gradient with shadow
- **Hover**: Slightly darker gradient, increased shadow
- **Active**: Pressed state with reduced shadow
- **Focus**: 2px outline in Primary color with 2px offset
- **Disabled**: 40% opacity, no interactions
- **Loading**: Gradient maintained with spinner overlay

**Interaction Specifications**:
- **Hover Transition**: `200ms ease-out` for smooth color changes
- **Press Feedback**: Scale down to 98% with `100ms ease-in`
- **Focus Animation**: Outline fades in over `150ms`

#### Secondary Button
**Purpose**: Secondary actions, alternative paths, supportive CTAs

**Visual Specifications**:
- **Height**: Same as Primary
- **Padding**: Same as Primary  
- **Border**: `2px solid #F97316` (Primary color)
- **Background**: `#FFFFFF` (White) with `#F97316` text
- **Border Radius**: `12px`

**States**: Similar timing to Primary with border color changes

#### Ghost Button
**Purpose**: Tertiary actions, subtle interactions, navigation elements

**Visual Specifications**:
- **Background**: Transparent
- **Text Color**: `#F97316` (Primary)
- **Hover Background**: `rgba(99, 102, 241, 0.1)`

### Form Elements

#### Text Input
**Visual Specifications**:
- **Height**: `48px` – Touch-friendly sizing
- **Padding**: `12px 16px` – Comfortable text spacing
- **Border**: `2px solid #E5E7EB` (Neutral-200)
- **Border Radius**: `8px` – Subtle, clean corners
- **Background**: `#FFFFFF` (White)
- **Typography**: Body (16px/22px) – Prevents zoom on iOS

**States**:
- **Default**: Light border, white background
- **Focus**: `#F97316` border, subtle shadow
- **Error**: `#EF4444` border with error message below
- **Success**: `#10B981` border with checkmark icon
- **Disabled**: Gray background, reduced opacity

#### Select/Dropdown
**Visual Specifications**:
- **Height**: `48px` – Consistent with text inputs
- **Chevron Icon**: 16px, positioned right with 12px margin
- **Background**: White with subtle down arrow
- **Options**: Full-width overlay with shadows

### Cards

#### Scenario Card
**Purpose**: Display location scenarios with difficulty selection

**Visual Specifications**:
- **Size**: Full-width mobile, 320px fixed tablet+
- **Border Radius**: `16px` – Modern, friendly appearance
- **Background**: White with subtle gradient overlay
- **Shadow**: `0 2px 8px rgba(0, 0, 0, 0.1)`
- **Padding**: `20px` – Generous content spacing
- **Image**: 16:9 aspect ratio background with overlay
- **Title**: H3 typography over image with text shadow

**Interactive States**:
- **Default**: Subtle shadow and clean presentation
- **Hover**: Increased shadow, slight lift effect
- **Selected**: Primary border, increased elevation

#### Feedback Card
**Purpose**: Display post-conversation scores and tips

**Visual Specifications**:
- **Layout**: Score prominent at top, tips listed below
- **Score Circle**: 80px diameter with Primary gradient progress
- **Background**: White with colored left border (success/warning/error)
- **Typography**: Score uses H1, tips use Body text
- **Icons**: 16px semantic icons for tip categories

### Navigation

#### Tab Bar (Bottom Navigation)
**Visual Specifications**:
- **Height**: `84px` (including safe area)
- **Background**: White with subtle top border
- **Icon Size**: 24px with 8px margin to text
- **Active State**: Primary color with slight scale increase
- **Inactive State**: Neutral-400 with standard sizing

#### Header Bar
**Visual Specifications**:
- **Height**: `64px` plus safe area
- **Background**: White with bottom shadow
- **Title**: H3 typography, centered
- **Back Button**: 24px icon, left-aligned with 16px margin
- **Action Button**: Right-aligned, consistent with button styles

## Motion & Animation System

### Timing Functions
- **Ease-out**: `cubic-bezier(0.0, 0, 0.2, 1)` – Entrances, expansions, natural deceleration
- **Ease-in-out**: `cubic-bezier(0.4, 0, 0.6, 1)` – Smooth transitions, position changes
- **Ease-in**: `cubic-bezier(0.4, 0, 1, 1)` – Exits, disappearing elements
- **Spring**: `tension: 300, friction: 20` – Playful interactions, elastic feedback

### Duration Scale
- **Micro**: `100-150ms` – State changes, hover effects, micro-interactions
- **Short**: `200-300ms` – Local transitions, dropdowns, button feedback
- **Medium**: `400-500ms` – Page transitions, modal appearances
- **Long**: `600-800ms` – Complex animations, onboarding flows, celebration

### Animation Principles
- **Performance**: Target 60fps minimum, prefer transform/opacity changes
- **Purpose**: Every animation serves functional purpose (feedback, guidance, delight)
- **Consistency**: Similar actions use similar timings and easing
- **Accessibility**: Respect `prefers-reduced-motion`, provide instant alternatives

### Key Animation Patterns

#### Page Transitions
- **Stack Navigation**: Slide from right (300ms ease-out)
- **Modal Presentation**: Scale up from center with backdrop fade (400ms ease-out)
- **Tab Switching**: Cross-fade content (200ms ease-in-out)

#### Micro-interactions
- **Button Press**: Scale 98% (100ms ease-in), return (200ms ease-out)
- **Card Selection**: Lift with shadow increase (200ms ease-out)
- **Input Focus**: Border color change with subtle scale (150ms ease-out)

#### Loading States
- **Spinner**: 1-second rotation loop, Primary color
- **Skeleton**: Shimmer animation across placeholder content
- **Progress**: Smooth progress bar advancement with spring easing

## Accessibility Guidelines

### WCAG 2.1 AA Compliance
- **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Touch Targets**: Minimum 44×44px for all interactive elements
- **Focus Indicators**: Visible focus rings with 2px outline and 2px offset
- **Text Scaling**: Support up to 200% text size increase
- **Motion**: Respect `prefers-reduced-motion` settings

### Screen Reader Support
- **Semantic HTML**: Proper heading hierarchy, landmark regions
- **ARIA Labels**: Descriptive labels for complex interactions
- **Live Regions**: Announce dynamic content changes
- **Alternative Text**: Meaningful descriptions for all images

### Keyboard Navigation
- **Tab Order**: Logical flow through interactive elements
- **Skip Links**: Quick navigation to main content areas
- **Keyboard Shortcuts**: Standard platform shortcuts supported
- **Focus Management**: Clear indication of current focus position

## Implementation Notes

### Technology Stack Implementation

#### NativeBase Integration
**Implementation Benefits:**
- **Battle-tested**: Mature, stable component library with extensive community support
- **Comprehensive Components**: Full suite of pre-built components for rapid development
- **Type Safety**: Full TypeScript support with comprehensive type definitions
- **Universal Compatibility**: Excellent cross-platform support for iOS, Android, and Web
- **Accessibility**: Built-in accessibility features and ARIA support

#### NativeBase Configuration
- **Theme System**: Custom theme extending NativeBase config with extendTheme()
- **Component Imports**: Import from 'native-base'
- **Styled Components**: Use theme customization and style props
- **Platform Variants**: Automatic platform-specific adaptations

#### NativeWind 4.1 Features
- **Dark Mode**: Built-in dark mode support with `dark:` prefix
- **Performance**: Compile-time CSS generation for better performance
- **Responsive Design**: Enhanced breakpoint system
- **Custom Utilities**: Extended utility classes for FlirtCraft-specific needs

#### React Native Gifted Chat
- **Message Rendering**: Custom message bubble rendering
- **Input Customization**: Styled input toolbar with FlirtCraft design
- **Avatar Integration**: Custom avatar rendering with difficulty colors
- **Accessibility**: Built-in screen reader support

### Design Token Export

#### NativeBase Theme Configuration
```javascript
import { extendTheme } from 'native-base';

const theme = extendTheme({
  colors: {
    primary: {
      50: '#FFF5E6',
      100: '#FFE4B8',
      200: '#FFD38A',
      300: '#FDBA74',
      400: '#FB923C',
      500: '#F97316',
      600: '#EA580C',
      700: '#C2410C',
      800: '#9A3412',
      900: '#7C2D12',
    },
    secondary: {
      50: '#FEF7F0',
      100: '#FEEEE0',
      200: '#FEDCC7',
      300: '#FDBA8C',
      400: '#FB9A3C',
      500: '#E65100',
      600: '#D84315',
      700: '#BF360C',
      800: '#A5300A',
      900: '#8B2508',
    },
    success: {
      500: '#10B981',
    },
    warning: {
      500: '#F59E0B',
    },
    error: {
      500: '#EF4444',
    },
    info: {
      500: '#3B82F6',
    },
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
  },
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
  components: {
    Button: {
      defaultProps: {
        size: 'md',
      },
      sizes: {
        lg: {
          px: 6,
          py: 4,
          fontSize: 'lg',
        },
        md: {
          px: 5,
          py: 3,
          fontSize: 'md',
        },
        sm: {
          px: 4,
          py: 2,
          fontSize: 'sm',
        },
      },
    },
    Input: {
      defaultProps: {
        size: 'md',
      },
      sizes: {
        md: {
          fontSize: 'md',
          py: 3,
          px: 4,
        },
      },
    },
  },
});

export default theme;
```

#### NativeWind 4.1 Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,tsx,ts,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#F97316',
        'primary-dark': '#C2410C',
        'primary-light': '#FDBA74',
        secondary: '#E65100',
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
        info: '#3B82F6',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
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
      }
    }
  },
  plugins: [],
};
```

### Component Usage Examples

#### NativeBase Components
```javascript
// NativeBase imports
import { 
  Box, 
  VStack, 
  HStack, 
  Button, 
  Text, 
  Input,
  FormControl,
  Select,
  Checkbox,
  Radio,
  Switch,
  Slider,
  Badge,
  Avatar,
  Card,
  Modal,
  Toast,
  Spinner,
  Progress,
  Skeleton
} from 'native-base';

// Usage examples:
// Button with text
<Button colorScheme="primary" size="lg">
  Click me
</Button>

// Input field
<Input 
  placeholder="Type here" 
  size="md"
  borderColor="gray.300"
  _focus={{ borderColor: 'primary.500' }}
/>

// Card component
<Box bg="white" rounded="lg" shadow={2} p={4}>
  <VStack space={3}>
    <Text fontSize="lg" fontWeight="bold">Card Title</Text>
    <Text color="gray.500">Card content goes here</Text>
  </VStack>
</Box>
```

### Quality Assurance
- **Design Review**: All components reviewed against style guide before implementation
- **Accessibility Testing**: Regular audits with screen readers and accessibility tools
- **Cross-Platform Testing**: Verify consistency across iOS, Android, and Web
- **Performance Monitoring**: Track animation performance and loading times
- **Component Testing**: Verify all NativeBase components work correctly across platforms
- **Dark Mode Testing**: Ensure all components work in both light and dark modes

---

*This style guide serves as the foundation for all FlirtCraft design decisions. Version 2.0 uses NativeBase as the core component library, React Native Gifted Chat for chat UI, and NativeWind 4.1 for utility styling, maintaining design consistency while leveraging battle-tested React Native tooling for reliability and developer experience.*