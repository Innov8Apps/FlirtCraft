# FlirtCraft Onboarding: Premium FANG-Level Redesign

---
title: FlirtCraft Premium Onboarding Experience
description: Complete redesign with sophisticated animations, orange-only color system, and FANG-level polish
feature: onboarding-redesign
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native Reanimated 3
  - Lottie React Native
  - Expo Linear Gradient
  - React Native Gesture Handler
status: draft
---

## Design Philosophy

FlirtCraft's premium onboarding creates a psychologically safe, confidence-building experience through sophisticated visual design, smooth animations, and warm orange-centered aesthetics. The redesign eliminates all teal references, focusing exclusively on an orange gradient system that evokes warmth, energy, and optimism.

### Key Design Principles
- **Confidence-First Design**: Every visual element builds user confidence
- **Warm Psychology**: Orange-only palette creates emotional safety and enthusiasm
- **Premium Sophistication**: FANG-level polish with advanced animations and micro-interactions
- **Progressive Disclosure**: Information revealed elegantly without overwhelming users
- **Accessible Excellence**: WCAG 2.1 AA compliance with premium aesthetics

## Advanced Color System (Orange-Only)

### Primary Orange Gradient System
```javascript
export const premiumOrangeSystem = {
  // Core Brand Gradients
  primaryGradient: {
    start: '#F97316', // Primary orange
    end: '#FB923C',   // Warm orange
    angle: 135,
    locations: [0, 1]
  },
  
  // Advanced Gradient Variations
  heroGradient: {
    start: '#FF8C42',  // Vibrant orange
    end: '#F97316',    // Primary orange
    end2: '#E65100',   // Deep orange
    angle: 45,
    locations: [0, 0.6, 1]
  },
  
  // Sophisticated Orange Palette
  orange: {
    50: '#FFF9F5',   // Lightest warm background
    75: '#FFF5ED',   // Ultra-light orange
    100: '#FFEDD5',  // Light orange background
    200: '#FED7AA',  // Soft orange accent
    300: '#FDBA74',  // Medium orange highlight
    350: '#FC9D4A',  // Rich orange mid-tone
    400: '#FB923C',  // Warm orange
    500: '#F97316',  // Primary brand (main)
    550: '#F26B0C',  // Deeper primary
    600: '#EA580C',  // Dark orange
    650: '#DD4E08',  // Rich dark orange
    700: '#C2410C',  // Deep orange
    750: '#B8370B',  // Darker orange
    800: '#9A3412',  // Very dark orange
    850: '#8B2F10',  // Deep rust
    900: '#7C2D12',  // Darkest orange
    950: '#6B240E'   // Ultra-dark rust
  },
  
  // Warm Neutral Complements
  warmNeutral: {
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
```

### Semantic Color Adaptations
```javascript
export const semanticColors = {
  success: {
    primary: '#16A34A',    // Green with warm undertone
    background: '#F0FDF4', // Light green background
    gradient: 'linear-gradient(135deg, #16A34A 0%, #22C55E 100%)'
  },
  
  warning: {
    primary: '#D97706',    // Warm amber (orange-based)
    background: '#FFFBEB', // Light amber background
    gradient: 'linear-gradient(135deg, #D97706 0%, #F59E0B 100%)'
  },
  
  error: {
    primary: '#DC2626',    // Red with warm undertone
    background: '#FEF2F2', // Light red background
    gradient: 'linear-gradient(135deg, #DC2626 0%, #EF4444 100%)'
  },
  
  info: {
    primary: '#EA580C',    // Orange-based info (replacing blue)
    background: '#FFF9F5', // Warm orange background
    gradient: 'linear-gradient(135deg, #EA580C 0%, #F97316 100%)'
  }
}
```

## Advanced Animation Architecture

### Core Animation System
```javascript
// React Native Reanimated 3 Specifications
export const animationConfig = {
  // Timing Functions
  easing: {
    bounceOut: Easing.bezier(0.68, -0.55, 0.265, 1.55),
    smoothOut: Easing.bezier(0.25, 0.46, 0.45, 0.94),
    spring: Easing.bezier(0.175, 0.885, 0.32, 1.275),
    confident: Easing.bezier(0.2, 0, 0.2, 1) // Custom confidence-building curve
  },
  
  // Duration System
  duration: {
    micro: 150,      // Button presses, small state changes
    fast: 250,       // Card selections, form inputs
    medium: 400,     // Screen transitions, major state changes  
    slow: 600,       // Hero animations, celebration sequences
    cinematic: 1000  // Welcome sequence, major moments
  },
  
  // Stagger Configurations
  stagger: {
    listItems: 80,   // Milliseconds between list item animations
    formFields: 120, // Milliseconds between form field appearances
    features: 200,   // Milliseconds between feature highlights
    celebration: 150 // Milliseconds between celebration particle bursts
  }
}
```

