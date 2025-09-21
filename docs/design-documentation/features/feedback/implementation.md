# Feedback Feature - Implementation

---
title: Feedback Feature Implementation Guide
description: Complete technical specifications and developer handoff for feedback system
feature: feedback
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
  - ../../design-system/components/gamification.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native 0.72+
  - NativeBase
  - NativeWind 4.1
  - React Native Reanimated 3.6+
  - Zustand 4.4+
status: approved
---

## Implementation Overview

The feedback feature is a critical MVP component that transforms conversation data into actionable learning insights. This implementation guide provides complete technical specifications for building a performant, accessible, and engaging feedback system.

## Table of Contents

1. [Component Architecture](#component-architecture)
2. [State Management](#state-management)
3. [API Integration](#api-integration)
4. [Component Specifications](#component-specifications)
5. [Performance Optimization](#performance-optimization)
6. [Testing Strategy](#testing-strategy)

---

## Component Architecture

### Feature Structure

```
src/features/feedback/
├── components/
│   ├── FeedbackScreen.tsx           # Main feedback container
│   ├── ScoreDisplay/
│   │   ├── index.tsx               # Animated score reveal
│   │   ├── ScoreRing.tsx           # Circular progress indicator
│   │   └── ScoreContext.tsx        # Score interpretation
│   ├── FeedbackCards/
│   │   ├── index.tsx               # Card container
│   │   ├── StrengthCard.tsx        # Positive feedback card
│   │   ├── ImprovementCard.tsx     # Growth area card
│   │   └── InsightCard.tsx         # General insight card
│   ├── ProgressChart/
│   │   ├── index.tsx               # Progress visualization
│   │   ├── TrendLine.tsx           # Skill progression line
│   │   └── Milestones.tsx          # Achievement markers
│   ├── ActionButtons/
│   │   ├── index.tsx               # Action selection
│   │   ├── PrimaryAction.tsx       # Main recommendation
│   │   └── SecondaryActions.tsx    # Alternative options
│   └── LoadingStates/
│       ├── FeedbackLoader.tsx      # Analysis loading state
│       ├── SkeletonCard.tsx        # Loading card placeholder
│       └── ErrorFallback.tsx       # Error recovery
├── hooks/
│   ├── useFeedbackAnalysis.ts      # Feedback generation logic
│   ├── useFeedbackAnimation.ts     # Animation orchestration
│   ├── useFeedbackAccessibility.ts # Accessibility features
│   └── useFeedbackNavigation.ts    # Navigation logic
├── stores/
│   ├── feedbackStore.ts            # Zustand feedback state
│   └── progressStore.ts            # Historical progress data
├── types/
│   ├── feedback.types.ts           # TypeScript definitions
│   └── conversation.types.ts       # Conversation data types
└── utils/
    ├── feedbackCalculator.ts       # Overall score calculation
    ├── metricCalculators/
    │   ├── aiEngagementCalculator.ts    # AI engagement quality scoring
    │   ├── listeningCalculator.ts       # Responsiveness & listening scoring
    │   ├── storytellingCalculator.ts    # Narrative building scoring
    │   ├── emotionalIQCalculator.ts     # Emotional intelligence scoring
    │   ├── momentumCalculator.ts        # Conversation momentum scoring
    │   └── flirtationCalculator.ts      # Creative flirtation scoring
    ├── contentFormatter.ts         # Text processing
    ├── personaAdapters.ts          # Persona-specific feedback adaptation
    └── performanceMetrics.ts       # Analytics tracking
```

### Core Component Dependencies

```typescript
// Design System Components Used
import {
  Button,        // from ../../design-system/components/buttons
  Card,          // from ../../design-system/components/cards  
  Modal,         // from ../../design-system/components/modals
  ProgressRing,  // from ../../design-system/components/gamification
} from '../../../design-system';

// NativeBase Components
import {
  Box,
  VStack,
  HStack,
  Text,
  ScrollView,
  Skeleton,
  useToast,
} from 'native-base';

// Animation Library
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  withSequence,
  runOnJS,
} from 'react-native-reanimated';
```

---

## State Management

### Zustand Store Implementation

#### Feedback Store

```typescript
// stores/feedbackStore.ts
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

interface FeedbackState {
  // Core feedback data
  currentFeedback: FeedbackData | null;
  isAnalyzing: boolean;
  analysisProgress: number;
  
  // Animation states
  scoreAnimation: {
    isAnimating: boolean;
    currentValue: number;
    targetValue: number;
  };
  
  // User interaction
  selectedDetailLevel: 'basic' | 'standard' | 'detailed';
  viewedCards: string[];
  feedbackRating: number | null;
  
  // Actions
  generateFeedback: (conversationData: ConversationData) => Promise<void>;
  setDetailLevel: (level: string) => void;
  markCardViewed: (cardId: string) => void;
  rateFeedback: (rating: number) => void;
  clearFeedback: () => void;
}

export const useFeedbackStore = create<FeedbackState>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    currentFeedback: null,
    isAnalyzing: false,
    analysisProgress: 0,
    scoreAnimation: {
      isAnimating: false,
      currentValue: 0,
      targetValue: 0,
    },
    selectedDetailLevel: 'standard',
    viewedCards: [],
    feedbackRating: null,

    // Actions
    generateFeedback: async (conversationData) => {
      set({ isAnalyzing: true, analysisProgress: 0 });
      
      try {
        // Simulate analysis progress
        const progressInterval = setInterval(() => {
          set(state => ({
            analysisProgress: Math.min(state.analysisProgress + 10, 90)
          }));
        }, 200);

        // API call for feedback generation
        const feedback = await analyzeFeedback(conversationData);
        
        clearInterval(progressInterval);
        set({
          currentFeedback: feedback,
          isAnalyzing: false,
          analysisProgress: 100,
          scoreAnimation: {
            isAnimating: true,
            currentValue: 0,
            targetValue: feedback.score,
          },
        });

        // Track analytics
        analytics.track('feedback_generated', {
          score: feedback.score,
          conversationId: conversationData.id,
        });

      } catch (error) {
        set({ 
          isAnalyzing: false, 
          analysisProgress: 0,
          error: error.message 
        });
        console.error('Feedback generation failed:', error);
      }
    },

    setDetailLevel: (level) => {
      set({ selectedDetailLevel: level });
      analytics.track('feedback_detail_changed', { level });
    },

    markCardViewed: (cardId) => {
      set(state => ({
        viewedCards: [...new Set([...state.viewedCards, cardId])]
      }));
    },

    rateFeedback: (rating) => {
      set({ feedbackRating: rating });
      
      // Send rating to API
      if (get().currentFeedback) {
        submitFeedbackRating(get().currentFeedback!.id, rating);
      }
    },

    clearFeedback: () => {
      set({
        currentFeedback: null,
        scoreAnimation: {
          isAnimating: false,
          currentValue: 0,
          targetValue: 0,
        },
        viewedCards: [],
        feedbackRating: null,
      });
    },
  }))
);
```

#### Progress Store Integration

```typescript
// stores/progressStore.ts
interface ProgressState {
  historicalScores: ScoreHistory[];
  skillProgression: SkillProgression;
  achievements: Achievement[];
  
  // Actions
  addScore: (score: ScoreData) => void;
  getProgressComparison: () => ProgressComparison;
  checkAchievements: (newScore: ScoreData) => Achievement[];
}

export const useProgressStore = create<ProgressState>()((set, get) => ({
  historicalScores: [],
  skillProgression: initializeSkillProgression(),
  achievements: [],

  addScore: (score) => {
    set(state => ({
      historicalScores: [...state.historicalScores, score].slice(-20), // Keep last 20
      skillProgression: updateSkillProgression(state.skillProgression, score),
    }));

    // Check for new achievements
    const newAchievements = get().checkAchievements(score);
    if (newAchievements.length > 0) {
      set(state => ({
        achievements: [...state.achievements, ...newAchievements]
      }));
    }
  },

  getProgressComparison: () => {
    const scores = get().historicalScores;
    if (scores.length < 2) return null;
    
    const recent = scores.slice(-3);
    const previous = scores.slice(-6, -3);
    
    return calculateProgressComparison(recent, previous);
  },

  checkAchievements: (newScore) => {
    const currentAchievements = get().achievements;
    return detectNewAchievements(newScore, currentAchievements);
  },
}));
```

---

## API Integration

### Feedback Analysis Endpoint

```typescript
// api/feedback.ts
interface FeedbackRequest {
  conversationId: string;
  messages: ConversationMessage[];
  preContext: PreConversationContext;
  userProfile: UserProfile;
  aiStateChanges: AIEmotionalState[];
  contextUsageTracking: ContextUsageEvent[];
  metadata: {
    duration: number;
    scenario: string;
    difficulty: 'green' | 'yellow' | 'red';
    userSkillLevel: 'beginner' | 'intermediate' | 'advanced';
  };
}

interface FeedbackResponse {
  id: string;
  overallScore: number;
  coreMetrics: {
    confidence: number;
    appropriateness: number;
    engagement: number;
  };
  advancedMetrics: {
    contextUtilization: ContextUtilizationScore;
    activeListening: ActiveListeningScore;
    storytelling: StorytellingScore;
    emotionalIntelligence: EmotionalIntelligenceScore;
    momentumManagement: MomentumScore;
    creativeFlirtation?: FlirtationScore; // Only for Yellow/Red difficulty
  };
  personaAdaptations: PersonaFeedback;
  strengths: DetailedInsight[];
  improvements: DetailedInsight[];
  recommendations: ActionRecommendation[];
  progressComparison?: ProgressComparison;
  achievements?: Achievement[];
}

// Advanced Metric Type Definitions
interface ContextUtilizationScore {
  overall: number; // 0-100
  breakdown: {
    appearanceIntegration: number; // How well they referenced appearance cues
    environmentAwareness: number; // Usage of location/time/crowd details
    starterAdaptation: number; // Creative variation on AI suggestions
    bodyLanguageResponse: number; // Reactions to receptiveness signals
  };
  strongExamples: string[]; // "Great job mentioning the coffee shop's jazz music!"
  missedCues: string[]; // "They mentioned being a regular - could have asked about favorites"
  improvementTips: string[]; // Actionable advice for next time
}

interface ActiveListeningScore {
  overall: number;
  breakdown: {
    directResponseQuality: number; // Addressing specific AI points
    threadFollowing: number; // Building on AI topics
    contextualRelevance: number; // Shows full conversation understanding
    hintRecognition: number; // Picking up subtle interests
  };
  listeningHighlights: ConversationMoment[]; // Best listening moments
  missedOpportunities: {
    timestamp: number;
    aiStatement: string;
    missedElement: string;
    suggestion: string;
  }[];
}

interface StorytellingScore {
  overall: number;
  breakdown: {
    anecdoteQuality: number; // Engaging, relevant stories
    storyArcDevelopment: number; // Beginning, middle, end structure
    reciprocalSharing: number; // Balanced story exchange
    detailRichness: number; // Vivid, memorable details
  };
  bestStory: {
    snippet: string;
    strengths: string[];
    couldImprove: string[];
  };
  storyBalance: {
    userStories: number;
    aiStories: number;
    exchangeQuality: 'one-sided' | 'balanced' | 'collaborative';
  };
}

interface EmotionalIntelligenceScore {
  overall: number;
  breakdown: {
    emotionRecognition: number; // Identifying AI feelings
    empatheticResponse: number; // Appropriate support/validation
    moodMatching: number; // Energy adjustment
    cueInterpretation: number; // Reading between lines
  };
  emotionalMoments: {
    timestamp: number;
    aiEmotion: string;
    userResponse: string;
    effectiveness: 'missed' | 'adequate' | 'excellent';
  }[];
  coachingNotes: string[];
}

interface MomentumScore {
  overall: number;
  breakdown: {
    revivalSkills: number; // Rescuing dying conversations
    transitionSmoothness: number; // Natural topic changes
    energyCalibration: number; // Building/maintaining excitement
    exitAwareness: number; // Knowing when to conclude
  };
  momentumGraph: {
    timestamp: number;
    energy: number; // 0-100 conversation energy level
    userContribution: 'positive' | 'neutral' | 'negative';
  }[];
  criticalSaves: string[]; // Moments where user rescued conversation
  smoothTransitions: string[]; // Examples of good topic changes
}

interface FlirtationScore {
  overall: number;
  breakdown: {
    humorTiming: number; // Well-placed jokes
    teasingBalance: number; // Playful without crossing lines
    genuineCompliments: number; // Specific, authentic appreciation
    tensionBuilding: number; // Creating anticipation
  };
  flirtationHighlights: {
    type: 'humor' | 'tease' | 'compliment' | 'tension';
    snippet: string;
    effectiveness: number;
    aiReaction: string;
  }[];
  boundaryAwareness: {
    respectful: boolean;
    calibrated: boolean;
    notes: string[];
  };
  coachingTips: string[];
}

interface MetricResult {
  score: number; // 0-100
  level: 'exceptional' | 'good' | 'developing' | 'needs_practice';
  feedback: string;
  improvementTip: string;
  specificExamples: ConversationExample[];
  levelUpChallenge?: string;
}

interface ConversationExample {
  turnNumber: number;
  context: string; // What was happening in conversation
  userResponse: string;
  aiResponse?: string;
  evaluation: string;
  rating: 'positive' | 'neutral' | 'improvement_opportunity';
  suggestion?: string;
}

interface PersonaFeedback {
  userPersona: 'anxious_alex' | 'comeback_catherine' | 'confident_carlos' | 'shy_sarah';
  encouragementBoosts: string[];
  toneAdjustments: {
    gentleGuidance: boolean;
    competitiveElements: boolean;
    realWorldContext: boolean;
    confidenceBuilding: boolean;
  };
  focusAreas: string[];
}

interface DetailedInsight {
  id: string;
  title: string;
  description: string;
  category: string;
  relatedMetric: string;
  specificExample?: ConversationExample;
  actionableAdvice: string;
}

export const analyzeFeedback = async (data: ConversationData): Promise<FeedbackResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations/${data.conversationId}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await getAuthToken()}`,
      },
      body: JSON.stringify({
        conversationId: data.id,
        messages: data.messages,
        preContext: data.preContext,
        userProfile: await getUserProfile(),
        metadata: {
          duration: data.duration,
          scenario: data.scenario,
          difficulty: data.difficulty,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Feedback analysis failed: ${response.statusText}`);
    }

    const feedback = await response.json();
    
    // Cache feedback for offline access
    await cacheService.storeFeedback(feedback);
    
    return feedback;
    
  } catch (error) {
    console.error('Feedback API error:', error);
    
    // Fallback to cached or basic feedback
    const fallback = await generateFallbackFeedback(data);
    return fallback;
  }
};

// Advanced Metric Calculation Functions
const calculateAdvancedMetrics = (data: ConversationData): AdvancedMetrics => {
  return {
    contextUtilization: calculateContextUtilization(data),
    activeListening: calculateActiveListening(data),
    storytelling: calculateStorytelling(data),
    emotionalIntelligence: calculateEmotionalIntelligence(data),
    momentumManagement: calculateMomentum(data),
    creativeFlirtation: data.difficulty !== 'green' ? calculateFlirtation(data) : undefined,
  };
};

const calculateContextUtilization = (data: ConversationData): ContextUtilizationScore => {
  const { messages, preContext } = data;
  
  // Analyze how well user incorporated pre-conversation context
  const appearanceRefs = messages.filter(m => 
    m.sender === 'user' && containsAppearanceReference(m.content, preContext.appearance)
  );
  
  const environmentRefs = messages.filter(m =>
    m.sender === 'user' && containsEnvironmentReference(m.content, preContext.environment)
  );
  
  const starterVariation = analyzeStarterAdaptation(
    messages[0]?.content || '',
    preContext.starterSuggestions
  );
  
  const bodyLanguageAlignment = analyzeBodyLanguageResponse(
    messages,
    preContext.bodyLanguage
  );
  
  return {
    overall: calculateWeightedAverage([
      { value: appearanceRefs.length > 0 ? 80 : 40, weight: 0.25 },
      { value: environmentRefs.length > 0 ? 85 : 45, weight: 0.25 },
      { value: starterVariation.score, weight: 0.25 },
      { value: bodyLanguageAlignment.score, weight: 0.25 },
    ]),
    breakdown: {
      appearanceIntegration: appearanceRefs.length > 0 ? 80 : 40,
      environmentAwareness: environmentRefs.length > 0 ? 85 : 45,
      starterAdaptation: starterVariation.score,
      bodyLanguageResponse: bodyLanguageAlignment.score,
    },
    strongExamples: extractStrongContextExamples(messages, preContext),
    missedCues: identifyMissedContextCues(messages, preContext),
    improvementTips: generateContextTips(data.userSkillLevel),
  };
};

const calculateActiveListening = (data: ConversationData): ActiveListeningScore => {
  const { messages } = data;
  const aiMessages = messages.filter(m => m.sender === 'ai');
  const userMessages = messages.filter(m => m.sender === 'user');
  
  const listeningMoments = [];
  const missedOpportunities = [];
  
  aiMessages.forEach((aiMsg, idx) => {
    const nextUserMsg = userMessages.find(u => u.timestamp > aiMsg.timestamp);
    if (nextUserMsg) {
      const responseQuality = analyzeResponseRelevance(aiMsg.content, nextUserMsg.content);
      if (responseQuality.score > 75) {
        listeningMoments.push({
          timestamp: nextUserMsg.timestamp,
          description: responseQuality.description,
        });
      } else if (responseQuality.missedOpportunity) {
        missedOpportunities.push({
          timestamp: aiMsg.timestamp,
          aiStatement: aiMsg.content.substring(0, 100),
          missedElement: responseQuality.missedElement,
          suggestion: responseQuality.suggestion,
        });
      }
    }
  });
  
  return {
    overall: calculateListeningScore(listeningMoments, missedOpportunities),
    breakdown: {
      directResponseQuality: listeningMoments.length * 10,
      threadFollowing: calculateThreadFollowing(messages),
      contextualRelevance: calculateContextualRelevance(messages),
      hintRecognition: calculateHintRecognition(messages),
    },
    listeningHighlights: listeningMoments,
    missedOpportunities: missedOpportunities.slice(0, 3), // Top 3 missed opportunities
  };
};

// Offline fallback feedback generation
const generateFallbackFeedback = async (data: ConversationData): Promise<FeedbackResponse> => {
  const basicScore = calculateBasicScore(data);
  
  return {
    id: `fallback_${Date.now()}`,
    score: basicScore,
    breakdown: {
      confidence: basicScore,
      flow: basicScore,
      appropriateness: basicScore,
      engagement: basicScore,
    },
    strengths: [
      {
        id: 'participation',
        title: 'Great job participating!',
        description: 'You completed the conversation practice.',
        category: 'engagement',
      },
    ],
    improvements: [
      {
        id: 'continue_practice',
        title: 'Keep practicing',
        description: 'Regular practice will help you improve your conversation skills.',
        category: 'general',
      },
    ],
    recommendations: [
      {
        action: 'practice_again',
        title: 'Practice Again',
        description: 'Try the same scenario to build confidence.',
        priority: 'primary',
      },
    ],
  };
};
```

### Progress Tracking API

```typescript
// api/progress.ts
export const submitFeedbackRating = async (feedbackId: string, rating: number): Promise<void> => {
  try {
    await fetch(`${API_BASE_URL}/feedback/${feedbackId}/rating`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await getAuthToken()}`,
      },
      body: JSON.stringify({ rating }),
    });
  } catch (error) {
    console.error('Failed to submit feedback rating:', error);
    // Store rating locally for later sync
    await storeOfflineRating(feedbackId, rating);
  }
};

export const syncProgressData = async (): Promise<void> => {
  const offlineData = await getOfflineProgressData();
  
  if (offlineData.length === 0) return;
  
  try {
    await fetch(`${API_BASE_URL}/progress/sync`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await getAuthToken()}`,
      },
      body: JSON.stringify({ data: offlineData }),
    });
    
    // Clear offline data after successful sync
    await clearOfflineProgressData();
    
  } catch (error) {
    console.error('Progress sync failed:', error);
  }
};
```

---

---

## Advanced Metric Calculation System

### Core Metric Calculators

#### AI Engagement Quality Calculator

```typescript
// utils/metricCalculators/aiEngagementCalculator.ts
interface ContextUsageEvent {
  type: 'appearance' | 'environment' | 'body_language' | 'ai_suggestion';
  contextItem: string;
  userResponse: string;
  integrationQuality: 'natural' | 'forced' | 'creative' | 'ignored';
  turnNumber: number;
}

interface AIEngagementAnalysis {
  contextUsageRate: number; // Percentage of available context used
  integrationQuality: number; // How naturally context was woven in
  creativityScore: number; // Original variations vs direct copying
  continuityScore: number; // Consistent awareness throughout conversation
}

export class AIEngagementCalculator {
  private preContext: PreConversationContext;
  private contextEvents: ContextUsageEvent[];
  private conversationLength: number;

  constructor(preContext: PreConversationContext, contextEvents: ContextUsageEvent[], conversationLength: number) {
    this.preContext = preContext;
    this.contextEvents = contextEvents;
    this.conversationLength = conversationLength;
  }

  calculateScore(): MetricResult {
    const analysis = this.analyzeEngagement();
    const rawScore = this.computeRawScore(analysis);
    const adjustedScore = this.applyDifficultyAdjustments(rawScore);
    
    return {
      score: Math.round(adjustedScore),
      level: this.getPerformanceLevel(adjustedScore),
      feedback: this.generateFeedback(analysis),
      improvementTip: this.generateImprovementTip(analysis),
      specificExamples: this.getSpecificExamples(),
      levelUpChallenge: adjustedScore > 80 ? this.generateLevelUpChallenge() : undefined,
    };
  }

  private analyzeEngagement(): AIEngagementAnalysis {
    const totalContextItems = this.preContext.appearanceCues.length + 
                             this.preContext.environmentDetails.length + 
                             this.preContext.bodyLanguageSignals.length + 
                             this.preContext.aiSuggestions.length;

    const usedItems = new Set(this.contextEvents.map(e => e.contextItem)).size;
    const contextUsageRate = (usedItems / totalContextItems) * 100;

    const naturalIntegrations = this.contextEvents.filter(e => 
      e.integrationQuality === 'natural' || e.integrationQuality === 'creative'
    ).length;
    const integrationQuality = (naturalIntegrations / this.contextEvents.length) * 100;

    const creativeVariations = this.contextEvents.filter(e => 
      e.integrationQuality === 'creative'
    ).length;
    const creativityScore = (creativeVariations / Math.max(this.contextEvents.length, 1)) * 100;

    // Measure consistency - did they maintain contextual awareness throughout?
    const earlyUse = this.contextEvents.filter(e => e.turnNumber <= this.conversationLength * 0.3).length;
    const lateUse = this.contextEvents.filter(e => e.turnNumber >= this.conversationLength * 0.7).length;
    const continuityScore = Math.min((earlyUse + lateUse) / 2, 100);

    return {
      contextUsageRate,
      integrationQuality,
      creativityScore,
      continuityScore,
    };
  }

  private computeRawScore(analysis: AIEngagementAnalysis): number {
    // Weighted scoring based on importance
    return (
      analysis.contextUsageRate * 0.3 +      // 30% weight on coverage
      analysis.integrationQuality * 0.4 +    // 40% weight on naturalness  
      analysis.creativityScore * 0.2 +       // 20% weight on creativity
      analysis.continuityScore * 0.1         // 10% weight on consistency
    );
  }

  private generateFeedback(analysis: AIEngagementAnalysis): string {
    if (analysis.integrationQuality > 80) {
      return "Excellent context integration! You made pre-conversation details feel like natural observations.";
    } else if (analysis.contextUsageRate > 70) {
      return "Good use of context details! You incorporated the information well into conversation.";
    } else if (analysis.contextUsageRate > 40) {
      return "You're starting to use context well! Try incorporating more details naturally.";
    } else {
      return "Focus on using the pre-conversation context more - it helps create personalized conversations.";
    }
  }
}
```

#### Responsiveness & Listening Calculator

```typescript
// utils/metricCalculators/listeningCalculator.ts
interface ListeningEvent {
  aiStatement: string;
  aiEmotionalState: string;
  userResponse: string;
  responseType: 'direct_acknowledgment' | 'follow_up_question' | 'emotional_response' | 'topic_building' | 'generic';
  turnNumber: number;
  qualityScore: number; // 1-5 scale
}

export class ListeningCalculator {
  private listeningEvents: ListeningEvent[];
  private aiEmotionalChanges: AIEmotionalState[];

  calculateScore(): MetricResult {
    const directResponses = this.analyzeDirectResponses();
    const emotionalAwareness = this.analyzeEmotionalAwareness();
    const threadBuilding = this.analyzeThreadBuilding();
    
    const rawScore = (
      directResponses * 0.4 +      // 40% weight on direct response
      emotionalAwareness * 0.35 +  // 35% weight on emotional intelligence
      threadBuilding * 0.25        // 25% weight on conversation building
    );

    return {
      score: Math.round(rawScore),
      level: this.getPerformanceLevel(rawScore),
      feedback: this.generateListeningFeedback(directResponses, emotionalAwareness),
      improvementTip: this.generateListeningTip(directResponses, emotionalAwareness),
      specificExamples: this.getBestListeningExamples(),
    };
  }

  private analyzeDirectResponses(): number {
    const directResponseCount = this.listeningEvents.filter(e => 
      e.responseType === 'direct_acknowledgment' || 
      e.responseType === 'follow_up_question'
    ).length;
    
    return (directResponseCount / this.listeningEvents.length) * 100;
  }

  private analyzeEmotionalAwareness(): number {
    const emotionalResponses = this.listeningEvents.filter(e => 
      e.responseType === 'emotional_response' && e.qualityScore >= 4
    ).length;
    
    const emotionalOpportunities = this.aiEmotionalChanges.filter(change => 
      change.intensity > 0.3 // Significant emotional expression
    ).length;

    if (emotionalOpportunities === 0) return 100; // No emotional cues to respond to
    return (emotionalResponses / emotionalOpportunities) * 100;
  }
}
```

#### Emotional Intelligence Calculator

```typescript
// utils/metricCalculators/emotionalIQCalculator.ts
interface EmotionalEvent {
  aiEmotionalState: {
    emotion: string;
    intensity: number; // 0-1 scale
    bodyLanguageCues: string[];
    verbalCues: string[];
  };
  userResponse: string;
  emotionalRecognition: 'none' | 'basic' | 'nuanced' | 'exceptional';
  responseAppropriateness: number; // 1-5 scale
  empathyLevel: number; // 1-5 scale
}

export class EmotionalIQCalculator {
  private emotionalEvents: EmotionalEvent[];
  private difficulty: 'green' | 'yellow' | 'red';

  calculateScore(): MetricResult {
    const recognitionScore = this.calculateRecognitionScore();
    const responseScore = this.calculateResponseScore();
    const empathyScore = this.calculateEmpathyScore();
    const adaptationScore = this.calculateAdaptationScore();

    const rawScore = (
      recognitionScore * 0.3 +     // 30% recognition
      responseScore * 0.3 +        // 30% appropriate response
      empathyScore * 0.25 +        // 25% empathy
      adaptationScore * 0.15       // 15% adaptation
    );

    return {
      score: Math.round(rawScore),
      level: this.getPerformanceLevel(rawScore),
      feedback: this.generateEmotionalFeedback(recognitionScore, empathyScore),
      improvementTip: this.generateEmotionalTip(recognitionScore, responseScore),
      specificExamples: this.getBestEmotionalExamples(),
    };
  }

  private calculateRecognitionScore(): number {
    const totalEvents = this.emotionalEvents.length;
    if (totalEvents === 0) return 100;

    const recognitionLevels = this.emotionalEvents.map(e => {
      switch (e.emotionalRecognition) {
        case 'exceptional': return 100;
        case 'nuanced': return 80;
        case 'basic': return 60;
        case 'none': return 0;
        default: return 0;
      }
    });

    return recognitionLevels.reduce((sum, score) => sum + score, 0) / totalEvents;
  }

  private generateEmotionalFeedback(recognitionScore: number, empathyScore: number): string {
    if (recognitionScore > 85 && empathyScore > 85) {
      return "Outstanding emotional intelligence! You recognized subtle cues and responded with genuine empathy.";
    } else if (recognitionScore > 70) {
      return "Great emotional awareness! You picked up on their feelings and responded appropriately.";
    } else if (recognitionScore > 50) {
      return "You're developing emotional awareness! Focus on noticing how they feel about what they share.";
    } else {
      return "Try paying attention to emotional cues - not just what they say, but how they might be feeling.";
    }
  }
}
```

#### Conversation Momentum Calculator

```typescript
// utils/metricCalculators/momentumCalculator.ts
interface MomentumEvent {
  turnNumber: number;
  energyLevel: number; // 1-5 scale
  transitionQuality: 'smooth' | 'awkward' | 'creative' | 'jarring';
  recoveryAttempt?: {
    previousEnergyLevel: number;
    recoveryMethod: string;
    success: boolean;
  };
  topicShift?: {
    relevance: number; // 1-5 scale
    naturalness: number; // 1-5 scale
  };
}

export class MomentumCalculator {
  private momentumEvents: MomentumEvent[];
  private conversationLength: number;

  calculateScore(): MetricResult {
    const energyManagement = this.analyzeEnergyManagement();
    const transitionQuality = this.analyzeTransitions();
    const recoverySkill = this.analyzeRecoverySkill();

    const rawScore = (
      energyManagement * 0.4 +     // 40% energy management
      transitionQuality * 0.35 +   // 35% smooth transitions
      recoverySkill * 0.25         // 25% recovery ability
    );

    return {
      score: Math.round(rawScore),
      level: this.getPerformanceLevel(rawScore),
      feedback: this.generateMomentumFeedback(energyManagement, recoverySkill),
      improvementTip: this.generateMomentumTip(transitionQuality, recoverySkill),
      specificExamples: this.getBestMomentumExamples(),
    };
  }

  private analyzeEnergyManagement(): number {
    const averageEnergy = this.momentumEvents.reduce((sum, event) => 
      sum + event.energyLevel, 0) / this.momentumEvents.length;
    
    // Analyze energy consistency and building
    const energyTrend = this.calculateEnergyTrend();
    const energyConsistency = this.calculateEnergyConsistency();

    return (averageEnergy * 20) + energyTrend + energyConsistency;
  }

  private analyzeRecoverySkill(): number {
    const recoveryAttempts = this.momentumEvents.filter(e => e.recoveryAttempt);
    if (recoveryAttempts.length === 0) return 100; // No recovery needed

    const successfulRecoveries = recoveryAttempts.filter(e => 
      e.recoveryAttempt?.success
    ).length;

    return (successfulRecoveries / recoveryAttempts.length) * 100;
  }
}
```

---

## Component Specifications

### Enhanced Feedback Screen with Advanced Metrics

```typescript
// components/AdvancedFeedbackScreen.tsx
import React, { useEffect } from 'react';
import { Box, VStack, ScrollView } from 'native-base';
import { MetricCard } from './MetricCard';
import { PersonaFeedbackAdapter } from './PersonaFeedbackAdapter';

interface AdvancedFeedbackScreenProps {
  conversationData: ConversationData;
  onNavigateNext: (action: string) => void;
}

export const AdvancedFeedbackScreen: React.FC<AdvancedFeedbackScreenProps> = ({
  conversationData,
  onNavigateNext,
}) => {
  const { 
    generateAdvancedFeedback, 
    currentFeedback, 
    isAnalyzing,
    userPersona 
  } = useFeedbackStore();

  useEffect(() => {
    generateAdvancedFeedback(conversationData);
  }, [conversationData]);

  if (isAnalyzing) {
    return <AdvancedFeedbackLoader />;
  }

  if (!currentFeedback) {
    return <ErrorFallback onRetry={() => generateAdvancedFeedback(conversationData)} />;
  }

  return (
    <Box flex={1} safeArea>
      <ScrollView showsVerticalScrollIndicator={false}>
        <VStack space={6} p={4}>
          {/* Overall Score Display */}
          <OverallScoreDisplay score={currentFeedback.overallScore} />

          {/* Advanced Metrics Cards */}
          <VStack space={4}>
            <MetricCard 
              title="AI Engagement Quality"
              metric={currentFeedback.evaluationMetrics.aiEngagementQuality}
              icon="target"
              persona={userPersona}
            />
            
            <MetricCard 
              title="Active Listening"
              metric={currentFeedback.evaluationMetrics.responsivenessListening}
              icon="ear"
              persona={userPersona}
            />
            
            <MetricCard 
              title="Storytelling"
              metric={currentFeedback.evaluationMetrics.storytellingNarrative}
              icon="book-open"
              persona={userPersona}
            />
            
            <MetricCard 
              title="Emotional Intelligence"
              metric={currentFeedback.evaluationMetrics.emotionalIntelligence}
              icon="heart"
              persona={userPersona}
            />
            
            <MetricCard 
              title="Conversation Momentum"
              metric={currentFeedback.evaluationMetrics.conversationMomentum}
              icon="trending-up"
              persona={userPersona}
            />

            {currentFeedback.evaluationMetrics.creativeFlirtation && (
              <MetricCard 
                title="Creative Flirtation"
                metric={currentFeedback.evaluationMetrics.creativeFlirtation}
                icon="smile"
                persona={userPersona}
                isPremiumMetric={true}
              />
            )}
          </VStack>

          {/* Persona-Adapted Feedback */}
          <PersonaFeedbackAdapter 
            personaFeedback={currentFeedback.personaAdaptations}
            overallPerformance={currentFeedback.overallScore}
          />

          {/* Action Recommendations */}
          <ActionRecommendations 
            recommendations={currentFeedback.recommendations}
            onAction={onNavigateNext}
          />
        </VStack>
      </ScrollView>
    </Box>
  );
};
```

### Advanced Metric Card Component

```typescript
// components/MetricCard.tsx
interface MetricCardProps {
  title: string;
  metric: MetricResult;
  icon: string;
  persona: UserPersona;
  isPremiumMetric?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  metric,
  icon,
  persona,
  isPremiumMetric = false,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const animatedHeight = useSharedValue(0);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'success.500';
    if (score >= 60) return 'primary.500';
    if (score >= 40) return 'warning.500';
    return 'error.500';
  };

  const getPersonaAdaptedFeedback = () => {
    // Adapt feedback tone based on persona
    switch (persona) {
      case 'anxious_alex':
        return metric.feedback.replace(/Great|Good/g, 'Wonderful');
      case 'confident_carlos':
        return metric.feedback + (metric.levelUpChallenge ? ` ${metric.levelUpChallenge}` : '');
      case 'shy_sarah':
        return `You're doing great! ${metric.feedback}`;
      default:
        return metric.feedback;
    }
  };

  return (
    <Animated.View
      entering={SlideInRight.delay(Math.random() * 300)}
      layout={Layout.springify()}
    >
      <Box
        bg="white"
        rounded="xl"
        shadow={2}
        p={4}
        borderLeft={`4px solid`}
        borderLeftColor={getScoreColor(metric.score)}
      >
        <Pressable onPress={() => setIsExpanded(!isExpanded)}>
          <HStack alignItems="center" justifyContent="space-between">
            <HStack alignItems="center" space={3}>
              <Icon name={icon} size={24} color={getScoreColor(metric.score)} />
              <VStack>
                <Text fontSize="md" fontWeight="semibold">{title}</Text>
                <Text fontSize="sm" color="gray.600">{metric.level}</Text>
              </VStack>
            </HStack>
            
            <VStack alignItems="center">
              <Text fontSize="2xl" fontWeight="bold" color={getScoreColor(metric.score)}>
                {metric.score}
              </Text>
              <Text fontSize="xs" color="gray.500">out of 100</Text>
            </VStack>
          </HStack>
        </Pressable>

        {isExpanded && (
          <Animated.View
            entering={FadeIn.duration(300)}
            exiting={FadeOut.duration(200)}
          >
            <VStack space={3} mt={4} pt={4} borderTopWidth={1} borderTopColor="gray.200">
              <Text fontSize="sm" color="gray.700">
                {getPersonaAdaptedFeedback()}
              </Text>
              
              <Box bg="blue.50" p={3} rounded="md">
                <Text fontSize="sm" fontWeight="medium" color="blue.800">
                  💡 Try This Next Time
                </Text>
                <Text fontSize="sm" color="blue.700" mt={1}>
                  {metric.improvementTip}
                </Text>
              </Box>

              {metric.specificExamples.length > 0 && (
                <VStack space={2}>
                  <Text fontSize="sm" fontWeight="medium" color="gray.800">
                    Examples from your conversation:
                  </Text>
                  {metric.specificExamples.map((example, index) => (
                    <Box key={index} bg="gray.50" p={2} rounded="md">
                      <Text fontSize="xs" color="gray.600">Turn {example.turnNumber}</Text>
                      <Text fontSize="sm" color="gray.800" fontStyle="italic">
                        "{example.userResponse}"
                      </Text>
                      <Text fontSize="xs" color={example.rating === 'positive' ? 'green.600' : 'orange.600'} mt={1}>
                        {example.evaluation}
                      </Text>
                    </Box>
                  ))}
                </VStack>
              )}
            </VStack>
          </Animated.View>
        )}
      </Box>
    </Animated.View>
  );
};
```

## Component Specifications

### Main Feedback Screen

```typescript
// components/FeedbackScreen.tsx
import React, { useEffect } from 'react';
import { Box, VStack, useColorModeValue } from 'native-base';
import Animated, { 
  FadeIn, 
  SlideInUp,
  useAnimatedScrollHandler,
  useSharedValue,
} from 'react-native-reanimated';

interface FeedbackScreenProps {
  conversationData: ConversationData;
  onNavigateNext: (action: string) => void;
}

export const FeedbackScreen: React.FC<FeedbackScreenProps> = ({
  conversationData,
  onNavigateNext,
}) => {
  const { 
    generateFeedback, 
    currentFeedback, 
    isAnalyzing,
    selectedDetailLevel 
  } = useFeedbackStore();
  
  const scrollY = useSharedValue(0);
  const backgroundColor = useColorModeValue('gray.50', 'gray.900');
  
  useEffect(() => {
    generateFeedback(conversationData);
  }, [conversationData]);

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollY.value = event.contentOffset.y;
    },
  });

  if (isAnalyzing) {
    return <FeedbackLoader />;
  }

  if (!currentFeedback) {
    return <ErrorFallback onRetry={() => generateFeedback(conversationData)} />;
  }

  return (
    <Box flex={1} bg={backgroundColor} safeArea>
      <Animated.ScrollView
        onScroll={scrollHandler}
        scrollEventThrottle={16}
        showsVerticalScrollIndicator={false}
      >
        <VStack space={6} p={4}>
          <Animated.View entering={FadeIn.delay(300)}>
            <ScoreDisplay score={currentFeedback.score} breakdown={currentFeedback.breakdown} />
          </Animated.View>

          <Animated.View entering={SlideInUp.delay(600)}>
            <FeedbackCards
              strengths={currentFeedback.strengths}
              improvements={currentFeedback.improvements}
              detailLevel={selectedDetailLevel}
            />
          </Animated.View>

          {currentFeedback.progressComparison && (
            <Animated.View entering={SlideInUp.delay(900)}>
              <ProgressChart comparison={currentFeedback.progressComparison} />
            </Animated.View>
          )}

          <Animated.View entering={SlideInUp.delay(1200)}>
            <ActionButtons
              recommendations={currentFeedback.recommendations}
              onAction={onNavigateNext}
            />
          </Animated.View>
        </VStack>
      </Animated.ScrollView>
    </Box>
  );
};
```

### Score Display Component

```typescript
// components/ScoreDisplay/index.tsx
import React, { useEffect } from 'react';
import { VStack, HStack, Text, Box } from 'native-base';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  useDerivedValue,
  withTiming,
  withSpring,
  interpolate,
  runOnJS,
} from 'react-native-reanimated';

