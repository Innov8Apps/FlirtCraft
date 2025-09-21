# Onboarding Feature - Implementation

---
title: Onboarding Feature Implementation Guide
description: Complete technical specifications and developer handoff for app onboarding system
feature: onboarding
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - accessibility.md
  - ../../design-system/components/buttons.md
  - ../../design-system/components/forms.md
  - ../../design-system/components/navigation.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/tokens/spacing.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native 0.72+ via Expo 52+
  - NativeBase with themed system
  - NativeWind 4.1 for utility-first styling
  - React Native Reanimated 3.6+ for 60fps animations
  - Zustand 4.4+ for global state management
  - React Hook Form 7.45+ for form state validation
  - React Query (@tanstack/react-query) for server state
  - React Navigation 6.x with Expo Router
  - Supabase JS SDK 2.39+ with Row Level Security
  - RevenueCat SDK for subscription management
status: approved
---

## Implementation Overview

The onboarding feature is the critical first impression system that introduces users to FlirtCraft, builds trust, and seamlessly transitions them into the app experience. This implementation guide provides complete technical specifications for building a trustworthy, accessible, and conversion-optimized onboarding flow.

## Table of Contents

1. [Component Architecture](#component-architecture)
2. [State Management](#state-management)
3. [Navigation System](#navigation-system)
4. [Animation Implementation](#animation-implementation)
5. [Platform Integration](#platform-integration)
6. [Analytics & Optimization](#analytics--optimization)

---

## Component Architecture

### Feature Structure

```
src/features/onboarding/
├── components/
│   ├── OnboardingFlow.tsx           # Main onboarding coordinator
│   ├── SplashScreen/
│   │   ├── index.tsx               # App launch splash
│   │   ├── BrandAnimation.tsx      # Logo animation component
│   │   └── LoadingIndicator.tsx    # Loading progress display
│   ├── WelcomeScreens/
│   │   ├── index.tsx               # Welcome screen container
│   │   ├── WelcomeIntro.tsx        # Main welcome message
│   │   ├── HowItWorksStep.tsx      # Individual "how it works" steps
│   │   ├── BenefitCard.tsx         # Benefit display cards
│   │   └── ValueProposition.tsx    # Why FlirtCraft works
│   ├── TrustBuilding/
│   │   ├── PrivacySafety.tsx       # Privacy assurance screen
│   │   ├── AgeVerification.tsx     # Age verification form
│   │   ├── TestimonialCards.tsx    # Success stories (optional)
│   │   └── SecurityBadges.tsx      # Trust indicators
│   ├── Registration/
│   │   ├── index.tsx               # Registration flow coordinator
│   │   ├── RegistrationForm.tsx    # Email/password registration
│   │   ├── SignInForm.tsx          # Existing user sign in
│   │   ├── PasswordStrength.tsx    # Password validation component
│   │   ├── EmailVerification.tsx   # Email verification UI
│   │   └── SupabaseAuth.tsx        # Supabase integration wrapper
│   ├── PermissionRequests/
│   │   ├── index.tsx               # Permission request coordinator
│   │   ├── NotificationPermission.tsx # Notification permission request
│   │   ├── AnalyticsConsent.tsx    # Analytics opt-in
│   │   └── PermissionModal.tsx     # Reusable permission dialog
│   ├── Completion/
│   │   ├── index.tsx               # Onboarding completion
│   │   ├── SuccessCelebration.tsx  # Completion animation
│   │   ├── ReadyToStart.tsx        # Transition to app
│   │   └── FirstAchievement.tsx    # Badge unlock animation
│   └── Navigation/
│       ├── StepIndicator.tsx       # Progress visualization
│       ├── NavigationButtons.tsx   # Next/back/skip buttons
│       ├── SkipOptions.tsx         # Skip functionality
│       └── KeyboardNavigation.tsx  # Keyboard navigation support
├── hooks/
│   ├── useOnboardingFlow.ts        # Flow management logic
│   ├── useOnboardingAnimations.ts  # Animation orchestration
│   ├── usePermissionRequests.ts    # Platform permission handling
│   ├── useOnboardingAnalytics.ts   # Analytics and tracking
│   ├── useAccessibilitySupport.ts  # Accessibility features
│   ├── useRegistrationValidation.ts # Email/password validation
│   ├── useSupabaseAuth.ts          # Supabase Auth integration
│   └── useTemporaryStorage.ts      # Local storage management
├── stores/
│   ├── onboardingStore.ts          # Zustand onboarding state
│   ├── permissionStore.ts          # Permission status management
│   └── registrationStore.ts        # Registration state and validation
├── types/
│   ├── onboarding.types.ts         # TypeScript definitions
│   └── permission.types.ts         # Permission-related types
├── utils/
│   ├── onboardingValidation.ts     # Input validation
│   ├── permissionManager.ts        # Platform permission handling
│   ├── onboardingAnalytics.ts      # Analytics tracking
│   ├── trustIndicators.ts          # Trust-building utilities
│   ├── passwordStrength.ts         # Password validation algorithms
│   ├── emailValidation.ts          # Email validation and availability checking
│   └── supabaseConfig.ts           # Supabase client configuration
└── constants/
    ├── onboardingSteps.ts          # Step definitions
    ├── trustMessages.ts            # Trust-building content
    ├── permissionConfig.ts         # Permission configurations
    └── registrationConfig.ts       # Password requirements and validation rules
```

### Core Component Dependencies

```typescript
// NativeBase Components with Themed System
import {
  Box,
  VStack,
  HStack,
  Text,
  Image,
  ScrollView,
  Toast,
  Progress,
  Button,
  ButtonText,
  Card,
  Modal,
  ModalBackdrop,
  ModalContent,
  ModalBody,
  Input,
  InputField,
  FormControl,
  FormControlLabel,
  FormControlLabelText,
  FormControlError,
  FormControlErrorText,
  Pressable,
  Center,
} from 'native-base';

// NativeWind 4.1 for Tailwind Utilities
import { styled } from 'nativewind';

// Design System Components (built on NativeBase)
import {
  PrimaryButton,
  SecondaryButton, 
  TextButton,
  InfoCard,
  ProgressIndicator,
} from '../../../design-system/components';

// Navigation
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';

// Animation
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  withSequence,
  FadeIn,
  SlideInRight,
  ZoomIn,
} from 'react-native-reanimated';

// Platform APIs
import { 
  AccessibilityInfo,
  PermissionsAndroid,
  Platform,
  Linking,
} from 'react-native';

// Supabase
import { createClient } from '@supabase/supabase-js';
import AsyncStorage from '@react-native-async-storage/async-storage';
```

---

## State Management

### Zustand Onboarding Store

```typescript
// stores/onboardingStore.ts
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface OnboardingStep {
  id: string;
  title: string;
  component: string;
  required: boolean;
  completed: boolean;
  skippable: boolean;
  validationSchema?: any; // React Hook Form schema
  estimatedDuration?: number; // seconds
  personaAdaptations?: {
    anxiousAlex?: Partial<OnboardingStep>;
    comebackCatherine?: Partial<OnboardingStep>;
    confidentCarlos?: Partial<OnboardingStep>;
    shySarah?: Partial<OnboardingStep>;
  };
}

interface RegistrationFormData {
  email: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: boolean;
  agreedToPrivacy: boolean;
  marketingOptIn: boolean;
}

interface PreferenceFormData {
  genderPreference: 'men' | 'women' | 'everyone';
  ageRangeMin: number;
  ageRangeMax: number;
  relationshipGoal: 'dating' | 'relationships' | 'practice' | 'confidence';
}

interface SkillGoalFormData {
  primaryGoals: ('conversation_starters' | 'keeping_flow' | 'storytelling')[];
  specificChallenges: string[];
  experienceLevel: 'beginner' | 'intermediate' | 'returning';
  practiceFrequency: 'daily' | 'weekly' | 'occasional';
}

interface OnboardingState {
  // Flow state
  currentStepIndex: number;
  totalSteps: number;
  steps: OnboardingStep[];
  isComplete: boolean;
  
  // User progress and analytics
  completedSteps: string[];
  skippedSteps: string[];
  startTime: Date | null;
  completionTime: Date | null;
  stepTimings: Record<string, { startTime: Date; endTime?: Date; duration?: number }>;
  dropOffPoints: { stepId: string; timestamp: Date; reason?: string }[];
  
  // Form data (structured for React Hook Form)
  formData: {
    registration: Partial<RegistrationFormData>;
    preferences: Partial<PreferenceFormData>;
    skillGoals: Partial<SkillGoalFormData>;
    ageVerification: { birthDate: Date | null; isVerified: boolean };
  };
  
  // Preferences and choices
  userChoices: {
    ageVerified: boolean;
    notificationsEnabled: boolean | null;
    analyticsOptIn: boolean | null;
    privacyLevel: 'standard' | 'enhanced';
    persona: 'anxiousAlex' | 'comebackCatherine' | 'confidentCarlos' | 'shySarah' | null;
    complexityPreference: 'simple' | 'standard' | 'detailed';
  };

  // Supabase Auth Integration
  authState: {
    user: any | null;
  
    session: any | null;
    emailVerificationSent: boolean;
    emailVerificationRequired: boolean;
    registrationComplete: boolean;
    authError: string | null;
  };
  
  // Validation and error state
  validation: {
    currentStepValid: boolean;
    validationErrors: Record<string, string[]>;
    isValidating: boolean;
  };
  
  // A/B Testing and Personalization
  experiments: {
    onboardingFlowVariant: 'control' | 'shortened' | 'detailed';
    welcomeMessageVariant: 'standard' | 'benefit_focused' | 'social_proof';
    permissionRequestVariant: 'standard' | 'benefit_heavy' | 'minimal';
  };
  
  // Flow control
  canGoBack: boolean;
  canSkipCurrent: boolean;
  isTransitioning: boolean;
  
  // Actions
  initializeOnboarding: () => void;
  goToNextStep: () => Promise<boolean>;
  goToPreviousStep: () => boolean;
  skipCurrentStep: () => void;
  jumpToStep: (stepIndex: number) => boolean;
  completeStep: (stepId: string, data?: any) => void;
  setUserChoice: (key: keyof OnboardingState['userChoices'], value: any) => void;
  setRegistrationData: (data: Partial<OnboardingState['registrationData']>) => void;
  completeOnboarding: () => Promise<void>;
  resetOnboarding: () => void;
}

const defaultSteps: OnboardingStep[] = [
  { id: 'welcome', title: 'Welcome', component: 'WelcomeIntro', required: true, completed: false, skippable: false },
  { id: 'howItWorks1', title: 'Choose Scenario', component: 'HowItWorksStep', required: true, completed: false, skippable: true },
  { id: 'howItWorks2', title: 'AI Conversation', component: 'HowItWorksStep', required: true, completed: false, skippable: true },
  { id: 'howItWorks3', title: 'Get Feedback', component: 'HowItWorksStep', required: true, completed: false, skippable: true },
  { id: 'privacy', title: 'Privacy & Safety', component: 'PrivacySafety', required: true, completed: false, skippable: false },
  { id: 'ageVerification', title: 'Age Verification', component: 'AgeVerification', required: true, completed: false, skippable: false },
  { id: 'registration', title: 'Create Account', component: 'Registration', required: true, completed: false, skippable: false },
  { id: 'preferences', title: 'Preferences', component: 'PreferenceSetup', required: true, completed: false, skippable: false },
  { id: 'skillGoals', title: 'Goals', component: 'SkillGoalSelection', required: true, completed: false, skippable: false },
  { id: 'notifications', title: 'Notifications', component: 'NotificationPermission', required: false, completed: false, skippable: true },
  { id: 'analytics', title: 'Help Improve', component: 'AnalyticsConsent', required: false, completed: false, skippable: true },
  { id: 'complete', title: 'Ready to Start', component: 'ReadyToStart', required: true, completed: false, skippable: false },
];

export const useOnboardingStore = create<OnboardingState>()(
  persist(
    subscribeWithSelector((set, get) => ({
      // Initial state
      currentStepIndex: 0,
      totalSteps: defaultSteps.length,
      steps: defaultSteps,
      isComplete: false,
      completedSteps: [],
      skippedSteps: [],
      startTime: null,
      completionTime: null,
      userChoices: {
        ageVerified: false,
        notificationsEnabled: null,
        analyticsOptIn: null,
        privacyLevel: 'standard',
      },
      registrationData: {
        email: '',
        password: '',
        isEmailVerified: false,
        registrationComplete: false,
      },
      canGoBack: false,
      canSkipCurrent: false,
      isTransitioning: false,

      // Actions
      initializeOnboarding: () => {
        set({
          currentStepIndex: 0,
          startTime: new Date(),
          isComplete: false,
          canGoBack: false,
          canSkipCurrent: get().steps[0]?.skippable || false,
        });

        // Track onboarding start
        analytics.track('onboarding_started', {
          timestamp: new Date().toISOString(),
          totalSteps: get().totalSteps,
        });
      },

      goToNextStep: async () => {
        const currentIndex = get().currentStepIndex;
        const steps = get().steps;
        const currentStep = steps[currentIndex];

        // Validate current step if required
        if (currentStep?.required && !currentStep.completed) {
          const isValid = await validateCurrentStep(currentStep.id);
          if (!isValid) {
            return false;
          }
        }

        // Mark current step as completed
        if (currentStep && !get().completedSteps.includes(currentStep.id)) {
          get().completeStep(currentStep.id);
        }

        const nextIndex = currentIndex + 1;
        if (nextIndex >= get().totalSteps) {
          // Complete onboarding
          await get().completeOnboarding();
          return true;
        }

        set({ isTransitioning: true });

        // Animate transition
        await new Promise(resolve => setTimeout(resolve, 300));

        set({
          currentStepIndex: nextIndex,
          canGoBack: nextIndex > 0,
          canSkipCurrent: steps[nextIndex]?.skippable || false,
          isTransitioning: false,
        });

        // Track step progression
        analytics.track('onboarding_step_completed', {
          stepId: currentStep?.id,
          stepIndex: currentIndex,
          nextStepId: steps[nextIndex]?.id,
        });

        return true;
      },

      goToPreviousStep: () => {
        const currentIndex = get().currentStepIndex;
        if (currentIndex <= 0) return false;

        const prevIndex = currentIndex - 1;
        const steps = get().steps;

        set({
          currentStepIndex: prevIndex,
          canGoBack: prevIndex > 0,
          canSkipCurrent: steps[prevIndex]?.skippable || false,
        });

        analytics.track('onboarding_step_back', {
          fromStepIndex: currentIndex,
          toStepIndex: prevIndex,
        });

        return true;
      },

      skipCurrentStep: () => {
        const currentIndex = get().currentStepIndex;
        const currentStep = get().steps[currentIndex];
        
        if (!currentStep?.skippable) return;

        // Add to skipped steps
        set(state => ({
          skippedSteps: [...state.skippedSteps, currentStep.id]
        }));

        // Proceed to next step
        get().goToNextStep();

        analytics.track('onboarding_step_skipped', {
          stepId: currentStep.id,
          stepIndex: currentIndex,
        });
      },

      jumpToStep: (stepIndex: number) => {
        const steps = get().steps;
        if (stepIndex < 0 || stepIndex >= steps.length) return false;

        set({
          currentStepIndex: stepIndex,
          canGoBack: stepIndex > 0,
          canSkipCurrent: steps[stepIndex]?.skippable || false,
        });

        return true;
      },

      completeStep: (stepId: string, data?: any) => {
        set(state => ({
          completedSteps: [...new Set([...state.completedSteps, stepId])],
          steps: state.steps.map(step =>
            step.id === stepId ? { ...step, completed: true } : step
          ),
        }));

        // Store step data if provided
        if (data) {
          // Handle step-specific data storage
          handleStepData(stepId, data);
        }
      },

      setUserChoice: (key, value) => {
        set(state => ({
          userChoices: {
            ...state.userChoices,
            [key]: value,
          },
        }));
      },

      setRegistrationData: (data) => {
        set(state => ({
          registrationData: {
            ...state.registrationData,
            ...data,
          },
        }));
      },

      completeOnboarding: async () => {
        const completionTime = new Date();
        const startTime = get().startTime;
        const duration = startTime ? completionTime.getTime() - startTime.getTime() : 0;
        const { registrationData, userChoices } = get();

        // Create Supabase Auth account and database record
        try {
          await createSupabaseAccount(registrationData, userChoices);
          
          set({
            isComplete: true,
            completionTime,
          });

          // Track completion
          analytics.track('onboarding_completed', {
            duration,
            completedSteps: get().completedSteps.length,
            skippedSteps: get().skippedSteps.length,
            userChoices: get().userChoices,
            registrationComplete: true,
          });

          // Transition to main app
          await navigateToMainApp();
        } catch (error) {
          console.error('Failed to complete onboarding:', error);
          // Handle onboarding completion error
          throw error;
        }
      },

      resetOnboarding: () => {
        set({
          currentStepIndex: 0,
          isComplete: false,
          completedSteps: [],
          skippedSteps: [],
          startTime: null,
          completionTime: null,
          steps: defaultSteps.map(step => ({ ...step, completed: false })),
          userChoices: {
            ageVerified: false,
            notificationsEnabled: null,
            analyticsOptIn: null,
            privacyLevel: 'standard',
          },
          registrationData: {
            email: '',
            password: '',
            isEmailVerified: false,
            registrationComplete: false,
          },
        });
      },
    })),
    {
      name: 'flirtcraft-onboarding',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        isComplete: state.isComplete,
        completedSteps: state.completedSteps,
        userChoices: state.userChoices,
        completionTime: state.completionTime,
      }),
    }
  )
);

// Helper functions
const validateCurrentStep = async (stepId: string): Promise<boolean> => {
  switch (stepId) {
    case 'ageVerification':
      return useOnboardingStore.getState().userChoices.ageVerified;
    case 'privacy':
      return true; // Privacy screen just needs to be viewed
    default:
      return true;
  }
};

const handleStepData = (stepId: string, data: any) => {
  switch (stepId) {
    case 'ageVerification':
      useOnboardingStore.getState().setUserChoice('ageVerified', data.isVerified);
      break;
    case 'registration':
      useOnboardingStore.getState().setRegistrationData({
        email: data.email,
        password: data.password,
        registrationComplete: data.registrationComplete || false,
      });
      break;
    case 'notifications':
      useOnboardingStore.getState().setUserChoice('notificationsEnabled', data.enabled);
      break;
    case 'analytics':
      useOnboardingStore.getState().setUserChoice('analyticsOptIn', data.optIn);
      break;
  }
};

const createSupabaseAccount = async (formData: any, userChoices: any) => {
  // Delayed account creation pattern - only create AFTER complete onboarding
  try {
    // 1. Create Supabase Auth account with email verification
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email: formData.registration.email,
      password: formData.registration.password,
      options: {
        emailRedirectTo: `${APP_URL}/auth/callback`,
        data: {
          // Additional metadata for the user
          onboarding_persona: userChoices.persona,
          privacy_level: userChoices.privacyLevel,
          marketing_opt_in: formData.registration.marketingOptIn,
        }
      }
    });

    if (authError) {
      throw new Error(`Failed to create account: ${authError.message}`);
    }

    const user = authData.user;
    if (!user) {
      throw new Error('User creation failed');
    }

    // 2. Create comprehensive user profile with RLS
    const { error: profileError } = await supabase.from('user_profiles').insert({
      id: user.id,
      email: user.email,
      
      // Onboarding data
      age_verified: userChoices.ageVerified,
      age_range_min: formData.preferences.ageRangeMin,
      age_range_max: formData.preferences.ageRangeMax,
      gender_preference: formData.preferences.genderPreference,
      relationship_goal: formData.preferences.relationshipGoal,
      
      // Skill goals
      primary_skills: formData.skillGoals.primaryGoals,
      specific_challenges: formData.skillGoals.specificChallenges,
      experience_level: formData.skillGoals.experienceLevel,
      practice_frequency: formData.skillGoals.practiceFrequency,
      
      // Preferences
      notifications_enabled: userChoices.notificationsEnabled,
      analytics_opt_in: userChoices.analyticsOptIn,
      privacy_level: userChoices.privacyLevel,
      persona_detected: userChoices.persona,
      
      // Metadata
      onboarding_completed: true,
      onboarding_completed_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });

    if (profileError) {
      throw new Error(`Failed to create user profile: ${profileError.message}`);
    }

    // 3. Initialize user progress tracking
    const { error: progressError } = await supabase.from('user_progress').insert({
      user_id: user.id,
      total_conversations: 0,
      total_practice_time: 0,
      current_streak: 0,
      longest_streak: 0,
      xp_points: 0,
      level: 1,
      achievements_unlocked: ['onboarding_complete'],
      created_at: new Date().toISOString(),
    });

    if (progressError) {
      console.warn('Failed to initialize user progress:', progressError.message);
      // Don't throw error - progress can be initialized later
    }

    // 4. Set up Row Level Security context
    await supabase.rpc('setup_user_security_context', { user_id: user.id });

    return {
      user: authData.user,
      session: authData.session,
      emailVerificationRequired: !user.email_confirmed_at
    };

  } catch (error) {
    console.error('Supabase account creation error:', error);
    throw error;
  }
};

// Supabase Auth helper functions
const signUpWithEmail = async (email: string, password: string) => {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${APP_URL}/auth/callback`,
      }
    });

    if (error) {
      return { success: false, error: error.message };
    }

    return { 
      success: true, 
      user: data.user, 
      emailVerificationRequired: !data.user?.email_confirmed_at 
    };
  } catch (error) {
    return { success: false, error: 'Network error occurred' };
  }
};

const signInWithEmail = async (email: string, password: string) => {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return { success: false, error: error.message };
    }

    return { success: true, user: data.user, session: data.session };
  } catch (error) {
    return { success: false, error: 'Network error occurred' };
  }
};

