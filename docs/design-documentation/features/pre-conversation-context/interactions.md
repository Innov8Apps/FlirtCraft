# Pre-Conversation Context Interactions

---
title: Pre-Conversation Context Interaction Specifications
description: Detailed interaction patterns, gestures, and animations for context review
feature: pre-conversation-context
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native Reanimated
  - Gesture Handler
  - Context card components
status: approved
---

## Overview

This document specifies all interaction patterns and animations for the pre-conversation context feature. The interactions are designed to feel natural and engaging while building user confidence through smooth, responsive feedback and clear affordances.

## Interaction Design Principles

### Core Interaction Goals
- **Confidence Building**: Every interaction reinforces user readiness
- **Natural Flow**: Gestures feel intuitive and platform-appropriate
- **Clear Feedback**: Users always understand interaction results
- **Accessible Control**: All interactions work with assistive technologies
- **Performance First**: 60fps animations maintain smooth experience

### Animation Philosophy
- **Purposeful Motion**: Every animation serves a functional purpose
- **Emotional Resonance**: Animations reinforce confidence and excitement
- **Respectful Timing**: Motion timing respects user cognitive processing
- **Reduced Motion Support**: Alternative feedback for motion-sensitive users

## Primary Interaction Patterns

### Context Card Review Interactions

#### Card Scroll Navigation

**Gesture**: Vertical scroll through context cards
**Platform**: iOS, Android, Web

**Implementation:**
```tsx
import { ScrollView } from 'react-native';
import Animated, { 
  useSharedValue, 
  useAnimatedScrollHandler,
  useAnimatedStyle,
  interpolate
} from 'react-native-reanimated';

const ContextCardScroll = () => {
  const scrollY = useSharedValue(0);
  
  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollY.value = event.contentOffset.y;
      // Track which cards are in view for progress tracking
      trackCardVisibility(event.contentOffset.y);
    }
  });
  
  return (
    <Animated.ScrollView
      onScroll={scrollHandler}
      scrollEventThrottle={16}
      showsVerticalScrollIndicator={false}
    >
      {contextCards.map((card, index) => (
        <ContextCard key={card.id} index={index} scrollY={scrollY} />
      ))}
    </Animated.ScrollView>
  );
};
```

**Animation Details:**
- **Scroll Physics**: Natural iOS/Android scrolling with appropriate bounce
- **Parallax Effect**: Subtle background movement during scroll
- **Card Highlighting**: Active card gets subtle emphasis
- **Progress Tracking**: Header dots update based on scroll position

**Accessibility Considerations:**
- **Screen Reader**: Announce when new card comes into focus
- **Keyboard Navigation**: Tab to move between card sections
- **Reduced Motion**: Disable parallax effects, maintain scroll functionality

#### Card Expansion/Collapse

**Gesture**: Tap card header to expand/collapse detailed content
**Platform**: All platforms
**Purpose**: Progressive disclosure of detailed information

