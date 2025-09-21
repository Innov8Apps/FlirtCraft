# Premium Animation System for FlirtCraft

---
title: FlirtCraft Premium Animation Architecture
description: Advanced animation specifications using React Native Reanimated 3 for FANG-level user experience
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./animations.md
  - ../components/buttons.md
  - ../../features/onboarding/premium-redesign.md
dependencies:
  - React Native Reanimated 3.x
  - React Native Gesture Handler 2.x
  - Lottie React Native 6.x
  - Expo Linear Gradient 12.x
status: draft
---

## Animation Philosophy

FlirtCraft's premium animation system creates psychological safety and confidence through smooth, purposeful motion that feels both sophisticated and warm. Every animation serves to build user confidence rather than just visual appeal.

### Core Principles
- **Confidence-Building Motion**: Animations that make users feel capable and supported
- **Warm Energy**: Orange-based color animations with organic, friendly movement
- **60fps Guarantee**: All animations maintain smooth performance across devices
- **Meaningful Purpose**: No decoration-only animations - every motion serves UX
- **Accessibility-First**: Respect for `prefers-reduced-motion` and cognitive load

## Advanced Timing System

### Custom Easing Functions
```javascript
export const confidenceEasing = {
  // Primary confidence-building curve
  confident: Easing.bezier(0.2, 0, 0.2, 1),
  
  // Warm, organic movements  
  warm: Easing.bezier(0.25, 0.46, 0.45, 0.94),
  
  // Energetic, optimistic motion
  energetic: Easing.bezier(0.68, -0.55, 0.265, 1.55),
  
  // Supportive, gentle transitions
  supportive: Easing.bezier(0.4, 0, 0.6, 1),
  
  // Achievement and success
  celebration: Easing.bezier(0.175, 0.885, 0.32, 1.275),
  
  // Progress and forward motion
  progress: Easing.bezier(0.25, 0.8, 0.25, 1)
}
```

### Duration Hierarchy
```javascript
export const animationDurations = {
  // Micro-interactions (button presses, taps)
  micro: {
    press: 100,        // Button press feedback
    hover: 150,        // Hover state changes
    focus: 200,        // Focus indicators
    validation: 250    // Form field validation feedback
  },
  
  // Component interactions
  component: {
    cardSelection: 300,  // Card selection animations
    formTransition: 350, // Form field state changes
    modalEnter: 400,     // Modal entrance
    pageElement: 450     // Page element animations
  },
  
  // Screen-level animations
  screen: {
    transition: 500,     // Screen-to-screen transitions
    heroEntrance: 600,   // Hero section entrances
    celebration: 800,    // Success celebrations
    onboardingFlow: 1000 // Major onboarding moments
  },
  
  // Cinematic experiences
  cinematic: {
    welcome: 1200,       // Welcome screen hero
    completion: 1500,    // Onboarding completion
    achievement: 1800    // Major achievement moments
  }
}
```

## Sophisticated Animation Components

### 1. Hero Entrance System
```javascript
export const HeroAnimationSystem = {
  // Orchestrated entrance sequence
  welcomeHero: {
    // Background gradient reveal
    backgroundReveal: {
      initial: { opacity: 0, scale: 1.1 },
      animate: {
        opacity: 1,
        scale: 1,
        transition: {
          duration: 1200,
          easing: confidenceEasing.warm
        }
      }
    },
    
    // Title animation with sophisticated staging
    titleSequence: {
      container: {
        initial: { opacity: 0 },
        animate: { 
          opacity: 1,
          transition: {
            staggerChildren: 0.2,
            delayChildren: 0.3
          }
        }
      },
      
      words: {
        initial: { 
          opacity: 0, 
          translateY: 40,
          scale: 0.9
        },
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
      }
    },
    
    // Floating confidence particles
    confidenceParticles: {
      count: 15,
      containerStyle: {
        position: 'absolute',
        width: '100%',
        height: '100%',
        pointerEvents: 'none'
      },
      
      particleAnimation: {
        // Random starting positions
        initialPosition: () => ({
          x: Math.random() * 300,
          y: Math.random() * 200 + 100
        }),
        
        // Floating movement
        floatPattern: {
          translateX: [0, 20, -15, 10, 0],
          translateY: [0, -30, -10, -25, 0],
          opacity: [0, 0.6, 0.8, 0.4, 0],
          scale: [0.5, 1, 1.2, 0.8, 0.5],
          rotate: [0, 180, 360],
          
          timing: {
            duration: 4000,
            repeat: -1,
            easing: confidenceEasing.warm,
            delay: () => Math.random() * 2000
          }
        }
      }
    },
    
    // CTA button sophisticated entrance
    ctaEntrance: {
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
          delay: 800,
          stiffness: 120,
          damping: 12,
          duration: 600
        }
      },
      
      // Advanced hover states
      hover: {
        scale: 1.05,
        shadowOpacity: 0.25,
        shadowRadius: 20,
        shadowOffset: { width: 0, height: 8 },
        transition: {
          duration: 200,
          easing: confidenceEasing.energetic
        }
      }
    }
  }
}
```