### Screen-Specific Animation Specs

#### 1. Welcome Screen Hero Animation
```javascript
const WelcomeAnimations = {
  // Hero Text Entrance
  heroTitle: {
    initial: { opacity: 0, translateY: 50, scale: 0.9 },
    animate: { 
      opacity: 1, 
      translateY: 0, 
      scale: 1,
      transition: {
        type: 'spring',
        stiffness: 100,
        damping: 15,
        duration: 800
      }
    }
  },
  
  // Gradient Background Animation
  backgroundGradient: {
    initial: { opacity: 0 },
    animate: { 
      opacity: 1,
      transition: {
        duration: 1200,
        easing: 'smoothOut'
      }
    }
  },
  
  // Floating Particle System
  confidenceParticles: {
    count: 12,
    animation: {
      translateX: 'random(-20, 20)',
      translateY: 'random(-30, -10)', 
      opacity: [0, 0.6, 0],
      scale: [0.5, 1, 0.8],
      duration: 3000,
      repeat: -1,
      delay: 'stagger(200)'
    }
  },
  
  // Primary CTA Button
  primaryCTA: {
    initial: { 
      opacity: 0, 
      scale: 0.8, 
      translateY: 30 
    },
    animate: {
      opacity: 1,
      scale: 1,
      translateY: 0,
      transition: {
        type: 'spring',
        delay: 600,
        stiffness: 120,
        damping: 12
      }
    },
    // Interactive States
    pressIn: {
      scale: 0.95,
      transition: { duration: 100 }
    },
    pressOut: {
      scale: 1,
      transition: { 
        type: 'spring',
        stiffness: 400,
        damping: 10
      }
    }
  }
}
```

#### 2. Preferences Screen Advanced Interactions
```javascript
const PreferenceAnimations = {
  // Selection Cards Staggered Entrance
  selectionCards: {
    container: {
      initial: { opacity: 0 },
      animate: { 
        opacity: 1,
        transition: {
          staggerChildren: 0.1,
          delayChildren: 0.2
        }
      }
    },
    item: {
      initial: { 
        opacity: 0, 
        scale: 0.9,
        translateY: 20
      },
      animate: {
        opacity: 1,
        scale: 1,
        translateY: 0,
        transition: {
          type: 'spring',
          stiffness: 100,
          damping: 12
        }
      }
    }
  },
  
  // Card Selection States
  cardInteraction: {
    default: {
      scale: 1,
      shadowOpacity: 0.1,
      shadowRadius: 4,
      shadowOffset: { width: 0, height: 2 }
    },
    hover: {
      scale: 1.02,
      shadowOpacity: 0.15,
      shadowRadius: 8,
      shadowOffset: { width: 0, height: 4 },
      transition: { duration: 200 }
    },
    selected: {
      scale: 1.05,
      shadowOpacity: 0.25,
      shadowRadius: 12,
      shadowOffset: { width: 0, height: 6 },
      backgroundColor: 'orange.50',
      borderColor: 'orange.500',
      borderWidth: 2,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 15
      }
    },
    press: {
      scale: 0.98,
      transition: { duration: 100 }
    }
  },
  
  // Progress Celebration
  progressUpdate: {
    bar: {
      width: [0, '100%'],
      transition: {
        duration: 500,
        easing: 'smoothOut'
      }
    },
    sparkles: {
      opacity: [0, 1, 0],
      scale: [0.5, 1.2, 0.8],
      translateY: [-10, -20, -15],
      duration: 800,
      easing: 'bounceOut'
    }
  }
}
```

## Screen-by-Screen Premium Design Specifications

### Screen 1: Welcome & Hero Experience

