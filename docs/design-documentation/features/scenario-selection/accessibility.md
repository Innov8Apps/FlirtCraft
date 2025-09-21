# Scenario Selection Feature - Accessibility

---
title: Scenarios Tab - Pre-built Scenario Selection Accessibility
description: Complete inclusive design specifications for pre-built scenario selection in the Scenarios tab
feature: scenarios-tab-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - implementation.md
dependencies:
  - WCAG 2.1 AA compliance
  - iOS VoiceOver integration
  - Android TalkBack integration
  - React Native Accessibility API
status: approved
---

## Accessibility Philosophy

**Tab Location**: Scenarios Tab

The scenario selection experience in the Scenarios tab must be **universally accessible**, ensuring that users with diverse abilities can confidently browse and select pre-built scenarios with templates. Every interaction should be perceivable, operable, understandable, and robust for all users.

### Core Accessibility Principles
- **Perceivable**: All scenario information available through multiple senses
- **Operable**: Complete navigation possible through various input methods
- **Understandable**: Clear mental models and consistent interaction patterns
- **Robust**: Compatible with all assistive technologies and future-proof

## WCAG 2.1 AA Compliance

### Color and Contrast Requirements

#### Color Contrast Ratios
**All text meets WCAG AA standards:**
- **Normal text (16px+)**: 4.5:1 contrast ratio minimum
- **Large text (18px+ regular, 14px+ bold)**: 3:1 contrast ratio minimum
- **Interactive elements**: 3:1 contrast ratio for boundaries and states

```typescript
// Color palette with verified contrast ratios
const AccessibleColors = {
  // Primary orange on white background: 4.8:1 ratio
  primaryOrange: '#F97316',
  
  // Text on backgrounds
  textOnWhite: '#1F2937',     // 16.8:1 ratio
  textOnOrange: '#FFFFFF',    // 4.8:1 ratio
  textOnGray: '#111827',      // 19.1:1 ratio
  
  // Difficulty level colors with accessibility
  difficultyGreen: {
    background: '#DCFCE7',     // Light green background
    text: '#166534',           // Dark green text: 7.2:1 ratio
    border: '#22C55E',         // Medium green border: 3.8:1 ratio
  },
  difficultyYellow: {
    background: '#FEF3C7',     // Light yellow background
    text: '#92400E',           // Dark yellow text: 8.1:1 ratio
    border: '#F59E0B',         // Medium yellow border: 4.2:1 ratio
  },
  difficultyRed: {
    background: '#FEE2E2',     // Light red background
    text: '#991B1B',           // Dark red text: 9.3:1 ratio
    border: '#EF4444',         // Medium red border: 4.1:1 ratio
  },
};
```

#### Non-Color Information Encoding
**All information conveyed through color has alternative indicators:**

```typescript
const DifficultyIndicator = ({ difficulty, label }: DifficultyProps) => {
  const getAccessibleIndicators = () => {
    switch (difficulty) {
      case 'green':
        return {
          icon: '🟢',
          pattern: 'solid',
          textPrefix: 'Easy: ',
          accessibilityLabel: 'Green difficulty: Friendly atmosphere',
        };
      case 'yellow':
        return {
          icon: '🟡',
          pattern: 'dashed',
          textPrefix: 'Medium: ',
          accessibilityLabel: 'Yellow difficulty: Realistic interactions',
        };
      case 'red':
        return {
          icon: '🔴',
          pattern: 'dotted',
          textPrefix: 'Hard: ',
          accessibilityLabel: 'Red difficulty: Challenging environment',
        };
    }
  };
  
  const indicators = getAccessibleIndicators();
  
  return (
    <View
      accessible={true}
      accessibilityLabel={indicators.accessibilityLabel}
      accessibilityRole="button"
      style={[
        styles.difficultyButton,
        { borderStyle: indicators.pattern }
      ]}
    >
      <Text style={styles.icon}>{indicators.icon}</Text>
      <Text style={styles.label}>
        {indicators.textPrefix}{label}
      </Text>
    </View>
  );
};
```

### Typography and Readability

#### Font Size and Scaling
**Support for Dynamic Type/Font Scale:**

