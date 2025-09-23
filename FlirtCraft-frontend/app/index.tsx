import React, { useEffect } from 'react';
import { useRouter } from 'expo-router';
import { useOnboardingStore } from '@/stores/onboardingStore';
import OnboardingFlow from '@/features/onboarding/components/OnboardingFlow';
import MainAppPlaceholder from '@/components/MainAppPlaceholder';

export default function HomePage() {
  const { isComplete } = useOnboardingStore();
  const router = useRouter();

  // Show onboarding or main app based on completion
  if (isComplete) {
    return <MainAppPlaceholder />;
  } else {
    return <OnboardingFlow />;
  }
}