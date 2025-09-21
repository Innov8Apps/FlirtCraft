# Pre-Conversation Context Implementation Guide

---
title: Pre-Conversation Context Implementation
description: Technical implementation guide for AI-generated context display and user preparation flow
feature: pre-conversation-context
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ./interactions.md
  - ./accessibility.md
  - ../../design-system/components/context-cards.md
  - ../../design-system/components/buttons.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
  - ../../design-system/tokens/typography.md
dependencies:
  - React Native with Expo
  - NativeBase UI components
  - NativeWind styling
  - Zustand state management
  - OpenRouter API for context generation
status: approved
---

## Overview

This implementation guide provides comprehensive technical specifications for building FlirtCraft's pre-conversation context feature. The system generates AI-powered scenario details, displays them in an accessible card interface, and seamlessly transitions users to conversation with comprehensive preparation.

## Architecture Overview

### Technology Stack

**Frontend Framework:**
- **React Native**: 0.72+ with Expo 52+
- **UI Library**: NativeBase for consistent components
- **Styling**: NativeWind 4.1 for utility-first styling
- **Navigation**: Expo Router for type-safe navigation
- **Animations**: React Native Reanimated 3.0+ for smooth card animations

**State Management:**
- **Global State**: Zustand 4.0+ for context data and generation state
- **Local State**: React hooks for UI-specific state (card expansion, etc.)
- **Context Cache**: AsyncStorage for recent context caching
- **Navigation State**: Expo Router navigation state

**AI Integration:**
- **Primary**: OpenRouter with google/gemini-2.5-flash-lite for context generation
- **Fallback**: OpenRouter with google/gemini-2.0-flash-lite-001
- **Context Generation**: Structured prompts for consistent scenario creation
- **Fallback Content**: Pre-written contexts for popular scenario/difficulty combinations
- **Performance Target**: <3 seconds generation time

## State Management Implementation

### Zustand Store Structure

```typescript
// stores/preConversationStore.ts
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface ScenarioContext {
  id: string;
  scenarioType: 'coffee_shop' | 'bookstore' | 'park' | 'campus' | 'grocery' | 'gym' | 'bar' | 'gallery';
  difficulty: 'green' | 'yellow' | 'red';
  generated: Date;
  partner: {
    ageRange: string;
    style: string;
    activity: string;
    details: string[];
    physicalDescription?: string;
  };
  environment: {
    timeContext: string;
    crowdLevel: string;
    atmosphere: string;
    details: string[];
  };
  bodyLanguage: {
    signals: Array<{
      type: 'positive' | 'neutral' | 'challenging';
      description: string;
    }>;
    overall: string;
    receptivenessLevel: 'high' | 'medium' | 'low';
  };
  conversationStarters: string[];
}

interface PreConversationState {
  // Current context data
  currentContext: ScenarioContext | null;
  isGenerating: boolean;
  generationError: string | null;
  
  // User interaction tracking
  reviewedCards: Set<string>;
  expandedCards: Set<string>;
  selectedStarter: string | null;
  
  // Generation parameters
  scenarioParams: {
    location: string;
    difficulty: string;
    userPreferences?: {
      ageRange?: string;
      targetGender?: string;
    };
  };
  
  // Cache management
  contextCache: Map<string, ScenarioContext>;
  fallbackContexts: Map<string, ScenarioContext>;
  
  // Actions
  generateContext: (params: ScenarioParams) => Promise<void>;
  regenerateContext: () => Promise<void>;
  markCardReviewed: (cardType: string) => void;
  toggleCardExpansion: (cardType: string) => void;
  selectConversationStarter: (starter: string) => void;
  clearContext: () => void;
  cacheContext: (context: ScenarioContext) => void;
  loadFromCache: (cacheKey: string) => ScenarioContext | null;
}

export const usePreConversationStore = create<PreConversationState>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    currentContext: null,
    isGenerating: false,
    generationError: null,
    reviewedCards: new Set(),
    expandedCards: new Set(),
    selectedStarter: null,
    scenarioParams: {
      location: '',
      difficulty: 'green',
    },
    contextCache: new Map(),
    fallbackContexts: new Map(),
    
    // Actions implementation
    generateContext: async (params: ScenarioParams) => {
      set({ isGenerating: true, generationError: null, scenarioParams: params });
      
      try {
        // Check cache first
        const cacheKey = `${params.location}_${params.difficulty}`;
        const cachedContext = get().loadFromCache(cacheKey);
        
        if (cachedContext && isRecentContext(cachedContext)) {
          set({ 
            currentContext: cachedContext, 
            isGenerating: false,
            reviewedCards: new Set(),
            expandedCards: new Set(),
          });
          return;
        }
        
        // Generate new context
        const startTime = Date.now();
        const newContext = await aiContextService.generateContext(params);
        const generationTime = Date.now() - startTime;
        
        // Log performance metrics
        performanceMonitor.trackContextGeneration(generationTime);
        
        // Cache the new context
        get().cacheContext(newContext);
        
        set({ 
          currentContext: newContext, 
          isGenerating: false,
          reviewedCards: new Set(),
          expandedCards: new Set(),
        });
        
      } catch (error) {
        console.error('Context generation failed:', error);
        
        // Try fallback content
        const fallbackContext = get().getFallbackContext(params);
        if (fallbackContext) {
          set({ 
            currentContext: fallbackContext, 
            isGenerating: false,
            generationError: null,
          });
        } else {
          set({ 
            isGenerating: false, 
            generationError: 'Failed to generate context. Please try again.' 
          });
        }
      }
    },
    
    regenerateContext: async () => {
      const params = get().scenarioParams;
      // Force new generation by skipping cache
      await get().generateContext({ ...params, forceNew: true });
    },
    
    markCardReviewed: (cardType: string) => {
      set((state) => ({
        reviewedCards: new Set([...state.reviewedCards, cardType]),
      }));
    },
    
    toggleCardExpansion: (cardType: string) => {
      set((state) => {
        const newExpanded = new Set(state.expandedCards);
        if (newExpanded.has(cardType)) {
          newExpanded.delete(cardType);
        } else {
          newExpanded.add(cardType);
        }
        return { expandedCards: newExpanded };
      });
    },
    
    selectConversationStarter: (starter: string) => {
      set({ selectedStarter: starter });
      // Copy to clipboard or input field
      copyToClipboard(starter);
    },
    
    clearContext: () => {
      set({
        currentContext: null,
        reviewedCards: new Set(),
        expandedCards: new Set(),
        selectedStarter: null,
        generationError: null,
      });
    },
    
    cacheContext: (context: ScenarioContext) => {
      const cacheKey = `${context.scenarioType}_${context.difficulty}`;
      set((state) => ({
        contextCache: new Map([...state.contextCache, [cacheKey, context]]),
      }));
      
      // Persist to AsyncStorage
      AsyncStorage.setItem(`context_cache_${cacheKey}`, JSON.stringify(context));
    },
    
    loadFromCache: (cacheKey: string) => {
      return get().contextCache.get(cacheKey) || null;
    },
    
    // Additional helper methods...
  }))
);

// Helper functions
const isRecentContext = (context: ScenarioContext): boolean => {
  const ageMs = Date.now() - context.generated.getTime();
  const maxAgeMs = 5 * 60 * 1000; // 5 minutes
  return ageMs < maxAgeMs;
};
```