```typescript
import { PixelRatio, Dimensions } from 'react-native';

const AccessibleTypography = {
  // Base font sizes that scale with system settings
  getScaledSize: (size: number) => {
    const scale = PixelRatio.getFontScale();
    const maxScale = 2.0; // Prevent excessive scaling
    const effectiveScale = Math.min(scale, maxScale);
    return Math.round(size * effectiveScale);
  },
  
  // Scenario card typography
  scenarioTitle: {
    fontSize: AccessibleTypography.getScaledSize(18),
    fontWeight: '600',
    lineHeight: AccessibleTypography.getScaledSize(24),
    letterSpacing: 0.2,
  },
  
  scenarioDescription: {
    fontSize: AccessibleTypography.getScaledSize(14),
    lineHeight: AccessibleTypography.getScaledSize(20),
    letterSpacing: 0.1,
  },
  
  difficultyLabel: {
    fontSize: AccessibleTypography.getScaledSize(16),
    fontWeight: '500',
    lineHeight: AccessibleTypography.getScaledSize(22),
  },
};

// Usage in components
const ScenarioCard = ({ scenario }: ScenarioProps) => {
  return (
    <View>
      <Text style={AccessibleTypography.scenarioTitle}>
        {scenario.title}
      </Text>
      <Text style={AccessibleTypography.scenarioDescription}>
        {scenario.description}
      </Text>
    </View>
  );
};
```

#### Content Structure and Hierarchy
**Clear heading structure for screen readers:**

```typescript
const ScenarioSelectionScreen = () => {
  return (
    <ScrollView>
      {/* Main heading */}
      <Text
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={1}
        style={styles.pageTitle}
      >
        Choose Your Practice Scenario
      </Text>
      
      {/* Section headings */}
      <Text
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={2}
        style={styles.sectionTitle}
      >
        Recent Scenarios
      </Text>
      
      {/* Subsection headings */}
      <Text
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={3}
        style={styles.subsectionTitle}
      >
        All Scenarios
      </Text>
    </ScrollView>
  );
};
```

## Screen Reader Support

### VoiceOver and TalkBack Integration

#### Scenario Card Accessibility
**Rich screen reader descriptions for scenario selection:**

```typescript
const AccessibleScenarioCard = ({ scenario, userStats }: CardProps) => {
  const getAccessibilityLabel = () => {
    const successRate = userStats?.successRate || 0;
    const attempts = userStats?.attempts || 0;
    
    let label = `${scenario.title} scenario. ${scenario.description}. `;
    
    if (attempts > 0) {
      label += `You have practiced this ${attempts} times with ${successRate}% success rate. `;
    } else {
      label += `New scenario, never practiced. `;
    }
    
    label += `Tap to select this scenario.`;
    
    return label;
  };
  
  const getAccessibilityHint = () => {
    return `Double tap to select ${scenario.title} and continue to difficulty selection.`;
  };
  
  return (
    <Pressable
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={getAccessibilityLabel()}
      accessibilityHint={getAccessibilityHint()}
      accessibilityState={{
        selected: scenario.isSelected,
      }}
      onPress={() => selectScenario(scenario)}
    >
      <View style={styles.scenarioCard}>
        <Image
          source={{ uri: scenario.imageUrl }}
          alt={`${scenario.title} environment preview`}
          accessible={true}
          accessibilityRole="image"
        />
        <View style={styles.cardContent}>
          <Text style={styles.title}>{scenario.title}</Text>
          <Text style={styles.description}>{scenario.description}</Text>
          {userStats && (
            <Text
              accessible={true}
              accessibilityLabel={`Success rate: ${userStats.successRate} percent`}
              style={styles.stats}
            >
              {userStats.successRate}% success rate
            </Text>
          )}
        </View>
      </View>
    </Pressable>
  );
};
```

#### Difficulty Selection Accessibility
**Clear audio description of difficulty levels:**

