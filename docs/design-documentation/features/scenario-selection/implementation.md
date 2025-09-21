# Scenario Selection Feature - Implementation Guide

---
title: Scenarios Tab - Pre-built Scenario Selection Implementation
description: Complete developer handoff for pre-built scenario selection in the Scenarios tab
feature: scenarios-tab-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - accessibility.md
  - ../../design-system/components/cards.md
  - ../../design-system/components/buttons.md
  - ../../design-system/components/modals.md
  - ../../design-system/components/navigation.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native 0.72+
  - Expo 52+
  - NativeBase
  - NativeWind 4.1
  - React Native Reanimated 3.6+
  - Zustand 4.4+
status: approved
---

## Implementation Overview

The Scenario Selection feature implements a **two-step selection flow** with rich animations, accessibility support, and seamless state management. Users browse 8 scenario categories, select their preferred environment, choose from 3 difficulty levels, and transition smoothly to practice preparation.

### Architecture Patterns
- **State Management**: Zustand store for selection state and user preferences
- **Navigation**: React Navigation 6 with custom transitions
- **Animations**: React Native Reanimated 3 with 60fps performance
- **UI Components**: NativeBase with NativeWind styling
- **Data Persistence**: AsyncStorage for user preferences and history
- **Analytics**: Event tracking for selection patterns and user behavior

## Project Structure

```
src/
├── features/
│   └── scenario-selection/
│       ├── components/
│       │   ├── ScenarioGrid.tsx
│       │   ├── ScenarioCard.tsx
│       │   ├── DifficultySelector.tsx
│       │   ├── QuickPractice.tsx
│       │   └── SelectionProgress.tsx
│       ├── screens/
│       │   ├── ScenarioSelectionScreen.tsx
│       │   ├── DifficultySelectionScreen.tsx
│       │   └── SelectionConfirmationScreen.tsx
│       ├── hooks/
│       │   ├── useScenarioSelection.ts
│       │   ├── useSelectionHistory.ts
│       │   └── useScenarioRecommendations.ts
│       ├── store/
│       │   └── scenarioSelectionStore.ts
│       ├── types/
│       │   └── scenarios.ts
│       └── utils/
│           ├── scenarioData.ts
│           └── difficultyCalculator.ts
└── shared/
    ├── components/
    │   ├── AnimatedCard.tsx
    │   └── ProgressIndicator.tsx
    └── hooks/
        └── useAccessibleAnimations.ts
```

## Core Data Models

### Scenario Type Definitions
```typescript
// src/features/scenario-selection/types/scenarios.ts

export interface Scenario {
  id: string;
  name: string;
  description: string;
  category: ScenarioCategory;
  environment: EnvironmentDetails;
  imageUrl: string;
  popularityRank: number;
  averageCompletionTime: number;
  skillFocus: SkillType[];
  isPremium: boolean; // Premium scenarios (gyms, bars, galleries)
  isRecommended?: boolean;
  isNew?: boolean;
}

export interface EnvironmentDetails {
  setting: string;
  timeOfDay: 'morning' | 'afternoon' | 'evening' | 'night';
  crowdLevel: 'quiet' | 'moderate' | 'busy';
  ambientNoise: 'low' | 'medium' | 'high';
  lightingCondition: 'bright' | 'dim' | 'natural';
  socialExpectation: 'casual' | 'formal' | 'relaxed';
}

export interface Difficulty {
  level: 'green' | 'yellow' | 'red';
  name: string;
  description: string;
  shortDescription: string;
  emoji: string;
  aiPersonality: AIPersonalitySettings;
  expectedSuccessRate: number;
  requiredSkillLevel: number;
}

export interface AIPersonalitySettings {
  receptiveness: number; // 0-100
  conversationFlow: number; // 0-100
  challengeLevel: number; // 0-100
  responseVariability: number; // 0-100
  contextAwareness: number; // 0-100
}

export interface UserSelectionData {
  scenario: Scenario;
  difficulty: Difficulty;
  timestamp: Date;
  sessionId: string;
  estimatedDuration: number;
  userGoals: string[];
  previousAttempts?: number;
}

export type ScenarioCategory = 
  | 'social-casual'
  | 'activity-based'
  | 'educational'
  | 'service-interaction';

export type SkillType = 
  | 'conversation-starters'
  | 'active-listening'
  | 'storytelling'
  | 'humor'
  | 'confidence-building'
  | 'body-language';
```

