# Unified Selection Feature - Implementation

---
title: Chat Tab - Unified Selection Implementation Specifications
description: Technical specifications and developer handoff for the Chat tab unified location and difficulty selection screen
feature: chat-unified-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - accessibility.md
dependencies:
  - React Native
  - NativeBase
  - React Native Reanimated 3
  - React Native Gesture Handler
status: approved
---

## Implementation Overview

**Tab Location**: Chat Tab

The unified selection screen in the Chat tab combines horizontal location browsing with difficulty selection in a single, performant interface. After selection, the app proceeds to AI-generated randomized context based on these choices. This implementation guide provides complete technical specifications for the React Native development team.

## Technology Stack Requirements

### Core Dependencies
- **React Native**: 0.72+ (for latest performance optimizations)
- **NativeBase**: 3.4+ (consistent UI components)
- **React Native Reanimated**: 3.0+ (smooth animations)
- **React Native Gesture Handler**: 2.12+ (carousel interactions)
- **React Native Fast Image**: 8.6+ (optimized image loading)

### Development Dependencies
- **TypeScript**: 5.0+ (type safety)
- **ESLint**: Accessibility plugin enabled
- **Testing Library**: React Native Testing Library
- **Flipper**: Performance debugging (development only)

## Component Architecture

### File Structure
```
src/
├── components/
│   └── unified-selection/
│       ├── UnifiedSelectionScreen.tsx          # Main screen component
│       ├── LocationCarousel.tsx                # Horizontal location scroll
│       ├── LocationCard.tsx                    # Individual location card
│       ├── DifficultySelection.tsx             # Bottom difficulty section
│       ├── DifficultyCard.tsx                  # Individual difficulty card
│       ├── CreateScenarioButton.tsx            # Action button component
│       └── types.ts                            # TypeScript interfaces
├── hooks/
│   ├── useLocationSelection.ts                 # Location state management
│   ├── useDifficultySelection.ts               # Difficulty state management
│   └── useSelectionValidation.ts               # Combined validation logic
├── constants/
│   ├── locations.ts                            # Location data and images
│   └── difficulties.ts                         # Difficulty configurations
└── utils/
    ├── imageOptimization.ts                    # Image loading utilities
    └── accessibility.ts                        # Accessibility helpers
```

## Data Models and Types

### TypeScript Interfaces
```typescript
// Core data types
export interface Location {
  id: string;
  name: string;
  description: string;
  imageUrl: string;
  imageAlt: string;
  category: 'social' | 'activity' | 'cultural' | 'everyday';
}

export interface Difficulty {
  id: string;
  name: string;
  level: 'green' | 'yellow' | 'red';
  title: string;
  description: string;
  detailedDescription: string;
  successRate: string;
  gradient: [string, string];
  selectionColor: string;
  icon: React.ComponentType;
}

// Component state types
export interface SelectionState {
  selectedLocation: Location | null;
  selectedDifficulty: Difficulty | null;
  isValidForCreation: boolean;
}

// Animation state types
export interface AnimationState {
  locationScale: Animated.SharedValue<number>;
  difficultyScale: Animated.SharedValue<number>;
  buttonOpacity: Animated.SharedValue<number>;
}
```

### Static Data Configuration
```typescript
// constants/locations.ts
export const LOCATIONS: Location[] = [
  {
    id: 'coffee-shop',
    name: 'Coffee Shop',
    description: 'Casual and relaxed conversations',
    imageUrl: require('../../assets/images/locations/coffee-shop.jpg'),
    imageAlt: 'Warm coffee shop interior with natural lighting and comfortable seating',
    category: 'social'
  },
  {
    id: 'bar-lounge',
    name: 'Bar & Lounge',
    description: 'Social nightlife interactions',
    imageUrl: require('../../assets/images/locations/bar-lounge.jpg'),
    imageAlt: 'Upscale bar environment with ambient lighting and social atmosphere',
    category: 'social'
  },
  // ... remaining locations
];

// constants/difficulties.ts
export const DIFFICULTIES: Difficulty[] = [
  {
    id: 'friendly',
    name: 'Friendly',
    level: 'green',
    title: 'Friendly',
    description: 'Open and encouraging',
    detailedDescription: 'Practice partner is welcoming and receptive to conversation',
    successRate: '85% success rate',
    gradient: ['#10B981', '#047857'],
    selectionColor: '#065F46',
    icon: SmileIcon
  },
  // ... remaining difficulties
];
```