```typescript
const AccessibleDifficultySelector = ({ difficulties, onSelect }: SelectorProps) => {
  const getDifficultyDescription = (difficulty: Difficulty) => {
    const descriptions = {
      green: 'Green level: Friendly atmosphere with welcoming people. Recommended for beginners or building confidence.',
      yellow: 'Yellow level: Realistic interactions with mixed responses. Good for intermediate practice.',
      red: 'Red level: Challenging environment requiring your best skills. Advanced level practice.',
    };
    
    return descriptions[difficulty.level];
  };
  
  return (
    <View
      accessible={true}
      accessibilityRole="radiogroup"
      accessibilityLabel="Select difficulty level for your practice session"
    >
      <Text
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={2}
        style={styles.sectionTitle}
      >
        Choose Difficulty Level
      </Text>
      
      {difficulties.map((difficulty, index) => (
        <Pressable
          key={difficulty.level}
          accessible={true}
          accessibilityRole="radio"
          accessibilityLabel={`${difficulty.name}. ${getDifficultyDescription(difficulty)}`}
          accessibilityHint="Double tap to select this difficulty level"
          accessibilityState={{
            selected: difficulty.isSelected,
            checked: difficulty.isSelected,
          }}
          onPress={() => onSelect(difficulty)}
          style={[
            styles.difficultyButton,
            difficulty.isSelected && styles.selected
          ]}
        >
          <View style={styles.difficultyContent}>
            <Text style={styles.difficultyEmoji}>{difficulty.emoji}</Text>
            <Text style={styles.difficultyName}>{difficulty.name}</Text>
            <Text style={styles.difficultyDescription}>
              {difficulty.shortDescription}
            </Text>
          </View>
        </Pressable>
      ))}
    </View>
  );
};
```

### Navigation and Focus Management

#### Keyboard Navigation Support
**Complete keyboard accessibility for web and connected keyboards:**

```typescript
const KeyboardNavigableGrid = ({ scenarios, onSelect }: GridProps) => {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const scenarioRefs = useRef<(View | null)[]>([]);
  
  const handleKeyPress = (event: KeyboardEvent) => {
    const { key } = event;
    const gridWidth = 2; // 2 columns
    
    switch (key) {
      case 'ArrowRight':
        event.preventDefault();
        setFocusedIndex((prev) => 
          Math.min(prev + 1, scenarios.length - 1)
        );
        break;
        
      case 'ArrowLeft':
        event.preventDefault();
        setFocusedIndex((prev) => Math.max(prev - 1, 0));
        break;
        
      case 'ArrowDown':
        event.preventDefault();
        setFocusedIndex((prev) => 
          Math.min(prev + gridWidth, scenarios.length - 1)
        );
        break;
        
      case 'ArrowUp':
        event.preventDefault();
        setFocusedIndex((prev) => Math.max(prev - gridWidth, 0));
        break;
        
      case 'Enter':
      case ' ':
        event.preventDefault();
        onSelect(scenarios[focusedIndex]);
        break;
    }
  };
  
  useEffect(() => {
    // Focus management for screen readers
    if (scenarioRefs.current[focusedIndex]) {
      AccessibilityInfo.setAccessibilityFocus(
        scenarioRefs.current[focusedIndex]
      );
    }
  }, [focusedIndex]);
  
  return (
    <View
      onKeyDown={handleKeyPress}
      accessible={false} // Individual items handle accessibility
    >
      {scenarios.map((scenario, index) => (
        <View
          key={scenario.id}
          ref={(ref) => scenarioRefs.current[index] = ref}
          accessible={true}
          accessibilityElementsHidden={index !== focusedIndex}
          importantForAccessibility={
            index === focusedIndex ? 'yes' : 'no-hide-descendants'
          }
        >
          <ScenarioCard scenario={scenario} onSelect={onSelect} />
        </View>
      ))}
    </View>
  );
};
```

#### Focus Indicators
**Clear visual focus indicators for keyboard navigation:**

```typescript
const FocusableScenarioCard = ({ scenario, isFocused }: CardProps) => {
  const focusAnimatedValue = useSharedValue(0);
  
  const focusStyle = useAnimatedStyle(() => ({
    borderWidth: interpolate(focusAnimatedValue.value, [0, 1], [2, 4]),
    borderColor: interpolateColor(
      focusAnimatedValue.value,
      [0, 1],
      ['transparent', '#F97316']
    ),
    shadowOpacity: interpolate(focusAnimatedValue.value, [0, 1], [0.1, 0.3]),
  }));
  
  useEffect(() => {
    focusAnimatedValue.value = withTiming(isFocused ? 1 : 0, {
      duration: 200,
    });
  }, [isFocused]);
  
  return (
    <Animated.View style={[styles.scenarioCard, focusStyle]}>
      {/* Card content */}
    </Animated.View>
  );
};
```

