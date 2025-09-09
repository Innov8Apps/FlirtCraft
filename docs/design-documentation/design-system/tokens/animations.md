# Animation Tokens

---
title: FlirtCraft Animation System
description: Motion design tokens including timing functions, durations, and easing curves
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../../accessibility/guidelines.md
dependencies:
  - React Native Reanimated 3
  - Platform-specific animation APIs
status: approved
---

## Overview

FlirtCraft's animation system creates delightful, purposeful motion that enhances user experience without causing distraction or accessibility issues. Every animation serves a functional purpose: providing feedback, guiding attention, or communicating state changes.

## Animation Philosophy

### Core Principles

**Purposeful Motion:**
- Every animation has a clear functional purpose
- No motion for decoration alone
- Animations guide user attention and understanding

**Performance First:**
- Target 60fps on all supported devices
- Use hardware-accelerated properties (transform, opacity)
- Optimize for battery efficiency

**Accessibility Minded:**
- Respect `prefers-reduced-motion` settings
- Provide instant alternatives for critical interactions
- Never rely solely on motion to convey information

## Timing Function Tokens

### Easing Curves

**Ease Out** - `animation-easing-out`
**Value**: `cubic-bezier(0.0, 0, 0.2, 1)`
**Usage:**
- Element entrances and expansions
- Natural deceleration feeling
- Content appearing and growing

**Examples:**
- Modal slide-up animations
- Button press feedback
- Card hover effects
- Progress bar filling

```css
/* CSS implementation */
transition-timing-function: cubic-bezier(0.0, 0, 0.2, 1);
```

```jsx
// React Native Reanimated implementation
import { withSpring, withTiming } from 'react-native-reanimated';

const slideUp = withTiming(0, {
  duration: 300,
  easing: Easing.out(Easing.cubic)
});
```

**Ease In Out** - `animation-easing-in-out`
**Value**: `cubic-bezier(0.4, 0, 0.6, 1)`
**Usage:**
- Smooth transitions between states
- Position changes and movements
- Balanced acceleration and deceleration

**Examples:**
- Tab switching animations
- Carousel transitions
- Menu item rearrangement
- Content sliding

**Ease In** - `animation-easing-in`
**Value**: `cubic-bezier(0.4, 0, 1, 1)`
**Usage:**
- Element exits and disappearing
- Natural acceleration feeling
- Reverse of entrance animations

**Examples:**
- Modal dismissal
- Button release
- Element fade out
- Slide down exits

**Spring** - `animation-easing-spring`
**Values**: 
```json
{
  "gentle": { "tension": 200, "friction": 25 },
  "bouncy": { "tension": 300, "friction": 20 },
  "stiff": { "tension": 400, "friction": 30 }
```
**Usage:**
- Playful interactions and feedback
- Natural, physics-based motion
- Interactive element responses

**Examples:**
- Achievement badge appearances
- Button press feedback
- Interactive card selections
- Gamification celebrations

## Duration Scale Tokens

### Micro Animations

**Micro Duration** - `animation-duration-micro`
**Value**: `100-150ms`
**Usage:**
- Instant feedback interactions
- State change indicators
- Hover effects
- Focus indicators

**Examples:**
- Button color changes
- Input field focus
- Icon state changes
- Small element highlighting

```jsx
// React Native implementation
const microFeedback = withTiming(newValue, {
  duration: 120,
  easing: Easing.out(Easing.cubic)
});
```

### Short Animations

**Short Duration** - `animation-duration-short`
**Value**: `200-300ms`
**Usage:**
- Local transitions
- Component state changes
- Dropdown appearances
- Quick user feedback

**Examples:**
- Dropdown menu opening
- Tooltip appearances
- Button press feedback
- Small modal presentations

```jsx
const shortTransition = withTiming(newValue, {
  duration: 250,
  easing: Easing.out(Easing.cubic)
});
```

### Medium Animations

**Medium Duration** - `animation-duration-medium`
**Value**: `400-500ms`
**Usage:**
- Page transitions
- Modal presentations
- Card flips and rotations
- Content area changes

**Examples:**
- Screen navigation transitions
- Modal slide-up animations
- Tab content switching
- Card expansion/collapse

```jsx
const mediumTransition = withSpring(newValue, {
  tension: 200,
  friction: 25
});
```

### Long Animations

**Long Duration** - `animation-duration-long`
**Value**: `600-800ms`
**Usage:**
- Complex animations
- Celebration sequences
- Onboarding flows
- Major state changes

**Examples:**
- Level-up celebrations
- Achievement unlock sequences
- Complex onboarding transitions
- Major layout changes

```jsx
const longCelebration = withSequence(
  withTiming(1.1, { duration: 300 }),
  withSpring(1.0, { tension: 300, friction: 20 })
);
```