## Core Component Implementation

### Main Screen Component
```typescript
// UnifiedSelectionScreen.tsx
import React, { useState, useCallback } from 'react';
import { Box, VStack, HStack } from 'native-base';
import { useNavigation } from '@react-navigation/native';
import { LocationCarousel } from './LocationCarousel';
import { DifficultySelection } from './DifficultySelection';
import { CreateScenarioButton } from './CreateScenarioButton';
import { useLocationSelection } from '../hooks/useLocationSelection';
import { useDifficultySelection } from '../hooks/useDifficultySelection';
import { useSelectionValidation } from '../hooks/useSelectionValidation';

export const UnifiedSelectionScreen: React.FC = () => {
  const navigation = useNavigation();
  
  // State management hooks
  const { 
    selectedLocation, 
    selectLocation, 
    clearLocationSelection 
  } = useLocationSelection();
  
  const { 
    selectedDifficulty, 
    selectDifficulty, 
    clearDifficultySelection 
  } = useDifficultySelection();
  
  const { isValidForCreation } = useSelectionValidation(
    selectedLocation, 
    selectedDifficulty
  );

  const handleCreateScenario = useCallback(async () => {
    if (!isValidForCreation) return;
    
    try {
      // Pass selection data to context creation
      navigation.navigate('ChatContext', {
        location: selectedLocation,
        difficulty: selectedDifficulty
      });
    } catch (error) {
      console.error('Navigation error:', error);
    }
  }, [navigation, selectedLocation, selectedDifficulty, isValidForCreation]);

  return (
    <Box flex={1} bg="white" safeArea>
      {/* Header Section */}
      <VStack space={2} px={4} py={3} borderBottomWidth={1} borderBottomColor="gray.100">
        <Text fontSize="xl" fontWeight="semibold" textAlign="center">
          Create Your Practice Session
        </Text>
        <Text fontSize="sm" color="gray.500" textAlign="center">
          Choose location and difficulty level
        </Text>
      </VStack>

      {/* Location Selection Section */}
      <Box flex={0.6} bg="gray.50" py={6}>
        <LocationCarousel
          selectedLocation={selectedLocation}
          onLocationSelect={selectLocation}
        />
      </Box>

      {/* Difficulty Selection Section */}
      <Box flex={0.3} px={4} py={5} borderTopWidth={1} borderTopColor="gray.100">
        <DifficultySelection
          selectedDifficulty={selectedDifficulty}
          onDifficultySelect={selectDifficulty}
        />
      </Box>

      {/* Action Section */}
      <Box flex={0.1} px={4} py={3} justifyContent="center">
        <CreateScenarioButton
          isEnabled={isValidForCreation}
          onPress={handleCreateScenario}
        />
      </Box>
    </Box>
  );
};
```

### Location Carousel Implementation
```typescript
// LocationCarousel.tsx
import React, { useRef } from 'react';
import { ScrollView, Dimensions } from 'react-native';
import { Box, HStack } from 'native-base';
import Animated, { 
  useSharedValue, 
  useAnimatedScrollHandler,
  interpolate 
} from 'react-native-reanimated';
import { LocationCard } from './LocationCard';
import { LOCATIONS } from '../constants/locations';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const CARD_WIDTH = 280;
const CARD_SPACING = 16;
const SIDE_PADDING = 48;

interface Props {
  selectedLocation: Location | null;
  onLocationSelect: (location: Location) => void;
}

export const LocationCarousel: React.FC<Props> = ({
  selectedLocation,
  onLocationSelect
}) => {
  const scrollX = useSharedValue(0);
  const scrollViewRef = useRef<ScrollView>(null);

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollX.value = event.contentOffset.x;
    }
  });

  return (
    <Box height={180}>
      <Animated.ScrollView
        ref={scrollViewRef}
        horizontal
        showsHorizontalScrollIndicator={false}
        snapToInterval={CARD_WIDTH + CARD_SPACING}
        snapToAlignment="center"
        decelerationRate="fast"
        contentInset={{ left: SIDE_PADDING, right: SIDE_PADDING }}
        contentOffset={{ x: -SIDE_PADDING, y: 0 }}
        onScroll={scrollHandler}
        scrollEventThrottle={16}
      >
        <HStack space={CARD_SPACING} px={SIDE_PADDING}>
          {LOCATIONS.map((location, index) => (
            <LocationCard
              key={location.id}
              location={location}
              isSelected={selectedLocation?.id === location.id}
              onSelect={onLocationSelect}
              index={index}
              scrollX={scrollX}
            />
          ))}
        </HStack>
      </Animated.ScrollView>
    </Box>
  );
};
```