## AI Context Generation Service

### OpenRouter Integration for Context Generation

```typescript
// services/aiContextService.ts
import axios from 'axios';
import { ScenarioContext, ScenarioParams } from '../types';

class AIContextService {
  private apiKey: string;
  private baseUrl: string;
  private primaryModel: string;
  private fallbackModel: string;
  private generationCache = new Map<string, ScenarioContext>();

  constructor() {
    this.apiKey = process.env.EXPO_PUBLIC_OPENROUTER_API_KEY!;
    this.baseUrl = 'https://openrouter.ai/api/v1/chat/completions';
    this.primaryModel = 'google/gemini-2.5-flash-lite';
    this.fallbackModel = 'google/gemini-2.0-flash-lite-001';
  }

  async generateContext(params: ScenarioParams): Promise<ScenarioContext> {
    const prompt = this.buildContextPrompt(params);
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'HTTP-Referer': 'https://flirtcraft.app',
      'X-Title': 'FlirtCraft',
      'Content-Type': 'application/json'
    };

    const messages = [
      { role: 'system', content: 'You are a creative scenario generator for conversation training. Always respond in valid JSON format.' },
      { role: 'user', content: prompt }
    ];

    try {
      // Try primary model first
      let rawContext;
      try {
        const response = await axios.post(this.baseUrl, {
          model: this.primaryModel,
          messages: messages,
          temperature: 0.8, // Higher creativity for varied scenarios
          max_tokens: 800,
          response_format: { type: 'json_object' },
          reasoning: { enabled: true }
        }, { headers });

        rawContext = JSON.parse(response.data.choices[0].message.content);
      } catch (primaryError) {
        console.warn('Primary model failed, trying fallback:', primaryError);
        // Use fallback model
        const response = await axios.post(this.baseUrl, {
          model: this.fallbackModel,
          messages: messages,
          temperature: 0.8,
          max_tokens: 800,
          response_format: { type: 'json_object' }
        }, { headers });

        rawContext = JSON.parse(response.data.choices[0].message.content);
      }

      const validatedContext = this.validateAndStructureContext(rawContext, params);
      
      return validatedContext;
      
    } catch (error) {
      console.error('AI context generation failed:', error);
      throw new Error('Context generation failed');
    }
  }
  
  private buildContextPrompt(params: ScenarioParams): string {
    const locationDescriptions = {
      coffee_shop: 'busy coffee shop with comfortable seating and ambient music',
      bar: 'trendy bar with good atmosphere and moderate noise level',
      bookstore: 'cozy bookstore with quiet reading nooks and literary atmosphere',
      park: 'scenic park with walking paths and outdoor seating areas',
      gym: 'modern fitness center with various workout areas',
    };
    
    const difficultyInstructions = {
      green: 'Create a receptive, encouraging person showing clear interest signs',
      yellow: 'Create a neutral person with mixed signals - some positive, some reserved',
      red: 'Create a person who is polite but distracted/busy with challenging body language',
    };
    
    return `You are creating a realistic romantic conversation practice scenario for a dating confidence app.

SCENARIO PARAMETERS:
- Location: ${locationDescriptions[params.location]}
- Difficulty: ${params.difficulty} (${difficultyInstructions[params.difficulty]})
- User preferences: ${JSON.stringify(params.userPreferences || {})}

Create a detailed JSON response with this exact structure:
{
  "partner": {
    "ageRange": "Early 20s/Mid 20s/Late 20s/Early 30s/etc",
    "style": "Brief clothing/style description (1-2 words)",
    "activity": "What they're currently doing (reading, working on laptop, etc)",
    "details": ["Observable detail 1", "Observable detail 2", "Observable detail 3"],
    "physicalDescription": "Brief, respectful physical appearance note"
  },
  "environment": {
    "timeContext": "Day and time (e.g., 'Tuesday afternoon, 2:30 PM')",
    "crowdLevel": "Busy/Moderate/Quiet with brief description",
    "atmosphere": "Overall mood and energy of the space",
    "details": ["Environmental detail 1", "Environmental detail 2", "Environmental detail 3"]
  },
  "bodyLanguage": {
    "signals": [
      {
        "type": "positive/neutral/challenging",
        "description": "Specific observable behavior"
      }
    ],
    "overall": "Summary of their general receptiveness",
    "receptivenessLevel": "high/medium/low"
  },
  "conversationStarters": [
    "Natural opener 1 that fits the scenario",
    "Natural opener 2 that references observable details",
    "Natural opener 3 that fits the environment",
    "Natural opener 4 as backup option"
  ]
}

