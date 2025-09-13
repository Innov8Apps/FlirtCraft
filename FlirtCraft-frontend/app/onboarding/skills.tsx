import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import { Ionicons, MaterialIcons, FontAwesome5, Feather } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { OnboardingHeader } from '../../components/onboarding/OnboardingHeader';
import { GradientButton } from '../../components/onboarding/GradientButton';
import { useOnboardingStore } from '../../stores/onboardingStore';
import { authService } from '../../services/supabase';
import { AnimatedContainer, StaggeredContainer } from '../../components/animations/AnimatedContainer';

const SKILL_GOALS = [
  {
    id: 'conversation_starters',
    title: 'The Art of Hello',
    description: 'Turn awkward hovering into smooth, confident approaches',
    icon: 'chatbubbles',
    iconType: 'ionicons',
  },
  {
    id: 'active_listening', 
    title: 'Listen Like You Mean It',
    description: 'Show genuine interest, not just waiting your turn',
    icon: 'headphones',
    iconType: 'feather',
  },
  {
    id: 'storytelling',
    title: 'Stories Worth Telling',
    description: 'Captivate them with tales that keep them leaning in',
    icon: 'book-open',
    iconType: 'feather',
  },
  {
    id: 'reading_the_room',
    title: 'Read the Signals',
    description: 'Know when to advance or when to gracefully retreat',
    icon: 'eye',
    iconType: 'ionicons',
  },
  {
    id: 'graceful_exits',
    title: 'Leave at Your Peak',
    description: 'End on a high note, not when conversation flatlines',
    icon: 'exit',
    iconType: 'ionicons',
  },
  {
    id: 'authentic_charm',
    title: 'Natural Magnetism',
    description: 'Be genuinely irresistible without the fake persona',
    icon: 'star',
    iconType: 'ionicons',
  },
  {
    id: 'flow_like_water',
    title: 'Conversation Flow',
    description: 'Keep things smooth even when your mind goes blank',
    icon: 'water',
    iconType: 'ionicons',
  },
  {
    id: 'confidence_building',
    title: 'Quiet Confidence',
    description: 'Build that magnetic self-assurance everyone notices',
    icon: 'trending-up',
    iconType: 'ionicons',
  },
];