#### Visual Design Specifications
```javascript
const WelcomeScreen = {
  layout: {
    container: {
      backgroundColor: 'linear-gradient(135deg, #F97316 0%, #FB923C 50%, #FF8C42 100%)',
      paddingHorizontal: 24,
      paddingVertical: 60,
      flex: 1,
      justifyContent: 'space-between'
    },
    
    heroSection: {
      alignItems: 'center',
      marginTop: 80,
      marginBottom: 40
    },
    
    contentSection: {
      alignItems: 'center',
      paddingHorizontal: 20
    },
    
    ctaSection: {
      alignItems: 'center',
      marginBottom: 60
    }
  },
  
  typography: {
    heroTitle: {
      fontSize: 36,
      fontWeight: '700',
      lineHeight: 44,
      textAlign: 'center',
      color: '#FFFFFF',
      letterSpacing: -0.5,
      marginBottom: 16,
      // Advanced shadow for depth
      textShadowColor: 'rgba(0, 0, 0, 0.15)',
      textShadowOffset: { width: 0, height: 2 },
      textShadowRadius: 4
    },
    
    heroSubtitle: {
      fontSize: 18,
      fontWeight: '500',
      lineHeight: 24,
      textAlign: 'center',
      color: 'rgba(255, 255, 255, 0.9)',
      marginBottom: 32,
      letterSpacing: 0.2
    },
    
    valueProposition: {
      fontSize: 16,
      fontWeight: '400',
      lineHeight: 22,
      textAlign: 'center',
      color: 'rgba(255, 255, 255, 0.8)',
      marginBottom: 40,
      paddingHorizontal: 20
    }
  },
  
  components: {
    // Premium Glass Morphism Card
    featureHighlight: {
      backgroundColor: 'rgba(255, 255, 255, 0.15)',
      backdropFilter: 'blur(20px)',
      borderRadius: 16,
      padding: 20,
      marginHorizontal: 20,
      marginBottom: 24,
      borderWidth: 1,
      borderColor: 'rgba(255, 255, 255, 0.2)',
      // Advanced shadow system
      shadowColor: 'rgba(0, 0, 0, 0.1)',
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: 1,
      shadowRadius: 24,
      elevation: 12
    },
    
    // Premium CTA Button
    primaryCTA: {
      backgroundColor: '#FFFFFF',
      borderRadius: 14,
      paddingVertical: 16,
      paddingHorizontal: 40,
      minWidth: 280,
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: 16,
      // Advanced elevation
      shadowColor: 'rgba(0, 0, 0, 0.15)',
      shadowOffset: { width: 0, height: 6 },
      shadowOpacity: 1,
      shadowRadius: 16,
      elevation: 8
    },
    
    // Secondary Login Button
    secondaryCTA: {
      backgroundColor: 'transparent',
      borderRadius: 14,
      paddingVertical: 14,
      paddingHorizontal: 32,
      borderWidth: 1.5,
      borderColor: 'rgba(255, 255, 255, 0.4)',
      alignItems: 'center',
      justifyContent: 'center'
    }
  },
  
  // Content Specifications
  content: {
    heroTitle: "Build Your Dating Confidence",
    heroSubtitle: "AI-powered conversation practice that actually works",
    valueProposition: "Join thousands who've transformed their dating life through personalized conversation training",
    
    featureHighlights: [
      {
        icon: "💬",
        title: "Realistic Practice",
        description: "AI conversations that feel completely natural"
      },
      {
        icon: "🎯",
        title: "Personalized Training", 
        description: "Tailored to your style and comfort level"
      },
      {
        icon: "📈",
        title: "Real Results",
        description: "Track your progress and see confidence grow"
      }
    ],
    
    primaryCTAText: "Start Building Confidence",
    secondaryCTAText: "Already have an account? Sign In"
  }
}
```

#### Animation Implementation
```javascript
// Lottie Animations
const WelcomeLottieAssets = {
  confidenceParticles: require('./assets/confidence-particles.json'),
  heartBeat: require('./assets/heart-beat-subtle.json'),
  floatingElements: require('./assets/floating-elements.json')
}

// Reanimated 3 Implementation
const WelcomeAnimationComponent = () => {
  const fadeIn = useSharedValue(0)
  const slideUp = useSharedValue(50)
  const scale = useSharedValue(0.9)
  
  useEffect(() => {
    // Orchestrated entrance sequence
    fadeIn.value = withDelay(200, withTiming(1, { duration: 800 }))
    slideUp.value = withDelay(300, withSpring(0, { stiffness: 100, damping: 15 }))
    scale.value = withDelay(400, withSpring(1, { stiffness: 120, damping: 12 }))
  }, [])
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: fadeIn.value,
    transform: [
      { translateY: slideUp.value },
      { scale: scale.value }
    ]
  }))
  
  return (
    <Animated.View style={animatedStyle}>
      {/* Screen content */}
    </Animated.View>
  )
}
```

### Screen 2: Age Verification (Premium Polish)