## Animation Pattern Tokens

### Entrance Animations

**Fade In** - `animation-pattern-fade-in`
```json
{
  "duration": "300ms",
  "easing": "ease-out",
  "properties": {
    "opacity": "0 → 1"
  }
}
```

**Slide Up** - `animation-pattern-slide-up`
```json
{
  "duration": "400ms", 
  "easing": "ease-out",
  "properties": {
    "transform": "translateY(20px) → translateY(0)",
    "opacity": "0 → 1"
  }
}
```

**Scale In** - `animation-pattern-scale-in`
```json
{
  "duration": "250ms",
  "easing": "spring",
  "properties": {
    "transform": "scale(0.8) → scale(1.0)",
    "opacity": "0 → 1"
  }
}
```

### Exit Animations

**Fade Out** - `animation-pattern-fade-out`
```json
{
  "duration": "200ms",
  "easing": "ease-in", 
  "properties": {
    "opacity": "1 → 0"
  }
}
```

**Slide Down** - `animation-pattern-slide-down`
```json
{
  "duration": "300ms",
  "easing": "ease-in",
  "properties": {
    "transform": "translateY(0) → translateY(20px)",
    "opacity": "1 → 0"
  }
}
```

**Scale Out** - `animation-pattern-scale-out`
```json
{
  "duration": "200ms",
  "easing": "ease-in",
  "properties": {
    "transform": "scale(1.0) → scale(0.8)",
    "opacity": "1 → 0"
  }
}
```

### Transition Animations

**Slide Left** - `animation-pattern-slide-left`
```json
{
  "duration": "300ms",
  "easing": "ease-in-out",
  "properties": {
    "transform": "translateX(100%) → translateX(0)"
  }
}
```

**Slide Right** - `animation-pattern-slide-right`
```json
{
  "duration": "300ms", 
  "easing": "ease-in-out",
  "properties": {
    "transform": "translateX(-100%) → translateX(0)"
  }
}
```

**Cross Fade** - `animation-pattern-cross-fade`
```json
{
  "duration": "200ms",
  "easing": "ease-in-out",
  "stagger": "50ms",
  "properties": {
    "outgoing": { "opacity": "1 → 0" },
    "incoming": { "opacity": "0 → 1" }
  }
}
```

## Component-Specific Animation Tokens

### Button Animations

**Button Press** - `animation-button-press`
```json
{
  "press": {
    "duration": "100ms",
    "easing": "ease-in",
    "transform": "scale(0.98)"
  },
  "release": {
    "duration": "200ms", 
    "easing": "ease-out",
    "transform": "scale(1.0)"
  }
}
```

**Button Hover** - `animation-button-hover`
```json
{
  "duration": "150ms",
  "easing": "ease-out",
  "properties": {
    "transform": "translateY(-1px)",
    "shadow": "increase elevation"
  }
}
```

### Card Animations

**Card Hover** - `animation-card-hover`
```json
{
  "duration": "200ms",
  "easing": "ease-out", 
  "properties": {
    "transform": "translateY(-2px) scale(1.02)",
    "shadow": "0 4px 16px rgba(0,0,0,0.15)"
  }
}
```

**Card Selection** - `animation-card-selection`
```json
{
  "duration": "300ms",
  "easing": "spring",
  "properties": {
    "border": "animate to primary color",
    "shadow": "increase elevation",
    "transform": "scale(1.02)"
  }
}
```

### Modal Animations

**Modal Present** - `animation-modal-present`
```json
{
  "backdrop": {
    "duration": "300ms",
    "easing": "ease-out",
    "opacity": "0 → 0.5"
  },
  "content": {
    "duration": "400ms",
    "easing": "ease-out", 
    "transform": "translateY(100%) → translateY(0)",
    "stagger": "100ms"
  }
}
```

**Modal Dismiss** - `animation-modal-dismiss`
```json
{
  "content": {
    "duration": "300ms",
    "easing": "ease-in",
    "transform": "translateY(0) → translateY(100%)"
  },
  "backdrop": {
    "duration": "200ms",
    "easing": "ease-in",
    "opacity": "0.5 → 0",
    "delay": "100ms"
  }
}
```

### Navigation Animations

**Stack Push** - `animation-nav-push`
```json
{
  "duration": "300ms",
  "easing": "ease-out",
  "incoming": {
    "transform": "translateX(100%) → translateX(0)"
  },
  "outgoing": {
    "transform": "translateX(0) → translateX(-20%)",
    "opacity": "1 → 0.3"
  }
}
```