### Individual Location Card
```typescript
// LocationCard.tsx
import React from 'react';
import { Pressable, ImageBackground } from 'react-native';
import { Box, Text } from 'native-base';
import Animated, { 
  useAnimatedStyle, 
  useSharedValue,
  withSpring,
  withTiming,
  interpolate
} from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import FastImage from 'react-native-fast-image';

const CARD_WIDTH = 280;
const CARD_HEIGHT = 180;

interface Props {
  location: Location;
  isSelected: boolean;
  onSelect: (location: Location) => void;
  index: number;
  scrollX: Animated.SharedValue<number>;
}

export const LocationCard: React.FC<Props> = ({
  location,
  isSelected,
  onSelect,
  index,
  scrollX
}) => {
  const scale = useSharedValue(1);
  const pressed = useSharedValue(false);

  // Parallax effect based on scroll position
  const animatedStyle = useAnimatedStyle(() => {
    const inputRange = [
      (index - 1) * (CARD_WIDTH + 16),
      index * (CARD_WIDTH + 16),
      (index + 1) * (CARD_WIDTH + 16)
    ];
    
    const translateX = interpolate(
      scrollX.value,
      inputRange,
      [-50, 0, 50],
      'clamp'
    );

    return {
      transform: [
        { translateX },
        { scale: scale.value }
      ],
      borderWidth: isSelected ? 3 : 0,
      borderColor: isSelected ? '#F97316' : 'transparent',
      shadowOpacity: isSelected ? 0.25 : 0.1,
      shadowRadius: isSelected ? 16 : 8
    };
  });

  // Gesture handling for tap vs scroll differentiation
  const tapGesture = Gesture.Tap()
    .onBegin(() => {
      scale.value = withSpring(0.98);
      pressed.value = true;
    })
    .onEnd(() => {
      scale.value = withSpring(1);
      pressed.value = false;
      onSelect(location);
    })
    .onFinalize(() => {
      scale.value = withSpring(1);
      pressed.value = false;
    });

  return (
    <GestureDetector gesture={tapGesture}>
      <Animated.View style={animatedStyle}>
        <Box
          width={CARD_WIDTH}
          height={CARD_HEIGHT}
          borderRadius={16}
          overflow="hidden"
          bg="white"
          // Accessibility props
          accessibilityRole="button"
          accessibilityLabel={`${location.name} location for conversation practice`}
          accessibilityState={{ selected: isSelected }}
          accessibilityHint={
            isSelected 
              ? "Currently selected. Double-tap to confirm or swipe to explore other locations."
              : "Double-tap to select this location for your practice session."
          }
        >
          <FastImage
            source={typeof location.imageUrl === 'string' 
              ? { uri: location.imageUrl } 
              : location.imageUrl
            }
            style={{
              width: '100%',
              height: '100%',
              position: 'absolute'
            }}
            resizeMode={FastImage.resizeMode.cover}
          />
          
          {/* Gradient overlay */}
          <Box
            position="absolute"
            bottom={0}
            left={0}
            right={0}
            height="50%"
            bg={{
              linearGradient: {
                colors: ['transparent', 'rgba(0,0,0,0.4)'],
                start: [0, 0],
                end: [0, 1]
              }
            }}
          />
          
          {/* Text content */}
          <Box position="absolute" bottom={4} left={4} right={4}>
            <Text
              fontSize="lg"
              fontWeight="semibold"
              color="white"
              textShadowColor="rgba(0,0,0,0.6)"
              textShadowOffset={{ width: 0, height: 1 }}
              textShadowRadius={2}
            >
              {location.name}
            </Text>
          </Box>
        </Box>
      </Animated.View>
    </GestureDetector>
  );
};
```

