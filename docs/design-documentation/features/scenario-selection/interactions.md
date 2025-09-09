# Scenario Selection Feature - Interactions & Animations

---
title: Scenarios Tab - Pre-built Scenario Interactions and Animations
description: Complete interaction patterns and motion design for pre-built scenario selection in the Scenarios tab
feature: scenarios-tab-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - accessibility.md
  - implementation.md
dependencies:
  - React Native Reanimated 3.6+
  - NativeBase component interactions
  - Haptic feedback integration
status: approved
---

## Animation Philosophy

**Tab Location**: Scenarios Tab

The scenario selection experience in the Scenarios tab uses **anticipation-building animations** that create excitement for browsing pre-built, trending scenarios. Every interaction reinforces quick discovery of curated content with templated contexts.

### Core Animation Principles
- **Progressive Disclosure**: Reveal information gradually to maintain engagement
- **Spatial Continuity**: Maintain clear relationships between selection states
- **Feedback Responsiveness**: Immediate visual confirmation of all interactions
- **Performance Optimization**: 60fps animations with hardware acceleration
- **Accessibility Respect**: Honor `prefers-reduced-motion` user preferences

## Interaction Specifications

### 1. Scenario Grid/Carousel Browsing

#### Initial Load Animation
**Duration**: 400ms with staggered reveals
**Easing**: `cubic-bezier(0.0, 0, 0.2, 1)` (ease-out)

```typescript
// React Native Reanimated 3 implementation
const ScenarioCardReveal = ({ children, index }: CardProps) => {
  const opacity = useSharedValue(0);
  const translateY = useSharedValue(30);
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateY: translateY.value }],
  }));
  
  useEffect(() => {
    // Staggered reveal based on card index
    const delay = index * 80; // 80ms stagger
    
    opacity.value = withDelay(delay, withTiming(1, {
      duration: 400,
      easing: Easing.out(Easing.cubic),
    }));
    
    translateY.value = withDelay(delay, withTiming(0, {
      duration: 400,
      easing: Easing.out(Easing.cubic),
    }));
  }, []);
  
  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
};
```

#### Scenario Card Hover/Press States
**Touch Down**: Immediate scale response (100ms)
**Touch Release**: Return animation (200ms)
**Haptic**: Light impact on touch down

```typescript
const ScenarioCard = ({ scenario, onSelect }: ScenarioCardProps) => {
  const scale = useSharedValue(1);
  const elevation = useSharedValue(2);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    shadowOpacity: elevation.value * 0.1,
    shadowOffset: {
      width: 0,
      height: elevation.value,
    },
    shadowRadius: elevation.value * 2,
  }));
  
  const handlePressIn = () => {
    // Haptic feedback
    HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Light);
    
    scale.value = withTiming(0.95, {
      duration: 100,
      easing: Easing.out(Easing.quad),
    });
    
    elevation.value = withTiming(4, {
      duration: 100,
    });
  };
  
  const handlePressOut = () => {
    scale.value = withTiming(1, {
      duration: 200,
      easing: Easing.out(Easing.cubic),
    });
    
    elevation.value = withTiming(2, {
      duration: 200,
    });
  };
  
  return (
    <Pressable
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={() => onSelect(scenario)}
    >
      <Animated.View style={[styles.card, animatedStyle]}>
        {/* Card content */}
      </Animated.View>
    </Pressable>
  );
};
```

#### Scenario Preview Expansion
**Trigger**: Long press or info icon tap
**Duration**: 300ms expansion, 250ms collapse
**Behavior**: Modal-style overlay with backdrop blur

```typescript
const ScenarioPreview = ({ scenario, isVisible, onClose }: PreviewProps) => {
  const backdropOpacity = useSharedValue(0);
  const modalScale = useSharedValue(0.8);
  const modalOpacity = useSharedValue(0);
  
  const backdropStyle = useAnimatedStyle(() => ({
    opacity: backdropOpacity.value,
  }));
  
  const modalStyle = useAnimatedStyle(() => ({
    opacity: modalOpacity.value,
    transform: [{ scale: modalScale.value }],
  }));
  
  useEffect(() => {
    if (isVisible) {
      // Show animation
      backdropOpacity.value = withTiming(0.7, { duration: 300 });
      modalScale.value = withTiming(1, {
        duration: 300,
        easing: Easing.out(Easing.back(1.1)),
      });
      modalOpacity.value = withTiming(1, { duration: 300 });
    } else {
      // Hide animation
      backdropOpacity.value = withTiming(0, { duration: 250 });
      modalScale.value = withTiming(0.8, { duration: 250 });
      modalOpacity.value = withTiming(0, { duration: 250 });
    }
  }, [isVisible]);
  
  return (
    <Modal transparent visible={isVisible}>
      <Animated.View style={[styles.backdrop, backdropStyle]}>
        <Pressable style={StyleSheet.absoluteFill} onPress={onClose} />
        <Animated.View style={[styles.previewModal, modalStyle]}>
          {/* Preview content */}
        </Animated.View>
      </Animated.View>
    </Modal>
  );
};
```