### Selection State Management
```typescript
// src/features/scenario-selection/store/scenarioSelectionStore.ts

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface ScenarioSelectionState {
  // Current selection state
  selectedScenario: Scenario | null;
  selectedDifficulty: Difficulty | null;
  selectionStep: 'scenario' | 'difficulty' | 'confirmation';
  
  // User history and preferences
  recentSelections: UserSelectionData[];
  favoriteScenarios: string[];
  completionStats: Record<string, ScenarioStats>;
  userPreferences: UserPreferences;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  showRecommendations: boolean;
  
  // Actions
  setSelectedScenario: (scenario: Scenario) => void;
  setSelectedDifficulty: (difficulty: Difficulty) => void;
  nextStep: () => void;
  previousStep: () => void;
  resetSelection: () => void;
  
  // History management
  addToHistory: (selection: UserSelectionData) => void;
  toggleFavorite: (scenarioId: string) => void;
  updateCompletionStats: (scenarioId: string, success: boolean) => void;
  
  // Recommendations
  getRecommendedScenarios: () => Scenario[];
  getOptimalDifficulty: (scenarioId: string) => Difficulty;
}

interface ScenarioStats {
  attempts: number;
  successes: number;
  averageScore: number;
  lastPlayed: Date;
  bestStreak: number;
  currentStreak: number;
}

interface UserPreferences {
  preferredTimeSlots: string[];
  avoidedScenarios: string[];
  difficultyProgression: 'conservative' | 'balanced' | 'aggressive';
  notificationSettings: NotificationPreferences;
}

export const useScenarioSelectionStore = create<ScenarioSelectionState>()(
  persist(
    (set, get) => ({
      // Initial state
      selectedScenario: null,
      selectedDifficulty: null,
      selectionStep: 'scenario',
      recentSelections: [],
      favoriteScenarios: [],
      completionStats: {},
      userPreferences: {
        preferredTimeSlots: [],
        avoidedScenarios: [],
        difficultyProgression: 'balanced',
        notificationSettings: {
          reminderFrequency: 'daily',
          achievementNotifications: true,
          recommendationAlerts: true,
        },
      },
      isLoading: false,
      error: null,
      showRecommendations: true,
      
      // Selection actions
      setSelectedScenario: (scenario) => {
        set({ selectedScenario: scenario });
        
        // Analytics tracking
        trackEvent('scenario_selected', {
          scenario_id: scenario.id,
          scenario_name: scenario.name,
          category: scenario.category,
          user_previous_attempts: get().completionStats[scenario.id]?.attempts || 0,
        });
      },
      
      setSelectedDifficulty: (difficulty) => {
        set({ selectedDifficulty: difficulty });
        
        trackEvent('difficulty_selected', {
          difficulty_level: difficulty.level,
          scenario_id: get().selectedScenario?.id,
          expected_success_rate: difficulty.expectedSuccessRate,
        });
      },
      
      nextStep: () => {
        const currentStep = get().selectionStep;
        const nextSteps = {
          'scenario': 'difficulty',
          'difficulty': 'confirmation',
          'confirmation': 'confirmation', // Stay on confirmation
        } as const;
        
        set({ selectionStep: nextSteps[currentStep] });
      },
      
      previousStep: () => {
        const currentStep = get().selectionStep;
        const previousSteps = {
          'scenario': 'scenario', // Stay on scenario
          'difficulty': 'scenario',
          'confirmation': 'difficulty',
        } as const;
        
        set({ selectionStep: previousSteps[currentStep] });
      },
      
      resetSelection: () => {
        set({
          selectedScenario: null,
          selectedDifficulty: null,
          selectionStep: 'scenario',
          error: null,
        });
      },
      
      // History management
      addToHistory: (selection) => {
        const current = get().recentSelections;
        const updated = [selection, ...current.slice(0, 19)]; // Keep last 20
        
        set({ recentSelections: updated });
      },
      
      toggleFavorite: (scenarioId) => {
        const current = get().favoriteScenarios;
        const updated = current.includes(scenarioId)
          ? current.filter(id => id !== scenarioId)
          : [...current, scenarioId];
          
        set({ favoriteScenarios: updated });
      },
      
      updateCompletionStats: (scenarioId, success) => {
        const current = get().completionStats;
        const existing = current[scenarioId] || {
          attempts: 0,
          successes: 0,
          averageScore: 0,
          lastPlayed: new Date(),
          bestStreak: 0,
          currentStreak: 0,
        };
        
        const updated = {
          ...existing,
          attempts: existing.attempts + 1,
          successes: success ? existing.successes + 1 : existing.successes,
          lastPlayed: new Date(),
          currentStreak: success ? existing.currentStreak + 1 : 0,
          bestStreak: success 
            ? Math.max(existing.bestStreak, existing.currentStreak + 1)
            : existing.bestStreak,
        };
        
        set({
          completionStats: {
            ...current,
            [scenarioId]: updated,
          },
        });
      },
      
      // Recommendation engine
      getRecommendedScenarios: () => {
        const { completionStats, recentSelections, userPreferences } = get();
        
        // Algorithm factors:
        // 1. Success rate in similar scenarios
        // 2. Time since last played
        // 3. User goals alignment
        // 4. Progressive difficulty matching
        
        return SCENARIOS.filter(scenario => {
          const stats = completionStats[scenario.id];
          
          // Skip recently played scenarios
          const recentlyPlayed = recentSelections.some(
            selection => selection.scenario.id === scenario.id &&
            Date.now() - selection.timestamp.getTime() < 24 * 60 * 60 * 1000
          );
          
          if (recentlyPlayed) return false;
          
          // Skip avoided scenarios
          if (userPreferences.avoidedScenarios.includes(scenario.id)) {
            return false;
          }
          
          // Include scenarios with no history (exploration)
          if (!stats) return true;
          
          // Include scenarios with room for improvement
          const successRate = stats.successes / stats.attempts;
          return successRate < 0.8; // Less than 80% success rate
        });
      },
      
      getOptimalDifficulty: (scenarioId) => {
        const stats = get().completionStats[scenarioId];
        const progression = get().userPreferences.difficultyProgression;
        
        if (!stats || stats.attempts < 3) {
          return DIFFICULTIES.green; // Start with green for new scenarios
        }
        
        const successRate = stats.successes / stats.attempts;
        const progressionThresholds = {
          conservative: { green: 0.9, yellow: 0.85 },
          balanced: { green: 0.8, yellow: 0.75 },
          aggressive: { green: 0.7, yellow: 0.65 },
        };
        
        const thresholds = progressionThresholds[progression];
        
        if (successRate >= thresholds.green) {
          return stats.attempts >= 5 ? DIFFICULTIES.yellow : DIFFICULTIES.green;
        } else if (successRate >= thresholds.yellow) {
          return stats.attempts >= 8 ? DIFFICULTIES.red : DIFFICULTIES.yellow;
        } else {
          return DIFFICULTIES.green; // Step back if struggling
        }
      },
    }),
    {
      name: 'scenario-selection-store',
      storage: {
        getItem: async (name) => {
          const value = await AsyncStorage.getItem(name);
          return value ? JSON.parse(value) : null;
        },
        setItem: async (name, value) => {
          await AsyncStorage.setItem(name, JSON.stringify(value));
        },
        removeItem: async (name) => {
          await AsyncStorage.removeItem(name);
        },
      },
      partialize: (state) => ({
        recentSelections: state.recentSelections,
        favoriteScenarios: state.favoriteScenarios,
        completionStats: state.completionStats,
        userPreferences: state.userPreferences,
      }),
    }
  )
);
```

## Core Components Implementation

