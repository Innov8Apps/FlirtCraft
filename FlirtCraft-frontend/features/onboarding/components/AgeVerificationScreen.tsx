import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Platform,
  Alert,
} from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import Animated, {
  FadeIn,
  SlideInUp,
  useAnimatedStyle,
  useSharedValue,
  withSpring,
  withDelay,
} from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';
import OnboardingButton from '@/components/onboarding/OnboardingButton';
import { OnboardingStepProps } from '../types';
import { useOnboardingStore } from '@/stores/onboardingStore';

export default function AgeVerificationScreen({ onNext, onBack }: OnboardingStepProps) {
  const [birthDate, setBirthDate] = useState<Date>(new Date(2000, 0, 1));
  const [showDatePicker, setShowDatePicker] = useState(Platform.OS === 'ios');
  const [isEligible, setIsEligible] = useState(false);

  const { updateFormData, setUserChoice } = useOnboardingStore();

  const buttonOpacity = useSharedValue(0.5);

  useEffect(() => {
    const age = calculateAge(birthDate);
    const eligible = age >= 18;
    setIsEligible(eligible);
    buttonOpacity.value = withSpring(eligible ? 1 : 0.5);
  }, [birthDate]);

  const calculateAge = (date: Date): number => {
    const today = new Date();
    const birth = new Date(date);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }

    return age;
  };

  const handleDateChange = (event: any, selectedDate?: Date) => {
    if (Platform.OS === 'android') {
      setShowDatePicker(false);
    }

    if (selectedDate) {
      setBirthDate(selectedDate);
    }
  };

  const handleConfirmAge = async () => {
    if (!isEligible) {
      Alert.alert(
        'Age Requirement',
        'FlirtCraft is designed for adults 18 and over. Thanks for your interest!',
        [{ text: 'OK' }]
      );
      return;
    }

    // Update form data
    updateFormData('ageVerification', {
      birthDate,
      isVerified: true,
    });

    // Update user choice
    setUserChoice('ageVerified', true);

    await onNext();
  };


  const buttonAnimatedStyle = useAnimatedStyle(() => ({
    opacity: buttonOpacity.value,
  }));

  const age = calculateAge(birthDate);

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#FFFFFF', '#FFF7F4']}
        style={styles.backgroundGradient}
      >
        <Animated.View style={styles.content}>
          <Animated.View entering={FadeIn.delay(200).duration(500)}>
            <Text style={styles.headline}>
              Let's make sure you're 18+
            </Text>
            <Text style={styles.explanation}>
              FlirtCraft is designed for adults who want to improve their conversation skills in a safe environment.
            </Text>
          </Animated.View>

          <Animated.View entering={FadeIn.delay(400).duration(500)} style={styles.datePickerContainer}>
            <Text style={styles.datePickerLabel}>Your birth date:</Text>

            {Platform.OS === 'ios' ? (
              <DateTimePicker
                value={birthDate}
                mode="date"
                display="spinner"
                onChange={handleDateChange}
                maximumDate={new Date()}
                minimumDate={new Date(1900, 0, 1)}
                style={styles.datePickerIOS}
              />
            ) : (
              <View>
                <OnboardingButton
                  title={birthDate.toLocaleDateString()}
                  onPress={() => setShowDatePicker(true)}
                  variant="secondary"
                />
                {showDatePicker && (
                  <DateTimePicker
                    value={birthDate}
                    mode="date"
                    display="default"
                    onChange={handleDateChange}
                    maximumDate={new Date()}
                    minimumDate={new Date(1900, 0, 1)}
                  />
                )}
              </View>
            )}

            {age >= 13 && (
              <Animated.View entering={FadeIn.duration(300)} style={styles.ageDisplay}>
                <Text style={[
                  styles.ageText,
                  isEligible ? styles.ageTextValid : styles.ageTextInvalid
                ]}>
                  Age: {age} years old
                </Text>
                {!isEligible && age >= 13 && (
                  <Text style={styles.ageRequirement}>
                    You must be 18 or older to use FlirtCraft
                  </Text>
                )}
              </Animated.View>
            )}
          </Animated.View>

          <Animated.View
            entering={FadeIn.delay(600).duration(400)}
            style={[styles.buttonContainer, buttonAnimatedStyle]}
          >
            <OnboardingButton
              title="Confirm Age"
              onPress={handleConfirmAge}
              disabled={!isEligible}
              accessibilityLabel={`Confirm age ${age} years old`}
              accessibilityHint={isEligible ? "Continue to next step" : "Age verification required"}
            />
          </Animated.View>

          <Animated.View entering={FadeIn.delay(700).duration(400)} style={styles.legalText}>
            <Text style={styles.complianceText}>
              This verification is required for legal compliance and to ensure an age-appropriate experience.
            </Text>
          </Animated.View>
        </Animated.View>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  backgroundGradient: {
    flex: 1,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingVertical: 32,
    justifyContent: 'center',
  },
  headline: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1A1A1A',
    textAlign: 'center',
    marginBottom: 16,
  },
  explanation: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 48,
    lineHeight: 24,
  },
  datePickerContainer: {
    alignItems: 'center',
    marginBottom: 48,
  },
  datePickerLabel: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 16,
  },
  datePickerIOS: {
    height: 200,
    width: '100%',
  },
  ageDisplay: {
    marginTop: 16,
    alignItems: 'center',
  },
  ageText: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  ageTextValid: {
    color: '#4CAF50',
  },
  ageTextInvalid: {
    color: '#EF4444',
  },
  ageRequirement: {
    fontSize: 14,
    color: '#EF4444',
    textAlign: 'center',
  },
  buttonContainer: {
    marginBottom: 24,
  },
  legalText: {
    paddingHorizontal: 16,
  },
  complianceText: {
    fontSize: 12,
    color: '#9CA3AF',
    textAlign: 'center',
    lineHeight: 16,
  },
});