### 2. Advanced Selection Interface
```javascript
export const SelectionAnimationSystem = {
  // Card-based selection with premium interactions
  selectionCards: {
    // Container entrance with stagger
    container: {
      initial: { opacity: 0 },
      animate: {
        opacity: 1,
        transition: {
          staggerChildren: 0.12,
          delayChildren: 0.2,
          duration: 400
        }
      }
    },
    
    // Individual card animations
    card: {
      initial: {
        opacity: 0,
        scale: 0.9,
        translateY: 20,
        rotateX: 15
      },
      animate: {
        opacity: 1,
        scale: 1,
        translateY: 0,
        rotateX: 0,
        transition: {
          type: 'spring',
          stiffness: 100,
          damping: 15,
          duration: 500
        }
      },
      
      // Sophisticated interaction states
      hover: {
        scale: 1.02,
        translateY: -4,
        shadowOpacity: 0.15,
        shadowRadius: 16,
        shadowOffset: { width: 0, height: 8 },
        
        // Subtle glow effect
        borderColor: '#FDBA74',
        backgroundColor: '#FFF9F5',
        
        transition: {
          duration: 200,
          easing: confidenceEasing.supportive
        }
      },
      
      // Selection animation
      selected: {
        scale: 1.05,
        translateY: -8,
        shadowOpacity: 0.25,
        shadowRadius: 24,
        shadowOffset: { width: 0, height: 12 },
        
        // Premium selection styling
        borderColor: '#F97316',
        borderWidth: 2,
        backgroundColor: '#FFF9F5',
        
        // Checkmark reveal
        checkmarkReveal: {
          scale: [0, 1.2, 1],
          opacity: [0, 1],
          rotate: [0, 360],
          duration: 400,
          easing: confidenceEasing.celebration
        },
        
        transition: {
          type: 'spring',
          stiffness: 200,
          damping: 20,
          duration: 300
        }
      },
      
      // Press feedback
      press: {
        scale: 0.98,
        transition: {
          duration: 100,
          easing: confidenceEasing.confident
        }
      },
      
      // Ripple effect on selection
      rippleEffect: {
        backgroundColor: 'rgba(249, 115, 22, 0.15)',
        scale: [0, 4],
        opacity: [0.8, 0],
        borderRadius: '50%',
        duration: 600,
        easing: confidenceEasing.progress
      }
    }
  },
  
  // Progress ring animation
  progressRing: {
    size: 80,
    strokeWidth: 6,
    
    // Background circle
    background: {
      stroke: '#F3F4F6',
      strokeOpacity: 1
    },
    
    // Animated progress circle
    progress: {
      stroke: 'url(#orangeGradient)',
      strokeLinecap: 'round',
      
      // Sophisticated progress animation
      animation: {
        strokeDasharray: 251.2, // 2 * π * r (r = 40)
        strokeDashoffset: [251.2, 0],
        
        timing: {
          duration: 1000,
          easing: confidenceEasing.progress,
          delay: 300
        }
      },
      
      // Pulsing effect during animation
      pulse: {
        shadowColor: 'rgba(249, 115, 22, 0.4)',
        shadowOpacity: [0.4, 0.8, 0.4],
        shadowRadius: [8, 16, 8],
        
        timing: {
          duration: 1500,
          repeat: -1,
          easing: confidenceEasing.warm
        }
      }
    },
    
    // Percentage text animation
    percentageText: {
      initial: { opacity: 0, scale: 0.5 },
      animate: {
        opacity: 1,
        scale: 1,
        transition: {
          delay: 400,
          duration: 300,
          easing: confidenceEasing.confident
        }
      },
      
      // Number counting animation
      countUp: {
        from: 0,
        duration: 800,
        easing: confidenceEasing.progress
      }
    }
  }
}
```

