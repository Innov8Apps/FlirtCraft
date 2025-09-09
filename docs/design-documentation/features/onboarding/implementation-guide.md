# FlirtCraft Premium Onboarding Implementation Guide

---
title: Premium Onboarding Implementation Roadmap
description: Comprehensive developer guide for implementing FANG-level onboarding with React Native
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./premium-redesign.md
  - ../../design-system/tokens/premium-animations.md
  - ../../design-system/components/premium-buttons.md
dependencies:
  - React Native 0.73+
  - Expo SDK 50+
  - React Native Reanimated 3.6+
  - React Native Gesture Handler 2.14+
  - Lottie React Native 6.4+
status: implementation-ready
---

## Implementation Overview

This guide provides the complete technical implementation for FlirtCraft's premium onboarding experience. The redesign focuses on:

1. **Orange-Only Color System** - Eliminating all teal references for consistent warm branding
2. **Advanced Animations** - React Native Reanimated 3 for 60fps smooth interactions
3. **Premium Polish** - FANG-level attention to detail and micro-interactions
4. **Performance Excellence** - Optimized for smooth performance across all devices
5. **Accessibility First** - WCAG 2.1 AA compliance with premium UX

## Technical Architecture

### Dependencies Installation
```bash
# Core animation libraries
npm install react-native-reanimated@^3.6.0
npm install react-native-gesture-handler@^2.14.0
npm install lottie-react-native@^6.4.0

# Visual enhancements
npm install expo-linear-gradient@^12.7.0
npm install expo-blur@^12.9.0
npm install react-native-svg@^14.1.0

# Additional utilities
npm install react-native-haptic-feedback@^2.2.0
npm install @react-native-async-storage/async-storage@^1.21.0
```

### Project Structure
```
src/
├── components/
│   ├── onboarding/
│   │   ├── screens/
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── AgeVerificationScreen.tsx
│   │   │   ├── AuthScreen.tsx
│   │   │   ├── PreferencesScreen.tsx
│   │   │   └── SkillGoalsScreen.tsx
│   │   ├── animations/
│   │   │   ├── HeroAnimation.tsx
│   │   │   ├── ParticleSystem.tsx
│   │   │   ├── ProgressRing.tsx
│   │   │   └── CelebrationSequence.tsx
│   │   └── shared/
│   │       ├── PremiumButton.tsx
│   │       ├── SelectionCard.tsx
│   │       ├── FormField.tsx
│   │       └── ProgressIndicator.tsx
│   └── ui/
│       ├── buttons/
│       ├── forms/
│       └── animations/
├── hooks/
│   ├── useConfidenceAnimation.ts
│   ├── useSelectionCard.ts
│   ├── useFormValidation.ts
│   └── useOnboardingFlow.ts
├── styles/
│   ├── colors.ts
│   ├── animations.ts
│   ├── typography.ts
│   └── spacing.ts
└── utils/
    ├── haptics.ts
    ├── accessibility.ts
    └── performance.ts
```

## Updated Color System Implementation

### colors.ts (Updated)
```typescript
// FlirtCraft Orange-Only Color System
export const colors = {
  // Primary Orange System (no teal)
  primary: {
    50: '#FFF9F5',   // Lightest background
    75: '#FFF5ED',   // Ultra-light
    100: '#FFEDD5',  // Light background
    200: '#FED7AA',  // Soft accent
    300: '#FDBA74',  // Medium highlight
    350: '#FC9D4A',  // Rich mid-tone
    400: '#FB923C',  // Warm orange
    500: '#F97316',  // Primary brand
    550: '#F26B0C',  // Deeper primary
    600: '#EA580C',  // Dark orange
    650: '#DD4E08',  // Rich dark
    700: '#C2410C',  // Deep orange
    750: '#B8370B',  // Darker
    800: '#9A3412',  // Very dark
    850: '#8B2F10',  // Deep rust
    900: '#7C2D12',  // Darkest
    950: '#6B240E'   // Ultra-dark
  },

  // Secondary Orange Complements (replaces teal)
  secondary: {
    50: '#FEF7F0',   // Warm cream
    100: '#FEEEE0',  // Light peach
    200: '#FEDCC7',  // Soft peach
    300: '#FDBA8C',  // Warm peach (replaces teal usage)
    400: '#FB9A3C',  // Rich orange
    500: '#E65100',  // Deep orange secondary
    600: '#D84315',  // Dark orange
    700: '#BF360C',  // Deep rust
    800: '#A5300A',  // Dark rust
    900: '#8B2508'   // Darkest rust
  },

  // Premium Gradients
  gradients: {
    primary: ['#F97316', '#FB923C'],
    hero: ['#FF8C42', '#F97316', '#E65100'],
    success: ['#16A34A', '#22C55E'],
    warning: ['#D97706', '#F59E0B'],
    error: ['#DC2626', '#EF4444'],
    subtle: ['#FFF9F5', '#FEEEE0']
  },

  // Semantic Colors (warm-adjusted)
  semantic: {
    success: '#16A34A',
    warning: '#D97706', // Orange-based warning
    error: '#DC2626',
    info: '#EA580C'     // Orange-based info (no blue)
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
  }
}

// Export for easy component usage
export const { primary, secondary, semantic, neutral, gradients } = colors
```

