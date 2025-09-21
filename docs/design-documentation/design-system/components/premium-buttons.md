# Premium Button Components for FlirtCraft

---
title: FlirtCraft Premium Button System
description: Advanced button components with sophisticated animations and orange-only color system
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./buttons.md
  - ../tokens/colors.md
  - ../tokens/premium-animations.md
dependencies:
  - React Native Reanimated 3
  - React Native Gesture Handler
  - Expo Linear Gradient
status: draft
---

## Design Philosophy

FlirtCraft's premium button system creates confidence-building interactions through sophisticated animations, warm orange gradients, and tactile feedback that feels both premium and approachable. Every button interaction reinforces the user's sense of progress and capability.

### Button Hierarchy
1. **Hero CTA** - Primary onboarding actions that build maximum confidence
2. **Primary Button** - Main actions and positive forward progress
3. **Secondary Button** - Supporting actions and alternative paths
4. **Tertiary Button** - Subtle actions and navigation helpers
5. **Icon Button** - Compact actions with sophisticated micro-interactions

## Hero CTA Button

### Visual Specifications
```javascript
export const HeroCTAButton = {
  // Base styling
  base: {
    minHeight: 56,
    minWidth: 280,
    borderRadius: 16,
    paddingHorizontal: 32,
    paddingVertical: 16,
    
    // Premium gradient background
    background: 'linear-gradient(135deg, #F97316 0%, #FB923C 50%, #FF8C42 100%)',
    
    // Sophisticated shadow system
    shadowColor: 'rgba(249, 115, 22, 0.25)',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 1,
    shadowRadius: 20,
    elevation: 12,
    
    // Typography
    textColor: '#FFFFFF',
    fontSize: 18,
    fontWeight: '700',
    letterSpacing: 0.5,
    textAlign: 'center',
    
    // Advanced text shadow for depth
    textShadowColor: 'rgba(0, 0, 0, 0.2)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2
  },
  
  // Interaction states with premium animations
  states: {
    default: {
      scale: 1,
      opacity: 1,
      shadowOpacity: 1,
      shadowRadius: 20,
      
      // Subtle breathing animation when idle
      breathingEffect: {
        scale: [1, 1.01, 1],
        shadowOpacity: [1, 0.8, 1],
        timing: {
          duration: 3000,
          repeat: -1,
          easing: 'easeInOut'
        }
      }
    },
    
    hover: {
      scale: 1.02,
      shadowOpacity: 1,
      shadowRadius: 24,
      shadowOffset: { width: 0, height: 12 },
      
      // Gradient intensity increase
      backgroundGradient: 'linear-gradient(135deg, #FF8C42 0%, #F97316 50%, #E65100 100%)',
      
      transition: {
        duration: 200,
        easing: 'confidenceOut'
      }
    },
    
    pressIn: {
      scale: 0.98,
      shadowOpacity: 0.6,
      shadowRadius: 12,
      shadowOffset: { width: 0, height: 4 },
      
      transition: {
        duration: 100,
        easing: 'easeIn'
      }
    },
    
    pressOut: {
      scale: 1.02,
      shadowOpacity: 1,
      shadowRadius: 24,
      
      // Energetic spring back
      transition: {
        type: 'spring',
        stiffness: 400,
        damping: 15,
        duration: 300
      }
    },
    
    loading: {
      opacity: 0.8,
      
      // Sophisticated loading animation
      loadingOverlay: {
        background: 'rgba(255, 255, 255, 0.15)',
        borderRadius: 'inherit'
      },
      
      // Spinner with brand colors
      spinner: {
        size: 24,
        color: '#FFFFFF',
        animation: {
          rotate: [0, 360],
          duration: 1000,
          repeat: -1,
          easing: 'linear'
        }
      }
    },
    
    disabled: {
      opacity: 0.5,
      scale: 1,
      shadowOpacity: 0.3,
      
      background: 'linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%)',
      
      // No interactions allowed
      pointerEvents: 'none'
    }
  },
  
  // Special effects
  effects: {
    // Ripple effect on press
    ripple: {
      backgroundColor: 'rgba(255, 255, 255, 0.25)',
      scale: [0, 4],
      opacity: [0.8, 0],
      borderRadius: '50%',
      
      animation: {
        duration: 600,
        easing: 'easeOut'
      }
    },
    
    // Success completion animation
    successPulse: {
      scale: [1, 1.05, 1],
      shadowOpacity: [1, 0.4, 1],
      
      timing: {
        duration: 800,
        repeat: 2,
        easing: 'confidenceOut'
      }
    },
    
    // Particle burst on successful action
    particleBurst: {
      count: 8,
      colors: ['#FFFFFF', 'rgba(255, 255, 255, 0.8)'],
      
      animation: {
        translateX: () => (Math.random() - 0.5) * 60,
        translateY: () => (Math.random() - 0.5) * 60,
        scale: [0, 1, 0],
        opacity: [0, 1, 0],
        
        timing: {
          duration: 800,
          stagger: 50,
          easing: 'easeOut'
        }
      }
    }
  }
}
```