interface ScoreDisplayProps {
  score: number;
  breakdown: ScoreBreakdown;
}

export const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ score, breakdown }) => {
  const animatedScore = useSharedValue(0);
  const scaleValue = useSharedValue(0.8);
  const { announceScore } = useFeedbackAccessibility();

  useEffect(() => {
    // Animate score reveal
    animatedScore.value = withTiming(score, {
      duration: 2000,
      easing: Easing.bezier(0.4, 0, 0.2, 1),
    });

    // Scale animation for emphasis
    scaleValue.value = withSpring(1, {
      damping: 12,
      stiffness: 100,
    });

    // Announce to screen readers after animation
    const timeoutId = setTimeout(() => {
      runOnJS(announceScore)(score);
    }, 2500);

    return () => clearTimeout(timeoutId);
  }, [score]);

  const displayScore = useDerivedValue(() => {
    return Math.round(animatedScore.value);
  });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scaleValue.value }],
  }));

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'success.500';
    if (score >= 80) return 'success.400';
    if (score >= 70) return 'warning.400';
    if (score >= 60) return 'primary.500';
    return 'error.500';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return 'Exceptional!';
    if (score >= 80) return 'Great job!';
    if (score >= 70) return 'Well done!';
    if (score >= 60) return 'Good effort!';
    if (score >= 50) return 'Keep practicing!';
    return 'Learning opportunity!';
  };

  return (
    <VStack space={4} alignItems="center">
      <Animated.View style={animatedStyle}>
        <Box alignItems="center">
          <ScoreRing 
            value={animatedScore} 
            maxValue={100} 
            color={getScoreColor(score)}
            size={120}
          />
          <Text
            fontSize="4xl"
            fontWeight="bold"
            color={getScoreColor(score)}
            position="absolute"
            top="35%"
          >
            <AnimatedText text={displayScore} />
          </Text>
        </Box>
      </Animated.View>

      <VStack space={2} alignItems="center">
        <Text fontSize="lg" fontWeight="semibold" color={getScoreColor(score)}>
          {getScoreLabel(score)}
        </Text>
        <Text fontSize="sm" color="gray.600" textAlign="center">
          out of 100 points
        </Text>
      </VStack>

      <ScoreBreakdown breakdown={breakdown} />
    </VStack>
  );
};

