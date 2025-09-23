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
import OnboardingButton from '@/components/onboarding/OnboardingButton';
import { OnboardingStepProps } from '../types';
import { useOnboardingStore } from '@/stores/onboardingStore';

const skillGoalsSchema = z.object({
  primaryGoals: z.array(z.enum(['conversation_starters', 'keeping_flow', 'storytelling']))
    .min(1, 'Please select at least one skill goal')
    .max(3, 'Please select up to 3 primary goals'),
  specificChallenges: z.array(z.string()).optional(),
  experienceLevel: z.enum(['beginner', 'intermediate', 'returning']),
  practiceFrequency: z.enum(['daily', 'weekly', 'occasional']),
});

type SkillGoalsFormData = z.infer<typeof skillGoalsSchema>;

interface SkillCardProps {
  value: 'conversation_starters' | 'keeping_flow' | 'storytelling';
  title: string;
  description: string;
  icon: keyof typeof Ionicons.glyphMap;
  selected: boolean;
  onToggle: (value: 'conversation_starters' | 'keeping_flow' | 'storytelling') => void;
  disabled?: boolean;
}

const SkillCard: React.FC<SkillCardProps> = ({
  value,
  title,
  description,
  icon,
  selected,
  onToggle,
  disabled = false,
}) => {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePress = () => {
    if (disabled) return;

    scale.value = withSpring(0.95, { duration: 100 }, () => {
      scale.value = withSpring(1, { duration: 200 });
    });
    onToggle(value);
  };

  return (
    <Animated.View style={animatedStyle}>
      <TouchableOpacity
        style={[
          styles.skillCard,
          selected && styles.skillCardSelected,
          disabled && styles.skillCardDisabled,
        ]}
        onPress={handlePress}
        disabled={disabled}
        accessibilityRole="checkbox"
        accessibilityState={{ checked: selected, disabled }}
        accessibilityLabel={`${title}: ${description}`}
      >
        <View style={[styles.skillIconContainer, selected && styles.skillIconSelected]}>
          <Ionicons name={icon} size={28} color={selected ? '#FFFFFF' : '#FF6B35'} />
        </View>
        <View style={styles.skillContent}>
          <Text style={[styles.skillTitle, selected && styles.skillTitleSelected]}>
            {title}
          </Text>
          <Text style={[styles.skillDescription, selected && styles.skillDescriptionSelected]}>
            {description}
          </Text>
        </View>
        {selected && (
          <View style={styles.selectedCheck}>
            <Ionicons name="checkmark-circle" size={24} color="#4CAF50" />
          </View>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
};

interface ChallengeChipProps {
  label: string;
  selected: boolean;
  onToggle: () => void;
}

const ChallengeChip: React.FC<ChallengeChipProps> = ({ label, selected, onToggle }) => {
  return (
    <TouchableOpacity
      style={[styles.challengeChip, selected && styles.challengeChipSelected]}
      onPress={onToggle}
      accessibilityRole="checkbox"
      accessibilityState={{ checked: selected }}
    >
      <Text style={[styles.challengeChipText, selected && styles.challengeChipTextSelected]}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

interface RadioOptionProps {
  value: string;
  label: string;
  description: string;
  selected: boolean;
  onSelect: () => void;
}

const RadioOption: React.FC<RadioOptionProps> = ({
  value,
  label,
  description,
  selected,
  onSelect,
}) => {
  return (
    <TouchableOpacity
      style={[styles.radioOption, selected && styles.radioOptionSelected]}
      onPress={onSelect}
      accessibilityRole="radio"
      accessibilityState={{ selected }}
    >
      <View style={styles.radioContent}>
        <Text style={[styles.radioLabel, selected && styles.radioLabelSelected]}>
          {label}
        </Text>
        <Text style={[styles.radioDescription, selected && styles.radioDescriptionSelected]}>
          {description}
        </Text>
      </View>
      <View style={[styles.radioCircle, selected && styles.radioCircleSelected]}>
        {selected && <View style={styles.radioInner} />}
      </View>
    </TouchableOpacity>
  );
};

export default function SkillGoalsScreen({ onNext, onBack }: OnboardingStepProps) {
  const { updateFormData, formData } = useOnboardingStore();
  const [isLoading, setIsLoading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);


  const form = useForm<SkillGoalsFormData>({
    resolver: zodResolver(skillGoalsSchema),
    defaultValues: {
      primaryGoals: formData.skillGoals.primaryGoals || [],
      specificChallenges: formData.skillGoals.specificChallenges || [],
      experienceLevel: formData.skillGoals.experienceLevel || 'beginner',
      practiceFrequency: formData.skillGoals.practiceFrequency || 'weekly',
    }
  });

  const { control, handleSubmit, watch, setValue, formState: { isValid } } = form;
  const watchedPrimaryGoals = watch('primaryGoals');
  const watchedChallenges = watch('specificChallenges');

  const handleSubmitSkillGoals = async (data: SkillGoalsFormData) => {
    setIsLoading(true);
    try {
      updateFormData('skillGoals', data);
      await onNext();
    } catch (error) {
      console.error('Error saving skill goals:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePrimaryGoal = (goal: 'conversation_starters' | 'keeping_flow' | 'storytelling') => {
    const currentGoals = watchedPrimaryGoals || [];
    const isSelected = currentGoals.includes(goal);
    const maxGoals = 3;

    if (isSelected) {
      // Remove the goal
      const newGoals = currentGoals.filter(g => g !== goal);
      setValue('primaryGoals', newGoals, { shouldValidate: true });
    } else if (currentGoals.length < maxGoals) {
      // Add the goal
      const newGoals = [...currentGoals, goal];
      setValue('primaryGoals', newGoals, { shouldValidate: true });
    }
  };

  const toggleChallenge = (challenge: string) => {
    const currentChallenges = watchedChallenges || [];
    const isSelected = currentChallenges.includes(challenge);

    if (isSelected) {
      const newChallenges = currentChallenges.filter(c => c !== challenge);
      setValue('specificChallenges', newChallenges);
    } else {
      const newChallenges = [...currentChallenges, challenge];
      setValue('specificChallenges', newChallenges);
    }
  };


  const primarySkills = [
    {
      value: 'conversation_starters' as const,
      title: 'Conversation Starters',
      description: 'Learn to break the ice naturally and start engaging conversations',
      icon: 'chatbubble-ellipses-outline' as keyof typeof Ionicons.glyphMap,
    },
    {
      value: 'keeping_flow' as const,
      title: 'Keeping Flow',
      description: 'Maintain natural conversation rhythm and avoid awkward silences',
      icon: 'trending-up-outline' as keyof typeof Ionicons.glyphMap,
    },
    {
      value: 'storytelling' as const,
      title: 'Storytelling',
      description: 'Share experiences in compelling and engaging ways',
      icon: 'book-outline' as keyof typeof Ionicons.glyphMap,
    },
  ];

  const specificChallenges = [
    'Handling rejection gracefully',
    'Reading body language signals',
    'Escalating from chat to asking out',
    'Dealing with nervousness',
    'Being authentic while flirting',
    'Recovering from awkward moments',
  ];

  const experienceLevels = [
    {
      value: 'beginner',
      label: 'Complete Beginner',
      description: 'New to dating or conversation skills',
    },
    {
      value: 'intermediate',
      label: 'Some Experience',
      description: 'Have some dating experience but want to improve',
    },
    {
      value: 'returning',
      label: 'Getting Back Out There',
      description: 'Returning to dating after a break',
    },
  ];

  const practiceFrequencies = [
    {
      value: 'daily',
      label: 'Daily Practice',
      description: 'Short daily sessions to build habits',
    },
    {
      value: 'weekly',
      label: 'Weekly Sessions',
      description: 'Focused weekly practice sessions',
    },
    {
      value: 'occasional',
      label: 'As Needed',
      description: 'Practice when preparing for specific situations',
    },
  ];

  const selectedCount = watchedPrimaryGoals?.length || 0;
  const maxCount = 3;

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
                What conversation skills do you want to improve?
              </Text>
              <Text style={styles.explanation}>
                Choose 1-3 primary areas to focus on. We'll customize your practice sessions based on your goals.
              </Text>
            </Animated.View>

            {/* Primary Skills Section */}
            <Animated.View entering={FadeIn.delay(700).duration(500)} style={styles.section}>
              <View style={styles.sectionHeader}>
                <Text style={styles.sectionTitle}>Primary Skills ({selectedCount}/{maxCount})</Text>
                {selectedCount > 0 && (
                  <Text style={styles.selectedCount}>
                    {selectedCount} selected
                  </Text>
                )}
              </View>

              <View style={styles.skillCards}>
                {primarySkills.map((skill) => (
                  <SkillCard
                    key={skill.value}
                    value={skill.value}
                    title={skill.title}
                    description={skill.description}
                    icon={skill.icon}
                    selected={watchedPrimaryGoals?.includes(skill.value) || false}
                    onToggle={togglePrimaryGoal}
                    disabled={!watchedPrimaryGoals?.includes(skill.value) && selectedCount >= maxCount}
                  />
                ))}
              </View>
            </Animated.View>

            {/* Experience Level Section */}
            <Animated.View entering={FadeIn.delay(1100).duration(500)} style={styles.section}>
              <Text style={styles.sectionTitle}>Experience Level</Text>
              <Text style={styles.sectionDescription}>
                This helps us adjust the difficulty and pace of your practice sessions.
              </Text>

              <Controller
                control={control}
                name="experienceLevel"
                render={({ field: { onChange, value } }) => (
                  <View style={styles.radioGroup}>
                    {experienceLevels.map((level) => (
                      <RadioOption
                        key={level.value}
                        value={level.value}
                        label={level.label}
                        description={level.description}
                        selected={value === level.value}
                        onSelect={() => onChange(level.value)}
                      />
                    ))}
                  </View>
                )}
              />
            </Animated.View>

            {/* Practice Frequency Section */}
            <Animated.View entering={FadeIn.delay(1500).duration(500)} style={styles.section}>
              <Text style={styles.sectionTitle}>Practice Frequency</Text>
              <Text style={styles.sectionDescription}>
                How often would you like to practice? You can always adjust this later.
              </Text>

              <Controller
                control={control}
                name="practiceFrequency"
                render={({ field: { onChange, value } }) => (
                  <View style={styles.radioGroup}>
                    {practiceFrequencies.map((frequency) => (
                      <RadioOption
                        key={frequency.value}
                        value={frequency.value}
                        label={frequency.label}
                        description={frequency.description}
                        selected={value === frequency.value}
                        onSelect={() => onChange(frequency.value)}
                      />
                    ))}
                  </View>
                )}
              />
            </Animated.View>

            {/* Advanced Options */}
            <Animated.View entering={FadeIn.delay(1900).duration(500)} style={styles.section}>
              <TouchableOpacity
                style={styles.advancedToggle}
                onPress={() => setShowAdvanced(!showAdvanced)}
              >
                <Text style={styles.advancedToggleText}>
                  Specific Challenges (Optional)
                </Text>
                <Ionicons
                  name={showAdvanced ? 'chevron-up' : 'chevron-down'}
                  size={20}
                  color="#FF6B35"
                />
              </TouchableOpacity>

              {showAdvanced && (
                <Animated.View entering={FadeIn} style={styles.challengesContainer}>
                  <Text style={styles.sectionDescription}>
                    Select any specific areas you'd like extra help with.
                  </Text>
                  <View style={styles.challengeChips}>
                    {specificChallenges.map((challenge) => (
                      <ChallengeChip
                        key={challenge}
                        label={challenge}
                        selected={watchedChallenges?.includes(challenge) || false}
                        onToggle={() => toggleChallenge(challenge)}
                      />
                    ))}
                  </View>
                </Animated.View>
              )}
            </Animated.View>

            <Animated.View entering={FadeIn.delay(2300).duration(400)} style={styles.buttonContainer}>
              <OnboardingButton
                title="Start Practicing"
                onPress={handleSubmit(handleSubmitSkillGoals)}
                loading={isLoading}
                disabled={!isValid}
                accessibilityLabel="Complete onboarding and start practicing"
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
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1A1A1A',
  },
  selectedCount: {
    fontSize: 14,
    color: '#FF6B35',
    fontWeight: '500',
  },
  sectionDescription: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 16,
    lineHeight: 20,
  },
  skillCards: {
    gap: 16,
  },
  skillCard: {
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
  skillCardSelected: {
    borderColor: '#FF6B35',
    backgroundColor: '#FFF7F4',
  },
  skillCardDisabled: {
    opacity: 0.5,
  },
  skillIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#FFF7F4',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  skillIconSelected: {
    backgroundColor: '#FF6B35',
  },
  skillContent: {
    flex: 1,
  },
  skillTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  skillTitleSelected: {
    color: '#FF6B35',
  },
  skillDescription: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  skillDescriptionSelected: {
    color: '#FF7F50',
  },
  selectedCheck: {
    marginLeft: 12,
  },
  radioGroup: {
    gap: 12,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#E5E5E5',
  },
  radioOptionSelected: {
    borderColor: '#FF6B35',
    backgroundColor: '#FFF7F4',
  },
  radioContent: {
    flex: 1,
  },
  radioLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  radioLabelSelected: {
    color: '#FF6B35',
  },
  radioDescription: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  radioDescriptionSelected: {
    color: '#FF7F50',
  },
  radioCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#E5E5E5',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 12,
  },
  radioCircleSelected: {
    borderColor: '#FF6B35',
  },
  radioInner: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#FF6B35',
  },
  advancedToggle: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
  },
  advancedToggleText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FF6B35',
  },
  challengesContainer: {
    marginTop: 16,
  },
  challengeChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  challengeChip: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#E5E5E5',
  },
  challengeChipSelected: {
    backgroundColor: '#FF6B35',
    borderColor: '#FF6B35',
  },
  challengeChipText: {
    fontSize: 14,
    color: '#6B7280',
    fontWeight: '500',
  },
  challengeChipTextSelected: {
    color: '#FFFFFF',
  },
  buttonContainer: {
    marginTop: 24,
  },
});