#### Visual Design Specifications
```javascript
const AgeVerificationScreen = {
  layout: {
    container: {
      backgroundColor: '#FFFFFF',
      flex: 1,
      paddingHorizontal: 24,
      justifyContent: 'center'
    },
    
    headerSection: {
      alignItems: 'center',
      marginBottom: 60
    },
    
    inputSection: {
      alignItems: 'center',
      marginBottom: 40
    },
    
    legalSection: {
      alignItems: 'center',
      marginBottom: 40,
      paddingHorizontal: 20
    }
  },
  
  components: {
    // Premium Input Field
    ageInput: {
      backgroundColor: '#F9FAFB',
      borderRadius: 12,
      borderWidth: 1,
      borderColor: '#E5E7EB',
      paddingVertical: 16,
      paddingHorizontal: 20,
      fontSize: 18,
      fontWeight: '600',
      textAlign: 'center',
      minWidth: 120,
      // Focus state
      focusedBorderColor: '#F97316',
      focusedBackgroundColor: '#FFF9F5',
      // Shadow
      shadowColor: 'rgba(0, 0, 0, 0.04)',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 1,
      shadowRadius: 8
    },
    
    // Animated Check Icon
    validationIcon: {
      position: 'absolute',
      right: 16,
      top: '50%',
      transform: [{ translateY: -12 }]
    }
  },
  
  content: {
    title: "Verify Your Age",
    subtitle: "FlirtCraft is designed for adults 18 and older",
    inputLabel: "Enter your age",
    legalText: "By continuing, you confirm you are at least 18 years old and agree to our Terms of Service and Privacy Policy.",
    continueText: "Continue"
  }
}
```

### Screen 3: Registration/Sign In (Enhanced UX)

#### Visual Design Specifications  
```javascript
const AuthScreen = {
  layout: {
    container: {
      backgroundColor: 'linear-gradient(180deg, #FFF9F5 0%, #FFFFFF 100%)',
      flex: 1,
      paddingHorizontal: 24,
      justifyContent: 'space-between'
    },
    
    formSection: {
      backgroundColor: '#FFFFFF',
      borderRadius: 20,
      padding: 28,
      marginHorizontal: 8,
      // Premium shadow
      shadowColor: 'rgba(249, 115, 22, 0.08)',
      shadowOffset: { width: 0, height: 12 },
      shadowOpacity: 1,
      shadowRadius: 24,
      elevation: 12
    }
  },
  
  components: {
    // Premium Form Fields
    inputField: {
      backgroundColor: '#F9FAFB',
      borderRadius: 12,
      borderWidth: 1,
      borderColor: '#E5E7EB',
      paddingVertical: 16,
      paddingHorizontal: 20,
      fontSize: 16,
      fontWeight: '500',
      marginBottom: 16,
      // Advanced focus states
      focusedBorderColor: '#F97316',
      focusedBackgroundColor: '#FFF9F5',
      focusedShadowColor: 'rgba(249, 115, 22, 0.1)',
      focusedShadowRadius: 8
    },
    
    // Password Strength Indicator
    passwordStrength: {
      height: 4,
      backgroundColor: '#E5E7EB',
      borderRadius: 2,
      marginTop: 8,
      marginBottom: 16,
      // Dynamic color based on strength
      strengthColors: {
        weak: '#EF4444',
        medium: '#F59E0B', 
        strong: '#10B981'
      }
    }
  },
  
  // Enhanced Form Validation
  validation: {
    email: {
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: "Please enter a valid email address"
    },
    password: {
      minLength: 8,
      requireUppercase: true,
      requireNumber: true,
      requireSpecial: true,
      message: "Password must be at least 8 characters with uppercase, number, and special character"
    }
  }
}
```

### Screen 4: Preferences (Advanced Selection Interface)