const resendEmailVerification = async () => {
  try {
    const { error } = await supabase.auth.resend({
      type: 'signup',
      email: getCurrentUserEmail(), // Implement this helper
    });
    
    return !error;
  } catch (error) {
    return false;
  }
};

const checkAuthState = async () => {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    return session;
  } catch (error) {
    return null;
  }
};

const navigateToMainApp = async () => {
  // Navigate to main app after successful onboarding completion
  // Implementation depends on navigation setup (React Navigation/Expo Router)
  try {
    // Clear onboarding state
    await AsyncStorage.removeItem('onboarding-state');
    
    // Navigate to main app
    navigation.reset({
      index: 0,
      routes: [{ name: 'MainApp' }],
    });
  } catch (error) {
    console.error('Navigation error:', error);
  }
};

// Database Schema and RLS Policies for Onboarding
const ONBOARDING_DATABASE_SCHEMA = `
-- User Profiles Table with RLS
CREATE TABLE user_profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT NOT NULL,
  
  -- Onboarding data
  age_verified BOOLEAN DEFAULT FALSE,
  age_range_min INTEGER,
  age_range_max INTEGER,
  gender_preference TEXT CHECK (gender_preference IN ('men', 'women', 'everyone')),
  relationship_goal TEXT CHECK (relationship_goal IN ('dating', 'relationships', 'practice', 'confidence')),
  
  -- Skill goals
  primary_skills TEXT[] DEFAULT '{}',
  specific_challenges TEXT[] DEFAULT '{}',
  experience_level TEXT CHECK (experience_level IN ('beginner', 'intermediate', 'returning')),
  practice_frequency TEXT CHECK (practice_frequency IN ('daily', 'weekly', 'occasional')),
  
  -- Preferences
  notifications_enabled BOOLEAN,
  analytics_opt_in BOOLEAN,
  privacy_level TEXT CHECK (privacy_level IN ('standard', 'enhanced')),
  persona_detected TEXT CHECK (persona_detected IN ('anxiousAlex', 'comebackCatherine', 'confidentCarlos', 'shySarah')),
  
  -- Metadata
  onboarding_completed BOOLEAN DEFAULT FALSE,
  onboarding_completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security Policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Users can only access their own profile
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

-- User Progress Table
CREATE TABLE user_progress (
  user_id UUID REFERENCES auth.users(id) PRIMARY KEY,
  total_conversations INTEGER DEFAULT 0,
  total_practice_time INTEGER DEFAULT 0, -- in minutes
  current_streak INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  xp_points INTEGER DEFAULT 0,
  level INTEGER DEFAULT 1,
  achievements_unlocked TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own progress" ON user_progress
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress" ON user_progress
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress" ON user_progress
  FOR UPDATE USING (auth.uid() = user_id);

-- Security Context Function
CREATE OR REPLACE FUNCTION setup_user_security_context(user_id UUID)
RETURNS VOID AS $$
BEGIN
  -- Set up any additional security context
  -- This can include setting session variables or initializing security policies
  PERFORM set_config('app.current_user_id', user_id::TEXT, TRUE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
`;