### 3. Form Field Premium Interactions
```javascript
export const FormAnimationSystem = {
  // Advanced input field animations
  textInput: {
    // Container with floating label
    container: {
      initial: { opacity: 0, translateY: 20 },
      animate: {
        opacity: 1,
        translateY: 0,
        transition: {
          duration: 300,
          easing: confidenceEasing.supportive
        }
      }
    },
    
    // Input field states
    field: {
      // Focus animation
      focus: {
        borderColor: '#F97316',
        backgroundColor: '#FFF9F5',
        shadowColor: 'rgba(249, 115, 22, 0.1)',
        shadowOpacity: 1,
        shadowRadius: 12,
        shadowOffset: { width: 0, height: 4 },
        
        // Subtle scale effect
        scale: 1.01,
        
        transition: {
          duration: 200,
          easing: confidenceEasing.confident
        }
      },
      
      // Validation states
      valid: {
        borderColor: '#10B981',
        backgroundColor: '#F0FDF4',
        
        // Success checkmark animation
        checkmarkAnimation: {
          scale: [0, 1.2, 1],
          opacity: [0, 1],
          translateX: [10, 0],
          
          timing: {
            duration: 400,
            easing: confidenceEasing.celebration,
            delay: 100
          }
        }
      },
      
      invalid: {
        borderColor: '#EF4444',
        backgroundColor: '#FEF2F2',
        
        // Shake animation for errors
        shakeAnimation: {
          translateX: [-4, 4, -4, 4, 0],
          timing: {
            duration: 400,
            easing: confidenceEasing.energetic
          }
        }
      }
    },
    
    // Floating label animation
    floatingLabel: {
      inactive: {
        translateY: 0,
        scale: 1,
        color: '#9CA3AF',
        opacity: 0.7
      },
      
      active: {
        translateY: -28,
        scale: 0.85,
        color: '#F97316',
        opacity: 1,
        
        transition: {
          duration: 200,
          easing: confidenceEasing.supportive
        }
      }
    },
    
    // Password strength indicator
    passwordStrength: {
      container: {
        height: 4,
        backgroundColor: '#F3F4F6',
        borderRadius: 2,
        marginTop: 8,
        overflow: 'hidden'
      },
      
      // Animated strength bar
      strengthBar: {
        height: '100%',
        borderRadius: 2,
        
        // Dynamic color and width based on strength
        weak: {
          backgroundColor: '#EF4444',
          width: '33%',
          transition: { duration: 300 }
        },
        
        medium: {
          backgroundColor: 'linear-gradient(90deg, #F59E0B, #F97316)',
          width: '66%',
          transition: { duration: 300 }
        },
        
        strong: {
          backgroundColor: 'linear-gradient(90deg, #10B981, #22C55E)',
          width: '100%',
          transition: { duration: 300 }
        }
      },
      
      // Pulse effect for active typing
      typingPulse: {
        shadowColor: 'rgba(249, 115, 22, 0.3)',
        shadowOpacity: [0.3, 0.6, 0.3],
        shadowRadius: [2, 4, 2],
        
        timing: {
          duration: 1200,
          repeat: -1,
          easing: confidenceEasing.warm
        }
      }
    }
  }
}
```