### Scenario Grid Component
```typescript
// src/features/scenario-selection/components/ScenarioGrid.tsx

import React from 'react';
import { FlatList, Dimensions } from 'react-native';
import { Box, VStack } from 'native-base';
import Animated, { 
  FadeInDown, 
  useSharedValue, 
  useAnimatedStyle,
  withTiming,
  interpolate,
} from 'react-native-reanimated';
import { ScenarioCard } from './ScenarioCard';
import { useScenarioSelectionStore } from '../store/scenarioSelectionStore';
import { useAccessibleAnimations } from '@/shared/hooks/useAccessibleAnimations';

const { width } = Dimensions.get('window');
const CARD_MARGIN = 16;
const CARDS_PER_ROW = 2;
const CARD_WIDTH = (width - (CARD_MARGIN * 3)) / CARDS_PER_ROW;

interface ScenarioGridProps {
  scenarios: Scenario[];
  onScenarioSelect: (scenario: Scenario) => void;
  showRecommendations?: boolean;
}

export const ScenarioGrid: React.FC<ScenarioGridProps> = ({
  scenarios,
  onScenarioSelect,
  showRecommendations = true,
}) => {
  const { 
    selectedScenario,
    completionStats,
    getRecommendedScenarios,
  } = useScenarioSelectionStore();
  
  const { reduceMotion, getAnimationConfig } = useAccessibleAnimations();
  const scrollY = useSharedValue(0);
  
  const recommendedScenarios = showRecommendations 
    ? getRecommendedScenarios() 
    : [];
  
  const organizedScenarios = React.useMemo(() => {
    const recommended = scenarios.filter(s => 
      recommendedScenarios.some(r => r.id === s.id)
    );
    const other = scenarios.filter(s => 
      !recommendedScenarios.some(r => r.id === s.id)
    );
    
    return { recommended, other };
  }, [scenarios, recommendedScenarios]);
  
  const renderScenarioCard = ({ item: scenario, index }: { 
    item: Scenario; 
    index: number 
  }) => {
    const stats = completionStats[scenario.id];
    const isRecommended = recommendedScenarios.some(r => r.id === scenario.id);
    
    return (
      <Animated.View
        entering={reduceMotion ? undefined : FadeInDown.delay(index * 100)}
        style={{
          width: CARD_WIDTH,
          marginBottom: CARD_MARGIN,
          marginHorizontal: CARD_MARGIN / 2,
        }}
      >
        <ScenarioCard
          scenario={scenario}
          stats={stats}
          isSelected={selectedScenario?.id === scenario.id}
          isRecommended={isRecommended}
          onPress={() => onScenarioSelect(scenario)}
        />
      </Animated.View>
    );
  };
  
  const headerAnimatedStyle = useAnimatedStyle(() => {
    const opacity = interpolate(
      scrollY.value,
      [0, 100, 200],
      [1, 0.8, 0.6]
    );
    
    return {
      opacity: reduceMotion ? 1 : opacity,
    };
  });
  
  return (
    <VStack flex={1} space={6}>
      {/* Recommended Scenarios Section */}
      {organizedScenarios.recommended.length > 0 && (
        <Animated.View style={headerAnimatedStyle}>
          <VStack space={4}>
            <Box
              accessible={true}
              accessibilityRole="header"
              accessibilityLevel={2}
              px={4}
            >
              <Text
                fontSize="lg"
                fontWeight="600"
                color="gray.800"
                className="text-gray-800 font-semibold"
              >
                Recommended for You
              </Text>
              <Text
                fontSize="sm"
                color="gray.600"
                className="text-gray-600"
              >
                Based on your goals and progress
              </Text>
            </Box>
            
            <FlatList
              data={organizedScenarios.recommended}
              renderItem={renderScenarioCard}
              keyExtractor={(item) => `recommended-${item.id}`}
              numColumns={CARDS_PER_ROW}
              scrollEnabled={false}
              contentContainerStyle={{
                paddingHorizontal: CARD_MARGIN / 2,
              }}
              accessibilityLabel="Recommended practice scenarios"
            />
          </VStack>
        </Animated.View>
      )}
      
      {/* All Scenarios Section */}
      <VStack flex={1} space={4}>
        <Box
          accessible={true}
          accessibilityRole="header"
          accessibilityLevel={2}
          px={4}
        >
          <Text
            fontSize="lg"
            fontWeight="600"
            color="gray.800"
            className="text-gray-800 font-semibold"
          >
            All Scenarios
          </Text>
          <Text
            fontSize="sm"
            color="gray.600"
            className="text-gray-600"
          >
            Choose any scenario to practice
          </Text>
        </Box>
        
        <FlatList
          data={organizedScenarios.other}
          renderItem={renderScenarioCard}
          keyExtractor={(item) => item.id}
          numColumns={CARDS_PER_ROW}
          onScroll={(event) => {
            scrollY.value = event.nativeEvent.contentOffset.y;
          }}
          contentContainerStyle={{
            paddingHorizontal: CARD_MARGIN / 2,
            paddingBottom: 100,
          }}
          accessibilityLabel="All available practice scenarios"
          showsVerticalScrollIndicator={false}
        />
      </VStack>
    </VStack>
  );
};
```

