import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert, TouchableOpacity, Animated } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { StatusBar } from 'expo-status-bar';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { OnboardingHeader } from '../../components/onboarding/OnboardingHeader';
import { GradientButton } from '../../components/onboarding/GradientButton';
import { WheelDatePicker } from '../../components/onboarding/WheelDatePicker';
import { useOnboardingStore } from '../../stores/onboardingStore';
import { AnimatedContainer } from '../../components/animations/AnimatedContainer';

// Fun and sassy age-specific messages
const AGE_MESSAGES: Record<number, string> = {
  // Nonsense ages for fun
  [-1]: "Congratulations time traveler! You need to be born first before learning to flirt! ⏰",
  0: "Goo goo ga ga? More like 'come back in 18 years!' Fresh out the womb charm! 👶",
  1: "First steps, first words... first pickup lines come much later, little one! 🚼",
  2: "Terrible twos include terrible conversation skills - wait about 16 more years! 😤",
  3: "Preschool playground game strong, but adult conversation game needs time! 🎪",
  4: "Kindergarten social skills unlocked! Only 14 more years until advanced training! 📖",
  5: "Elementary charm detected! Keep practicing with juice boxes for now! 🧃",
  6: "Lost your first tooth but not ready to lose your conversation training virginity! 🦷",
  7: "Seven-year-old sass is real, but conversation mastery requires more birthdays! 💫",
  8: "Third grade confidence peaks! Save some of that energy for when you're legal! 🎯",
  9: "Almost double digits! Still single digits away from conversation boot camp though! 🔢",

  // Under 18 messages (sassy but clear about age requirement)
  10: "Double digits unlocked! Now unlock 8 more years until conversation mastery! 🌟",
  11: "Eleven and heaven... ly patient you'll need to be until conversation training! ✨",
  12: "Middle school drama queen/king energy! Channel that into waiting 6 more years! 📚",
  13: "Sliding into DMs like a pro already? Hold that energy for a few more years! 📱",
  14: "Confidence is building, but conversation skills training starts at 18! 😬✨",
  15: "Almost ready to drive... and almost ready for advanced social skills practice! 🚗",
  16: "Sweet sixteen and ready to charm? Save that energy for when you hit 18! 🎂",
  17: "Senior year confidence boost incoming! One more year until conversation mastery begins! 🎓",

  // 18-30 specific messages
  18: "Fresh adult energy! Time to turn that natural confidence into conversation gold! 🗳️",
  19: "College social scene or real world - either way, conversation skills are everything! 🎒",
  20: "Peak social years ahead! Perfect time to polish those natural conversation talents! 🤷‍♀️",
  21: "Legal everywhere and socially fearless? Let's channel that energy into smooth talking! 🍻",
  22: "Everything's fine and your conversation game can be too! Time to level up! 🎵",
  23: "Dating apps love confidence - let's make sure your conversation skills match! 😅",
  24: "Real world socializing hits different - good thing conversation skills are learnable! 💪",
  25: "Quarter-century wisdom meets fresh conversation techniques - perfect combo! 🎯",
  26: "Adulting is optional, but smooth conversation skills are essential! 💬",
  27: "Wisdom is setting in - time to let your conversation skills catch up! 🛏️",
  28: "Almost thirty means almost peak confidence - let's perfect that chat game! 🎭",
  29: "Last year of twenty-something spontaneity - make every conversation count! ⏰",
  30: "Dirty thirty energy! Confidence is high, now let's make conversation skills match! 🎉"
};