// Email validation and availability checking
const validateEmailAvailability = async (email: string): Promise<{ isAvailable: boolean; error?: string }> => {
  try {
    // Check if email is already registered
    const { data, error } = await supabase
      .from('user_profiles')
      .select('email')
      .eq('email', email.toLowerCase())
      .single();

    if (error && error.code === 'PGRST116') {
      // No rows found - email is available
      return { isAvailable: true };
    } else if (error) {
      return { isAvailable: false, error: 'Unable to check email availability' };
    } else if (data) {
      return { isAvailable: false, error: 'Email is already registered' };
    }

    return { isAvailable: true };
  } catch (error) {
    return { isAvailable: false, error: 'Network error occurred' };
  }
};
```

### Permission Management Store

```typescript
// stores/permissionStore.ts
interface PermissionState {
  permissions: {
    notifications: 'granted' | 'denied' | 'pending';
    analytics: 'granted' | 'denied' | 'pending';
  };
  
  // Actions
  requestNotificationPermission: () => Promise<boolean>;
  setAnalyticsPermission: (granted: boolean) => void;
  checkAllPermissions: () => Promise<void>;
}

export const usePermissionStore = create<PermissionState>()((set, get) => ({
  permissions: {
    notifications: 'pending',
    analytics: 'pending',
  },

  requestNotificationPermission: async () => {
    try {
      if (Platform.OS === 'ios') {
        const { status } = await Notifications.requestPermissionsAsync({
          ios: {
            allowAlert: true,
            allowBadge: true,
            allowSound: true,
            allowAnnouncements: false,
          },
        });
        
        const granted = status === 'granted';
        set(state => ({
          permissions: {
            ...state.permissions,
            notifications: granted ? 'granted' : 'denied',
          },
        }));
        
        return granted;
      } else {
        // Android notification permission handling
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS
        );
        
        const isGranted = granted === PermissionsAndroid.RESULTS.GRANTED;
        set(state => ({
          permissions: {
            ...state.permissions,
            notifications: isGranted ? 'granted' : 'denied',
          },
        }));
        
        return isGranted;
      }
    } catch (error) {
      console.error('Notification permission request failed:', error);
      return false;
    }
  },

  setAnalyticsPermission: (granted: boolean) => {
    set(state => ({
      permissions: {
        ...state.permissions,
        analytics: granted ? 'granted' : 'denied',
      },
    }));
  },

  checkAllPermissions: async () => {
    // Check current permission statuses
    const notificationStatus = await Notifications.getPermissionsAsync();
    
    set(state => ({
      permissions: {
        ...state.permissions,
        notifications: notificationStatus.status === 'granted' ? 'granted' : 'denied',
      },
    }));
  },
}));
```

---

## Navigation System

### Onboarding Navigation Setup

```typescript
// navigation/OnboardingNavigator.tsx
import { createStackNavigator } from '@react-navigation/stack';