### 4. Celebration & Success Animations
```javascript
export const CelebrationAnimationSystem = {
  // Onboarding completion celebration
  completionCelebration: {
    // Main container orchestration
    sequence: {
      duration: 3000,
      phases: [
        'confetti_burst',
        'checkmark_reveal', 
        'success_message',
        'cta_entrance'
      ]
    },
    
    // Confetti burst system
    confettiBurst: {
      particleCount: 50,
      colors: ['#F97316', '#FB923C', '#FDBA74', '#FED7AA'],
      
      // Particle physics
      particles: {
        initial: {
          position: { x: 'center', y: 'center' },
          velocity: {
            x: () => (Math.random() - 0.5) * 200,
            y: () => Math.random() * -150 - 50
          },
          rotation: 0,
          scale: 0
        },
        
        animation: {
          // Burst outward movement
          translateX: 'velocity.x * time',
          translateY: 'velocity.y * time + 0.5 * gravity * time^2',
          
          // Rotation and scaling
          rotate: [0, 360 * (Math.random() > 0.5 ? 1 : -1)],
          scale: [0, 1, 0.8, 0],
          
          // Fade out
          opacity: [0, 1, 1, 0],
          
          timing: {
            duration: 2000,
            easing: confidenceEasing.celebration
          }
        }
      }
    },
    
    // Success checkmark reveal
    checkmarkReveal: {
      container: {
        size: 80,
        backgroundColor: 'linear-gradient(135deg, #10B981, #22C55E)',
        borderRadius: 40,
        
        // Container animation
        initial: { scale: 0, opacity: 0 },
        animate: {
          scale: [0, 1.2, 1],
          opacity: 1,
          
          transition: {
            delay: 500,
            duration: 600,
            easing: confidenceEasing.celebration
          }
        }
      },
      
      // Checkmark path animation
      checkmark: {
        stroke: '#FFFFFF',
        strokeWidth: 4,
        strokeLinecap: 'round',
        strokeLinejoin: 'round',
        
        // Path drawing animation
        pathAnimation: {
          strokeDasharray: 100,
          strokeDashoffset: [100, 0],
          
          timing: {
            delay: 800,
            duration: 400,
            easing: confidenceEasing.confident
          }
        }
      }
    },
    
    // Success message entrance
    successMessage: {
      title: {
        initial: {
          opacity: 0,
          translateY: 30,
          scale: 0.9
        },
        animate: {
          opacity: 1,
          translateY: 0,
          scale: 1,
          
          transition: {
            delay: 1200,
            duration: 500,
            easing: confidenceEasing.warm
          }
        }
      },
      
      subtitle: {
        initial: {
          opacity: 0,
          translateY: 20
        },
        animate: {
          opacity: 1,
          translateY: 0,
          
          transition: {
            delay: 1400,
            duration: 400,
            easing: confidenceEasing.supportive
          }
        }
      }
    },
    
    // Final CTA entrance
    finalCTA: {
      initial: {
        opacity: 0,
        scale: 0.8,
        translateY: 20
      },
      animate: {
        opacity: 1,
        scale: 1,
        translateY: 0,
        
        transition: {
          delay: 1800,
          type: 'spring',
          stiffness: 150,
          damping: 15,
          duration: 600
        }
      },
      
      // Pulsing effect to draw attention
      pulse: {
        scale: [1, 1.05, 1],
        shadowOpacity: [0.15, 0.25, 0.15],
        
        timing: {
          delay: 2400,
          duration: 1500,
          repeat: -1,
          easing: confidenceEasing.warm
        }
      }
    }
  },
  
  // Micro-celebration for step completion
  stepCompletion: {
    // Progress bar fill animation
    progressFill: {
      width: ['0%', '100%'],
      backgroundColor: 'linear-gradient(90deg, #F97316, #FB923C)',
      
      timing: {
        duration: 600,
        easing: confidenceEasing.progress
      }
    },
    
    // Sparkle effect
    sparkles: {
      count: 8,
      animation: {
        opacity: [0, 1, 0],
        scale: [0.5, 1.2, 0.8],
        translateY: [-5, -15, -10],
        rotate: [0, 180],
        
        timing: {
          duration: 800,
          stagger: 100,
          easing: confidenceEasing.celebration
        }
      }
    }
  }
}
```