### Implementation Example
```javascript
import { useConfidenceButtonAnimation } from '../hooks/useConfidenceButtonAnimation'

const HeroCTAButton = ({ onPress, children, loading = false, disabled = false }) => {
  const {
    animatedStyle,
    gestureHandler,
    triggerSuccessEffect
  } = useConfidenceButtonAnimation()
  
  const handlePress = () => {
    triggerSuccessEffect()
    onPress?.()
  }
  
  return (
    <GestureDetector gesture={gestureHandler}>
      <Animated.View style={[styles.heroButton, animatedStyle]}>
        <LinearGradient
          colors={['#F97316', '#FB923C', '#FF8C42']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.gradient}
        >
          <Pressable
            onPress={handlePress}
            disabled={disabled || loading}
            style={styles.pressable}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" size="small" />
            ) : (
              <Text style={styles.buttonText}>{children}</Text>
            )}
          </Pressable>
        </LinearGradient>
      </Animated.View>
    </GestureDetector>
  )
}
```

## Primary Button

### Visual Specifications
```javascript
export const PrimaryButton = {
  base: {
    minHeight: 52,
    borderRadius: 14,
    paddingHorizontal: 24,
    paddingVertical: 14,
    
    background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
    
    shadowColor: 'rgba(249, 115, 22, 0.2)',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 1,
    shadowRadius: 16,
    elevation: 8,
    
    textColor: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    letterSpacing: 0.3
  },
  
  variants: {
    // Standard primary
    standard: {
      minWidth: 200,
      justifyContent: 'center'
    },
    
    // Compact for forms
    compact: {
      minHeight: 48,
      paddingHorizontal: 20,
      fontSize: 15
    },
    
    // Full width for mobile
    fullWidth: {
      alignSelf: 'stretch',
      minWidth: '100%'
    },
    
    // Icon with text
    withIcon: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: 8
    }
  },
  
  states: {
    default: {
      scale: 1,
      opacity: 1
    },
    
    hover: {
      scale: 1.01,
      shadowRadius: 20,
      shadowOffset: { width: 0, height: 8 },
      
      backgroundGradient: 'linear-gradient(135deg, #FB923C 0%, #F97316 100%)',
      
      transition: {
        duration: 200,
        easing: 'confidenceOut'
      }
    },
    
    pressIn: {
      scale: 0.97,
      shadowRadius: 8,
      shadowOffset: { width: 0, height: 3 },
      
      transition: {
        duration: 100,
        easing: 'easeIn'
      }
    },
    
    pressOut: {
      scale: 1.01,
      shadowRadius: 20,
      
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 20
      }
    },
    
    loading: {
      opacity: 0.8,
      
      spinner: {
        size: 20,
        color: '#FFFFFF'
      }
    },
    
    disabled: {
      opacity: 0.4,
      background: 'linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%)',
      pointerEvents: 'none'
    }
  }
}
```

## Secondary Button

