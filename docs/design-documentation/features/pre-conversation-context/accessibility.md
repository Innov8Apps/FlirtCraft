# Pre-Conversation Context Accessibility Implementation

---
title: Pre-Conversation Context Accessibility Guide
description: Complete accessibility implementation for context generation and review interface
feature: pre-conversation-context
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ./interactions.md
  - ../../accessibility/guidelines.md
dependencies:
  - React Native Accessibility APIs
  - Screen reader optimization
  - Platform accessibility services
status: approved
---

## Overview

The pre-conversation context accessibility implementation ensures all users can successfully prepare for practice conversations through comprehensive scenario review. This guide provides detailed specifications for making context generation, card review, and action selection fully accessible across visual, auditory, motor, and cognitive accessibility needs.

## Screen Reader Support

### Context Generation Loading State

#### Loading Announcement Strategy
**Initial State Communication:**
- **Announcement Pattern**: "Creating your practice scenario. Please wait while we generate your context."
- **Progress Updates**: No specific progress percentages (indeterminate loading)
- **Completion Signal**: "Your scenario is ready. Four context cards are now available for review."
- **Error Handling**: "We're having trouble creating your scenario. Retry options are available."

**Implementation:**
```tsx
import { AccessibilityInfo } from 'react-native';

const ContextGenerationLoading = () => {
  useEffect(() => {
    // Announce loading start
    AccessibilityInfo.announceForAccessibility(
      "Creating your practice scenario. Please wait while we generate your context."
    );
    
    // Announce completion when context loads
    if (contextLoaded) {
      AccessibilityInfo.announceForAccessibility(
        "Your scenario is ready. Four context cards are now available for review."
      );
      
      // Focus first card after announcement
      setTimeout(() => {
        firstCardRef.current?.focus();
      }, 1000);
    }
  }, [contextLoaded]);
  
  return (
    <View
      accessible={true}
      accessibilityRole="progressbar"
      accessibilityLabel="Creating practice scenario"
      accessibilityValue={{ text: "Loading in progress" }}
    >
      {/* Loading content */}
    </View>
  );
};
```

### Context Cards Screen Reader Structure

#### Card Navigation Hierarchy
**Semantic Structure:**
- **Main Container**: Marked as main content region
- **Progress Header**: Navigation landmark with progress indication
- **Card Container**: List role with four context card items
- **Action Area**: Complementary landmark with primary actions

```tsx
const AccessibleContextCards = () => {
  return (
    <View
      accessible={false} // Allow children to be individually accessible
      accessibilityRole="main"
      accessibilityLabel="Practice scenario context review"
    >
      {/* Header with progress */}
      <View
        accessible={true}
        accessibilityRole="header"
        accessibilityLabel={`Context review progress: ${reviewedCards} of 4 cards reviewed`}
      >
        <ProgressHeader />
      </View>
      
      {/* Context cards */}
      <ScrollView
        accessible={false}
        accessibilityLabel="Context cards list"
      >
        {contextCards.map((card, index) => (
          <ContextCardAccessible
            key={card.id}
            card={card}
            index={index}
            total={contextCards.length}
          />
        ))}
      </ScrollView>
      
      {/* Action buttons */}
      <View
        accessible={false}
        accessibilityRole="toolbar"
        accessibilityLabel="Context actions"
      >
        <ActionButtonsAccessible />
      </View>
    </View>
  );
};
```

#### Individual Card Accessibility

**Practice Partner Card:**
```tsx
const PracticePartnerCard = ({ card, index, isExpanded, onToggle }) => {
  const cardRef = useRef();
  
  // Generate descriptive content for screen reader
  const generateAccessibleDescription = () => {
    return `Practice partner details: ${card.ageRange}, ${card.style}. Currently ${card.activity}. ${card.details.join('. ')}.`;
  };
  
  return (
    <View
      ref={cardRef}
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={`Practice partner card, ${index + 1} of 4`}
      accessibilityHint="Double tap to expand or collapse details"
      accessibilityValue={{ 
        text: isExpanded ? "Expanded" : "Collapsed" 
      }}
      onAccessibilityTap={() => onToggle(card.id)}
    >
      <View accessible={true} accessibilityRole="header">
        <Text accessibilityRole="text">Your Practice Partner</Text>
      </View>
      
      <View accessible={true}>
        <Text accessibilityLabel={generateAccessibleDescription()}>
          {/* Visual content */}
        </Text>
      </View>
      
      {isExpanded && (
        <View accessible={true}>
          <Text accessibilityLabel={`Additional details: ${card.expandedContent}`}>
            {/* Expanded content */}
          </Text>
        </View>
      )}
    </View>
  );
};
```