### Advanced Animation System

#### hooks/useConfidenceAnimation.ts
```typescript
import { useEffect } from 'react'
import { useSharedValue, useAnimatedStyle, withDelay, withTiming, withSpring, Easing } from 'react-native-reanimated'
import { AccessibilityInfo } from 'react-native'

// Custom easing curves for confidence-building animations
const confidenceEasing = {
  confident: Easing.bezier(0.2, 0, 0.2, 1),
  warm: Easing.bezier(0.25, 0.46, 0.45, 0.94),
  energetic: Easing.bezier(0.68, -0.55, 0.265, 1.55),
  supportive: Easing.bezier(0.4, 0, 0.6, 1)
}

interface ConfidenceAnimationOptions {
  delay?: number
  stagger?: number
  reducedMotion?: boolean
}

export const useConfidenceAnimation = (options: ConfidenceAnimationOptions = {}) => {
  const { delay = 0, stagger = 0, reducedMotion = false } = options
  
  // Animation values
  const opacity = useSharedValue(0)
  const scale = useSharedValue(0.9)
  const translateY = useSharedValue(30)
  const rotate = useSharedValue(0)
  
  useEffect(() => {
    const startAnimations = async () => {
      // Check for reduced motion preference
      const isReduceMotionEnabled = await AccessibilityInfo.isReduceMotionEnabled()
      const useReducedMotion = reducedMotion || isReduceMotionEnabled
      
      // Adjust animations for accessibility
      const animationDuration = useReducedMotion ? 200 : 400
      const scaleRange = useReducedMotion ? [0.98, 1] : [0.9, 1]
      const translateRange = useReducedMotion ? 10 : 30
      
      // Orchestrated entrance
      opacity.value = withDelay(
        delay,
        withTiming(1, {
          duration: animationDuration,
          easing: confidenceEasing.confident
        })
      )
      
      scale.value = withDelay(
        delay + stagger,
        withSpring(1, {
          stiffness: useReducedMotion ? 200 : 100,
          damping: useReducedMotion ? 25 : 15
        })
      )
      
      translateY.value = withDelay(
        delay + stagger * 1.2,
        withSpring(0, {
          stiffness: useReducedMotion ? 180 : 120,
          damping: useReducedMotion ? 20 : 12
        })
      )
    }
    
    startAnimations()
  }, [delay, stagger, reducedMotion])
  
  // Success celebration animation
  const triggerSuccess = () => {
    scale.value = withTiming(1.05, { duration: 150 }, () => {
      scale.value = withTiming(1, { duration: 150 })
    })
    
    rotate.value = withTiming(2, { duration: 300 }, () => {
      rotate.value = withTiming(0, { duration: 300 })
    })
  }
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [
      { scale: scale.value },
      { translateY: translateY.value },
      { rotate: `${rotate.value}deg` }
    ]
  }))
  
  return {
    animatedStyle,
    triggerSuccess,
    isComplete: opacity.value === 1
  }
}
```

