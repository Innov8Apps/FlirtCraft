import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authService, rateLimitService } from '../services/supabase';
import { rateLimitService as emailRateLimitService } from '../lib/services/rateLimitService';

// 5-step onboarding flow for NEW users (sign-in is separate)
export type OnboardingStepId = 
  | 'welcome'              // Welcome & Value Proposition
  | 'age_verification'     // Age Verification  
  | 'registration'         // Registration (create account)
  | 'preferences'          // Preference Setup
  | 'skill_goals';         // Skill Goal Selection

export interface OnboardingFormData {
  // Age verification
  birthDate?: Date;
  ageVerified: boolean;

  // Registration
  email: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: boolean;
  agreedToPrivacy: boolean;
  
  // Preferences
  userGender?: 'male' | 'female' | 'non-binary' | 'prefer-not-to-say';
  targetGender?: 'male' | 'female' | 'everyone';
  targetAgeMin?: number;
  targetAgeMax?: number;
  
  // Skill goals
  primarySkillGoals: string[];
}

export interface OnboardingProgress {
  currentStep: number;
  currentStepId: OnboardingStepId;
  totalSteps: number;
  completedSteps: number;
  isCompleted: boolean;
  startedAt?: Date;
  lastNavigationDirection?: 'forward' | 'backward';
}

export interface OnboardingState {
  // Data
  formData: Partial<OnboardingFormData>;
  progress: OnboardingProgress;

  // UI state
  isLoading: boolean;
  error: string | null;

  // Actions
  updateFormData: (data: Partial<OnboardingFormData>) => void;
  setCurrentStep: (step: number) => void;
  setCurrentStepById: (stepId: OnboardingStepId) => void;
  nextStep: () => void;
  previousStep: () => void;
  completeStep: (step: number) => void;
  completeOnboarding: () => void;
  resetOnboarding: () => void;
  startOnboarding: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  finalizeAccountCreation: () => Promise<{ success: boolean; error?: string; shouldReturnToRegistration?: boolean }>;
}

const TOTAL_STEPS = 5; // 5-Screen Flow for NEW users

const STEP_SEQUENCE: OnboardingStepId[] = [
  'welcome',
  'age_verification', 
  'registration',
  'preferences',
  'skill_goals'
];

const initialProgress: OnboardingProgress = {
  currentStep: 1,
  currentStepId: 'welcome',
  totalSteps: TOTAL_STEPS,
  completedSteps: 0,
  isCompleted: false,
  startedAt: undefined,
};

const initialFormData: Partial<OnboardingFormData> = {
  // Age verification
  birthDate: undefined,
  ageVerified: false,

  // Registration
  email: '',
  password: '',
  confirmPassword: '',
  agreedToTerms: false,
  agreedToPrivacy: false,
  
  // Preferences
  userGender: undefined,
  targetGender: undefined,
  targetAgeMin: undefined,
  targetAgeMax: undefined,
  
  // Skill goals
  primarySkillGoals: [],
};