## Screen Transition System

### Advanced Page Transitions
```javascript
export const ScreenTransitionSystem = {
  // Onboarding flow transitions
  onboardingTransitions: {
    // Forward navigation (next screen)
    forward: {
      exitingScreen: {
        translateX: [0, -100],
        opacity: [1, 0],
        scale: [1, 0.95],
        
        timing: {
          duration: 300,
          easing: confidenceEasing.confident
        }
      },
      
      enteringScreen: {
        translateX: [100, 0],
        opacity: [0, 1],
        scale: [1.05, 1],
        
        timing: {
          duration: 400,
          easing: confidenceEasing.warm,
          delay: 100
        }
      }
    },
    
    // Backward navigation (previous screen)
    backward: {
      exitingScreen: {
        translateX: [0, 100],
        opacity: [1, 0],
        scale: [1, 0.95],
        
        timing: {
          duration: 300,
          easing: confidenceEasing.confident
        }
      },
      
      enteringScreen: {
        translateX: [-100, 0],
        opacity: [0, 1],
        scale: [1.05, 1],
        
        timing: {
          duration: 400,
          easing: confidenceEasing.supportive,
          delay: 100
        }
      }
    }
  },
  
  // Modal transitions
  modalTransitions: {
    // Modal entrance
    enter: {
      backdrop: {
        opacity: [0, 1],
        timing: { duration: 200 }
      },
      
      modal: {
        opacity: [0, 1],
        scale: [0.9, 1],
        translateY: [20, 0],
        
        timing: {
          duration: 300,
          easing: confidenceEasing.supportive,
          delay: 100
        }
      }
    },
    
    // Modal exit
    exit: {
      modal: {
        opacity: [1, 0],
        scale: [1, 0.9],
        translateY: [0, 20],
        
        timing: {
          duration: 200,
          easing: confidenceEasing.confident
        }
      },
      
      backdrop: {
        opacity: [1, 0],
        timing: { 
          duration: 300,
          delay: 100
        }
      }
    }
  }
}
```

## Loading States & Skeleton Screens

### Premium Loading Animations
```javascript
export const LoadingAnimationSystem = {
  // Sophisticated skeleton screens
  skeletonSystem: {
    // Base skeleton component
    baseSkeleton: {
      backgroundColor: '#F3F4F6',
      borderRadius: 8,
      
      // Shimmer overlay effect
      shimmerOverlay: {
        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent)',
        
        animation: {
          translateX: [-200, 400],
          timing: {
            duration: 1500,
            repeat: -1,
            easing: 'linear'
          }
        }
      }
    },
    
    // Screen-specific skeleton layouts
    welcomeScreenSkeleton: {
      heroTitle: {
        width: '80%',
        height: 40,
        marginBottom: 16
      },
      subtitle: {
        width: '60%', 
        height: 20,
        marginBottom: 32
      },
      featureCards: {
        count: 3,
        height: 80,
        marginBottom: 16,
        stagger: 200
      }
    },
    
    preferencesScreenSkeleton: {
      selectionCards: {
        count: 3,
        height: 120,
        marginBottom: 16,
        stagger: 150
      }
    }
  },
  
  // Loading indicators
  loadingIndicators: {
    // Primary loading spinner
    primarySpinner: {
      size: 24,
      color: '#F97316',
      
      // Custom spinner animation
      rotation: {
        rotate: [0, 360],
        timing: {
          duration: 1000,
          repeat: -1,
          easing: 'linear'
        }
      },
      
      // Pulsing effect
      pulse: {
        opacity: [0.6, 1, 0.6],
        scale: [0.9, 1, 0.9],
        timing: {
          duration: 1500,
          repeat: -1,
          easing: confidenceEasing.warm
        }
      }
    },
    
    // Progress loading bar
    progressBar: {
      track: {
        backgroundColor: '#F3F4F6',
        height: 4,
        borderRadius: 2
      },
      
      fill: {
        backgroundColor: 'linear-gradient(90deg, #F97316, #FB923C)',
        height: 4,
        borderRadius: 2,
        
        // Indeterminate animation
        indeterminateAnimation: {
          translateX: [-200, 400],
          width: [0, 200, 0],
          
          timing: {
            duration: 1500,
            repeat: -1,
            easing: confidenceEasing.progress
          }
        }
      }
    },
    
    // Dots loading indicator
    dotsIndicator: {
      dotCount: 3,
      dotSize: 8,
      dotColor: '#F97316',
      spacing: 12,
      
      // Staggered bounce animation
      bounceAnimation: {
        translateY: [0, -8, 0],
        timing: {
          duration: 600,
          repeat: -1,
          stagger: 200,
          easing: confidenceEasing.energetic
        }
      }
    }
  }
}
```