**Environment Card:**
```tsx
const EnvironmentCard = ({ card, index }) => {
  const generateEnvironmentDescription = () => {
    return `Environment details: ${card.timeContext}, ${card.crowdLevel} crowd. Atmosphere: ${card.atmosphere}. Additional details: ${card.details.join(', ')}.`;
  };
  
  return (
    <View
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={`Environment card, ${index + 1} of 4`}
      accessibilityHint="Contains location and atmosphere details"
    >
      <View accessible={true} accessibilityRole="header">
        <Text>Environment & Setting</Text>
      </View>
      
      <View accessible={true}>
        <Text accessibilityLabel={generateEnvironmentDescription()}>
          {/* Content layout */}
        </Text>
      </View>
    </View>
  );
};
```

**Body Language Card:**
```tsx
const BodyLanguageCard = ({ card, index }) => {
  const generateBodyLanguageDescription = () => {
    const signalDescriptions = card.signals.map(signal => 
      `${getSignalAccessibilityLabel(signal.type)}: ${signal.description}`
    ).join('. ');
    
    return `Body language signals: ${signalDescriptions}. Overall assessment: ${card.overall}.`;
  };
  
  const getSignalAccessibilityLabel = (type) => {
    switch (type) {
      case 'positive': return 'Encouraging signal';
      case 'neutral': return 'Neutral signal';
      case 'challenging': return 'Cautious signal';
      default: return 'Mixed signal';
    }
  };
  
  return (
    <View
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={`Body language card, ${index + 1} of 4`}
      accessibilityHint="Contains receptiveness signals and interpretation"
    >
      <View accessible={true} accessibilityRole="header">
        <Text>Body Language Signals</Text>
      </View>
      
      {/* Individual signals with proper labeling */}
      {card.signals.map((signal, signalIndex) => (
        <View
          key={signalIndex}
          accessible={true}
          accessibilityLabel={`${getSignalAccessibilityLabel(signal.type)}: ${signal.description}`}
        >
          <SignalIndicator signal={signal} />
        </View>
      ))}
      
      <View
        accessible={true}
        accessibilityRole="summary"
        accessibilityLabel={`Overall assessment: ${card.overall}`}
      >
        <OverallAssessment content={card.overall} />
      </View>
    </View>
  );
};
```

**Conversation Starters Card:**
```tsx
const ConversationStartersCard = ({ card, index, onStarterSelect }) => {
  const generateStartersDescription = () => {
    const startersList = card.starters.map((starter, i) => 
      `Option ${i + 1}: ${starter}`
    ).join('. ');
    
    return `Conversation starter options: ${startersList}. Tap any starter to select and use it in conversation.`;
  };
  
  return (
    <View
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={`Conversation starters card, ${index + 1} of 4`}
      accessibilityHint="Contains suggested conversation openers"
    >
      <View accessible={true} accessibilityRole="header">
        <Text>Conversation Starters</Text>
      </View>
      
      <View
        accessible={true}
        accessibilityLabel="Tap any starter to select and use it in conversation"
        accessibilityRole="text"
      >
        <Text>Choose one to break the ice, or use as inspiration:</Text>
      </View>
      
      {/* Individual starters as buttons */}
      {card.starters.map((starter, starterIndex) => (
        <Pressable
          key={starterIndex}
          accessible={true}
          accessibilityRole="button"
          accessibilityLabel={`Conversation starter ${starterIndex + 1}: ${starter}`}
          accessibilityHint="Double tap to select this starter for conversation"
          onPress={() => onStarterSelect(starter, starterIndex)}
        >
          <StarterOption starter={starter} index={starterIndex} />
        </Pressable>
      ))}
      
      <View
        accessible={true}
        accessibilityRole="text"
        accessibilityLabel="Tip: You can edit any selected starter before sending it in conversation"
      >
        <TipBox />
      </View>
    </View>
  );
};
```

### Action Buttons Accessibility