**Implementation:**
```tsx
const ExpandableCard = ({ card, isExpanded, onToggle }) => {
  const height = useSharedValue(isExpanded ? 'auto' : 120);
  const rotation = useSharedValue(isExpanded ? 180 : 0);
  
  const animatedStyle = useAnimatedStyle(() => ({
    height: height.value === 'auto' ? undefined : height.value,
    overflow: 'hidden',
  }));
  
  const chevronStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${rotation.value}deg` }],
  }));
  
  const handlePress = () => {
    const newExpanded = !isExpanded;
    
    height.value = withSpring(newExpanded ? 200 : 120, {
      damping: 15,
      stiffness: 150,
    });
    
    rotation.value = withSpring(newExpanded ? 180 : 0);
    onToggle(card.id, newExpanded);
  };
  
  return (
    <Pressable onPress={handlePress}>
      <Animated.View style={animatedStyle}>
        <CardHeader>
          <CardTitle>{card.title}</CardTitle>
          <Animated.View style={chevronStyle}>
            <ChevronDown size={20} color="gray.500" />
          </Animated.View>
        </CardHeader>
        <CardContent>{card.content}</CardContent>
      </Animated.View>
    </Pressable>
  );
};
```

**Animation Specifications:**
- **Duration**: 300ms with spring physics
- **Easing**: Natural spring animation (damping: 15, stiffness: 150)
- **Visual Feedback**: Chevron rotates, card height animates smoothly
- **State Persistence**: Expansion state maintained during session

### Conversation Starter Interactions

#### Starter Selection Animation

**Gesture**: Tap conversation starter to select for use
**Platform**: All platforms
**Visual Feedback**: Selection highlight with copy-to-input indication

**Implementation:**
```tsx
const ConversationStarter = ({ starter, index, onSelect }) => {
  const scale = useSharedValue(1);
  const backgroundColor = useSharedValue('transparent');
  const borderColor = useSharedValue('gray.200');
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    backgroundColor: backgroundColor.value,
    borderColor: borderColor.value,
  }));
  
  const handlePressIn = () => {
    scale.value = withSpring(0.98);
    backgroundColor.value = withTiming('purple.50', { duration: 150 });
    borderColor.value = withTiming('purple.200', { duration: 150 });
  };
  
  const handlePressOut = () => {
    scale.value = withSpring(1);
  };
  
  const handlePress = () => {
    // Selection animation
    backgroundColor.value = withSequence(
      withTiming('purple.200', { duration: 200 }),
      withTiming('purple.100', { duration: 300 })
    );
    
    // Trigger selection callback with feedback
    onSelect(starter, index);
    
    // Show selection confirmation
    showSelectionFeedback();
  };
  
  return (
    <Pressable
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={handlePress}
    >
      <Animated.View style={[styles.starterCard, animatedStyle]}>
        <Text>{starter}</Text>
        <SelectionIcon />
      </Animated.View>
    </Pressable>
  );
};
```

**Selection Feedback:**
```tsx
const showSelectionFeedback = () => {
  // Toast notification
  showToast({
    message: "Starter copied! You can edit it before sending.",
    type: "success",
    duration: 2000
  });
  
  // Haptic feedback on mobile
  if (Platform.OS !== 'web') {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  }
};
```

**Animation Details:**
- **Press Feedback**: Scale down to 98% with color change
- **Selection Highlight**: Purple background fade-in
- **Success Animation**: Brief pulse animation on successful selection
- **Haptic Feedback**: Light impact on mobile platforms

### Action Button Interactions

#### Primary Action Button (Start Conversation)

**Button State Animations:**
- **Disabled → Enabled**: Fade from gray to orange gradient
- **Press Feedback**: Scale animation with color intensification
- **Loading State**: Spinner replacement with maintained button size

**Implementation:**
```tsx
const StartConversationButton = ({ disabled, loading, onPress }) => {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(disabled ? 0.5 : 1);
  const gradientOpacity = useSharedValue(disabled ? 0 : 1);
  
  useEffect(() => {
    opacity.value = withTiming(disabled ? 0.5 : 1, { duration: 300 });
    gradientOpacity.value = withTiming(disabled ? 0 : 1, { duration: 300 });
  }, [disabled]);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));
  
  const gradientStyle = useAnimatedStyle(() => ({
    opacity: gradientOpacity.value,
  }));
  
  const handlePressIn = () => {
    if (!disabled && !loading) {
      scale.value = withSpring(0.96);
    }
  };
  
  const handlePressOut = () => {
    scale.value = withSpring(1);
  };
  
  const handlePress = () => {
    if (!disabled && !loading) {
      // Success animation before navigation
      scale.value = withSequence(
        withSpring(0.94),
        withSpring(1.02),
        withSpring(1)
      );
      
      setTimeout(onPress, 200); // Allow animation to complete
    }
  };
  
  return (
    <Pressable
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={handlePress}
    >
      <Animated.View style={[styles.button, animatedStyle]}>
        <Animated.View style={[styles.gradient, gradientStyle]} />
        {loading ? (
          <Spinner color="white" />
        ) : (
          <Text style={styles.buttonText}>Start Conversation</Text>
        )}
      </Animated.View>
    </Pressable>
  );
};
```

#### Secondary Action Buttons (Regenerate, Back)

**Interaction Pattern**: Lighter feedback with outline style preservation
**Animation**: Subtle background color change and scale feedback

```tsx
const SecondaryButton = ({ variant, onPress, children }) => {
  const scale = useSharedValue(1);
  const backgroundColor = useSharedValue('transparent');
  
  const backgroundColors = {
    outline: 'orange.50',
    ghost: 'gray.100'
  };
  
  const handlePressIn = () => {
    scale.value = withSpring(0.98);
    backgroundColor.value = withTiming(backgroundColors[variant], { duration: 150 });
  };
  
  const handlePressOut = () => {
    scale.value = withSpring(1);
    backgroundColor.value = withTiming('transparent', { duration: 200 });
  };
  
  // Similar implementation with lighter feedback
};
```

### Context Regeneration Interactions

#### Regeneration Trigger Animation

**Gesture**: Tap "Generate New Context" button
**Visual Flow**: 
1. Button shows loading state
2. Cards fade out with scale animation
3. Loading overlay appears
4. New cards fade in with stagger

**Implementation:**
```tsx
const ContextRegenerationFlow = () => {
  const cardsOpacity = useSharedValue(1);
  const cardsScale = useSharedValue(1);
  const loadingOpacity = useSharedValue(0);
  
  const regenerateContext = async () => {
    // Step 1: Hide current cards
    cardsOpacity.value = withTiming(0, { duration: 300 });
    cardsScale.value = withTiming(0.9, { duration: 300 });
    
    // Step 2: Show loading overlay
    setTimeout(() => {
      loadingOpacity.value = withTiming(1, { duration: 200 });
    }, 200);
    
    // Step 3: Generate new content
    const newContext = await generateContext();
    
    // Step 4: Hide loading and show new cards
    loadingOpacity.value = withTiming(0, { duration: 200 });
    
    setTimeout(() => {
      cardsOpacity.value = withTiming(1, { duration: 400 });
      cardsScale.value = withSpring(1);
      
      // Trigger card entrance animations
      triggerCardEntranceSequence();
    }, 300);
  };
  
  return (
    <View>
      <Animated.View style={[{ opacity: cardsOpacity, transform: [{ scale: cardsScale }] }]}>
        {contextCards}
      </Animated.View>
      
      <Animated.View style={[styles.loadingOverlay, { opacity: loadingOpacity }]}>
        <LoadingSpinner />
        <Text>Creating new scenario...</Text>
      </Animated.View>
    </View>
  );
};
```

#### Pull-to-Refresh Alternative

**Gesture**: Pull down on card container to regenerate
**Platform**: Mobile only
**Visual Feedback**: Refresh indicator with contextual message

```tsx
const PullToRegenerateCards = ({ onRefresh, refreshing }) => {
  return (
    <ScrollView
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor="orange.500"
          title="Pull to generate new context"
          titleColor="gray.600"
        />
      }
    >
      {contextCards}
    </ScrollView>
  );
};
```

### Card Entrance Animations

#### Staggered Card Appearance

**Animation Flow**: Cards appear in sequence with spring physics
**Timing**: 100ms stagger between each card
**Physics**: Natural bounce effect without overshot

```tsx
const CardEntranceAnimation = ({ cards, trigger }) => {
  const cardAnimations = cards.map(() => ({
    opacity: useSharedValue(0),
    translateY: useSharedValue(30),
    scale: useSharedValue(0.8),
  }));
  
  useEffect(() => {
    if (trigger) {
      cardAnimations.forEach((animation, index) => {
        const delay = index * 100; // 100ms stagger
        
        setTimeout(() => {
          animation.opacity.value = withTiming(1, { duration: 400 });
          animation.translateY.value = withSpring(0, {
            damping: 12,
            stiffness: 120,
          });
          animation.scale.value = withSpring(1, {
            damping: 10,
            stiffness: 100,
          });
        }, delay);
      });
    }
  }, [trigger]);
  
  return (
    <>
      {cards.map((card, index) => (
        <Animated.View
          key={card.id}
          style={[
            {
              opacity: cardAnimations[index].opacity,
              transform: [
                { translateY: cardAnimations[index].translateY },
                { scale: cardAnimations[index].scale },
              ],
            },
          ]}
        >
          <ContextCard card={card} />
        </Animated.View>
      ))}
    </>
  );
};
```

### Navigation and Transition Interactions

#### Smooth Page Transitions

**Context to Conversation Transition:**
```tsx
const PageTransition = () => {
  const screenOpacity = useSharedValue(1);
  const screenScale = useSharedValue(1);
  
  const navigateToConversation = () => {
    // Exit animation
    screenOpacity.value = withTiming(0, { duration: 300 });
    screenScale.value = withTiming(0.95, { duration: 300 });
    
    // Navigate after animation completes
    setTimeout(() => {
      navigation.navigate('Conversation', { context: contextData });
    }, 300);
  };
  
  return (
    <Animated.View style={[
      { opacity: screenOpacity, transform: [{ scale: screenScale }] }
    ]}>
      {/* Screen content */}
    </Animated.View>
  );
};
```

#### Back Navigation Confirmation

**Gesture**: Back button press or swipe gesture
**Confirmation**: Modal for unsaved context

```tsx
const BackNavigationHandler = () => {
  const [showConfirmation, setShowConfirmation] = useState(false);
  
  const handleBackPress = () => {
    if (hasGeneratedContext) {
      setShowConfirmation(true);
    } else {
      navigation.goBack();
    }
  };
  
  return (
    <ConfirmationModal
      visible={showConfirmation}
      title="Leave scenario preparation?"
      message="Your generated context will be lost. Are you sure?"
      confirmText="Leave"
      cancelText="Stay"
      onConfirm={() => {
        setShowConfirmation(false);
        navigation.goBack();
      }}
      onCancel={() => setShowConfirmation(false)}
    />
  );
};
```

## Advanced Interaction Features

### Progress Tracking Animations

#### Header Progress Dots

**Animation**: Dots fill with color as cards are reviewed
**Timing**: Smooth transition when card comes into view

```tsx
const ProgressDots = ({ currentCard, totalCards }) => {
  const dotAnimations = Array.from({ length: totalCards }, () => ({
    scale: useSharedValue(0.8),
    backgroundColor: useSharedValue('gray.300'),
  }));
  
  useEffect(() => {
    dotAnimations.forEach((dot, index) => {
      const isActive = index <= currentCard;
      
      dot.scale.value = withSpring(isActive ? 1 : 0.8);
      dot.backgroundColor.value = withTiming(
        isActive ? 'orange.500' : 'gray.300',
        { duration: 300 }
      );
    });
  }, [currentCard]);
  
  return (
    <HStack space={2}>
      {dotAnimations.map((animation, index) => (
        <Animated.View
          key={index}
          style={[
            styles.progressDot,
            {
              backgroundColor: animation.backgroundColor,
              transform: [{ scale: animation.scale }],
            },
          ]}
        />
      ))}
    </HStack>
  );
};
```

### Context Reference Modal Interactions

#### Modal Presentation Animation

**Gesture**: Tap context button during conversation
**Animation**: Slide up from bottom with backdrop blur

```tsx
const ContextReferenceModal = ({ visible, onClose, contextData }) => {
  const translateY = useSharedValue(400);
  const backdropOpacity = useSharedValue(0);
  
  useEffect(() => {
    if (visible) {
      backdropOpacity.value = withTiming(0.5, { duration: 300 });
      translateY.value = withSpring(0, {
        damping: 20,
        stiffness: 90,
      });
    } else {
      backdropOpacity.value = withTiming(0, { duration: 250 });
      translateY.value = withTiming(400, { duration: 250 });
    }
  }, [visible]);
  
  const backdropStyle = useAnimatedStyle(() => ({
    opacity: backdropOpacity.value,
  }));
  
  const modalStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));
  
  return (
    <Modal transparent visible={visible}>
      <Pressable style={StyleSheet.absoluteFill} onPress={onClose}>
        <Animated.View style={[styles.backdrop, backdropStyle]} />
      </Pressable>
      
      <Animated.View style={[styles.modal, modalStyle]}>
        <ContextSummaryCards data={contextData} />
      </Animated.View>
    </Modal>
  );
};
```

#### Context Card Horizontal Scroll

**Gesture**: Horizontal swipe between context categories
**Visual Feedback**: Card transition with pagination dots

```tsx
const HorizontalContextCards = ({ contextData }) => {
  const scrollX = useSharedValue(0);
  const [currentIndex, setCurrentIndex] = useState(0);
  
  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollX.value = event.contentOffset.x;
    },
  });
  
  return (
    <>
      <Animated.ScrollView
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onScroll={scrollHandler}
        scrollEventThrottle={16}
      >
        {contextData.map((card, index) => (
          <ContextSummaryCard
            key={card.id}
            card={card}
            index={index}
            scrollX={scrollX}
          />
        ))}
      </Animated.ScrollView>
      
      <PaginationDots
        data={contextData}
        scrollX={scrollX}
        currentIndex={currentIndex}
      />
    </>
  );
};
```

## Accessibility Interaction Patterns

### Screen Reader Interactions

**Focus Management:**
```tsx
const AccessibleContextCards = () => {
  const cardRefs = useRef([]);
  
  const announceCardFocus = (cardIndex) => {
    if (Platform.OS === 'ios') {
      AccessibilityInfo.announceForAccessibility(
        `Viewing ${contextCards[cardIndex].title} card, ${cardIndex + 1} of ${contextCards.length}`
      );
    }
  };
  
  return (
    <ScrollView>
      {contextCards.map((card, index) => (
        <View
          key={card.id}
          ref={(ref) => (cardRefs.current[index] = ref)}
          accessible={true}
          accessibilityRole="region"
          accessibilityLabel={`${card.title} context card`}
          onAccessibilityFocus={() => announceCardFocus(index)}
        >
          <ContextCard card={card} />
        </View>
      ))}
    </ScrollView>
  );
};
```

### Keyboard Navigation

**Tab Order Management:**
```tsx
const KeyboardNavigableInterface = () => {
  const [focusedElement, setFocusedElement] = useState(0);
  
  const handleKeyPress = (event) => {
    switch (event.key) {
      case 'Tab':
        setFocusedElement((prev) => (prev + 1) % totalElements);
        break;
      case 'Enter':
        activateFocusedElement();
        break;
      case 'Escape':
        handleBackNavigation();
        break;
    }
  };
  
  return (
    <View onKeyPress={handleKeyPress}>
      {/* Keyboard accessible interface */}
    </View>
  );
};
```

### Haptic Feedback Integration

**Mobile Haptic Patterns:**
```tsx
import * as Haptics from 'expo-haptics';

