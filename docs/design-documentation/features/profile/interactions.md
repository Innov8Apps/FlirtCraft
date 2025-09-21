# Profile Feature - Interactions

---
title: Profile Feature Interactions and Animations
description: Complete interaction patterns, form animations, and micro-interactions for profile system
feature: profile
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
  - form component animations
status: approved
---

## Interactions Overview

The profile feature uses thoughtful animations and interactions to guide users through personal data entry, preference customization, and progress review. All interactions prioritize user trust, data transparency, and seamless form completion.

## Table of Contents

1. [Profile Creation Flow Interactions](#profile-creation-flow-interactions)
2. [Form Field Interactions](#form-field-interactions)
3. [Preference Selection Animations](#preference-selection-animations)
4. [Progress Visualization Interactions](#progress-visualization-interactions)
5. [Privacy Control Interactions](#privacy-control-interactions)
6. [Micro-interactions & Feedback](#micro-interactions--feedback)

---

## Profile Creation Flow Interactions

### Multi-Step Form Navigation

#### Step Transition Animations

```javascript
// React Native Reanimated 3 Implementation
const stepTransition = useSharedValue(0);
const contentOpacity = useSharedValue(1);
const contentTranslateX = useSharedValue(0);

const navigateToNextStep = (nextStepIndex) => {
  'worklet';
  
  // Fade out current content
  contentOpacity.value = withTiming(0, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  // Slide content out
  contentTranslateX.value = withTiming(-50, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  // Update step indicator
  stepTransition.value = withTiming(nextStepIndex, {
    duration: 300,
    easing: Easing.inOut(Easing.cubic),
  });
  
  // Slide new content in
  runOnJS(updateStepContent)(nextStepIndex);
  
  contentTranslateX.value = withDelay(100, 
    withTiming(0, {
      duration: 300,
      easing: Easing.out(Easing.back(1.1)),
    })
  );
  
  contentOpacity.value = withDelay(150,
    withTiming(1, {
      duration: 250,
      easing: Easing.out(Easing.cubic),
    })
  );
};
```

#### Progress Indicator Animation

```javascript
const progressValue = useSharedValue(0);
const progressBarWidth = useSharedValue(0);

const updateProgress = (currentStep, totalSteps) => {
  const progress = currentStep / totalSteps;
  
  progressValue.value = withSpring(progress, {
    damping: 15,
    stiffness: 100,
  });
  
  progressBarWidth.value = withTiming(progress * 100, {
    duration: 400,
    easing: Easing.out(Easing.cubic),
  });
};

// Progress bar animated style
const progressBarStyle = useAnimatedStyle(() => ({
  width: `${progressBarWidth.value}%`,
  backgroundColor: interpolateColor(
    progressValue.value,
    [0, 0.5, 1],
    ['#FED7AA', '#F97316', '#15803D'] // Orange to green progression
  ),
}));
```

#### Form Validation Feedback

```javascript
const validationState = useSharedValue(0); // 0: neutral, 1: valid, -1: error
const fieldBorderColor = useSharedValue('#E5E7EB');
const validationScale = useSharedValue(1);

const showValidationFeedback = (isValid, hasError) => {
  if (hasError) {
    validationState.value = -1;
    fieldBorderColor.value = '#EF4444'; // Error red
    
    // Shake animation for errors
    validationScale.value = withSequence(
      withTiming(1.02, { duration: 100 }),
      withTiming(0.98, { duration: 100 }),
      withTiming(1, { duration: 100 })
    );
  } else if (isValid) {
    validationState.value = 1;
    fieldBorderColor.value = '#10B981'; // Success green
  } else {
    validationState.value = 0;
    fieldBorderColor.value = '#E5E7EB'; // Neutral gray
  }
};
```

---

## Form Field Interactions

### Input Field Focus States

#### Focus Animation Sequence

```javascript
const focusScale = useSharedValue(1);
const labelTranslateY = useSharedValue(0);
const labelScale = useSharedValue(1);

const handleFieldFocus = () => {
  // Field container subtle scale
  focusScale.value = withSpring(1.01, {
    damping: 20,
    stiffness: 300,
  });
  
  // Label animation (moves up and scales down)
  labelTranslateY.value = withTiming(-24, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  labelScale.value = withTiming(0.85, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
};

const handleFieldBlur = () => {
  focusScale.value = withSpring(1, {
    damping: 20,
    stiffness: 300,
  });
  
  // Only return label if field is empty
  if (!fieldValue) {
    labelTranslateY.value = withTiming(0, {
      duration: 200,
      easing: Easing.out(Easing.cubic),
    });
    
    labelScale.value = withTiming(1, {
      duration: 200,
      easing: Easing.out(Easing.cubic),
    });
  }
};
```

#### Real-time Validation Animation

```javascript
const validationOpacity = useSharedValue(0);
const validationTranslateY = useSharedValue(10);
const checkmarkScale = useSharedValue(0);

const showValidationMessage = (message, isError = false) => {
  // Fade in validation message
  validationOpacity.value = withTiming(1, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  validationTranslateY.value = withTiming(0, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  // Show checkmark for successful validation
  if (!isError) {
    checkmarkScale.value = withSpring(1, {
      damping: 10,
      stiffness: 200,
    });
  }
};

const hideValidationMessage = () => {
  validationOpacity.value = withTiming(0, {
    duration: 150,
    easing: Easing.in(Easing.cubic),
  });
  
  checkmarkScale.value = withTiming(0, {
    duration: 150,
  });
};
```

### Age Selection Interaction

#### Custom Age Picker Animation

```javascript
const pickerScale = useSharedValue(0.95);
const pickerOpacity = useSharedValue(0);
const selectedItemScale = useSharedValue(1);

const showAgePicker = () => {
  pickerOpacity.value = withTiming(1, {
    duration: 250,
    easing: Easing.out(Easing.cubic),
  });
  
  pickerScale.value = withSpring(1, {
    damping: 12,
    stiffness: 100,
  });
};

const highlightSelectedAge = () => {
  selectedItemScale.value = withSequence(
    withTiming(1.05, { duration: 100 }),
    withTiming(1, { duration: 100 })
  );
};
```

### Location Search Interaction

#### Type-ahead Search Animation

```javascript
const searchResultsHeight = useSharedValue(0);
const searchResultsOpacity = useSharedValue(0);
const loadingSpinnerRotation = useSharedValue(0);

const showSearchResults = (resultCount) => {
  const maxHeight = Math.min(resultCount * 50, 200); // 50px per result, max 200px
  
  searchResultsHeight.value = withSpring(maxHeight, {
    damping: 15,
    stiffness: 100,
  });
  
  searchResultsOpacity.value = withTiming(1, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
};

const animateSearchLoading = () => {
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

## Preference Selection Animations

### Card-Based Selection System

#### Selection State Animations

```javascript
const selectionScale = useSharedValue(1);
const selectionBorderWidth = useSharedValue(1);
const checkmarkOpacity = useSharedValue(0);
const checkmarkScale = useSharedValue(0.5);

const selectPreferenceCard = () => {
  // Card selection feedback
  selectionScale.value = withSequence(
    withTiming(0.98, { duration: 100 }),
    withSpring(1, { damping: 10, stiffness: 200 })
  );
  
  // Border enhancement
  selectionBorderWidth.value = withTiming(3, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  // Checkmark appearance
  checkmarkOpacity.value = withTiming(1, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  checkmarkScale.value = withSpring(1, {
    damping: 10,
    stiffness: 200,
  });
};

const deselectPreferenceCard = () => {
  selectionBorderWidth.value = withTiming(1, {
    duration: 200,
    easing: Easing.out(Easing.cubic),
  });
  
  checkmarkOpacity.value = withTiming(0, {
    duration: 150,
  });
  
  checkmarkScale.value = withTiming(0.5, {
    duration: 150,
  });
};
```

### Range Slider Interactions

#### Dual-Thumb Age Range Slider

```javascript
const leftThumbPosition = useSharedValue(0);
const rightThumbPosition = useSharedValue(100);
const trackFillWidth = useSharedValue(100);
const thumbScale = useSharedValue(1);

const updateAgeRange = (minAge, maxAge, ageRange) => {
  const minPosition = ((minAge - ageRange.min) / (ageRange.max - ageRange.min)) * 100;
  const maxPosition = ((maxAge - ageRange.min) / (ageRange.max - ageRange.min)) * 100;
  
  leftThumbPosition.value = withSpring(minPosition, {
    damping: 15,
    stiffness: 100,
  });
  
  rightThumbPosition.value = withSpring(maxPosition, {
    damping: 15,
    stiffness: 100,
  });
  
  trackFillWidth.value = withSpring(maxPosition - minPosition, {
    damping: 15,
    stiffness: 100,
  });
};

const handleThumbPress = () => {
  thumbScale.value = withSpring(1.2, {
    damping: 10,
    stiffness: 200,
  });
};

const handleThumbRelease = () => {
  thumbScale.value = withSpring(1, {
    damping: 12,
    stiffness: 150,
  });
};
```

### Multi-Select Skill Goals

#### Dynamic Grid Layout Animation

```javascript
const skillCardPositions = useSharedValue({});
const skillCardScales = useSharedValue({});
const selectionCountOpacity = useSharedValue(0);

const animateSkillSelection = (skillId, isSelected, selectedCount) => {
  // Individual card animation
  skillCardScales.value = {
    ...skillCardScales.value,
    [skillId]: withSpring(isSelected ? 1.03 : 1, {
      damping: 12,
      stiffness: 150,
    }),
  };
  
  // Show selection counter when skills are selected
  if (selectedCount > 0) {
    selectionCountOpacity.value = withTiming(1, {
      duration: 200,
    });
  } else {
    selectionCountOpacity.value = withTiming(0, {
      duration: 200,
    });
  }
  
  // Reorder cards based on selection (selected cards move to top)
  animateCardReordering(selectedCount);
};

const animateCardReordering = (selectedCount) => {
  // Subtle reordering animation for better visual hierarchy
  Object.keys(skillCardPositions.value).forEach((skillId, index) => {
    const isSelected = skillCardScales.value[skillId] > 1;
    const targetY = isSelected ? 0 : selectedCount * 10; // Slight offset for unselected
    
    skillCardPositions.value = {
      ...skillCardPositions.value,
      [skillId]: withSpring(targetY, {
        damping: 20,
        stiffness: 100,
      }),
    };
  });
};
```

---

## Progress Visualization Interactions

### Animated Charts and Metrics

#### Progress Chart Animation Sequence

```javascript
const chartDataPoints = useSharedValue([]);
const chartLineProgress = useSharedValue(0);
const chartPointScales = useSharedValue({});

const animateProgressChart = (newDataPoints) => {
  // Animate chart line drawing
  chartLineProgress.value = withTiming(1, {
    duration: 1500,
    easing: Easing.out(Easing.cubic),
  });
  
  // Staggered animation of data points
  newDataPoints.forEach((point, index) => {
    chartPointScales.value = {
      ...chartPointScales.value,
      [point.id]: withDelay(
        index * 100,
        withSpring(1, {
          damping: 10,
          stiffness: 200,
        })
      ),
    };
  });
  
  // Animate data values counting up
  chartDataPoints.value = newDataPoints.map((point, index) => ({
    ...point,
    animatedValue: withDelay(
      index * 100,
      withTiming(point.value, {
        duration: 800,
        easing: Easing.out(Easing.cubic),
      })
    ),
  }));
};
```

#### Skill Radar Chart Animation

```javascript
const radarVertices = useSharedValue([]);
const radarAreaOpacity = useSharedValue(0);
const skillLabelScales = useSharedValue({});

const animateRadarChart = (skillData) => {
  // Animate radar vertices expanding from center
  radarVertices.value = skillData.map((skill, index) => ({
    ...skill,
    radius: withDelay(
      index * 50,
      withSpring(skill.score / 100, {
        damping: 15,
        stiffness: 100,
      })
    ),
  }));
  
  // Fade in the filled area
  radarAreaOpacity.value = withDelay(300,
    withTiming(0.3, {
      duration: 500,
      easing: Easing.out(Easing.cubic),
    })
  );
  
  // Scale in skill labels
  skillData.forEach((skill, index) => {
    skillLabelScales.value = {
      ...skillLabelScales.value,
      [skill.id]: withDelay(
        index * 50,
        withSpring(1, {
          damping: 12,
          stiffness: 150,
        })
      ),
    };
  });
};
```

### Achievement Unlock Animations

#### Achievement Card Reveal

```javascript
const achievementScale = useSharedValue(0);
const achievementRotation = useSharedValue(-10);
const achievementGlow = useSharedValue(0);
const confettiOpacity = useSharedValue(0);

const triggerAchievementUnlock = () => {
  // Dramatic entrance with rotation correction
  achievementScale.value = withSpring(1, {
    damping: 8,
    stiffness: 100,
  });
  
  achievementRotation.value = withSpring(0, {
    damping: 12,
    stiffness: 150,
  });
  
  // Glowing effect
  achievementGlow.value = withRepeat(
    withSequence(
      withTiming(1, { duration: 300 }),
      withTiming(0.7, { duration: 300 })
    ),
    3, // Repeat 3 times
    true
  );
  
  // Confetti celebration
  confettiOpacity.value = withSequence(
    withTiming(1, { duration: 200 }),
    withDelay(2000, withTiming(0, { duration: 800 }))
  );
};
```

### Interactive Progress Metrics

#### Hover/Press Interactions for Data Points

```javascript
const dataPointHover = useSharedValue(0);
const tooltipOpacity = useSharedValue(0);
const tooltipScale = useSharedValue(0.9);

const handleDataPointInteraction = (isInteracting, dataPoint) => {
  if (isInteracting) {
    dataPointHover.value = withSpring(1.3, {
      damping: 10,
      stiffness: 200,
    });
    
    tooltipOpacity.value = withTiming(1, {
      duration: 200,
      easing: Easing.out(Easing.cubic),
    });
    
    tooltipScale.value = withSpring(1, {
      damping: 12,
      stiffness: 150,
    });
  } else {
    dataPointHover.value = withSpring(1, {
      damping: 15,
      stiffness: 200,
    });
    
    tooltipOpacity.value = withTiming(0, {
      duration: 150,
    });
    
    tooltipScale.value = withTiming(0.9, {
      duration: 150,
    });
  }
};
```

---

## Privacy Control Interactions

### Privacy Toggle Animations

#### Data Sharing Control Animation

```javascript
const togglePosition = useSharedValue(0);
const toggleBackgroundColor = useSharedValue('#E5E7EB');
const privacyIconScale = useSharedValue(1);

const animatePrivacyToggle = (isEnabled) => {
  // Toggle position animation
  togglePosition.value = withSpring(isEnabled ? 1 : 0, {
    damping: 15,
    stiffness: 200,
  });
  
  // Background color transition
  toggleBackgroundColor.value = withTiming(
    isEnabled ? '#10B981' : '#E5E7EB',
    { duration: 200 }
  );
  
  // Privacy icon feedback
  privacyIconScale.value = withSequence(
    withTiming(1.1, { duration: 100 }),
    withTiming(1, { duration: 100 })
  );
};
```

#### Data Usage Explanation Accordion

```javascript
const accordionHeight = useSharedValue(0);
const accordionOpacity = useSharedValue(0);
const chevronRotation = useSharedValue(0);

const togglePrivacyExplanation = (isExpanded, contentHeight) => {
  if (isExpanded) {
    accordionHeight.value = withSpring(contentHeight, {
      damping: 15,
      stiffness: 100,
    });
    
    accordionOpacity.value = withDelay(100,
      withTiming(1, {
        duration: 200,
        easing: Easing.out(Easing.cubic),
      })
    );
    
    chevronRotation.value = withTiming(180, {
      duration: 200,
    });
  } else {
    accordionOpacity.value = withTiming(0, {
      duration: 150,
    });
    
    accordionHeight.value = withDelay(150,
      withSpring(0, {
        damping: 20,
        stiffness: 150,
      })
    );
    
    chevronRotation.value = withTiming(0, {
      duration: 200,
    });
  }
};
```

---

## Micro-interactions & Feedback

### Button Press Feedback

#### Profile Action Buttons

```javascript
const buttonScale = useSharedValue(1);
const buttonOpacity = useSharedValue(1);
const rippleScale = useSharedValue(0);
const rippleOpacity = useSharedValue(0);

const handleButtonPress = () => {
  // Button press animation
  buttonScale.value = withSequence(
    withTiming(0.95, { duration: 100 }),
    withTiming(1, { duration: 150 })
  );
  
  // Subtle opacity change
  buttonOpacity.value = withSequence(
    withTiming(0.8, { duration: 100 }),
    withTiming(1, { duration: 150 })
  );
  
  // Ripple effect for material feedback
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

### Save State Feedback

#### Profile Save Animation

```javascript
const saveIconRotation = useSharedValue(0);
const saveSuccessScale = useSharedValue(0);
const saveSuccessOpacity = useSharedValue(0);

const animateProfileSave = () => {
  // Saving indicator
  saveIconRotation.value = withRepeat(
    withTiming(360, {
      duration: 1000,
      easing: Easing.linear,
    }),
    -1, // Infinite until save completes
    false
  );
};

const showSaveSuccess = () => {
  // Stop rotation
  saveIconRotation.value = withTiming(0, { duration: 200 });
  
  // Success checkmark animation
  saveSuccessScale.value = withSpring(1, {
    damping: 10,
    stiffness: 200,
  });
  
  saveSuccessOpacity.value = withSequence(
    withTiming(1, { duration: 200 }),
    withDelay(2000, withTiming(0, { duration: 300 }))
  );
};
```

### Form Error Animations

#### Validation Error Shake

```javascript
const errorShakeX = useSharedValue(0);
const errorHighlightOpacity = useSharedValue(0);

const triggerValidationError = () => {
  // Shake animation for error fields
  errorShakeX.value = withSequence(
    withTiming(-10, { duration: 50 }),
    withTiming(10, { duration: 50 }),
    withTiming(-10, { duration: 50 }),
    withTiming(0, { duration: 50 })
  );
  
  // Error highlight
  errorHighlightOpacity.value = withSequence(
    withTiming(0.3, { duration: 200 }),
    withDelay(1500, withTiming(0, { duration: 300 }))
  );
};
```

### Loading State Micro-animations

#### Profile Data Loading

```javascript
const skeletonShimmer = useSharedValue(0);
const loadingDots = useSharedValue(0);

const animateProfileLoading = () => {
  // Skeleton shimmer effect
  skeletonShimmer.value = withRepeat(
    withSequence(
      withTiming(1, { duration: 1000 }),
      withTiming(0, { duration: 1000 })
    ),
    -1, // Infinite
    false
  );
  
  // Loading dots animation
  loadingDots.value = withRepeat(
    withSequence(
      withTiming(0.3, { duration: 400 }),
      withTiming(1, { duration: 400 }),
      withTiming(0.3, { duration: 400 })
    ),
    -1, // Infinite
    false
  );
};
```

---

## Platform-Specific Adaptations

### iOS Specific Interactions

#### Native iOS Form Behaviors

```javascript
const iOSSpring = {
  damping: 20,
  stiffness: 300,
  mass: 0.8,
};

const iOSFormTransition = () => {
  return withSpring(targetValue, iOSSpring);
};

// iOS-style picker presentation
const presentIOSPicker = () => {
  pickerTranslateY.value = withSpring(0, iOSSpring);
  backdropOpacity.value = withTiming(0.4, { duration: 250 });
};
```

#### iOS Haptic Integration

```javascript
import { HapticFeedback } from 'react-native-haptic-feedback';

const profileHaptics = {
  fieldSelection: () => HapticFeedback.trigger('selection'),
  validationError: () => HapticFeedback.trigger('notificationWarning'),
  saveSuccess: () => HapticFeedback.trigger('notificationSuccess'),
  achievementUnlock: () => HapticFeedback.trigger('notificationSuccess'),
  buttonPress: () => HapticFeedback.trigger('impactLight'),
};
```

### Android Specific Interactions

#### Material Design Ripple Effects

```javascript
const materialRipple = useSharedValue(0);
const rippleCenter = useSharedValue({ x: 0, y: 0 });

const triggerMaterialRipple = (touchPoint) => {
  rippleCenter.value = touchPoint;
  
  materialRipple.value = withTiming(1, {
    duration: 300,
    easing: Easing.out(Easing.cubic),
  });
  
  // Auto-fade ripple
  runOnJS(setTimeout)(() => {
    materialRipple.value = withTiming(0, { duration: 200 });
  }, 100);
};
```

## Performance Optimization

### Animation Performance

#### Efficient Form Animation Management

```javascript
const useFormAnimationManager = () => {
  const activeAnimations = useRef(new Set());
  const performanceMode = useSharedValue('normal'); // 'normal' | 'reduced'
  
  const registerAnimation = (animationRef) => {
    activeAnimations.current.add(animationRef);
  };
  
  const cleanupAnimation = (animationRef) => {
    activeAnimations.current.delete(animationRef);
  };
  
  const optimizeForPerformance = () => {
    if (activeAnimations.current.size > 10) {
      performanceMode.value = 'reduced';
      // Reduce animation complexity
    } else {
      performanceMode.value = 'normal';
    }
  };
  
  return { registerAnimation, cleanupAnimation, optimizeForPerformance };
};
```

#### Memory Management for Progress Charts

```javascript
const useProgressChartOptimization = () => {
  const chartDataCache = useRef(new Map());
  const maxCacheSize = 50;
  
  const getCachedChartData = (dataKey) => {
    if (chartDataCache.current.has(dataKey)) {
      return chartDataCache.current.get(dataKey);
    }
    
    // Generate and cache new chart data
    const chartData = generateChartData(dataKey);
    
    // Manage cache size
    if (chartDataCache.current.size >= maxCacheSize) {
      const firstKey = chartDataCache.current.keys().next().value;
      chartDataCache.current.delete(firstKey);
    }
    
    chartDataCache.current.set(dataKey, chartData);
    return chartData;
  };
  
  return { getCachedChartData };
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
  interpolate,
  interpolateColor,
} from 'react-native-reanimated';

import { Gesture, GestureHandlerRootView } from 'react-native-gesture-handler';
```

### Performance Monitoring

```javascript
const useInteractionPerformance = () => {
  const interactionMetrics = useRef({
    formCompletionTime: 0,
    animationFrameDrops: 0,
    averageResponseTime: 0,
  });
  
  const trackInteractionStart = () => {
    interactionMetrics.current.startTime = performance.now();
  };
  
  const trackInteractionEnd = () => {
    const duration = performance.now() - interactionMetrics.current.startTime;
    interactionMetrics.current.formCompletionTime = duration;
    
    // Log metrics for optimization
    if (duration > 500) {
      console.warn('Slow profile interaction detected:', duration);
    }
  };
  
  return { trackInteractionStart, trackInteractionEnd };
};
```

## Last Updated
- **Version 1.0.0**: Complete interaction and animation specifications for profile system
- **Focus**: Trust-building animations with performance optimization
- **Next**: Technical implementation with form validation and privacy controls