// Age range messages for 31+ (randomized within each 5-year range)
const AGE_RANGE_MESSAGES: Record<string, string[]> = {
  "31-35": [
    "Life experience meets fresh conversation techniques - what a powerful combination! 🏠",
    "Social circles are shifting, but great conversation skills work everywhere! 💒",
    "Confidence levels rising - perfect time to master the art of meaningful chat! 📈",
    "Quality over quantity in everything, including conversations - let's perfect yours! 🍽️",
    "Maturity with a playful edge - the recipe for unforgettable conversations! 🪴"
  ],
  "36-40": [
    "Confidence is peaking - time to let your conversation skills shine just as bright! 💪",
    "Life's full, but there's always room for better social connections! 👑",
    "You've got wisdom and charm - let's make sure everyone gets to experience both! 😂",
    "Experience is your superpower - time to use it in every conversation! 🍷",
    "Cross-generational appeal is real - master conversations with everyone! 📱"
  ],
  "41-45": [
    "Authentic confidence unlocked - perfect foundation for genuine conversations! ✨",
    "Your stories are getting better, now let's perfect how you tell them! 📸",
    "Self-awareness plus social skills equals magnetic conversation abilities! 🧴",
    "Professional success meets personal charm - time to showcase both! 💼",
    "You bridge generations - perfect time to master conversation with all of them! 📚"
  ],
  "46-50": [
    "Life's complexities make you an incredible conversationalist - let's prove it! 🎭",
    "Cool factor confirmed - now let's add smooth conversation skills to the mix! 😎",
    "Authenticity is your brand - make sure every conversation reflects that! 💁‍♀️",
    "Decades of stories and wisdom - perfect ingredients for captivating conversations! 🌙",
    "Adventure and sophistication combined - your conversation game should match! ✈️"
  ],
  "51+": [
    "Sharp wit and zero patience for small talk - let's make every conversation count! 🍾",
    "Experience has sharpened everything, especially your ability to connect with others! 🎯",
    "Multi-generational charm is your specialty - time to perfect those conversation skills! 🪄",
    "Rules are suggestions at this point - including boring conversation conventions! 💃",
    "Confidence, wisdom, and style - the trifecta of great conversation partners! 👗"
  ]
};