type OnboardingStackParamList = {
  Splash: undefined;
  OnboardingFlow: undefined;
  MainApp: undefined;
};

const Stack = createStackNavigator<OnboardingStackParamList>();

export const OnboardingNavigator = () => {
  const { isComplete } = useOnboardingStore();
  
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        gestureEnabled: false, // Prevent swipe back during onboarding
        cardStyleInterpolator: ({ current }) => ({
          cardStyle: {
            opacity: current.progress,
          },
        }),
      }}
    >
      <Stack.Screen name="Splash" component={SplashScreen} />
      {!isComplete && (
        <Stack.Screen name="OnboardingFlow" component={OnboardingFlow} />
      )}
      <Stack.Screen name="MainApp" component={MainApp} />
    </Stack.Navigator>
  );
};
```

### Main Onboarding Flow Component

```typescript
// components/OnboardingFlow.tsx
import React, { useEffect } from 'react';
import { Box, KeyboardAvoidingView } from 'native-base';
import { Platform } from 'react-native';
import Animated, { FadeIn, SlideInRight } from 'react-native-reanimated';

const OnboardingFlow: React.FC = () => {
  const {
    currentStepIndex,
    steps,
    initializeOnboarding,
    goToNextStep,
    goToPreviousStep,
    skipCurrentStep,
    canGoBack,
    canSkipCurrent,
    isTransitioning,
  } = useOnboardingStore();

  const { trackScreenView } = useOnboardingAnalytics();

  useEffect(() => {
    initializeOnboarding();
  }, []);

  useEffect(() => {
    const currentStep = steps[currentStepIndex];
    if (currentStep) {
      trackScreenView(currentStep.id);
    }
  }, [currentStepIndex, steps]);

  const currentStep = steps[currentStepIndex];
  if (!currentStep) return null;

  const renderStepComponent = () => {
    const stepProps = {
      onNext: goToNextStep,
      onBack: canGoBack ? goToPreviousStep : undefined,
      onSkip: canSkipCurrent ? skipCurrentStep : undefined,
      step: currentStep,
      stepIndex: currentStepIndex,
      totalSteps: steps.length,
    };

    switch (currentStep.component) {
      case 'WelcomeIntro':
        return <WelcomeIntro {...stepProps} />;
      case 'HowItWorksStep':
        return <HowItWorksStep {...stepProps} />;
      case 'PrivacySafety':
        return <PrivacySafety {...stepProps} />;
      case 'AgeVerification':
        return <AgeVerification {...stepProps} />;
      case 'Registration':
        return <Registration {...stepProps} />;
      case 'PreferenceSetup':
        return <PreferenceSetup {...stepProps} />;
      case 'SkillGoalSelection':
        return <SkillGoalSelection {...stepProps} />;
      case 'NotificationPermission':
        return <NotificationPermission {...stepProps} />;
      case 'AnalyticsConsent':
        return <AnalyticsConsent {...stepProps} />;
      case 'ReadyToStart':
        return <ReadyToStart {...stepProps} />;
      default:
        return <WelcomeIntro {...stepProps} />;
    }
  };

  return (
    <KeyboardAvoidingView
      flex={1}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <Box flex={1} bg="white" safeArea>
        {/* Step Indicator */}
        <StepIndicator
          currentStep={currentStepIndex + 1}
          totalSteps={steps.length}
          stepTitle={currentStep.title}
        />

        {/* Main Content with Transition Animation */}
        <Animated.View
          key={currentStep.id}
          entering={isTransitioning ? SlideInRight : FadeIn}
          style={{ flex: 1 }}
        >
          {renderStepComponent()}
        </Animated.View>

        {/* Navigation Controls */}
        <NavigationButtons
          onNext={goToNextStep}
          onBack={canGoBack ? goToPreviousStep : undefined}
          onSkip={canSkipCurrent ? skipCurrentStep : undefined}
          isLoading={isTransitioning}
          nextDisabled={currentStep.required && !currentStep.completed}
        />
      </Box>
    </KeyboardAvoidingView>
  );
};