#### Primary Action Button
```tsx
const StartConversationButton = ({ disabled, loading, allCardsReviewed, onPress }) => {
  const getAccessibilityLabel = () => {
    if (loading) return "Starting conversation, please wait";
    if (disabled) return "Start conversation button, disabled";
    return "Start conversation";
  };
  
  const getAccessibilityHint = () => {
    if (disabled && !allCardsReviewed) {
      return "Review all context cards before starting conversation";
    }
    return "Double tap to begin practice conversation with AI partner";
  };
  
  return (
    <Pressable
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={getAccessibilityLabel()}
      accessibilityHint={getAccessibilityHint()}
      accessibilityState={{ disabled }}
      onPress={onPress}
    >
      <ButtonContent disabled={disabled} loading={loading} />
    </Pressable>
  );
};
```

#### Secondary Action Buttons
```tsx
const RegenerateButton = ({ loading, onPress }) => {
  return (
    <Pressable
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={loading ? "Generating new context" : "Generate new context"}
      accessibilityHint={loading ? "Please wait while new scenario is created" : "Double tap to create different scenario details"}
      accessibilityState={{ disabled: loading }}
      onPress={onPress}
    >
      <RegenerateButtonContent loading={loading} />
    </Pressable>
  );
};

const BackButton = ({ onPress }) => {
  return (
    <Pressable
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel="Back to scenario selection"
      accessibilityHint="Double tap to return to scenario and difficulty selection"
      onPress={onPress}
    >
      <BackButtonContent />
    </Pressable>
  );
};
```

### Dynamic Content Announcements

#### Context Regeneration Announcements
```tsx
const ContextRegenerationAccessibility = () => {
  const [isRegenerating, setIsRegenerating] = useState(false);
  
  const handleRegeneration = async () => {
    setIsRegenerating(true);
    
    // Announce start of regeneration
    AccessibilityInfo.announceForAccessibility(
      "Generating new context. Please wait while we create different scenario details."
    );
    
    try {
      const newContext = await regenerateContext();
      
      // Announce completion
      AccessibilityInfo.announceForAccessibility(
        "New context generated successfully. Updated scenario cards are now available for review."
      );
      
      // Focus first card after regeneration
      setTimeout(() => {
        firstCardRef.current?.focus();
      }, 500);
      
    } catch (error) {
      // Announce error
      AccessibilityInfo.announceForAccessibility(
        "Context generation failed. Please try again or return to scenario selection."
      );
    } finally {
      setIsRegenerating(false);
    }
  };
  
  return { handleRegeneration, isRegenerating };
};
```

## Keyboard Navigation

### Desktop Web Keyboard Support

#### Tab Order Management
**Navigation Sequence:**
1. **Skip to main content** link (hidden, appears on focus)
2. **Back button** (header)
3. **Help button** (header)
4. **Context cards** (as a group or individually navigable)
5. **Start conversation** button (primary action)
6. **Generate new context** button (secondary)
7. **Back to scenarios** button (tertiary)

```tsx
const KeyboardNavigationManager = () => {
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const elementRefs = useRef([]);
  
  const handleKeyDown = (event) => {
    switch (event.key) {
      case 'Tab':
        // Natural tab order handled by accessibility structure
        break;
        
      case 'Enter':
      case ' ':
        event.preventDefault();
        activateCurrentElement();
        break;
        
      case 'Escape':
        handleBackNavigation();
        break;
        
      case 'ArrowDown':
        // Navigate to next card
        if (focusedIndex < contextCards.length - 1) {
          event.preventDefault();
          focusCard(focusedIndex + 1);
        }
        break;
        
      case 'ArrowUp':
        // Navigate to previous card
        if (focusedIndex > 0) {
          event.preventDefault();
          focusCard(focusedIndex - 1);
        }
        break;
    }
  };
  
  const focusCard = (index) => {
    setFocusedIndex(index);
    elementRefs.current[index]?.focus();
  };
  
  return (
    <View onKeyDown={handleKeyDown}>
      {/* Keyboard accessible interface */}
    </View>
  );
};
```