export default function AgeVerificationScreen() {
  const {
    formData,
    progress,
    updateFormData,
    setCurrentStepById,
    nextStep,
    previousStep,
  } = useOnboardingStore();

  const [selectedDate, setSelectedDate] = useState<Date | undefined>(formData.birthDate);
  const [error, setError] = useState<string>('');
  const [isNavigating, setIsNavigating] = useState(false);
  const [ageMessage, setAgeMessage] = useState<string>('');
  const [yearAdjusted, setYearAdjusted] = useState<boolean>(false);
  const fadeAnim = useState(new Animated.Value(0))[0];
  const slideAnim = useState(new Animated.Value(20))[0];
  const insets = useSafeAreaInsets();

  // Set age message when year is adjusted and date is selected
  useEffect(() => {
    if (selectedDate && yearAdjusted) {
      const age = calculateAge(selectedDate);
      const message = getAgeMessage(age);
      setAgeMessage(message);

      // Animate in the age message box
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start();
    }
  }, [selectedDate, yearAdjusted, fadeAnim, slideAnim]);

  const calculateAge = (birthDate: Date): number => {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }

    return age;
  };

  const getAgeMessage = (age: number): string => {
    // For specific ages with individual messages (13-30)
    if (AGE_MESSAGES[age]) {
      return AGE_MESSAGES[age];
    }

    // For age ranges 31+, use randomized messages within the range
    if (age >= 31) {
      let rangeKey: string;

      if (age >= 31 && age <= 35) {
        rangeKey = "31-35";
      } else if (age >= 36 && age <= 40) {
        rangeKey = "36-40";
      } else if (age >= 41 && age <= 45) {
        rangeKey = "41-45";
      } else if (age >= 46 && age <= 50) {
        rangeKey = "46-50";
      } else {
        rangeKey = "51+";
      }

      const messages = AGE_RANGE_MESSAGES[rangeKey];
      const randomIndex = Math.floor(Math.random() * messages.length);
      return messages[randomIndex];
    }

    // Fallback for ages not covered (under 13, etc.)
    return "Please verify you are 18 or older to continue.";
  };

  const handleDateChange = (date: Date) => {
    setSelectedDate(date);
    setError('');
    updateFormData({ birthDate: date });
  };

  // Validation function to check if form is complete and valid
  const isFormValid = () => {
    if (!selectedDate) return false;
    const age = calculateAge(selectedDate);
    return age >= 18;
  };

  const handleContinue = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    if (!selectedDate) {
      setError('Please select your birth date');
      return;
    }

    const age = calculateAge(selectedDate);

    if (age < 18) {
      Alert.alert(
        'Age Requirement',
        'You must be at least 18 years old to use FlirtCraft.',
        [{ text: 'OK' }]
      );
      return;
    }

    setIsNavigating(true);

    // Update form data with age verification
    updateFormData({
      birthDate: selectedDate,
      ageVerified: true,
    });

    // Navigate to registration
    nextStep();
    router.push('/onboarding/register');
  };

  const handleBack = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    setIsNavigating(true);
    previousStep();
    router.push('/onboarding/welcome');
  };

  // Maximum date is 18 years ago
  const maxDate = new Date();
  maxDate.setFullYear(maxDate.getFullYear() - 18);

  // Minimum date is 100 years ago (reasonable limit)
  const minDate = new Date();
  minDate.setFullYear(minDate.getFullYear() - 100);

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
        title="Age Check"
        onBackPress={handleBack}
        rightIcon={{
          name: 'shield-checkmark',
          type: 'ionicons',
          color: '#FA7215',
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
              <Ionicons name="shield-checkmark" size={56} color="#FA7215" />
            </View>
            <Text style={styles.title}>Age Verification Required</Text>
            <Text style={styles.description}>
              You must be 18 or older to use FlirtCraft.
              Please verify your age to continue.
            </Text>
          </View>
        </AnimatedContainer>

        <View style={styles.inputSection}>
          <WheelDatePicker
            value={selectedDate}
            onChange={handleDateChange}
            onYearAdjusted={() => setYearAdjusted(true)}
            placeholder="15 Jun 2008"
            maximumDate={maxDate}
            minimumDate={minDate}
            error={error}
          />

          {/* Age Message Display - Show when year is adjusted */}
          {selectedDate && yearAdjusted && (
            <Animated.View
              style={[
                styles.ageMessageContainer,
                {
                  opacity: fadeAnim,
                  transform: [{ translateY: slideAnim }],
                }
              ]}
            >
              <Animated.View style={[
                styles.ageMessageCard,
                calculateAge(selectedDate) < 18 && styles.ageMessageCardWarning,
                { opacity: fadeAnim }
              ]}>
                <Text style={[
                  styles.ageNumberText,
                  calculateAge(selectedDate) < 18 && styles.ageNumberTextWarning
                ]}>
                  You are {calculateAge(selectedDate)} years old
                </Text>
                {ageMessage && (
                  <Text style={[
                    styles.ageMessageText,
                    calculateAge(selectedDate) < 18 && styles.ageMessageTextWarning
                  ]}>
                    {ageMessage}
                  </Text>
                )}
              </Animated.View>
            </Animated.View>
          )}
        </View>
      </ScrollView>

      <AnimatedContainer animation="fadeSlideUp" delay={250}>
        <View style={styles.buttonSection}>
          <GradientButton
            title="Verify Age & Continue"
            onPress={handleContinue}
            disabled={!isFormValid()}
            style={styles.continueButton}
          />
        </View>
      </AnimatedContainer>
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
    paddingTop: 0,
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
    color: '#1f2937',
    marginBottom: 12,
    textAlign: 'center',
  },
  description: {
    fontSize: 16,
    color: '#6b7280',
    lineHeight: 24,
    textAlign: 'center',
    paddingHorizontal: 8,
  },
  inputSection: {
    marginBottom: 24,
  },
  ageMessageContainer: {
    marginTop: 16,
  },
  ageMessageCard: {
    backgroundColor: '#FFF5F0',
    borderWidth: 2,
    borderColor: '#FF8C42',
    borderRadius: 16,
    paddingHorizontal: 16,
    paddingVertical: 16,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  ageMessageCardWarning: {
    backgroundColor: '#FEF2F2',
    borderColor: '#F87171',
    borderWidth: 2,
    shadowColor: '#F87171',
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  ageNumberText: {
    fontSize: 16,
    color: '#FF6B35',
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 8,
  },
  ageMessageText: {
    fontSize: 14,
    lineHeight: 20,
    color: '#6B7280',
    fontWeight: '500',
    textAlign: 'center',
  },
  ageMessageTextWarning: {
    color: '#DC2626',
  },
  ageNumberTextWarning: {
    color: '#DC2626',
  },
  infoSection: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#F3F4F6',
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  infoText: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
    marginBottom: 8,
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