### 2. Scenario Selection Transition

#### Selected Card Highlight
**Duration**: 200ms selection confirmation
**Visual**: Orange accent border with subtle glow
**Haptic**: Selection feedback (medium impact)

```typescript
const handleScenarioSelection = (scenario: Scenario) => {
  // Haptic feedback for selection
  HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Medium);
  
  // Visual selection confirmation
  selectedBorderWidth.value = withSequence(
    withTiming(3, { duration: 200 }),
    withDelay(500, withTiming(2, { duration: 300 }))
  );
  
  glowOpacity.value = withSequence(
    withTiming(0.8, { duration: 200 }),
    withDelay(500, withTiming(0.4, { duration: 300 }))
  );
  
  // Navigate to difficulty selection
  setTimeout(() => {
    navigation.navigate('DifficultySelection', { scenario });
  }, 800);
};
```

#### Page Transition to Difficulty Selection
**Duration**: 400ms slide transition
**Direction**: Right-to-left slide with parallax effect
**Continuity**: Selected scenario image carries through

```typescript
const ScenarioToDifficultyTransition = () => {
  const slideX = useSharedValue(width);
  const scenarioImageScale = useSharedValue(1);
  
  const slideStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: slideX.value }],
  }));
  
  const scenarioImageStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scenarioImageScale.value }],
  }));
  
  const animateTransition = () => {
    // Slide in difficulty selection
    slideX.value = withTiming(0, {
      duration: 400,
      easing: Easing.out(Easing.cubic),
    });
    
    // Scale scenario image for continuity
    scenarioImageScale.value = withTiming(0.8, {
      duration: 400,
      easing: Easing.inOut(Easing.quad),
    });
  };
  
  return (
    <View style={styles.transitionContainer}>
      <Animated.View style={scenarioImageStyle}>
        {/* Scenario image */}
      </Animated.View>
      <Animated.View style={[styles.difficultyPanel, slideStyle]}>
        {/* Difficulty selection content */}
      </Animated.View>
    </View>
  );
};
```

### 3. Difficulty Level Selection

#### Difficulty Button States
**Idle**: Subtle glow with difficulty color
**Hover**: Scale up with enhanced glow
**Selected**: Confirm animation with haptic feedback

```typescript
const DifficultyButton = ({ difficulty, isSelected, onSelect }: DifficultyProps) => {
  const scale = useSharedValue(1);
  const glowOpacity = useSharedValue(0.3);
  const borderWidth = useSharedValue(isSelected ? 2 : 1);
  
  const getDifficultyColor = () => {
    switch (difficulty) {
      case 'green': return '#22C55E';
      case 'yellow': return '#F59E0B';
      case 'red': return '#EF4444';
    }
  };
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    shadowOpacity: glowOpacity.value,
    shadowColor: getDifficultyColor(),
    borderWidth: borderWidth.value,
    borderColor: getDifficultyColor(),
  }));
  
  const handlePress = () => {
    HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Medium);
    
    // Selection animation
    scale.value = withSequence(
      withTiming(0.95, { duration: 100 }),
      withTiming(1.05, { duration: 150 }),
      withTiming(1, { duration: 100 })
    );
    
    borderWidth.value = withTiming(2, { duration: 200 });
    glowOpacity.value = withTiming(0.6, { duration: 200 });
    
    onSelect(difficulty);
  };
  
  return (
    <Pressable onPress={handlePress}>
      <Animated.View style={[styles.difficultyButton, animatedStyle]}>
        {/* Button content */}
      </Animated.View>
    </Pressable>
  );
};
```

#### Progress Indicator Animation
**Purpose**: Show selection progress through the flow
**Style**: Horizontal progress bar with smooth fills
**Duration**: 300ms per step completion