#### components/animations/ParticleSystem.tsx
```typescript
import React, { useEffect } from 'react'
import { View, StyleSheet } from 'react-native'
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withTiming, 
  withRepeat,
  withDelay,
  runOnJS
} from 'react-native-reanimated'
import { colors } from '../../../styles/colors'

interface Particle {
  id: string
  initialX: number
  initialY: number
  color: string
  size: number
}

interface ParticleSystemProps {
  count?: number
  colors?: string[]
  duration?: number
  isActive?: boolean
  onComplete?: () => void
}

export const ParticleSystem: React.FC<ParticleSystemProps> = ({
  count = 12,
  colors: particleColors = [colors.primary[500], colors.primary[400], colors.primary[300]],
  duration = 3000,
  isActive = false,
  onComplete
}) => {
  // Generate particles
  const particles: Particle[] = Array.from({ length: count }, (_, index) => ({
    id: `particle-${index}`,
    initialX: Math.random() * 300,
    initialY: Math.random() * 200 + 100,
    color: particleColors[Math.floor(Math.random() * particleColors.length)],
    size: Math.random() * 8 + 4
  }))
  
  return (
    <View style={styles.container} pointerEvents="none">
      {particles.map((particle) => (
        <ParticleComponent
          key={particle.id}
          particle={particle}
          duration={duration}
          isActive={isActive}
          onComplete={onComplete}
        />
      ))}
    </View>
  )
}

const ParticleComponent: React.FC<{
  particle: Particle
  duration: number
  isActive: boolean
  onComplete?: () => void
}> = ({ particle, duration, isActive, onComplete }) => {
  const translateX = useSharedValue(particle.initialX)
  const translateY = useSharedValue(particle.initialY)
  const opacity = useSharedValue(0)
  const scale = useSharedValue(0.5)
  const rotate = useSharedValue(0)
  
  useEffect(() => {
    if (isActive) {
      // Random floating pattern
      const floatX = (Math.random() - 0.5) * 40
      const floatY = -Math.random() * 50 - 20
      
      // Start animation sequence
      opacity.value = withDelay(
        Math.random() * 500,
        withTiming(0.8, { duration: 400 }, () => {
          opacity.value = withTiming(0, { duration: duration - 800 })
        })
      )
      
      scale.value = withDelay(
        Math.random() * 300,
        withTiming(1.2, { duration: 600 }, () => {
          scale.value = withTiming(0.8, { duration: duration - 1200 })
        })
      )
      
      translateX.value = withRepeat(
        withTiming(translateX.value + floatX, { duration: duration }),
        1,
        false
      )
      
      translateY.value = withRepeat(
        withTiming(translateY.value + floatY, { duration: duration }),
        1,
        false,
        () => {
          if (onComplete) {
            runOnJS(onComplete)()
          }
        }
      )
      
      rotate.value = withRepeat(
        withTiming(360, { duration: duration }),
        1,
        false
      )
    }
  }, [isActive])
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
      { scale: scale.value },
      { rotate: `${rotate.value}deg` }
    ],
    opacity: opacity.value
  }))
  
  return (
    <Animated.View
      style={[
        styles.particle,
        {
          backgroundColor: particle.color,
          width: particle.size,
          height: particle.size,
          borderRadius: particle.size / 2
        },
        animatedStyle
      ]}
    />
  )
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 1000
  },
  particle: {
    position: 'absolute',
    shadowColor: 'rgba(0, 0, 0, 0.2)',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4
  }
})
```

### Screen Implementations