#### Skip Navigation Links
```tsx
const SkipNavigationLinks = () => {
  return (
    <>
      <Pressable
        accessible={true}
        accessibilityRole="link"
        accessibilityLabel="Skip to main content"
        style={styles.skipLink}
        onPress={() => mainContentRef.current?.focus()}
      >
        <Text>Skip to main content</Text>
      </Pressable>
      
      <Pressable
        accessible={true}
        accessibilityRole="link"
        accessibilityLabel="Skip to actions"
        style={styles.skipLink}
        onPress={() => actionsRef.current?.focus()}
      >
        <Text>Skip to actions</Text>
      </Pressable>
    </>
  );
};

const styles = StyleSheet.create({
  skipLink: {
    position: 'absolute',
    left: -10000,
    top: 'auto',
    width: 1,
    height: 1,
    overflow: 'hidden',
    // Show when focused
    ':focus': {
      position: 'static',
      width: 'auto',
      height: 'auto',
      overflow: 'visible',
    },
  },
});
```

### Mobile Screen Reader Navigation

#### iOS VoiceOver Optimization
```tsx
const VoiceOverOptimizedCard = ({ card, index }) => {
  return (
    <View
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={`${card.title} card`}
      accessibilityHint={`Card ${index + 1} of ${totalCards}. ${card.hint}`}
      // Custom actions for VoiceOver
      accessibilityActions={[
        { name: 'expand', label: 'Expand details' },
        { name: 'next', label: 'Next card' },
        { name: 'previous', label: 'Previous card' },
      ]}
      onAccessibilityAction={(event) => {
        switch (event.nativeEvent.actionName) {
          case 'expand':
            toggleCardExpansion(card.id);
            break;
          case 'next':
            focusNextCard();
            break;
          case 'previous':
            focusPreviousCard();
            break;
        }
      }}
    >
      {/* Card content */}
    </View>
  );
};
```

#### Android TalkBack Optimization
```tsx
const TalkBackOptimizedInterface = () => {
  return (
    <ScrollView
      accessible={false} // Let children handle accessibility
      accessibilityLiveRegion="polite" // Announce dynamic changes
    >
      {contextCards.map((card, index) => (
        <View
          key={card.id}
          accessible={true}
          accessibilityRole="region"
          accessibilityLiveRegion="polite"
          importantForAccessibility="yes"
        >
          <ContextCard card={card} index={index} />
        </View>
      ))}
    </ScrollView>
  );
};
```

## Visual Accessibility

### High Contrast Support

#### Color Contrast Enhancements
**Text Contrast Requirements:**
- **Card Headers**: Dark gray text (`#1F2937`) on white background - 16.1:1 ratio
- **Body Text**: Medium gray text (`#374151`) on white background - 11.2:1 ratio
- **Button Text**: White text (`#FFFFFF`) on orange background (`#F97316`) - 4.8:1 ratio
- **Signal Indicators**: High contrast color coding with pattern alternatives

```tsx
const HighContrastCard = ({ card, highContrastMode }) => {
  const getHighContrastStyles = () => {
    if (!highContrastMode) return styles.default;
    
    return {
      backgroundColor: '#FFFFFF',
      borderWidth: 2,
      borderColor: '#000000',
      padding: 20,
    };
  };
  
  const getHighContrastTextColor = (type) => {
    if (!highContrastMode) return styles.defaultText;
    
    return {
      color: type === 'header' ? '#000000' : '#1F2937',
      fontWeight: type === 'header' ? 'bold' : 'normal',
    };
  };
  
  return (
    <View style={[styles.card, getHighContrastStyles()]}>
      <Text style={[styles.header, getHighContrastTextColor('header')]}>
        {card.title}
      </Text>
      <Text style={[styles.content, getHighContrastTextColor('content')]}>
        {card.content}
      </Text>
    </View>
  );
};
```

#### Color-Independent Signaling
**Body Language Signals with Pattern Alternatives:**
```tsx
const AccessibleSignalIndicator = ({ signal, highContrastMode }) => {
  const getSignalPattern = (type) => {
    switch (type) {
      case 'positive':
        return { symbol: '✓', pattern: 'solid', ariaLabel: 'Positive signal' };
      case 'neutral':
        return { symbol: '—', pattern: 'dashed', ariaLabel: 'Neutral signal' };
      case 'challenging':
        return { symbol: '!', pattern: 'dotted', ariaLabel: 'Cautious signal' };
      default:
        return { symbol: '?', pattern: 'none', ariaLabel: 'Mixed signal' };
    }
  };
  
  const pattern = getSignalPattern(signal.type);
  
  return (
    <View
      accessible={true}
      accessibilityLabel={`${pattern.ariaLabel}: ${signal.description}`}
      style={[
        styles.signalIndicator,
        { borderStyle: pattern.pattern },
        highContrastMode && styles.highContrastBorder
      ]}
    >
      <Text style={styles.signalSymbol}>{pattern.symbol}</Text>
      <Text style={styles.signalText}>{signal.description}</Text>
    </View>
  );
};
```