// Animated text component for score counter
const AnimatedText: React.FC<{ text: Animated.SharedValue<number> }> = ({ text }) => {
  const animatedProps = useAnimatedProps(() => ({
    text: text.value.toString(),
  }));

  return <Animated.Text animatedProps={animatedProps} />;
};
```

### Feedback Cards Component

```typescript
// components/FeedbackCards/index.tsx
import React from 'react';
import { VStack, HStack, Text } from 'native-base';
import Animated, { 
  SlideInRight,
  Layout,
  useAnimatedStyle,
  useSharedValue,
} from 'react-native-reanimated';

interface FeedbackCardsProps {
  strengths: FeedbackInsight[];
  improvements: FeedbackInsight[];
  detailLevel: 'basic' | 'standard' | 'detailed';
}

export const FeedbackCards: React.FC<FeedbackCardsProps> = ({
  strengths,
  improvements,
  detailLevel,
}) => {
  const { markCardViewed } = useFeedbackStore();
  
  const getDisplayCount = () => {
    switch (detailLevel) {
      case 'basic': return 1;
      case 'standard': return 3;
      case 'detailed': return 5;
    }
  };

  const displayCount = getDisplayCount();
  const displayStrengths = strengths.slice(0, displayCount);
  const displayImprovements = improvements.slice(0, displayCount);

  return (
    <VStack space={6}>
      {displayStrengths.length > 0 && (
        <VStack space={3}>
          <Text fontSize="lg" fontWeight="bold" color="success.600">
            🌟 What you did well
          </Text>
          {displayStrengths.map((strength, index) => (
            <Animated.View
              key={strength.id}
              entering={SlideInRight.delay(index * 100)}
              layout={Layout}
            >
              <StrengthCard
                insight={strength}
                onView={() => markCardViewed(strength.id)}
              />
            </Animated.View>
          ))}
        </VStack>
      )}

      {displayImprovements.length > 0 && (
        <VStack space={3}>
          <Text fontSize="lg" fontWeight="bold" color="primary.600">
            🎯 Areas to improve
          </Text>
          {displayImprovements.map((improvement, index) => (
            <Animated.View
              key={improvement.id}
              entering={SlideInRight.delay((displayStrengths.length + index) * 100)}
              layout={Layout}
            >
              <ImprovementCard
                insight={improvement}
                onView={() => markCardViewed(improvement.id)}
              />
            </Animated.View>
          ))}
        </VStack>
      )}

      <DetailLevelSelector 
        current={detailLevel} 
        onChange={(level) => useFeedbackStore.getState().setDetailLevel(level)}
      />
    </VStack>
  );
};
```

### NativeWind Classes Specification

```typescript
// styles/feedback.styles.ts
export const feedbackStyles = {
  // Main container
  screenContainer: 'flex-1 bg-gray-50 dark:bg-gray-900',
  contentContainer: 'p-4 space-y-6',
  
  // Score display
  scoreContainer: 'items-center space-y-4',
  scoreRing: 'relative',
  scoreText: 'absolute top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-4xl font-bold',
  scoreLabel: 'text-lg font-semibold text-center',
  scoreContext: 'text-sm text-gray-600 text-center',
  
  // Feedback cards
  cardContainer: 'space-y-3',
  sectionHeader: 'text-lg font-bold mb-3',
  strengthCard: 'bg-green-50 border-l-4 border-green-500 p-4 rounded-lg shadow-sm',
  improvementCard: 'bg-orange-50 border-l-4 border-orange-500 p-4 rounded-lg shadow-sm',
  cardTitle: 'font-semibold text-gray-900 mb-2',
  cardDescription: 'text-gray-700 text-sm leading-relaxed',
  
  // Action buttons
  actionContainer: 'space-y-3 mt-6',
  primaryButton: 'bg-primary-500 hover:bg-primary-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md',
  secondaryButton: 'bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-6 rounded-lg',
  
  // Loading states
  loadingContainer: 'flex-1 justify-center items-center space-y-4',
  loadingSpinner: 'w-16 h-16',
  loadingText: 'text-lg text-gray-600',
  
  // Error states
  errorContainer: 'flex-1 justify-center items-center space-y-4 p-6',
  errorIcon: 'w-12 h-12 text-gray-400',
  errorTitle: 'text-lg font-semibold text-gray-900',
  errorMessage: 'text-gray-600 text-center',
  retryButton: 'bg-primary-500 text-white font-semibold py-2 px-4 rounded-lg mt-4',
};
```

---

## Premium Integration

### Limited Metrics for Free Users

The feedback feature shows limited metrics for free users while promoting premium upgrade:

```typescript
// src/features/feedback/hooks/usePremiumFeedback.ts
import { useSubscriptionStore } from '../../../stores/subscriptionStore';