#### components/onboarding/screens/WelcomeScreen.tsx
```typescript
import React, { useEffect, useState } from 'react'
import { View, Text, StyleSheet, Dimensions } from 'react-native'
import { LinearGradient } from 'expo-linear-gradient'
import Animated from 'react-native-reanimated'
import LottieView from 'lottie-react-native'
import { ParticleSystem } from '../animations/ParticleSystem'
import { PremiumButton } from '../shared/PremiumButton'
import { useConfidenceAnimation } from '../../../hooks/useConfidenceAnimation'
import { colors, gradients } from '../../../styles/colors'
import { typography } from '../../../styles/typography'

const { width, height } = Dimensions.get('window')

interface WelcomeScreenProps {
  onContinue: () => void
  onSignIn: () => void
}

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({
  onContinue,
  onSignIn
}) => {
  const [showParticles, setShowParticles] = useState(false)
  
  // Staggered animations for different elements
  const heroAnimation = useConfidenceAnimation({ delay: 300 })
  const subtitleAnimation = useConfidenceAnimation({ delay: 600 })
  const featuresAnimation = useConfidenceAnimation({ delay: 900, stagger: 150 })
  const ctaAnimation = useConfidenceAnimation({ delay: 1200 })
  
  useEffect(() => {
    // Start particle system after hero loads
    const timer = setTimeout(() => {
      setShowParticles(true)
    }, 800)
    
    return () => clearTimeout(timer)
  }, [])
  
  const features = [
    {
      icon: '💬',
      title: 'Realistic Practice',
      description: 'AI conversations that feel completely natural'
    },
    {
      icon: '🎯',
      title: 'Personalized Training',
      description: 'Tailored to your style and comfort level'
    },
    {
      icon: '📈',
      title: 'Real Results',
      description: 'Track your progress and see confidence grow'
    }
  ]
  
  return (
    <LinearGradient
      colors={gradients.hero}
      locations={[0, 0.6, 1]}
      style={styles.container}
    >
      {/* Background particle system */}
      <ParticleSystem
        count={15}
        isActive={showParticles}
        colors={[
          'rgba(255, 255, 255, 0.6)',
          'rgba(255, 255, 255, 0.4)',
          'rgba(255, 255, 255, 0.8)'
        ]}
      />
      
      {/* Hero Content */}
      <View style={styles.heroSection}>
        <Animated.View style={heroAnimation.animatedStyle}>
          <Text style={styles.heroTitle}>
            Build Your Dating Confidence
          </Text>
        </Animated.View>
        
        <Animated.View style={subtitleAnimation.animatedStyle}>
          <Text style={styles.heroSubtitle}>
            AI-powered conversation practice that actually works
          </Text>
        </Animated.View>
      </View>
      
      {/* Feature Highlights */}
      <View style={styles.featuresSection}>
        {features.map((feature, index) => (
          <Animated.View
            key={feature.title}
            style={[
              featuresAnimation.animatedStyle,
              { transform: [{ scale: 1 }] } // Override to prevent stacking
            ]}
          >
            <View style={styles.featureCard}>
              <Text style={styles.featureIcon}>{feature.icon}</Text>
              <View style={styles.featureContent}>
                <Text style={styles.featureTitle}>{feature.title}</Text>
                <Text style={styles.featureDescription}>
                  {feature.description}
                </Text>
              </View>
            </View>
          </Animated.View>
        ))}
      </View>
      
      {/* Call-to-Action Section */}
      <Animated.View style={[styles.ctaSection, ctaAnimation.animatedStyle]}>
        <PremiumButton
          type="hero"
          onPress={onContinue}
          style={styles.primaryCTA}
        >
          Start Building Confidence
        </PremiumButton>
        
        <PremiumButton
          type="secondary"
          variant="ghost"
          onPress={onSignIn}
          style={styles.secondaryCTA}
        >
          Already have an account? Sign In
        </PremiumButton>
      </Animated.View>
      
      {/* Social Proof */}
      <Animated.View style={[styles.socialProof, ctaAnimation.animatedStyle]}>
        <Text style={styles.socialProofText}>
          ⭐⭐⭐⭐⭐ Rated 4.8/5 by users who saw real results
        </Text>
      </Animated.View>
    </LinearGradient>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40
  },
  
  heroSection: {
    alignItems: 'center',
    marginTop: 80,
    marginBottom: 60
  },
  
  heroTitle: {
    ...typography.display.large,
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 16,
    textShadowColor: 'rgba(0, 0, 0, 0.15)',
    textShadowOffset: { width: 0, height: 2 },
    textShadowRadius: 4
  },
  
  heroSubtitle: {
    ...typography.body.large,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
    paddingHorizontal: 20,
    lineHeight: 24
  },
  
  featuresSection: {
    marginBottom: 60
  },
  
  featureCard: {
    flexDirection: 'row',
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    backdropFilter: 'blur(20px)',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
    shadowColor: 'rgba(0, 0, 0, 0.1)',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 1,
    shadowRadius: 24
  },
  
  featureIcon: {
    fontSize: 32,
    marginRight: 16,
    alignSelf: 'center'
  },
  
  featureContent: {
    flex: 1
  },
  
  featureTitle: {
    ...typography.heading.small,
    color: '#FFFFFF',
    marginBottom: 4
  },
  
  featureDescription: {
    ...typography.body.medium,
    color: 'rgba(255, 255, 255, 0.8)',
    lineHeight: 20
  },
  
  ctaSection: {
    alignItems: 'center',
    marginBottom: 20
  },
  
  primaryCTA: {
    marginBottom: 16
  },
  
  secondaryCTA: {
    // Styles handled by component
  },
  
  socialProof: {
    alignItems: 'center'
  },
  
  socialProofText: {
    ...typography.body.small,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center'
  }
})
```

