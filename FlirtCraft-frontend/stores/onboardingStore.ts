import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { supabase } from '@/lib/supabase';
import {
  OnboardingStep,
  OnboardingFormData,
  OnboardingPersona,
  RegistrationFormData,
  PreferenceFormData,
  SkillGoalFormData
} from '@/features/onboarding/types';

interface OnboardingState {
  // Flow state
  currentStepIndex: number;
  totalSteps: number;
  steps: OnboardingStep[];
  isComplete: boolean;

  // User progress
  completedSteps: string[];
  skippedSteps: string[];
  startTime: Date | null;
  completionTime: Date | null;

  // Form data
  formData: OnboardingFormData;

  // Preferences and choices
  userChoices: {
    ageVerified: boolean;
    notificationsEnabled: boolean | null;
    analyticsOptIn: boolean | null;
    privacyLevel: 'standard' | 'enhanced';
    persona: OnboardingPersona;
    trialOffered: boolean;
    trialAccepted: boolean | null;
  };

  // Auth state
  authState: {
    user: any | null;
    session: any | null;
    emailVerificationSent: boolean;
    emailVerificationRequired: boolean;
    registrationComplete: boolean;
    authError: string | null;
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
  updateFormData: (section: keyof OnboardingFormData, data: any) => void;
  completeOnboarding: () => Promise<void>;
  resetOnboarding: () => void;
}

const defaultSteps: OnboardingStep[] = [
  {
    id: 'welcome',
    title: 'Welcome',
    component: 'WelcomeIntro',
    required: true,
    completed: false,
    skippable: false,
    estimatedDuration: 30
  },
  {
    id: 'ageVerification',
    title: 'Age Verification',
    component: 'AgeVerification',
    required: true,
    completed: false,
    skippable: false,
    estimatedDuration: 15
  },
  {
    id: 'registration',
    title: 'Create Account',
    component: 'Registration',
    required: true,
    completed: false,
    skippable: false,
    estimatedDuration: 45
  },
  {
    id: 'preferences',
    title: 'Preferences',
    component: 'PreferenceSetup',
    required: true,
    completed: false,
    skippable: false,
    estimatedDuration: 60
  },
  {
    id: 'skillGoals',
    title: 'Goals',
    component: 'SkillGoalSelection',
    required: true,
    completed: false,
    skippable: false,
    estimatedDuration: 45
  },
];

export const useOnboardingStore = create<OnboardingState>()(
  persist(
    (set, get) => ({
      // Initial state
      currentStepIndex: 0,
      totalSteps: defaultSteps.length,
      steps: defaultSteps,
      isComplete: false,
      completedSteps: [],
      skippedSteps: [],
      startTime: null,
      completionTime: null,

      formData: {
        registration: {},
        preferences: {},
        skillGoals: {},
        ageVerification: {
          birthDate: null,
          isVerified: false,
        },
      },

      userChoices: {
        ageVerified: false,
        notificationsEnabled: null,
        analyticsOptIn: null,
        privacyLevel: 'standard',
        persona: null,
        trialOffered: false,
        trialAccepted: null,
      },

      authState: {
        user: null,
        session: null,
        emailVerificationSent: false,
        emailVerificationRequired: false,
        registrationComplete: false,
        authError: null,
      },

      canGoBack: false,
      canSkipCurrent: false,
      isTransitioning: false,

      // Actions
      initializeOnboarding: () => {
        const steps = get().steps;
        set({
          currentStepIndex: 0,
          startTime: new Date(),
          isComplete: false,
          canGoBack: false,
          canSkipCurrent: steps[0]?.skippable || false,
        });
      },

      goToNextStep: async () => {
        const currentIndex = get().currentStepIndex;
        const steps = get().steps;
        const currentStep = steps[currentIndex];

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

        set({
          currentStepIndex: nextIndex,
          canGoBack: nextIndex > 0,
          canSkipCurrent: steps[nextIndex]?.skippable || false,
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
          handleStepData(stepId, data, get(), set);
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

      updateFormData: (section, data) => {
        set(state => ({
          formData: {
            ...state.formData,
            [section]: {
              ...state.formData[section],
              ...data,
            },
          },
        }));
      },

      completeOnboarding: async () => {
        const completionTime = new Date();
        const startTime = get().startTime;
        const { formData, userChoices } = get();

        try {
          // Calculate onboarding duration
          const durationSeconds = startTime ? Math.round((completionTime.getTime() - startTime.getTime()) / 1000) : null;

          // Create Supabase Auth account
          const authResult = await createSupabaseAccount(formData, userChoices, durationSeconds);

          if (authResult.success) {
            set({
              isComplete: true,
              completionTime,
              authState: {
                ...get().authState,
                user: authResult.user,
                session: authResult.session,
                registrationComplete: true,
                emailVerificationRequired: authResult.emailVerificationRequired || false,
              },
            });
          } else {
            throw new Error(authResult.error);
          }
        } catch (error) {
          console.error('Failed to complete onboarding:', error);
          set(state => ({
            authState: {
              ...state.authState,
              authError: error instanceof Error ? error.message : 'Unknown error',
            },
          }));
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
          formData: {
            registration: {},
            preferences: {},
            skillGoals: {},
            ageVerification: {
              birthDate: null,
              isVerified: false,
            },
          },
          userChoices: {
            ageVerified: false,
            notificationsEnabled: null,
            analyticsOptIn: null,
            privacyLevel: 'standard',
            persona: null,
            trialOffered: false,
            trialAccepted: null,
          },
          authState: {
            user: null,
            session: null,
            emailVerificationSent: false,
            emailVerificationRequired: false,
            registrationComplete: false,
            authError: null,
          },
        });
      },
    }),
    {
      name: 'flirtcraft-onboarding',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        isComplete: state.isComplete,
        completedSteps: state.completedSteps,
        userChoices: state.userChoices,
        completionTime: state.completionTime,
        formData: state.formData,
      }),
    }
  )
);

// Helper functions
const validateCurrentStep = async (stepId: string, state: OnboardingState): Promise<boolean> => {
  switch (stepId) {
    case 'ageVerification':
      return state.userChoices.ageVerified;
    case 'registration':
      const regData = state.formData.registration;
      return !!(regData.email && regData.password && regData.agreedToTerms);
    case 'preferences':
      const prefData = state.formData.preferences;
      return !!(prefData.genderPreference && prefData.ageRangeMin && prefData.ageRangeMax);
    case 'skillGoals':
      const skillData = state.formData.skillGoals;
      return !!(skillData.primaryGoals && skillData.primaryGoals.length > 0);
    default:
      return true;
  }
};

const handleStepData = (
  stepId: string,
  data: any,
  state: OnboardingState,
  set: (fn: (state: OnboardingState) => Partial<OnboardingState>) => void
) => {
  switch (stepId) {
    case 'ageVerification':
      set(state => ({
        userChoices: {
          ...state.userChoices,
          ageVerified: data.isVerified,
        },
        formData: {
          ...state.formData,
          ageVerification: data,
        },
      }));
      break;
    case 'registration':
      set(state => ({
        formData: {
          ...state.formData,
          registration: data,
        },
      }));
      break;
    case 'preferences':
      set(state => ({
        formData: {
          ...state.formData,
          preferences: data,
        },
      }));
      break;
    case 'skillGoals':
      set(state => ({
        formData: {
          ...state.formData,
          skillGoals: data,
        },
      }));
      break;
  }
};

const createSupabaseAccount = async (
  formData: OnboardingFormData,
  userChoices: OnboardingState['userChoices'],
  durationSeconds?: number | null
): Promise<{ success: boolean; user?: any; session?: any; emailVerificationRequired?: boolean; error?: string }> => {
  try {
    const registrationData = formData.registration;
    const preferencesData = formData.preferences;
    const skillGoalsData = formData.skillGoals;
    const ageVerificationData = formData.ageVerification;

    if (!registrationData.email || !registrationData.password) {
      return { success: false, error: 'Email and password are required' };
    }

    // Create Supabase Auth account
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email: registrationData.email,
      password: registrationData.password,
      options: {
        data: {
          // Additional metadata
          onboarding_persona: userChoices.persona,
          privacy_level: userChoices.privacyLevel,
          marketing_opt_in: registrationData.marketingOptIn,
        }
      }
    });