#### Visual Design Specifications
```javascript
const PreferencesScreen = {
  layout: {
    container: {
      backgroundColor: '#FFFFFF',
      flex: 1,
      paddingTop: 40
    },
    
    headerSection: {
      paddingHorizontal: 24,
      marginBottom: 32
    },
    
    selectionGrid: {
      paddingHorizontal: 16,
      marginBottom: 40
    }
  },
  
  components: {
    // Advanced Selection Cards
    selectionCard: {
      backgroundColor: '#FFFFFF',
      borderRadius: 16,
      padding: 20,
      marginHorizontal: 8,
      marginBottom: 16,
      borderWidth: 2,
      borderColor: '#F3F4F6',
      // Default state
      default: {
        shadowColor: 'rgba(0, 0, 0, 0.04)',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 1,
        shadowRadius: 12,
        elevation: 4
      },
      // Selected state
      selected: {
        borderColor: '#F97316',
        backgroundColor: '#FFF9F5',
        shadowColor: 'rgba(249, 115, 22, 0.15)',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 1,
        shadowRadius: 20,
        elevation: 8
      }
    },
    
    // Animated Progress Ring
    progressRing: {
      size: 80,
      strokeWidth: 6,
      backgroundColor: '#F3F4F6',
      progressColor: 'linear-gradient(45deg, #F97316, #FB923C)',
      animationDuration: 800
    }
  },
  
  // Selection Options
  genderPreferences: [
    {
      id: 'women',
      title: 'Women',
      icon: '👩',
      description: 'Practice conversations with women'
    },
    {
      id: 'men', 
      title: 'Men',
      icon: '👨',
      description: 'Practice conversations with men'
    },
    {
      id: 'mixed',
      title: 'Mixed',
      icon: '🌟',
      description: 'Practice with both for variety'
    }
  ],
  
  ageRanges: [
    { id: '18-25', label: '18-25', popular: true },
    { id: '26-35', label: '26-35', popular: true },
    { id: '36-45', label: '36-45', popular: false },
    { id: '46+', label: '46+', popular: false }
  ]
}
```

### Screen 5: Skill Goals (Sophisticated Completion)

#### Visual Design Specifications
```javascript
const SkillGoalsScreen = {
  layout: {
    container: {
      backgroundColor: 'linear-gradient(135deg, #FFFFFF 0%, #FFF9F5 100%)',
      flex: 1,
      paddingTop: 40
    },
    
    completionSection: {
      alignItems: 'center',
      paddingVertical: 60
    }
  },
  
  components: {
    // Skill Goal Cards with Advanced Interactions
    skillCard: {
      backgroundColor: '#FFFFFF',
      borderRadius: 20,
      padding: 24,
      marginHorizontal: 16,
      marginBottom: 20,
      borderWidth: 1,
      borderColor: '#F3F4F6',
      // Hover effects
      pressable: true,
      hoverEffects: {
        scale: 1.02,
        shadowIntensity: 1.5,
        borderColor: '#FDBA74'
      }
    },
    
    // Celebration Animation Container
    celebrationContainer: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 1000,
      pointerEvents: 'none'
    },
    
    // Completion Checkmark
    completionCheckmark: {
      size: 64,
      backgroundColor: 'linear-gradient(135deg, #10B981, #22C55E)',
      borderRadius: 32,
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: 24
    }
  },
  
  // Skill Goal Options
  skillGoals: [
    {
      id: 'conversation_starters',
      title: 'Conversation Starters',
      icon: '💬',
      description: 'Learn how to break the ice naturally',
      difficulty: 'beginner',
      estimatedTime: '2-3 weeks'
    },
    {
      id: 'maintaining_flow',
      title: 'Maintaining Flow', 
      icon: '🌊',
      description: 'Keep conversations engaging and natural',
      difficulty: 'intermediate',
      estimatedTime: '3-4 weeks'
    },
    {
      id: 'storytelling',
      title: 'Storytelling',
      icon: '📚', 
      description: 'Share experiences in captivating ways',
      difficulty: 'advanced',
      estimatedTime: '4-6 weeks'
    }
  ],
  
  // Completion Celebration
  celebrationSequence: {
    duration: 3000,
    effects: [
      'confetti_burst',
      'success_checkmark',
      'progress_completion',
      'welcome_message'
    ]
  }
}
```

## Advanced Micro-Interactions

### Button Interaction System
```javascript
const ButtonMicroInteractions = {
  // Primary CTA Button
  primaryButton: {
    idle: {
      scale: 1,
      opacity: 1,
      shadowOpacity: 0.15
    },
    
    hover: {
      scale: 1.02,
      shadowOpacity: 0.25,
      transition: { duration: 150, easing: 'easeOut' }
    },
    
    pressIn: {
      scale: 0.98,
      shadowOpacity: 0.1,
      transition: { duration: 100, easing: 'easeIn' }
    },
    
    pressOut: {
      scale: 1.02,
      shadowOpacity: 0.25,
      transition: { 
        type: 'spring',
        stiffness: 400,
        damping: 15
      }
    },
    
    loading: {
      opacity: 0.7,
      // Spinner animation
      rotateZ: '360deg',
      transition: {
        repeat: -1,
        duration: 1000,
        easing: 'linear'
      }
    }
  },
  
  // Selection Card Interactions
  selectionCard: {
    idle: {
      scale: 1,
      shadowOpacity: 0.08,
      borderColor: '#F3F4F6'
    },
    
    hover: {
      scale: 1.01,
      shadowOpacity: 0.12,
      borderColor: '#FDBA74',
      transition: { duration: 200 }
    },
    
    selected: {
      scale: 1.03,
      shadowOpacity: 0.2,
      borderColor: '#F97316',
      backgroundColor: '#FFF9F5',
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 20
      }
    },
    
    // Ripple effect on tap
    ripple: {
      backgroundColor: 'rgba(249, 115, 22, 0.1)',
      scale: [0, 4],
      opacity: [0.6, 0],
      duration: 600,
      easing: 'easeOut'
    }
  }
}
```