QUALITY REQUIREMENTS:
- Make details specific and observable (not assumptions about personality)
- Ensure body language matches the difficulty level appropriately
- Create conversation starters that naturally fit the scenario
- Keep all content appropriate and respectful
- Make the scenario feel realistic and relatable
- Include 2-3 body language signals that match difficulty level
- Ensure environmental details enhance the scenario authenticity`;
  }
  
  private validateAndStructureContext(
    rawContext: any, 
    params: ScenarioParams
  ): ScenarioContext {
    // Validate required fields and structure
    const requiredFields = ['partner', 'environment', 'bodyLanguage', 'conversationStarters'];
    for (const field of requiredFields) {
      if (!rawContext[field]) {
        throw new Error(`Missing required field: ${field}`);
      }
    }
    
    // Structure and validate the context
    const structuredContext: ScenarioContext = {
      id: generateContextId(),
      scenarioType: params.location,
      difficulty: params.difficulty,
      generated: new Date(),
      partner: {
        ageRange: rawContext.partner.ageRange || 'Mid-20s',
        style: rawContext.partner.style || 'Casual',
        activity: rawContext.partner.activity || 'Reading',
        details: rawContext.partner.details || [],
        physicalDescription: rawContext.partner.physicalDescription,
      },
      environment: {
        timeContext: rawContext.environment.timeContext || 'Afternoon',
        crowdLevel: rawContext.environment.crowdLevel || 'Moderate',
        atmosphere: rawContext.environment.atmosphere || 'Comfortable',
        details: rawContext.environment.details || [],
      },
      bodyLanguage: {
        signals: rawContext.bodyLanguage.signals || [],
        overall: rawContext.bodyLanguage.overall || 'Generally approachable',
        receptivenessLevel: rawContext.bodyLanguage.receptivenessLevel || 'medium',
      },
      conversationStarters: rawContext.conversationStarters || [
        'Hi there! How are you enjoying your time here?',
        'I love the atmosphere in this place.',
        'That looks interesting - would you recommend it?',
      ],
    };
    
    // Additional validation
    this.validateContextQuality(structuredContext);
    
    return structuredContext;
  }
  
  private validateContextQuality(context: ScenarioContext): void {
    // Ensure conversation starters are appropriate length
    context.conversationStarters = context.conversationStarters.map(starter => 
      starter.length > 100 ? starter.substring(0, 100) + '...' : starter
    );
    
    // Ensure we have enough body language signals
    if (context.bodyLanguage.signals.length < 2) {
      throw new Error('Insufficient body language signals generated');
    }
    
    // Validate difficulty alignment
    const positiveSignals = context.bodyLanguage.signals.filter(s => s.type === 'positive').length;
    const challengingSignals = context.bodyLanguage.signals.filter(s => s.type === 'challenging').length;
    
    if (context.difficulty === 'green' && positiveSignals < 1) {
      throw new Error('Green difficulty should have at least one positive signal');
    }
    
    if (context.difficulty === 'red' && challengingSignals < 1) {
      throw new Error('Red difficulty should have at least one challenging signal');
    }
  }
}

export const aiContextService = new AIContextService();

// Utility functions
const generateContextId = (): string => {
  return `context_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};
```

### Fallback Content System

```typescript
// services/fallbackContextService.ts
class FallbackContextService {
  private fallbackContexts: Map<string, ScenarioContext> = new Map();
  
  constructor() {
    this.initializeFallbackContexts();
  }
  
  private initializeFallbackContexts() {
    // Coffee shop scenarios
    this.fallbackContexts.set('coffee_shop_green', {
      id: 'fallback_coffee_green',
      scenarioType: 'coffee_shop',
      difficulty: 'green',
      generated: new Date(),
      partner: {
        ageRange: 'Mid-20s',
        style: 'Casual-professional',
        activity: 'Reading a paperback novel while sipping a latte',
        details: [
          'Has a genuine smile when she looks up',
          'Makes brief eye contact with people passing by',
          'Seems relaxed and approachable'
        ],
        physicalDescription: 'Friendly appearance with an easy-going demeanor'
      },
      environment: {
        timeContext: 'Saturday afternoon, 2:00 PM',
        crowdLevel: 'Comfortably busy with a good energy',
        atmosphere: 'Warm and inviting with soft jazz playing',
        details: [
          'Soft lighting creates a cozy ambiance',
          'The scent of freshly ground coffee fills the air',
          'Several people working on laptops at nearby tables'
        ]
      },
      bodyLanguage: {
        signals: [
          {
            type: 'positive',
            description: 'Looks up and makes friendly eye contact when people approach nearby'
          },
          {
            type: 'positive',
            description: 'Has an open posture with relaxed shoulders'
          },
          {
            type: 'neutral',
            description: 'Occasionally checks her phone but isn\'t glued to it'
          }
        ],
        overall: 'Appears approachable and open to friendly interaction',
        receptivenessLevel: 'high'
      },
      conversationStarters: [
        'That book looks interesting - would you recommend it?',
        'I love the atmosphere here. Do you come here often?',
        'The coffee smells amazing. Have you tried their specialty drinks?',
        'Excuse me, is this seat taken? This place is so popular!'
      ]
    });
    
    // Add more fallback contexts for different scenarios/difficulties
    this.addMoreFallbackContexts();
  }
  
  getFallbackContext(params: ScenarioParams): ScenarioContext | null {
    const key = `${params.location}_${params.difficulty}`;
    return this.fallbackContexts.get(key) || null;
  }
  
  private addMoreFallbackContexts() {
    // Add fallback contexts for all scenario/difficulty combinations
    // This would include coffee_shop_yellow, coffee_shop_red, bar_green, etc.
  }
}

export const fallbackContextService = new FallbackContextService();
```

## Component Implementation

### Main Pre-Conversation Screen

```tsx
// screens/PreConversationScreen.tsx
import React, { useEffect, useState } from 'react';
import { ScrollView, Alert } from 'react-native';
import { Box, VStack, HStack, Text, Button, IconButton, Spinner } from 'native-base';
import { ArrowLeft, HelpCircle } from 'lucide-react-native';
import { usePreConversationStore } from '../stores/preConversationStore';
import { ContextCard } from '../components/ContextCard';
import { ContextGenerationLoading } from '../components/ContextGenerationLoading';
import { useNavigation, useRoute } from '@react-navigation/native';

interface PreConversationScreenProps {
  route: {
    params: {
      scenarioParams: ScenarioParams;
    };
  };
}