### Scenario Card Component
```typescript
// src/features/scenario-selection/components/ScenarioCard.tsx

import React from 'react';
import { Pressable } from 'react-native';
import { Box, Image, Text, VStack, HStack, Badge } from 'native-base';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSequence,
  interpolate,
} from 'react-native-reanimated';
import { HapticFeedback } from 'expo-haptics';
import { useAccessibleAnimations } from '@/shared/hooks/useAccessibleAnimations';

interface ScenarioCardProps {
  scenario: Scenario;
  stats?: ScenarioStats;
  isSelected: boolean;
  isRecommended: boolean;
  onPress: () => void;
}

export const ScenarioCard: React.FC<ScenarioCardProps> = ({
  scenario,
  stats,
  isSelected,
  isRecommended,
  onPress,
}) => {
  const { reduceMotion } = useAccessibleAnimations();
  
  const scale = useSharedValue(1);
  const elevation = useSharedValue(2);
  const selectedScale = useSharedValue(isSelected ? 1.05 : 1);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { scale: scale.value * selectedScale.value }
    ],
    shadowOpacity: elevation.value * 0.1,
    shadowOffset: {
      width: 0,
      height: elevation.value,
    },
    shadowRadius: elevation.value * 2,
  }));
  
  const handlePressIn = () => {
    if (!reduceMotion) {
      HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Light);
      
      scale.value = withTiming(0.95, { duration: 100 });
      elevation.value = withTiming(4, { duration: 100 });
    }
  };
  
  const handlePressOut = () => {
    if (!reduceMotion) {
      scale.value = withTiming(1, { duration: 200 });
      elevation.value = withTiming(2, { duration: 200 });
    }
  };
  
  const handlePress = () => {
    if (!reduceMotion && !isSelected) {
      selectedScale.value = withSequence(
        withTiming(1.1, { duration: 150 }),
        withTiming(1.05, { duration: 100 })
      );
    }
    
    HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Medium);
    onPress();
  };
  
  React.useEffect(() => {
    selectedScale.value = withTiming(isSelected ? 1.05 : 1, {
      duration: 300,
    });
  }, [isSelected]);
  
  const getAccessibilityLabel = () => {
    let label = `${scenario.name} scenario. ${scenario.description}. `;
    
    if (isRecommended) {
      label += 'Recommended for you. ';
    }
    
    if (stats) {
      const successRate = Math.round((stats.successes / stats.attempts) * 100);
      label += `You have practiced this ${stats.attempts} times with ${successRate}% success rate. `;
    } else {
      label += 'New scenario, never practiced. ';
    }
    
    if (isSelected) {
      label += 'Currently selected. ';
    }
    
    label += 'Double tap to select this scenario.';
    
    return label;
  };
  
  const successRate = stats 
    ? Math.round((stats.successes / stats.attempts) * 100) 
    : null;
  
  return (
    <Pressable
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={getAccessibilityLabel()}
      accessibilityHint="Select this scenario to continue to difficulty selection"
      accessibilityState={{ selected: isSelected }}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={handlePress}
    >
      <Animated.View style={animatedStyle}>
        <Box
          bg="white"
          borderRadius="xl"
          shadow={2}
          overflow="hidden"
          borderWidth={isSelected ? 3 : 1}
          borderColor={isSelected ? "orange.500" : "gray.200"}
          className={`
            bg-white rounded-xl overflow-hidden shadow-sm
            ${isSelected ? 'border-3 border-orange-500' : 'border border-gray-200'}
          `}
        >
          {/* Scenario Image */}
          <Box position="relative">
            <Image
              source={{ uri: scenario.imageUrl }}
              alt={`${scenario.name} environment preview`}
              width="100%"
              height={120}
              resizeMode="cover"
            />
            
            {/* Badges Overlay */}
            <Box position="absolute" top={2} right={2}>
              <VStack space={1} alignItems="flex-end">
                {isRecommended && (
                  <Badge
                    variant="solid"
                    colorScheme="orange"
                    rounded="full"
                    px={2}
                    py={1}
                    _text={{ fontSize: "xs", fontWeight: "600" }}
                  >
                    ⭐ Recommended
                  </Badge>
                )}
                
                {scenario.isNew && (
                  <Badge
                    variant="solid"
                    colorScheme="green"
                    rounded="full"
                    px={2}
                    py={1}
                    _text={{ fontSize: "xs", fontWeight: "600" }}
                  >
                    🆕 New
                  </Badge>
                )}
              </VStack>
            </Box>
            
            {/* Success Rate Indicator */}
            {successRate !== null && (
              <Box position="absolute" bottom={2} left={2}>
                <Badge
                  variant="solid"
                  colorScheme={successRate >= 80 ? "green" : successRate >= 60 ? "yellow" : "red"}
                  rounded="full"
                  px={2}
                  py={1}
                  _text={{ fontSize: "xs", fontWeight: "600" }}
                >
                  {successRate}% success
                </Badge>
              </Box>
            )}
          </Box>
          
          {/* Card Content */}
          <VStack p={4} space={2}>
            <Text
              fontSize="md"
              fontWeight="600"
              color="gray.800"
              numberOfLines={1}
              className="text-gray-800 font-semibold"
            >
              {scenario.name}
            </Text>
            
            <Text
              fontSize="sm"
              color="gray.600"
              numberOfLines={2}
              className="text-gray-600"
            >
              {scenario.description}
            </Text>
            
            {/* Stats Row */}
            {stats && (
              <HStack justifyContent="space-between" alignItems="center" mt={2}>
                <Text fontSize="xs" color="gray.500" className="text-gray-500">
                  {stats.attempts} attempts
                </Text>
                
                {stats.currentStreak > 0 && (
                  <Text fontSize="xs" color="orange.600" className="text-orange-600">
                    🔥 {stats.currentStreak} streak
                  </Text>
                )}
              </HStack>
            )}
          </VStack>
        </Box>
      </Animated.View>
    </Pressable>
  );
};
```