### Form Field Enhancements
```javascript
const FormFieldMicroInteractions = {
  textInput: {
    // Focus states
    focus: {
      borderColor: '#F97316',
      backgroundColor: '#FFF9F5',
      shadowColor: 'rgba(249, 115, 22, 0.1)',
      shadowOpacity: 1,
      shadowRadius: 12,
      transition: { duration: 200 }
    },
    
    // Validation states
    valid: {
      borderColor: '#10B981',
      backgroundColor: '#F0FDF4',
      // Checkmark animation
      checkmarkScale: [0, 1.2, 1],
      checkmarkOpacity: [0, 1],
      transition: { duration: 300, delay: 100 }
    },
    
    invalid: {
      borderColor: '#EF4444',
      backgroundColor: '#FEF2F2',
      // Shake animation
      translateX: [-4, 4, -4, 4, 0],
      transition: { duration: 400, easing: 'easeInOut' }
    },
    
    // Typing animation
    typing: {
      // Subtle pulse on active typing
      shadowOpacity: [0.1, 0.2, 0.1],
      transition: {
        repeat: -1,
        duration: 1500,
        easing: 'easeInOut'
      }
    }
  },
  
  // Label animations
  floatingLabel: {
    inactive: {
      translateY: 0,
      scale: 1,
      color: '#9CA3AF'
    },
    
    active: {
      translateY: -24,
      scale: 0.85,
      color: '#F97316',
      transition: {
        duration: 200,
        easing: 'easeOut'
      }
    }
  }
}
```

## Premium Loading States

### Screen Transitions
```javascript
const ScreenTransitions = {
  // Page transitions
  screenSlide: {
    enter: {
      translateX: [300, 0],
      opacity: [0, 1],
      transition: {
        duration: 400,
        easing: 'confidenceCurve'
      }
    },
    
    exit: {
      translateX: [0, -300],
      opacity: [1, 0],
      transition: {
        duration: 300,
        easing: 'easeIn'
      }
    }
  },
  
  // Loading skeletons
  skeleton: {
    backgroundColor: '#F3F4F6',
    borderRadius: 8,
    // Shimmer effect
    shimmer: {
      translateX: [-100, 400],
      opacity: [0.3, 0.7, 0.3],
      transition: {
        repeat: -1,
        duration: 1500,
        easing: 'linear'
      }
    }
  },
  
  // Progress indicators
  progressBar: {
    track: {
      backgroundColor: '#F3F4F6',
      height: 6,
      borderRadius: 3
    },
    
    fill: {
      backgroundColor: 'linear-gradient(90deg, #F97316, #FB923C)',
      height: 6,
      borderRadius: 3,
      // Smooth progress animation
      widthAnimation: {
        duration: 800,
        easing: 'confidenceCurve'
      }
    },
    
    // Pulse effect for active progress
    pulse: {
      shadowColor: 'rgba(249, 115, 22, 0.4)',
      shadowOpacity: [0.4, 0.8, 0.4],
      shadowRadius: [4, 8, 4],
      transition: {
        repeat: -1,
        duration: 1200,
        easing: 'easeInOut'
      }
    }
  }
}
```

## Content Strategy Enhancement