export const PreConversationScreen: React.FC<PreConversationScreenProps> = ({ route }) => {
  const navigation = useNavigation();
  const { scenarioParams } = route.params;
  
  const {
    currentContext,
    isGenerating,
    generationError,
    reviewedCards,
    generateContext,
    regenerateContext,
    clearContext,
  } = usePreConversationStore();
  
  const [showHelp, setShowHelp] = useState(false);
  
  // Generate context on screen mount
  useEffect(() => {
    generateContext(scenarioParams);
    
    return () => {
      // Cleanup on unmount
      clearContext();
    };
  }, [scenarioParams]);
  
  const handleStartConversation = () => {
    if (!currentContext) return;
    
    navigation.navigate('Conversation', {
      contextData: currentContext,
    });
  };
  
  const handleRegenerate = async () => {
    try {
      await regenerateContext();
    } catch (error) {
      Alert.alert('Error', 'Failed to generate new context. Please try again.');
    }
  };
  
  const handleBackPress = () => {
    Alert.alert(
      'Leave Preparation?',
      'Your generated context will be lost. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Leave', onPress: () => navigation.goBack() },
      ]
    );
  };
  
  const allCardsReviewed = reviewedCards.size === 4;
  
  if (isGenerating) {
    return <ContextGenerationLoading />;
  }
  
  if (generationError) {
    return (
      <ErrorScreen 
        error={generationError}
        onRetry={() => generateContext(scenarioParams)}
        onBack={handleBackPress}
      />
    );
  }
  
  if (!currentContext) {
    return <EmptyState onBack={handleBackPress} />;
  }
  
  return (
    <Box flex={1} bg="gray.50" safeArea>
      {/* Header */}
      <HStack
        justifyContent="space-between"
        alignItems="center"
        px={4}
        py={3}
        bg="white"
        shadow={1}
      >
        <IconButton
          icon={<ArrowLeft size={24} color="gray.700" />}
          onPress={handleBackPress}
          accessible={true}
          accessibilityLabel="Return to scenario selection"
        />
        
        <VStack alignItems="center" space={1}>
          <Text fontSize="sm" fontWeight="medium" color="gray.700">
            Review Your Scenario
          </Text>
          <ProgressIndicator reviewedCards={reviewedCards.size} totalCards={4} />
        </VStack>
        
        <IconButton
          icon={<HelpCircle size={24} color="gray.700" />}
          onPress={() => setShowHelp(true)}
          accessible={true}
          accessibilityLabel="Get help understanding context"
        />
      </HStack>
      
      {/* Content */}
      <VStack flex={1}>
        <ScrollView
          flex={1}
          px={4}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{ paddingVertical: 20 }}
        >
          <VStack space={4}>
            <ContextCard
              type="partner"
              data={currentContext.partner}
              cardNumber={1}
              onReviewed={() => usePreConversationStore.getState().markCardReviewed('partner')}
            />
            
            <ContextCard
              type="environment"
              data={currentContext.environment}
              cardNumber={2}
              onReviewed={() => usePreConversationStore.getState().markCardReviewed('environment')}
            />
            
            <ContextCard
              type="bodyLanguage"
              data={currentContext.bodyLanguage}
              cardNumber={3}
              onReviewed={() => usePreConversationStore.getState().markCardReviewed('bodyLanguage')}
            />
            
            <ContextCard
              type="starters"
              data={currentContext.conversationStarters}
              cardNumber={4}
              onReviewed={() => usePreConversationStore.getState().markCardReviewed('starters')}
              onStarterSelect={(starter) => usePreConversationStore.getState().selectConversationStarter(starter)}
            />
          </VStack>
        </ScrollView>
        
        {/* Action Buttons */}
        <VStack
          space={3}
          px={4}
          py={4}
          bg="white"
          borderTopWidth={1}
          borderTopColor="gray.200"
        >
          <Button
            size="lg"
            bg="orange.500"
            _pressed={{ bg: "orange.600" }}
            disabled={!allCardsReviewed}
            onPress={handleStartConversation}
            accessible={true}
            accessibilityLabel={allCardsReviewed ? "Start conversation" : "Review all cards before starting"}
          >
            <Text fontSize="md" fontWeight="semibold" color="white">
              Start Conversation
            </Text>
          </Button>
          
          <HStack space={3}>
            <Button
              flex={1}
              variant="outline"
              borderColor="orange.200"
              _pressed={{ bg: "orange.50" }}
              onPress={handleRegenerate}
              isLoading={isGenerating}
            >
              <Text fontSize="sm" color="orange.600">
                Generate New Context
              </Text>
            </Button>
            
            <Button
              flex={1}
              variant="ghost"
              _pressed={{ bg: "gray.100" }}
              onPress={handleBackPress}
            >
              <Text fontSize="sm" color="gray.600">
                Back to Scenarios
              </Text>
            </Button>
          </HStack>
        </VStack>
      </VStack>
      
      {/* Help Modal */}
      {showHelp && (
        <HelpModal
          visible={showHelp}
          onClose={() => setShowHelp(false)}
        />
      )}
    </Box>
  );
};
```

### Context Card Component

```tsx
// components/ContextCard.tsx
import React, { useState, useRef, useEffect } from 'react';
import { Pressable } from 'react-native';
import { Box, VStack, HStack, Text, Icon, Badge } from 'native-base';
import { User, MapPin, Eye, MessageCircle, ChevronDown } from 'lucide-react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  Layout,
  FadeInDown,
} from 'react-native-reanimated';
import { useIntersectionObserver } from '../hooks/useIntersectionObserver';

interface ContextCardProps {
  type: 'partner' | 'environment' | 'bodyLanguage' | 'starters';
  data: any;
  cardNumber: number;
  onReviewed: () => void;
  onStarterSelect?: (starter: string) => void;
}

