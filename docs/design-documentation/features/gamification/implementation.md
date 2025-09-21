# Gamification Implementation

---
title: FlirtCraft Gamification Technical Implementation Guide
description: Complete technical specifications for XP systems, achievements, streaks, and progress tracking implementation
feature: gamification
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ./interactions.md
  - ./accessibility.md
  - ../../design-system/components/gamification.md
  - ../../design-system/components/modals.md
  - ../../design-system/components/cards.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
dependencies:
  - Zustand state management
  - React Native AsyncStorage
  - Animation libraries
  - Local database (SQLite)
  - Push notification system
status: planned-phase-2
---

## Overview

This document provides comprehensive technical implementation specifications for FlirtCraft's gamification system, including state management architecture, local storage strategies, achievement detection algorithms, XP calculation systems, and performance optimizations for React Native implementation.

## Table of Contents

1. [State Management Architecture](#state-management-architecture)
2. [Local Storage and Persistence](#local-storage-and-persistence)
3. [XP Calculation System](#xp-calculation-system)
4. [Achievement Detection Engine](#achievement-detection-engine)
5. [Streak Tracking Implementation](#streak-tracking-implementation)
6. [Progress Analytics](#progress-analytics)
7. [Performance Optimizations](#performance-optimizations)
8. [Testing Strategy](#testing-strategy)

## State Management Architecture

### Zustand Store Structure

#### Core Gamification Store
```typescript
// stores/gamificationStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface GamificationState {
  // XP and Level System
  totalXP: number;
  currentLevel: number;
  xpForCurrentLevel: number;
  xpForNextLevel: number;
  
  // Achievement System
  achievements: Achievement[];
  unlockedAchievementIds: string[];
  achievementProgress: Record<string, number>;
  
  // Streak System
  currentStreak: number;
  longestStreak: number;
  lastPracticeDate: string | null;
  streakMultiplier: number;
  
  // Session Tracking
  totalConversations: number;
  conversationsThisWeek: number;
  conversationsThisMonth: number;
  
  // Skill Tracking
  skillProgress: SkillProgress;
  confidenceReports: ConfidenceReport[];
  
  // Feedback Metric Tracking (Integration with Feedback System)
  feedbackMetricHistory: {
    aiEngagementQuality: number[];
    responsivenessListening: number[];
    storytellingNarrative: number[];
    emotionalIntelligence: number[];
    conversationMomentum: number[];
    creativeFlirtation: number[];
  };
  averageMetricScores: {
    aiEngagementQuality: number;
    responsivenessListening: number;
    storytellingNarrative: number;
    emotionalIntelligence: number;
    conversationMomentum: number;
    creativeFlirtation?: number;
  };
  
  // Analytics Data
  dailyXPHistory: DailyXPRecord[];
  weeklyStats: WeeklyStats[];
  monthlyStats: MonthlyStats[];
  
  // Actions
  awardXP: (amount: number, source: XPSource) => void;
  unlockAchievement: (achievementId: string) => void;
  updateAchievementProgress: (achievementId: string, progress: number) => void;
  recordConversation: (conversationData: ConversationRecord) => void;
  updateStreak: () => void;
  calculateLevel: () => void;
  generateWeeklyReport: () => WeeklyReport;
  exportProgress: () => GamificationExport;
  resetProgress: () => void;
}

// Achievement Interface
interface Achievement {
  id: string;
  name: string;
  description: string;
  category: AchievementCategory;
  xpReward: number;
  criteria: AchievementCriteria;
  isSecret: boolean;
  unlockDate?: string;
  iconName: string;
}

// XP Source Types
interface XPSource {
  type: 'conversation' | 'bonus' | 'achievement' | 'streak';
  description: string;
  multiplier?: number;
}

// Skill Progress Tracking
interface SkillProgress {
  questionAsking: SkillLevel;
  activeListening: SkillLevel;
  storytelling: SkillLevel;
  contextUsage: SkillLevel;
  confidenceBuilding: SkillLevel;
}

interface SkillLevel {
  level: number;
  xp: number;
  conversationsWithSkill: number;
  lastImprovement: string;
}
```

#### Store Implementation
```typescript
export const useGamificationStore = create<GamificationState>()(
  persist(
    (set, get) => ({
      // Initial State
      totalXP: 0,
      currentLevel: 1,
      xpForCurrentLevel: 0,
      xpForNextLevel: LEVEL_THRESHOLDS[1],
      achievements: ACHIEVEMENT_DEFINITIONS,
      unlockedAchievementIds: [],
      achievementProgress: {},
      currentStreak: 0,
      longestStreak: 0,
      lastPracticeDate: null,
      streakMultiplier: 1.0,
      totalConversations: 0,
      conversationsThisWeek: 0,
      conversationsThisMonth: 0,
      skillProgress: initializeSkillProgress(),
      confidenceReports: [],
      dailyXPHistory: [],
      weeklyStats: [],
      monthlyStats: [],
      
      // XP Award Action
      awardXP: (amount: number, source: XPSource) => {
        set((state) => {
          const multipliedAmount = amount * (source.multiplier || 1) * state.streakMultiplier;
          const newTotalXP = state.totalXP + multipliedAmount;
          
          // Update daily XP history
          const today = new Date().toISOString().split('T')[0];
          const updatedHistory = [...state.dailyXPHistory];
          const todayRecord = updatedHistory.find(record => record.date === today);
          
          if (todayRecord) {
            todayRecord.xp += multipliedAmount;
            todayRecord.sources.push({ ...source, amount: multipliedAmount });
          } else {
            updatedHistory.push({
              date: today,
              xp: multipliedAmount,
              sources: [{ ...source, amount: multipliedAmount }],
              conversationsCompleted: source.type === 'conversation' ? 1 : 0
            });
          }
          
          const newState = {
            ...state,
            totalXP: newTotalXP,
            dailyXPHistory: updatedHistory.slice(-90) // Keep 90 days of history
          };
          
          // Calculate new level
          return calculateNewLevel(newState);
        });
      },
      
      // Achievement Unlock Action
      unlockAchievement: (achievementId: string) => {
        set((state) => {
          if (state.unlockedAchievementIds.includes(achievementId)) {
            return state; // Already unlocked
          }
          
          const achievement = state.achievements.find(a => a.id === achievementId);
          if (!achievement) {
            console.warn(`Achievement ${achievementId} not found`);
            return state;
          }
          
          // Award achievement XP
          const xpSource: XPSource = {
            type: 'achievement',
            description: `Achievement: ${achievement.name}`
          };
          
          return {
            ...state,
            unlockedAchievementIds: [...state.unlockedAchievementIds, achievementId],
            totalXP: state.totalXP + achievement.xpReward
          };
        });
      },
      
      // Conversation Recording Action
      recordConversation: (conversationData: ConversationRecord) => {
        set((state) => {
          const now = new Date();
          const today = now.toISOString().split('T')[0];
          
          // Update conversation counts
          const newState = {
            ...state,
            totalConversations: state.totalConversations + 1,
            conversationsThisWeek: calculateWeeklyConversations(state.dailyXPHistory, now),
            conversationsThisMonth: calculateMonthlyConversations(state.dailyXPHistory, now),
            lastPracticeDate: today
          };
          
          // Update skill progress based on conversation analysis
          const updatedSkillProgress = updateSkillProgress(
            state.skillProgress,
            conversationData
          );
          
          // Check for achievement unlocks
          const newlyUnlockedAchievements = checkAchievementUnlocks(
            newState,
            conversationData
          );
          
          return {
            ...newState,
            skillProgress: updatedSkillProgress,
            unlockedAchievementIds: [
              ...state.unlockedAchievementIds,
              ...newlyUnlockedAchievements
            ]
          };
        });
      },
      
      // Streak Update Action
      updateStreak: () => {
        set((state) => {
          const now = new Date();
          const today = now.toISOString().split('T')[0];
          const lastPractice = state.lastPracticeDate;
          
          if (!lastPractice) {
            // First conversation ever
            return {
              ...state,
              currentStreak: 1,
              longestStreak: Math.max(1, state.longestStreak),
              streakMultiplier: calculateStreakMultiplier(1)
            };
          }
          
          const daysSinceLastPractice = calculateDaysBetween(lastPractice, today);
          
          if (daysSinceLastPractice === 0) {
            // Same day practice - no streak change
            return state;
          } else if (daysSinceLastPractice === 1) {
            // Consecutive day - extend streak
            const newStreak = state.currentStreak + 1;
            return {
              ...state,
              currentStreak: newStreak,
              longestStreak: Math.max(newStreak, state.longestStreak),
              streakMultiplier: calculateStreakMultiplier(newStreak)
            };
          } else {
            // Streak broken - reset to 1
            return {
              ...state,
              currentStreak: 1,
              streakMultiplier: calculateStreakMultiplier(1)
            };
          }
        });
      },
      
      // Other actions...
      calculateLevel: () => {
        set((state) => calculateNewLevel(state));
      },
      
      generateWeeklyReport: (): WeeklyReport => {
        const state = get();
        return generateWeeklyAnalytics(state);
      },
      
      exportProgress: (): GamificationExport => {
        const state = get();
        return {
          exportDate: new Date().toISOString(),
          totalXP: state.totalXP,
          currentLevel: state.currentLevel,
          achievements: state.unlockedAchievementIds,
          streakRecord: {
            current: state.currentStreak,
            longest: state.longestStreak
          },
          skillProgress: state.skillProgress,
          analytics: {
            totalConversations: state.totalConversations,
            dailyHistory: state.dailyXPHistory.slice(-30),
            monthlyStats: state.monthlyStats
          }
        };
      },
      
      resetProgress: () => {
        set((state) => ({
          ...state,
          totalXP: 0,
          currentLevel: 1,
          unlockedAchievementIds: [],
          achievementProgress: {},
          currentStreak: 0,
          lastPracticeDate: null,
          skillProgress: initializeSkillProgress(),
          dailyXPHistory: [],
          weeklyStats: [],
          monthlyStats: []
        }));
      }
    }),
    {
      name: 'flirtcraft-gamification',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        // Only persist essential data
        totalXP: state.totalXP,
        currentLevel: state.currentLevel,
        unlockedAchievementIds: state.unlockedAchievementIds,
        achievementProgress: state.achievementProgress,
        currentStreak: state.currentStreak,
        longestStreak: state.longestStreak,
        lastPracticeDate: state.lastPracticeDate,
        skillProgress: state.skillProgress,
        dailyXPHistory: state.dailyXPHistory,
        totalConversations: state.totalConversations
      })
    }
  )
);
```

## Local Storage and Persistence

### AsyncStorage Strategy

#### Data Structure Optimization
```typescript
// utils/storageOptimization.ts
interface StorageStrategy {
  key: string;
  compressionLevel: 'none' | 'light' | 'heavy';
  syncFrequency: 'immediate' | 'batched' | 'periodic';
  maxSize: number; // bytes
}

const STORAGE_STRATEGIES: Record<string, StorageStrategy> = {
  // Critical data - immediate sync, no compression
  progress: {
    key: 'gamification-progress',
    compressionLevel: 'none',
    syncFrequency: 'immediate',
    maxSize: 10240 // 10KB
  },
  
  // Analytics data - batched sync, light compression
  analytics: {
    key: 'gamification-analytics',
    compressionLevel: 'light',
    syncFrequency: 'batched',
    maxSize: 51200 // 50KB
  },
  
  // Historical data - periodic sync, heavy compression
  history: {
    key: 'gamification-history',
    compressionLevel: 'heavy',
    syncFrequency: 'periodic',
    maxSize: 102400 // 100KB
  }
};

class GamificationStorage {
  private static instance: GamificationStorage;
  private batchQueue: StorageOperation[] = [];
  private isProcessing = false;
  
  static getInstance(): GamificationStorage {
    if (!this.instance) {
      this.instance = new GamificationStorage();
    }
    return this.instance;
  }
  
  async saveProgress(data: GamificationProgress): Promise<void> {
    try {
      const optimizedData = this.optimizeData(data, 'progress');
      await AsyncStorage.setItem(STORAGE_STRATEGIES.progress.key, JSON.stringify(optimizedData));
    } catch (error) {
      console.error('Failed to save gamification progress:', error);
      throw new StorageError('Progress save failed', error);
    }
  }
  
  async loadProgress(): Promise<GamificationProgress | null> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_STRATEGIES.progress.key);
      if (!data) return null;
      
      const parsed = JSON.parse(data);
      return this.hydrateData(parsed, 'progress');
    } catch (error) {
      console.error('Failed to load gamification progress:', error);
      return null; // Graceful degradation
    }
  }
  
  private optimizeData(data: any, strategy: keyof typeof STORAGE_STRATEGIES): any {
    const config = STORAGE_STRATEGIES[strategy];
    
    // Remove unnecessary fields for storage
    const optimized = { ...data };
    
    // Apply compression based on strategy
    switch (config.compressionLevel) {
      case 'light':
        return this.lightCompress(optimized);
      case 'heavy':
        return this.heavyCompress(optimized);
      default:
        return optimized;
    }
  }
  
  private lightCompress(data: any): any {
    // Remove computed fields that can be recalculated
    const { computedFields, ...essential } = data;
    return essential;
  }
  
  private heavyCompress(data: any): any {
    // Compress arrays, round numbers, remove old entries
    if (data.dailyXPHistory) {
      data.dailyXPHistory = data.dailyXPHistory
        .slice(-30) // Keep only last 30 days
        .map((day: any) => ({
          ...day,
          xp: Math.round(day.xp) // Round XP to integers
        }));
    }
    
    return data;
  }
}
```

#### Storage Migration System
```typescript
// utils/storageMigration.ts
interface MigrationStep {
  version: number;
  migrate: (data: any) => any;
  validate: (data: any) => boolean;
}

const MIGRATIONS: MigrationStep[] = [
  {
    version: 1,
    migrate: (data: any) => {
      // Initial version - no migration needed
      return { ...data, version: 1 };
    },
    validate: (data: any) => data.version === 1
  },
  {
    version: 2,
    migrate: (data: any) => {
      // Add skill tracking to existing progress
      return {
        ...data,
        skillProgress: initializeSkillProgress(),
        version: 2
      };
    },
    validate: (data: any) => data.version === 2 && data.skillProgress
  }
];

class StorageMigrationManager {
  async migrateIfNeeded(data: any): Promise<any> {
    const currentVersion = data.version || 0;
    const targetVersion = MIGRATIONS[MIGRATIONS.length - 1].version;
    
    if (currentVersion >= targetVersion) {
      return data; // No migration needed
    }
    
    let migratedData = { ...data };
    
    for (const migration of MIGRATIONS) {
      if (migration.version > currentVersion) {
        console.log(`Migrating gamification data to version ${migration.version}`);
        migratedData = migration.migrate(migratedData);
        
        if (!migration.validate(migratedData)) {
          throw new Error(`Migration to version ${migration.version} failed validation`);
        }
      }
    }
    
    return migratedData;
  }
}
```

## XP Calculation System

### XP Award Algorithms

#### Base XP Calculation
```typescript
// utils/xpCalculation.ts
interface ConversationMetrics {
  duration: number; // seconds
  messageCount: number;
  contextUsage: boolean;
  difficultyLevel: 'green' | 'yellow' | 'red';
  qualityScore: number; // 0-1 from AI assessment
  skillsUsed: string[];
  isFirstToday: boolean;
  isNewScenario: boolean;
  
  // Integration with Feedback System's 6 Advanced Metrics
  feedbackMetrics?: {
    aiEngagementQuality: number;      // 0-100 score from feedback system
    responsivenessListening: number;  // 0-100 score from feedback system
    storytellingNarrative: number;    // 0-100 score from feedback system
    emotionalIntelligence: number;    // 0-100 score from feedback system
    conversationMomentum: number;     // 0-100 score from feedback system
    creativeFlirtation?: number;      // 0-100 score (Yellow/Red difficulty only)
  };
}

class XPCalculator {
  private static readonly BASE_XP = 100;
  private static readonly BONUS_MULTIPLIERS = {
    firstDaily: 0.5,      // +50 XP
    contextUsage: 0.15,   // +15 XP
    difficulty: {
      green: 0,
      yellow: 0.15,       // +15 XP
      red: 0.25          // +25 XP
    },
    newScenario: 0.2,     // +20 XP
    qualityBonus: 0.3     // Up to +30 XP
  };
  
  calculateTotalXP(metrics: ConversationMetrics, streakMultiplier: number = 1): XPBreakdown {
    const breakdown: XPBreakdown = {
      baseXP: XPCalculator.BASE_XP,
      bonuses: [],
      streakMultiplier,
      totalBeforeMultiplier: 0,
      finalTotal: 0
    };
    
    // First conversation of day bonus
    if (metrics.isFirstToday) {
      const bonus = Math.round(XPCalculator.BASE_XP * XPCalculator.BONUS_MULTIPLIERS.firstDaily);
      breakdown.bonuses.push({
        type: 'firstDaily',
        description: 'First conversation today',
        amount: bonus
      });
    }
    
    // Context usage bonus
    if (metrics.contextUsage) {
      const bonus = Math.round(XPCalculator.BASE_XP * XPCalculator.BONUS_MULTIPLIERS.contextUsage);
      breakdown.bonuses.push({
        type: 'contextUsage',
        description: 'Used context effectively',
        amount: bonus
      });
    }
    
    // Difficulty bonus
    const difficultyMultiplier = XPCalculator.BONUS_MULTIPLIERS.difficulty[metrics.difficultyLevel];
    if (difficultyMultiplier > 0) {
      const bonus = Math.round(XPCalculator.BASE_XP * difficultyMultiplier);
      breakdown.bonuses.push({
        type: 'difficulty',
        description: `${metrics.difficultyLevel.toUpperCase()} difficulty challenge`,
        amount: bonus
      });
    }
    
    // New scenario bonus
    if (metrics.isNewScenario) {
      const bonus = Math.round(XPCalculator.BASE_XP * XPCalculator.BONUS_MULTIPLIERS.newScenario);
      breakdown.bonuses.push({
        type: 'newScenario',
        description: 'Tried new scenario type',
        amount: bonus
      });
    }
    
    // Quality bonus (variable based on AI assessment)
    if (metrics.qualityScore > 0.6) {
      const qualityMultiplier = (metrics.qualityScore - 0.6) / 0.4; // Scale 0.6-1.0 to 0-1
      const maxQualityBonus = XPCalculator.BASE_XP * XPCalculator.BONUS_MULTIPLIERS.qualityBonus;
      const bonus = Math.round(maxQualityBonus * qualityMultiplier);
      
      if (bonus > 0) {
        breakdown.bonuses.push({
          type: 'quality',
          description: 'High conversation quality',
          amount: bonus
        });
      }
    }
    
    // Advanced Metric Bonuses from Feedback System
    if (metrics.feedbackMetrics) {
      // Bonus for exceptional AI Engagement (context usage)
      if (metrics.feedbackMetrics.aiEngagementQuality >= 80) {
        const engagementBonus = Math.round((metrics.feedbackMetrics.aiEngagementQuality - 80) * 0.5);
        breakdown.bonuses.push({
          type: 'ai_engagement',
          description: `Excellent context usage (${metrics.feedbackMetrics.aiEngagementQuality}/100)`,
          amount: engagementBonus
        });
      }
      
      // Bonus for strong emotional intelligence
      if (metrics.feedbackMetrics.emotionalIntelligence >= 75) {
        const eqBonus = Math.round((metrics.feedbackMetrics.emotionalIntelligence - 75) * 0.6);
        breakdown.bonuses.push({
          type: 'emotional_intelligence',
          description: `High emotional awareness (${metrics.feedbackMetrics.emotionalIntelligence}/100)`,
          amount: eqBonus
        });
      }
      
      // Bonus for excellent listening skills
      if (metrics.feedbackMetrics.responsivenessListening >= 85) {
        const listeningBonus = Math.round((metrics.feedbackMetrics.responsivenessListening - 85) * 0.8);
        breakdown.bonuses.push({
          type: 'active_listening',
          description: `Outstanding listening (${metrics.feedbackMetrics.responsivenessListening}/100)`,
          amount: listeningBonus
        });
      }
      
      // Bonus for creative flirtation (Yellow/Red difficulty only)
      if (metrics.feedbackMetrics.creativeFlirtation && metrics.feedbackMetrics.creativeFlirtation >= 70) {
        const flirtBonus = Math.round((metrics.feedbackMetrics.creativeFlirtation - 70) * 0.7);
        breakdown.bonuses.push({
          type: 'flirtation_mastery',
          description: `Masterful flirtation (${metrics.feedbackMetrics.creativeFlirtation}/100)`,
          amount: flirtBonus
        });
      }
    }
    
    // Calculate totals
    breakdown.totalBeforeMultiplier = breakdown.baseXP + 
      breakdown.bonuses.reduce((sum, bonus) => sum + bonus.amount, 0);
    
    breakdown.finalTotal = Math.round(breakdown.totalBeforeMultiplier * streakMultiplier);
    
    return breakdown;
  }
  
  calculateSkillXP(skillUsage: SkillUsage): SkillXPBreakdown {
    const skillXP: SkillXPBreakdown = {};
    
    for (const [skillName, usage] of Object.entries(skillUsage)) {
      if (usage.demonstrated) {
        const baseSkillXP = 10;
        const qualityMultiplier = usage.quality || 1;
        const skillXPAmount = Math.round(baseSkillXP * qualityMultiplier);
        
        skillXP[skillName] = {
          baseXP: baseSkillXP,
          qualityMultiplier,
          totalXP: skillXPAmount,
          description: `Demonstrated ${skillName.replace(/([A-Z])/g, ' $1').toLowerCase()}`
        };
      }
    }
    
    return skillXP;
  }
}

interface XPBreakdown {
  baseXP: number;
  bonuses: XPBonus[];
  streakMultiplier: number;
  totalBeforeMultiplier: number;
  finalTotal: number;
}

interface XPBonus {
  type: string;
  description: string;
  amount: number;
}
```

#### Level Progression System
```typescript
// utils/levelSystem.ts
class LevelSystem {
  // Level XP thresholds (exponential growth with diminishing returns)
  private static readonly LEVEL_THRESHOLDS = [
    0,      // Level 1: 0 XP
    200,    // Level 2: 200 XP
    500,    // Level 3: 500 XP  
    1000,   // Level 4: 1,000 XP
    1800,   // Level 5: 1,800 XP
    2800,   // Level 6: 2,800 XP
    4200,   // Level 7: 4,200 XP
    6000,   // Level 8: 6,000 XP
    8500,   // Level 9: 8,500 XP
    12000   // Level 10: 12,000 XP
  ];
  
  private static readonly LEVEL_BENEFITS: Record<number, string[]> = {
    2: ['Basic conversation scenarios unlocked'],
    3: ['Daily streak bonuses available'],
    4: ['Advanced conversation contexts'],
    5: ['Detailed progress analytics'],
    6: ['Premium scenario types'],
    7: ['Advanced achievement challenges'],
    8: ['Master-level conversation scenarios'],
    9: ['Expert analytics and insights'],
    10: ['All features and scenarios unlocked']
  };
  
  static calculateLevel(totalXP: number): LevelInfo {
    let currentLevel = 1;
    let xpForCurrentLevel = 0;
    let xpForNextLevel = LevelSystem.LEVEL_THRESHOLDS[1];
    
    for (let level = 1; level < LevelSystem.LEVEL_THRESHOLDS.length; level++) {
      if (totalXP >= LevelSystem.LEVEL_THRESHOLDS[level]) {
        currentLevel = level + 1;
        xpForCurrentLevel = LevelSystem.LEVEL_THRESHOLDS[level];
        xpForNextLevel = LevelSystem.LEVEL_THRESHOLDS[level + 1] || LevelSystem.LEVEL_THRESHOLDS[level];
      } else {
        break;
      }
    }
    
    const progressToNextLevel = totalXP - xpForCurrentLevel;
    const xpNeededForNextLevel = xpForNextLevel - totalXP;
    const progressPercentage = (progressToNextLevel / (xpForNextLevel - xpForCurrentLevel)) * 100;
    
    return {
      currentLevel,
      totalXP,
      xpForCurrentLevel,
      xpForNextLevel,
      progressToNextLevel,
      xpNeededForNextLevel,
      progressPercentage: Math.min(100, Math.max(0, progressPercentage)),
      benefits: LevelSystem.LEVEL_BENEFITS[currentLevel] || [],
      isMaxLevel: currentLevel >= LevelSystem.LEVEL_THRESHOLDS.length
    };
  }
  
  static getStreakMultiplier(streakDays: number): number {
    if (streakDays >= 30) return 2.0;      // 30+ days: 2x
    if (streakDays >= 14) return 1.5;      // 14-29 days: 1.5x
    if (streakDays >= 7) return 1.25;      // 7-13 days: 1.25x
    if (streakDays >= 3) return 1.1;       // 3-6 days: 1.1x
    return 1.0;                             // 0-2 days: 1x
  }
  
  static checkLevelUp(oldXP: number, newXP: number): LevelUpResult | null {
    const oldLevel = LevelSystem.calculateLevel(oldXP).currentLevel;
    const newLevel = LevelSystem.calculateLevel(newXP).currentLevel;
    
    if (newLevel > oldLevel) {
      return {
        oldLevel,
        newLevel,
        newBenefits: LevelSystem.LEVEL_BENEFITS[newLevel] || [],
        celebrationDuration: Math.min(5000, 2000 + (newLevel * 200)) // 2-5 seconds
      };
    }
    
    return null;
  }
}
```

## Achievement Detection Engine

### Achievement System Architecture

#### Achievement Definitions
```typescript
// data/achievements.ts
export const ACHIEVEMENT_DEFINITIONS: Achievement[] = [
  // Getting Started Series
  {
    id: 'first_steps',
    name: 'First Steps',
    description: 'Complete your first practice conversation',
    category: 'getting_started',
    xpReward: 5,
    iconName: 'star-outline',
    isSecret: false,
    criteria: {
      type: 'conversation_count',
      target: 1,
      conditions: []
    }
  },
  
  {
    id: 'breaking_ice',
    name: 'Breaking the Ice',
    description: 'Use a conversation starter in 3 different conversations',
    category: 'getting_started',
    xpReward: 15,
    iconName: 'ice-cube',
    isSecret: false,
    criteria: {
      type: 'skill_usage',
      skill: 'contextUsage',
      target: 3,
      conditions: ['unique_conversations']
    }
  },
  
  // Consistency Achievements
  {
    id: 'daily_practice',
    name: 'Daily Practice',
    description: 'Complete one conversation per day for 3 consecutive days',
    category: 'consistency',
    xpReward: 10,
    iconName: 'calendar-check',
    isSecret: false,
    criteria: {
      type: 'streak',
      target: 3,
      conditions: ['consecutive_days']
    }
  },
  
  {
    id: 'weekly_warrior',
    name: 'Weekly Warrior',
    description: 'Complete at least 5 conversations in one week',
    category: 'consistency',
    xpReward: 50,
    iconName: 'trophy',
    isSecret: false,
    criteria: {
      type: 'conversations_per_period',
      period: 'week',
      target: 5,
      conditions: []
    }
  },
  
  // Skill Development Achievements
  {
    id: 'question_asker',
    name: 'Question Asker',
    description: 'Ask engaging questions in 10 conversations',
    category: 'skill_development',
    xpReward: 20,
    iconName: 'help-circle',
    isSecret: false,
    criteria: {
      type: 'skill_demonstration',
      skill: 'questionAsking',
      target: 10,
      conditions: ['quality_threshold_0.7']
    }
  },
  
  // Advanced Achievements
  {
    id: 'versatile_conversationalist',
    name: 'Versatile Conversationalist',
    description: 'Successfully navigate all difficulty levels across all scenarios',
    category: 'advanced',
    xpReward: 75,
    iconName: 'diamond',
    isSecret: false,
    criteria: {
      type: 'scenario_completion',
      target: 'all',
      conditions: ['all_difficulties', 'all_locations']
    }
  },
  
  // Secret/Milestone Achievements
  {
    id: 'confidence_champion',
    name: 'Confidence Champion',
    description: 'Report increased confidence in 20 post-conversation surveys',
    category: 'milestone',
    xpReward: 80,
    iconName: 'trending-up',
    isSecret: true,
    criteria: {
      type: 'confidence_improvement',
      target: 20,
      conditions: ['positive_improvement']
    }
  },
  
  // Feedback Metric-Based Achievements
  {
    id: 'context_master',
    name: 'Context Master',
    description: 'Score 90+ in AI Engagement Quality 5 times',
    category: 'advanced',
    xpReward: 60,
    iconName: 'eye-outline',
    isSecret: false,
    criteria: {
      type: 'feedback_metric',
      metric: 'aiEngagementQuality',
      threshold: 90,
      target: 5,
      conditions: []
    }
  },
  {
    id: 'empathy_expert',
    name: 'Empathy Expert',
    description: 'Score 85+ in Emotional Intelligence 10 times',
    category: 'skill_development',
    xpReward: 70,
    iconName: 'heart-outline',
    isSecret: false,
    criteria: {
      type: 'feedback_metric',
      metric: 'emotionalIntelligence',
      threshold: 85,
      target: 10,
      conditions: []
    }
  },
  {
    id: 'conversation_conductor',
    name: 'Conversation Conductor',
    description: 'Master conversation flow with 85+ Momentum score 7 times',
    category: 'advanced',
    xpReward: 65,
    iconName: 'pulse',
    isSecret: false,
    criteria: {
      type: 'feedback_metric',
      metric: 'conversationMomentum',
      threshold: 85,
      target: 7,
      conditions: []
    }
  },
  {
    id: 'well_rounded_conversationalist',
    name: 'Well-Rounded Conversationalist',
    description: 'Score 70+ in all 6 metrics in a single conversation',
    category: 'advanced',
    xpReward: 100,
    iconName: 'star',
    isSecret: false,
    criteria: {
      type: 'all_metrics_threshold',
      threshold: 70,
      target: 1,
      conditions: ['single_conversation']
    }
  }
];
```

#### Achievement Detection Engine
```typescript
// services/achievementEngine.ts
class AchievementEngine {
  private achievements: Achievement[] = ACHIEVEMENT_DEFINITIONS;
  
  checkAchievements(
    userProgress: GamificationState,
    newConversation: ConversationRecord
  ): string[] {
    const newlyUnlocked: string[] = [];
    
    for (const achievement of this.achievements) {
      // Skip already unlocked achievements
      if (userProgress.unlockedAchievementIds.includes(achievement.id)) {
        continue;
      }
      
      // Check if criteria is met
      const currentProgress = this.calculateAchievementProgress(
        achievement,
        userProgress,
        newConversation
      );
      
      if (this.isCriteriaMet(achievement.criteria, currentProgress)) {
        newlyUnlocked.push(achievement.id);
      }
    }
    
    return newlyUnlocked;
  }
  
  private calculateAchievementProgress(
    achievement: Achievement,
    userProgress: GamificationState,
    newConversation?: ConversationRecord
  ): number {
    const { criteria } = achievement;
    
    switch (criteria.type) {
      case 'conversation_count':
        return userProgress.totalConversations;
        
      case 'streak':
        return userProgress.currentStreak;
        
      case 'conversations_per_period':
        return this.getConversationsInPeriod(
          userProgress.dailyXPHistory,
          criteria.period as 'week' | 'month'
        );
        
      case 'skill_demonstration':
        return this.countSkillDemonstrations(
          userProgress.skillProgress,
          criteria.skill as keyof SkillProgress,
          criteria.conditions
        );
        
      case 'scenario_completion':
        return this.calculateScenarioProgress(
          userProgress,
          criteria.conditions
        );
        
      case 'confidence_improvement':
        return userProgress.confidenceReports.filter(
          report => report.improvement > 0
        ).length;
        
      case 'feedback_metric':
        // Track specific feedback metric achievements
        if (newConversation?.feedbackMetrics) {
          const metricScore = newConversation.feedbackMetrics[criteria.metric as keyof typeof newConversation.feedbackMetrics];
          const threshold = criteria.threshold as number;
          if (metricScore && metricScore >= threshold) {
            // Count historical occurrences of this achievement
            const historicalCount = userProgress.feedbackMetricHistory?.[criteria.metric]?.filter(
              (score: number) => score >= threshold
            ).length || 0;
            return historicalCount + 1;
          }
        }
        return 0;
        
      case 'all_metrics_threshold':
        // Check if all 6 feedback metrics meet threshold
        if (newConversation?.feedbackMetrics) {
          const metrics = newConversation.feedbackMetrics;
          const threshold = criteria.threshold as number;
          const allMetricsMet = 
            metrics.aiEngagementQuality >= threshold &&
            metrics.responsivenessListening >= threshold &&
            metrics.storytellingNarrative >= threshold &&
            metrics.emotionalIntelligence >= threshold &&
            metrics.conversationMomentum >= threshold &&
            (!metrics.creativeFlirtation || metrics.creativeFlirtation >= threshold);
          
          return allMetricsMet ? 1 : 0;
        }
        return 0;
        
      default:
        return 0;
    }
  }
  
  private isCriteriaMet(criteria: AchievementCriteria, currentProgress: number): boolean {
    if (criteria.target === 'all') {
      return currentProgress >= 100; // Assuming 100% completion
    }
    
    return currentProgress >= (criteria.target as number);
  }
  
  private getConversationsInPeriod(
    history: DailyXPRecord[],
    period: 'week' | 'month'
  ): number {
    const now = new Date();
    const startDate = new Date();
    
    if (period === 'week') {
      startDate.setDate(now.getDate() - 7);
    } else {
      startDate.setMonth(now.getMonth() - 1);
    }
    
    return history
      .filter(record => new Date(record.date) >= startDate)
      .reduce((total, record) => total + record.conversationsCompleted, 0);
  }
  
  private countSkillDemonstrations(
    skillProgress: SkillProgress,
    skillName: keyof SkillProgress,
    conditions: string[]
  ): number {
    const skill = skillProgress[skillName];
    if (!skill) return 0;
    
    let count = skill.conversationsWithSkill;
    
    // Apply quality threshold condition
    const qualityThreshold = conditions.find(c => c.startsWith('quality_threshold_'));
    if (qualityThreshold) {
      const threshold = parseFloat(qualityThreshold.split('_')[2]);
      // Filter by quality - this would need to be tracked in more detail
      count = Math.floor(count * 0.8); // Approximation for demo
    }
    
    return count;
  }
  
  getAchievementProgress(
    achievementId: string,
    userProgress: GamificationState
  ): AchievementProgressInfo {
    const achievement = this.achievements.find(a => a.id === achievementId);
    if (!achievement) {
      throw new Error(`Achievement ${achievementId} not found`);
    }
    
    const currentProgress = this.calculateAchievementProgress(achievement, userProgress);
    const target = typeof achievement.criteria.target === 'number' 
      ? achievement.criteria.target 
      : 100;
    
    const percentage = Math.min(100, (currentProgress / target) * 100);
    
    return {
      achievementId,
      currentProgress,
      target,
      percentage,
      isCompleted: percentage >= 100,
      nextMilestone: this.getNextMilestone(achievement, currentProgress),
      estimatedCompletion: this.estimateCompletionTime(achievement, currentProgress, userProgress)
    };
  }
  
  private getNextMilestone(achievement: Achievement, currentProgress: number): string {
    const target = typeof achievement.criteria.target === 'number' 
      ? achievement.criteria.target 
      : 100;
    
    const remaining = target - currentProgress;
    
    switch (achievement.criteria.type) {
      case 'conversation_count':
        return `${remaining} more conversation${remaining === 1 ? '' : 's'}`;
      case 'streak':
        return `${remaining} more consecutive day${remaining === 1 ? '' : 's'}`;
      case 'skill_demonstration':
        return `Demonstrate ${achievement.criteria.skill} in ${remaining} more conversation${remaining === 1 ? '' : 's'}`;
      default:
        return `${remaining} more to complete`;
    }
  }
}
```

## Streak Tracking Implementation

### Streak Calculation System

#### Daily Streak Logic
```typescript
// services/streakService.ts
class StreakService {
  private timezone: string;
  
  constructor(timezone: string = Intl.DateTimeFormat().resolvedOptions().timeZone) {
    this.timezone = timezone;
  }
  
  calculateCurrentStreak(practiceHistory: DailyXPRecord[]): StreakInfo {
    if (practiceHistory.length === 0) {
      return this.createEmptyStreakInfo();
    }
    
    const today = this.getCurrentDate();
    const sortedHistory = practiceHistory
      .filter(record => record.conversationsCompleted > 0)
      .sort((a, b) => b.date.localeCompare(a.date));
    
    if (sortedHistory.length === 0) {
      return this.createEmptyStreakInfo();
    }
    
    const mostRecentPractice = sortedHistory[0].date;
    const daysSinceLastPractice = this.getDaysDifference(mostRecentPractice, today);
    
    // If more than 1 day since last practice, streak is broken
    if (daysSinceLastPractice > 1) {
      return {
        currentStreak: 0,
        lastPracticeDate: mostRecentPractice,
        isActive: false,
        canContinueToday: true,
        nextMilestone: this.getNextMilestone(0),
        graceTimeRemaining: null
      };
    }
    
    // Calculate consecutive days
    let streak = 0;
    let currentDate = today;
    
    for (const record of sortedHistory) {
      const recordDate = record.date;
      const daysDiff = this.getDaysDifference(recordDate, currentDate);
      
      if (daysDiff === 0) {
        // Same day
        streak++;
        currentDate = this.subtractDays(currentDate, 1);
      } else if (daysDiff === 1 && streak === 0) {
        // Yesterday (starting streak count)
        streak++;
        currentDate = this.subtractDays(currentDate, 1);
      } else {
        // Gap in practice - stop counting
        break;
      }
    }
    
    return {
      currentStreak: streak,
      lastPracticeDate: mostRecentPractice,
      isActive: daysSinceLastPractice === 0,
      canContinueToday: daysSinceLastPractice <= 0,
      nextMilestone: this.getNextMilestone(streak),
      graceTimeRemaining: this.calculateGraceTime(mostRecentPractice)
    };
  }
  
  private calculateGraceTime(lastPracticeDate: string): number | null {
    const lastPractice = new Date(lastPracticeDate + 'T23:59:59');
    const now = new Date();
    const gracePeriodEnd = new Date(lastPractice.getTime() + (25 * 60 * 60 * 1000)); // 25 hours grace
    
    if (now > gracePeriodEnd) {
      return null; // Grace period expired
    }
    
    return gracePeriodEnd.getTime() - now.getTime(); // Milliseconds remaining
  }
  
  private getNextMilestone(currentStreak: number): StreakMilestone {
    const milestones = [
      { days: 3, name: 'Streak Starter', multiplier: 1.1 },
      { days: 7, name: 'Weekly Warrior', multiplier: 1.25 },
      { days: 14, name: 'Dedicated Learner', multiplier: 1.5 },
      { days: 30, name: 'Master of Consistency', multiplier: 2.0 }
    ];
    
    for (const milestone of milestones) {
      if (currentStreak < milestone.days) {
        return {
          daysNeeded: milestone.days - currentStreak,
          name: milestone.name,
          multiplier: milestone.multiplier,
          description: `Reach ${milestone.days} consecutive days to unlock ${milestone.name}`
        };
      }
    }
    
    // Already at max milestone
    return {
      daysNeeded: 0,
      name: 'Master of Consistency',
      multiplier: 2.0,
      description: 'You\'ve reached the highest streak level!'
    };
  }
  
  private getCurrentDate(): string {
    return new Date().toLocaleDateString('en-CA'); // YYYY-MM-DD format
  }
  
  private getDaysDifference(date1: string, date2: string): number {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    const timeDiff = d2.getTime() - d1.getTime();
    return Math.floor(timeDiff / (1000 * 3600 * 24));
  }
  
  private subtractDays(date: string, days: number): string {
    const d = new Date(date);
    d.setDate(d.getDate() - days);
    return d.toLocaleDateString('en-CA');
  }
  
  private createEmptyStreakInfo(): StreakInfo {
    return {
      currentStreak: 0,
      lastPracticeDate: null,
      isActive: false,
      canContinueToday: true,
      nextMilestone: this.getNextMilestone(0),
      graceTimeRemaining: null
    };
  }
}
```

#### Streak Notification System
```typescript
// services/streakNotifications.ts
class StreakNotificationService {
  private notificationScheduler: NotificationScheduler;
  
  constructor(notificationScheduler: NotificationScheduler) {
    this.notificationScheduler = notificationScheduler;
  }
  
  scheduleStreakReminders(streakInfo: StreakInfo): void {
    // Cancel existing streak notifications
    this.notificationScheduler.cancelByCategory('streak');
    
    if (!streakInfo.isActive && streakInfo.currentStreak > 0) {
      // Schedule reminder for streak continuation
      const reminderTime = new Date();
      reminderTime.setHours(19, 0, 0, 0); // 7 PM reminder
      
      if (reminderTime > new Date()) {
        this.notificationScheduler.schedule({
          id: 'streak-reminder-today',
          category: 'streak',
          title: `Continue Your ${streakInfo.currentStreak}-Day Streak!`,
          body: 'Practice a conversation today to keep your learning momentum going.',
          scheduledTime: reminderTime,
          priority: 'normal'
        });
      }
    }
    
    // Schedule milestone celebration notifications
    if (streakInfo.nextMilestone.daysNeeded === 1) {
      const celebrationTime = new Date();
      celebrationTime.setDate(celebrationTime.getDate() + 1);
      celebrationTime.setHours(9, 0, 0, 0); // 9 AM celebration
      
      this.notificationScheduler.schedule({
        id: 'streak-milestone-celebration',
        category: 'streak',
        title: 'Streak Milestone Achieved!',
        body: `Congratulations! You've unlocked ${streakInfo.nextMilestone.name}!`,
        scheduledTime: celebrationTime,
        priority: 'high'
      });
    }
  }
  
  sendStreakBreakRecovery(brokenStreakLength: number): void {
    // Gentle recovery message after streak is broken
    setTimeout(() => {
      this.notificationScheduler.schedule({
        id: 'streak-recovery',
        category: 'streak',
        title: 'Ready to Start Fresh?',
        body: `Your ${brokenStreakLength}-day streak was impressive! Ready to start building a new one?`,
        scheduledTime: new Date(Date.now() + 30 * 60 * 1000), // 30 minutes delay
        priority: 'low'
      });
    }, 30 * 60 * 1000); // 30 minute delay
  }
}
```

## Progress Analytics

### Analytics Data Processing

#### Weekly and Monthly Reports
```typescript
// services/analyticsService.ts
class ProgressAnalyticsService {
  generateWeeklyReport(
    gamificationState: GamificationState,
    weekStartDate: Date = this.getWeekStart()
  ): WeeklyReport {
    const weekData = this.filterDataByWeek(
      gamificationState.dailyXPHistory,
      weekStartDate
    );
    
    const previousWeekData = this.filterDataByWeek(
      gamificationState.dailyXPHistory,
      new Date(weekStartDate.getTime() - 7 * 24 * 60 * 60 * 1000)
    );
    
    const totalXP = weekData.reduce((sum, day) => sum + day.xp, 0);
    const totalConversations = weekData.reduce((sum, day) => sum + day.conversationsCompleted, 0);
    const practiceDays = weekData.filter(day => day.conversationsCompleted > 0).length;
    
    const previousTotalXP = previousWeekData.reduce((sum, day) => sum + day.xp, 0);
    const previousTotalConversations = previousWeekData.reduce((sum, day) => sum + day.conversationsCompleted, 0);
    
    const newAchievements = this.getAchievementsUnlockedInPeriod(
      gamificationState.unlockedAchievementIds,
      weekStartDate,
      7
    );
    
    return {
      period: {
        start: weekStartDate.toISOString(),
        end: new Date(weekStartDate.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString()
      },
      metrics: {
        totalXP,
        totalConversations,
        practiceDays,
        averageXPPerDay: Math.round(totalXP / 7),
        averageConversationsPerDay: Math.round(totalConversations / 7 * 10) / 10
      },
      comparisons: {
        xpChange: {
          absolute: totalXP - previousTotalXP,
          percentage: previousTotalXP > 0 ? Math.round(((totalXP - previousTotalXP) / previousTotalXP) * 100) : 0
        },
        conversationChange: {
          absolute: totalConversations - previousTotalConversations,
          percentage: previousTotalConversations > 0 ? 
            Math.round(((totalConversations - previousTotalConversations) / previousTotalConversations) * 100) : 0
        }
      },
      achievements: {
        unlocked: newAchievements.length,
        details: newAchievements
      },
      dailyBreakdown: weekData.map(day => ({
        date: day.date,
        xp: day.xp,
        conversations: day.conversationsCompleted,
        sources: day.sources
      })),
      insights: this.generateWeeklyInsights(weekData, previousWeekData),
      goals: this.generateNextWeekGoals(weekData, gamificationState)
    };
  }
  
  generateMonthlyReport(
    gamificationState: GamificationState,
    monthStartDate: Date = this.getMonthStart()
  ): MonthlyReport {
    const monthData = this.filterDataByMonth(
      gamificationState.dailyXPHistory,
      monthStartDate
    );
    
    const skillAnalysis = this.analyzeSkillDevelopment(
      gamificationState.skillProgress,
      monthData
    );
    
    const streakAnalysis = this.analyzeStreakPatterns(monthData);
    const practicePatterns = this.analyzePracticePatterns(monthData);
    
    return {
      period: {
        start: monthStartDate.toISOString(),
        end: new Date(monthStartDate.getFullYear(), monthStartDate.getMonth() + 1, 0).toISOString()
      },
      summary: {
        totalXP: monthData.reduce((sum, day) => sum + day.xp, 0),
        totalConversations: monthData.reduce((sum, day) => sum + day.conversationsCompleted, 0),
        activeDays: monthData.filter(day => day.conversationsCompleted > 0).length,
        averageSessionsPerWeek: this.calculateAverageSessionsPerWeek(monthData),
        longestStreak: streakAnalysis.longestStreak
      },
      skillDevelopment: skillAnalysis,
      practicePatterns,
      achievements: {
        unlocked: this.getAchievementsUnlockedInPeriod(
          gamificationState.unlockedAchievementIds,
          monthStartDate,
          30
        )
      },
      insights: this.generateMonthlyInsights(monthData, skillAnalysis, practicePatterns),
      recommendations: this.generateRecommendations(gamificationState)
    };
  }
  
  private analyzeSkillDevelopment(
    skillProgress: SkillProgress,
    monthData: DailyXPRecord[]
  ): SkillAnalysis {
    const skillAnalysis: SkillAnalysis = {};
    
    for (const [skillName, skill] of Object.entries(skillProgress)) {
      const conversationsThisMonth = monthData
        .reduce((sum, day) => sum + day.conversationsCompleted, 0);
      
      const skillUsageRate = skill.conversationsWithSkill / conversationsThisMonth;
      const improvementTrend = this.calculateSkillTrend(skill, monthData);
      
      skillAnalysis[skillName] = {
        currentLevel: skill.level,
        totalXP: skill.xp,
        usageRate: skillUsageRate,
        improvementTrend,
        conversationsWithSkill: skill.conversationsWithSkill,
        lastImprovement: skill.lastImprovement,
        insights: this.generateSkillInsights(skillName, skill, skillUsageRate, improvementTrend)
      };
    }
    
    return skillAnalysis;
  }
  
  private analyzePracticePatterns(monthData: DailyXPRecord[]): PracticePatternAnalysis {
    const dayOfWeekPattern = this.calculateDayOfWeekPattern(monthData);
    const timeConsistency = this.calculateTimeConsistency(monthData);
    const sessionLengthTrends = this.calculateSessionLengthTrends(monthData);
    
    return {
      preferredDays: this.getPreferredPracticeDays(dayOfWeekPattern),
      consistencyScore: timeConsistency.score,
      averageSessionLength: sessionLengthTrends.average,
      sessionLengthTrend: sessionLengthTrends.trend,
      insights: [
        `You practice most frequently on ${this.getMostActiveDays(dayOfWeekPattern).join(' and ')}`,
        timeConsistency.score > 0.7 ? 
          'Your practice schedule is very consistent' : 
          'Consider establishing a more regular practice routine',
        sessionLengthTrends.trend > 0 ? 
          'Your practice sessions are getting longer over time' :
          'Try gradually extending your practice sessions'
      ]
    };
  }
  
  private generateRecommendations(state: GamificationState): Recommendation[] {
    const recommendations: Recommendation[] = [];
    
    // Streak-based recommendations
    if (state.currentStreak === 0 && state.longestStreak > 0) {
      recommendations.push({
        type: 'streak_recovery',
        priority: 'medium',
        title: 'Rebuild Your Practice Streak',
        description: `You had a great ${state.longestStreak}-day streak before. Start with just one conversation today to begin building again.`,
        action: 'Start Practice Session'
      });
    }
    
    // Achievement-based recommendations
    const nearCompletionAchievements = this.findNearCompletionAchievements(state);
    nearCompletionAchievements.forEach(achievement => {
      recommendations.push({
        type: 'achievement_completion',
        priority: 'high',
        title: `Almost there: ${achievement.name}`,
        description: `You're close to unlocking this achievement. ${achievement.nextSteps}`,
        action: 'View Achievement Details'
      });
    });
    
    // Skill development recommendations
    const skillRecommendations = this.generateSkillRecommendations(state.skillProgress);
    recommendations.push(...skillRecommendations);
    
    return recommendations.slice(0, 5); // Limit to 5 recommendations
  }
}
```

## Performance Optimizations

### Efficient State Management

#### Memoization and Optimization
```typescript
// hooks/useOptimizedGamification.ts
import { useMemo, useCallback } from 'react';
import { useGamificationStore } from '../stores/gamificationStore';

export const useOptimizedGamification = () => {
  const store = useGamificationStore();
  
  // Memoized derived state
  const levelInfo = useMemo(() => {
    return LevelSystem.calculateLevel(store.totalXP);
  }, [store.totalXP]);
  
  const streakInfo = useMemo(() => {
    return new StreakService().calculateCurrentStreak(store.dailyXPHistory);
  }, [store.dailyXPHistory, store.lastPracticeDate]);
  
  const achievementProgress = useMemo(() => {
    const engine = new AchievementEngine();
    return ACHIEVEMENT_DEFINITIONS.map(achievement => 
      engine.getAchievementProgress(achievement.id, store)
    );
  }, [store.totalConversations, store.skillProgress, store.unlockedAchievementIds]);
  
  // Memoized analytics
  const weeklyStats = useMemo(() => {
    return new ProgressAnalyticsService().generateWeeklyReport(store);
  }, [store.dailyXPHistory, store.totalXP]);
  
  // Optimized actions with debouncing
  const awardXP = useCallback(
    debounce((amount: number, source: XPSource) => {
      store.awardXP(amount, source);
    }, 100),
    [store]
  );
  
  const recordConversation = useCallback(
    throttle((conversationData: ConversationRecord) => {
      store.recordConversation(conversationData);
    }, 1000), // Prevent rapid-fire conversation recording
    [store]
  );
  
  return {
    // State
    totalXP: store.totalXP,
    currentLevel: levelInfo.currentLevel,
    levelProgress: levelInfo.progressPercentage,
    currentStreak: streakInfo.currentStreak,
    achievements: achievementProgress,
    weeklyStats,
    
    // Actions
    awardXP,
    recordConversation,
    unlockAchievement: store.unlockAchievement,
    updateStreak: store.updateStreak,
    
    // Computed values
    levelInfo,
    streakInfo,
    xpToNextLevel: levelInfo.xpNeededForNextLevel,
    streakMultiplier: LevelSystem.getStreakMultiplier(streakInfo.currentStreak)
  };
};

// Utility functions for optimization
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

#### Background Processing
```typescript
// services/backgroundProcessor.ts
class GamificationBackgroundProcessor {
  private queue: BackgroundTask[] = [];
  private isProcessing = false;
  private worker?: Worker;
  
  constructor() {
    this.initializeWorker();
  }
  
  private initializeWorker() {
    // For React Native, we'll use a simple queue system
    // For web, we could use Web Workers
    this.processQueue();
  }
  
  queueAchievementCheck(data: AchievementCheckData): void {
    this.queue.push({
      type: 'achievement_check',
      data,
      priority: 'normal',
      timestamp: Date.now()
    });
  }
  
  queueAnalyticsUpdate(data: AnalyticsData): void {
    this.queue.push({
      type: 'analytics_update',
      data,
      priority: 'low',
      timestamp: Date.now()
    });
  }
  
  queueProgressCalculation(data: ProgressData): void {
    this.queue.push({
      type: 'progress_calculation',
      data,
      priority: 'high',
      timestamp: Date.now()
    });
  }
  
  private async processQueue(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) {
      return;
    }
    
    this.isProcessing = true;
    
    try {
      // Sort by priority and timestamp
      this.queue.sort((a, b) => {
        const priorityOrder = { high: 3, normal: 2, low: 1 };
        const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];
        return priorityDiff !== 0 ? priorityDiff : a.timestamp - b.timestamp;
      });
      
      // Process up to 5 tasks at a time
      const tasksToProcess = this.queue.splice(0, 5);
      
      await Promise.all(tasksToProcess.map(task => this.processTask(task)));
      
    } catch (error) {
      console.error('Background processing error:', error);
    } finally {
      this.isProcessing = false;
      
      // Schedule next processing cycle
      if (this.queue.length > 0) {
        setTimeout(() => this.processQueue(), 100);
      }
    }
  }
  
  private async processTask(task: BackgroundTask): Promise<void> {
    switch (task.type) {
      case 'achievement_check':
        await this.processAchievementCheck(task.data as AchievementCheckData);
        break;
        
      case 'analytics_update':
        await this.processAnalyticsUpdate(task.data as AnalyticsData);
        break;
        
      case 'progress_calculation':
        await this.processProgressCalculation(task.data as ProgressData);
        break;
    }
  }
  
  private async processAchievementCheck(data: AchievementCheckData): Promise<void> {
    const engine = new AchievementEngine();
    const newAchievements = engine.checkAchievements(data.userProgress, data.newConversation);
    
    if (newAchievements.length > 0) {
      // Notify main thread of new achievements
      this.notifyMainThread('achievements_unlocked', newAchievements);
    }
  }
  
  private notifyMainThread(type: string, data: any): void {
    // In React Native, we'll use events or callbacks
    // In web with workers, we'd use postMessage
    if (this.onBackgroundProcessComplete) {
      this.onBackgroundProcessComplete(type, data);
    }
  }
  
  onBackgroundProcessComplete?: (type: string, data: any) => void;
}
```

### Memory Management

#### Data Cleanup and Optimization
```typescript
// services/dataCleanupService.ts
class GamificationDataCleanup {
  private static readonly HISTORY_RETENTION_DAYS = 90;
  private static readonly ANALYTICS_RETENTION_DAYS = 365;
  private static readonly CLEANUP_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours
  
  startAutomaticCleanup(): void {
    // Run cleanup immediately
    this.performCleanup();
    
    // Schedule recurring cleanup
    setInterval(() => {
      this.performCleanup();
    }, GamificationDataCleanup.CLEANUP_INTERVAL);
  }
  
  private performCleanup(): void {
    const store = useGamificationStore.getState();
    
    // Clean up old daily XP history
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - GamificationDataCleanup.HISTORY_RETENTION_DAYS);
    const cutoffDateString = cutoffDate.toISOString().split('T')[0];
    
    const cleanedHistory = store.dailyXPHistory.filter(
      record => record.date >= cutoffDateString
    );
    
    // Clean up old confidence reports
    const cleanedReports = store.confidenceReports.filter(
      report => new Date(report.date) >= cutoffDate
    );
    
    // Update store with cleaned data
    useGamificationStore.setState({
      dailyXPHistory: cleanedHistory,
      confidenceReports: cleanedReports
    });
    
    // Compress and archive old analytics data
    this.compressOldAnalytics(store);
    
    console.log('Gamification data cleanup completed');
  }
  
  private compressOldAnalytics(store: GamificationState): void {
    // Compress weekly stats older than 3 months into monthly summaries
    const threeMonthsAgo = new Date();
    threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
    
    const recentWeeklyStats = store.weeklyStats.filter(
      stat => new Date(stat.period.start) >= threeMonthsAgo
    );
    
    const oldWeeklyStats = store.weeklyStats.filter(
      stat => new Date(stat.period.start) < threeMonthsAgo
    );
    
    // Convert old weekly stats to monthly summaries
    const additionalMonthlyStats = this.compressWeeklyStatsToMonthly(oldWeeklyStats);
    
    useGamificationStore.setState({
      weeklyStats: recentWeeklyStats,
      monthlyStats: [...store.monthlyStats, ...additionalMonthlyStats]
    });
  }
}
```

## Testing Strategy

### Unit Testing

#### State Management Tests
```typescript
// __tests__/gamificationStore.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useGamificationStore } from '../stores/gamificationStore';

describe('GamificationStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useGamificationStore.getState().resetProgress();
  });
  
  describe('XP Award System', () => {
    it('should award base XP for conversation completion', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      act(() => {
        result.current.awardXP(100, {
          type: 'conversation',
          description: 'Conversation completed'
        });
      });
      
      expect(result.current.totalXP).toBe(100);
      expect(result.current.currentLevel).toBe(1);
    });
    
    it('should apply streak multiplier to XP awards', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      // Set up a 7-day streak (1.25x multiplier)
      act(() => {
        result.current.updateStreak();
        // Simulate 7 days of practice
        for (let i = 0; i < 6; i++) {
          result.current.updateStreak();
        }
      });
      
      act(() => {
        result.current.awardXP(100, {
          type: 'conversation',
          description: 'Conversation completed',
          multiplier: result.current.streakMultiplier
        });
      });
      
      expect(result.current.totalXP).toBe(125); // 100 * 1.25
    });
    
    it('should trigger level up when XP threshold is reached', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      act(() => {
        result.current.awardXP(200, {
          type: 'conversation',
          description: 'Large XP award'
        });
      });
      
      expect(result.current.currentLevel).toBe(2);
    });
  });
  
  describe('Achievement System', () => {
    it('should unlock achievement when criteria is met', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      act(() => {
        result.current.recordConversation({
          id: 'test-1',
          completedAt: new Date().toISOString(),
          duration: 300,
          qualityScore: 0.8,
          skillsUsed: ['questionAsking'],
          contextUsed: false
        });
      });
      
      expect(result.current.unlockedAchievementIds).toContain('first_steps');
    });
    
    it('should not unlock achievement twice', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      act(() => {
        result.current.unlockAchievement('first_steps');
        result.current.unlockAchievement('first_steps');
      });
      
      const firstStepsCount = result.current.unlockedAchievementIds.filter(
        id => id === 'first_steps'
      ).length;
      
      expect(firstStepsCount).toBe(1);
    });
  });
  
  describe('Streak System', () => {
    it('should start streak on first conversation', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      act(() => {
        result.current.updateStreak();
      });
      
      expect(result.current.currentStreak).toBe(1);
    });
    
    it('should reset streak after gap in practice', () => {
      const { result } = renderHook(() => useGamificationStore());
      
      // Set initial streak
      act(() => {
        result.current.updateStreak();
      });
      
      // Simulate 2-day gap by setting last practice date
      act(() => {
        const twoDaysAgo = new Date();
        twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
        useGamificationStore.setState({
          lastPracticeDate: twoDaysAgo.toISOString().split('T')[0]
        });
        result.current.updateStreak();
      });
      
      expect(result.current.currentStreak).toBe(1); // Reset to 1
    });
  });
});
```

#### Achievement Engine Tests
```typescript
// __tests__/achievementEngine.test.ts
import { AchievementEngine } from '../services/achievementEngine';
import { ACHIEVEMENT_DEFINITIONS } from '../data/achievements';

describe('AchievementEngine', () => {
  let engine: AchievementEngine;
  let mockUserProgress: GamificationState;
  
  beforeEach(() => {
    engine = new AchievementEngine();
    mockUserProgress = {
      totalXP: 0,
      currentLevel: 1,
      totalConversations: 0,
      currentStreak: 0,
      unlockedAchievementIds: [],
      skillProgress: initializeSkillProgress(),
      dailyXPHistory: [],
      confidenceReports: []
    };
  });
  
  it('should detect first steps achievement on first conversation', () => {
    const newConversation = {
      id: 'test-1',
      completedAt: new Date().toISOString(),
      duration: 300,
      qualityScore: 0.7
    };
    
    mockUserProgress.totalConversations = 1;
    
    const unlockedAchievements = engine.checkAchievements(mockUserProgress, newConversation);
    
    expect(unlockedAchievements).toContain('first_steps');
  });
  
  it('should detect weekly warrior achievement after 5 conversations in a week', () => {
    // Mock 5 conversations in current week
    const weekData = Array.from({ length: 5 }, (_, i) => ({
      date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      xp: 100,
      conversationsCompleted: 1,
      sources: []
    }));
    
    mockUserProgress.dailyXPHistory = weekData;
    mockUserProgress.totalConversations = 5;
    
    const newConversation = {
      id: 'test-5',
      completedAt: new Date().toISOString(),
      duration: 300,
      qualityScore: 0.7
    };
    
    const unlockedAchievements = engine.checkAchievements(mockUserProgress, newConversation);
    
    expect(unlockedAchievements).toContain('weekly_warrior');
  });
  
  it('should calculate achievement progress correctly', () => {
    mockUserProgress.totalConversations = 7;
    
    const progress = engine.getAchievementProgress('question_asker', mockUserProgress);
    
    expect(progress.currentProgress).toBe(7);
    expect(progress.percentage).toBe(70); // 7/10 * 100
    expect(progress.isCompleted).toBe(false);
  });
});
```

### Integration Testing

#### End-to-End Gamification Flow
```typescript
// __tests__/integration/gamificationFlow.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useOptimizedGamification } from '../hooks/useOptimizedGamification';

describe('Gamification Integration', () => {
  it('should handle complete conversation-to-achievement flow', async () => {
    const { result } = renderHook(() => useOptimizedGamification());
    
    // Start with empty state
    expect(result.current.totalXP).toBe(0);
    expect(result.current.currentLevel).toBe(1);
    expect(result.current.currentStreak).toBe(0);
    
    // Complete first conversation
    await act(async () => {
      result.current.recordConversation({
        id: 'integration-test-1',
        completedAt: new Date().toISOString(),
        duration: 300,
        qualityScore: 0.8,
        contextUsed: true,
        difficultyLevel: 'yellow',
        isFirstToday: true,
        skillsUsed: ['questionAsking']
      });
    });
    
    // Verify XP award and achievement unlock
    expect(result.current.totalXP).toBeGreaterThan(100); // Base + bonuses
    expect(result.current.currentStreak).toBe(1);
    expect(result.current.achievements.find(a => a.achievementId === 'first_steps')?.isCompleted).toBe(true);
    
    // Complete enough conversations to level up
    for (let i = 0; i < 3; i++) {
      await act(async () => {
        result.current.recordConversation({
          id: `integration-test-${i + 2}`,
          completedAt: new Date().toISOString(),
          duration: 300,
          qualityScore: 0.7,
          skillsUsed: ['activeListening']
        });
      });
    }
    
    // Verify level up
    expect(result.current.currentLevel).toBe(2);
    expect(result.current.levelProgress).toBeGreaterThan(0);
  });
});
```

---

## Related Documentation

- [Gamification Feature Overview](./README.md) - Complete system design and philosophy
- [Gamification User Journey](./user-journey.md) - User experience flow analysis
- [Gamification Screen States](./screen-states.md) - Visual interface specifications  
- [Gamification Interactions](./interactions.md) - Animation and interaction patterns
- [Gamification Accessibility](./accessibility.md) - Inclusive design implementation

## Implementation Dependencies

### Core Technology Stack
- **React Native**: 0.72+ for cross-platform mobile development
- **Zustand**: 4.4+ for state management with persistence
- **AsyncStorage**: For local data persistence and offline support
- **React Native Reanimated**: 3.0+ for smooth animations and transitions
- **React Native Haptic Feedback**: For tactile user feedback

### Optional Enhancements
- **Lottie React Native**: For complex achievement celebration animations
- **React Native Chart Kit**: For progress visualization and analytics charts
- **React Native Push Notifications**: For streak reminders and achievement celebrations
- **React Native SQLite Storage**: For advanced local data querying and analytics

### Development Tools
- **Jest**: Unit testing framework
- **React Native Testing Library**: Component testing utilities
- **Flipper**: Debugging and state inspection
- **CodePush**: Over-the-air updates for gamification improvements

---

*This implementation guide provides a comprehensive technical foundation for building FlirtCraft's gamification system with performance, scalability, and user experience as primary considerations while maintaining the privacy-first, confidence-building approach central to the app's mission.*