### Confidence-Building Copy Framework
```javascript
const ContentStrategy = {
  // Tone of voice guidelines
  toneOfVoice: {
    confident: "Encouraging without being pushy",
    warm: "Friendly and approachable language",
    supportive: "Acknowledges user's feelings and concerns", 
    progressive: "Focuses on growth and improvement",
    inclusive: "Welcoming to all experience levels"
  },
  
  // Enhanced screen copy
  enhancedCopy: {
    welcomeScreen: {
      heroTitle: "Transform Your Dating Confidence",
      heroSubtitle: "AI-powered conversation practice that feels completely natural",
      valueProposition: "Join over 50,000 people who've already improved their dating conversations through personalized AI training",
      
      benefits: [
        {
          icon: "💬",
          title: "Realistic Practice",
          description: "Chat with AI that responds like real people, building genuine conversation skills"
        },
        {
          icon: "🎯", 
          title: "Personalized Training",
          description: "Scenarios tailored to your comfort level, goals, and dating preferences"
        },
        {
          icon: "📈",
          title: "Measurable Progress", 
          description: "Track improvement with detailed insights and confidence metrics"
        }
      ],
      
      socialProof: "★★★★★ Rated 4.8/5 by users who saw real results"
    },
    
    ageVerification: {
      title: "Let's Get Started",
      subtitle: "First, we need to verify you're 18 or older to continue",
      inputPlaceholder: "Enter your age",
      legalText: "FlirtCraft is designed for adults. By continuing, you confirm you meet the age requirement and agree to our Terms & Privacy Policy.",
      encouragement: "Don't worry - we only use this to ensure appropriate content"
    },
    
    registration: {
      title: "Create Your Account",
      subtitle: "Join thousands building their confidence every day",
      emailPlaceholder: "Enter your email address",
      passwordPlaceholder: "Create a secure password",
      privacyAssurance: "🔒 Your data is encrypted and completely private",
      buttonText: "Start My Confidence Journey",
      
      passwordStrengthLabels: {
        weak: "Choose a stronger password",
        medium: "Good password strength", 
        strong: "Great! Very secure password"
      }
    },
    
    preferences: {
      title: "Personalize Your Experience",
      subtitle: "Help us create the perfect practice environment for you",
      
      genderSection: {
        title: "Who would you like to practice conversations with?",
        subtitle: "This helps us provide relevant scenarios and responses"
      },
      
      ageSection: {
        title: "What age range interests you?",
        subtitle: "We'll adjust conversation topics and cultural references accordingly"
      },
      
      encouragement: "These preferences help create realistic practice - you can change them anytime!"
    },
    
    skillGoals: {
      title: "What's Your Main Goal?",
      subtitle: "We'll focus your training on what matters most to you right now",
      
      completionTitle: "You're All Set! 🎉",
      completionSubtitle: "Your personalized training environment is ready",
      completionMessage: "Based on your preferences, we've created custom scenarios to help you build confidence naturally. Let's start practicing!",
      
      finalCTA: "Start Practicing Now"
    }
  },
  
  // Persona-specific messaging
  personaAdaptations: {
    anxiousAlex: {
      reassuranceMessages: [
        "Take your time - there's no rush",
        "Remember: this is a safe space to practice",
        "Every expert was once a beginner"
      ],
      progressEncouragement: [
        "You're doing great!",
        "Small steps lead to big improvements",
        "Your confidence is already growing"
      ]
    },
    
    comebackCatherine: {
      relevanceMessages: [
        "Dating has changed, but good conversation never goes out of style",
        "You're not starting over - you're leveling up",
        "Your experience gives you advantages others don't have"
      ]
    },
    
    confidentCarlos: {
      challengeMessages: [
        "Ready to take your game to the next level?",
        "Let's optimize what you're already good at",
        "Time to master the advanced techniques"
      ]
    },
    
    shySarah: {
      supportMessages: [
        "Everyone starts somewhere - you're being brave!",
        "Practice makes progress, not perfection",
        "You've got this - we believe in you!"
      ]
    }
  }
}
```

## Technical Implementation Guidelines

### React Native Reanimated 3 Integration
```javascript
// Advanced animation hooks
const useConfidenceAnimation = () => {
  const confidence = useSharedValue(0)
  const scale = useSharedValue(0.8)
  const opacity = useSharedValue(0)
  
  const startAnimation = () => {
    confidence.value = withSpring(1, {
      stiffness: 100,
      damping: 15
    })
    
    scale.value = withSpring(1, {
      stiffness: 120,
      damping: 12
    })
    
    opacity.value = withTiming(1, {
      duration: 800,
      easing: Easing.bezier(0.2, 0, 0.2, 1)
    })
  }
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [
      { scale: scale.value },
      { 
        translateY: interpolate(
          confidence.value,
          [0, 1],
          [50, 0],
          Extrapolate.CLAMP
        )
      }
    ]
  }))
  
  return {
    startAnimation,
    animatedStyle,
    confidence
  }
}

// Gesture handling for premium interactions
const useCardInteraction = () => {
  const scale = useSharedValue(1)
  const opacity = useSharedValue(1)
  
  const gesture = Gesture.Tap()
    .onBegin(() => {
      scale.value = withTiming(0.98, { duration: 100 })
    })
    .onFinalize(() => {
      scale.value = withSpring(1, {
        stiffness: 400,
        damping: 15
      })
    })
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value
  }))
  
  return {
    gesture,
    animatedStyle
  }
}
```

