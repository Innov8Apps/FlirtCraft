import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Animated, {
  FadeIn,
  SlideInUp,
  useAnimatedStyle,
  useSharedValue,
  withSpring,
  withDelay,
} from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import Slider from '@react-native-community/slider';
import OnboardingButton from '@/components/onboarding/OnboardingButton';
import { OnboardingStepProps } from '../types';
import { useOnboardingStore } from '@/stores/onboardingStore';

const preferencesSchema = z.object({
  genderPreference: z.enum(['male', 'female', 'randomized']),
  ageRangeMin: z.number().min(18).max(100),
  ageRangeMax: z.number().min(18).max(100),
  relationshipGoal: z.enum(['dating', 'relationships', 'practice', 'confidence']),
}).refine(data => data.ageRangeMin <= data.ageRangeMax, {
  message: "Minimum age cannot be greater than maximum age",
  path: ["ageRangeMin"],
});

type PreferencesFormData = z.infer<typeof preferencesSchema>;

interface GenderOptionProps {
  value: 'male' | 'female' | 'randomized';
  label: string;
  icon: keyof typeof Ionicons.glyphMap;
  description: string;
  selected: boolean;
  onSelect: (value: 'male' | 'female' | 'randomized') => void;
}

const GenderOption: React.FC<GenderOptionProps> = ({
  value,
  label,
  icon,
  description,
  selected,
  onSelect,
}) => {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePress = () => {
    // Simple press feedback
    scale.value = withSpring(0.96, { damping: 15, stiffness: 200 }, () => {
      scale.value = withSpring(1, { damping: 15, stiffness: 200 });
    });
    onSelect(value);
  };

  return (
    <Animated.View style={animatedStyle}>
      <TouchableOpacity
        style={[styles.genderOption, selected && styles.genderOptionSelected]}
        onPress={handlePress}
        accessibilityRole="radio"
        accessibilityState={{ selected }}
        accessibilityLabel={`${label}: ${description}`}
      >
        <View style={[styles.genderIconContainer, selected && styles.genderIconSelected]}>
          <Ionicons name={icon} size={24} color={selected ? '#FFFFFF' : '#FF6B35'} />
        </View>
        <View style={styles.genderContent}>
          <Text style={[styles.genderLabel, selected && styles.genderLabelSelected]}>
            {label}
          </Text>
          <Text style={[styles.genderDescription, selected && styles.genderDescriptionSelected]}>
            {description}
          </Text>
        </View>
        {selected && (
          <View style={styles.selectedIndicator}>
            <Ionicons name="checkmark-circle" size={24} color="#FF6B35" />
          </View>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
};

interface RelationshipGoalProps {
  value: 'dating' | 'relationships' | 'practice' | 'confidence';
  label: string;
  description: string;
  selected: boolean;
  onSelect: (value: 'dating' | 'relationships' | 'practice' | 'confidence') => void;
}

const RelationshipGoal: React.FC<RelationshipGoalProps> = ({
  value,
  label,
  description,
  selected,
  onSelect,
}) => {
  return (
    <TouchableOpacity
      style={[styles.goalOption, selected && styles.goalOptionSelected]}
      onPress={() => onSelect(value)}
      accessibilityRole="radio"
      accessibilityState={{ selected }}
      accessibilityLabel={`${label}: ${description}`}
    >
      <View style={styles.goalContent}>
        <Text style={[styles.goalLabel, selected && styles.goalLabelSelected]}>
          {label}
        </Text>
        <Text style={[styles.goalDescription, selected && styles.goalDescriptionSelected]}>
          {description}
        </Text>
      </View>
      <View style={[styles.goalRadio, selected && styles.goalRadioSelected]}>
        {selected && <View style={styles.goalRadioInner} />}
      </View>
    </TouchableOpacity>
  );
};

export default function PreferencesScreen({ onNext, onBack }: OnboardingStepProps) {
  const { updateFormData, formData } = useOnboardingStore();
  const [isLoading, setIsLoading] = useState(false);


  const form = useForm<PreferencesFormData>({
    resolver: zodResolver(preferencesSchema),
    defaultValues: {
      genderPreference: formData.preferences.genderPreference || 'randomized',
      ageRangeMin: formData.preferences.ageRangeMin || 22,
      ageRangeMax: formData.preferences.ageRangeMax || 32,
      relationshipGoal: formData.preferences.relationshipGoal || 'practice',
    }
  });

  const { watch, control, handleSubmit, formState: { isValid } } = form;
  const watchedValues = watch();

  const handleSubmitPreferences = async (data: PreferencesFormData) => {
    setIsLoading(true);
    try {
      updateFormData('preferences', data);
      await onNext();
    } catch (error) {
      console.error('Error saving preferences:', error);
    } finally {
      setIsLoading(false);
    }
  };


  const genderOptions = [
    {
      value: 'male' as const,
      label: 'Men',
      icon: 'male' as keyof typeof Ionicons.glyphMap,
      description: 'Practice conversations with male AI partners',
    },
    {
      value: 'female' as const,
      label: 'Women',
      icon: 'female' as keyof typeof Ionicons.glyphMap,
      description: 'Practice conversations with female AI partners',
    },
    {
      value: 'randomized' as const,
      label: 'Everyone',
      icon: 'people' as keyof typeof Ionicons.glyphMap,
      description: 'Mix of different conversation partners',
    },
  ];

  const relationshipGoals = [
    {
      value: 'practice' as const,
      label: 'General Practice',
      description: 'Build overall conversation skills',
    },
    {
      value: 'dating' as const,
      label: 'Dating',
      description: 'Focus on dating and romantic connections',
    },
    {
      value: 'relationships' as const,
      label: 'Relationships',
      description: 'Improve existing relationship communication',
    },
    {
      value: 'confidence' as const,
      label: 'Confidence Building',
      description: 'Overcome social anxiety and build confidence',
    },
  ];

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#FFFFFF', '#FFF7F4']}
        style={styles.backgroundGradient}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          <Animated.View style={styles.content}>
            <Animated.View entering={FadeIn.delay(300).duration(600)}>
              <Text style={styles.headline}>
                Who would you like to practice with?
              </Text>
              <Text style={styles.explanation}>
                This helps create realistic practice scenarios tailored to your preferences.
              </Text>
            </Animated.View>

            {/* Gender Preference Section */}
            <Animated.View entering={FadeIn.delay(700).duration(500)} style={styles.section}>
              <Text style={styles.sectionTitle}>Practice Partner Gender</Text>
              <Controller
                control={control}
                name="genderPreference"
                render={({ field: { onChange, value } }) => (
                  <View style={styles.genderOptions}>
                    {genderOptions.map((option) => (
                      <GenderOption
                        key={option.value}
                        value={option.value}
                        label={option.label}
                        icon={option.icon}
                        description={option.description}
                        selected={value === option.value}
                        onSelect={onChange}
                      />
                    ))}
                  </View>
                )}
              />
            </Animated.View>

            {/* Age Range Section */}
            <Animated.View entering={FadeIn.delay(1100).duration(500)} style={styles.section}>
              <Text style={styles.sectionTitle}>Age Range</Text>
              <Text style={styles.sectionDescription}>
                What age range interests you? ({watchedValues.ageRangeMin} - {watchedValues.ageRangeMax} years old)
              </Text>

              <View style={styles.ageRangeContainer}>
                <Controller
                  control={control}
                  name="ageRangeMin"
                  render={({ field: { onChange, value } }) => (
                    <View style={styles.sliderContainer}>
                      <Text style={styles.sliderLabel}>Minimum Age: {value}</Text>
                      <Slider
                        style={styles.slider}
                        minimumValue={18}
                        maximumValue={watchedValues.ageRangeMax || 50}
                        value={value}
                        onValueChange={onChange}
                        step={1}
                        minimumTrackTintColor="#FF6B35"
                        maximumTrackTintColor="#E5E5E5"
                      />
                    </View>
                  )}
                />

                <Controller
                  control={control}
                  name="ageRangeMax"
                  render={({ field: { onChange, value } }) => (
                    <View style={styles.sliderContainer}>
                      <Text style={styles.sliderLabel}>Maximum Age: {value}</Text>
                      <Slider
                        style={styles.slider}
                        minimumValue={watchedValues.ageRangeMin || 18}
                        maximumValue={65}
                        value={value}
                        onValueChange={onChange}
                        step={1}
                        minimumTrackTintColor="#FF6B35"
                        maximumTrackTintColor="#E5E5E5"
                      />
                    </View>
                  )}
                />
              </View>
            </Animated.View>

            {/* Relationship Goal Section */}
            <Animated.View entering={FadeIn.delay(1500).duration(500)} style={styles.section}>
              <Text style={styles.sectionTitle}>What's your main goal?</Text>
              <Text style={styles.sectionDescription}>
                This helps us customize the practice scenarios for you.
              </Text>

              <Controller
                control={control}
                name="relationshipGoal"
                render={({ field: { onChange, value } }) => (
                  <View style={styles.goalOptions}>
                    {relationshipGoals.map((goal) => (
                      <RelationshipGoal
                        key={goal.value}
                        value={goal.value}
                        label={goal.label}
                        description={goal.description}
                        selected={value === goal.value}
                        onSelect={onChange}
                      />
                    ))}
                  </View>
                )}
              />
            </Animated.View>

            <Animated.View entering={FadeIn.delay(1900).duration(400)} style={styles.buttonContainer}>
              <OnboardingButton
                title="Continue Setup"
                onPress={handleSubmit(handleSubmitPreferences)}
                loading={isLoading}
                disabled={!isValid}
                accessibilityLabel="Continue to skill goals setup"
              />
            </Animated.View>
          </Animated.View>
        </ScrollView>
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
  scrollContent: {
    paddingHorizontal: 24,
    paddingVertical: 32,
  },
  content: {
    flex: 1,
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
    marginBottom: 32,
    lineHeight: 24,
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  sectionDescription: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 16,
    lineHeight: 20,
  },
  genderOptions: {
    gap: 12,
  },
  genderOption: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#E5E5E5',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 3,
  },
  genderOptionSelected: {
    borderColor: '#FF6B35',
    backgroundColor: '#FFF7F4',
  },
  genderIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#FFF7F4',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  genderIconSelected: {
    backgroundColor: '#FF6B35',
  },
  genderContent: {
    flex: 1,
  },
  genderLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  genderLabelSelected: {
    color: '#FF6B35',
  },
  genderDescription: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  genderDescriptionSelected: {
    color: '#FF7F50',
  },
  selectedIndicator: {
    marginLeft: 12,
  },
  ageRangeContainer: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#E5E5E5',
  },
  sliderContainer: {
    marginBottom: 20,
  },
  sliderLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  sliderThumb: {
    backgroundColor: '#FF6B35',
    width: 20,
    height: 20,
  },
  goalOptions: {
    gap: 12,
  },
  goalOption: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#E5E5E5',
  },
  goalOptionSelected: {
    borderColor: '#FF6B35',
    backgroundColor: '#FFF7F4',
  },
  goalContent: {
    flex: 1,
  },
  goalLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  goalLabelSelected: {
    color: '#FF6B35',
  },
  goalDescription: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  goalDescriptionSelected: {
    color: '#FF7F50',
  },
  goalRadio: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#E5E5E5',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 12,
  },
  goalRadioSelected: {
    borderColor: '#FF6B35',
  },
  goalRadioInner: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#FF6B35',
  },
  buttonContainer: {
    marginTop: 24,
  },
});