# Feedback Feature - Interactions

---
title: Feedback Feature Interactions and Animations
description: Complete interaction patterns, animations, and micro-interactions for feedback system
feature: feedback
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
  - React Native Reanimated
  - design system animation tokens
status: approved
---

## Interactions Overview

The feedback feature uses choreographed animations and interactions to create emotional engagement, celebrate user progress, and guide attention to key learning moments. All animations follow the design system's motion principles for consistency and performance.

## Table of Contents

1. [Entry Animations](#entry-animations)
2. [Score Reveal Choreography](#score-reveal-choreography)
3. [Content Interactions](#content-interactions)
4. [Gesture Patterns](#gesture-patterns)
5. [Micro-interactions](#micro-interactions)
6. [Haptic Feedback](#haptic-feedback)
7. [Performance Specifications](#performance-specifications)

---

## Entry Animations

### Conversation to Feedback Transition

#### Animation Sequence (Total: 800ms)

**Phase 1: Conversation Fade-Out (0-300ms)**
```javascript
// React Native Reanimated 3 Specification
const conversationFade = useSharedValue(1);
const backdropBlur = useSharedValue(0);

const fadeOutConversation = () => {
  conversationFade.value = withTiming(0, {
    duration: 300,
    easing: Easing.bezier(0.4, 0, 0.6, 1), // Material ease-in-out
  });
  
  backdropBlur.value = withTiming(4, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
};
```

**Phase 2: Loading Animation Entrance (300-500ms)**
```javascript
const loadingScale = useSharedValue(0);
const loadingOpacity = useSharedValue(0);

const showLoadingAnimation = () => {
  loadingScale.value = withSpring(1, {
    damping: 12,
    stiffness: 100,
    mass: 0.8,
  });
  
  loadingOpacity.value = withTiming(1, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
};
```

**Phase 3: Content Preparation (500-800ms)**
```javascript
const contentTranslateY = useSharedValue(20);
const contentOpacity = useSharedValue(0);

const prepareContent = () => {
  contentTranslateY.value = withTiming(0, {
    duration: 300,
    easing: Easing.out(Easing.back(1.1)),
  });
  
  contentOpacity.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
};
```

#### Visual Effects Specifications

**Backdrop Treatment**:
- **Blur Effect**: Conversation interface blurred with 4px radius
- **Overlay**: Semi-transparent white overlay (0.95 alpha)
- **Color Transition**: Subtle shift toward feedback theme colors

**Loading Animation**:
- **Primary Element**: Circular progress ring with smooth rotation
- **Secondary Element**: Pulsing analysis icon in center
- **Timing**: 1.5s rotation cycle with spring easing
- **Performance**: Hardware accelerated with `useNativeDriver: true`

---

## Score Reveal Choreography

### Dramatic Score Animation Sequence

The score reveal is the emotional centerpiece of the feedback experience, designed to create anticipation and celebration.

#### Animation Timeline (Total: 3200ms)

**Phase 1: Anticipation Build (0-800ms)**
```javascript
const scoreContainerScale = useSharedValue(0.8);
const anticipationPulse = useSharedValue(1);

const buildAnticipation = () => {
  scoreContainerScale.value = withSpring(1, {
    damping: 10,
    stiffness: 80,
  });
  
  anticipationPulse.value = withRepeat(
    withTiming(1.05, {
      duration: 600,
      easing: Easing.inOut(Easing.sine),
    }),
    2,
    true
  );
};
```

**Phase 2: Score Counter Animation (800-2800ms)**
```javascript
const scoreValue = useSharedValue(0);
const finalScore = 78; // Example score from API

const animateScore = () => {
  scoreValue.value = withTiming(finalScore, {
    duration: 2000,
    easing: Easing.bezier(0.4, 0, 0.2, 1), // Custom ease-out
  });
};

// Custom hook for score counter display
const useAnimatedScore = () => {
  return useDerivedValue(() => {
    return Math.round(scoreValue.value);
  });
};
```

**Phase 3: Score Context & Celebration (2800-3200ms)**
```javascript
const contextOpacity = useSharedValue(0);
const celebrationScale = useSharedValue(0);

const showScoreContext = () => {
  contextOpacity.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
  
  // Celebration only for high scores (80+)
  if (finalScore >= 80) {
    celebrationScale.value = withSpring(1, {
      damping: 8,
      stiffness: 100,
    });
  }
};
```

#### Score-Based Visual Variations

**High Performance Scores (90-100)**:
```javascript
const celebrationParticles = useSharedValue(0);
const successColor = useSharedValue(0);

const triggerCelebration = () => {
  // Particle animation
  celebrationParticles.value = withSequence(
    withTiming(1, { duration: 500 }),
    withDelay(2000, withTiming(0, { duration: 1000 }))
  );
  
  // Color pulse effect
  successColor.value = withRepeat(
    withTiming(1, { duration: 300 }),
    4,
    true
  );
};
```

**Learning Opportunity Scores (Below 60)**:
```javascript
const encouragementGlow = useSharedValue(0);
const supportiveScale = useSharedValue(1);

const showEncouragement = () => {
  encouragementGlow.value = withRepeat(
    withTiming(1, {
      duration: 800,
      easing: Easing.inOut(Easing.sine),
    }),
    3,
    true
  );
  
  supportiveScale.value = withSpring(1.05, {
    damping: 12,
    stiffness: 100,
  });
};
```

#### Progress Ring Animation

**Circular Progress Specification**:
```javascript
const progressValue = useSharedValue(0);
const ringRotation = useSharedValue(0);

const animateProgressRing = () => {
  progressValue.value = withTiming(finalScore / 100, {
    duration: 2000,
    easing: Easing.out(Easing.cubic),
  });
  
  ringRotation.value = withTiming(360 * (finalScore / 100), {
    duration: 2000,
    easing: Easing.out(Easing.cubic),
  });
};
```

---

## Content Interactions

### Feedback Cards Animation System

#### Staggered Card Entrance

```javascript
const cardAnimations = useSharedValue([]);

const animateCardsIn = (cardCount) => {
  cardCount.forEach((_, index) => {
    cardAnimations.value[index] = {
      translateY: withDelay(
        index * 100, // 100ms stagger
        withSpring(0, {
          damping: 12,
          stiffness: 80,
        })
      ),
      opacity: withDelay(
        index * 100,
        withTiming(1, {
          duration: 300,
          easing: Easing.out(Easing.cubic),
        })
      ),
    };
  });
};
```

#### Card Interaction States

**Hover State (Desktop/Tablet)**:
```javascript
const cardHover = useSharedValue(0);

const handleCardHover = (isHovered) => {
  cardHover.value = withSpring(isHovered ? 1 : 0, {
    damping: 15,
    stiffness: 200,
  });
};

// Animated style for hover effect
const cardHoverStyle = useAnimatedStyle(() => ({
  transform: [
    { scale: interpolate(cardHover.value, [0, 1], [1, 1.02]) },
    { translateY: interpolate(cardHover.value, [0, 1], [0, -2]) },
  ],
  shadowOffset: {
    width: 0,
    height: interpolate(cardHover.value, [0, 1], [2, 8]),
  },
  shadowOpacity: interpolate(cardHover.value, [0, 1], [0.1, 0.15]),
}));
```

**Press State (All Platforms)**:
```javascript
const cardPress = useSharedValue(0);

const handleCardPress = () => {
  cardPress.value = withSequence(
    withTiming(1, { duration: 100 }),
    withTiming(0, { duration: 150 })
  );
};

const cardPressStyle = useAnimatedStyle(() => ({
  transform: [
    { scale: interpolate(cardPress.value, [0, 1], [1, 0.98]) },
  ],
}));
```

#### Expandable Card Interactions

**Card Expansion Animation**:
```javascript
const cardHeight = useSharedValue(80); // Initial collapsed height
const expandedHeight = 200; // Full content height

const expandCard = (shouldExpand) => {
  cardHeight.value = withSpring(
    shouldExpand ? expandedHeight : 80,
    {
      damping: 20,
      stiffness: 100,
    }
  );
};
```

**Content Fade-In on Expansion**:
```javascript
const expandedContentOpacity = useSharedValue(0);

const showExpandedContent = () => {
  expandedContentOpacity.value = withDelay(
    200, // Wait for height animation
    withTiming(1, {
      duration: 300,
      easing: Easing.out(Easing.cubic),
    })
  );
};
```

---

## Gesture Patterns

### Swipe Interactions

#### Horizontal Card Swiping
```javascript
const panGestureHandler = useAnimatedGestureHandler({
  onStart: (_, context) => {
    context.startX = translateX.value;
  },
  
  onActive: (event, context) => {
    translateX.value = context.startX + event.translationX;
  },
  
  onEnd: (event) => {
    const shouldSwipeNext = event.velocityX < -500 || event.translationX < -100;
    const shouldSwipePrev = event.velocityX > 500 || event.translationX > 100;
    
    if (shouldSwipeNext && hasNextCard) {
      translateX.value = withSpring(-cardWidth);
      runOnJS(navigateToNextCard)();
    } else if (shouldSwipePrev && hasPrevCard) {
      translateX.value = withSpring(cardWidth);
      runOnJS(navigateToPrevCard)();
    } else {
      translateX.value = withSpring(0);
    }
  },
});
```

#### Pull-to-Refresh for Updated Feedback
```javascript
const pullGestureHandler = useAnimatedGestureHandler({
  onActive: (event) => {
    if (event.translationY > 0 && scrollY.value === 0) {
      refreshTranslateY.value = Math.min(event.translationY / 2, 60);
    }
  },
  
  onEnd: (event) => {
    if (refreshTranslateY.value > 40) {
      refreshTranslateY.value = withTiming(40);
      runOnJS(refreshFeedback)();
    } else {
      refreshTranslateY.value = withTiming(0);
    }
  },
});
```

### Touch Feedback Patterns

#### Button Press Interactions
```javascript
const buttonScale = useSharedValue(1);
const buttonOpacity = useSharedValue(1);

const handleButtonPress = () => {
  buttonScale.value = withSequence(
    withTiming(0.96, { duration: 100 }),
    withTiming(1, { duration: 150 })
  );
  
  buttonOpacity.value = withSequence(
    withTiming(0.8, { duration: 100 }),
    withTiming(1, { duration: 150 })
  );
};
```

---

## Micro-interactions

### Loading State Micro-animations

#### Skeleton Loading for Content
```javascript
const skeletonOpacity = useSharedValue(0.3);

const animateSkeleton = () => {
  skeletonOpacity.value = withRepeat(
    withTiming(1, {
      duration: 1000,
      easing: Easing.inOut(Easing.sine),
    }),
    -1, // Infinite repeat
    true // Reverse
  );
};
```

#### Pulse Animation for Interactive Elements
```javascript
const pulseScale = useSharedValue(1);

const startPulse = () => {
  pulseScale.value = withRepeat(
    withSequence(
      withTiming(1.05, { duration: 600 }),
      withTiming(1, { duration: 600 })
    ),
    -1, // Infinite
    false
  );
};
```

### Success State Celebrations

#### Achievement Unlock Animation
```javascript
const achievementScale = useSharedValue(0);
const achievementRotation = useSharedValue(-15);

const showAchievement = () => {
  achievementScale.value = withSpring(1, {
    damping: 8,
    stiffness: 100,
  });
  
  achievementRotation.value = withSpring(0, {
    damping: 12,
    stiffness: 200,
  });
};
```

#### Progress Bar Fill Animation
```javascript
const progressWidth = useSharedValue(0);
const previousProgress = 0.6; // Previous skill level
const newProgress = 0.75; // New skill level after feedback

const animateProgress = () => {
  progressWidth.value = withSequence(
    withTiming(previousProgress, { duration: 500 }),
    withDelay(300, withTiming(newProgress, { duration: 800 }))
  );
};
```

---

## Haptic Feedback

### iOS Haptic Patterns

#### Score Reveal Haptics
```javascript
import { HapticFeedback } from 'react-native-haptic-feedback';

const triggerScoreHaptic = (score) => {
  if (score >= 90) {
    // Success notification for exceptional scores
    HapticFeedback.trigger('notificationSuccess');
  } else if (score >= 70) {
    // Light impact for good scores
    HapticFeedback.trigger('impactLight');
  } else if (score >= 50) {
    // Medium impact for learning scores
    HapticFeedback.trigger('impactMedium');
  } else {
    // Gentle selection for low scores (non-punishing)
    HapticFeedback.trigger('selection');
  }
};
```

#### Interaction Haptics
```javascript
const feedbackHaptics = {
  cardTap: () => HapticFeedback.trigger('selection'),
  buttonPress: () => HapticFeedback.trigger('impactLight'),
  achievementUnlock: () => HapticFeedback.trigger('notificationSuccess'),
  errorState: () => HapticFeedback.trigger('notificationWarning'),
  swipeAction: () => HapticFeedback.trigger('impactMedium'),
};
```

### Android Haptic Patterns

#### System Integration
```javascript
import { Vibration } from 'react-native';

const androidHaptics = {
  scoreReveal: (score) => {
    if (score >= 90) {
      Vibration.vibrate([0, 100, 50, 100]); // Celebration pattern
    } else if (score >= 70) {
      Vibration.vibrate(50); // Single success tap
    } else {
      Vibration.vibrate(30); // Gentle acknowledgment
    }
  },
  
  buttonPress: () => Vibration.vibrate(10),
  cardInteraction: () => Vibration.vibrate(20),
  achievement: () => Vibration.vibrate([0, 100, 100, 100]),
};
```

---

## Performance Specifications

### Animation Performance Requirements

#### Frame Rate Targets
- **Target FPS**: 60fps sustained throughout all animations
- **Minimum FPS**: 45fps on lower-end devices
- **Critical Animations**: Score reveal, card transitions, gesture responses

#### Memory Management
```javascript
// Proper cleanup of animation listeners
useEffect(() => {
  const listener = scoreValue.addListener(({ value }) => {
    // Update UI based on animated value
  });
  
  return () => {
    scoreValue.removeListener(listener);
  };
}, []);
```

#### Hardware Acceleration
```javascript
// Ensure native driver usage for performance
const animatedStyle = useAnimatedStyle(() => ({
  transform: [
    { translateX: translateX.value },
    { scale: scale.value },
  ],
  opacity: opacity.value,
}), []);

// Use native driver for gesture handling
const gestureHandler = useAnimatedGestureHandler({
  // Handler implementation
}, [], 'native'); // Enable native driver
```

### Battery Optimization

#### Efficient Animation Patterns
- **Reduce Over-Animation**: Limit simultaneous animations to 3-4 elements
- **Use SharedValue Wisely**: Batch updates to minimize re-renders
- **Implement Animation Pausing**: Pause animations when app goes to background

#### Reduced Motion Support
```javascript
import { AccessibilityInfo } from 'react-native';

const [reduceMotion, setReduceMotion] = useState(false);

useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
}, []);

const animationConfig = reduceMotion 
  ? { duration: 0 } 
  : { duration: 300, easing: Easing.ease };
```

---

## Platform-Specific Adaptations

### iOS Specific Interactions

#### Native Gesture Recognition
```javascript
// iOS-style swipe back gesture
const iosSwipeBack = useAnimatedGestureHandler({
  onActive: (event) => {
    if (event.translationX > 50 && event.x < 20) {
      // Trigger iOS-style back navigation
      runOnJS(navigateBack)();
    }
  },
});
```

#### iOS Animation Curves
```javascript
const iOSAnimations = {
  easeInOut: Easing.bezier(0.42, 0, 0.58, 1), // iOS standard
  spring: { damping: 15, stiffness: 300 }, // iOS spring feel
  modalPresent: Easing.out(Easing.back(1.1)), // iOS modal presentation
};
```

### Android Specific Interactions

#### Material Motion Patterns
```javascript
const materialAnimations = {
  standardEasing: Easing.bezier(0.4, 0, 0.2, 1),
  emphasizedEasing: Easing.bezier(0.2, 0, 0, 1),
  deceleratedEasing: Easing.out(Easing.cubic),
};
```

#### Android Back Button Handling
```javascript
import { BackHandler } from 'react-native';

useEffect(() => {
  const backAction = () => {
    if (feedbackVisible) {
      // Custom back animation for feedback
      animateFeedbackOut();
      return true; // Prevent default
    }
    return false;
  };

  const backHandler = BackHandler.addEventListener(
    'hardwareBackPress',
    backAction
  );

  return () => backHandler.remove();
}, [feedbackVisible]);
```

## Implementation Guidelines

### React Native Reanimated 3 Setup

#### Core Dependencies
```json
{
  "react-native-reanimated": "^3.6.0",
  "react-native-gesture-handler": "^2.14.0",
  "react-native-haptic-feedback": "^2.0.3"
}
```

#### Animation Context Setup
```javascript
import { ReanimatedProvider } from 'react-native-reanimated';

const FeedbackScreen = () => (
  <ReanimatedProvider>
    <FeedbackContent />
  </ReanimatedProvider>
);
```

### Performance Monitoring

#### Animation Performance Tracking
```javascript
const performanceMetrics = {
  animationStartTime: 0,
  frameDrops: 0,
  
  startTracking() {
    this.animationStartTime = performance.now();
  },
  
  endTracking() {
    const duration = performance.now() - this.animationStartTime;
    // Log metrics for analysis
    analytics.track('animation_performance', { duration });
  },
};
```

## Related Documentation

- **[Screen States](./screen-states.md)** - Visual specifications for all animated states
- **[User Journey](./user-journey.md)** - Context for when interactions occur
- **[Accessibility](./accessibility.md)** - Accessible interaction patterns
- **[Implementation](./implementation.md)** - Technical implementation details
- **[Design System Animations](../../design-system/tokens/animations.md)** - Base animation tokens

## Last Updated
- **Version 1.0.0**: Complete interaction and animation specifications
- **Focus**: Performance-optimized animations with platform-specific adaptations
- **Next**: Technical implementation with React Native Reanimated 3