const HapticFeedbackPatterns = {
  cardSelection: () => {
    if (Platform.OS !== 'web') {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  },
  
  buttonPress: () => {
    if (Platform.OS !== 'web') {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
  },
  
  regenerationComplete: () => {
    if (Platform.OS !== 'web') {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    }
  },
  
  error: () => {
    if (Platform.OS !== 'web') {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    }
  },
};
```

## Performance Optimization

### Animation Performance

**Optimization Strategies:**
```tsx
const PerformantAnimations = {
  // Use native driver for transform and opacity
  useNativeDriver: true,
  
  // Avoid animating layout properties
  avoidLayoutAnimations: ['width', 'height', 'padding', 'margin'],
  
  // Optimize re-renders with React.memo
  memoizedComponents: React.memo(ContextCard),
  
  // Use useSharedValue for high-frequency updates
  sharedValues: useSharedValue(0),
  
  // Optimize gesture handlers
  optimizedGestures: {
    shouldCancelWhenOutside: true,
    simultaneousHandlers: [],
  },
};
```

### Memory Management

**Component Cleanup:**
```tsx
useEffect(() => {
  return () => {
    // Cleanup animations on unmount
    cancelAnimation(scrollY);
    cancelAnimation(cardOpacity);
    
    // Remove event listeners
    removeEventListener('keydown', handleKeyPress);
  };
}, []);
```

## Testing Specifications

### Interaction Testing

**Automated Testing:**
```tsx
// Test card selection interaction
test('context card selection provides proper feedback', async () => {
  const { getByTestId } = render(<ContextCards />);
  const card = getByTestId('context-card-0');
  
  fireEvent.press(card);
  
  await waitFor(() => {
    expect(getByTestId('selection-feedback')).toBeTruthy();
  });
});

// Test regeneration flow
test('regeneration animation completes successfully', async () => {
  const { getByText } = render(<PreConversationContext />);
  const regenerateButton = getByText('Generate New Context');
  
  fireEvent.press(regenerateButton);
  
  await waitFor(() => {
    expect(getByTestId('loading-overlay')).toBeTruthy();
  }, { timeout: 100 });
  
  await waitFor(() => {
    expect(queryByTestId('loading-overlay')).toBeNull();
  }, { timeout: 5000 });
});
```

**Manual Testing Checklist:**
- [ ] All animations run at 60fps
- [ ] Haptic feedback works on mobile devices
- [ ] Screen reader announces interactions correctly
- [ ] Keyboard navigation follows logical tab order
- [ ] Reduced motion preferences are respected
- [ ] Touch targets meet 44px minimum requirement
- [ ] Gesture conflicts are resolved appropriately

---

## Related Documentation

- [Pre-Conversation Context README](./README.md) - Feature overview and requirements
- [Screen States](./screen-states.md) - Visual specifications for all interface states
- [User Journey](./user-journey.md) - Complete user flow through context review
- [Animation Tokens](../../design-system/tokens/animations.md) - System-wide animation specifications

## Implementation Checklist

### Core Interactions
- [ ] Context card scroll navigation implemented
- [ ] Conversation starter selection with feedback
- [ ] Primary action button with state animations
- [ ] Context regeneration flow with loading states
- [ ] Modal presentation for context reference

### Advanced Features
- [ ] Pull-to-refresh alternative for regeneration
- [ ] Staggered card entrance animations
- [ ] Progress tracking with animated indicators
- [ ] Smooth page transitions between features
- [ ] Back navigation confirmation flow

### Accessibility & Performance
- [ ] Screen reader interaction patterns
- [ ] Keyboard navigation support
- [ ] Haptic feedback integration
- [ ] Animation performance optimization
- [ ] Reduced motion support implemented

---

*These interaction specifications ensure that FlirtCraft's pre-conversation context feature provides an engaging, accessible, and confidence-building experience through carefully crafted animations and feedback patterns.*