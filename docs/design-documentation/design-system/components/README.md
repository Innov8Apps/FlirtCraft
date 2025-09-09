# FlirtCraft Component Library

---
title: Component Library Overview and Standards
description: Comprehensive UI component specifications for consistent implementation
last-updated: 2025-08-23
version: 1.0.0
related-files:
  - ../style-guide.md
  - ./buttons.md
  - ./cards.md
  - ./forms.md
  - ./navigation.md
dependencies:
  - NativeBase foundation components
  - NativeWind utility classes
  - React Native Reanimated animations
status: approved
---

## Component Library Philosophy

FlirtCraft's component library prioritizes psychological safety and confidence-building through consistent, accessible design patterns. Every component is designed to reduce user anxiety while providing clear interaction feedback and maintaining visual appeal.

## Design Principles

### Accessibility First
- **WCAG 2.1 AA compliance** minimum for all components
- **44×44px minimum touch targets** for all interactive elements
- **Clear focus indicators** with consistent visual treatment
- **Screen reader optimization** with proper semantic markup and ARIA labels

### Confidence Building
- **Encouraging visual feedback** for all user interactions
- **Clear state communication** preventing user uncertainty
- **Forgiving interaction patterns** that accommodate user mistakes
- **Progressive disclosure** to prevent cognitive overload

### Consistency and Performance
- **Systematic visual language** across all components
- **Smooth animations** targeting 60fps performance
- **Platform conventions** respecting iOS and Android patterns
- **Scalable architecture** supporting future feature expansion

## Component Categories

### Core Interactive Elements
- **[Buttons](./buttons.md)** - Primary actions, secondary actions, ghost buttons
- **[Form Elements](./forms.md)** - Text inputs, selectors, validation states
- **[Navigation](./navigation.md)** - Tab bars, headers, back navigation

### Content Display
- **[Cards](./cards.md)** - Scenario cards, feedback cards, progress cards
- **[Lists](./lists.md)** - Message lists, achievement lists, preference lists
- **[Modals](./modals.md)** - Confirmation dialogs, settings panels, help overlays

### Specialized Components
- **[Chat Interface](./chat.md)** - Message bubbles, input fields, typing indicators
- **[Progress Elements](./progress.md)** - Score circles, progress bars, achievement badges
- **[Context Panels](./context.md)** - Pre-conversation context, helper panels

## Component Specifications Standard

### Required Documentation for Each Component

#### Visual Specifications
- **Dimensions**: Exact measurements in px/rem
- **Colors**: Specific color tokens from design system
- **Typography**: Font size, weight, line height from type scale
- **Spacing**: Internal padding and external margins
- **Border Radius**: Corner treatments for brand consistency
- **Shadows**: Elevation and depth specifications

#### Interactive States
- **Default**: Standard appearance and behavior
- **Hover**: Desktop/cursor interaction feedback (where applicable)
- **Active**: Press state with appropriate feedback
- **Focus**: Keyboard navigation and accessibility focus
- **Disabled**: Non-interactive state with clear visual indication
- **Loading**: Processing state with appropriate feedback

#### Responsive Behavior
- **Mobile**: Primary target platform adaptations
- **Tablet**: Medium screen size adjustments  
- **Desktop**: Large screen optimizations (future web version)
- **Breakpoint Handling**: Smooth transitions between screen sizes

#### Accessibility Requirements
- **Semantic Markup**: Proper HTML/React Native roles and properties
- **ARIA Labels**: Descriptive labels for screen readers
- **Keyboard Support**: Complete keyboard navigation capability
- **Focus Management**: Logical tab order and focus indicators
- **Screen Reader**: Optimized announcements and descriptions

## Implementation Standards

### NativeBase Integration
**Component Extension Pattern:**
```jsx
import { Button as NBButton } from 'native-base'
import { useTheme } from '../theme/ThemeProvider'

export const Button = ({ variant = 'primary', size = 'medium', ...props }) => {
  const theme = useTheme()
  
  return (
    <NBButton
      {...props}
      variant={variant}
      size={size}
      _pressed={{ transform: [{ scale: 0.95 }] }}
      // Additional FlirtCraft customizations
    />
  )
}
```