export default function SkillsScreen() {
  const {
    formData,
    progress,
    updateFormData,
    setCurrentStepById,
    nextStep,
    previousStep,
    completeOnboarding,
    setLoading,
    isLoading,
  } = useOnboardingStore();

  const [selectedSkills, setSelectedSkills] = useState<string[]>(
    formData.primarySkillGoals || []
  );
  const [isNavigating, setIsNavigating] = useState(false);
  const insets = useSafeAreaInsets();

  // Validation function to check if at least 1 and up to 3 skills are selected
  const isFormValid = () => {
    return selectedSkills.length >= 1 && selectedSkills.length <= 3;
  };

  const toggleSkill = (skillId: string) => {
    setSelectedSkills((prev) => {
      if (prev.includes(skillId)) {
        return prev.filter((id) => id !== skillId);
      } else {
        if (prev.length >= 3) {
          Alert.alert(
            'Maximum Skills',
            'You can select up to 3 skills to focus on. You can always change these later in your profile.',
            [{ text: 'OK' }]
          );
          return prev;
        }
        return [...prev, skillId];
      }
    });
  };

  const handleComplete = async () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    if (selectedSkills.length < 1 || selectedSkills.length > 3) {
      Alert.alert(
        'Select Skills',
        'Please select at least 1 skill and up to 3 skills to focus on.',
        [{ text: 'OK' }]
      );
      return;
    }

    try {
      setIsNavigating(true);
      setLoading(true);

      // Update form data with selected skills
      updateFormData({
        primarySkillGoals: selectedSkills,
      });

      // Update user profile with complete onboarding data
      const user = await authService.getCurrentUser();
      if (user) {
        await authService.updateProfile({
          skill_goals: selectedSkills,
        });
      }

      // Complete onboarding
      completeOnboarding();

      // Navigate to main app
      router.replace('/main');
    } catch (error) {
      console.error('Error completing onboarding:', error);
      Alert.alert(
        'Something went wrong',
        'Please try again or contact support if the issue persists.',
        [{ text: 'OK' }]
      );
      setIsNavigating(false);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    setIsNavigating(true);
    previousStep();
    router.push('/onboarding/preferences');
  };

  const renderIcon = (skill: any, isSelected: boolean, isDisabled: boolean) => {
    const iconColor = isDisabled ? '#D1D5DB' : (isSelected ? '#FF6B35' : '#FF6B35');
    const iconSize = 24;

    switch(skill.iconType) {
      case 'feather':
        return <Feather name={skill.icon as any} size={iconSize} color={iconColor} />;
      case 'material':
        return <MaterialIcons name={skill.icon as any} size={iconSize} color={iconColor} />;
      case 'fontawesome':
        return <FontAwesome5 name={skill.icon as any} size={iconSize} color={iconColor} />;
      default:
        return <Ionicons name={skill.icon as any} size={iconSize} color={iconColor} />;
    }
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
          title="Learning Goals"
          onBackPress={handleBack}
          rightIcon={{
            name: 'trophy',
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
              <Ionicons name="trophy" size={56} color="#FA7215" />
            </View>
            <Text style={styles.title}>Pick Your Power-Ups</Text>
            <Text style={styles.description}>
              We'll craft your training around what matters most to you.
            </Text>
          </View>

          <View style={styles.skillsSection}>
            <Text style={styles.selectedCountText}>
              {selectedSkills.length} of 3 skills selected
            </Text>

            <View style={styles.skillsList}>
            {SKILL_GOALS.map((skill) => {
              const isSelected = selectedSkills.includes(skill.id);
              const isDisabled = selectedSkills.length >= 3 && !isSelected;

              return (
                <TouchableOpacity
                  key={skill.id}
                  style={[
                    styles.skillCard,
                    isSelected && styles.skillCardSelected,
                    isDisabled && styles.skillCardDisabled,
                  ]}
                  onPress={() => toggleSkill(skill.id)}
                  activeOpacity={0.7}
                  disabled={isDisabled}
                >
                  <View style={styles.skillIcon}>
                    {renderIcon(skill, isSelected, isDisabled)}
                  </View>

                  <View style={styles.skillContent}>
                    <Text style={[
                      styles.skillTitle,
                      isDisabled && styles.skillTitleDisabled,
                    ]}>
                      {skill.title}
                    </Text>
                    <Text style={[
                      styles.skillDescription,
                      isDisabled && styles.skillDescriptionDisabled,
                    ]}>
                      {skill.description}
                    </Text>
                  </View>

                  {isSelected && (
                    <View style={styles.checkMark}>
                      <Ionicons name="checkmark" size={12} color="#ffffff" />
                    </View>
                  )}
                </TouchableOpacity>
              );
            })}
            </View>
          </View>
        </AnimatedContainer>
      </ScrollView>

        <View style={styles.buttonSection}>
          <GradientButton
            title="Complete Setup"
            onPress={handleComplete}
            loading={isLoading}
            disabled={!isFormValid() || isLoading}
            style={styles.completeButton}
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
    marginBottom: 24,
    alignItems: 'center',
  },
  titleIcon: {
    marginBottom: 12,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 16,
    textAlign: 'center',
  },
  description: {
    fontSize: 16,
    color: '#6b7280',
    lineHeight: 24,
    textAlign: 'center',
    paddingHorizontal: 8,
  },
  skillsSection: {
    marginBottom: 8,
  },
  selectedCountText: {
    fontSize: 14,
    color: '#FF6B35',
    fontWeight: '500',
    textAlign: 'center',
    marginBottom: 20,
  },
  skillsList: {
    gap: 12,
  },
  skillCard: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  skillCardSelected: {
    backgroundColor: '#FFF5F0',
    borderColor: '#FF8C42',
    borderWidth: 2,
    shadowColor: '#FF8C42',
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 5,
  },
  skillCardDisabled: {
    // Keep same background color and dimensions as enabled cards
    backgroundColor: '#FFFFFF',

    // Maintain identical border dimensions
    borderWidth: 2,
    borderColor: '#E5E7EB', // Lighter border color for disabled look
    borderRadius: 16,

    // Maintain identical shadow properties but make them lighter
    shadowColor: '#E5E7EB',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.08, // Reduced from 0.15
    shadowRadius: 8,
    elevation: 2, // Reduced from 5

    // Visual indication it's disabled with overlay
    opacity: 0.6,
  },
  skillIcon: {
    width: 36,
    height: 36,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  skillContent: {
    flex: 1,
    marginRight: 12,
  },
  skillTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  skillTitleDisabled: {
    color: '#9CA3AF',
  },
  skillDescription: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
  },
  skillDescriptionDisabled: {
    color: '#9CA3AF',
  },
  checkMark: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#FF8C42',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'absolute',
    right: 16,
    top: 16,
  },
  buttonSection: {
    paddingHorizontal: 24,
    paddingTop: 16,
    paddingBottom: 16,
    backgroundColor: 'transparent',
  },
  completeButton: {
    width: '100%',
  },
});