export const usePremiumFeedback = () => {
  const { isPremium } = useSubscriptionStore();
  
  const getAccessibleMetrics = (allMetrics: FeedbackMetrics) => {
    const coreMetrics = {
      confidence: allMetrics.confidence,
      appropriateness: allMetrics.appropriateness,
      engagement: allMetrics.engagement,
    };
    
    if (isPremium) {
      return allMetrics; // Show all metrics for premium users
    }
    
    return coreMetrics; // Only show 3 basic metrics for free users
  };
  
  const getHiddenMetricsCount = (allMetrics: FeedbackMetrics): number => {
    if (isPremium) return 0;
    
    const totalMetrics = Object.keys(allMetrics).length;
    const visibleMetrics = 3; // confidence, appropriateness, engagement
    return Math.max(0, totalMetrics - visibleMetrics);
  };
  
  return { getAccessibleMetrics, getHiddenMetricsCount, isPremium };
};
```

### Feedback Display with Premium Upsell

```typescript
// Update FeedbackScreen to show limited metrics for free users
export const FeedbackScreen: React.FC<FeedbackScreenProps> = ({ conversationData, onNavigateNext }) => {
  const { 
    generateFeedback, 
    currentFeedback, 
    isAnalyzing 
  } = useFeedbackStore();
  
  const { getAccessibleMetrics, getHiddenMetricsCount, isPremium } = usePremiumFeedback();
  const navigation = useNavigation();

  if (!currentFeedback) return <FeedbackLoader />;
  
  const accessibleMetrics = getAccessibleMetrics(currentFeedback.advancedMetrics);
  const hiddenCount = getHiddenMetricsCount(currentFeedback.advancedMetrics);

  return (
    <Box flex={1} bg="gray.50" safeArea>
      <ScrollView showsVerticalScrollIndicator={false}>
        <VStack space={6} p={4}>
          {/* Overall Score - always visible */}
          <ScoreDisplay score={currentFeedback.overallScore} />
          
          {/* Core Metrics - always visible */}
          <VStack space={4}>
            <Text fontSize="lg" fontWeight="bold">Performance Breakdown</Text>
            
            {Object.entries(accessibleMetrics).map(([key, metric]) => (
              <MetricCard key={key} title={key} metric={metric} />
            ))}
            
            {/* Premium upsell for hidden metrics */}
            {!isPremium && hiddenCount > 0 && (
              <Pressable 
                onPress={() => navigation.navigate('PremiumUpgrade', {
                  source: 'feedback_metrics',
                  blockedFeature: 'advanced_metrics'
                })}
              >
                <Box
                  bg="orange.50"
                  borderWidth={2}
                  borderColor="orange.200"
                  borderStyle="dashed"
                  p={4}
                  borderRadius="xl"
                  alignItems="center"
                >
                  <VStack alignItems="center" space={2}>
                    <Icon name="lock" size={24} color="orange.500" />
                    <Text fontSize="md" fontWeight="semibold" color="orange.700">
                      {hiddenCount} more metrics available in Premium
                    </Text>
                    <Text fontSize="sm" color="orange.600" textAlign="center">
                      Get detailed insights on listening skills, storytelling, 
                      emotional intelligence, and more
                    </Text>
                    <Button size="sm" bg="orange.500" _pressed={{ bg: "orange.600" }}>
                      <Text color="white" fontSize="sm" fontWeight="medium">
                        Upgrade Now
                      </Text>
                    </Button>
                  </VStack>
                </Box>
              </Pressable>
            )}
          </VStack>
          
          {/* Strengths and Improvements - always visible */}
          <FeedbackCards
            strengths={currentFeedback.strengths}
            improvements={currentFeedback.improvements}
            detailLevel="standard"
          />
          
          {/* Action Buttons */}
          <ActionButtons
            recommendations={currentFeedback.recommendations}
            onAction={onNavigateNext}
          />
        </VStack>
      </ScrollView>
    </Box>
  );
};
```

### Metric Card Premium State

```typescript
// Update MetricCard to show premium-only metrics differently
const MetricCard: React.FC<MetricCardProps> = ({ 
  title, 
  metric, 
  icon, 
  isPremiumOnly = false 
}) => {
  if (isPremiumOnly) {
    return (
      <Box
        bg="gray.100"
        rounded="xl"
        p={4}
        borderWidth={1}
        borderColor="gray.300"
        opacity={0.7}
      >
        <HStack alignItems="center" justifyContent="space-between">
          <HStack alignItems="center" space={3}>
            <Icon name={icon} size={24} color="gray.400" />
            <VStack>
              <Text fontSize="md" fontWeight="semibold" color="gray.500">
                {title}
              </Text>
              <Text fontSize="sm" color="gray.400">Premium only</Text>
            </VStack>
          </HStack>
          <Icon name="lock" size={20} color="gray.400" />
        </HStack>
      </Box>
    );
  }
  
  // Regular metric card for accessible metrics
  return (
    <Box bg="white" rounded="xl" shadow={2} p={4}>
      {/* ... existing metric card implementation ... */}
    </Box>
  );
};
```

---

## Performance Optimization

### Animation Performance

```typescript
// hooks/useFeedbackAnimation.ts
import { useSharedValue, runOnJS, withTiming } from 'react-native-reanimated';
import { useCallback, useEffect } from 'react';