### Text Scaling Support

#### Dynamic Type Integration
```tsx
const ScalableText = ({ children, style, maxFontSizeMultiplier = 1.3, ...props }) => {
  return (
    <Text
      {...props}
      style={style}
      maxFontSizeMultiplier={maxFontSizeMultiplier}
      allowFontScaling={true}
    >
      {children}
    </Text>
  );
};

const AdaptiveCardLayout = ({ card, fontScale }) => {
  const getAdaptiveStyles = () => {
    return {
      padding: Math.max(16, 16 * fontScale),
      marginBottom: Math.max(12, 12 * fontScale),
      minHeight: 100 * Math.min(fontScale, 1.5), // Cap scaling for layout
    };
  };
  
  return (
    <View style={[styles.card, getAdaptiveStyles()]}>
      <ScalableText style={styles.title}>
        {card.title}
      </ScalableText>
      <ScalableText style={styles.content}>
        {card.content}
      </ScalableText>
    </View>
  );
};
```

#### Layout Adaptation for Large Text
```tsx
const TextScaleAwareLayout = () => {
  const { fontScale } = useWindowDimensions();
  const isLargeText = fontScale > 1.2;
  
  return (
    <View style={isLargeText ? styles.largeTextLayout : styles.defaultLayout}>
      {/* Adapted layout for large text */}
      <ScrollView contentContainerStyle={isLargeText && styles.largeTextContainer}>
        {contextCards.map((card, index) => (
          <AdaptiveCard key={card.id} card={card} isLargeText={isLargeText} />
        ))}
      </ScrollView>
    </View>
  );
};
```

## Motion and Animation Accessibility

### Reduced Motion Support

#### Animation Preferences Detection
```tsx
const useReducedMotion = () => {
  const [reduceMotion, setReduceMotion] = useState(false);
  
  useEffect(() => {
    // Check system preference
    AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
    
    // Listen for changes
    const listener = AccessibilityInfo.addEventListener(
      'reduceMotionChanged',
      setReduceMotion
    );
    
    return () => listener?.remove();
  }, []);
  
  return reduceMotion;
};
```

#### Motion-Sensitive Alternatives
```tsx
const AccessibleCardAnimation = ({ card, index, trigger }) => {
  const reduceMotion = useReducedMotion();
  const opacity = useSharedValue(0);
  const translateY = useSharedValue(reduceMotion ? 0 : 30);
  
  useEffect(() => {
    if (trigger) {
      if (reduceMotion) {
        // Instant appearance with focus announcement
        opacity.value = 1;
        translateY.value = 0;
        
        // Announce appearance for screen readers
        AccessibilityInfo.announceForAccessibility(
          `${card.title} card is now available for review`
        );
      } else {
        // Standard animation
        opacity.value = withDelay(
          index * 100,
          withTiming(1, { duration: 400 })
        );
        translateY.value = withDelay(
          index * 100,
          withSpring(0)
        );
      }
    }
  }, [trigger, reduceMotion]);
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateY: translateY.value }],
  }));
  
  return (
    <Animated.View style={animatedStyle}>
      <ContextCard card={card} />
    </Animated.View>
  );
};
```

### Vestibular Disorder Considerations

#### Safe Animation Parameters
```tsx
const VestibularSafeAnimations = {
  // Avoid parallax effects
  disableParallax: true,
  
  // Limit rotation animations
  maxRotation: 5, // degrees
  
  // Gentle scaling only
  scaleRange: [0.98, 1.02],
  
  // Linear motion paths
  useLinearTransitions: true,
  
  // Slower animation speeds
  safeDuration: 600, // ms minimum
};
```

## Cognitive Accessibility

### Information Processing Support