### Difficulty Selector Component
```typescript
// src/features/scenario-selection/components/DifficultySelector.tsx

import React from 'react';
import { Pressable } from 'react-native';
import { Box, Text, VStack, HStack } from 'native-base';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSequence,
  interpolateColor,
} from 'react-native-reanimated';
import { HapticFeedback } from 'expo-haptics';
import { DIFFICULTIES } from '../utils/scenarioData';
import { useScenarioSelectionStore } from '../store/scenarioSelectionStore';

interface DifficultySelectorProps {
  scenarioId: string;
  onDifficultySelect: (difficulty: Difficulty) => void;
}

export const DifficultySelector: React.FC<DifficultySelectorProps> = ({
  scenarioId,
  onDifficultySelect,
}) => {
  const { 
    selectedDifficulty, 
    completionStats,
    getOptimalDifficulty,
  } = useScenarioSelectionStore();
  
  const optimalDifficulty = getOptimalDifficulty(scenarioId);
  const stats = completionStats[scenarioId];
  
  const getDifficultyColor = (level: string) => {
    const colors = {
      green: '#22C55E',
      yellow: '#F59E0B', 
      red: '#EF4444',
    };
    return colors[level as keyof typeof colors];
  };
  
  const getDifficultyStats = (difficulty: Difficulty) => {
    if (!stats) return null;
    
    // This would come from more detailed analytics
    // For now, we'll estimate based on overall stats
    const overallSuccessRate = stats.successes / stats.attempts;
    const estimatedSuccessRate = {
      green: Math.min(overallSuccessRate + 0.2, 1),
      yellow: overallSuccessRate,
      red: Math.max(overallSuccessRate - 0.2, 0),
    };
    
    return {
      attempts: Math.floor(stats.attempts * 0.33), // Rough distribution
      successRate: estimatedSuccessRate[difficulty.level],
    };
  };
  
  return (
    <VStack space={4} px={4}>
      <Box
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={2}
      >
        <Text
          fontSize="xl"
          fontWeight="bold"
          color="gray.800"
          textAlign="center"
          className="text-gray-800 font-bold text-center"
        >
          Choose Your Challenge Level
        </Text>
        <Text
          fontSize="md"
          color="gray.600"
          textAlign="center"
          mt={2}
          className="text-gray-600 text-center"
        >
          How challenging do you want this practice to be?
        </Text>
      </Box>
      
      {Object.values(DIFFICULTIES).map((difficulty) => {
        const isSelected = selectedDifficulty?.level === difficulty.level;
        const isOptimal = optimalDifficulty.level === difficulty.level;
        const difficultyStats = getDifficultyStats(difficulty);
        
        return (
          <DifficultyButton
            key={difficulty.level}
            difficulty={difficulty}
            isSelected={isSelected}
            isOptimal={isOptimal}
            stats={difficultyStats}
            onPress={() => onDifficultySelect(difficulty)}
          />
        );
      })}
      
      {/* Optimal Difficulty Hint */}
      {optimalDifficulty && (
        <Box
          bg="blue.50"
          p={3}
          borderRadius="md"
          borderLeftWidth={4}
          borderLeftColor="blue.500"
          className="bg-blue-50 border-l-4 border-blue-500 rounded-md"
        >
          <Text
            fontSize="sm"
            color="blue.700"
            className="text-blue-700"
          >
            💡 Based on your progress, <Text fontWeight="600">{optimalDifficulty.name}</Text> difficulty 
            might be optimal for skill building.
          </Text>
        </Box>
      )}
    </VStack>
  );
};

const DifficultyButton: React.FC<{
  difficulty: Difficulty;
  isSelected: boolean;
  isOptimal: boolean;
  stats: { attempts: number; successRate: number } | null;
  onPress: () => void;
}> = ({ difficulty, isSelected, isOptimal, stats, onPress }) => {
  const scale = useSharedValue(1);
  const borderOpacity = useSharedValue(isSelected ? 1 : 0.3);
  
  const color = getDifficultyColor(difficulty.level);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    borderColor: color,
    borderOpacity: borderOpacity.value,
  }));
  
  const handlePressIn = () => {
    scale.value = withTiming(0.98, { duration: 100 });
  };
  
  const handlePressOut = () => {
    scale.value = withTiming(1, { duration: 200 });
  };
  
  const handlePress = () => {
    HapticFeedback.impactAsync(HapticFeedback.ImpactFeedbackStyle.Medium);
    
    if (!isSelected) {
      scale.value = withSequence(
        withTiming(1.05, { duration: 150 }),
        withTiming(1, { duration: 100 })
      );
      
      borderOpacity.value = withTiming(1, { duration: 200 });
    }
    
    onPress();
  };
  
  React.useEffect(() => {
    borderOpacity.value = withTiming(isSelected ? 1 : 0.3, {
      duration: 300,
    });
  }, [isSelected]);
  
  const getAccessibilityLabel = () => {
    let label = `${difficulty.name} difficulty. ${difficulty.description}. `;
    
    if (isOptimal) {
      label += 'Recommended difficulty based on your progress. ';
    }
    
    if (stats && stats.attempts > 0) {
      const successPercentage = Math.round(stats.successRate * 100);
      label += `You have ${successPercentage}% success rate at this level. `;
    }
    
    if (isSelected) {
      label += 'Currently selected. ';
    }
    
    label += 'Double tap to select this difficulty level.';
    
    return label;
  };
  
  return (
    <Pressable
      accessible={true}
      accessibilityRole="radio"
      accessibilityLabel={getAccessibilityLabel()}
      accessibilityHint="Select this difficulty level for your practice session"
      accessibilityState={{ 
        selected: isSelected,
        checked: isSelected,
      }}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={handlePress}
    >
      <Animated.View style={animatedStyle}>
        <Box
          bg="white"
          borderWidth={3}
          borderRadius="xl"
          p={4}
          shadow={isSelected ? 3 : 1}
          position="relative"
          className={`
            bg-white rounded-xl shadow-sm
            ${isSelected ? 'shadow-md' : 'shadow-sm'}
          `}
        >
          {/* Optimal Badge */}
          {isOptimal && (
            <Box
              position="absolute"
              top={-2}
              right={4}
              bg="blue.500"
              px={2}
              py={1}
              borderRadius="full"
              className="bg-blue-500 rounded-full"
            >
              <Text
                fontSize="xs"
                color="white"
                fontWeight="600"
                className="text-white font-semibold"
              >
                Optimal
              </Text>
            </Box>
          )}
          
          <HStack space={4} alignItems="center">
            {/* Difficulty Icon */}
            <Box
              w={12}
              h={12}
              borderRadius="full"
              bg={`${difficulty.level}.100`}
              justifyContent="center"
              alignItems="center"
              className={`w-12 h-12 rounded-full justify-center items-center`}
              style={{ backgroundColor: color + '20' }}
            >
              <Text fontSize="2xl">{difficulty.emoji}</Text>
            </Box>
            
            {/* Difficulty Info */}
            <VStack flex={1} space={1}>
              <HStack justifyContent="space-between" alignItems="center">
                <Text
                  fontSize="lg"
                  fontWeight="600"
                  color="gray.800"
                  className="text-gray-800 font-semibold"
                >
                  {difficulty.name}
                </Text>
                
                {stats && stats.attempts > 0 && (
                  <Text
                    fontSize="sm"
                    color="gray.500"
                    className="text-gray-500"
                  >
                    {Math.round(stats.successRate * 100)}% success
                  </Text>
                )}
              </HStack>
              
              <Text
                fontSize="sm"
                color="gray.600"
                className="text-gray-600"
              >
                {difficulty.shortDescription}
              </Text>
              
              {/* Expected Success Rate */}
              <Text
                fontSize="xs"
                color="gray.500"
                className="text-gray-500"
              >
                Expected success: {difficulty.expectedSuccessRate}%
              </Text>
            </VStack>
          </HStack>
        </Box>
      </Animated.View>
    </Pressable>
  );
};
```