### Visual Specifications
```javascript
export const SecondaryButton = {
  base: {
    minHeight: 48,
    borderRadius: 12,
    paddingHorizontal: 20,
    paddingVertical: 12,
    
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#F97316',
    
    shadowColor: 'rgba(249, 115, 22, 0.1)',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 1,
    shadowRadius: 8,
    elevation: 4,
    
    textColor: '#F97316',
    fontSize: 16,
    fontWeight: '600',
    letterSpacing: 0.2
  },
  
  variants: {
    // Standard outlined
    outlined: {
      backgroundColor: 'transparent'
    },
    
    // Subtle filled
    subtle: {
      backgroundColor: '#FFF9F5',
      borderColor: '#FDBA74'
    },
    
    // Ghost version
    ghost: {
      backgroundColor: 'transparent',
      borderWidth: 0,
      shadowOpacity: 0
    }
  },
  
  states: {
    default: {
      scale: 1,
      opacity: 1
    },
    
    hover: {
      backgroundColor: '#FFF9F5',
      borderColor: '#FB923C',
      scale: 1.005,
      
      shadowRadius: 12,
      shadowOffset: { width: 0, height: 6 },
      
      transition: {
        duration: 200,
        easing: 'easeOut'
      }
    },
    
    pressIn: {
      scale: 0.98,
      backgroundColor: '#FEF5ED',
      
      transition: {
        duration: 100,
        easing: 'easeIn'
      }
    },
    
    pressOut: {
      scale: 1.005,
      backgroundColor: '#FFF9F5',
      
      transition: {
        type: 'spring',
        stiffness: 400,
        damping: 20
      }
    },
    
    loading: {
      opacity: 0.7,
      
      spinner: {
        size: 18,
        color: '#F97316'
      }
    },
    
    disabled: {
      opacity: 0.3,
      borderColor: '#D1D5DB',
      textColor: '#9CA3AF',
      pointerEvents: 'none'
    }
  }
}
```

## Icon Button

### Visual Specifications
```javascript
export const IconButton = {
  base: {
    width: 44,
    height: 44,
    borderRadius: 12,
    
    backgroundColor: '#FFFFFF',
    
    shadowColor: 'rgba(0, 0, 0, 0.08)',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 1,
    shadowRadius: 8,
    elevation: 4,
    
    alignItems: 'center',
    justifyContent: 'center'
  },
  
  variants: {
    // Standard white background
    standard: {
      backgroundColor: '#FFFFFF'
    },
    
    // Primary color background
    primary: {
      backgroundColor: '#F97316',
      iconColor: '#FFFFFF'
    },
    
    // Subtle background
    subtle: {
      backgroundColor: '#FFF9F5',
      iconColor: '#F97316'
    },
    
    // Ghost version
    ghost: {
      backgroundColor: 'transparent',
      shadowOpacity: 0,
      iconColor: '#F97316'
    },
    
    // Large version
    large: {
      width: 56,
      height: 56,
      borderRadius: 16
    },
    
    // Small version
    small: {
      width: 36,
      height: 36,
      borderRadius: 10
    }
  },
  
  states: {
    default: {
      scale: 1,
      opacity: 1
    },
    
    hover: {
      scale: 1.05,
      shadowRadius: 12,
      shadowOffset: { width: 0, height: 4 },
      
      // Subtle background tint
      backgroundTint: 'rgba(249, 115, 22, 0.05)',
      
      transition: {
        duration: 150,
        easing: 'easeOut'
      }
    },
    
    pressIn: {
      scale: 0.95,
      shadowRadius: 4,
      shadowOffset: { width: 0, height: 1 },
      
      transition: {
        duration: 100,
        easing: 'easeIn'
      }
    },
    
    pressOut: {
      scale: 1.05,
      shadowRadius: 12,
      
      transition: {
        type: 'spring',
        stiffness: 500,
        damping: 25
      }
    },
    
    loading: {
      opacity: 0.6,
      
      spinner: {
        size: 16,
        color: '#F97316'
      }
    },
    
    disabled: {
      opacity: 0.3,
      backgroundColor: '#F3F4F6',
      iconColor: '#9CA3AF',
      pointerEvents: 'none'
    }
  },
  
  // Special icon animations
  iconAnimations: {
    // Bounce on press
    bounce: {
      scale: [1, 0.8, 1.1, 1],
      timing: {
        duration: 300,
        easing: 'easeOut'
      }
    },
    
    // Rotate animation
    rotate: {
      rotate: [0, 180],
      timing: {
        duration: 200,
        easing: 'easeInOut'
      }
    },
    
    // Pulse for attention
    pulse: {
      scale: [1, 1.1, 1],
      opacity: [1, 0.7, 1],
      timing: {
        duration: 1000,
        repeat: -1,
        easing: 'easeInOut'
      }
    }
  }
}
```

