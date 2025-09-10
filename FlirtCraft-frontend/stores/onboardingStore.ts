import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

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
  userGender: 'male' | 'female' | 'non-binary' | 'prefer-not-to-say';
  targetGender: 'male' | 'female' | 'everyone';
  targetAgeMin: number;
  targetAgeMax: number;
  
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
  currentStep: 0,
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
  userGender: 'female',
  targetGender: 'everyone',
  targetAgeMin: 22,
  targetAgeMax: 32,
  
  // Skill goals
  primarySkillGoals: [],
};

export const useOnboardingStore = create<OnboardingState>()(
  persist(
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
        if (step < 0 || step >= TOTAL_STEPS) return;
        
        const stepId = STEP_SEQUENCE[step];
        
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
        
        set((state) => ({
          progress: {
            ...state.progress,
            currentStep: stepIndex,
            currentStepId: stepId,
          },
        }));
      },

      nextStep: () => {
        const { progress } = get();
        const nextStep = Math.min(progress.currentStep + 1, TOTAL_STEPS - 1);
        const stepId = STEP_SEQUENCE[nextStep];
        
        set((state) => ({
          progress: {
            ...state.progress,
            currentStep: nextStep,
            currentStepId: stepId,
          },
        }));
      },

      previousStep: () => {
        const { progress } = get();
        const prevStep = Math.max(progress.currentStep - 1, 0);
        const stepId = STEP_SEQUENCE[prevStep];
        
        set((state) => ({
          progress: {
            ...state.progress,
            currentStep: prevStep,
            currentStepId: stepId,
          },
        }));
      },

      completeStep: (step: number) => {
        set((state) => {
          const newCompletedSteps = Math.max(state.progress.completedSteps, step + 1);
          
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
    }),
    {
      name: 'onboarding-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
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