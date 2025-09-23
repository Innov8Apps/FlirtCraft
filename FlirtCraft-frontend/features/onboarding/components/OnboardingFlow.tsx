import React, { useEffect } from 'react';
import { View, StyleSheet, Platform, KeyboardAvoidingView } from 'react-native';
import Animated, {
  FadeIn,
  SlideInRight,
  SlideOutLeft,
  Easing,
} from 'react-native-reanimated';
import OnboardingHeader from '@/components/onboarding/OnboardingHeader';
import { useOnboardingStore } from '@/stores/onboardingStore';
import WelcomeScreen from './WelcomeScreen';
import AgeVerificationScreen from './AgeVerificationScreen';
import AuthenticationScreen from './AuthenticationScreen';
import PreferencesScreen from './PreferencesScreen';
import SkillGoalsScreen from './SkillGoalsScreen';

export default function OnboardingFlow() {
  const {
    currentStepIndex,
    steps,
    initializeOnboarding,
    goToNextStep,
    goToPreviousStep,
    canGoBack,
    isTransitioning,
  } = useOnboardingStore();


  useEffect(() => {
    initializeOnboarding();
  }, []);

  const renderStepProps = () => ({
    onNext: goToNextStep,
    onBack: canGoBack ? goToPreviousStep : undefined,
    stepIndex: currentStepIndex,
    totalSteps: steps.length,
  });

  const currentStep = steps[currentStepIndex];
  if (!currentStep) return null;

  const renderStepComponent = () => {
    const stepProps = renderStepProps();

    switch (currentStep.component) {
      case 'WelcomeIntro':
        return <WelcomeScreen {...stepProps} />;
      case 'AgeVerification':
        return <AgeVerificationScreen {...stepProps} />;
      case 'Registration':
        return <AuthenticationScreen {...stepProps} />;
      case 'PreferenceSetup':
        return <PreferencesScreen {...stepProps} />;
      case 'SkillGoalSelection':
        return <SkillGoalsScreen {...stepProps} />;
      default:
        return <WelcomeScreen {...stepProps} />;
    }
  };

  const showHeader = currentStep.id !== 'welcome';

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={styles.container}>
        {/* Header - NO ANIMATIONS */}
        {showHeader && (
          <OnboardingHeader
            currentStep={currentStepIndex + 1}
            totalSteps={steps.length}
            onBack={canGoBack ? goToPreviousStep : undefined}
            showBackButton={canGoBack}
          />
        )}

        {/* Content Container - Isolates animations */}
        <View style={styles.contentContainer}>
          <Animated.View
            key={`content-${currentStep.id}`}
            entering={SlideInRight.duration(350).easing(Easing.out(Easing.cubic))}
            exiting={SlideOutLeft.duration(250).easing(Easing.in(Easing.cubic))}
            style={styles.content}
          >
            {renderStepComponent()}
          </Animated.View>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  headerContainer: {
    // Header should not flex, just take required space
  },
  contentContainer: {
    flex: 1,
    overflow: 'hidden', // Prevents slide animations from affecting other elements
  },
  content: {
    flex: 1,
  },
});