#### Content Organization for Cognitive Load
```tsx
const CognitivelyAccessibleCard = ({ card }) => {
  return (
    <View
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={`${card.title} information`}
    >
      {/* Clear heading hierarchy */}
      <View accessible={true} accessibilityRole="header">
        <Text style={styles.clearHeading}>{card.title}</Text>
      </View>
      
      {/* Summary first for overview */}
      <View accessible={true} accessibilityRole="summary">
        <Text style={styles.summary}>{card.summary}</Text>
      </View>
      
      {/* Detailed information in logical order */}
      <View accessible={true}>
        {card.details.map((detail, index) => (
          <View key={index} style={styles.detailItem}>
            <Text style={styles.detailText}>{detail}</Text>
          </View>
        ))}
      </View>
      
      {/* Clear action if applicable */}
      {card.action && (
        <View accessible={true} accessibilityRole="button">
          <Text style={styles.actionText}>{card.action}</Text>
        </View>
      )}
    </View>
  );
};
```

#### Reading Time and Pacing Control
```tsx
const PacingControlledInterface = () => {
  const [userControlledPacing, setUserControlledPacing] = useState(true);
  
  return (
    <View>
      {/* No automatic timeouts or forced progression */}
      <ScrollView
        // User controls scrolling speed
        decelerationRate="normal"
        scrollEventThrottle={16}
      >
        {contextCards.map((card, index) => (
          <View key={card.id}>
            <CognitivelyAccessibleCard card={card} />
            
            {/* Optional reading confirmation */}
            <Pressable
              accessible={true}
              accessibilityRole="button"
              accessibilityLabel={`Mark ${card.title} as reviewed`}
              accessibilityHint="Optional: Confirm you've finished reading this card"
              onPress={() => markCardAsReviewed(card.id)}
            >
              <Text>✓ I've reviewed this section</Text>
            </Pressable>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};
```

### Error Prevention and Recovery

#### Clear Error Communication
```tsx
const AccessibleErrorHandling = ({ error, onRetry, onFallback }) => {
  // Announce errors immediately
  useEffect(() => {
    if (error) {
      AccessibilityInfo.announceForAccessibility(
        `Error: ${error.message}. Recovery options are available.`
      );
    }
  }, [error]);
  
  return (
    <View
      accessible={true}
      accessibilityRole="alert"
      accessibilityLiveRegion="assertive"
    >
      <View accessible={true} accessibilityRole="heading">
        <Text style={styles.errorTitle}>Something went wrong</Text>
      </View>
      
      <View accessible={true}>
        <Text style={styles.errorMessage}>{error.message}</Text>
      </View>
      
      <View style={styles.recoveryOptions}>
        <Pressable
          accessible={true}
          accessibilityRole="button"
          accessibilityLabel="Try generating context again"
          accessibilityHint="This will attempt to create your scenario context again"
          onPress={onRetry}
        >
          <Text>Try Again</Text>
        </Pressable>
        
        <Pressable
          accessible={true}
          accessibilityRole="button"
          accessibilityLabel="Use a pre-written scenario"
          accessibilityHint="This will load a ready-made scenario for your selected difficulty"
          onPress={onFallback}
        >
          <Text>Use Quick Scenario</Text>
        </Pressable>
      </View>
    </View>
  );
};
```

## Platform-Specific Accessibility

### iOS Accessibility Features

#### VoiceOver Custom Actions
```tsx
const iOSAccessibleCard = ({ card, onExpand, onNext, onPrevious }) => {
  return (
    <View
      accessible={true}
      accessibilityRole="region"
      accessibilityLabel={card.title}
      accessibilityActions={[
        { name: 'expand', label: 'Show more details' },
        { name: 'next', label: 'Next card' },
        { name: 'previous', label: 'Previous card' },
        { name: 'magicTap', label: 'Start conversation' }, // Global action
      ]}
      onAccessibilityAction={(event) => {
        switch (event.nativeEvent.actionName) {
          case 'expand':
            onExpand(card.id);
            break;
          case 'next':
            onNext();
            break;
          case 'previous':
            onPrevious();
            break;
          case 'magicTap':
            handleStartConversation();
            break;
        }
      }}
    >
      {/* Card content */}
    </View>
  );
};
```

#### Switch Control Support
```tsx
const SwitchControlOptimized = () => {
  return (
    <View>
      {/* Grouped related controls */}
      <View accessibilityRole="group" accessibilityLabel="Context review">
        {contextCards.map((card) => (
          <SwitchControlCard key={card.id} card={card} />
        ))}
      </View>
      
      {/* Grouped action controls */}
      <View accessibilityRole="group" accessibilityLabel="Actions">
        <StartConversationButton />
        <RegenerateButton />
        <BackButton />
      </View>
    </View>
  );
};
```