## Advanced Button Animations

### Gesture-Based Interactions
```javascript
export const AdvancedButtonGestures = {
  // Long press for additional options
  longPress: {
    threshold: 500,
    
    // Visual feedback during long press
    feedbackAnimation: {
      scale: [1, 1.05, 1.1],
      shadowOpacity: [1, 0.6, 0.3],
      
      // Progress ring around button
      progressRing: {
        strokeDasharray: 251.2,
        strokeDashoffset: [251.2, 0],
        
        timing: {
          duration: 500,
          easing: 'linear'
        }
      }
    },
    
    // Activation feedback
    activation: {
      scale: [1.1, 0.95, 1],
      
      // Haptic feedback
      haptic: 'impactMedium',
      
      timing: {
        duration: 200,
        easing: 'easeOut'
      }
    }
  },
  
  // Double tap for quick actions
  doubleTap: {
    timeWindow: 300,
    
    // Double tap feedback
    feedback: {
      scale: [1, 1.15, 1],
      
      // Quick flash effect
      backgroundFlash: {
        backgroundColor: ['transparent', 'rgba(249, 115, 22, 0.2)', 'transparent'],
        
        timing: {
          duration: 200,
          easing: 'easeInOut'
        }
      }
    }
  },
  
  // Swipe gestures on buttons
  swipeGestures: {
    // Swipe right for quick approve
    swipeRight: {
      threshold: 50,
      
      // Visual feedback
      feedback: {
        translateX: [0, 10, 0],
        backgroundColor: ['transparent', 'rgba(16, 185, 129, 0.1)', 'transparent'],
        
        timing: {
          duration: 300,
          easing: 'easeOut'
        }
      }
    },
    
    // Swipe left for quick dismiss
    swipeLeft: {
      threshold: -50,
      
      feedback: {
        translateX: [0, -10, 0],
        backgroundColor: ['transparent', 'rgba(239, 68, 68, 0.1)', 'transparent'],
        
        timing: {
          duration: 300,
          easing: 'easeOut'
        }
      }
    }
  }
}
```

## Implementation Hooks

### useConfidenceButtonAnimation Hook
```javascript
import { useSharedValue, useAnimatedStyle, withSpring, withTiming } from 'react-native-reanimated'
import { Gesture } from 'react-native-gesture-handler'

export const useConfidenceButtonAnimation = (type = 'primary') => {
  const scale = useSharedValue(1)
  const shadowOpacity = useSharedValue(type === 'hero' ? 1 : 0.2)
  const shadowRadius = useSharedValue(type === 'hero' ? 20 : 16)
  
  // Gesture handler for all button interactions
  const gestureHandler = Gesture.Tap()
    .onBegin(() => {
      // Press in animation
      scale.value = withTiming(0.97, { duration: 100 })
      shadowOpacity.value = withTiming(shadowOpacity.value * 0.6, { duration: 100 })
      shadowRadius.value = withTiming(shadowRadius.value * 0.5, { duration: 100 })
    })
    .onFinalize(() => {
      // Release animation with confident spring
      scale.value = withSpring(1, {
        stiffness: 400,
        damping: 15
      })
      
      const baseShadowOpacity = type === 'hero' ? 1 : 0.2
      const baseShadowRadius = type === 'hero' ? 20 : 16
      
      shadowOpacity.value = withTiming(baseShadowOpacity, { duration: 200 })
      shadowRadius.value = withTiming(baseShadowRadius, { duration: 200 })
    })
  
  // Success effect for important actions
  const triggerSuccessEffect = () => {
    scale.value = withSequence(
      withTiming(1.05, { duration: 150 }),
      withTiming(1, { duration: 150 })
    )
    
    shadowOpacity.value = withSequence(
      withTiming(0.4, { duration: 150 }),
      withTiming(shadowOpacity.value, { duration: 150 })
    )
  }
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    shadowOpacity: shadowOpacity.value,
    shadowRadius: shadowRadius.value
  }))
  
  return {
    gestureHandler,
    animatedStyle,
    triggerSuccessEffect
  }
}
```