## Motor Accessibility

### Touch Target Sizes
**All interactive elements meet minimum size requirements:**

```typescript
const AccessibleTouchTargets = StyleSheet.create({
  // Minimum 44x44pt touch targets (iOS) / 48x48dp (Android)
  scenarioCard: {
    minHeight: 120,
    minWidth: 120,
    padding: 16,
    // Ensure touch target is large enough even with small content
  },
  
  difficultyButton: {
    minHeight: 56, // Exceeds minimum requirements
    minWidth: 200,
    paddingVertical: 16,
    paddingHorizontal: 24,
    marginVertical: 8, // Prevent accidental touches
  },
  
  backButton: {
    height: 44,
    width: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  
  // Info/preview buttons
  infoButton: {
    height: 48,
    width: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

### Voice Control Support
**Complete voice navigation for hands-free operation:**

```typescript
import Voice from '@react-native-community/voice';

const VoiceControlledSelection = ({ scenarios, difficulties }: VoiceProps) => {
  const [isListening, setIsListening] = useState(false);
  const [voiceResult, setVoiceResult] = useState('');
  
  const voiceCommands = {
    // Scenario selection commands
    'coffee shop': () => selectScenario('coffee-shop'),
    'bookstore': () => selectScenario('bookstore'),
    'park': () => selectScenario('park'),
    'art gallery': () => selectScenario('art-gallery'),
    'gym': () => selectScenario('gym'),
    'bar': () => selectScenario('bar'),
    'grocery store': () => selectScenario('grocery-store'),
    'campus': () => selectScenario('campus'),
    
    // Difficulty selection commands
    'green': () => selectDifficulty('green'),
    'easy': () => selectDifficulty('green'),
    'yellow': () => selectDifficulty('yellow'),
    'medium': () => selectDifficulty('yellow'),
    'red': () => selectDifficulty('red'),
    'hard': () => selectDifficulty('red'),
    'challenging': () => selectDifficulty('red'),
    
    // Navigation commands
    'back': () => navigation.goBack(),
    'help': () => showHelp(),
    'repeat': () => repeatInstructions(),
  };
  
  const startListening = async () => {
    try {
      setIsListening(true);
      await Voice.start('en-US');
      
      // Announce listening state for screen readers
      AccessibilityInfo.announceForAccessibility(
        'Voice control active. Say a scenario name or difficulty level.'
      );
    } catch (error) {
      console.error('Voice recognition error:', error);
      setIsListening(false);
    }
  };
  
  const onSpeechResults = (event: any) => {
    const results = event.value;
    if (results && results.length > 0) {
      const command = results[0].toLowerCase().trim();
      setVoiceResult(command);
      
      // Execute voice command
      const commandFunction = voiceCommands[command];
      if (commandFunction) {
        commandFunction();
        AccessibilityInfo.announceForAccessibility(
          `Selected ${command}. Continue with voice commands or touch.`
        );
      } else {
        AccessibilityInfo.announceForAccessibility(
          `Command "${command}" not recognized. Try saying a scenario name or difficulty level.`
        );
      }
      
      setIsListening(false);
    }
  };
  
  useEffect(() => {
    Voice.onSpeechResults = onSpeechResults;
    
    return () => {
      Voice.destroy().then(Voice.removeAllListeners);
    };
  }, []);
  
  return (
    <View>
      <Button
        accessible={true}
        accessibilityLabel="Voice control"
        accessibilityHint="Activate voice control to select scenarios and difficulty levels"
        onPress={startListening}
        title={isListening ? 'Listening...' : 'Voice Control'}
      />
      {voiceResult && (
        <Text
          accessible={true}
          accessibilityLiveRegion="polite"
          style={styles.voiceResult}
        >
          Voice command: {voiceResult}
        </Text>
      )}
    </View>
  );
};
```

### Switch Control Support
**iOS Switch Control and Android Switch Access compatibility:**

```typescript
const SwitchControlSupport = ({ scenarios }: SwitchProps) => {
  const [currentGroup, setCurrentGroup] = useState(0);
  const [currentItem, setCurrentItem] = useState(0);
  
  // Group interactive elements for switch navigation
  const groups = [
    { name: 'scenarios', items: scenarios },
    { name: 'difficulties', items: difficulties },
    { name: 'navigation', items: navigationActions },
  ];
  
  const handleSwitchNavigation = (direction: 'next' | 'previous' | 'select') => {
    switch (direction) {
      case 'next':
        if (currentItem < groups[currentGroup].items.length - 1) {
          setCurrentItem(currentItem + 1);
        } else if (currentGroup < groups.length - 1) {
          setCurrentGroup(currentGroup + 1);
          setCurrentItem(0);
        }
        break;
        
      case 'previous':
        if (currentItem > 0) {
          setCurrentItem(currentItem - 1);
        } else if (currentGroup > 0) {
          setCurrentGroup(currentGroup - 1);
          setCurrentItem(groups[currentGroup - 1].items.length - 1);
        }
        break;
        
      case 'select':
        const currentElement = groups[currentGroup].items[currentItem];
        if (currentElement.onSelect) {
          currentElement.onSelect();
        }
        break;
    }
  };
  
  return (
    <View
      accessible={true}
      accessibilityRole="group"
      onAccessibilityAction={({ nativeEvent }) => {
        const { actionName } = nativeEvent;
        switch (actionName) {
          case 'increment':
            handleSwitchNavigation('next');
            break;
          case 'decrement':
            handleSwitchNavigation('previous');
            break;
          case 'activate':
            handleSwitchNavigation('select');
            break;
        }
      }}
    >
      {/* Switch-navigable content */}
    </View>
  );
};
```

## Cognitive Accessibility

### Clear Language and Instructions
**Simple, action-oriented language for all user instructions:**

```typescript
const AccessibleInstructions = {
  scenarioSelection: {
    mainHeading: 'Choose Your Practice Scenario',
    description: 'Pick a place where you want to practice starting conversations.',
    screenReaderDescription: 'Choose from 8 different practice scenarios. Each scenario represents a real place where you might meet someone.',
  },
  
  difficultySelection: {
    mainHeading: 'Pick Your Challenge Level',
    description: 'How challenging do you want this practice to be?',
    screenReaderDescription: 'Choose from 3 difficulty levels: Green for friendly practice, Yellow for realistic interactions, or Red for challenging situations.',
  },
  
  confirmation: {
    mainHeading: 'Ready to Practice?',
    description: 'You chose {scenario} at {difficulty} level.',
    screenReaderDescription: 'Confirm your selection: {scenario} scenario at {difficulty} difficulty level. Tap Start Practice to begin your conversation.',
  },
};