export default OnboardingFlow;
```

---

## Animation Implementation

### Onboarding Animation Hooks

```typescript
// hooks/useOnboardingAnimations.ts
import { useSharedValue, withTiming, withSpring, withSequence } from 'react-native-reanimated';

export const useOnboardingAnimations = () => {
  // Screen transition animations
  const screenOpacity = useSharedValue(1);
  const screenTranslateX = useSharedValue(0);
  
  // Content entrance animations
  const contentOpacity = useSharedValue(0);
  const contentTranslateY = useSharedValue(30);
  const contentScale = useSharedValue(0.95);
  
  // Step indicator animation
  const progressValue = useSharedValue(0);
  
  // Button animations
  const buttonScale = useSharedValue(1);
  const buttonOpacity = useSharedValue(1);

  const animateScreenTransition = (direction: 'forward' | 'backward') => {
    const translateValue = direction === 'forward' ? -100 : 100;
    
    // Fade out current screen
    screenOpacity.value = withTiming(0, { duration: 200 });
    screenTranslateX.value = withTiming(translateValue, { duration: 300 });
    
    // Reset for new screen
    setTimeout(() => {
      screenTranslateX.value = direction === 'forward' ? 100 : -100;
      screenOpacity.value = withTiming(1, { duration: 300 });
      screenTranslateX.value = withTiming(0, { duration: 400 });
    }, 300);
  };

  const animateContentEntrance = () => {
    contentOpacity.value = withTiming(1, {
      duration: 600,
      easing: Easing.out(Easing.cubic),
    });
    
    contentTranslateY.value = withTiming(0, {
      duration: 500,
      easing: Easing.out(Easing.back(1.1)),
    });
    
    contentScale.value = withSpring(1, {
      damping: 12,
      stiffness: 100,
    });
  };

  const animateProgressUpdate = (progress: number) => {
    progressValue.value = withSpring(progress, {
      damping: 15,
      stiffness: 100,
    });
  };

  const animateButtonPress = () => {
    buttonScale.value = withSequence(
      withTiming(0.95, { duration: 100 }),
      withTiming(1, { duration: 150 })
    );
    
    buttonOpacity.value = withSequence(
      withTiming(0.8, { duration: 100 }),
      withTiming(1, { duration: 150 })
    );
  };

  const resetAnimations = () => {
    contentOpacity.value = 0;
    contentTranslateY.value = 30;
    contentScale.value = 0.95;
  };

  return {
    // Animation values
    screenOpacity,
    screenTranslateX,
    contentOpacity,
    contentTranslateY,
    contentScale,
    progressValue,
    buttonScale,
    buttonOpacity,
    
    // Animation functions
    animateScreenTransition,
    animateContentEntrance,
    animateProgressUpdate,
    animateButtonPress,
    resetAnimations,
  };
};
```

### Step Component Implementations

```typescript
// components/WelcomeScreens/WelcomeIntro.tsx
import React, { useEffect } from 'react';
import { VStack, Text, Image } from 'native-base';
import Animated, { 
  useAnimatedStyle,
  FadeIn,
  SlideInUp,
  ZoomIn 
} from 'react-native-reanimated';

interface WelcomeIntroProps {
  onNext: () => Promise<boolean>;
  onSkip?: () => void;
  stepIndex: number;
  totalSteps: number;
}

export const WelcomeIntro: React.FC<WelcomeIntroProps> = ({
  onNext,
  onSkip,
  stepIndex,
  totalSteps,
}) => {
  const { 
    contentOpacity,
    contentTranslateY,
    animateContentEntrance 
  } = useOnboardingAnimations();

  useEffect(() => {
    animateContentEntrance();
  }, []);

  const contentAnimatedStyle = useAnimatedStyle(() => ({
    opacity: contentOpacity.value,
    transform: [{ translateY: contentTranslateY.value }],
  }));

  return (
    <VStack flex={1} p={6} justifyContent="center" alignItems="center" space={6}>
      {/* Logo Animation */}
      <Animated.View entering={ZoomIn.delay(300)}>
        <Image
          source={require('../../assets/logo.png')}
          alt="FlirtCraft Logo"
          size="xl"
          resizeMode="contain"
        />
      </Animated.View>

      {/* Welcome Content */}
      <Animated.View style={contentAnimatedStyle}>
        <VStack space={4} alignItems="center">
          <Animated.View entering={FadeIn.delay(600)}>
            <Text
              fontSize="3xl"
              fontWeight="bold"
              color="primary.900"
              textAlign="center"
              accessibilityRole="header"
              accessibilityLevel={1}
            >
              Welcome to FlirtCraft
            </Text>
          </Animated.View>

          <Animated.View entering={FadeIn.delay(800)}>
            <Text
              fontSize="lg"
              color="gray.600"
              textAlign="center"
              maxW="sm"
            >
              Practice conversations. Build confidence. Find connections.
            </Text>
          </Animated.View>
        </VStack>
      </Animated.View>

      {/* Benefits */}
      <VStack space={3} width="100%">
        {benefits.map((benefit, index) => (
          <Animated.View
            key={benefit.id}
            entering={SlideInUp.delay(1000 + index * 100)}
          >
            <BenefitCard benefit={benefit} />
          </Animated.View>
        ))}
      </VStack>

      {/* Get Started Button */}
      <Animated.View entering={FadeIn.delay(1400)} style={{ width: '100%' }}>
        <Button
          onPress={onNext}
          size="lg"
          colorScheme="primary"
          accessibilityLabel="Get started with FlirtCraft"
          accessibilityHint="Begin the onboarding process"
        >
          Get Started
        </Button>
      </Animated.View>
    </VStack>
  );
};

// Benefit Card Component
const BenefitCard: React.FC<{ benefit: Benefit }> = ({ benefit }) => {
  return (
    <Card>
      <HStack space={3} alignItems="center" p={4}>
        <Box
          w={10}
          h={10}
          borderRadius="full"
          bg="primary.100"
          justifyContent="center"
          alignItems="center"
        >
          <Icon name={benefit.icon} size={20} color="primary.600" />
        </Box>
        <VStack flex={1}>
          <Text fontSize="md" fontWeight="semibold" color="gray.900">
            {benefit.title}
          </Text>
          <Text fontSize="sm" color="gray.600">
            {benefit.description}
          </Text>
        </VStack>
      </HStack>
    </Card>
  );
};
```

---

## Platform Integration

### iOS Specific Implementation

```typescript
// utils/iosIntegration.ts
import { Platform, Linking } from 'react-native';
import { HapticFeedback } from 'react-native-haptic-feedback';