## State Management Hooks

### Location Selection Hook
```typescript
// hooks/useLocationSelection.ts
import { useState, useCallback } from 'react';
import { Location } from '../types';

export const useLocationSelection = () => {
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);

  const selectLocation = useCallback((location: Location) => {
    setSelectedLocation(location);
    
    // Analytics tracking
    analyticsTrack('location_selected', {
      locationId: location.id,
      locationName: location.name,
      category: location.category
    });
    
    // Haptic feedback
    if (Platform.OS === 'ios') {
      HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Medium);
    }
  }, []);

  const clearLocationSelection = useCallback(() => {
    setSelectedLocation(null);
  }, []);

  return {
    selectedLocation,
    selectLocation,
    clearLocationSelection
  };
};
```

### Difficulty Selection Hook
```typescript
// hooks/useDifficultySelection.ts
import { useState, useCallback } from 'react';
import { Difficulty } from '../types';

export const useDifficultySelection = () => {
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty | null>(null);

  const selectDifficulty = useCallback((difficulty: Difficulty) => {
    setSelectedDifficulty(difficulty);
    
    // Analytics tracking
    analyticsTrack('difficulty_selected', {
      difficultyId: difficulty.id,
      difficultyLevel: difficulty.level
    });
    
    // Haptic feedback
    if (Platform.OS === 'ios') {
      HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Light);
    }
  }, []);

  const clearDifficultySelection = useCallback(() => {
    setSelectedDifficulty(null);
  }, []);

  return {
    selectedDifficulty,
    selectDifficulty,
    clearDifficultySelection
  };
};
```

### Validation Hook
```typescript
// hooks/useSelectionValidation.ts
import { useMemo } from 'react';
import { Location, Difficulty } from '../types';

export const useSelectionValidation = (
  location: Location | null,
  difficulty: Difficulty | null
) => {
  const isValidForCreation = useMemo(() => {
    return location !== null && difficulty !== null;
  }, [location, difficulty]);

  const validationMessage = useMemo(() => {
    if (!location && !difficulty) {
      return 'Select location and difficulty to continue';
    }
    if (!location) {
      return 'Select location to continue';
    }
    if (!difficulty) {
      return 'Select difficulty to continue';
    }
    return '';
  }, [location, difficulty]);

  return {
    isValidForCreation,
    validationMessage
  };
};
```

## Performance Optimizations

### Image Loading Strategy
```typescript
// utils/imageOptimization.ts
import FastImage from 'react-native-fast-image';

export const preloadLocationImages = () => {
  const imagesToPreload = LOCATIONS.map(location => ({
    uri: location.imageUrl,
    priority: FastImage.priority.high
  }));
  
  FastImage.preload(imagesToPreload);
};

export const getOptimizedImageProps = (imageUrl: string) => ({
  source: { uri: imageUrl },
  cache: FastImage.cacheControl.immutable,
  priority: FastImage.priority.normal,
  resizeMode: FastImage.resizeMode.cover
});
```

### Animation Performance
```typescript
// Animation configuration for 60fps performance
const SPRING_CONFIG = {
  tension: 400,
  friction: 40,
  useNativeDriver: true
};

const TIMING_CONFIG = {
  duration: 200,
  easing: Easing.out(Easing.quad),
  useNativeDriver: true
};

// Memory-efficient animation cleanup
export const useAnimationCleanup = () => {
  useEffect(() => {
    return () => {
      // Cancel any running animations
      cancelAnimation(scaleValue);
      cancelAnimation(opacityValue);
    };
  }, []);
};
```

### Bundle Size Optimization
```typescript
// Lazy loading for non-critical components
const LocationCarousel = React.lazy(() => import('./LocationCarousel'));
const DifficultySelection = React.lazy(() => import('./DifficultySelection'));

// Image bundle optimization
const getLocationImage = (locationId: string) => {
  switch (locationId) {
    case 'coffee-shop':
      return require('../../assets/images/locations/coffee-shop.webp');
    // Use WebP format for smaller bundle size
    default:
      return require('../../assets/images/locations/default.webp');
  }
};
```

