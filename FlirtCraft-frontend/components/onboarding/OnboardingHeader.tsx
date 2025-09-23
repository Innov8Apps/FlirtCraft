import React, { useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  Easing
} from 'react-native-reanimated';

interface OnboardingHeaderProps {
  currentStep: number;
  totalSteps: number;
  onBack: () => void;
  showBackButton?: boolean;
}

export default function OnboardingHeader({
  currentStep,
  totalSteps,
  onBack,
  showBackButton = true,
}: OnboardingHeaderProps) {
  const progress = currentStep / totalSteps;
  const progressWidth = useSharedValue(progress * 100);

  useEffect(() => {
    progressWidth.value = withTiming(progress * 100, {
      duration: 300,
      easing: Easing.out(Easing.cubic),
    });
  }, [currentStep, progress]);

  const progressBarStyle = useAnimatedStyle(() => ({
    width: `${Math.max(0, Math.min(100, progressWidth.value))}%`,
  }));

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.headerRow}>
          <View style={styles.leftSection}>
            {showBackButton && (
              <TouchableOpacity
                onPress={onBack}
                style={styles.backButtonTouchable}
                accessibilityRole="button"
                accessibilityLabel="Go back"
                accessibilityHint="Return to previous step"
              >
                <Ionicons name="chevron-back" size={24} color="#FF6B35" />
              </TouchableOpacity>
            )}
          </View>

          <View style={styles.centerSection}>
            <Text style={styles.stepText}>Step {currentStep} of {totalSteps}</Text>
          </View>

          <View style={styles.rightSection} />
        </View>

        <View style={styles.progressBarContainer}>
          <View style={styles.progressBarBackground} />
          <Animated.View
            style={[styles.progressBarFill, progressBarStyle]}
          />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
  },
  content: {
    paddingHorizontal: 20,
    paddingVertical: 15,
    minHeight: 80,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  leftSection: {
    flex: 1,
    alignItems: 'flex-start',
  },
  centerSection: {
    flex: 1,
    alignItems: 'center',
  },
  rightSection: {
    flex: 1,
  },
  backButtonTouchable: {
    paddingVertical: 0,
    paddingHorizontal: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FF6B35',
  },
  progressBarContainer: {
    width: '100%',
    height: 8,
    position: 'relative',
    marginTop: 4,
  },
  progressBarBackground: {
    width: '100%',
    height: 8,
    backgroundColor: '#E5E5E5',
    borderRadius: 4,
  },
  progressBarFill: {
    position: 'absolute',
    top: 0,
    left: 0,
    height: 8,
    backgroundColor: '#FF6B35',
    borderRadius: 4,
  },
});