## Gesture-Based Interactions

### Advanced Gesture Animations
```javascript
export const GestureAnimationSystem = {
  // Swipe gestures for card selection
  cardSwipeGestures: {
    // Pan gesture configuration
    panGesture: {
      threshold: 50,
      velocity: 500,
      
      // During gesture
      active: {
        translateX: 'gestureX',
        translateY: 'gestureY * 0.2',
        rotate: 'gestureX * 0.1',
        scale: 1.05,
        
        // Dynamic shadow based on movement
        shadowOpacity: 'Math.abs(gestureX) * 0.001 + 0.1',
        shadowRadius: 'Math.abs(gestureX) * 0.05 + 8'
      },
      
      // Gesture completion
      complete: {
        accepted: {
          translateX: 300,
          opacity: 0,
          rotate: 15,
          
          timing: {
            duration: 300,
            easing: confidenceEasing.confident
          }
        },
        
        rejected: {
          translateX: -300,
          opacity: 0,
          rotate: -15,
          
          timing: {
            duration: 300,
            easing: confidenceEasing.confident
          }
        },
        
        // Snap back if gesture incomplete
        snapBack: {
          translateX: 0,
          translateY: 0,
          rotate: 0,
          scale: 1,
          
          timing: {
            type: 'spring',
            stiffness: 200,
            damping: 20
          }
        }
      }
    }
  },
  
  // Pull-to-refresh gesture
  pullToRefresh: {
    // Pull gesture configuration
    pullGesture: {
      threshold: 80,
      maxPull: 120,
      
      // During pull
      pulling: {
        translateY: 'Math.min(gestureY, maxPull)',
        
        // Dynamic refresh indicator
        indicatorOpacity: 'Math.min(gestureY / threshold, 1)',
        indicatorRotation: 'gestureY * 2',
        indicatorScale: 'Math.min(gestureY / threshold, 1)'
      },
      
      // Release animations
      release: {
        refresh: {
          translateY: 60,
          indicatorRotation: [0, 720],
          
          timing: {
            duration: 1000,
            easing: confidenceEasing.progress
          }
        },
        
        snapBack: {
          translateY: 0,
          indicatorOpacity: 0,
          
          timing: {
            type: 'spring',
            stiffness: 150,
            damping: 20
          }
        }
      }
    }
  }
}
```

## Performance Optimization

### Animation Performance Guidelines
```javascript
export const PerformanceOptimizations = {
  // Native driver usage
  nativeDriver: {
    // Properties that can use native driver
    nativeProperties: [
      'opacity',
      'transform.translateX',
      'transform.translateY', 
      'transform.scale',
      'transform.rotate'
    ],
    
    // Properties that require JS thread
    jsProperties: [
      'backgroundColor',
      'borderColor',
      'width',
      'height',
      'shadowOpacity'
    ],
    
    // Optimization strategy
    strategy: 'Use native driver for all transform and opacity animations, batch JS thread animations'
  },
  
  // Memory management
  memoryOptimization: {
    // Animation cleanup
    cleanup: {
      onUnmount: 'Cancel all running animations',
      onBackground: 'Pause non-essential animations',
      onLowMemory: 'Stop decorative animations'
    },
    
    // Resource management
    resources: {
      lottieAnimations: 'Preload and cache essential animations',
      complexAnimations: 'Use requestAnimationFrame for complex calculations',
      particleSystems: 'Limit particle count based on device performance'
    }
  },
  
  // Performance monitoring
  monitoring: {
    frameRate: {
      target: 60,
      monitoring: 'Track frame drops during animations',
      fallback: 'Reduce animation complexity if frames drop below 50fps'
    },
    
    cpuUsage: {
      threshold: '70%',
      optimization: 'Simplify animations if CPU usage exceeds threshold'
    }
  }
}
```