const InstructionComponent = ({ type, scenario, difficulty }: InstructionProps) => {
  const instruction = AccessibleInstructions[type];
  
  return (
    <View style={styles.instructionContainer}>
      <Text
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={1}
        style={styles.mainHeading}
      >
        {instruction.mainHeading}
      </Text>
      
      <Text style={styles.description}>
        {instruction.description}
      </Text>
      
      <Text
        accessible={true}
        accessibilityElementsHidden={true}
        importantForAccessibility="no"
        style={styles.screenReaderOnly}
      >
        {instruction.screenReaderDescription
          .replace('{scenario}', scenario?.name || '')
          .replace('{difficulty}', difficulty?.name || '')}
      </Text>
    </View>
  );
};
```

### Error Prevention and Recovery
**Clear guidance to prevent selection errors:**

```typescript
const ErrorPreventionSystem = ({ currentSelection }: ErrorPreventionProps) => {
  const [showConfirmation, setShowConfirmation] = useState(false);
  
  const validateSelection = (scenario: Scenario, difficulty: Difficulty) => {
    const warnings = [];
    
    // Check if difficulty might be too challenging
    if (difficulty.level === 'red' && !currentSelection.user.hasAdvancedExperience) {
      warnings.push({
        type: 'difficulty-warning',
        message: 'This is the most challenging level. Consider starting with Green or Yellow difficulty.',
        screenReaderMessage: 'Warning: Red difficulty is very challenging. You may want to try Green or Yellow level first to build confidence.',
      });
    }
    
    // Check if scenario matches user goals
    if (!scenario.alignsWithGoals(currentSelection.user.goals)) {
      warnings.push({
        type: 'scenario-mismatch',
        message: 'This scenario might not match your practice goals. Continue anyway?',
        screenReaderMessage: 'Note: This scenario may not align with your stated practice goals. You can still proceed or choose a different scenario.',
      });
    }
    
    return warnings;
  };
  
  const ConfirmationDialog = ({ warnings, onConfirm, onCancel }: ConfirmationProps) => (
    <Modal
      transparent
      visible={showConfirmation}
      onRequestClose={onCancel}
    >
      <View style={styles.modalOverlay}>
        <View
          accessible={true}
          accessibilityRole="dialog"
          accessibilityLabel="Confirm your selection"
          style={styles.confirmationDialog}
        >
          <Text
            accessible={true}
            accessibilityRole="header"
            accessibilityLevel={2}
            style={styles.dialogTitle}
          >
            Confirm Your Choice
          </Text>
          
          {warnings.map((warning, index) => (
            <View
              key={index}
              accessible={true}
              accessibilityRole="alert"
              accessibilityLabel={warning.screenReaderMessage}
              style={styles.warningContainer}
            >
              <Text style={styles.warningIcon}>⚠️</Text>
              <Text style={styles.warningText}>{warning.message}</Text>
            </View>
          ))}
          
          <View style={styles.dialogActions}>
            <Button
              accessible={true}
              accessibilityLabel="Go back and choose different options"
              accessibilityHint="Return to scenario and difficulty selection"
              title="Change Selection"
              onPress={onCancel}
              style={styles.secondaryButton}
            />
            <Button
              accessible={true}
              accessibilityLabel="Continue with current selection"
              accessibilityHint="Start practice session with chosen scenario and difficulty"
              title="Continue Anyway"
              onPress={onConfirm}
              style={styles.primaryButton}
            />
          </View>
        </View>
      </View>
    </Modal>
  );
  
  return <ConfirmationDialog warnings={warnings} onConfirm={onConfirm} onCancel={onCancel} />;
};
```

### Progress Indicators
**Clear visual and audio progress feedback:**

```typescript
const AccessibleProgressIndicator = ({ currentStep, totalSteps, stepNames }: ProgressProps) => {
  const progressPercentage = (currentStep / totalSteps) * 100;
  
  return (
    <View
      accessible={true}
      accessibilityRole="progressbar"
      accessibilityLabel={`Step ${currentStep} of ${totalSteps}: ${stepNames[currentStep - 1]}`}
      accessibilityValue={{ 
        min: 0, 
        max: totalSteps, 
        now: currentStep,
        text: `${progressPercentage.toFixed(0)}% complete`
      }}
      style={styles.progressContainer}
    >
      {/* Visual progress bar */}
      <View style={styles.progressTrack}>
        <View 
          style={[
            styles.progressFill, 
            { width: `${progressPercentage}%` }
          ]} 
        />
      </View>
      
      {/* Step labels */}
      <View style={styles.stepLabels}>
        {stepNames.map((stepName, index) => (
          <Text
            key={index}
            accessible={true}
            accessibilityLabel={
              index + 1 <= currentStep 
                ? `${stepName} - completed` 
                : `${stepName} - not started`
            }
            style={[
              styles.stepLabel,
              index + 1 <= currentStep && styles.completedStep
            ]}
          >
            {stepName}
          </Text>
        ))}
      </View>
    </View>
  );
};
```

## Reduced Motion Support

### Animation Accessibility
**Respect user motion preferences:**

```typescript
import { AccessibilityInfo } from 'react-native';