export class iOSOnboardingIntegration {
  // iOS haptic feedback for onboarding interactions
  static triggerHaptic = (type: 'selection' | 'success' | 'warning' | 'error') => {
    if (Platform.OS !== 'ios') return;
    
    const hapticTypes = {
      selection: 'selection',
      success: 'notificationSuccess',
      warning: 'notificationWarning',
      error: 'notificationError',
    };
    
    HapticFeedback.trigger(hapticTypes[type]);
  };

  // iOS notification permission with enhanced UX
  static requestNotificationPermission = async () => {
    if (Platform.OS !== 'ios') return false;
    
    try {
      const { status } = await Notifications.requestPermissionsAsync({
        ios: {
          allowAlert: true,
          allowBadge: true,
          allowSound: true,
          allowDisplayInCarPlay: false,
          allowCriticalAlerts: false,
          provideAppNotificationSettings: true,
        },
      });
      
      if (status === 'granted') {
        this.triggerHaptic('success');
        return true;
      } else if (status === 'denied') {
        // Offer to open settings
        this.showSettingsAlert();
        return false;
      }
      
      return false;
    } catch (error) {
      console.error('iOS notification permission error:', error);
      return false;
    }
  };

  private static showSettingsAlert = () => {
    Alert.alert(
      'Notification Settings',
      'You can enable notifications anytime in Settings > FlirtCraft > Notifications',
      [
        { text: 'Maybe Later', style: 'cancel' },
        { 
          text: 'Open Settings', 
          onPress: () => Linking.openSettings(),
          style: 'default' 
        },
      ]
    );
  };

  // iOS accessibility support
  static announceForAccessibility = (message: string) => {
    if (Platform.OS === 'ios') {
      AccessibilityInfo.announceForAccessibility(message);
    }
  };

  // iOS guided access detection
  static checkGuidedAccess = async (): Promise<boolean> => {
    if (Platform.OS !== 'ios') return false;
    
    try {
      return await AccessibilityInfo.isGuidedAccessEnabled();
    } catch {
      return false;
    }
  };
}
```

### Android Specific Implementation

```typescript
// utils/androidIntegration.ts
import { Platform, PermissionsAndroid, ToastAndroid } from 'react-native';

export class AndroidOnboardingIntegration {
  // Android notification permission (API 33+)
  static requestNotificationPermission = async (): Promise<boolean> => {
    if (Platform.OS !== 'android') return false;
    
    // Check Android version
    if (Platform.Version < 33) {
      // Pre-Android 13 doesn't require notification permission
      return true;
    }
    
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
        {
          title: 'FlirtCraft Notifications',
          message: 'FlirtCraft would like to send you gentle practice reminders and celebrate your progress.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'Allow',
        }
      );
      
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        ToastAndroid.show('Notifications enabled!', ToastAndroid.SHORT);
        return true;
      } else {
        ToastAndroid.show('You can enable notifications in Settings later', ToastAndroid.LONG);
        return false;
      }
    } catch (error) {
      console.error('Android notification permission error:', error);
      return false;
    }
  };

  // Android back button handling during onboarding
  static handleBackButton = (currentStep: number, onBack?: () => void): boolean => {
    if (Platform.OS !== 'android') return false;
    
    if (currentStep === 0) {
      // On first step, show exit confirmation
      Alert.alert(
        'Exit Setup?',
        'You can complete FlirtCraft setup anytime',
        [
          { text: 'Continue Setup', style: 'cancel' },
          { text: 'Exit', style: 'destructive', onPress: () => BackHandler.exitApp() },
        ]
      );
      return true;
    } else if (onBack) {
      // Go to previous step
      onBack();
      return true;
    }
    
    return false;
  };

  // Android accessibility services detection
  static getAccessibilityServices = async (): Promise<string[]> => {
    if (Platform.OS !== 'android') return [];
    
    try {
      // This would require native module implementation
      return await NativeModules.AccessibilityInfo.getEnabledAccessibilityServices();
    } catch {
      return [];
    }
  };

  // Android material design transitions
  static getMaterialTransition = () => ({
    duration: 300,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)', // Material standard easing
  });
}
```

---

## Analytics & Optimization

### Onboarding Analytics Implementation

```typescript
// hooks/useOnboardingAnalytics.ts
export const useOnboardingAnalytics = () => {
  const trackScreenView = (stepId: string) => {
    analytics.track('onboarding_screen_view', {
      stepId,
      timestamp: new Date().toISOString(),
    });
  };

  const trackStepCompletion = (stepId: string, duration: number) => {
    analytics.track('onboarding_step_completed', {
      stepId,
      duration,
      timestamp: new Date().toISOString(),
    });
  };

  const trackStepSkipped = (stepId: string, reason?: string) => {
    analytics.track('onboarding_step_skipped', {
      stepId,
      reason: reason || 'user_choice',
      timestamp: new Date().toISOString(),
    });
  };

  const trackPermissionRequest = (
    permissionType: string, 
    granted: boolean, 
    method: 'dialog' | 'settings'
  ) => {
    analytics.track('onboarding_permission_request', {
      permissionType,
      granted,
      method,
      timestamp: new Date().toISOString(),
    });
  };

  const trackOnboardingCompletion = (
    duration: number,
    completedSteps: number,
    skippedSteps: number,
    userChoices: any
  ) => {
    analytics.track('onboarding_completed', {
      duration,
      completedSteps,
      skippedSteps,
      completionRate: completedSteps / (completedSteps + skippedSteps),
      userChoices,
      timestamp: new Date().toISOString(),
    });
  };

  const trackOnboardingAbandonment = (
    stepId: string,
    stepIndex: number,
    timeSpent: number
  ) => {
    analytics.track('onboarding_abandoned', {
      lastStepId: stepId,
      lastStepIndex: stepIndex,
      timeSpent,
      timestamp: new Date().toISOString(),
    });
  };

  return {
    trackScreenView,
    trackStepCompletion,
    trackStepSkipped,
    trackPermissionRequest,
    trackOnboardingCompletion,
    trackOnboardingAbandonment,
  };
};
```

### A/B Testing Integration

```typescript
// utils/onboardingExperiments.ts
export class OnboardingExperiments {
  static async getOnboardingVariant(): Promise<'control' | 'shortened' | 'detailed'> {
    try {
      const variant = await experiments.getVariant('onboarding_flow_v1');
      return variant || 'control';
    } catch {
      return 'control';
    }
  }

  static async getWelcomeMessageVariant(): Promise<'standard' | 'benefit_focused' | 'social_proof'> {
    try {
      const variant = await experiments.getVariant('welcome_message_v1');
      return variant || 'standard';
    } catch {
      return 'standard';
    }
  }

  static async getPermissionRequestVariant(): Promise<'standard' | 'benefit_heavy' | 'minimal'> {
    try {
      const variant = await experiments.getVariant('permission_request_v1');
      return variant || 'standard';
    } catch {
      return 'standard';
    }
  }