export const ContextCard: React.FC<ContextCardProps> = ({
  type,
  data,
  cardNumber,
  onReviewed,
  onStarterSelect,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [hasBeenViewed, setHasBeenViewed] = useState(false);
  const cardRef = useRef(null);
  
  const scale = useSharedValue(1);
  const chevronRotation = useSharedValue(0);
  
  // Track when card comes into view
  const { isIntersecting } = useIntersectionObserver(cardRef, { threshold: 0.7 });
  
  useEffect(() => {
    if (isIntersecting && !hasBeenViewed) {
      setHasBeenViewed(true);
      onReviewed();
    }
  }, [isIntersecting, hasBeenViewed, onReviewed]);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  
  const chevronStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${chevronRotation.value}deg` }],
  }));
  
  const handleCardPress = () => {
    scale.value = withSpring(0.98, {}, () => {
      scale.value = withSpring(1);
    });
  };
  
  const toggleExpansion = () => {
    const newExpanded = !isExpanded;
    setIsExpanded(newExpanded);
    chevronRotation.value = withSpring(newExpanded ? 180 : 0);
  };
  
  const getCardConfig = () => {
    const configs = {
      partner: {
        icon: User,
        title: 'Your Practice Partner',
        iconBg: 'orange.100',
        iconColor: 'orange.600',
      },
      environment: {
        icon: MapPin,
        title: 'Environment & Setting',
        iconBg: 'green.100',
        iconColor: 'green.600',
      },
      bodyLanguage: {
        icon: Eye,
        title: 'Body Language Signals',
        iconBg: 'blue.100',
        iconColor: 'blue.600',
      },
      starters: {
        icon: MessageCircle,
        title: 'Conversation Starters',
        iconBg: 'purple.100',
        iconColor: 'purple.600',
      },
    };
    return configs[type];
  };
  
  const config = getCardConfig();
  const IconComponent = config.icon;
  
  return (
    <Animated.View
      ref={cardRef}
      entering={FadeInDown.delay((cardNumber - 1) * 200)}
      layout={Layout.springify()}
      style={animatedStyle}
    >
      <Pressable onPress={handleCardPress}>
        <Box
          bg="white"
          borderRadius="xl"
          p={5}
          shadow={2}
          borderWidth={hasBeenViewed ? 2 : 0}
          borderColor={hasBeenViewed ? "orange.200" : "transparent"}
        >
          <HStack space={4} alignItems="flex-start">
            {/* Icon */}
            <Box
              w={12}
              h={12}
              bg={config.iconBg}
              borderRadius="full"
              alignItems="center"
              justifyContent="center"
            >
              <IconComponent size={24} color={config.iconColor} />
            </Box>
            
            {/* Content */}
            <VStack flex={1} space={3}>
              {/* Header */}
              <HStack justifyContent="space-between" alignItems="center">
                <Text fontSize="lg" fontWeight="semibold" color="gray.800">
                  {config.title}
                </Text>
                
                <Pressable onPress={toggleExpansion}>
                  <Animated.View style={chevronStyle}>
                    <ChevronDown size={20} color="gray.500" />
                  </Animated.View>
                </Pressable>
              </HStack>
              
              {/* Card-specific content */}
              {type === 'partner' && <PartnerContent data={data} expanded={isExpanded} />}
              {type === 'environment' && <EnvironmentContent data={data} expanded={isExpanded} />}
              {type === 'bodyLanguage' && <BodyLanguageContent data={data} expanded={isExpanded} />}
              {type === 'starters' && (
                <StartersContent 
                  data={data} 
                  expanded={isExpanded} 
                  onStarterSelect={onStarterSelect}
                />
              )}
            </VStack>
          </HStack>
        </Box>
      </Pressable>
    </Animated.View>
  );
};

// Content components for each card type
const PartnerContent: React.FC<{ data: any; expanded: boolean }> = ({ data, expanded }) => (
  <VStack space={2}>
    <Text fontSize="md" color="gray.700">
      {data.ageRange} • {data.style}
    </Text>
    
    <Text fontSize="md" color="gray.600" lineHeight={22}>
      {data.activity}
    </Text>
    
    {expanded && (
      <VStack space={1} mt={2}>
        {data.details.map((detail: string, index: number) => (
          <Text key={index} fontSize="sm" color="gray.600">
            • {detail}
          </Text>
        ))}
      </VStack>
    )}
  </VStack>
);

const EnvironmentContent: React.FC<{ data: any; expanded: boolean }> = ({ data, expanded }) => (
  <VStack space={2}>
    <HStack justifyContent="space-between" alignItems="center">
      <Text fontSize="md" color="gray.700">
        {data.timeContext}
      </Text>
      <Badge colorScheme="gray" variant="subtle">
        {data.crowdLevel}
      </Badge>
    </HStack>
    
    <Text fontSize="md" color="gray.600" lineHeight={22}>
      {data.atmosphere}
    </Text>
    
    {expanded && (
      <VStack space={1} mt={2}>
        {data.details.map((detail: string, index: number) => (
          <Text key={index} fontSize="sm" color="gray.600">
            • {detail}
          </Text>
        ))}
      </VStack>
    )}
  </VStack>
);

const BodyLanguageContent: React.FC<{ data: any; expanded: boolean }> = ({ data, expanded }) => {
  const getSignalColor = (type: string) => {
    switch (type) {
      case 'positive': return 'green.500';
      case 'neutral': return 'yellow.500';
      case 'challenging': return 'red.500';
      default: return 'gray.400';
    }
  };
  
  return (
    <VStack space={3}>
      {data.signals.map((signal: any, index: number) => (
        <HStack key={index} space={3} alignItems="flex-start">
          <Box
            w={3}
            h={3}
            bg={getSignalColor(signal.type)}
            borderRadius="full"
            mt={2}
          />
          <VStack flex={1} space={1}>
            <Text fontSize="sm" fontWeight="medium" color="gray.700">
              {signal.type === 'positive' ? 'Encouraging Signal' : 
               signal.type === 'neutral' ? 'Neutral Signal' : 'Cautious Signal'}
            </Text>
            <Text fontSize="sm" color="gray.600" lineHeight={18}>
              {signal.description}
            </Text>
          </VStack>
        </HStack>
      ))}
      
      {expanded && (
        <Box
          bg="gray.50"
          borderRadius="lg"
          p={3}
          borderLeftWidth={3}
          borderLeftColor="orange.500"
          mt={2}
        >
          <Text fontSize="sm" fontWeight="medium" color="gray.700">
            Overall Assessment
          </Text>
          <Text fontSize="sm" color="gray.600" mt={1}>
            {data.overall}
          </Text>
        </Box>
      )}
    </VStack>
  );
};

const StartersContent: React.FC<{ 
  data: string[]; 
  expanded: boolean; 
  onStarterSelect?: (starter: string) => void 
}> = ({ data, expanded, onStarterSelect }) => (
  <VStack space={3}>
    <Text fontSize="sm" color="gray.600" mb={2}>
      Choose one to break the ice, or use as inspiration:
    </Text>
    
    {data.map((starter: string, index: number) => (
      <ConversationStarterOption
        key={index}
        starter={starter}
        index={index}
        onSelect={() => onStarterSelect?.(starter)}
      />
    ))}
    
    {expanded && (
      <Box bg="purple.50" borderRadius="lg" p={3} mt={2}>
        <Text fontSize="xs" color="purple.700" textAlign="center">
          💡 Tap any starter to select it, or create your own!
        </Text>
      </Box>
    )}
  </VStack>
);
```

### Context Generation Loading Component

```tsx
// components/ContextGenerationLoading.tsx
import React, { useEffect } from 'react';
import { Box, VStack, Text } from 'native-base';
import { Sparkles } from 'lucide-react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withTiming,
  withSequence,
  Easing,
} from 'react-native-reanimated';

export const ContextGenerationLoading: React.FC = () => {
  const sparkleScale = useSharedValue(1);
  const sparkleRotation = useSharedValue(0);
  const progressWidth = useSharedValue(0);
  
  useEffect(() => {
    // Sparkle animation
    sparkleScale.value = withRepeat(
      withSequence(
        withTiming(1.2, { duration: 1000, easing: Easing.inOut(Easing.ease) }),
        withTiming(1, { duration: 1000, easing: Easing.inOut(Easing.ease) })
      ),
      -1,
      false
    );
    
    sparkleRotation.value = withRepeat(
      withTiming(360, { duration: 3000, easing: Easing.linear }),
      -1,
      false
    );
    
    // Progress bar animation
    progressWidth.value = withRepeat(
      withSequence(
        withTiming(100, { duration: 2000 }),
        withTiming(0, { duration: 100 })
      ),
      -1,
      false
    );
  }, []);
  
  const sparkleStyle = useAnimatedStyle(() => ({
    transform: [
      { scale: sparkleScale.value },
      { rotate: `${sparkleRotation.value}deg` }
    ],
  }));
  
  const progressStyle = useAnimatedStyle(() => ({
    width: `${progressWidth.value}%`,
  }));
  
  return (
    <Box flex={1} bg="gray.50" justifyContent="center" alignItems="center" px={6}>
      <VStack space={6} alignItems="center">
        {/* Animated sparkle icon */}
        <Animated.View style={sparkleStyle}>
          <Box
            w={16}
            h={16}
            bg="orange.100"
            borderRadius="full"
            alignItems="center"
            justifyContent="center"
          >
            <Sparkles size={32} color="#EA580C" />
          </Box>
        </Animated.View>
        
        {/* Loading text */}
        <VStack space={3} alignItems="center">
          <Text fontSize="xl" fontWeight="semibold" color="gray.800" textAlign="center">
            Creating your scenario...
          </Text>
          <Text 
            fontSize="md" 
            color="gray.600" 
            textAlign="center" 
            maxW="280px"
            lineHeight={22}
          >
            Our AI is crafting the perfect practice situation for you
          </Text>
        </VStack>
        
        {/* Animated progress bar */}
        <Box w="200px" h={1} bg="orange.200" borderRadius="full" overflow="hidden">
          <Animated.View 
            style={[
              { height: '100%', backgroundColor: '#F97316', borderRadius: 2 },
              progressStyle
            ]} 
          />
        </Box>
      </VStack>
    </Box>
  );
};
```

## Performance Optimization

### Context Caching Strategy

```typescript
// services/contextCacheService.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

class ContextCacheService {
  private memoryCache = new Map<string, ScenarioContext>();
  private readonly CACHE_PREFIX = 'flirtcraft_context_';
  private readonly MAX_MEMORY_CACHE = 10;
  private readonly CACHE_EXPIRY_MS = 24 * 60 * 60 * 1000; // 24 hours
  
  async cacheContext(context: ScenarioContext): Promise<void> {
    const cacheKey = this.getCacheKey(context);
    
    // Store in memory cache
    this.memoryCache.set(cacheKey, context);
    
    // Limit memory cache size
    if (this.memoryCache.size > this.MAX_MEMORY_CACHE) {
      const firstKey = this.memoryCache.keys().next().value;
      this.memoryCache.delete(firstKey);
    }
    
    // Store in persistent cache
    try {
      const cacheData = {
        context,
        timestamp: Date.now(),
      };
      await AsyncStorage.setItem(
        this.CACHE_PREFIX + cacheKey,
        JSON.stringify(cacheData)
      );
    } catch (error) {
      console.warn('Failed to cache context to storage:', error);
    }
  }
  
  async getCachedContext(params: ScenarioParams): Promise<ScenarioContext | null> {
    const cacheKey = this.getCacheKey(params);
    
    // Check memory cache first
    const memoryResult = this.memoryCache.get(cacheKey);
    if (memoryResult && this.isValidCache(memoryResult)) {
      return memoryResult;
    }
    
    // Check persistent cache
    try {
      const cached = await AsyncStorage.getItem(this.CACHE_PREFIX + cacheKey);
      if (cached) {
        const cacheData = JSON.parse(cached);
        
        if (this.isValidCacheData(cacheData)) {
          // Move to memory cache
          this.memoryCache.set(cacheKey, cacheData.context);
          return cacheData.context;
        } else {
          // Clean up expired cache
          await AsyncStorage.removeItem(this.CACHE_PREFIX + cacheKey);
        }
      }
    } catch (error) {
      console.warn('Failed to retrieve cached context:', error);
    }
    
    return null;
  }
  
  private getCacheKey(contextOrParams: ScenarioContext | ScenarioParams): string {
    if ('scenarioType' in contextOrParams) {
      // It's a ScenarioContext
      return `${contextOrParams.scenarioType}_${contextOrParams.difficulty}`;
    } else {
      // It's ScenarioParams
      return `${contextOrParams.location}_${contextOrParams.difficulty}`;
    }
  }
  
  private isValidCache(context: ScenarioContext): boolean {
    const age = Date.now() - context.generated.getTime();
    return age < this.CACHE_EXPIRY_MS;
  }
  
  private isValidCacheData(cacheData: any): boolean {
    if (!cacheData.timestamp || !cacheData.context) return false;
    
    const age = Date.now() - cacheData.timestamp;
    return age < this.CACHE_EXPIRY_MS;
  }
  
  async clearExpiredCache(): Promise<void> {
    try {
      const keys = await AsyncStorage.getAllKeys();
      const contextKeys = keys.filter(key => key.startsWith(this.CACHE_PREFIX));
      
      for (const key of contextKeys) {
        const cached = await AsyncStorage.getItem(key);
        if (cached) {
          const cacheData = JSON.parse(cached);
          if (!this.isValidCacheData(cacheData)) {
            await AsyncStorage.removeItem(key);
          }
        }
      }
    } catch (error) {
      console.warn('Failed to clear expired cache:', error);
    }
  }
}

export const contextCacheService = new ContextCacheService();
```

### Performance Monitoring

```typescript
// services/performanceMonitor.ts
class PerformanceMonitor {
  trackContextGeneration(duration: number, success: boolean, method: 'ai' | 'cache' | 'fallback') {
    console.log(`Context generation: ${duration}ms (${method}) - ${success ? 'success' : 'failed'}`);
    
    // Report to analytics
    this.reportMetric('context_generation_time', {
      duration,
      success,
      method,
      timestamp: Date.now(),
    });
  }
  
  trackCardReview(cardType: string, timeSpent: number) {
    console.log(`Card review: ${cardType} - ${timeSpent}ms`);
    
    this.reportMetric('card_review_time', {
      cardType,
      timeSpent,
      timestamp: Date.now(),
    });
  }
  
  trackUserFlow(event: string, metadata?: any) {
    console.log(`User flow: ${event}`, metadata);
    
    this.reportMetric('user_flow_event', {
      event,
      metadata,
      timestamp: Date.now(),
    });
  }
  
  private reportMetric(event: string, data: any) {
    // Integration with analytics service (Firebase, Mixpanel, etc.)
    // analytics.track(event, data);
  }
}

export const performanceMonitor = new PerformanceMonitor();
```

## Testing Implementation

### Unit Tests

```typescript
// __tests__/preConversationStore.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { usePreConversationStore } from '../stores/preConversationStore';

// Mock AI service
jest.mock('../services/aiContextService', () => ({
  aiContextService: {
    generateContext: jest.fn(),
  },
}));

describe('PreConversationStore', () => {
  beforeEach(() => {
    usePreConversationStore.getState().clearContext();
  });
  
  it('should generate context successfully', async () => {
    const mockContext = {
      id: 'test-context',
      scenarioType: 'coffee_shop',
      difficulty: 'green',
      // ... other properties
    };
    
    const aiService = require('../services/aiContextService').aiContextService;
    aiService.generateContext.mockResolvedValue(mockContext);
    
    const { result } = renderHook(() => usePreConversationStore());
    
    await act(async () => {
      await result.current.generateContext({
        location: 'coffee_shop',
        difficulty: 'green',
      });
    });
    
    expect(result.current.currentContext).toEqual(mockContext);
    expect(result.current.isGenerating).toBe(false);
  });
  
  it('should mark cards as reviewed', () => {
    const { result } = renderHook(() => usePreConversationStore());
    
    act(() => {
      result.current.markCardReviewed('partner');
      result.current.markCardReviewed('environment');
    });
    
    expect(result.current.reviewedCards.has('partner')).toBe(true);
    expect(result.current.reviewedCards.has('environment')).toBe(true);
    expect(result.current.reviewedCards.size).toBe(2);
  });
});
```

### Integration Tests

```typescript
// __tests__/PreConversationScreen.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { PreConversationScreen } from '../screens/PreConversationScreen';

const mockRoute = {
  params: {
    scenarioParams: {
      location: 'coffee_shop',
      difficulty: 'green',
    },
  },
};

describe('PreConversationScreen', () => {
  it('should display loading state initially', () => {
    const { getByText } = render(<PreConversationScreen route={mockRoute} />);
    expect(getByText('Creating your scenario...')).toBeTruthy();
  });
  
  it('should display context cards after generation', async () => {
    const { getByText } = render(<PreConversationScreen route={mockRoute} />);
    
    await waitFor(() => {
      expect(getByText('Your Practice Partner')).toBeTruthy();
      expect(getByText('Environment & Setting')).toBeTruthy();
      expect(getByText('Body Language Signals')).toBeTruthy();
      expect(getByText('Conversation Starters')).toBeTruthy();
    });
  });
  
  it('should enable start button after all cards reviewed', async () => {
    const { getByText, getByTestId } = render(<PreConversationScreen route={mockRoute} />);
    
    // Wait for context to load
    await waitFor(() => {
      expect(getByText('Your Practice Partner')).toBeTruthy();
    });
    
    // Start button should be disabled initially
    const startButton = getByText('Start Conversation');
    expect(startButton).toBeDisabled();
    
    // Simulate card reviews
    fireEvent.scroll(getByTestId('context-scroll'), {
      nativeEvent: {
        contentOffset: { y: 1000 }, // Scroll to trigger all card reviews
      },
    });
    
    await waitFor(() => {
      expect(startButton).not.toBeDisabled();
    });
  });
});
```

## Security and Privacy Implementation

### Data Privacy Protection

```typescript
// services/privacyService.ts
class PrivacyService {
  // Don't store personal context data persistently
  sanitizeContextForStorage(context: ScenarioContext): Partial<ScenarioContext> {
    return {
      id: context.id,
      scenarioType: context.scenarioType,
      difficulty: context.difficulty,
      generated: context.generated,
      // Don't include detailed personal descriptions
    };
  }
  
  // Clear sensitive data on app backgrounding
  clearSensitiveData(): void {
    usePreConversationStore.getState().clearContext();
    contextCacheService.clearMemoryCache();
  }
  
  // Encrypt context data if needed
  encryptContext(context: ScenarioContext): string {
    // Implementation depends on encryption library
    return JSON.stringify(context); // Simplified
  }
}

export const privacyService = new PrivacyService();
```

---

## Premium Integration

### Daily Conversation Limit Check

The pre-conversation context feature must check daily usage limits before generating context:

```typescript
// src/features/pre-conversation-context/hooks/useDailyLimit.ts
import { useSubscriptionStore } from '../../../stores/subscriptionStore';

export const useDailyLimit = () => {
  const { isPremium, dailyUsage, incrementDailyUsage } = useSubscriptionStore();
  
  const getDailyLimit = (): number => {
    return isPremium ? Infinity : 1; // Free: 1 daily, Premium: unlimited
  };
  
  const getRemainingConversations = (): number => {
    const limit = getDailyLimit();
    return Math.max(0, limit - dailyUsage.conversations);
  };
  
  const canStartConversation = (): boolean => {
    return isPremium || dailyUsage.conversations < 1;
  };
  
  const getUsageDisplayText = (): string => {
    if (isPremium) return "Unlimited conversations";
    const remaining = getRemainingConversations();
    return `${remaining}/1 conversations remaining today`;
  };
  
  return {
    canStartConversation,
    getRemainingConversations,
    getUsageDisplayText,
    incrementDailyUsage,
  };
};
```

### Pre-Conversation Screen Daily Limit Integration

```typescript
// Update PreConversationScreen to check limits before generating context
export const PreConversationScreen: React.FC<PreConversationScreenProps> = ({ route }) => {
  const navigation = useNavigation();
  const { canStartConversation, getUsageDisplayText, incrementDailyUsage } = useDailyLimit();
  const { generateContext, currentContext, isGenerating } = usePreConversationStore();
  
  // Check daily limit before generating context
  useEffect(() => {
    if (!canStartConversation()) {
      // Redirect to upgrade screen if limit reached
      navigation.replace('PremiumUpgrade', {
        source: 'daily_limit',
        blockedFeature: 'conversations',
        message: 'Daily conversation limit reached'
      });
      return;
    }
    
    // Generate context if within limits
    generateContext(route.params.scenarioParams);
  }, []);
  
  const handleStartConversation = () => {
    if (!canStartConversation()) {
      navigation.navigate('PremiumUpgrade', {
        source: 'conversation_start',
        blockedFeature: 'conversations'
      });
      return;
    }
    
    // Increment daily usage counter
    incrementDailyUsage('conversations');
    
    navigation.navigate('Conversation', {
      contextData: currentContext,
    });
  };
  
  return (
    <Box flex={1} bg="gray.50" safeArea>
      {/* Header with usage indicator */}
      <HStack justifyContent="space-between" alignItems="center" px={4} py={3}>
        <Text fontSize="md" fontWeight="medium">
          Review Your Scenario
        </Text>
        <Text fontSize="sm" color="gray.600">
          {getUsageDisplayText()}
        </Text>
      </HStack>
      
      {/* Rest of component remains unchanged */}
      {/* ... existing context display logic ... */}
      
      {/* Start button with limit check */}
      <Button
        size="lg"
        bg="orange.500"
        _pressed={{ bg: "orange.600" }}
        disabled={!canStartConversation() || !allCardsReviewed}
        onPress={handleStartConversation}
      >
        <Text fontSize="md" fontWeight="semibold" color="white">
          {canStartConversation() ? 'Start Conversation' : 'Upgrade to Continue'}
        </Text>
      </Button>
    </Box>
  );
};
```

### Usage Tracking Store Integration

```typescript
// Update subscription store to track daily usage
// src/stores/subscriptionStore.ts
interface SubscriptionState {
  isPremium: boolean;
  dailyUsage: {
    conversations: number;
    lastReset: string; // ISO date string
  };
  
  // Actions
  incrementDailyUsage: (type: 'conversations') => void;
  resetDailyUsageIfNeeded: () => void;
}

export const useSubscriptionStore = create<SubscriptionState>()((set, get) => ({
  isPremium: false,
  dailyUsage: {
    conversations: 0,
    lastReset: new Date().toISOString().split('T')[0], // Today's date
  },
  
  incrementDailyUsage: (type) => {
    get().resetDailyUsageIfNeeded();
    
    set(state => ({
      dailyUsage: {
        ...state.dailyUsage,
        [type]: state.dailyUsage[type] + 1,
      }
    }));
  },
  
  resetDailyUsageIfNeeded: () => {
    const today = new Date().toISOString().split('T')[0];
    const lastReset = get().dailyUsage.lastReset;
    
    if (lastReset !== today) {
      set({
        dailyUsage: {
          conversations: 0,
          lastReset: today,
        }
      });
    }
  },
}));
```

---

## Related Documentation

- [Pre-Conversation Context README](./README.md) - Complete feature overview and requirements
- [User Journey](./user-journey.md) - Detailed user flow through context preparation
- [Screen States](./screen-states.md) - All possible interface states and visual specifications
- [Interactions](./interactions.md) - Animation and interaction patterns
- [Accessibility Implementation](./accessibility.md) - Complete accessibility compliance guide

## Implementation Checklist

### Core Features
- [ ] Zustand store with context management
- [ ] OpenRouter API integration with fallback models
- [ ] Context card display with animations
- [ ] Progress tracking and review completion detection
- [ ] Action buttons with proper state management

### AI Integration
- [ ] Structured context generation prompts
- [ ] Response validation and error handling
- [ ] Fallback content for generation failures
- [ ] Context caching for performance
- [ ] Content appropriateness filtering

### Performance Features
- [ ] Context caching with expiration
- [ ] Memory optimization for large contexts
- [ ] Performance monitoring and analytics
- [ ] Background context pre-generation
- [ ] Efficient re-rendering with React.memo

### User Experience Features
- [ ] Smooth card entrance animations
- [ ] Context regeneration with loading states
- [ ] Help modal for context interpretation
- [ ] Progress indicators and completion tracking
- [ ] Seamless transition to conversation

### Testing Complete
- [ ] Unit tests for store and services
- [ ] Integration tests for main components
- [ ] End-to-end user flow testing
- [ ] Performance testing under various conditions
- [ ] Error handling and recovery testing

---

*This implementation guide provides the technical foundation for FlirtCraft's pre-conversation context feature, ensuring users receive high-quality, contextually appropriate scenario preparation that builds confidence for successful practice conversations.*