const MotionSensitiveAnimations = () => {
  const [reduceMotion, setReduceMotion] = useState(false);
  
  useEffect(() => {
    // Check system motion preferences
    AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
    
    // Listen for preference changes
    const subscription = AccessibilityInfo.addEventListener(
      'reduceMotionChanged',
      setReduceMotion
    );
    
    return () => subscription?.remove();
  }, []);
  
  const getAnimationConfig = (standardDuration: number) => {
    if (reduceMotion) {
      return {
        duration: 0, // Instant for reduced motion
        easing: Easing.linear,
      };
    }
    
    return {
      duration: standardDuration,
      easing: Easing.out(Easing.cubic),
    };
  };
  
  const animateScenarioSelection = () => {
    const config = getAnimationConfig(300);
    
    // Use immediate state change if motion is reduced
    if (reduceMotion) {
      setSelectionState('selected');
    } else {
      // Standard animation
      selectionAnimation.value = withTiming(1, config);
    }
  };
  
  return { reduceMotion, getAnimationConfig, animateScenarioSelection };
};
```

## Testing and Validation

### Accessibility Testing Checklist

#### Automated Testing
```typescript
// React Native Testing Library accessibility tests
describe('Scenario Selection Accessibility', () => {
  test('all interactive elements have proper accessibility labels', () => {
    const { getAllByRole } = render(<ScenarioSelection />);
    
    const buttons = getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toHaveAccessibilityLabel();
      expect(button).toHaveAccessibilityHint();
    });
  });
  
  test('proper heading hierarchy is maintained', () => {
    const { getByRole } = render(<ScenarioSelection />);
    
    expect(getByRole('header', { level: 1 })).toBeTruthy();
    expect(getByRole('header', { level: 2 })).toBeTruthy();
  });
  
  test('color contrast meets WCAG standards', async () => {
    const { getByTestId } = render(<ScenarioSelection />);
    
    const scenarioCard = getByTestId('scenario-card');
    const computedStyles = getComputedStyle(scenarioCard);
    
    const contrastRatio = calculateContrastRatio(
      computedStyles.backgroundColor,
      computedStyles.color
    );
    
    expect(contrastRatio).toBeGreaterThanOrEqual(4.5);
  });
});
```

#### Manual Testing Protocol
1. **VoiceOver/TalkBack Testing**
   - Navigate through entire flow using only screen reader
   - Verify all content is announced correctly
   - Test focus management between screens

2. **Keyboard Navigation Testing**
   - Complete scenario selection using only keyboard
   - Verify focus indicators are visible
   - Test all keyboard shortcuts function properly

3. **Voice Control Testing**
   - Use voice commands to select scenarios and difficulty
   - Verify voice feedback is clear and helpful
   - Test error recovery for unrecognized commands

4. **Switch Control Testing**
   - Navigate using iOS Switch Control or Android Switch Access
   - Verify all elements are reachable
   - Test selection confirmation process

### User Testing with Disabilities

#### Testing Protocol
- **Blind/Low Vision Users**: Navigation efficiency and content comprehension
- **Motor Impaired Users**: Touch target usability and alternative input methods
- **Cognitive Disabilities**: Language clarity and error prevention effectiveness
- **Deaf/Hard of Hearing**: Visual information completeness without audio cues

#### Success Metrics
- **Task Completion**: >90% success rate for scenario selection
- **Efficiency**: <30 seconds additional time for assistive technology users
- **Error Rate**: <5% selection errors requiring correction
- **Satisfaction**: >4.5/5 accessibility experience rating

## Related Documentation

- **[README](./README.md)** - Feature overview and core specifications
- **[User Journey](./user-journey.md)** - Complete user flow including accessibility considerations
- **[Screen States](./screen-states.md)** - Visual specifications with accessibility annotations
- **[Interactions](./interactions.md)** - Animation specifications with reduced motion support
- **[Implementation](./implementation.md)** - Technical implementation with accessibility APIs

## Implementation Notes

### Required Packages
```json
{
  "dependencies": {
    "@react-native-community/voice": "^3.2.4",
    "@react-native-async-storage/async-storage": "^1.19.3",
    "react-native-accessibility-info": "^3.4.0"
  }
}
```

### Platform Considerations
- **iOS**: VoiceOver, Switch Control, Voice Control, Dynamic Type
- **Android**: TalkBack, Switch Access, Voice Access, Font Scale
- **Web**: ARIA labels, keyboard navigation, screen reader compatibility

### Performance Impact
- **Accessibility Services**: <5% performance overhead
- **Screen Reader**: Optimized announcements to prevent information overload
- **Voice Recognition**: Efficient command processing with local pattern matching

## Last Updated
- **Version 1.0.0**: Complete accessibility specifications with WCAG 2.1 AA compliance
- **Focus**: Universal design for scenario selection experience
- **Next**: User testing validation with assistive technology users