### Premium Button Component

#### components/shared/PremiumButton.tsx
```typescript
import React from 'react'
import { Text, StyleSheet, ActivityIndicator } from 'react-native'
import { LinearGradient } from 'expo-linear-gradient'
import Animated from 'react-native-reanimated'
import { GestureDetector } from 'react-native-gesture-handler'
import { useConfidenceButtonAnimation } from '../../../hooks/useConfidenceButtonAnimation'
import { colors, gradients } from '../../../styles/colors'
import { typography } from '../../../styles/typography'

interface PremiumButtonProps {
  children: React.ReactNode
  onPress?: () => void
  type?: 'hero' | 'primary' | 'secondary' | 'tertiary'
  variant?: 'solid' | 'outlined' | 'ghost'
  size?: 'small' | 'medium' | 'large'
  loading?: boolean
  disabled?: boolean
  style?: any
  accessibilityLabel?: string
  accessibilityHint?: string
}

export const PremiumButton: React.FC<PremiumButtonProps> = ({
  children,
  onPress,
  type = 'primary',
  variant = 'solid',
  size = 'medium',
  loading = false,
  disabled = false,
  style,
  accessibilityLabel,
  accessibilityHint
}) => {
  const {
    animatedStyle,
    gestureHandler,
    triggerSuccessEffect
  } = useConfidenceButtonAnimation(type)
  
  const handlePress = () => {
    if (!disabled && !loading) {
      triggerSuccessEffect()
      onPress?.()
    }
  }
  
  const buttonStyles = [
    styles.base,
    styles[type],
    styles[size],
    variant === 'outlined' && styles.outlined,
    variant === 'ghost' && styles.ghost,
    disabled && styles.disabled,
    style
  ]
  
  const textStyles = [
    styles.text,
    styles[`${type}Text`],
    disabled && styles.disabledText
  ]
  
  // Choose gradient based on button type
  const gradientColors = type === 'hero' 
    ? gradients.hero 
    : type === 'primary' 
    ? gradients.primary 
    : ['transparent', 'transparent']
  
  const ButtonContent = () => (
    <>
      {loading ? (
        <ActivityIndicator 
          color={type === 'secondary' ? colors.primary[500] : '#FFFFFF'} 
          size="small" 
        />
      ) : (
        <Text style={textStyles}>{children}</Text>
      )}
    </>
  )
  
  return (
    <GestureDetector gesture={gestureHandler}>
      <Animated.View style={[buttonStyles, animatedStyle]}>
        {(type === 'hero' || (type === 'primary' && variant === 'solid')) ? (
          <LinearGradient
            colors={gradientColors}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.gradient}
          >
            <Animated.Pressable
              onPress={handlePress}
              disabled={disabled || loading}
              style={styles.pressable}
              accessible={true}
              accessibilityRole="button"
              accessibilityLabel={accessibilityLabel || (typeof children === 'string' ? children : 'Button')}
              accessibilityHint={accessibilityHint}
              accessibilityState={{
                busy: loading,
                disabled: disabled
              }}
            >
              <ButtonContent />
            </Animated.Pressable>
          </LinearGradient>
        ) : (
          <Animated.Pressable
            onPress={handlePress}
            disabled={disabled || loading}
            style={[styles.pressable, buttonStyles]}
            accessible={true}
            accessibilityRole="button"
            accessibilityLabel={accessibilityLabel || (typeof children === 'string' ? children : 'Button')}
            accessibilityHint={accessibilityHint}
            accessibilityState={{
              busy: loading,
              disabled: disabled
            }}
          >
            <ButtonContent />
          </Animated.Pressable>
        )}
      </Animated.View>
    </GestureDetector>
  )
}

const styles = StyleSheet.create({
  base: {
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: 'rgba(249, 115, 22, 0.2)',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 1,
    shadowRadius: 16,
    elevation: 8
  },
  
  hero: {
    minHeight: 56,
    minWidth: 280,
    borderRadius: 16,
    shadowColor: 'rgba(249, 115, 22, 0.25)',
    shadowRadius: 20,
    elevation: 12
  },
  
  primary: {
    minHeight: 52,
    backgroundColor: colors.primary[500]
  },
  
  secondary: {
    minHeight: 48,
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: colors.primary[500]
  },
  
  tertiary: {
    minHeight: 44,
    backgroundColor: colors.primary[50],
    shadowOpacity: 0.5
  },
  
  small: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    minHeight: 40
  },
  
  medium: {
    paddingHorizontal: 24,
    paddingVertical: 14
  },
  
  large: {
    paddingHorizontal: 32,
    paddingVertical: 18,
    minHeight: 56
  },
  
  outlined: {
    backgroundColor: 'transparent'
  },
  
  ghost: {
    backgroundColor: 'transparent',
    borderWidth: 0,
    shadowOpacity: 0
  },
  
  disabled: {
    opacity: 0.5,
    shadowOpacity: 0.2
  },
  
  gradient: {
    flex: 1,
    borderRadius: 'inherit',
    alignItems: 'center',
    justifyContent: 'center'
  },
  
  pressable: {
    flex: 1,
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
    paddingVertical: 14
  },
  
  text: {
    ...typography.button.medium,
    textAlign: 'center'
  },
  
  heroText: {
    ...typography.button.large,
    color: '#FFFFFF',
    fontWeight: '700',
    textShadowColor: 'rgba(0, 0, 0, 0.2)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2
  },
  
  primaryText: {
    color: '#FFFFFF',
    fontWeight: '600'
  },
  
  secondaryText: {
    color: colors.primary[500],
    fontWeight: '600'
  },
  
  tertiaryText: {
    color: colors.primary[700],
    fontWeight: '500'
  },
  
  disabledText: {
    color: colors.neutral[400]
  }
})
```