export const useFeedbackAnimation = () => {
  const animationProgress = useSharedValue(0);
  const [performanceMetrics, setPerformanceMetrics] = useState({
    frameDrops: 0,
    averageFPS: 60,
  });

  // Monitor animation performance
  const startPerformanceMonitoring = useCallback(() => {
    const startTime = performance.now();
    let frameCount = 0;
    
    const monitor = () => {
      frameCount++;
      if (frameCount % 60 === 0) { // Check every 60 frames
        const currentTime = performance.now();
        const fps = (frameCount / (currentTime - startTime)) * 1000;
        
        runOnJS(setPerformanceMetrics)({
          frameDrops: fps < 50 ? performanceMetrics.frameDrops + 1 : performanceMetrics.frameDrops,
          averageFPS: fps,
        });
      }
      
      if (animationProgress.value < 1) {
        requestAnimationFrame(monitor);
      }
    };
    
    requestAnimationFrame(monitor);
  }, []);

  // Optimized animation with performance fallbacks
  const animateWithPerformanceCheck = useCallback((config: any) => {
    if (performanceMetrics.averageFPS < 45) {
      // Reduce animation complexity on low-performance devices
      return withTiming(config.toValue, { duration: config.duration / 2 });
    }
    
    return withTiming(config.toValue, config);
  }, [performanceMetrics]);

  return {
    animationProgress,
    performanceMetrics,
    startPerformanceMonitoring,
    animateWithPerformanceCheck,
  };
};
```

### Memory Management

```typescript
// utils/performanceMetrics.ts
export class FeedbackPerformanceManager {
  private animationRefs: Set<any> = new Set();
  private subscriptions: any[] = [];
  private memoryUsage = { initial: 0, current: 0 };