## Accessibility Integration

### Screen Reader Support
```javascript
export const ButtonAccessibility = {
  // Comprehensive accessibility props
  accessibilityProps: {
    role: 'button',
    accessible: true,
    accessibilityRole: 'button',
    
    // Dynamic accessibility labels
    accessibilityLabel: (children, loading, disabled) => {
      if (loading) return `${children}, loading`
      if (disabled) return `${children}, disabled`
      return children
    },
    
    // Accessibility hints
    accessibilityHint: (type) => {
      switch (type) {
        case 'hero':
          return 'Primary action button'
        case 'primary':
          return 'Activates main action'
        case 'secondary':
          return 'Alternative action'
        default:
          return 'Button'
      }
    },
    
    // State announcements
    accessibilityState: (loading, disabled, selected) => ({
      busy: loading,
      disabled: disabled,
      selected: selected
    })
  },
  
  // Focus management
  focusManagement: {
    // Visible focus indicators
    focusStyle: {
      borderWidth: 3,
      borderColor: '#3B82F6',
      borderStyle: 'solid',
      
      // Enhanced contrast for focus
      shadowColor: 'rgba(59, 130, 246, 0.4)',
      shadowOpacity: 1,
      shadowRadius: 8
    },
    
    // Focus animations
    focusAnimation: {
      scale: [1, 1.02, 1],
      timing: {
        duration: 300,
        easing: 'easeInOut'
      }
    }
  },
  
  // Reduced motion support
  reducedMotion: {
    // Alternative animations for reduced motion
    scale: {
      normal: [0.97, 1.05, 1],
      reduced: [0.99, 1.01, 1]
    },
    
    shadow: {
      normal: [0.6, 0.4, 1],
      reduced: [0.8, 0.9, 1]
    },
    
    duration: {
      normal: [100, 200, 300],
      reduced: [50, 100, 150]
    }
  }
}
```

## Testing Specifications

### Button Testing Framework
```javascript
export const ButtonTestingSpecs = {
  // Visual regression testing
  visualTests: {
    states: [
      'default',
      'hover', 
      'pressed',
      'loading',
      'disabled'
    ],
    
    variants: [
      'hero',
      'primary', 
      'secondary',
      'tertiary',
      'icon'
    ],
    
    themes: [
      'light',
      'dark' // Future implementation
    ]
  },
  
  // Interaction testing
  interactionTests: {
    gestures: [
      'tap',
      'long_press',
      'double_tap',
      'swipe_right',
      'swipe_left'
    ],
    
    animations: [
      'press_feedback',
      'release_spring',
      'success_pulse',
      'loading_spinner'
    ],
    
    accessibility: [
      'screen_reader_navigation',
      'keyboard_navigation',
      'focus_indicators',
      'reduced_motion'
    ]
  },
  
  // Performance benchmarks
  performance: {
    animationFrameRate: '60fps minimum',
    gestureResponseTime: '<16ms',
    memoryUsage: '<2MB per button instance',
    renderTime: '<100ms for complex buttons'
  }
}
```

---

*These premium button components transform basic interactions into confidence-building moments that users will remember and appreciate. Every animation and interaction is designed to make users feel capable and supported throughout their FlirtCraft journey.*