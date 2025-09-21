# FlirtCraft Design System

---
title: FlirtCraft Design System Overview
description: Comprehensive design system for building consistent, accessible, and engaging user interfaces
last-updated: 2025-08-30
version: 2.0.0
technology-stack:
  - NativeBase
  - React Native Gifted Chat
  - NativeWind 4.1
  - React Native Reanimated 3
related-files:
  - ./style-guide.md
  - ./tokens/README.md
  - ./tokens/nativebase-theme.md
  - ./components/README.md
  - ./platform-adaptations/README.md
status: implemented
---

## Overview

The FlirtCraft Design System is a comprehensive collection of reusable components, design tokens, patterns, and guidelines that ensure consistent, accessible, and engaging user experiences across all platforms. Built with a focus on confidence-building interactions and supportive user journeys, this system empowers teams to create interfaces that feel both professional and approachable.

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [System Architecture](#system-architecture)
3. [Getting Started](#getting-started)
4. [Core Principles](#core-principles)
5. [Token System](#token-system)
6. [Component Library](#component-library)
7. [Usage Guidelines](#usage-guidelines)
8. [Platform Adaptations](#platform-adaptations)
9. [Contributing](#contributing)

## Design Philosophy

### Confidence-Building Design
FlirtCraft's design system is built around the core mission of helping users build romantic conversation confidence. Every component, interaction, and visual element is designed to:

- **Reduce anxiety** through clear, predictable interfaces
- **Build confidence** with positive feedback and encouraging interactions
- **Support learning** through intuitive information architecture
- **Celebrate progress** with delightful but non-overwhelming animations
- **Maintain privacy** with clearly communicated data practices

### Visual Design Principles

#### Bold Simplicity with Intuitive Navigation
- **Clean layouts** that prioritize content over decoration
- **Clear visual hierarchy** that guides users naturally through tasks
- **Intuitive navigation patterns** that match user mental models
- **Frictionless interactions** that remove barriers to engagement

#### Breathable Whitespace and Strategic Color
- **Generous whitespace** that provides cognitive breathing room
- **Strategic color accents** that draw attention to important elements
- **Purposeful color usage** that supports rather than overwhelms
- **Consistent color meanings** that build user understanding over time

#### Systematic Typography and Motion
- **Clear typography hierarchy** that makes content scannable
- **Proportional scaling** that works across all device sizes
- **Physics-based motion** that feels natural and responsive
- **Purposeful animation** that communicates meaning and status

## System Architecture

### Token-Based Design
```
Design Tokens (Atomic Level)
├── Colors
├── Typography
├── Spacing
├── Animations
└── Breakpoints

↓ Tokens inform ↓

Components (Molecular Level)
├── Buttons
├── Form Elements
├── Cards
├── Navigation
└── Gamification Elements

↓ Components compose ↓

Patterns (Organism Level)
├── Conversation Interface
├── Progress Dashboards
├── Onboarding Flows
└── Achievement Systems

↓ Patterns form ↓

Templates (Page Level)
├── Conversation Screens
├── Profile Pages
├── Settings Interfaces
└── Analytics Dashboards
```

### Cross-Platform Consistency
The design system maintains visual and interaction consistency while respecting platform conventions:

- **Universal Components**: Core components that work across all platforms
- **Platform Adaptations**: Specific implementations for iOS, Android, and Web
- **Responsive Behavior**: Fluid layouts that work from mobile to desktop
- **Accessibility Standards**: WCAG AAA compliance across all implementations

## Getting Started

### For Designers

#### Design Tool Setup
1. **Figma Component Library**: Access the complete component library in Figma
2. **Token Plugin**: Install the design token plugin for automatic updates
3. **Style Guide Reference**: Bookmark the comprehensive style guide
4. **Platform Guidelines**: Review platform-specific adaptation guides

#### Design Workflow
```
Design Process:
1. Start with design tokens (colors, typography, spacing)
2. Use pre-built components from the library
3. Follow established patterns for complex interactions
4. Validate designs against accessibility checklist
5. Test responsive behavior across breakpoints
6. Document any new patterns or variations
```

### For Developers

#### Installation and Setup
```bash
# Install NativeBase and dependencies
npm install native-base react-native-safe-area-context react-native-svg
npm install react-native-gifted-chat
npm install nativewind

# iOS additional setup
cd ios && pod install
```

#### Project Configuration
```javascript
// App.js
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

#### Component Usage
```tsx
// NativeBase with FlirtCraft theme
import { Box, VStack, HStack, Button, Text, Pressable } from 'native-base';

function ConversationCard() {
  return (
    <Box 
      bg="white"
      rounded="2xl"
      p={6}
      shadow={3}
      _dark={{ bg: 'gray.900' }}
    >
      <VStack space={4}>
        <Text 
          fontSize="xl" 
          fontWeight="semibold" 
          color="gray.900"
          _dark={{ color: 'white' }}
        >
          Practice Conversation
        </Text>
        
        <Text 
          color="gray.600"
          _dark={{ color: 'gray.300' }}
        >
          Ready to practice your conversation skills in a coffee shop setting?
        </Text>
        
        <Button 
          colorScheme="primary"
          size="lg"
          onPress={handleStartConversation}
          mt={4}
        >
          Start Practice
        </Button>
      </VStack>
    </Box>
  );
}
```

#### React Native Gifted Chat Integration
```tsx
// Chat interface with FlirtCraft styling
import { GiftedChat, Bubble, InputToolbar } from 'react-native-gifted-chat';

const renderBubble = (props) => (
  <Bubble
    {...props}
    wrapperStyle={{
      right: { backgroundColor: '#F97316' },
      left: { backgroundColor: '#F3F4F6' }
    }}
    textStyle={{
      right: { color: '#FFFFFF' },
      left: { color: '#374151' }
    }}
  />
);

<GiftedChat
  messages={messages}
  onSend={onSend}
  user={{ _id: 1 }}
  renderBubble={renderBubble}
/>
```

## Core Principles

### 1. Consistency
**Principle**: Use established patterns and components to create predictable user experiences.

**Implementation**:
- Follow component specifications exactly
- Use design tokens instead of hardcoded values
- Apply patterns consistently across similar interactions
- Maintain visual and behavioral consistency across platforms

### 2. Accessibility
**Principle**: Design for users of all abilities and assistive technology needs.

**Implementation**:
- Meet WCAG AAA standards (7:1 contrast ratio when possible)
- Support screen readers with proper ARIA labeling
- Ensure keyboard navigation for all interactive elements
- Provide alternatives for motion-sensitive users
- Test with real users across disability spectrum

### 3. Scalability
**Principle**: Components and patterns should work efficiently at any scale.

**Implementation**:
- Token-based system allows easy theme updates
- Component composition supports complex interfaces
- Performance optimization built into all components
- Responsive design works from mobile to large desktop

### 4. User-Centered Design
**Principle**: Every design decision should serve user needs and goals.

**Implementation**:
- Prioritize user tasks over visual decoration
- Provide clear feedback for all user actions
- Support different user personas and skill levels
- Validate designs with user testing and feedback

### 5. Progressive Enhancement
**Principle**: Core functionality works everywhere, enhancements improve the experience.

**Implementation**:
- Essential features work without JavaScript
- Advanced interactions enhance but don't replace basic functionality
- Graceful degradation for older browsers or devices
- Offline functionality where appropriate

## Token System

### Design Token Categories

#### Color Tokens
```css
/* Primary Colors */
--color-primary: #F97316;           /* Orange - Main CTAs, brand elements */
--color-primary-dark: #EA580C;      /* Hover states, emphasis */
--color-primary-light: #FED7AA;     /* Backgrounds, highlights */

/* Semantic Colors */
--color-success: #10B981;           /* Positive actions, confirmations */
--color-warning: #F59E0B;           /* Caution states, alerts */
--color-error: #EF4444;             /* Errors, destructive actions */
--color-info: #3B82F6;              /* Informational messages */

/* Neutral Palette */
--color-neutral-50: #F9FAFB;        /* Lightest backgrounds */
--color-neutral-900: #111827;       /* Primary text */
```

#### Typography Tokens
```css
/* Font Families */
--font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-family-mono: 'JetBrains Mono', Consolas, monospace;

/* Font Scales */
--font-size-h1: clamp(2rem, 4vw, 3rem);     /* 32px - 48px */
--font-size-h2: clamp(1.5rem, 3vw, 2.25rem); /* 24px - 36px */
--font-size-body: 1rem;                       /* 16px */
--font-size-caption: 0.875rem;                /* 14px */

/* Line Heights */
--line-height-tight: 1.2;
--line-height-normal: 1.5;
--line-height-loose: 1.8;
```

#### Spacing Tokens
```css
/* Base spacing unit: 4px */
--space-xs: 0.25rem;    /* 4px */
--space-sm: 0.5rem;     /* 8px */
--space-md: 1rem;       /* 16px */
--space-lg: 1.5rem;     /* 24px */
--space-xl: 2rem;       /* 32px */
--space-2xl: 3rem;      /* 48px */
--space-3xl: 4rem;      /* 64px */
```

### Token Usage Guidelines

#### When to Use Tokens
- **Always**: Use tokens for colors, spacing, typography, and timing
- **Component Props**: Components accept token names as prop values
- **Custom Styles**: Reference tokens in custom CSS/styles
- **Platform Adaptations**: Tokens adapt automatically to platform conventions

#### When to Avoid Hardcoding
- **Never**: Hardcode hex colors, pixel values, or font sizes
- **Never**: Use magic numbers or arbitrary spacing values
- **Never**: Create one-off styles that don't follow the system
- **Exception**: Platform-specific values that can't be tokenized

## Component Library

### Component Categories

#### **Foundation Components**
- **Button**: Primary, secondary, ghost variants with multiple sizes
- **Text**: Typography component with semantic variants
- **Input**: Text fields, textareas, and specialized form inputs
- **Card**: Container component with elevation and spacing variants

#### **Navigation Components**
- **Tab Bar**: Bottom navigation for mobile apps
- **Navigation Header**: Top navigation with back buttons and actions
- **Menu**: Dropdown and slide-out menu components
- **Breadcrumbs**: Hierarchical navigation for deep content

#### **Feedback Components**
- **Progress Bar**: Linear progress indication with animations
- **Loading States**: Skeleton screens and spinner components
- **Toast Notifications**: Temporary message overlays
- **Modal Dialogs**: Centered overlay dialogs with focus management

#### **FlirtCraft-Specific Components**
- **Chat Bubble**: Conversation interface elements
- **XP Progress**: Gamification progress visualization
- **Achievement Badge**: Achievement unlock and display components
- **Streak Counter**: Daily streak tracking interface
- **Context Card**: Pre-conversation context display

### Component Documentation Structure
Each component includes:
- **Purpose and Usage**: When and why to use the component
- **Props and Variants**: All available customization options  
- **Accessibility Features**: Built-in accessibility support
- **Examples**: Code examples for common usage patterns
- **Do's and Don'ts**: Best practices and common mistakes to avoid

## Usage Guidelines

### Component Selection
1. **Start with Foundation**: Use basic components before creating custom solutions
2. **Compose Complexity**: Combine simple components to build complex interfaces
3. **Follow Patterns**: Use established patterns for common interaction flows
4. **Document Variations**: Record any new patterns for future reuse

### Customization Guidelines
1. **Use Design Tokens**: Customize through tokens, not hardcoded values
2. **Follow Brand Guidelines**: Maintain visual consistency with brand identity
3. **Test Accessibility**: Verify customizations don't break accessibility features
4. **Performance Impact**: Consider performance implications of customizations

### Quality Assurance
1. **Design Review**: All interfaces reviewed against design system standards
2. **Accessibility Testing**: Screen reader and keyboard navigation testing
3. **Cross-Platform Testing**: Verify functionality across all target platforms
4. **Performance Testing**: Ensure components meet performance benchmarks

## Platform Adaptations

### iOS Adaptations
- **Native Feel**: Components follow iOS Human Interface Guidelines
- **System Integration**: Uses iOS system fonts, colors, and interaction patterns
- **Accessibility**: Full VoiceOver and Switch Control support
- **Performance**: Optimized for iOS rendering and animation systems

### Android Adaptations
- **Material Design**: Components follow Material Design principles where appropriate
- **System Integration**: Respects Android system settings and preferences
- **Accessibility**: Complete TalkBack and system accessibility support
- **Performance**: Optimized for Android view system and animation framework

### Web Adaptations
- **Progressive Enhancement**: Works without JavaScript, enhanced with it
- **Responsive Design**: Fluid layouts from mobile to desktop
- **Browser Support**: Tested across modern browsers with graceful degradation
- **Web Standards**: Semantic HTML with proper ARIA labeling

## Contributing

### Design Contributions
1. **Propose New Components**: Submit component proposals with use case documentation
2. **Update Existing Components**: Suggest improvements with rationale and examples
3. **Submit Patterns**: Document new interaction patterns for community use
4. **Accessibility Improvements**: Contribute accessibility enhancements and testing

### Development Contributions
1. **Component Implementation**: Build new components following system standards
2. **Bug Fixes**: Report and fix issues in existing components
3. **Performance Optimization**: Improve component performance and bundle size
4. **Platform Support**: Add support for new platforms or framework versions

### Documentation Contributions
1. **Usage Examples**: Add practical examples and use cases
2. **Best Practices**: Document patterns and anti-patterns
3. **Accessibility Guides**: Contribute accessibility implementation guides
4. **Platform Guides**: Add platform-specific implementation details

---

## Quick Reference

### Essential Links
- [Complete Style Guide](./style-guide.md) - Visual specifications and migration guide
- [NativeBase Theme](./tokens/nativebase-theme.md) - Complete theme configuration
- [Design Tokens](./tokens/README.md) - Color, typography, and spacing foundations  
- [Component Library](./components/README.md) - Complete component documentation
- [Platform Adaptations](./platform-adaptations/README.md) - iOS, Android, and Web specifics
- [Accessibility Guidelines](../accessibility/guidelines.md) - Comprehensive accessibility standards

### Design Resources
- **Figma Library**: [FlirtCraft Design System Components](link-to-figma)
- **Token Generator**: Automated design token generation and distribution
- **Icon Library**: SVG icon set with accessibility features built-in
- **Brand Assets**: Logo variations, photography guidelines, and brand resources

### Development Resources
- **NativeBase**: `native-base` for comprehensive UI components
- **React Native Gifted Chat**: `react-native-gifted-chat` for chat interface
- **NativeWind**: `nativewind` for utility-first styling
- **Theme Configuration**: Complete NativeBase theme with FlirtCraft tokens
- **Code Templates**: Migration examples and implementation patterns
- **Testing Utilities**: Automated accessibility and visual regression testing

## Technology Stack v2.0

### Current Implementation
- **NativeBase**: Battle-tested component library with extensive community support
- **React Native Gifted Chat**: Mature chat interface with customizable components  
- **NativeWind 4.1**: Utility-first styling with enhanced dark mode support

### Migration Benefits
- **Better Performance**: Smaller bundle size and faster rendering
- **Enhanced TypeScript**: Full type safety with better IntelliSense
- **Dark Mode**: Built-in dark mode support across all components
- **Web Support**: Better cross-platform compatibility
- **Maintenance**: Reduced custom code with proven libraries

### Migration Guide
See [Style Guide Migration Section](./style-guide.md#technology-stack-migration) for detailed component mappings and examples.

---

*The FlirtCraft Design System v2.0 serves the fundamental mission of building user confidence in romantic conversations by providing consistent, accessible, and engaging interface patterns built on proven React Native tooling. This version leverages NativeBase, React Native Gifted Chat, and NativeWind 4.1 to deliver reliable performance, excellent developer experience, and comprehensive dark mode support while maintaining the core design principles that reduce anxiety and support learning throughout the user's journey.*