**Stack Pop** - `animation-nav-pop`
```json
{
  "duration": "250ms", 
  "easing": "ease-in-out",
  "incoming": {
    "transform": "translateX(-20%) → translateX(0)",
    "opacity": "0.3 → 1"
  },
  "outgoing": {
    "transform": "translateX(0) → translateX(100%)"
  }
}
```

**Tab Switch** - `animation-nav-tab`
```json
{
  "duration": "200ms",
  "easing": "ease-in-out", 
  "crossFade": true,
  "properties": {
    "opacity": "0 → 1"
  }
}
```

## Feedback Animation Tokens

### Loading States

**Spinner** - `animation-loading-spinner`
```json
{
  "duration": "1000ms",
  "easing": "linear",
  "repeat": "infinite",
  "transform": "rotate(0deg) → rotate(360deg)"
}
```

**Progress Bar** - `animation-loading-progress`
```json
{
  "duration": "variable",
  "easing": "ease-out",
  "properties": {
    "width": "animate to completion percentage"
  }
}
```

**Skeleton Shimmer** - `animation-loading-skeleton`
```json
{
  "duration": "1500ms",
  "easing": "ease-in-out", 
  "repeat": "infinite",
  "properties": {
    "background": "shimmer gradient animation"
  }
}
```

### Success Celebrations

**Achievement Unlock** - `animation-celebration-achievement`
```json
{
  "sequence": [
    {
      "duration": "300ms",
      "easing": "spring", 
      "transform": "scale(0) → scale(1.1)"
    },
    {
      "duration": "200ms",
      "easing": "ease-out",
      "transform": "scale(1.1) → scale(1.0)"
    }
  ],
  "particles": {
    "duration": "800ms",
    "count": 12,
    "spread": "radial"
  }
}
```

**Level Up** - `animation-celebration-level-up`
```json
{
  "sequence": [
    {
      "duration": "500ms",
      "easing": "ease-out",
      "properties": {
        "transform": "scale(1.0) → scale(1.2)",
        "glow": "add golden glow effect"
      }
    },
    {
      "duration": "400ms", 
      "easing": "spring",
      "transform": "scale(1.2) → scale(1.0)"
    }
  ],
  "particles": "celebration burst"
}
```

**Streak Milestone** - `animation-celebration-streak`
```json
{
  "duration": "600ms",
  "easing": "bounce",
  "properties": {
    "transform": "scale(1.0) → scale(1.15) → scale(1.0)",
    "glow": "fire effect animation"
  }
}
```

### Error States

**Input Error** - `animation-feedback-error`
```json
{
  "duration": "150ms",
  "easing": "ease-in-out",
  "repeat": 2,
  "properties": {
    "transform": "translateX(0) → translateX(4px) → translateX(-4px) → translateX(0)",
    "border": "animate to error color"
  }
}
```

**Connection Error** - `animation-feedback-connection-error`
```json
{
  "duration": "300ms",
  "easing": "ease-out",
  "properties": {
    "opacity": "fade in error state",
    "background": "animate to error background"
  }
}
```

## Accessibility Animation Tokens

### Reduced Motion Tokens

**Reduced Motion Duration** - `animation-duration-reduced`
**Value**: `0ms` or `50ms` maximum
**Usage:** When user prefers reduced motion

**Reduced Motion Easing** - `animation-easing-reduced`
**Value**: `linear` or `ease`
**Usage:** Simple easing for minimal motion

**Instant Feedback** - `animation-instant`
```json
{
  "duration": "0ms",
  "properties": {
    "all": "instant state change"
  }
}
```

### High Contrast Animations

**Focus Animations** - `animation-focus-high-contrast`
```json
{
  "duration": "100ms",
  "easing": "ease-out",
  "properties": {
    "outline": "high contrast focus ring",
    "background": "high contrast background"
  }
}
```

## Performance Optimization Tokens

### Hardware Accelerated Properties

**Preferred Properties** - `animation-properties-optimized`
```json
[
  "transform",
  "opacity", 
  "filter"
]
```

**Avoid Properties** - `animation-properties-avoid`
```json
[
  "width",
  "height",
  "padding",
  "margin",
  "border-width"
]
```

### Memory Management

**Animation Cleanup** - `animation-cleanup`
```json
{
  "autoCancel": true,
  "memoryOptimized": true,
  "cleanupDelay": "200ms"
}
```

## Platform-Specific Animation Tokens

### iOS Animations

**iOS Spring** - `animation-ios-spring`
```json
{
  "tension": 157,
  "friction": 26,
  "mass": 1
}
```

**iOS Navigation** - `animation-ios-navigation`
```json
{
  "duration": "350ms",
  "easing": "cubic-bezier(0.4, 0.0, 0.2, 1.0)",
  "type": "slide"
}
```

### Android Animations