## Testing Implementation

### Unit Tests
```typescript
// __tests__/UnifiedSelectionScreen.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { UnifiedSelectionScreen } from '../UnifiedSelectionScreen';

describe('UnifiedSelectionScreen', () => {
  it('renders all location cards', () => {
    const { getByLabelText } = render(<UnifiedSelectionScreen />);
    
    LOCATIONS.forEach(location => {
      expect(getByLabelText(new RegExp(location.name, 'i'))).toBeTruthy();
    });
  });

  it('enables create button when both selections made', async () => {
    const { getByLabelText, getByRole } = render(<UnifiedSelectionScreen />);
    
    // Select location
    const coffeeShopCard = getByLabelText(/coffee shop/i);
    fireEvent.press(coffeeShopCard);
    
    // Select difficulty
    const friendlyCard = getByLabelText(/friendly difficulty/i);
    fireEvent.press(friendlyCard);
    
    // Check button enabled
    await waitFor(() => {
      const createButton = getByRole('button', { name: /create scenario/i });
      expect(createButton).not.toBeDisabled();
    });
  });

  it('maintains accessibility standards', () => {
    const { getByLabelText } = render(<UnifiedSelectionScreen />);
    
    // Test accessibility labels
    expect(getByLabelText(/create your practice session/i)).toBeTruthy();
    expect(getByLabelText(/step 1 of 2/i)).toBeTruthy();
  });
});
```

### Integration Tests
```typescript
// __tests__/integration/selection-flow.test.tsx
import { renderScreen, navigateAndWait } from '../test-utils';

describe('Selection Flow Integration', () => {
  it('completes full selection and navigation flow', async () => {
    const { getByLabelText, getByRole, navigation } = renderScreen('Chat');
    
    // Select location
    const gymCard = getByLabelText(/gym location/i);
    fireEvent.press(gymCard);
    
    // Select difficulty  
    const realTalkCard = getByLabelText(/real talk difficulty/i);
    fireEvent.press(realTalkCard);
    
    // Create scenario
    const createButton = getByRole('button', { name: /create scenario/i });
    fireEvent.press(createButton);
    
    // Verify navigation
    await waitFor(() => {
      expect(navigation.navigate).toHaveBeenCalledWith('ChatContext', {
        location: expect.objectContaining({ id: 'gym' }),
        difficulty: expect.objectContaining({ id: 'real-talk' })
      });
    });
  });
});
```

### Performance Tests
```typescript
// __tests__/performance/carousel.test.tsx
describe('Carousel Performance', () => {
  it('maintains 60fps during scrolling', async () => {
    const { getByTestId } = render(<LocationCarousel />);
    const scrollView = getByTestId('location-carousel');
    
    // Simulate rapid scroll events
    const startTime = performance.now();
    for (let i = 0; i < 100; i++) {
      fireEvent.scroll(scrollView, {
        nativeEvent: { contentOffset: { x: i * 10 } }
      });
    }
    const endTime = performance.now();
    
    // Verify performance (should complete in <16ms per frame)
    expect(endTime - startTime).toBeLessThan(1600); // 100 frames * 16ms
  });
});
```

## Analytics Integration

### Event Tracking
```typescript
// analytics/selectionEvents.ts
export const trackLocationSelection = (location: Location, timeSpent: number) => {
  analytics.track('Location Selected', {
    locationId: location.id,
    locationName: location.name,
    category: location.category,
    timeToSelect: timeSpent,
    timestamp: Date.now()
  });
};

export const trackDifficultySelection = (difficulty: Difficulty, timeSpent: number) => {
  analytics.track('Difficulty Selected', {
    difficultyId: difficulty.id,
    difficultyLevel: difficulty.level,
    timeToSelect: timeSpent,
    timestamp: Date.now()
  });
};

export const trackScenarioCreation = (selections: SelectionState, totalTime: number) => {
  analytics.track('Scenario Created', {
    locationId: selections.selectedLocation?.id,
    difficultyId: selections.selectedDifficulty?.id,
    totalSelectionTime: totalTime,
    timestamp: Date.now()
  });
};
```