### Android Accessibility Features

#### TalkBack Optimizations
```xml
<!-- Android-specific accessibility attributes -->
<View
  android:contentDescription="Practice partner context card"
  android:accessibilityHeading="true"
  android:accessibilityLiveRegion="polite"
  android:importantForAccessibility="yes"
/>
```

```tsx
const AndroidAccessibleCard = ({ card }) => {
  return (
    <View
      accessibilityRole="region"
      accessibilityLiveRegion="polite"
      accessibilityLabel={card.title}
      // Android-specific props
      importantForAccessibility="yes"
      accessibilityComponentType="button" // If interactive
    >
      {/* Card content with proper labeling */}
    </View>
  );
};
```

## Testing and Validation

### Accessibility Testing Protocol

#### Automated Testing
```tsx
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Pre-Conversation Context Accessibility', () => {
  test('context cards meet accessibility standards', async () => {
    const { container } = render(<PreConversationContext />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  test('screen reader announcements work correctly', () => {
    const mockAnnounce = jest.spyOn(AccessibilityInfo, 'announceForAccessibility');
    
    render(<ContextGenerationLoading />);
    
    expect(mockAnnounce).toHaveBeenCalledWith(
      'Creating your practice scenario. Please wait while we generate your context.'
    );
  });
  
  test('keyboard navigation follows logical order', () => {
    const { container } = render(<PreConversationContext />);
    const focusableElements = getFocusableElements(container);
    
    // Test tab order
    expect(focusableElements[0]).toHaveAttribute('aria-label', 'Skip to main content');
    expect(focusableElements[1]).toHaveAttribute('aria-label', 'Return to scenario selection');
    // ... continue testing tab order
  });
});
```

#### Manual Testing Checklist
- [ ] **Screen Reader Navigation**: Complete flow with VoiceOver/TalkBack
- [ ] **Keyboard Only**: All functionality accessible via keyboard
- [ ] **High Contrast Mode**: Interface usable in high contrast
- [ ] **Text Scaling**: Layout maintains usability at 200% text scale
- [ ] **Reduced Motion**: Alternative feedback works when animations disabled
- [ ] **Voice Control**: Major actions work with voice commands
- [ ] **Switch Control**: Interface navigable with switch control

### User Testing with Accessibility Focus

#### Testing Scenarios
1. **Screen Reader User**: Complete context review and conversation start
2. **Keyboard User**: Navigate through all cards and actions using only keyboard
3. **Low Vision User**: Use interface with high contrast and magnification
4. **Motor Impairment**: Interact with interface using switch control or voice
5. **Cognitive Disability**: Process information and complete tasks without time pressure

---

## Related Documentation

- [Pre-Conversation Context README](./README.md) - Complete feature overview
- [User Journey](./user-journey.md) - User flow with accessibility considerations
- [Screen States](./screen-states.md) - Visual specifications with accessibility notes
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Project-wide accessibility standards

## Implementation Checklist

### Screen Reader Support
- [ ] Context generation loading announcements
- [ ] Card navigation with proper hierarchy
- [ ] Dynamic content announcements
- [ ] Action button accessibility labels
- [ ] Error state announcements

### Keyboard Navigation
- [ ] Logical tab order through interface
- [ ] Skip navigation links implemented
- [ ] Keyboard shortcuts for common actions
- [ ] Focus management during state changes
- [ ] Escape key handling for modal dismissal

### Visual Accessibility
- [ ] High contrast mode support
- [ ] Color-independent information conveyance
- [ ] Text scaling up to 200% support
- [ ] Focus indicators clearly visible
- [ ] Alternative text for all visual elements

### Motion Accessibility
- [ ] Reduced motion preference detection
- [ ] Alternative feedback for motion-sensitive users
- [ ] Vestibular-safe animation parameters
- [ ] Option to disable all animations

### Cognitive Accessibility
- [ ] Clear information hierarchy
- [ ] No time pressure on user actions
- [ ] Simple, clear language throughout
- [ ] Consistent interaction patterns
- [ ] Error recovery guidance provided

---

*This accessibility implementation ensures that FlirtCraft's pre-conversation context feature is usable by all users, providing equal access to the confidence-building scenario preparation experience.*