  constructor() {
    this.memoryUsage.initial = this.getCurrentMemoryUsage();
  }

  trackAnimation(animationRef: any) {
    this.animationRefs.add(animationRef);
  }

  cleanupAnimations() {
    this.animationRefs.forEach(ref => {
      if (ref && typeof ref.stop === 'function') {
        ref.stop();
      }
    });
    this.animationRefs.clear();
  }

  trackMemoryUsage() {
    this.memoryUsage.current = this.getCurrentMemoryUsage();
    
    if (this.memoryUsage.current - this.memoryUsage.initial > 50) { // 50MB threshold
      console.warn('High memory usage detected in feedback feature');
      this.optimizeMemory();
    }
  }

  private getCurrentMemoryUsage(): number {
    if (performance && performance.memory) {
      return performance.memory.usedJSHeapSize / (1024 * 1024); // Convert to MB
    }
    return 0;
  }

  private optimizeMemory() {
    // Clear unnecessary cached data
    this.cleanupAnimations();
    
    // Force garbage collection if available
    if (global.gc) {
      global.gc();
    }
  }

  cleanup() {
    this.cleanupAnimations();
    this.subscriptions.forEach(sub => sub?.unsubscribe?.());
  }
}
```

### Bundle Optimization

```typescript
// utils/lazyImports.ts
import { lazy } from 'react';