    if (authError) {
      return { success: false, error: authError.message };
    }

    const user = authData.user;
    if (!user) {
      return { success: false, error: 'User creation failed' };
    }

    // Create User record in database
    const { error: userError } = await supabase
      .from('users')
      .insert({
        id: user.id,
        email: user.email,
        email_verified: !!user.email_confirmed_at,
        onboarding_completed: true,
        onboarding_completed_at: new Date().toISOString(),
        is_active: true,
        is_premium: false,
      });

    if (userError) {
      console.error('Error creating user record:', userError);
      // Try to delete the auth user if user record creation failed
      try {
        await supabase.auth.signOut();
      } catch (cleanupError) {
        console.error('Failed to cleanup auth user:', cleanupError);
      }
      return { success: false, error: 'Failed to create user profile' };
    }

    // Create UserProfile record with onboarding data
    const { error: profileError } = await supabase
      .from('user_profiles')
      .insert({
        user_id: user.id,
        age_verified: userChoices.ageVerified,
        birth_year: ageVerificationData.birthDate ? new Date(ageVerificationData.birthDate).getFullYear() : null,
        target_gender: preferencesData.genderPreference === 'randomized' ? 'everyone' : preferencesData.genderPreference,
        target_age_min: preferencesData.ageRangeMin,
        target_age_max: preferencesData.ageRangeMax,
        relationship_goal: preferencesData.relationshipGoal,
        primary_skills: skillGoalsData.primaryGoals || [],
        specific_challenges: skillGoalsData.specificChallenges || [],
        experience_level: skillGoalsData.experienceLevel,
        practice_frequency: skillGoalsData.practiceFrequency,
        notifications_enabled: userChoices.notificationsEnabled,
        analytics_opt_in: userChoices.analyticsOptIn || false,
        privacy_level: userChoices.privacyLevel,
        marketing_opt_in: registrationData.marketingOptIn || false,
        detected_persona: userChoices.persona,
        onboarding_version: '1.0',
        onboarding_duration_seconds: durationSeconds,
        onboarding_steps_completed: ['welcome', 'ageVerification', 'registration', 'preferences', 'skillGoals'],
        onboarding_steps_skipped: [],
      });