## Screen Implementations

### Main Scenario Selection Screen
```typescript
// src/features/scenario-selection/screens/ScenarioSelectionScreen.tsx

import React, { useEffect } from 'react';
import { Box, VStack, Text, ScrollView } from 'native-base';
import { SafeAreaView } from 'react-native-safe-area-context';
import Animated, { FadeInUp, FadeOutDown } from 'react-native-reanimated';
import { useNavigation } from '@react-navigation/native';

import { ScenarioGrid } from '../components/ScenarioGrid';
import { QuickPractice } from '../components/QuickPractice';
import { SelectionProgress } from '../components/SelectionProgress';
import { useScenarioSelectionStore } from '../store/scenarioSelectionStore';
import { useScenarioSelection } from '../hooks/useScenarioSelection';
import { SCENARIOS } from '../utils/scenarioData';
import { trackScreenView } from '@/shared/analytics';

export const ScenarioSelectionScreen: React.FC = () => {
  const navigation = useNavigation();
  const { 
    selectedScenario,
    selectionStep,
    nextStep,
    setSelectedScenario,
    recentSelections,
  } = useScenarioSelectionStore();
  
  const { 
    isLoading,
    error,
    refreshScenarios,
  } = useScenarioSelection();
  
  useEffect(() => {
    trackScreenView('scenario_selection', {
      step: selectionStep,
      has_recent_selections: recentSelections.length > 0,
    });
  }, []);
  
  const handleScenarioSelect = (scenario: Scenario) => {
    setSelectedScenario(scenario);
    
    // Small delay for selection animation
    setTimeout(() => {
      nextStep();
      navigation.navigate('DifficultySelection', { scenario });
    }, 800);
  };
  
  if (isLoading) {
    return <LoadingState />;
  }
  
  if (error) {
    return <ErrorState error={error} onRetry={refreshScenarios} />;
  }
  
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#F9FAFB' }}>
      <Animated.View 
        entering={FadeInUp}
        exiting={FadeOutDown}
        style={{ flex: 1 }}
      >
        <ScrollView
          flex={1}
          showsVerticalScrollIndicator={false}
          contentInsetAdjustmentBehavior="automatic"
        >
          <VStack flex={1} space={6} py={4}>
            {/* Header */}
            <VStack space={2} px={4}>
              <SelectionProgress currentStep={1} totalSteps={3} />
              
              <Box
                accessible={true}
                accessibilityRole="header"
                accessibilityLevel={1}
              >
                <Text
                  fontSize="2xl"
                  fontWeight="bold"
                  color="gray.800"
                  textAlign="center"
                  className="text-gray-800 font-bold text-center"
                >
                  Choose Your Practice Scenario
                </Text>
                <Text
                  fontSize="md"
                  color="gray.600"
                  textAlign="center"
                  mt={2}
                  className="text-gray-600 text-center"
                >
                  Pick a place where you want to practice conversations
                </Text>
              </Box>
            </VStack>
            
            {/* Quick Practice Section */}
            {recentSelections.length > 0 && (
              <QuickPractice
                recentSelections={recentSelections.slice(0, 3)}
                onQuickSelect={handleScenarioSelect}
              />
            )}
            
            {/* Main Scenario Grid */}
            <ScenarioGrid
              scenarios={SCENARIOS}
              onScenarioSelect={handleScenarioSelect}
              showRecommendations={true}
            />
          </VStack>
        </ScrollView>
      </Animated.View>
    </SafeAreaView>
  );
};

// Loading and Error States
const LoadingState: React.FC = () => (
  <SafeAreaView style={{ flex: 1, backgroundColor: '#F9FAFB' }}>
    <VStack flex={1} justifyContent="center" alignItems="center" space={4}>
      <Box
        w={12}
        h={12}
        borderRadius="full"
        bg="orange.100"
        justifyContent="center"
        alignItems="center"
      >
        <Text fontSize="2xl">💭</Text>
      </Box>
      <VStack space={2} alignItems="center">
        <Text fontSize="lg" fontWeight="600" color="gray.800">
          Loading scenarios...
        </Text>
        <Text fontSize="sm" color="gray.600" textAlign="center">
          Preparing your practice environments
        </Text>
      </VStack>
    </VStack>
  </SafeAreaView>
);

const ErrorState: React.FC<{ error: string; onRetry: () => void }> = ({ 
  error, 
  onRetry 
}) => (
  <SafeAreaView style={{ flex: 1, backgroundColor: '#F9FAFB' }}>
    <VStack flex={1} justifyContent="center" alignItems="center" space={4} px={8}>
      <Box
        w={12}
        h={12}
        borderRadius="full"
        bg="red.100"
        justifyContent="center"
        alignItems="center"
      >
        <Text fontSize="2xl">⚠️</Text>
      </Box>
      <VStack space={2} alignItems="center">
        <Text fontSize="lg" fontWeight="600" color="gray.800">
          Something went wrong
        </Text>
        <Text fontSize="sm" color="gray.600" textAlign="center">
          {error}
        </Text>
      </VStack>
      <Button onPress={onRetry} colorScheme="orange" size="md">
        Try Again
      </Button>
    </VStack>
  </SafeAreaView>
);
```

## Premium Integration

### Premium Scenario and Difficulty Gating

The scenario selection feature integrates with RevenueCat subscription system to control access:

```typescript
// src/features/scenario-selection/hooks/usePremiumAccess.ts
import { useSubscriptionStore } from '../../../stores/subscriptionStore';

export const usePremiumAccess = () => {
  const { isPremium } = useSubscriptionStore();
  
  const premiumScenarios = ['gym', 'bar', 'gallery'];
  const premiumDifficulties = ['yellow', 'red'];
  
  const isScenarioAccessible = (scenario: Scenario): boolean => {
    return !scenario.isPremium || isPremium;
  };
  
  const isDifficultyAccessible = (difficulty: 'green' | 'yellow' | 'red'): boolean => {
    return difficulty === 'green' || isPremium;
  };
  
  return { isScenarioAccessible, isDifficultyAccessible, isPremium };
};
```

### Scenario Card Premium Overlay

```typescript
// Update ScenarioCard component to add premium indicators
const ScenarioCard: React.FC<{ scenario: Scenario }> = ({ scenario }) => {
  const { isScenarioAccessible } = usePremiumAccess();
  const navigation = useNavigation();
  
  const handlePress = () => {
    if (!isScenarioAccessible(scenario)) {
      navigation.navigate('PremiumUpgrade', { 
        source: 'scenario_selection',
        blockedItem: scenario.name 
      });
    } else {
      // Normal selection flow
      setSelectedScenario(scenario);
    }
  };
  
  return (
    <Pressable onPress={handlePress}>
      <Box opacity={isScenarioAccessible(scenario) ? 1 : 0.6}>
        {/* Existing scenario content */}
        
        {/* Premium badge overlay */}
        {scenario.isPremium && !isScenarioAccessible(scenario) && (
          <>
            <Box position="absolute" top={2} right={2}>
              <Badge colorScheme="orange" variant="solid">
                <Icon name="lock" size={12} color="white" mr={1} />
                <Text fontSize="xs" color="white">PREMIUM</Text>
              </Badge>
            </Box>
            <Box position="absolute" bottom={0} left={0} right={0} 
                 p={2} bg="rgba(0,0,0,0.8)" borderBottomRadius="xl">
              <Text color="white" fontSize="sm" textAlign="center">
                Unlock with Premium
              </Text>
            </Box>
          </>
        )}
      </Box>
    </Pressable>
  );
};
```

### Difficulty Selection Premium Logic

```typescript
// Update DifficultySelector to show premium requirements
const DifficultySelector: React.FC = () => {
  const { isDifficultyAccessible, isPremium } = usePremiumAccess();
  const navigation = useNavigation();
  
  const difficulties = [
    { level: 'green', name: 'Beginner', available: true },
    { level: 'yellow', name: 'Intermediate', available: isPremium },
    { level: 'red', name: 'Advanced', available: isPremium }
  ];
  
  const handleDifficultyPress = (difficulty) => {
    if (!difficulty.available) {
      navigation.navigate('PremiumUpgrade', { 
        source: 'difficulty_selection',
        blockedItem: `${difficulty.name} difficulty`
      });
    } else {
      selectDifficulty(difficulty.level);
    }
  };
  
  return (
    <VStack space={4}>
      {difficulties.map(diff => (
        <DifficultyCard
          key={diff.level}
          difficulty={diff}
          isLocked={!diff.available}
          onPress={() => handleDifficultyPress(diff)}
        />
      ))}
      
      {/* Premium upsell for locked difficulties */}
      {!isPremium && (
        <Box bg="orange.50" p={3} borderRadius="md" borderWidth={1} borderColor="orange.200">
          <Text fontSize="sm" color="orange.700" textAlign="center">
            <Icon name="star" size={16} color="orange.500" /> 
            Unlock Intermediate & Advanced difficulties with Premium
          </Text>
        </Box>
      )}
    </VStack>
  );
};
```

## Performance Optimizations

### Image Caching and Lazy Loading
```typescript
// src/features/scenario-selection/utils/imageOptimization.ts

import { Image } from 'react-native';
import FastImage from 'react-native-fast-image';

export const preloadScenarioImages = async (scenarios: Scenario[]) => {
  const imageUris = scenarios.map(scenario => scenario.imageUrl);
  
  // Preload images in background
  FastImage.preload(
    imageUris.map(uri => ({
      uri,
      priority: FastImage.priority.normal,
    }))
  );
};

export const OptimizedScenarioImage: React.FC<{
  uri: string;
  alt: string;
  style: any;
}> = ({ uri, alt, style }) => {
  return (
    <FastImage
      source={{ 
        uri,
        priority: FastImage.priority.normal,
        cache: FastImage.cacheControl.immutable,
      }}
      style={style}
      resizeMode={FastImage.resizeMode.cover}
      accessible={true}
      accessibilityRole="image"
      accessibilityLabel={alt}
    />
  );
};
```

### Memory Management
```typescript
// src/features/scenario-selection/hooks/useMemoryOptimization.ts

import { useEffect, useRef } from 'react';

export const useMemoryOptimization = () => {
  const animationRefs = useRef<Set<any>>(new Set());
  
  const registerAnimation = (animation: any) => {
    animationRefs.current.add(animation);
  };
  
  const cleanupAnimations = () => {
    animationRefs.current.forEach(animation => {
      if (animation.stop) {
        animation.stop();
      }
    });
    animationRefs.current.clear();
  };
  
  useEffect(() => {
    return () => {
      cleanupAnimations();
    };
  }, []);
  
  return { registerAnimation, cleanupAnimations };
};
```

## Analytics Integration

### Event Tracking
```typescript
// src/features/scenario-selection/analytics/events.ts

export const scenarioSelectionEvents = {
  // Selection flow events
  scenarioViewed: (scenarioId: string, position: number) => 
    trackEvent('scenario_viewed', {
      scenario_id: scenarioId,
      position_in_grid: position,
      timestamp: Date.now(),
    }),
  
  scenarioSelected: (scenarioId: string, selectionTime: number) =>
    trackEvent('scenario_selected', {
      scenario_id: scenarioId,
      time_to_select_ms: selectionTime,
      selection_method: 'tap', // or 'voice', 'recommendation'
    }),
  
  difficultySelected: (difficulty: string, scenarioId: string) =>
    trackEvent('difficulty_selected', {
      difficulty_level: difficulty,
      scenario_id: scenarioId,
      is_optimal_choice: false, // calculated based on recommendation engine
    }),
  
  // User behavior events
  recommendationFollowed: (scenarioId: string, recommendationType: string) =>
    trackEvent('recommendation_followed', {
      scenario_id: scenarioId,
      recommendation_type: recommendationType,
      user_experience_level: 'beginner', // from user profile
    }),
  
  quickPracticeUsed: (scenarioId: string) =>
    trackEvent('quick_practice_used', {
      scenario_id: scenarioId,
      days_since_last_practice: 0, // calculated
    }),
};
```