```typescript
const SelectionProgress = ({ currentStep, totalSteps }: ProgressProps) => {
  const progressWidth = useSharedValue(0);
  
  const progressStyle = useAnimatedStyle(() => ({
    width: `${progressWidth.value}%`,
  }));
  
  useEffect(() => {
    const targetProgress = (currentStep / totalSteps) * 100;
    
    progressWidth.value = withTiming(targetProgress, {
      duration: 300,
      easing: Easing.out(Easing.quad),
    });
  }, [currentStep]);
  
  return (
    <View style={styles.progressContainer}>
      <Animated.View style={[styles.progressBar, progressStyle]} />
    </View>
  );
};
```

### 4. Scenario Confirmation & Launch

#### Final Confirmation Screen
**Animation**: Summary card assembly with selected elements
**Duration**: 500ms staged reveal
**Feedback**: Success state with clear call-to-action

```typescript
const ConfirmationScreen = ({ scenario, difficulty }: ConfirmationProps) => {
  const scenarioOpacity = useSharedValue(0);
  const difficultyOpacity = useSharedValue(0);
  const startButtonScale = useSharedValue(0);
  
  const scenarioStyle = useAnimatedStyle(() => ({
    opacity: scenarioOpacity.value,
  }));
  
  const difficultyStyle = useAnimatedStyle(() => ({
    opacity: difficultyOpacity.value,
  }));
  
  const startButtonStyle = useAnimatedStyle(() => ({
    transform: [{ scale: startButtonScale.value }],
  }));
  
  useEffect(() => {
    // Staged reveal animation
    scenarioOpacity.value = withTiming(1, { duration: 300 });
    
    setTimeout(() => {
      difficultyOpacity.value = withTiming(1, { duration: 300 });
    }, 200);
    
    setTimeout(() => {
      startButtonScale.value = withTiming(1, {
        duration: 400,
        easing: Easing.out(Easing.back(1.2)),
      });
    }, 500);
  }, []);
  
  return (
    <View style={styles.confirmationContainer}>
      <Animated.View style={scenarioStyle}>
        {/* Scenario summary */}
      </Animated.View>
      <Animated.View style={difficultyStyle}>
        {/* Difficulty indicator */}
      </Animated.View>
      <Animated.View style={startButtonStyle}>
        {/* Start practice button */}
      </Animated.View>
    </View>
  );
};
```

#### Launch Transition
**Purpose**: Build anticipation for conversation start
**Style**: Expanding circle transition with scenario context
**Duration**: 800ms total with staged elements

```typescript
const LaunchTransition = ({ onComplete }: LaunchProps) => {
  const circleScale = useSharedValue(0);
  const overlayOpacity = useSharedValue(0);
  const contextOpacity = useSharedValue(1);
  
  const circleStyle = useAnimatedStyle(() => ({
    transform: [{ scale: circleScale.value }],
  }));
  
  const overlayStyle = useAnimatedStyle(() => ({
    opacity: overlayOpacity.value,
  }));
  
  const contextStyle = useAnimatedStyle(() => ({
    opacity: contextOpacity.value,
  }));
  
  const startLaunchAnimation = () => {
    // Context fade out
    contextOpacity.value = withTiming(0, { duration: 300 });
    
    // Circle expansion
    setTimeout(() => {
      circleScale.value = withTiming(10, {
        duration: 600,
        easing: Easing.out(Easing.quad),
      });
      
      overlayOpacity.value = withTiming(1, { duration: 600 });
    }, 200);
    
    // Complete transition
    setTimeout(() => {
      onComplete();
    }, 800);
  };
  
  return (
    <View style={styles.launchContainer}>
      <Animated.View style={contextStyle}>
        {/* Scenario context */}
      </Animated.View>
      <Animated.View style={[styles.expandingCircle, circleStyle]} />
      <Animated.View style={[styles.overlay, overlayStyle]} />
    </View>
  );
};
```

## Micro-Interactions

### 1. Success Rate Indicators
**Animation**: Subtle pulse on scenario cards showing personal success rates
**Timing**: 2-second intervals with 200ms pulse duration
**Visual**: Green glow for high success rates, yellow for moderate

### 2. Quick Practice Highlights
**Behavior**: Recently used scenarios have subtle animation attraction
**Style**: Gentle scale breathing effect (1.0 to 1.02 scale)
**Duration**: 3-second cycle with ease-in-out timing