### NativeWind Styling
**Utility Class Pattern:**
```jsx
import { styled } from 'nativewind'
import { Pressable } from 'react-native'

const StyledPressable = styled(Pressable)

export const CustomButton = ({ className, ...props }) => (
  <StyledPressable
    className={`
      bg-primary-500 px-6 py-3 rounded-xl
      active:scale-95 transition-transform duration-100
      ${className}
    `}
    {...props}
  />
)
```

### Animation Implementation
**React Native Reanimated 3 Pattern:**
```jsx
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring 
} from 'react-native-reanimated'

export const AnimatedButton = ({ children, onPress, ...props }) => {
  const scale = useSharedValue(1)
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }]
  }))
  
  const handlePressIn = () => {
    scale.value = withSpring(0.95, { damping: 15, stiffness: 150 })
  }
  
  const handlePressOut = () => {
    scale.value = withSpring(1, { damping: 15, stiffness: 150 })
  }
  
  return (
    <Animated.View style={animatedStyle}>
      <Pressable
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        onPress={onPress}
        {...props}
      >
        {children}
      </Pressable>
    </Animated.View>
  )
}
```

## Quality Assurance Standards

### Visual Consistency Checklist
- [ ] **Color Usage**: Only design system colors used
- [ ] **Typography**: Matches established type scale
- [ ] **Spacing**: Uses systematic spacing scale
- [ ] **Border Radius**: Consistent with component family
- [ ] **Shadows**: Appropriate elevation level

### Accessibility Validation
- [ ] **Touch Targets**: Meet 44×44px minimum requirement
- [ ] **Contrast Ratios**: Pass WCAG AA standards (4.5:1 minimum)
- [ ] **Focus Indicators**: Visible and consistent
- [ ] **Screen Reader**: Tested with VoiceOver/TalkBack
- [ ] **Keyboard Navigation**: Complete functionality via keyboard

### Performance Verification
- [ ] **Animation Performance**: 60fps on target devices
- [ ] **Memory Usage**: No significant memory leaks
- [ ] **Bundle Size**: Component tree-shaking enabled
- [ ] **Rendering**: Optimized re-render patterns

### Cross-Platform Testing
- [ ] **iOS Appearance**: Matches design specifications
- [ ] **Android Appearance**: Consistent cross-platform experience
- [ ] **Device Variations**: Tested on various screen sizes
- [ ] **Platform Conventions**: Respects native interaction patterns

## Component Usage Guidelines

### When to Create New Components
**Create New Component When:**
- Pattern used 3+ times across the app
- Complex interaction logic needs encapsulation
- Specific accessibility requirements need standardization
- Platform-specific behavior requires abstraction

**Extend Existing When:**
- Minor visual variations of existing component
- Additional props or configuration needed
- Platform-specific styling adjustments required

### Naming Conventions
**Component Names:**
- PascalCase for component names (`MessageBubble`, `ScenarioCard`)
- Descriptive names indicating function (`ProgressRing`, `DifficultySelector`)
- Avoid generic names like `Card` or `Button` (use `ScenarioCard`, `PrimaryButton`)

**Props and Variants:**
- Consistent variant names across component family
- Boolean props use positive naming (`isDisabled` not `disabled`)
- Event handlers follow `onEventName` pattern

### Documentation Requirements
**Each Component Must Include:**
- Purpose and use case description
- Visual design specifications
- Complete props interface
- Usage examples with code
- Accessibility implementation notes
- Platform-specific considerations

## Component Development Workflow

### Design to Development Handoff
1. **Design Review**: Component specifications reviewed against design system
2. **API Design**: Props interface designed for flexibility and consistency
3. **Implementation**: Component built following established patterns
4. **Testing**: Visual, accessibility, and performance testing completed
5. **Documentation**: Usage guidelines and examples created
6. **Review**: Code review focusing on consistency and performance

### Version Control and Updates
**Semantic Versioning:**
- **Major**: Breaking API changes
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes and small improvements

**Change Management:**
- All breaking changes require migration guide
- Deprecated components supported for 2 version releases
- New components require approval from design system team

---

*This component library serves as the foundation for consistent, accessible, and confidence-building user experiences throughout FlirtCraft. Regular maintenance and updates ensure the library evolves with user needs and platform capabilities.*