    if (profileError) {
      console.error('Error creating user profile:', profileError);
      // Cleanup: Delete user record and auth user
      try {
        await supabase.from('users').delete().eq('id', user.id);
        await supabase.auth.signOut();
      } catch (cleanupError) {
        console.error('Failed to cleanup after profile error:', cleanupError);
      }
      return { success: false, error: 'Failed to create user profile' };
    }

    // Create UserProgress record
    const { error: progressError } = await supabase
      .from('user_progress')
      .insert({
        user_id: user.id,
        total_conversations: 0,
        total_practice_time_minutes: 0,
        successful_conversations: 0,
        current_streak: 0,
        longest_streak: 0,
        xp_points: 0,
        level: 1,
        achievements_unlocked: [],
        weekly_conversations: 0,
        monthly_conversations: 0,
        weekly_reset_date: new Date().toISOString(),
        monthly_reset_date: new Date().toISOString(),
      });

    if (progressError) {
      console.error('Error creating user progress:', progressError);
      // Cleanup: Delete profile, user record and auth user
      try {
        await supabase.from('user_profiles').delete().eq('user_id', user.id);
        await supabase.from('users').delete().eq('id', user.id);
        await supabase.auth.signOut();
      } catch (cleanupError) {
        console.error('Failed to cleanup after progress error:', cleanupError);
      }
      return { success: false, error: 'Failed to create user progress' };
    }

    return {
      success: true,
      user: authData.user,
      session: authData.session,
      emailVerificationRequired: !user.email_confirmed_at
    };

  } catch (error) {
    console.error('Supabase account creation error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred'
    };
  }
};