### Performance Monitoring
```typescript
// monitoring/performanceMetrics.ts
export const trackScreenLoadTime = () => {
  const startTime = performance.now();
  
  return () => {
    const loadTime = performance.now() - startTime;
    analytics.track('Screen Load Performance', {
      screenName: 'UnifiedSelection',
      loadTimeMs: loadTime,
      timestamp: Date.now()
    });
  };
};

export const trackAnimationPerformance = (animationType: string) => {
  const startTime = performance.now();
  
  return () => {
    const duration = performance.now() - startTime;
    analytics.track('Animation Performance', {
      animationType,
      durationMs: duration,
      targetFps: 60,
      timestamp: Date.now()
    });
  };
};
```

## Deployment Configuration

### Build Optimizations
```typescript
// metro.config.js - Bundle optimization
module.exports = {
  transformer: {
    assetPlugins: ['react-native-svg-asset-plugin'],
  },
  resolver: {
    alias: {
      '@': './src',
    },
  },
};

// babel.config.js - Performance plugins
module.exports = {
  plugins: [
    'react-native-reanimated/plugin', // Must be last
    ['@babel/plugin-transform-react-jsx', { runtime: 'automatic' }],
  ],
};
```

### Environment Configuration
```typescript
// config/environment.ts
export const CONFIG = {
  development: {
    enableFlipperDebug: true,
    logLevel: 'debug',
    imageQuality: 'high'
  },
  production: {
    enableFlipperDebug: false,
    logLevel: 'error',
    imageQuality: 'optimized'
  }
};
```

## Monitoring and Maintenance

### Error Tracking
```typescript
// error/errorBoundary.tsx
export const UnifiedSelectionErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ 
  children 
}) => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        crashlytics.recordError(error);
        analytics.track('Screen Error', {
          screenName: 'UnifiedSelection',
          error: error.message,
          errorInfo: errorInfo.componentStack
        });
      }}
      fallback={(error) => (
        <Box flex={1} justifyContent="center" alignItems="center" p={4}>
          <Text fontSize="lg" textAlign="center" mb={4}>
            Something went wrong with the selection screen.
          </Text>
          <Button onPress={() => navigation.goBack()}>
            Go Back
          </Button>
        </Box>
      )}
    >
      {children}
    </ErrorBoundary>
  );
};
```

### Performance Monitoring
```typescript
// monitoring/performanceMonitor.ts
export const setupPerformanceMonitoring = () => {
  // Monitor frame drops
  const frameMonitor = new FrameMonitor();
  frameMonitor.onFrameDrop((droppedFrames) => {
    if (droppedFrames > 3) {
      analytics.track('Performance Issue', {
        type: 'frame_drops',
        droppedFrames,
        screenName: 'UnifiedSelection'
      });
    }
  });

  // Monitor memory usage
  const memoryMonitor = new MemoryMonitor();
  memoryMonitor.onMemoryPressure((level) => {
    analytics.track('Memory Pressure', {
      level,
      screenName: 'UnifiedSelection'
    });
  });
};
```

## Migration and Rollout

### Feature Flag Implementation
```typescript
// flags/unifiedSelection.ts
export const useUnifiedSelectionFlag = () => {
  const isEnabled = useFeatureFlag('unified_selection_enabled', true);
  const isExperimentActive = useExperiment('unified_vs_separate_selection');
  
  return {
    shouldShowUnifiedSelection: isEnabled && isExperimentActive.variant === 'unified',
    experimentVariant: isExperimentActive.variant
  };
};
```

### Rollback Strategy
```typescript
// If rollback needed, gracefully handle navigation
const handleNavigationFallback = (navigation: any) => {
  // Fallback to separate difficulty selection screen
  navigation.navigate('ChatDifficultySelection', {
    source: 'unified_selection_fallback'
  });
};
```

## Last Updated
- **Version 1.0.0**: Complete implementation specifications with performance optimizations
- **Focus**: Production-ready React Native implementation with comprehensive testing
- **Next**: Development team implementation and testing phase