  static trackExperimentExposure(experimentName: string, variant: string) {
    analytics.track('experiment_exposure', {
      experimentName,
      variant,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### Performance Monitoring

```typescript
// utils/onboardingPerformance.ts
export class OnboardingPerformanceMonitor {
  private static stepTimestamps: Map<string, number> = new Map();
  private static animationFrameDrops: number = 0;

  static startStepTimer(stepId: string) {
    this.stepTimestamps.set(stepId, performance.now());
  }

  static endStepTimer(stepId: string): number {
    const startTime = this.stepTimestamps.get(stepId);
    if (!startTime) return 0;
    
    const duration = performance.now() - startTime;
    this.stepTimestamps.delete(stepId);
    
    // Track if step took too long
    if (duration > 30000) { // 30 seconds
      analytics.track('onboarding_step_slow', {
        stepId,
        duration,
      });
    }
    
    return duration;
  }

  static monitorAnimationPerformance() {
    let lastFrameTime = performance.now();
    
    const checkFrame = () => {
      const currentTime = performance.now();
      const deltaTime = currentTime - lastFrameTime;
      
      if (deltaTime > 16.67) { // Dropped frame (60fps = 16.67ms)
        this.animationFrameDrops++;
      }
      
      lastFrameTime = currentTime;
      requestAnimationFrame(checkFrame);
    };
    
    requestAnimationFrame(checkFrame);
  }

  static getPerformanceMetrics() {
    return {
      frameDrops: this.animationFrameDrops,
      activeTimers: this.stepTimestamps.size,
    };
  }
}
```

## Testing Strategy

### Unit Tests

```typescript
// __tests__/onboardingStore.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useOnboardingStore } from '../stores/onboardingStore';

describe('OnboardingStore', () => {
  beforeEach(() => {
    useOnboardingStore.getState().resetOnboarding();
  });

  it('should initialize onboarding correctly', () => {
    const { result } = renderHook(() => useOnboardingStore());
    
    act(() => {
      result.current.initializeOnboarding();
    });

    expect(result.current.currentStepIndex).toBe(0);
    expect(result.current.startTime).toBeTruthy();
    expect(result.current.isComplete).toBe(false);
  });

  it('should advance to next step when conditions are met', async () => {
    const { result } = renderHook(() => useOnboardingStore());
    
    act(() => {
      result.current.initializeOnboarding();
    });

    const success = await act(async () => {
      return await result.current.goToNextStep();
    });

    expect(success).toBe(true);
    expect(result.current.currentStepIndex).toBe(1);
  });

  it('should handle step skipping correctly', () => {
    const { result } = renderHook(() => useOnboardingStore());
    
    act(() => {
      result.current.initializeOnboarding();
      result.current.jumpToStep(1); // Go to skippable step
      result.current.skipCurrentStep();
    });

    expect(result.current.skippedSteps).toContain(result.current.steps[1].id);
  });
});
```

### Integration Tests

```typescript
// __tests__/OnboardingFlow.integration.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { OnboardingFlow } from '../components/OnboardingFlow';

describe('Onboarding Flow Integration', () => {
  it('should complete full onboarding flow', async () => {
    const { getByText, getByLabelText } = render(<OnboardingFlow />);

    // Welcome screen
    expect(getByText('Welcome to FlirtCraft')).toBeTruthy();
    fireEvent.press(getByText('Get Started'));

    // How it works screens
    await waitFor(() => {
      expect(getByText('Choose Your Practice Scenario')).toBeTruthy();
    });
    
    fireEvent.press(getByText('Next'));

    // Continue through remaining steps...
    
    // Completion
    await waitFor(() => {
      expect(getByText('Ready to Start')).toBeTruthy();
    });
  });

  it('should handle permission requests correctly', async () => {
    const { getByText, getByLabelText } = render(<OnboardingFlow />);

    // Navigate to permission screen
    // ... navigation code

    fireEvent.press(getByText('Allow Notifications'));

    await waitFor(() => {
      expect(mockPermissionRequest).toHaveBeenCalled();
    });
  });
});
```

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete user flow context
- **[Screen States](./screen-states.md)** - Visual specifications for implementation
- **[Interactions](./interactions.md)** - Animation and interaction details
- **[Accessibility](./accessibility.md)** - Inclusive design requirements
- **[Design System Components](../../design-system/components/)** - Reusable component specifications
- **[Premium Monetization](../premium-monetization/README.md)** - Subscription and trial integration

## Premium Integration

### Premium Trial Offer During Onboarding

The onboarding flow includes an optional premium benefits screen after the "How It Works" steps to maximize trial conversion:

```typescript
// stores/onboardingStore.ts - Premium additions
interface OnboardingState {
  // ... existing state
  userChoices: {
    ageVerified: boolean;
    notificationsEnabled: boolean | null;
    analyticsOptIn: boolean | null;
    privacyLevel: 'standard' | 'enhanced';
    trialOffered: boolean;  // Track if trial was offered
    trialAccepted: boolean | null;  // Track trial decision
  };
}

// Add premium trial step after "How It Works" steps
const defaultSteps: OnboardingStep[] = [
  // ... existing steps through howItWorks3
  { id: 'premiumBenefits', title: 'Unlock Full Experience', component: 'PremiumBenefits', required: false, completed: false, skippable: true },
  // ... remaining steps
];
```

### RevenueCat Integration

```typescript
// Initialize RevenueCat during onboarding
import Purchases from 'react-native-purchases';

const initializePurchases = async () => {
  if (Platform.OS === 'ios') {
    await Purchases.configure({ apiKey: IOS_REVENUECAT_KEY });
  } else {
    await Purchases.configure({ apiKey: ANDROID_REVENUECAT_KEY });
  }
};
```

## Post-Onboarding Navigation

### Overview
After onboarding completion, users are directed to the main app's Home Dashboard where they can immediately start their first practice session.

### Placeholder Tab Navigation Component

```typescript
// components/MainAppPlaceholder.tsx
import React, { useState } from 'react';
import { Alert } from 'react-native';
import { 
  Box, 
  VStack, 
  HStack, 
  Text, 
  Button, 
  ButtonText,
  Pressable,
  Center,
  Divider
} from 'native-base';
import { Home, MessageCircle, Grid, User } from 'lucide-react-native';
import { supabase } from '@/lib/supabase';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useOnboardingStore } from '@/stores/onboardingStore';

export const MainAppPlaceholder: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'home' | 'chat' | 'scenarios' | 'profile'>('home');
  const resetOnboarding = useOnboardingStore((state) => state.resetOnboarding);

  const handleResetApp = async () => {
    Alert.alert(
      'Reset App',
      'This will sign you out and clear all data. You can test registration again.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            try {
              // Sign out from Supabase
              await supabase.auth.signOut();
              
              // Clear all local storage
              await AsyncStorage.clear();
              
              // Reset onboarding state
              resetOnboarding();
              
              // Navigate back to onboarding
              // Note: In production, use your navigation method
              // navigation.reset({
              //   index: 0,
              //   routes: [{ name: 'Onboarding' }],
              // });
            } catch (error) {
              console.error('Failed to reset app:', error);
              Alert.alert('Error', 'Failed to reset app. Please try again.');
            }
          },
        },
      ]
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'home':
        return (
          <Center flex={1} p={6}>
            <Text fontSize="2xl" fontWeight="bold" color="$primary500" mb={4}>
              Welcome to FlirtCraft! 🎉
            </Text>
            <VStack space={3} alignItems="center">
              <Text fontSize="lg" textAlign="center" color="$neutral600">
                Main features are in development
              </Text>
              <Text fontSize="md" textAlign="center" color="$neutral500">
                Use the tabs below to explore placeholder screens
              </Text>
              <Box mt={4} p={4} bg="$neutral100" borderRadius="$lg">
                <Text fontSize="sm" color="$neutral700">
                  This is a development build for testing the registration flow
                </Text>
              </Box>
            </VStack>
          </Center>
        );

      case 'chat':
        return (
          <Center flex={1} p={6}>
            <MessageCircle size={48} color="#F97316" />
            <Text fontSize="xl" fontWeight="bold" mt={4}>
              Chat Feature
            </Text>
            <Text fontSize="md" color="$neutral600" mt={2} textAlign="center">
              Custom conversation practice will be available here
            </Text>
            <Box mt={4} p={3} bg="$warning100" borderRadius="$md">
              <Text fontSize="sm" color="$warning800">
                Feature in development
              </Text>
            </Box>
          </Center>
        );

      case 'scenarios':
        return (
          <Center flex={1} p={6}>
            <Grid size={48} color="#F97316" />
            <Text fontSize="xl" fontWeight="bold" mt={4}>
              Scenarios Feature
            </Text>
            <Text fontSize="md" color="$neutral600" mt={2} textAlign="center">
              Predefined practice scenarios will be available here
            </Text>
            <Box mt={4} p={3} bg="$info100" borderRadius="$md">
              <Text fontSize="sm" color="$info800">
                Feature in development
              </Text>
            </Box>
          </Center>
        );

      case 'profile':
        return (
          <VStack flex={1} p={6}>
            <Text fontSize="2xl" fontWeight="bold" mb={6}>
              Profile
            </Text>
            
            <VStack space={4}>
              <Box p={4} bg="$neutral100" borderRadius="$lg">
                <Text fontSize="md" fontWeight="semibold" mb={2}>
                  User Information
                </Text>
                <Text fontSize="sm" color="$neutral600">
                  Profile features coming soon...
                </Text>
              </Box>

              <Divider my={4} />

              <Box p={4} bg="$error50" borderRadius="$lg" borderWidth={1} borderColor="$error200">
                <Text fontSize="md" fontWeight="semibold" color="$error800" mb={2}>
                  Development Tools
                </Text>
                <Text fontSize="sm" color="$error700" mb={4}>
                  Use this to test the registration flow again
                </Text>
                <Button
                  action="negative"
                  variant="solid"
                  size="lg"
                  onPress={handleResetApp}
                >
                  <ButtonText>Reset App & Clear Data</ButtonText>
                </Button>
              </Box>

              <Box p={3} bg="$neutral50" borderRadius="$md" mt={4}>
                <Text fontSize="xs" color="$neutral500">
                  Note: This reset function is only available in development builds
                </Text>
              </Box>
            </VStack>
          </VStack>
        );

      default:
        return null;
    }
  };

  return (
    <Box flex={1} bg="$white">
      {/* Main Content */}
      <Box flex={1}>
        {renderTabContent()}
      </Box>

      {/* Bottom Tab Bar */}
      <HStack
        bg="$white"
        borderTopWidth={1}
        borderTopColor="$neutral200"
        paddingVertical={2}
        paddingHorizontal={4}
        justifyContent="space-around"
        alignItems="center"
        safeAreaBottom
      >
        <Pressable
          onPress={() => setActiveTab('home')}
          flex={1}
          alignItems="center"
          py={2}
        >
          <Home
            size={24}
            color={activeTab === 'home' ? '#F97316' : '#9CA3AF'}
          />
          <Text
            fontSize="xs"
            mt={1}
            color={activeTab === 'home' ? '$primary500' : '$neutral400'}
          >
            Home
          </Text>
        </Pressable>

        <Pressable
          onPress={() => setActiveTab('chat')}
          flex={1}
          alignItems="center"
          py={2}
        >
          <MessageCircle
            size={24}
            color={activeTab === 'chat' ? '#F97316' : '#9CA3AF'}
          />
          <Text
            fontSize="xs"
            mt={1}
            color={activeTab === 'chat' ? '$primary500' : '$neutral400'}
          >
            Chat
          </Text>
        </Pressable>

        <Pressable
          onPress={() => setActiveTab('scenarios')}
          flex={1}
          alignItems="center"
          py={2}
        >
          <Grid
            size={24}
            color={activeTab === 'scenarios' ? '#F97316' : '#9CA3AF'}
          />
          <Text
            fontSize="xs"
            mt={1}
            color={activeTab === 'scenarios' ? '$primary500' : '$neutral400'}
          >
            Scenarios
          </Text>
        </Pressable>

        <Pressable
          onPress={() => setActiveTab('profile')}
          flex={1}
          alignItems="center"
          py={2}
        >
          <User
            size={24}
            color={activeTab === 'profile' ? '#F97316' : '#9CA3AF'}
          />
          <Text
            fontSize="xs"
            mt={1}
            color={activeTab === 'profile' ? '$primary500' : '$neutral400'}
          >
            Profile
          </Text>
        </Pressable>
      </HStack>
    </Box>
  );
};
```

### Navigation Helper Function

```typescript
// utils/navigation.ts
export const navigateToMainApp = async (navigation: any) => {
  // In development, navigate to placeholder
  if (__DEV__) {
    navigation.reset({
      index: 0,
      routes: [{ name: 'MainAppPlaceholder' }],
    });
  } else {
    // In production, navigate to actual main app
    navigation.reset({
      index: 0,
      routes: [{ name: 'MainApp' }],
    });
  }
};
```

### Testing Workflow

1. **Complete Registration**: User goes through full onboarding including email/password
2. **Land on Placeholder**: After completion, see the 4-tab placeholder interface
3. **Explore Tabs**: Each tab shows "in development" message
4. **Reset for Testing**: Go to Profile tab → tap "Reset App & Clear Data"
5. **Start Fresh**: App returns to onboarding, all data cleared
6. **Repeat Testing**: Can test registration flow multiple times

### Important Notes

- This placeholder is **temporary** and only for development/testing
- The reset function clears both Supabase auth and local storage
- In production, replace with actual feature implementations
- Tab structure matches the planned 4-tab navigation design
- Uses FlirtCraft color scheme (Primary Orange #F97316)

## Implementation Checklist

### Core Functionality
- [ ] Multi-step onboarding flow with state management
- [ ] Smooth screen transitions and animations
- [ ] Platform-specific permission requests
- [ ] Trust building and privacy assurance screens
- [ ] Age verification and compliance handling
- [ ] **Email/password registration with Supabase Auth**
- [ ] **Real-time email validation and availability checking**
- [ ] **Password strength indicator with visual feedback**
- [ ] **Temporary local storage until onboarding completion**
- [ ] **Delayed account creation pattern implementation**
- [ ] Premium trial offer integration
- [ ] RevenueCat SDK setup and initialization
- [ ] Completion celebration and app transition

### User Experience
- [ ] Engaging animations and micro-interactions
- [ ] Clear progress indication and navigation
- [ ] Skip options for non-essential steps
- [ ] **Registration form with intuitive UX and validation**
- [ ] **Sign in/sign up toggle with smooth transitions**
- [ ] **Helpful error messages and recovery guidance**
- [ ] Accessibility compliance (WCAG 2.1 AA)
- [ ] Responsive design (mobile → tablet)
- [ ] Error handling and recovery paths

### Platform Integration
- [ ] iOS notification permissions with settings fallback
- [ ] Android 13+ notification permission handling
- [ ] iOS haptic feedback integration
- [ ] Android back button handling
- [ ] **Supabase Auth SDK integration across platforms**
- [ ] **Cross-platform password manager compatibility**
- [ ] Platform-specific accessibility features
- [ ] Native performance optimization

### Analytics & Optimization
- [ ] Comprehensive analytics tracking
- [ ] A/B testing integration
- [ ] Performance monitoring
- [ ] Funnel analysis and drop-off tracking
- [ ] **Registration conversion rate tracking**
- [ ] **Email validation success/failure metrics**
- [ ] **Password strength distribution analysis**
- [ ] User behavior insights collection

## Last Updated
- **Version 1.0.0**: Complete implementation specification with platform integration
- **Focus**: Trust-building first impressions with seamless user experience
- **Next**: Development team implementation with A/B testing setup