### 3. Recommendation Badges
**Animation**: Gentle bounce when AI-recommended scenarios appear
**Trigger**: Based on profile analysis and progress patterns
**Style**: Small badge with spring animation and sparkle effect

### 4. Loading States
**Scenario Loading**: Skeleton cards with shimmer effects
**Image Loading**: Progressive blur-to-sharp reveal
**Transition Loading**: Smooth spinner with scenario theme colors

## Advanced Interaction Patterns

### 1. Gesture Navigation
**Swipe Right**: Quick access to recently used scenarios
**Swipe Left**: Browse scenario categories
**Long Press**: Scenario preview and detailed information
**Pull to Refresh**: Reload scenario recommendations

### 2. Voice Navigation Support
**Voice Commands**: "Select coffee shop", "Choose green difficulty"
**Voice Feedback**: Spoken confirmation of selections
**Integration**: React Native Voice for speech recognition

### 3. Apple Watch/Wear OS Integration
**Quick Selection**: Choose scenarios from watch interface
**Practice Reminders**: Gentle notifications to practice
**Progress Glances**: Quick view of scenario completion rates

## Platform-Specific Adaptations

### iOS Interactions
- **Haptic Feedback**: Rich haptic patterns for different selections
- **Dynamic Island**: Show current scenario selection in Dynamic Island
- **Shortcuts Integration**: Siri shortcuts for favorite scenarios
- **Context Menus**: 3D Touch/long press for scenario options

### Android Interactions
- **Material Motion**: Follow Material Design motion principles
- **Adaptive Brightness**: Adjust UI based on ambient light
- **Quick Settings**: Scenario shortcuts in notification panel
- **Accessibility Services**: Enhanced TalkBack integration

## Performance Optimization

### Animation Performance
```typescript
// Enable hardware acceleration for all animations
const styles = StyleSheet.create({
  card: {
    // Force hardware acceleration
    transform: [{ translateZ: 0 }],
    // Optimize for 60fps
    shouldRasterizeIOS: true,
    renderToHardwareTextureAndroid: true,
  },
});

// Use worklets for smooth animations
const gestureHandler = useAnimatedGestureHandler({
  onStart: (_, ctx) => {
    'worklet';
    ctx.startX = translateX.value;
  },
  onActive: (event, ctx) => {
    'worklet';
    translateX.value = ctx.startX + event.translationX;
  },
  onEnd: () => {
    'worklet';
    translateX.value = withSpring(0);
  },
});
```

### Memory Management
- **Image Caching**: Preload scenario images with smart cache management
- **Animation Cleanup**: Properly dispose of animation values on unmount
- **State Optimization**: Use React.memo for scenario cards to prevent unnecessary re-renders

## Accessibility Integration

### Screen Reader Support
- **Selection Announcements**: Clear audio feedback for scenario and difficulty selections
- **Progress Updates**: Announce completion of each selection step
- **Context Description**: Rich descriptions of scenario environments

### Motor Accessibility
- **Large Touch Targets**: Minimum 44×44pt touch areas for all interactive elements
- **Voice Selection**: Complete voice navigation for hands-free operation
- **Switch Control**: iOS Switch Control and Android Switch Access support

### Cognitive Accessibility
- **Clear Feedback**: Immediate visual and audio confirmation of selections
- **Undo Options**: Easy way to change selections before final confirmation
- **Progress Indicators**: Clear visual progress through selection flow

## Related Documentation

- **[README](./README.md)** - Feature overview and specifications
- **[User Journey](./user-journey.md)** - Complete user flow analysis
- **[Screen States](./screen-states.md)** - Visual specifications for all states
- **[Accessibility](./accessibility.md)** - Inclusive design considerations
- **[Implementation](./implementation.md)** - Technical implementation details

## Implementation Notes

### Animation Library Integration
- **React Native Reanimated 3.6+**: Primary animation framework
- **React Native Gesture Handler**: Touch and gesture management
- **Lottie React Native**: Complex animations and micro-interactions
- **React Native Haptic Feedback**: Platform-appropriate haptic responses

### Performance Targets
- **60fps**: All animations maintain 60fps on mid-range devices
- **Touch Response**: <16ms response time for touch interactions
- **Page Transitions**: <400ms complete transition times
- **Memory Usage**: <50MB additional memory for animations

## Last Updated
- **Version 1.0.0**: Complete interaction specifications with React Native Reanimated 3 implementations
- **Focus**: Performance-optimized animations with accessibility integration
- **Next**: Implementation testing and performance validation