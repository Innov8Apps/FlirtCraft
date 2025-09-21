# Onboarding Feature - Interactions

---
title: Onboarding Feature Interactions and Animations
description: Complete interaction patterns, animations, and micro-interactions for app onboarding
feature: onboarding
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - accessibility.md
  - implementation.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native Reanimated 3.6+
  - NativeBase UI v2 with animated components
  - NativeWind 4.1 for utility animations
  - design system animation tokens
status: approved
---

## Interactions Overview

The premium onboarding experience uses React Native Reanimated 3 sophisticated animations and micro-interactions to create emotional engagement, build confidence, and guide users smoothly into the app. All animations follow confidence-building psychology and the pure orange design system while addressing the unique emotional needs of first-time users through celebration effects and particle systems.

## Table of Contents

1. [App Launch Sequence](#app-launch-sequence)
2. [Welcome Flow Animations](#welcome-flow-animations)
3. [Trust Building Interactions](#trust-building-interactions)
4. [Registration Form Interactions](#registration-form-interactions)
5. [Step Navigation System](#step-navigation-system)
6. [Permission Request Interactions](#permission-request-interactions)
7. [Completion Celebrations](#completion-celebrations)

---

## App Launch Sequence

### Splash Screen Animation

#### Brand Introduction Sequence

```javascript
// React Native Reanimated 3 Implementation
const splashLogoScale = useSharedValue(0.8);
const splashLogoOpacity = useSharedValue(0);
const backgroundGradient = useSharedValue(0);
const loadingProgress = useSharedValue(0);

const startSplashSequence = () => {
  'worklet';
  
  // Background gradient animation
  backgroundGradient.value = withTiming(1, {
    duration: 800,
    easing: Easing.out(Easing.cubic),
  });
  
  // Logo entrance with spring
  splashLogoOpacity.value = withDelay(200,
    withTiming(1, {
      duration: 300,
      easing: Easing.out(Easing.cubic),
    })
  );
  
  splashLogoScale.value = withDelay(200,
    withSpring(1, {
      damping: 12,
      stiffness: 100,
    })
  );
  
  // Loading progress simulation
  loadingProgress.value = withDelay(500,
    withTiming(1, {
      duration: 1500,
      easing: Easing.out(Easing.cubic),
    })
  );
  
  // Transition to welcome screen
  runOnJS(setTimeout)(() => {
    navigateToWelcome();
  }, 2500);
};

// Splash screen animated styles
const splashLogoStyle = useAnimatedStyle(() => ({
  transform: [{ scale: splashLogoScale.value }],
  opacity: splashLogoOpacity.value,
}));

const splashBackgroundStyle = useAnimatedStyle(() => ({
  backgroundColor: interpolateColor(
    backgroundGradient.value,
    [0, 1],
    ['#FFFFFF', '#FFF7ED'] // White to Primary-50
  ),
}));
```

#### Loading Animation

```javascript
const loadingDots = useSharedValue(0);
const loadingTextOpacity = useSharedValue(0);

const animateLoading = () => {
  // Subtle loading dots animation
  loadingDots.value = withRepeat(
    withSequence(
      withTiming(0, { duration: 0 }),
      withTiming(1, { duration: 400 }),
      withTiming(0.3, { duration: 400 }),
      withTiming(1, { duration: 400 })
    ),
    -1, // Infinite
    false
  );
  
  // Loading text fade in
  loadingTextOpacity.value = withDelay(800,
    withTiming(1, {
      duration: 300,
      easing: Easing.out(Easing.cubic),
    })
  );
};
```

---

## Welcome Flow Animations

### Screen Transition System

#### Horizontal Slide Transitions

```typescript
// React Native Reanimated 3 with Layout Animations
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  withSequence,
  withDelay,
  Easing,
  SlideInRight,
  SlideOutLeft,
  FadeIn,
  FadeOut,
  Layout,
  runOnJS,
} from 'react-native-reanimated';

// Modern Reanimated 3 approach using Layout Animations
const OnboardingScreenTransition: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <Animated.View
      layout={Layout.springify().damping(15).stiffness(100)}
      entering={SlideInRight.duration(400).easing(Easing.out(Easing.quad))}
      exiting={SlideOutLeft.duration(300).easing(Easing.in(Easing.quad))}
      style={{ flex: 1 }}
    >
      {children}
    </Animated.View>
  );
};

// Custom hook for complex screen transitions
const useScreenTransition = () => {
  const screenTranslateX = useSharedValue(0);
  const screenOpacity = useSharedValue(1);
  const nextScreenTranslateX = useSharedValue(100);
  const isTransitioning = useSharedValue(false);

  const transitionToNextScreen = (onComplete?: () => void) => {
    'worklet';
    
    if (isTransitioning.value) return;
    isTransitioning.value = true;
    
    // Coordinated slide and fade animation
    screenTranslateX.value = withTiming(-100, {
      duration: 300,
      easing: Easing.bezier(0.25, 0.46, 0.45, 0.94), // ease-out-quart
    });
    
    screenOpacity.value = withTiming(0, {
      duration: 200,
      easing: Easing.in(Easing.cubic),
    });
    
    // Next screen entrance with spring physics
    nextScreenTranslateX.value = withDelay(150,
      withSpring(0, {
        damping: 20,
        stiffness: 150,
        mass: 1,
        overshootClamping: false,
        restSpeedThreshold: 0.01,
        restDisplacementThreshold: 0.01,
      }, () => {
        // Animation completed
        isTransitioning.value = false;
        if (onComplete) {
          runOnJS(onComplete)();
        }
      })
    );
    
    // Trigger content update mid-transition
    runOnJS(setTimeout)(() => {
      // Update screen content during transition
    }, 150);
  };

  // Animated styles with proper typing
  const currentScreenStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: `${screenTranslateX.value}%` }],
    opacity: screenOpacity.value,
  }), []);

  const nextScreenStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: `${nextScreenTranslateX.value}%` }],
  }), []);

  const resetTransition = () => {
    'worklet';
    screenTranslateX.value = 0;
    screenOpacity.value = 1;
    nextScreenTranslateX.value = 100;
    isTransitioning.value = false;
  };

  return {
    currentScreenStyle,
    nextScreenStyle,
    transitionToNextScreen,
    resetTransition,
    isTransitioning: isTransitioning.value,
  };
};
```

### Content Entrance Animations

#### Staggered Content Animation

```javascript
const titleOpacity = useSharedValue(0);
const titleTranslateY = useSharedValue(30);
const subtitleOpacity = useSharedValue(0);
const subtitleTranslateY = useSharedValue(30);
const benefitCardOpacities = useSharedValue([0, 0, 0]);
const benefitCardTranslateYs = useSharedValue([30, 30, 30]);
const buttonScale = useSharedValue(0.9);
const buttonOpacity = useSharedValue(0);

const animateWelcomeContent = () => {
  'worklet';
  
  // Title animation
  titleOpacity.value = withTiming(1, {
    duration: 400,
    easing: Easing.out(Easing.cubic),
  });
  
  titleTranslateY.value = withTiming(0, {
    duration: 500,
    easing: Easing.out(Easing.back(1.1)),
  });
  
  // Subtitle animation with delay
  subtitleOpacity.value = withDelay(200,
    withTiming(1, {
      duration: 400,
      easing: Easing.out(Easing.cubic),
    })
  );
  
  subtitleTranslateY.value = withDelay(200,
    withTiming(0, {
      duration: 500,
      easing: Easing.out(Easing.back(1.1)),
    })
  );
  
  // Staggered benefit cards
  benefitCardOpacities.value.forEach((_, index) => {
    const delay = 400 + (index * 100);
    
    benefitCardOpacities.value[index] = withDelay(delay,
      withTiming(1, {
        duration: 300,
        easing: Easing.out(Easing.cubic),
      })
    );
    
    benefitCardTranslateYs.value[index] = withDelay(delay,
      withTiming(0, {
        duration: 400,
        easing: Easing.out(Easing.back(1.1)),
      })
    );
  });
  
  // Button entrance
  buttonOpacity.value = withDelay(800,
    withTiming(1, {
      duration: 300,
      easing: Easing.out(Easing.cubic),
    })
  );
  
  buttonScale.value = withDelay(800,
    withSpring(1, {
      damping: 10,
      stiffness: 150,
    })
  );
};
```

### Hero Illustration Animation

#### Subtle Motion Graphics

```javascript
const illustrationScale = useSharedValue(1);
const illustrationRotation = useSharedValue(0);
const illustrationOpacity = useSharedValue(0);

const animateHeroIllustration = () => {
  // Fade in illustration
  illustrationOpacity.value = withDelay(300,
    withTiming(1, {
      duration: 600,
      easing: Easing.out(Easing.cubic),
    })
  );
  
  // Subtle breathing animation
  illustrationScale.value = withRepeat(
    withSequence(
      withTiming(1.02, {
        duration: 3000,
        easing: Easing.inOut(Easing.sine),
      }),
      withTiming(1, {
        duration: 3000,
        easing: Easing.inOut(Easing.sine),
      })
    ),
    -1, // Infinite
    false
  );
  
  // Very subtle rotation for liveliness
  illustrationRotation.value = withRepeat(
    withSequence(
      withTiming(-1, {
        duration: 4000,
        easing: Easing.inOut(Easing.sine),
      }),
      withTiming(1, {
        duration: 4000,
        easing: Easing.inOut(Easing.sine),
      })
    ),
    -1, // Infinite
    false
  );
};
```

---

## Trust Building Interactions

### Privacy Assurance Animations

#### Security Icon Animation

```javascript
const securityShieldScale = useSharedValue(0);
const securityShieldGlow = useSharedValue(0);
const privacyPointsOpacity = useSharedValue([0, 0, 0, 0]);
const checkmarkScales = useSharedValue([0, 0, 0, 0]);

const animatePrivacyScreen = () => {
  // Shield entrance with impact
  securityShieldScale.value = withSpring(1, {
    damping: 8,
    stiffness: 150,
  });
  
  // Subtle glow effect for trust
  securityShieldGlow.value = withRepeat(
    withSequence(
      withTiming(0.3, {
        duration: 2000,
        easing: Easing.inOut(Easing.sine),
      }),
      withTiming(0.1, {
        duration: 2000,
        easing: Easing.inOut(Easing.sine),
      })
    ),
    -1, // Infinite
    false
  );
  
  // Staggered privacy points with checkmark animations
  privacyPointsOpacity.value.forEach((_, index) => {
    const delay = 300 + (index * 150);
    
    privacyPointsOpacity.value[index] = withDelay(delay,
      withTiming(1, {
        duration: 400,
        easing: Easing.out(Easing.cubic),
      })
    );
    
    // Checkmark pop-in after text appears
    checkmarkScales.value[index] = withDelay(delay + 200,
      withSpring(1, {
        damping: 10,
        stiffness: 200,
      })
    );
  });
};
```

### Trust Building Micro-interactions

#### Card Hover/Press Effects

```javascript
const trustCardScale = useSharedValue(1);
const trustCardShadow = useSharedValue(2);
const trustCardBorderOpacity = useSharedValue(0);

const handleTrustCardPress = () => {
  // Subtle press feedback without being distracting
  trustCardScale.value = withSequence(
    withTiming(0.98, { duration: 100 }),
    withTiming(1, { duration: 150 })
  );
  
  // Enhanced shadow on interaction
  trustCardShadow.value = withSequence(
    withTiming(8, { duration: 100 }),
    withTiming(2, { duration: 300 })
  );
  
  // Brief border highlight
  trustCardBorderOpacity.value = withSequence(
    withTiming(0.3, { duration: 100 }),
    withDelay(200, withTiming(0, { duration: 300 }))
  );
};
```

---

## Registration Form Interactions

### Email Validation Animation

#### Real-time Email Validation

```javascript
const useEmailValidation = () => {
  const emailInputScale = useSharedValue(1);
  const emailBorderColor = useSharedValue('#D1D5DB'); // Neutral-300
  const validationIconOpacity = useSharedValue(0);
  const validationIconScale = useSharedValue(0);
  const loadingSpinnerRotation = useSharedValue(0);
  const loadingSpinnerOpacity = useSharedValue(0);

  const animateEmailValidation = (validationState) => {
    'worklet';
    
    switch (validationState) {
      case 'checking':
        // Show loading spinner
        loadingSpinnerOpacity.value = withTiming(1, { duration: 200 });
        loadingSpinnerRotation.value = withRepeat(
          withTiming(360, { duration: 1000, easing: Easing.linear }),
          -1, // Infinite
          false
        );
        emailBorderColor.value = '#F97316'; // Primary color during checking
        break;
        
      case 'valid':
        // Hide spinner, show success checkmark
        loadingSpinnerOpacity.value = withTiming(0, { duration: 200 });
        emailBorderColor.value = '#10B981'; // Success green
        validationIconOpacity.value = withTiming(1, { duration: 300 });
        validationIconScale.value = withSpring(1, {
          damping: 10,
          stiffness: 200,
        });
        break;
        
      case 'invalid':
        // Hide spinner, show error state
        loadingSpinnerOpacity.value = withTiming(0, { duration: 200 });
        emailBorderColor.value = '#EF4444'; // Error red
        // Gentle shake animation
        emailInputScale.value = withSequence(
          withTiming(1.02, { duration: 50 }),
          withTiming(0.98, { duration: 50 }),
          withTiming(1.02, { duration: 50 }),
          withTiming(1, { duration: 50 })
        );
        break;
        
      case 'exists':
        // Email already registered
        loadingSpinnerOpacity.value = withTiming(0, { duration: 200 });
        emailBorderColor.value = '#F59E0B'; // Warning orange
        break;
    }
  };

  return {
    emailInputScale,
    emailBorderColor,
    validationIconOpacity,
    validationIconScale,
    loadingSpinnerRotation,
    loadingSpinnerOpacity,
    animateEmailValidation,
  };
};
```

### Password Strength Indicator

#### Dynamic Strength Visualization

```javascript
const usePasswordStrengthAnimation = () => {
  const strengthBarWidth = useSharedValue(0);
  const strengthBarColor = useSharedValue('#EF4444'); // Start with red
  const requirementCheckmarks = useSharedValue([0, 0, 0, 0]); // 4 requirements
  const strengthTextOpacity = useSharedValue(0);
  const strengthIconBounce = useSharedValue(1);

  const animatePasswordStrength = (strength, requirements) => {
    'worklet';
    
    // Update strength bar
    const strengthColors = {
      0: '#EF4444',  // Red - weak
      25: '#F59E0B', // Orange - fair  
      50: '#EAB308', // Yellow - good
      75: '#84CC16', // Light green - strong
      100: '#10B981' // Green - excellent
    };
    
    strengthBarWidth.value = withTiming(strength, {
      duration: 300,
      easing: Easing.out(Easing.cubic),
    });
    
    // Smooth color transition
    const colorKey = Math.floor(strength / 25) * 25;
    strengthBarColor.value = strengthColors[colorKey];
    
    // Animate requirement checkmarks
    requirements.forEach((met, index) => {
      if (met && requirementCheckmarks.value[index] === 0) {
        // New requirement met - celebratory animation
        requirementCheckmarks.value[index] = withSpring(1, {
          damping: 8,
          stiffness: 150,
        });
      } else if (!met && requirementCheckmarks.value[index] === 1) {
        // Requirement no longer met
        requirementCheckmarks.value[index] = withTiming(0, { duration: 200 });
      }
    });
    
    // Strength text feedback
    if (strength >= 75) {
      strengthTextOpacity.value = withTiming(1, { duration: 200 });
      strengthIconBounce.value = withSequence(
        withTiming(1.2, { duration: 100 }),
        withTiming(1, { duration: 100 })
      );
    } else {
      strengthTextOpacity.value = withTiming(0.7, { duration: 200 });
    }
  };

  const getStrengthMessage = (strength) => {
    if (strength < 25) return "Add more characters and variety";
    if (strength < 50) return "Add numbers or symbols";
    if (strength < 75) return "Good password strength";
    return "Excellent password!";
  };

  return {
    strengthBarWidth,
    strengthBarColor,
    requirementCheckmarks,
    strengthTextOpacity,
    strengthIconBounce,
    animatePasswordStrength,
    getStrengthMessage,
  };
};
```

### Form Field Focus Management

#### Smart Focus Flow

```javascript
const useRegistrationFormFocus = () => {
  const emailFocusScale = useSharedValue(1);
  const passwordFocusScale = useSharedValue(1);
  const confirmFocusScale = useSharedValue(1);
  const activeFieldBorderWidth = useSharedValue(1);
  const activeFieldShadow = useSharedValue(0);

  const animateFieldFocus = (fieldName, focused) => {
    'worklet';
    
    const scaleMap = {
      email: emailFocusScale,
      password: passwordFocusScale,
      confirmPassword: confirmFocusScale,
    };
    
    const targetScale = scaleMap[fieldName];
    if (!targetScale) return;
    
    if (focused) {
      // Field focused
      targetScale.value = withSpring(1.02, {
        damping: 15,
        stiffness: 200,
      });
      
      activeFieldBorderWidth.value = withTiming(2, { duration: 200 });
      activeFieldShadow.value = withTiming(8, { duration: 200 });
    } else {
      // Field blurred
      targetScale.value = withSpring(1, {
        damping: 15,
        stiffness: 200,
      });
      
      activeFieldBorderWidth.value = withTiming(1, { duration: 200 });
      activeFieldShadow.value = withTiming(0, { duration: 200 });
    }
  };

  const animateFieldValidation = (fieldName, isValid) => {
    'worklet';
    
    if (isValid) {
      // Success pulse
      const targetScale = {
        email: emailFocusScale,
        password: passwordFocusScale,
        confirmPassword: confirmFocusScale,
      }[fieldName];
      
      if (targetScale) {
        targetScale.value = withSequence(
          withTiming(1.05, { duration: 150 }),
          withTiming(1, { duration: 150 })
        );
      }
    }
  };

  return {
    emailFocusScale,
    passwordFocusScale,
    confirmFocusScale,
    activeFieldBorderWidth,
    activeFieldShadow,
    animateFieldFocus,
    animateFieldValidation,
  };
};
```

### Form Submission Animation

#### Registration Button States

```javascript
const useRegistrationSubmission = () => {
  const submitButtonScale = useSharedValue(1);
  const submitButtonOpacity = useSharedValue(1);
  const loadingSpinnerOpacity = useSharedValue(0);
  const loadingSpinnerRotation = useSharedValue(0);
  const successIconScale = useSharedValue(0);
  const successIconOpacity = useSharedValue(0);
  const formOpacity = useSharedValue(1);

  const animateSubmissionStart = () => {
    'worklet';
    
    // Button pressed state
    submitButtonScale.value = withTiming(0.98, { duration: 100 });
    
    // Show loading spinner
    loadingSpinnerOpacity.value = withTiming(1, { duration: 200 });
    loadingSpinnerRotation.value = withRepeat(
      withTiming(360, { 
        duration: 1000, 
        easing: Easing.linear 
      }),
      -1, // Infinite
      false
    );
    
    // Reduce button text opacity
    submitButtonOpacity.value = withTiming(0.7, { duration: 200 });
  };

  const animateSubmissionSuccess = () => {
    'worklet';
    
    // Hide loading spinner
    loadingSpinnerOpacity.value = withTiming(0, { duration: 200 });
    
    // Show success checkmark
    successIconOpacity.value = withTiming(1, { duration: 300 });
    successIconScale.value = withSpring(1, {
      damping: 8,
      stiffness: 200,
    });
    
    // Button success state
    submitButtonScale.value = withSpring(1, {
      damping: 10,
      stiffness: 150,
    });
    
    // Brief success celebration
    runOnJS(HapticFeedback.trigger)('notificationSuccess');
    
    // Transition to next screen after celebration
    runOnJS(setTimeout)(() => {
      transitionToNextScreen();
    }, 1500);
  };

  const animateSubmissionError = (errorMessage) => {
    'worklet';
    
    // Hide loading spinner
    loadingSpinnerOpacity.value = withTiming(0, { duration: 200 });
    
    // Reset button state
    submitButtonScale.value = withSpring(1, {
      damping: 12,
      stiffness: 200,
    });
    
    submitButtonOpacity.value = withTiming(1, { duration: 200 });
    
    // Shake animation for error
    submitButtonScale.value = withSequence(
      withTiming(1.02, { duration: 50 }),
      withTiming(0.98, { duration: 50 }),
      withTiming(1.02, { duration: 50 }),
      withTiming(1, { duration: 50 })
    );
    
    // Error haptic feedback
    runOnJS(HapticFeedback.trigger)('notificationError');
    
    // Announce error to screen readers
    runOnJS(AccessibilityInfo.announceForAccessibility)(errorMessage);
  };

  return {
    submitButtonScale,
    submitButtonOpacity,
    loadingSpinnerOpacity,
    loadingSpinnerRotation,
    successIconScale,
    successIconOpacity,
    formOpacity,
    animateSubmissionStart,
    animateSubmissionSuccess,
    animateSubmissionError,
  };
};
```

### Sign In / Sign Up Toggle

#### Mode Switch Animation

```javascript
const useAuthModeToggle = () => {
  const formContentOpacity = useSharedValue(1);
  const formContentTranslateY = useSharedValue(0);
  const toggleButtonScale = useSharedValue(1);
  const headlineOpacity = useSharedValue(1);

  const animateModeSwitch = (newMode) => {
    'worklet';
    
    // Fade out current form
    formContentOpacity.value = withTiming(0, { duration: 200 });
    formContentTranslateY.value = withTiming(-20, { duration: 200 });
    headlineOpacity.value = withTiming(0, { duration: 200 });
    
    // Toggle button feedback
    toggleButtonScale.value = withSequence(
      withTiming(0.95, { duration: 100 }),
      withTiming(1, { duration: 100 })
    );
    
    // After fade out, update content and fade in
    runOnJS(setTimeout)(() => {
      updateFormMode(newMode);
      
      // Fade in new form
      formContentTranslateY.value = 20;
      formContentOpacity.value = withTiming(1, { duration: 300 });
      formContentTranslateY.value = withTiming(0, { duration: 300 });
      headlineOpacity.value = withTiming(1, { duration: 300 });
    }, 250);
  };

  const updateFormMode = (mode) => {
    // This would update the form state to show sign in vs sign up fields
    setAuthMode(mode);
  };

  return {
    formContentOpacity,
    formContentTranslateY,
    toggleButtonScale,
    headlineOpacity,
    animateModeSwitch,
  };
};
```

### Email Verification Flow

#### Verification Sent Animation

```javascript
const useEmailVerificationAnimation = () => {
  const emailIconScale = useSharedValue(0);
  const emailIconOpacity = useSharedValue(0);
  const checkmarkScale = useSharedValue(0);
  const messageOpacity = useSharedValue(0);
  const buttonSlideY = useSharedValue(20);
  const buttonOpacity = useSharedValue(0);
  const resendTimerOpacity = useSharedValue(0);

  const animateVerificationSent = (emailAddress) => {
    'worklet';
    
    // Email icon entrance
    emailIconOpacity.value = withTiming(1, { duration: 300 });
    emailIconScale.value = withSpring(1, {
      damping: 10,
      stiffness: 150,
    });
    
    // Checkmark overlay after email icon
    runOnJS(setTimeout)(() => {
      checkmarkScale.value = withSpring(1, {
        damping: 8,
        stiffness: 200,
      });
    }, 400);
    
    // Message fade in
    messageOpacity.value = withDelay(600,
      withTiming(1, { duration: 400 })
    );
    
    // Buttons slide up
    buttonSlideY.value = withDelay(800,
      withTiming(0, { duration: 400 })
    );
    buttonOpacity.value = withDelay(800,
      withTiming(1, { duration: 400 })
    );
    
    // Success haptic feedback
    runOnJS(HapticFeedback.trigger)('notificationSuccess');
    
    // Announce to screen readers
    runOnJS(AccessibilityInfo.announceForAccessibility)(
      `Verification email sent to ${emailAddress}. Check your inbox and click the link to verify your account.`
    );
  };

  const animateResendCooldown = (seconds) => {
    'worklet';
    
    resendTimerOpacity.value = withTiming(1, { duration: 200 });
    
    // This would be managed by a timer countdown
    runOnJS(startResendCountdown)(seconds);
  };

  const startResendCountdown = (seconds) => {
    // Implementation for countdown timer
    let remaining = seconds;
    const timer = setInterval(() => {
      remaining--;
      if (remaining <= 0) {
        clearInterval(timer);
        resendTimerOpacity.value = withTiming(0, { duration: 200 });
      }
    }, 1000);
  };

  return {
    emailIconScale,
    emailIconOpacity,
    checkmarkScale,
    messageOpacity,
    buttonSlideY,
    buttonOpacity,
    resendTimerOpacity,
    animateVerificationSent,
    animateResendCooldown,
  };
};
```

---

## Step Navigation System

### Progress Indicator Animation

#### Step Progress Animation

```javascript
const progressSteps = useSharedValue([0, 0, 0]); // 3 steps
const progressBarWidth = useSharedValue(0);
const currentStepScale = useSharedValue(1);

const updateProgressStep = (currentStep, totalSteps) => {
  'worklet';
  
  // Update progress bar
  const progressPercent = (currentStep - 1) / (totalSteps - 1);
  progressBarWidth.value = withTiming(progressPercent * 100, {
    duration: 400,
    easing: Easing.out(Easing.cubic),
  });
  
  // Update individual step indicators
  progressSteps.value.forEach((_, index) => {
    if (index < currentStep) {
      progressSteps.value[index] = withTiming(1, {
        duration: 300,
        easing: Easing.out(Easing.cubic),
      });
    } else {
      progressSteps.value[index] = withTiming(0.3, {
        duration: 300,
        easing: Easing.out(Easing.cubic),
      });
    }
  });
  
  // Current step emphasis
  if (currentStep <= totalSteps) {
    currentStepScale.value = withSequence(
      withTiming(1.2, { duration: 200 }),
      withTiming(1, { duration: 200 })
    );
  }
};
```

### "How It Works" Demonstration

#### Interactive Feature Preview

```javascript
const mockUIScale = useSharedValue(0.9);
const mockUIOpacity = useSharedValue(0);
const interactiveElements = useSharedValue([]);

const animateFeatureDemo = () => {
  // Mock UI entrance
  mockUIOpacity.value = withTiming(1, {
    duration: 500,
    easing: Easing.out(Easing.cubic),
  });
  
  mockUIScale.value = withSpring(1, {
    damping: 12,
    stiffness: 100,
  });
  
  // Highlight interactive elements in sequence
  const highlightSequence = [
    'scenario-selection',
    'conversation-start',
    'ai-response',
    'feedback-display'
  ];
  
  highlightSequence.forEach((elementId, index) => {
    interactiveElements.value[elementId] = withDelay(
      1000 + (index * 800),
      withSequence(
        withTiming(1, { duration: 300 }),
        withTiming(0.7, { duration: 500 }),
        withTiming(1, { duration: 300 })
      )
    );
  });
};
```

### Navigation Button Interactions

#### Next/Back Button Animation

```javascript
const nextButtonScale = useSharedValue(1);
const nextButtonArrowTranslateX = useSharedValue(0);
const backButtonOpacity = useSharedValue(0);

const handleNextButtonPress = () => {
  // Button press feedback
  nextButtonScale.value = withSequence(
    withTiming(0.95, { duration: 100 }),
    withTiming(1, { duration: 150 })
  );
  
  // Arrow animation for direction indication
  nextButtonArrowTranslateX.value = withSequence(
    withTiming(5, { duration: 150 }),
    withTiming(0, { duration: 150 })
  );
  
  // Trigger screen transition
  runOnJS(transitionToNextScreen)();
};

const showBackButton = () => {
  backButtonOpacity.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
};
```

---

## Permission Request Interactions

### Notification Permission Flow

#### Permission Dialog Animation

```javascript
const permissionModalScale = useSharedValue(0.9);
const permissionModalOpacity = useSharedValue(0);
const permissionOverlayOpacity = useSharedValue(0);
const notificationIconBounce = useSharedValue(1);

const showPermissionRequest = () => {
  // Modal entrance
  permissionOverlayOpacity.value = withTiming(0.5, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  permissionModalOpacity.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
  
  permissionModalScale.value = withSpring(1, {
    damping: 15,
    stiffness: 150,
  });
  
  // Icon attention animation
  notificationIconBounce.value = withRepeat(
    withSequence(
      withTiming(1.1, { duration: 600 }),
      withTiming(1, { duration: 600 })
    ),
    3, // Repeat 3 times
    false
  );
};

const handlePermissionResponse = (granted) => {
  if (granted) {
    // Success animation
    showPermissionSuccess();
  } else {
    // Gentle dismissal without penalty
    dismissPermissionModal();
  }
};

const showPermissionSuccess = () => {
  const successScale = useSharedValue(0);
  const successOpacity = useSharedValue(0);
  
  successScale.value = withSpring(1, {
    damping: 10,
    stiffness: 200,
  });
  
  successOpacity.value = withTiming(1, {
    duration: 300,
  });
  
  // Auto-dismiss after celebration
  runOnJS(setTimeout)(() => {
    dismissPermissionModal();
  }, 1500);
};
```

### Age Verification Interaction

#### Age Input Animation

```javascript
const ageInputFocus = useSharedValue(0);
const ageInputBorderColor = useSharedValue('#E5E7EB');
const validationMessageOpacity = useSharedValue(0);

const handleAgeInputFocus = () => {
  ageInputFocus.value = withSpring(1, {
    damping: 15,
    stiffness: 200,
  });
  
  ageInputBorderColor.value = '#F97316'; // Primary color
};

const handleAgeValidation = (isValid, age) => {
  if (isValid) {
    // Success state
    ageInputBorderColor.value = '#10B981'; // Success green
    showValidationSuccess();
  } else {
    // Error state with gentle shake
    const shakeX = useSharedValue(0);
    
    shakeX.value = withSequence(
      withTiming(-5, { duration: 50 }),
      withTiming(5, { duration: 50 }),
      withTiming(-5, { duration: 50 }),
      withTiming(0, { duration: 50 })
    );
    
    ageInputBorderColor.value = '#EF4444'; // Error red
    showValidationError();
  }
};

const showValidationError = () => {
  validationMessageOpacity.value = withTiming(1, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
};
```

---

## Completion Celebrations

### Onboarding Success Animation

#### Success Celebration Sequence

```javascript
const celebrationScale = useSharedValue(0);
const celebrationOpacity = useSharedValue(0);
const confettiOpacity = useSharedValue(0);
const successMessageTranslateY = useSharedValue(20);
const actionButtonScale = useSharedValue(0);

const triggerCompletionCelebration = () => {
  'worklet';
  
  // Main celebration element
  celebrationOpacity.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
  
  celebrationScale.value = withSpring(1, {
    damping: 8,
    stiffness: 150,
  });
  
  // Confetti effect (if appropriate)
  confettiOpacity.value = withSequence(
    withTiming(1, { duration: 200 }),
    withDelay(3000, withTiming(0, { duration: 800 }))
  );
  
  // Success message slide up
  successMessageTranslateY.value = withDelay(200,
    withTiming(0, {
      duration: 400,
      easing: Easing.out(Easing.back(1.1)),
    })
  );
  
  // Action button dramatic entrance
  actionButtonScale.value = withDelay(600,
    withSpring(1, {
      damping: 10,
      stiffness: 200,
    })
  );
  
  // Trigger haptic feedback
  runOnJS(HapticFeedback.trigger)('notificationSuccess');
};
```

### Achievement Unlock Animation

#### First Badge Earning

```javascript
const badgeScale = useSharedValue(0);
const badgeRotation = useSharedValue(-15);
const badgeGlow = useSharedValue(0);
const achievementTextOpacity = useSharedValue(0);

const unlockFirstAchievement = () => {
  // Badge dramatic entrance
  badgeScale.value = withSpring(1, {
    damping: 8,
    stiffness: 100,
  });
  
  badgeRotation.value = withSpring(0, {
    damping: 12,
    stiffness: 150,
  });
  
  // Glowing effect
  badgeGlow.value = withRepeat(
    withSequence(
      withTiming(1, { duration: 400 }),
      withTiming(0.6, { duration: 400 })
    ),
    4, // Repeat 4 times
    false
  );
  
  // Achievement text fade in
  achievementTextOpacity.value = withDelay(300,
    withTiming(1, {
      duration: 400,
      easing: Easing.out(Easing.cubic),
    })
  );
};
```

---

## Micro-interactions & Feedback

### Button Interaction States

#### Primary Button Interactions

```javascript
const primaryButtonScale = useSharedValue(1);
const primaryButtonOpacity = useSharedValue(1);
const primaryButtonShadow = useSharedValue(4);

const handlePrimaryButtonInteraction = {
  onPressIn: () => {
    primaryButtonScale.value = withTiming(0.98, { duration: 100 });
    primaryButtonShadow.value = withTiming(2, { duration: 100 });
    HapticFeedback.trigger('impactLight');
  },
  
  onPressOut: () => {
    primaryButtonScale.value = withTiming(1, { duration: 150 });
    primaryButtonShadow.value = withTiming(4, { duration: 150 });
  },
  
  onPress: () => {
    // Additional press animation if needed
    primaryButtonOpacity.value = withSequence(
      withTiming(0.8, { duration: 50 }),
      withTiming(1, { duration: 100 })
    );
  },
};
```

### Skip and Secondary Actions

#### Skip Link Interactions

```javascript
const skipLinkOpacity = useSharedValue(0.7);
const skipLinkScale = useSharedValue(1);

const handleSkipInteraction = {
  onPressIn: () => {
    skipLinkScale.value = withTiming(0.95, { duration: 100 });
    skipLinkOpacity.value = withTiming(1, { duration: 100 });
  },
  
  onPressOut: () => {
    skipLinkScale.value = withTiming(1, { duration: 150 });
    skipLinkOpacity.value = withTiming(0.7, { duration: 150 });
  },
};
```

### Loading States

#### Content Loading Animation

```javascript
const skeletonOpacity = useSharedValue(0.3);
const loadingSpinnerRotation = useSharedValue(0);

const animateContentLoading = () => {
  // Skeleton shimmer
  skeletonOpacity.value = withRepeat(
    withSequence(
      withTiming(0.7, { duration: 1000 }),
      withTiming(0.3, { duration: 1000 })
    ),
    -1, // Infinite
    false
  );
  
  // Loading spinner
  loadingSpinnerRotation.value = withRepeat(
    withTiming(360, {
      duration: 1000,
      easing: Easing.linear,
    }),
    -1, // Infinite
    false
  );
};
```

---

## Platform-Specific Adaptations

### iOS Specific Interactions

#### Native iOS Animation Feel

```javascript
const iOSSpringConfig = {
  damping: 20,
  stiffness: 300,
  mass: 0.8,
};

const iOSTransition = () => {
  return withSpring(targetValue, iOSSpringConfig);
};

// iOS-style modal presentation
const presentModal = () => {
  modalTranslateY.value = withSpring(0, iOSSpringConfig);
  modalOpacity.value = withTiming(1, { duration: 300 });
};
```

#### iOS Haptic Integration

```javascript
import { HapticFeedback } from 'react-native-haptic-feedback';

const onboardingHaptics = {
  stepComplete: () => HapticFeedback.trigger('notificationSuccess'),
  buttonPress: () => HapticFeedback.trigger('impactLight'),
  error: () => HapticFeedback.trigger('notificationWarning'),
  celebration: () => HapticFeedback.trigger('notificationSuccess'),
};
```

### Android Specific Interactions

#### Material Design Motion

```javascript
const materialEasing = {
  standardEasing: Easing.bezier(0.4, 0, 0.2, 1),
  decelerateEasing: Easing.out(Easing.cubic),
  accelerateEasing: Easing.in(Easing.cubic),
};

const materialTransition = () => {
  return withTiming(targetValue, {
    duration: 300,
    easing: materialEasing.standardEasing,
  });
};
```

#### Android Ripple Effects

```javascript
const rippleScale = useSharedValue(0);
const rippleOpacity = useSharedValue(0);

const triggerRippleEffect = (touchPoint) => {
  rippleScale.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
  
  rippleOpacity.value = withSequence(
    withTiming(0.3, { duration: 100 }),
    withTiming(0, { duration: 200 })
  );
};
```

## Performance Optimization

### Animation Performance Management

```javascript
const useOnboardingAnimationManager = () => {
  const activeAnimations = useRef(new Set());
  const [reducedMotion, setReducedMotion] = useState(false);
  
  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setReducedMotion);
  }, []);
  
  const registerAnimation = (animationRef) => {
    activeAnimations.current.add(animationRef);
  };
  
  const cleanupAnimations = () => {
    activeAnimations.current.forEach(animation => {
      if (animation && animation.stop) {
        animation.stop();
      }
    });
    activeAnimations.current.clear();
  };
  
  const getAnimationConfig = (config) => {
    if (reducedMotion) {
      return { ...config, duration: 0 };
    }
    return config;
  };
  
  return { registerAnimation, cleanupAnimations, getAnimationConfig };
};
```

### Memory Management

```javascript
const useOnboardingCleanup = () => {
  useEffect(() => {
    return () => {
      // Cleanup all animations on unmount
      cancelAllAnimations();
      clearAllTimeouts();
    };
  }, []);
};
```

## Related Documentation

- **[Screen States](./screen-states.md)** - Visual specifications for all animated states
- **[User Journey](./user-journey.md)** - Context for when interactions occur
- **[Accessibility](./accessibility.md)** - Accessible interaction patterns
- **[Implementation](./implementation.md)** - Technical implementation details
- **[Design System Animations](../../design-system/tokens/animations.md)** - Base animation tokens

## Implementation Guidelines

### React Native Reanimated 3 Setup

```javascript
// Core animation dependencies
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  withSequence,
  withDelay,
  withRepeat,
  runOnJS,
  Easing,
} from 'react-native-reanimated';
```

### Performance Monitoring

```javascript
const useAnimationPerformance = () => {
  const frameDrops = useRef(0);
  
  const trackPerformance = () => {
    // Monitor animation performance
    if (performance.now() - lastFrameTime > 16.67) {
      frameDrops.current++;
    }
  };
  
  return { frameDrops: frameDrops.current };
};
```

## Last Updated
- **Version 1.0.0**: Complete interaction and animation specifications for onboarding
- **Focus**: Trust-building animations with emotional engagement
- **Next**: Technical implementation with platform-specific optimizations