**Material Motion** - `animation-android-material`
```json
{
  "accelerate": "cubic-bezier(0.4, 0.0, 1, 1)",
  "decelerate": "cubic-bezier(0.0, 0.0, 0.2, 1)", 
  "standard": "cubic-bezier(0.4, 0.0, 0.2, 1)"
}
```

**Android Navigation** - `animation-android-navigation`
```json
{
  "duration": "300ms",
  "easing": "cubic-bezier(0.4, 0.0, 0.2, 1)",
  "type": "elevation"
}
```

## Usage Guidelines

### When to Animate

**Always Animate:**
- State changes that need user attention
- Navigation transitions
- User feedback (button presses, form submissions)
- Loading states and progress indicators

**Sometimes Animate:**
- Content updates and refreshes
- Secondary user interactions
- Decorative elements (sparingly)

**Never Animate:**
- Critical error messages (use instant state changes)
- When user has motion sensitivity
- Content that needs immediate attention

### Performance Best Practices

**Optimization Rules:**
1. Use transform and opacity properties when possible
2. Enable hardware acceleration with `will-change` or native flags
3. Limit simultaneous animations
4. Clean up animation resources after completion
5. Test on low-end devices

**Memory Management:**
- Cancel animations when components unmount
- Avoid memory leaks with proper cleanup
- Use animation pools for repeated animations

## Implementation Examples

### React Native Implementation

```jsx
import { useSharedValue, withSpring, withTiming, useAnimatedStyle } from 'react-native-reanimated';
import { Easing } from 'react-native-reanimated';

const AnimatedButton = ({ onPress, children }) => {
  const scale = useSharedValue(1);
  const pressed = useSharedValue(false);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePressIn = () => {
    pressed.value = true;
    scale.value = withTiming(0.98, {
      duration: 100,
      easing: Easing.out(Easing.cubic),
    });
  };

  const handlePressOut = () => {
    pressed.value = false;
    scale.value = withSpring(1.0, {
      tension: 300,
      friction: 20,
    });
  };

  return (
    <AnimatedTouchableOpacity
      style={animatedStyle}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={onPress}
    >
      {children}
    </AnimatedTouchableOpacity>
  );
};
```

### CSS Implementation

```css
/* Animation token CSS custom properties */
:root {
  --animation-duration-micro: 120ms;
  --animation-duration-short: 250ms;
  --animation-duration-medium: 400ms;
  --animation-duration-long: 600ms;
  
  --animation-easing-out: cubic-bezier(0.0, 0, 0.2, 1);
  --animation-easing-in-out: cubic-bezier(0.4, 0, 0.6, 1);
  --animation-easing-in: cubic-bezier(0.4, 0, 1, 1);
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  :root {
    --animation-duration-micro: 0ms;
    --animation-duration-short: 0ms;
    --animation-duration-medium: 50ms;
    --animation-duration-long: 50ms;
  }
}

/* Button animation example */
.button {
  transition: 
    transform var(--animation-duration-micro) var(--animation-easing-out),
    box-shadow var(--animation-duration-short) var(--animation-easing-out);
}

.button:active {
  transform: scale(0.98);
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
```

## Token Export Format

### JSON Export Structure

```json
{
  "animations": {
    "durations": {
      "micro": "120ms",
      "short": "250ms", 
      "medium": "400ms",
      "long": "600ms"
    },
    "easings": {
      "out": "cubic-bezier(0.0, 0, 0.2, 1)",
      "inOut": "cubic-bezier(0.4, 0, 0.6, 1)",
      "in": "cubic-bezier(0.4, 0, 1, 1)",
      "spring": {
        "gentle": { "tension": 200, "friction": 25 },
        "bouncy": { "tension": 300, "friction": 20 }
      }
    },
    "patterns": {
      "fadeIn": {
        "duration": "300ms",
        "easing": "out",
        "properties": { "opacity": "0 → 1" }
      },
      "slideUp": {
        "duration": "400ms",
        "easing": "out", 
        "properties": {
          "transform": "translateY(20px) → translateY(0)",
          "opacity": "0 → 1"
        }
      }
    },
    "components": {
      "button": {
        "press": {
          "duration": "100ms",
          "easing": "in",
          "transform": "scale(0.98)"
        }
      },
      "modal": {
        "present": {
          "duration": "400ms",
          "easing": "out"
        }
      }
    },
    "accessibility": {
      "reducedMotion": {
        "maxDuration": "50ms",
        "preferredEasing": "linear"
      }
    }
  }
}
```

---

## Related Documentation

- [Component Animations](../components/) - Specific component animation usage
- [Style Guide](../style-guide.md) - Animation principles in design system
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Animation accessibility requirements
- [Platform Adaptations](../platform-adaptations/) - Platform-specific animation implementations

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*