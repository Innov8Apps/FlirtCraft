export interface OnboardingStepProps {
  onNext: () => Promise<boolean>;
  onBack?: () => void;
  onSkip?: () => void;
  stepIndex: number;
  totalSteps: number;
}

export interface RegistrationFormData {
  email: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: boolean;
  agreedToPrivacy: boolean;
  marketingOptIn: boolean;
}

export interface PreferenceFormData {
  genderPreference: 'male' | 'female' | 'randomized';
  ageRangeMin: number;
  ageRangeMax: number;
  relationshipGoal: 'dating' | 'relationships' | 'practice' | 'confidence';
}

export interface SkillGoalFormData {
  primaryGoals: ('conversation_starters' | 'keeping_flow' | 'storytelling')[];
  specificChallenges: string[];
  experienceLevel: 'beginner' | 'intermediate' | 'returning';
  practiceFrequency: 'daily' | 'weekly' | 'occasional';
}

export interface OnboardingFormData {
  registration: Partial<RegistrationFormData>;
  preferences: Partial<PreferenceFormData>;
  skillGoals: Partial<SkillGoalFormData>;
  ageVerification: {
    birthDate: Date | null;
    isVerified: boolean;
  };
}

export type OnboardingPersona = 'anxiousAlex' | 'comebackCatherine' | 'confidentCarlos' | 'shySarah' | null;

export interface OnboardingStep {
  id: string;
  title: string;
  component: string;
  required: boolean;
  completed: boolean;
  skippable: boolean;
  estimatedDuration?: number;
}