### Performance Optimization
```javascript
const PerformanceOptimizations = {
  // Image optimization
  images: {
    format: 'WebP with PNG fallback',
    compression: 'High quality (85%)',
    dimensions: {
      '1x': 'Base resolution',
      '2x': 'Retina displays', 
      '3x': 'iPhone Plus and newer'
    },
    lazyLoading: true,
    caching: 'Aggressive with TTL'
  },
  
  // Animation performance
  animations: {
    useNativeDriver: true,
    removeClippedSubviews: true,
    shouldRasterizeIOS: true,
    renderToHardwareTextureAndroid: true,
    needsOffscreenAlphaCompositing: false
  },
  
  // Memory management
  memory: {
    autoCleanup: true,
    componentUnmounting: 'Cancel all animations',
    backgroundState: 'Pause non-essential animations',
    lowMemoryWarning: 'Clear cache and reduce quality'
  },
  
  // Network optimization
  network: {
    bundleAssets: 'Static animations and images',
    compression: 'Gzip for all text content',
    cacheStrategy: 'Cache-first with fallback',
    prefetch: 'Next screen assets during current screen'
  }
}
```

## Quality Assurance Specifications

### Accessibility Excellence
```javascript
const AccessibilitySpecs = {
  // Screen reader support
  screenReader: {
    semanticLabels: 'Clear, descriptive labels for all interactive elements',
    navigationOrder: 'Logical tab order following visual hierarchy',
    announcements: 'Screen change announcements with context',
    gestureSupport: 'Voice Control and Switch Control compatibility'
  },
  
  // Visual accessibility
  visual: {
    minimumContrastRatio: '4.5:1 for normal text, 3:1 for large text',
    enhancedContrast: '7:1 available for users who need it',
    textScaling: 'Support up to 200% text scaling',
    colorIndependence: 'No information conveyed by color alone'
  },
  
  // Motor accessibility  
  motor: {
    touchTargets: 'Minimum 44×44pt touch targets',
    gestureAlternatives: 'Button alternatives to all swipe gestures',
    timing: 'No time-based interactions without extensions',
    errorTolerance: 'Forgiving input with clear correction paths'
  },
  
  // Cognitive accessibility
  cognitive: {
    language: 'Clear, simple language with explanations',
    navigation: 'Consistent patterns throughout',
    errorHandling: 'Clear error messages with solutions',
    progress: 'Clear indication of progress and next steps'
  }
}
```

### Testing Framework
```javascript
const TestingProtocol = {
  // Visual regression testing
  visualTesting: {
    tools: ['Percy', 'Chromatic', 'Applitools'],
    coverage: 'All screen states and device types',
    threshold: 'Zero tolerance for visual regressions'
  },
  
  // Animation testing
  animationTesting: {
    performance: '60fps maintenance during all animations',
    completion: 'All animations complete as expected',
    interruption: 'Graceful handling of animation interruptions',
    accessibility: 'Respect for reduced motion preferences'
  },
  
  // User experience testing
  uxTesting: {
    completion: '>90% onboarding completion rate in testing',
    timing: 'Average 3.5 minutes total flow time',
    satisfaction: 'Post-onboarding survey >4.5/5 rating',
    retention: '>80% return within 24 hours'
  },
  
  // Cross-platform validation
  platformTesting: {
    devices: 'iPhone SE to iPhone 15 Pro Max, Android 6.0+',
    orientations: 'Portrait primary, landscape support',
    networkConditions: '3G, 4G, WiFi, offline scenarios',
    systemSettings: 'Dark mode, large text, reduced motion'
  }
}
```

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Update color system to orange-only palette
- [ ] Implement advanced gradient system
- [ ] Create premium component library
- [ ] Set up Reanimated 3 architecture

### Phase 2: Screen Redesign (Week 3-4)  
- [ ] Welcome screen with hero animations
- [ ] Age verification with micro-interactions
- [ ] Premium registration form
- [ ] Advanced preferences selection

### Phase 3: Advanced Features (Week 5-6)
- [ ] Skill goals with celebration sequence
- [ ] Loading states and transitions
- [ ] Particle systems and effects
- [ ] Performance optimization

### Phase 4: Polish & Testing (Week 7-8)
- [ ] Accessibility compliance verification
- [ ] Cross-platform testing
- [ ] Performance benchmarking
- [ ] User experience validation

---

*This premium redesign transforms FlirtCraft's onboarding from a basic functional flow into a sophisticated, confidence-building experience that users will remember and recommend. Every animation, color choice, and interaction is designed to build user confidence while maintaining the highest standards of accessibility and performance.*