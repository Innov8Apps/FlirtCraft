import { useEffect, useMemo } from 'react';
import { Redirect } from 'expo-router';
import { Box, Spinner, Center } from 'native-base';
import { useOnboardingProgress, useOnboardingStartOnboarding } from '../stores/onboardingStore';

export default function IndexScreen() {
  const progress = useOnboardingProgress();
  const startOnboarding = useOnboardingStartOnboarding();

  const stepRoutes = useMemo(() => ({
    welcome: '/onboarding/welcome',
    age_verification: '/onboarding/age-verification',
    registration: '/onboarding/register',
    preferences: '/onboarding/preferences',
    skill_goals: '/onboarding/skills',
  }), []);

  useEffect(() => {
    // Initialize onboarding if not started
    if (!progress.startedAt) {
      startOnboarding();
    }
  }, [progress.startedAt, startOnboarding]);

  // Check if onboarding is completed
  if (progress.isCompleted) {
    return <Redirect href="/main" />;
  }

  // Redirect to the current onboarding step
  const currentRoute = stepRoutes[progress.currentStepId];
  
  if (currentRoute) {
    return <Redirect href={currentRoute} />;
  }

  // Fallback loading state
  return (
    <Center flex={1} bg="white">
      <Spinner size="lg" color="primary.500" />
    </Center>
  );
}