// Lazy load heavy components to reduce initial bundle size
export const LazyProgressChart = lazy(() => 
  import('../components/ProgressChart').then(module => ({ 
    default: module.ProgressChart 
  }))
);

export const LazyDetailedAnalysis = lazy(() =>
  import('../components/DetailedAnalysis').then(module => ({
    default: module.DetailedAnalysis
  }))
);

// Preload components when likely to be needed
export const preloadFeedbackComponents = () => {
  import('../components/ProgressChart');
  import('../components/DetailedAnalysis');
};
```

---

## Testing Strategy

### Unit Tests

```typescript
// __tests__/FeedbackScreen.test.tsx
import React from 'react';
import { render, waitFor, fireEvent } from '@testing-library/react-native';
import { FeedbackScreen } from '../components/FeedbackScreen';
import { useFeedbackStore } from '../stores/feedbackStore';

// Mock the store
jest.mock('../stores/feedbackStore');

describe('FeedbackScreen', () => {
  const mockConversationData = {
    id: 'test-conversation',
    messages: [],
    score: 75,
    duration: 120,
  };

  beforeEach(() => {
    (useFeedbackStore as jest.Mock).mockReturnValue({
      generateFeedback: jest.fn(),
      currentFeedback: null,
      isAnalyzing: false,
    });
  });

  it('renders loading state initially', () => {
    (useFeedbackStore as jest.Mock).mockReturnValue({
      generateFeedback: jest.fn(),
      currentFeedback: null,
      isAnalyzing: true,
    });

    const { getByTestId } = render(
      <FeedbackScreen 
        conversationData={mockConversationData} 
        onNavigateNext={jest.fn()} 
      />
    );

    expect(getByTestId('feedback-loader')).toBeTruthy();
  });

  it('displays feedback when analysis completes', async () => {
    const mockFeedback = {
      score: 78,
      breakdown: { confidence: 80, flow: 75, appropriateness: 80, engagement: 78 },
      strengths: [{ id: '1', title: 'Great opener', description: 'Your opening was natural' }],
      improvements: [{ id: '2', title: 'Work on flow', description: 'Try smoother transitions' }],
    };

    (useFeedbackStore as jest.Mock).mockReturnValue({
      generateFeedback: jest.fn(),
      currentFeedback: mockFeedback,
      isAnalyzing: false,
    });

    const { getByText } = render(
      <FeedbackScreen 
        conversationData={mockConversationData} 
        onNavigateNext={jest.fn()} 
      />
    );

    await waitFor(() => {
      expect(getByText('78')).toBeTruthy();
      expect(getByText('Great opener')).toBeTruthy();
      expect(getByText('Work on flow')).toBeTruthy();
    });
  });

  it('handles accessibility correctly', () => {
    const mockFeedback = {
      score: 85,
      breakdown: { confidence: 85, flow: 80, appropriateness: 90, engagement: 85 },
      strengths: [],
      improvements: [],
    };

    (useFeedbackStore as jest.Mock).mockReturnValue({
      generateFeedback: jest.fn(),
      currentFeedback: mockFeedback,
      isAnalyzing: false,
    });

    const { getByLabelText } = render(
      <FeedbackScreen 
        conversationData={mockConversationData} 
        onNavigateNext={jest.fn()} 
      />
    );

    expect(getByLabelText(/conversation score.*85/i)).toBeTruthy();
  });
});
```

### Integration Tests

```typescript
// __tests__/feedbackIntegration.test.tsx
import { renderHook, act } from '@testing-library/react-hooks';
import { useFeedbackStore } from '../stores/feedbackStore';
import * as feedbackAPI from '../api/feedback';