## Testing Strategy

### Unit Tests
```typescript
// src/features/scenario-selection/__tests__/ScenarioCard.test.tsx

import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { ScenarioCard } from '../components/ScenarioCard';
import { mockScenario, mockStats } from '../__mocks__/scenarioData';

describe('ScenarioCard', () => {
  const defaultProps = {
    scenario: mockScenario,
    stats: mockStats,
    isSelected: false,
    isRecommended: false,
    onPress: jest.fn(),
  };
  
  test('renders scenario information correctly', () => {
    const { getByText, getByLabelText } = render(
      <ScenarioCard {...defaultProps} />
    );
    
    expect(getByText(mockScenario.name)).toBeTruthy();
    expect(getByText(mockScenario.description)).toBeTruthy();
    expect(getByLabelText(/scenario/i)).toBeTruthy();
  });
  
  test('shows success rate when stats are available', () => {
    const { getByText } = render(
      <ScenarioCard {...defaultProps} />
    );
    
    expect(getByText('75% success')).toBeTruthy();
  });
  
  test('handles press interaction correctly', async () => {
    const mockOnPress = jest.fn();
    const { getByLabelText } = render(
      <ScenarioCard {...defaultProps} onPress={mockOnPress} />
    );
    
    fireEvent.press(getByLabelText(/scenario/i));
    
    await waitFor(() => {
      expect(mockOnPress).toHaveBeenCalledWith(mockScenario);
    });
  });
  
  test('applies accessibility labels correctly', () => {
    const { getByLabelText } = render(
      <ScenarioCard {...defaultProps} isRecommended={true} />
    );
    
    const card = getByLabelText(/recommended for you/i);
    expect(card).toBeTruthy();
  });
});
```

### Integration Tests
```typescript
// src/features/scenario-selection/__tests__/ScenarioSelection.integration.test.tsx

import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { ScenarioSelectionScreen } from '../screens/ScenarioSelectionScreen';
import { useScenarioSelectionStore } from '../store/scenarioSelectionStore';

// Mock navigation
const mockNavigate = jest.fn();
jest.mock('@react-navigation/native', () => ({
  ...jest.requireActual('@react-navigation/native'),
  useNavigation: () => ({ navigate: mockNavigate }),
}));

describe('Scenario Selection Integration', () => {
  beforeEach(() => {
    // Reset store state
    useScenarioSelectionStore.getState().resetSelection();
    mockNavigate.mockClear();
  });
  
  test('completes full scenario selection flow', async () => {
    const { getByText, getByLabelText } = render(
      <NavigationContainer>
        <ScenarioSelectionScreen />
      </NavigationContainer>
    );
    
    // Select a scenario
    const coffeeShopCard = getByLabelText(/coffee shop scenario/i);
    fireEvent.press(coffeeShopCard);
    
    // Verify navigation to difficulty selection
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('DifficultySelection', {
        scenario: expect.objectContaining({
          name: 'Coffee Shop',
        }),
      });
    });
    
    // Verify store state update
    const store = useScenarioSelectionStore.getState();
    expect(store.selectedScenario?.name).toBe('Coffee Shop');
    expect(store.selectionStep).toBe('difficulty');
  });
  
  test('handles recommendation system correctly', () => {
    const { getByText } = render(
      <NavigationContainer>
        <ScenarioSelectionScreen />
      </NavigationContainer>
    );
    
    // Should show recommended section
    expect(getByText('Recommended for You')).toBeTruthy();
  });
});
```

## Related Documentation

- **[README](./README.md)** - Feature overview and specifications
- **[User Journey](./user-journey.md)** - Complete user experience flow
- **[Screen States](./screen-states.md)** - Visual design specifications
- **[Interactions](./interactions.md)** - Animation and interaction details
- **[Accessibility](./accessibility.md)** - Inclusive design specifications

## Deployment Checklist

### Pre-Implementation
- [ ] Design system components are available (cards, buttons, progress indicators)
- [ ] Analytics tracking is set up and tested
- [ ] Image assets are optimized and uploaded to CDN
- [ ] Scenario data is finalized and validated

### Implementation Phase
- [ ] All TypeScript interfaces match design specifications
- [ ] Zustand store handles all state management scenarios
- [ ] Animations are performance-optimized for 60fps
- [ ] Accessibility features are implemented and tested
- [ ] Error handling covers all edge cases

### Testing Phase
- [ ] Unit tests cover all components with >90% coverage
- [ ] Integration tests validate complete user flows
- [ ] Accessibility testing passes WCAG 2.1 AA standards
- [ ] Performance testing meets target metrics
- [ ] User acceptance testing with target personas

### Deployment
- [ ] Feature flags are configured for gradual rollout
- [ ] Analytics dashboards are set up for monitoring
- [ ] Performance monitoring is in place
- [ ] Support documentation is updated
- [ ] Team training is completed

## Performance Targets

### Loading Performance
- **Initial Load**: <2 seconds to display scenario grid
- **Image Loading**: <1 second for cached images, <3 seconds for new images
- **Navigation**: <400ms transition between selection screens
- **Search/Filter**: <200ms response time for real-time filtering

### Memory Usage
- **Baseline**: <50MB for scenario selection feature
- **Image Cache**: <100MB maximum cached images
- **Animation Memory**: <10MB additional during animations
- **Cleanup**: Proper memory cleanup on screen unmount

### Battery Impact
- **Background Processing**: Minimal when app is backgrounded
- **Animation Efficiency**: Hardware-accelerated animations only
- **Network Usage**: Efficient image loading with progressive enhancement

## Last Updated
- **Version 1.0.0**: Complete technical implementation specification
- **Focus**: Production-ready React Native implementation with performance optimization
- **Next**: Development sprint planning and implementation kickoff