## Performance Optimization Guide

### Memory Management
```typescript
// utils/performance.ts
export class PerformanceOptimizer {
  private static animationRefs = new Set<any>()
  
  static registerAnimation(ref: any) {
    this.animationRefs.add(ref)
  }
  
  static unregisterAnimation(ref: any) {
    this.animationRefs.delete(ref)
  }
  
  static pauseAllAnimations() {
    this.animationRefs.forEach(ref => {
      if (ref.pause) ref.pause()
    })
  }
  
  static resumeAllAnimations() {
    this.animationRefs.forEach(ref => {
      if (ref.resume) ref.resume()
    })
  }
  
  static clearAllAnimations() {
    this.animationRefs.forEach(ref => {
      if (ref.cancel) ref.cancel()
    })
    this.animationRefs.clear()
  }
}

// App state management for performance
export const usePerformanceOptimization = () => {
  useEffect(() => {
    const handleAppStateChange = (nextAppState: string) => {
      if (nextAppState === 'background') {
        PerformanceOptimizer.pauseAllAnimations()
      } else if (nextAppState === 'active') {
        PerformanceOptimizer.resumeAllAnimations()
      }
    }
    
    const subscription = AppState.addEventListener('change', handleAppStateChange)
    
    return () => {
      subscription?.remove()
      PerformanceOptimizer.clearAllAnimations()
    }
  }, [])
}
```