export const useOnboardingStore = create<OnboardingState>()(
  (set, get) => ({
      // Initial state
      formData: initialFormData,
      progress: initialProgress,
      isLoading: false,
      error: null,

      // Actions
      updateFormData: (data: Partial<OnboardingFormData>) => {
        set((state) => ({
          formData: {
            ...state.formData,
            ...data,
          },
        }));
      },

      setCurrentStep: (step: number) => {
        if (step < 1 || step > TOTAL_STEPS) return;
        
        const stepId = STEP_SEQUENCE[step - 1]; // Convert 1-based to 0-based for array index
        
        set((state) => ({
          progress: {
            ...state.progress,
            currentStep: step,
            currentStepId: stepId,
          },
        }));
      },

      setCurrentStepById: (stepId: OnboardingStepId) => {
        const stepIndex = STEP_SEQUENCE.indexOf(stepId);
        if (stepIndex === -1) return;
        
        const currentStep = stepIndex + 1; // Convert 0-based index to 1-based step
        
        set((state) => {
          // Only update if we're actually changing steps
          if (state.progress.currentStepId === stepId) {
            return state;
          }
          
          // When navigating to a step, ensure completedSteps reflects the steps that should be completed
          // If we're going to step N, then step N-1 should be completed
          const minCompletedSteps = Math.max(0, currentStep - 1);
          const completedSteps = Math.max(state.progress.completedSteps, minCompletedSteps);
          
          return {
            progress: {
              ...state.progress,
              currentStep,
              currentStepId: stepId,
              completedSteps,
            },
          };
        });
      },

      nextStep: () => {
        const { progress } = get();
        // Complete the current step before moving to next
        const completedSteps = Math.max(progress.completedSteps, progress.currentStep);
        const nextStep = Math.min(progress.currentStep + 1, TOTAL_STEPS);
        const stepId = STEP_SEQUENCE[nextStep - 1]; // Convert 1-based to 0-based for array index

        set((state) => ({
          progress: {
            ...state.progress,
            currentStep: nextStep,
            currentStepId: stepId,
            completedSteps: completedSteps,
            lastNavigationDirection: 'forward',
          },
        }));
      },

      previousStep: () => {
        const { progress } = get();
        const prevStep = Math.max(progress.currentStep - 1, 1);
        const stepId = STEP_SEQUENCE[prevStep - 1]; // Convert 1-based to 0-based for array index

        set((state) => {
          // When going back to step N, completed steps should be N-1
          // This ensures the progress bar shows the correct percentage
          const completedSteps = Math.max(0, prevStep - 1);

          return {
            progress: {
              ...state.progress,
              currentStep: prevStep,
              currentStepId: stepId,
              completedSteps,
              lastNavigationDirection: 'backward',
            },
          };
        });
      },

      completeStep: (step: number) => {
        set((state) => {
          const newCompletedSteps = Math.max(state.progress.completedSteps, step);
          
          return {
            progress: {
              ...state.progress,
              completedSteps: newCompletedSteps,
            },
          };
        });
      },

      completeOnboarding: () => {
        set((state) => ({
          progress: {
            ...state.progress,
            isCompleted: true,
            completedSteps: TOTAL_STEPS,
          },
        }));
      },

      resetOnboarding: () => {
        set({
          formData: initialFormData,
          progress: initialProgress,
          isLoading: false,
          error: null,
        });
      },

      startOnboarding: () => {
        set((state) => ({
          progress: {
            ...state.progress,
            startedAt: new Date(),
          },
        }));
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      setError: (error: string | null) => {
        set({ error });
      },

      finalizeAccountCreation: async (): Promise<{ success: boolean; error?: string; shouldReturnToRegistration?: boolean }> => {
        const { formData } = get();

        try {
          // Validate required fields
          if (!formData.email || !formData.password) {
            return {
              success: false,
              error: 'Email and password are required',
              shouldReturnToRegistration: true,
            };
          }

          // Check rate limiting
          const rateLimitCheck = await rateLimitService.checkRateLimit('signup');
          if (!rateLimitCheck.allowed) {
            return {
              success: false,
              error: rateLimitCheck.message || 'Too many attempts. Please try again later.',
              shouldReturnToRegistration: false,
            };
          }

          // Final email availability check
          const emailCheck = await authService.checkEmailExists(formData.email);
          if (emailCheck.error) {
            return {
              success: false,
              error: 'Unable to verify email availability. Please try again.',
              shouldReturnToRegistration: true,
            };
          }

          if (emailCheck.exists) {
            // Track failed attempt
            await emailRateLimitService.trackFailedAttempt();
            return {
              success: false,
              error: 'This email is already registered. Please try logging in instead.',
              shouldReturnToRegistration: true,
            };
          }

          // Track signup attempt
          await rateLimitService.trackAttempt('signup');

          // Create account with complete onboarding data
          const result = await authService.signUpWithProfile(
            formData.email,
            formData.password!,
            formData as OnboardingFormData
          );

          if (!result.success) {
            if (result.errorType === 'rate_limit' && result.retryAfter) {
              await rateLimitService.setRateLimitBlock(result.retryAfter, 'signup');
              return {
                success: false,
                error: 'Too many signup attempts. Please try again later.',
                shouldReturnToRegistration: false,
              };
            }

            return {
              success: false,
              error: result.error || 'Account creation failed. Please try again.',
              shouldReturnToRegistration: true,
            };
          }

          // Clear rate limits on successful signup
          await rateLimitService.clearRateLimit('signup');
          await emailRateLimitService.resetRateLimit();

          return { success: true };

        } catch (error) {
          console.error('Account creation error:', error);
          return {
            success: false,
            error: 'Account creation failed. Please try again.',
            shouldReturnToRegistration: true,
          };
        }
      },
    })
);

// Selectors for common state access patterns
export const useOnboardingProgress = () => 
  useOnboardingStore((state) => state.progress);

export const useOnboardingFormData = () => 
  useOnboardingStore((state) => state.formData);

export const useOnboardingIsLoading = () => 
  useOnboardingStore((state) => state.isLoading);

export const useOnboardingError = () => 
  useOnboardingStore((state) => state.error);

// Individual action selectors
export const useOnboardingNextStep = () => 
  useOnboardingStore((state) => state.nextStep);

export const useOnboardingPreviousStep = () => 
  useOnboardingStore((state) => state.previousStep);

export const useOnboardingUpdateFormData = () => 
  useOnboardingStore((state) => state.updateFormData);

export const useOnboardingSetCurrentStep = () => 
  useOnboardingStore((state) => state.setCurrentStep);

export const useOnboardingSetCurrentStepById = () => 
  useOnboardingStore((state) => state.setCurrentStepById);

export const useOnboardingCompleteStep = () => 
  useOnboardingStore((state) => state.completeStep);

export const useOnboardingCompleteOnboarding = () => 
  useOnboardingStore((state) => state.completeOnboarding);

export const useOnboardingResetOnboarding = () => 
  useOnboardingStore((state) => state.resetOnboarding);

export const useOnboardingSetLoading = () => 
  useOnboardingStore((state) => state.setLoading);

export const useOnboardingSetError = () => 
  useOnboardingStore((state) => state.setError);

export const useOnboardingStartOnboarding = () => 
  useOnboardingStore((state) => state.startOnboarding);