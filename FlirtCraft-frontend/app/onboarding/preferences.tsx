import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { StatusBar } from 'expo-status-bar';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Slider } from '@miblanchard/react-native-slider';
import { Ionicons } from '@expo/vector-icons';
import { OnboardingHeader } from '../../components/onboarding/OnboardingHeader';
import { GradientButton } from '../../components/onboarding/GradientButton';
import { useOnboardingStore } from '../../stores/onboardingStore';
import { AnimatedContainer, StaggeredContainer } from '../../components/animations/AnimatedContainer';

const GENDER_OPTIONS = [
  { id: 'male', label: 'Male', icon: 'male' },
  { id: 'female', label: 'Female', icon: 'female' },
  { id: 'non-binary', label: 'Non-binary', icon: 'person' },
  { id: 'prefer-not-to-say', label: 'Prefer not to say', icon: 'help-circle' },
];

const TARGET_GENDER_OPTIONS = [
  { id: 'male', label: 'Men', icon: 'male' },
  { id: 'female', label: 'Women', icon: 'female' },
  { id: 'everyone', label: 'Everyone', icon: 'people' },
];

export default function PreferencesScreen() {
  const {
    formData,
    progress,
    updateFormData,
    setCurrentStepById,
    nextStep,
    previousStep,
  } = useOnboardingStore();

  const [userGender, setUserGender] = useState(formData.userGender || '');
  const [targetGender, setTargetGender] = useState(formData.targetGender || '');
  const [ageRange, setAgeRange] = useState([
    formData.targetAgeMin || 25,
    formData.targetAgeMax || 35
  ]);
  const [isNavigating, setIsNavigating] = useState(false);
  const insets = useSafeAreaInsets();

  // Validation function to check if form is complete
  const isFormValid = () => {
    return userGender && targetGender;
  };

  const handleContinue = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    setIsNavigating(true);

    // Update form data
    updateFormData({
      userGender,
      targetGender,
      targetAgeMin: ageRange[0],
      targetAgeMax: ageRange[1],
    });

    // Navigate to next step
    nextStep();
    router.push('/onboarding/skills');
  };

  const handleBack = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    setIsNavigating(true);
    previousStep();
    router.push('/onboarding/register');
  };

  const handleAgeRangeChange = (values: number[]) => {
    setAgeRange(values);
  };

  return (
    <View style={styles.outerContainer}>
      <StatusBar style="dark" />
      <LinearGradient
        colors={['#FFF6F0', '#FFFAF6', '#FFFFFF']}
        locations={[0, 0.4, 1]}
        style={styles.container}
      >
      <OnboardingHeader
        currentStep={progress.currentStep}
        totalSteps={progress.totalSteps}
        completedSteps={progress.completedSteps}
        lastNavigationDirection={progress.lastNavigationDirection}
        title="Preferences"
        onBackPress={handleBack}
        rightIcon={{
          name: 'heart-outline',
          type: 'ionicons',
          color: '#FF6B35',
          size: 24,
        }}
      />

      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
      >
        <AnimatedContainer animation="fadeSlideUp" delay={40}>
          <View style={styles.textSection}>
            <View style={styles.titleIcon}>
              <Ionicons name="heart-outline" size={56} color="#FF6B35" />
            </View>
            <Text style={styles.title}>Set Your Preferences</Text>
            <Text style={styles.description}>
              Help us personalize your conversation practice experience
            </Text>
          </View>

          {/* Group all sections together for faster render */}
          {/* Gender Selection */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>What's your gender?</Text>
            <View style={styles.optionsGrid}>
              {GENDER_OPTIONS.map((option) => (
                <TouchableOpacity
                  key={option.id}
                  style={[
                    styles.optionCard,
                    userGender === option.id && styles.optionCardSelected,
                  ]}
                  onPress={() => setUserGender(option.id as any)}
                  activeOpacity={0.7}
                >
                  <Ionicons
                    name={option.icon as any}
                    size={24}
                    color="#FF6B35"
                  />
                  <Text
                    style={[
                      styles.optionText,
                      userGender === option.id && styles.optionTextSelected,
                    ]}
                  >
                    {option.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Target Gender Selection */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Who would you like to practice with?</Text>
            <View style={styles.targetGenderGrid}>
              {TARGET_GENDER_OPTIONS.map((option) => (
                <TouchableOpacity
                  key={option.id}
                  style={[
                    styles.targetGenderCard,
                    targetGender === option.id && styles.targetGenderCardSelected,
                  ]}
                  onPress={() => setTargetGender(option.id as any)}
                  activeOpacity={0.7}
                >
                  <Ionicons
                    name={option.icon as any}
                    size={20}
                    color="#FF6B35"
                  />
                  <Text
                    style={[
                      styles.targetGenderText,
                      targetGender === option.id && styles.targetGenderTextSelected,
                    ]}
                  >
                    {option.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Age Range Selection */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Age Range Preference</Text>
            <View style={styles.ageRangeContainer}>
              <View style={styles.ageRangeDisplay}>
                <Text style={styles.ageValue}>{ageRange[0]}</Text>
                <Text style={styles.ageRangeSeparator}>-</Text>
                <Text style={styles.ageValue}>{ageRange[1]}</Text>
              </View>
            </View>
            <View style={styles.sliderContainer}>
              <Slider
                value={ageRange}
                onValueChange={handleAgeRangeChange}
                minimumValue={18}
                maximumValue={80}
                step={1}
                allowTouchTrack
                trackStyle={styles.sliderTrack}
                thumbStyle={styles.sliderThumb}
                minimumTrackTintColor="#FF6B35"
                maximumTrackTintColor="#E5E7EB"
              />
            </View>
          </View>
        </AnimatedContainer>
      </ScrollView>

        <View style={styles.buttonSection}>
          <GradientButton
            title="Continue"
            onPress={handleContinue}
            disabled={!isFormValid()}
            style={styles.continueButton}
          />
        </View>
    </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  outerContainer: {
    flex: 1,
    backgroundColor: '#FFF6F0', // Match the top gradient color for seamless blending
  },
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    paddingHorizontal: 24,
    paddingTop: 8,
  },
  textSection: {
    alignItems: 'center',
    paddingTop: 8,
    marginBottom: 24,
  },
  titleIcon: {
    marginBottom: 12,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
    textAlign: 'center',
  },
  description: {
    fontSize: 16,
    color: '#6B7280',
    lineHeight: 22,
    textAlign: 'center',
    paddingHorizontal: 20,
  },
  section: {
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 12,
    textAlign: 'left',
  },
  // Unified grid layout for all options
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  optionCard: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    width: '48%',
    marginBottom: 8,
    minHeight: 70,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  optionCardSelected: {
    backgroundColor: '#FFF5F0',
    borderColor: '#FF8C42',
    borderWidth: 2,
    shadowColor: '#FF8C42',
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 5,
  },
  optionCardInner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    height: '100%',
  },
  optionText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#6B7280',
    textAlign: 'center',
    marginLeft: 8,
    lineHeight: 16,
  },
  optionTextSelected: {
    color: '#FF6B35',
    fontWeight: '600',
  },
  // Target gender specific styles for 3-card layout
  targetGenderGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  targetGenderCard: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    minHeight: 65,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  targetGenderCardSelected: {
    backgroundColor: '#FFF5F0',
    borderColor: '#FF8C42',
    borderWidth: 2,
    shadowColor: '#FF8C42',
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 5,
  },
  targetGenderCardInner: {
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    height: '100%',
  },
  targetGenderText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6B7280',
    textAlign: 'center',
    marginTop: 6,
    lineHeight: 14,
  },
  targetGenderTextSelected: {
    color: '#FF6B35',
    fontWeight: '600',
  },
  // Age range styling - more compact
  ageRangeContainer: {
    alignItems: 'center',
    marginBottom: 12,
  },
  ageRangeDisplay: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  ageValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF6B35',
    textAlign: 'center',
  },
  ageRangeSeparator: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#9CA3AF',
    marginHorizontal: 12,
  },
  sliderContainer: {
    paddingHorizontal: 8,
    marginBottom: 4,
  },
  sliderTrack: {
    height: 4,
    borderRadius: 2,
  },
  sliderThumb: {
    backgroundColor: '#FF6B35',
    width: 20,
    height: 20,
    borderRadius: 10,
    shadowColor: '#FF6B35',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 4,
  },
  buttonSection: {
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 32,
    backgroundColor: 'transparent',
  },
  continueButton: {
    width: '100%',
  },
});