### Bundle Size Optimization
```typescript
// Lazy load heavy components
const WelcomeScreen = lazy(() => import('./screens/WelcomeScreen'))
const ParticleSystem = lazy(() => import('./animations/ParticleSystem'))
const CelebrationSequence = lazy(() => import('./animations/CelebrationSequence'))

// Component-level code splitting
export const OnboardingFlow = () => {
  const [currentScreen, setCurrentScreen] = useState(0)
  
  const screens = [
    { component: WelcomeScreen, preload: true },
    { component: AgeVerificationScreen, preload: true },
    { component: AuthScreen, preload: false },
    { component: PreferencesScreen, preload: false },
    { component: SkillGoalsScreen, preload: false }
  ]
  
  // Preload next screen
  useEffect(() => {
    const nextScreen = screens[currentScreen + 1]
    if (nextScreen && !nextScreen.preload) {
      // Lazy load next screen in background
      import('./screens/' + nextScreen.component.name)
    }
  }, [currentScreen])
  
  return (
    <Suspense fallback={<LoadingScreen />}>
      {/* Render current screen */}
    </Suspense>
  )
}
```

## Testing Framework

### Animation Testing
```typescript
// __tests__/animations/confidence-animation.test.ts
import { renderHook, act } from '@testing-library/react-native'
import { useConfidenceAnimation } from '../../hooks/useConfidenceAnimation'

describe('useConfidenceAnimation', () => {
  it('should start with initial values', () => {
    const { result } = renderHook(() => useConfidenceAnimation())
    
    expect(result.current.isComplete).toBe(false)
  })
  
  it('should trigger success animation', async () => {
    const { result } = renderHook(() => useConfidenceAnimation())
    
    act(() => {
      result.current.triggerSuccess()
    })
    
    // Animation should be triggered
    expect(result.current.animatedStyle.value).toEqual(
      expect.objectContaining({
        transform: expect.arrayContaining([
          expect.objectContaining({ scale: expect.any(Number) })
        ])
      })
    )
  })
  
  it('should respect reduced motion preferences', async () => {
    // Mock AccessibilityInfo
    jest.mock('react-native', () => ({
      AccessibilityInfo: {
        isReduceMotionEnabled: jest.fn().mockResolvedValue(true)
      }
    }))
    
    const { result } = renderHook(() => useConfidenceAnimation())
    
    // Should use reduced animations
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 300))
    })
    
    expect(result.current.isComplete).toBe(true)
  })
})
```

### Visual Regression Testing
```typescript
// __tests__/visual/button-states.test.tsx
import { render } from '@testing-library/react-native'
import { PremiumButton } from '../components/shared/PremiumButton'

describe('PremiumButton Visual States', () => {
  const variants = ['hero', 'primary', 'secondary', 'tertiary']
  const states = ['default', 'loading', 'disabled']
  
  variants.forEach(variant => {
    states.forEach(state => {
      it(`renders ${variant} button in ${state} state correctly`, () => {
        const props = {
          type: variant,
          loading: state === 'loading',
          disabled: state === 'disabled'
        }
        
        const { toJSON } = render(
          <PremiumButton {...props}>
            Test Button
          </PremiumButton>
        )
        
        expect(toJSON()).toMatchSnapshot(`${variant}-${state}`)
      })
    })
  })
})
```

## Deployment Checklist

### Pre-Deployment Validation
- [ ] All teal color references removed and replaced with orange alternatives
- [ ] Animations tested at 60fps on minimum supported devices
- [ ] Accessibility compliance verified with screen readers
- [ ] Performance benchmarks met (load times, memory usage)
- [ ] Visual regression tests passing
- [ ] Cross-platform consistency verified
- [ ] Reduced motion preferences respected
- [ ] Error handling tested for all edge cases

### Post-Deployment Monitoring
- [ ] Animation frame rate monitoring in production
- [ ] User completion rates tracked
- [ ] Crash reporting for animation-related issues
- [ ] Performance metrics collection
- [ ] A/B testing setup for confidence-building messaging
- [ ] Accessibility feedback collection

---

*This implementation guide provides everything needed to transform FlirtCraft's onboarding into a premium, confidence-building experience that users will love. The focus on warm orange branding, sophisticated animations, and accessibility ensures both emotional impact and technical excellence.*