## Accessibility Integration

### Motion Accessibility
```javascript
export const MotionAccessibility = {
  // Reduced motion preferences
  reducedMotion: {
    detection: 'AccessibilityInfo.isReduceMotionEnabled()',
    
    // Alternative animations for reduced motion
    alternatives: {
      // Instead of slide transitions
      slideTransition: {
        normal: { translateX: [100, 0], duration: 300 },
        reduced: { opacity: [0, 1], duration: 200 }
      },
      
      // Instead of scale animations
      scaleAnimation: {
        normal: { scale: [0.8, 1], duration: 400 },
        reduced: { opacity: [0.5, 1], duration: 200 }
      },
      
      // Instead of rotation animations
      rotationAnimation: {
        normal: { rotate: [0, 360], duration: 1000 },
        reduced: { opacity: [0.7, 1, 0.7], duration: 500 }
      }
    }
  },
  
  // Screen reader integration
  screenReader: {
    // Animation announcements
    announcements: {
      onStart: 'Animation started',
      onComplete: 'Animation completed',
      onProgress: 'Progress updated to X%'
    },
    
    // Focus management during animations
    focusManagement: {
      preserveFocus: 'Maintain focus during non-disruptive animations',
      moveFocus: 'Move focus to new content after screen transitions',
      skipAnimation: 'Provide option to skip long animations'
    }
  }
}
```

## Implementation Examples

### React Native Reanimated 3 Hooks
```javascript
// Custom hook for confidence-building animations
export const useConfidenceAnimation = (delay = 0) => {
  const opacity = useSharedValue(0)
  const scale = useSharedValue(0.9)
  const translateY = useSharedValue(30)
  
  useEffect(() => {
    opacity.value = withDelay(
      delay,
      withTiming(1, {
        duration: animationDurations.component.pageElement,
        easing: confidenceEasing.confident
      })
    )
    
    scale.value = withDelay(
      delay,
      withSpring(1, {
        stiffness: 100,
        damping: 15
      })
    )
    
    translateY.value = withDelay(
      delay,
      withSpring(0, {
        stiffness: 120,
        damping: 12
      })
    )
  }, [delay])
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [
      { scale: scale.value },
      { translateY: translateY.value }
    ]
  }))
  
  return {
    animatedStyle,
    isComplete: opacity.value === 1
  }
}

// Hook for selection card interactions
export const useSelectionCardAnimation = () => {
  const scale = useSharedValue(1)
  const shadowOpacity = useSharedValue(0.08)
  const borderColor = useSharedValue('#F3F4F6')
  
  const gesture = Gesture.Tap()
    .onBegin(() => {
      scale.value = withTiming(0.98, { duration: 100 })
    })
    .onFinalize((_, success) => {
      if (success) {
        // Selection animation
        scale.value = withSpring(1.05, {
          stiffness: 200,
          damping: 20
        })
        shadowOpacity.value = withTiming(0.25, { duration: 200 })
        borderColor.value = withTiming('#F97316', { duration: 200 })
      } else {
        // Reset to normal
        scale.value = withSpring(1, {
          stiffness: 400,
          damping: 25
        })
      }
    })
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    shadowOpacity: shadowOpacity.value,
    borderColor: borderColor.value
  }))
  
  return {
    gesture,
    animatedStyle
  }
}
```

---

*This premium animation system transforms FlirtCraft from a static interface into a dynamic, confidence-building experience. Every motion is carefully crafted to support user psychology while maintaining excellent performance and accessibility standards.*