jest.mock('../api/feedback');

describe('Feedback Integration', () => {
  it('generates feedback and updates store correctly', async () => {
    const mockFeedback = {
      id: 'feedback-1',
      score: 82,
      strengths: [],
      improvements: [],
    };

    (feedbackAPI.analyzeFeedback as jest.Mock).mockResolvedValue(mockFeedback);

    const { result } = renderHook(() => useFeedbackStore());

    await act(async () => {
      await result.current.generateFeedback({
        id: 'conv-1',
        messages: [],
      });
    });

    expect(result.current.currentFeedback).toEqual(mockFeedback);
    expect(result.current.isAnalyzing).toBe(false);
  });

  it('handles API failures gracefully', async () => {
    (feedbackAPI.analyzeFeedback as jest.Mock).mockRejectedValue(
      new Error('Network error')
    );

    const { result } = renderHook(() => useFeedbackStore());

    await act(async () => {
      await result.current.generateFeedback({
        id: 'conv-1',
        messages: [],
      });
    });

    expect(result.current.isAnalyzing).toBe(false);
    expect(result.current.currentFeedback).toBeTruthy(); // Should have fallback
  });
});
```

### Accessibility Tests

```typescript
// __tests__/feedbackAccessibility.test.tsx
import { render } from '@testing-library/react-native';
import { axe, toHaveNoViolations } from 'jest-axe';
import { FeedbackScreen } from '../components/FeedbackScreen';

expect.extend(toHaveNoViolations);

describe('Feedback Accessibility', () => {
  it('should not have accessibility violations', async () => {
    const { container } = render(
      <FeedbackScreen 
        conversationData={mockData} 
        onNavigateNext={jest.fn()} 
      />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('provides proper ARIA labels', () => {
    const { getByRole } = render(
      <FeedbackScreen 
        conversationData={mockData} 
        onNavigateNext={jest.fn()} 
      />
    );

    expect(getByRole('button', { name: /practice again/i })).toBeTruthy();
    expect(getByRole('region', { name: /feedback details/i })).toBeTruthy();
  });
});
```

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete user flow context
- **[Screen States](./screen-states.md)** - Visual specifications for implementation
- **[Interactions](./interactions.md)** - Animation and interaction details
- **[Accessibility](./accessibility.md)** - Inclusive design requirements
- **[Design System Components](../../design-system/components/)** - Reusable component specifications

## Implementation Checklist

### Core Functionality
- [ ] Feedback analysis API integration
- [ ] Score calculation and display
- [ ] Animated score reveal
- [ ] Feedback card system
- [ ] Progress tracking
- [ ] Action recommendations

### User Experience
- [ ] Smooth animations (60fps)
- [ ] Loading states and error handling
- [ ] Responsive design (mobile → desktop)
- [ ] Haptic feedback integration
- [ ] Accessibility compliance (WCAG 2.1 AA)

### Performance
- [ ] Bundle optimization
- [ ] Memory management
- [ ] Animation performance monitoring
- [ ] Offline functionality
- [ ] Caching strategy

### Testing
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Accessibility tests
- [ ] Performance tests
- [ ] User acceptance testing

## Last Updated
- **Version 1.0.0**: Complete implementation specification
- **Focus**: Production-ready React Native implementation with performance optimization
- **Next**: Development team implementation and testing