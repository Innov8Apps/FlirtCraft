import React, { useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Dimensions,
  Image,
  TouchableOpacity,
} from 'react-native';
import Animated, {
  FadeIn,
  SlideInUp,
  ZoomIn,
  useAnimatedStyle,
  useSharedValue,
  withSpring,
  withDelay
} from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import OnboardingButton from '@/components/onboarding/OnboardingButton';
import { OnboardingStepProps } from '../types';
import { useRouter } from 'expo-router';

const { width } = Dimensions.get('window');

interface BenefitCardProps {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  description: string;
  delay: number;
}

const BenefitCard: React.FC<BenefitCardProps> = ({ icon, title, description, delay }) => {
  return (
    <Animated.View
      entering={FadeIn.delay(delay).duration(400)}
      style={styles.benefitCard}
    >
      <View style={styles.benefitIconContainer}>
        <Ionicons name={icon} size={24} color="#FF6B35" />
      </View>
      <View style={styles.benefitContent}>
        <Text style={styles.benefitTitle}>{title}</Text>
        <Text style={styles.benefitDescription}>{description}</Text>
      </View>
    </Animated.View>
  );
};

export default function WelcomeScreen({ onNext }: OnboardingStepProps) {
  const router = useRouter();

  const navigateToSignIn = () => {
    router.push('/signin');
  };

  const benefits = [
    {
      icon: 'chatbubble-outline' as keyof typeof Ionicons.glyphMap,
      title: 'Practice Safely',
      description: 'Build confidence in a judgment-free environment',
    },
    {
      icon: 'people-outline' as keyof typeof Ionicons.glyphMap,
      title: 'Realistic Scenarios',
      description: 'Experience conversations that feel natural',
    },
    {
      icon: 'trending-up-outline' as keyof typeof Ionicons.glyphMap,
      title: 'Track Progress',
      description: 'See your skills improve with detailed feedback',
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
          {/* Logo Section */}
          <Animated.View
            entering={FadeIn.delay(100).duration(500)}
            style={styles.logoContainer}
          >
            <View style={styles.logoPlaceholder}>
              <Ionicons name="heart" size={48} color="#FF6B35" />
            </View>
          </Animated.View>

          {/* Main Content */}
          <Animated.View
            entering={FadeIn.delay(300).duration(600)}
            style={styles.mainContent}
          >
            <Text style={styles.headline}>
              Welcome to FlirtCraft
            </Text>
            <Text style={styles.subheadline}>
              Practice conversations. Build confidence. Find connections.
            </Text>
            <Text style={styles.supportingText}>
              Free to try • No awkward real people • Private practice
            </Text>
          </Animated.View>

          {/* Benefits Section */}
          <View style={styles.benefitsContainer}>
            {benefits.map((benefit, index) => (
              <BenefitCard
                key={benefit.title}
                icon={benefit.icon}
                title={benefit.title}
                description={benefit.description}
                delay={500 + index * 100}
              />
            ))}
          </View>

          {/* CTA Section */}
          <Animated.View
            entering={FadeIn.delay(800).duration(400)}
            style={styles.ctaContainer}
          >
            <OnboardingButton
              title="Start Building Confidence"
              onPress={onNext}
              accessibilityLabel="Get started with FlirtCraft"
              accessibilityHint="Begin the onboarding process"
            />

            <TouchableOpacity
              onPress={navigateToSignIn}
              style={styles.signInButton}
            >
              <Text style={styles.signInButtonText}>
                Already have an account? Sign In
              </Text>
            </TouchableOpacity>
          </Animated.View>

          {/* Legal Footer */}
          <Animated.View
            entering={FadeIn.delay(900).duration(400)}
            style={styles.legalFooter}
          >
            <Text style={styles.legalText}>
              By continuing, you agree to our Terms of Service and Privacy Policy
            </Text>
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
    alignItems: 'center',
  },
  logoContainer: {
    marginBottom: 48,
    marginTop: 32,
  },
  logoPlaceholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#FFF7F4',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FDBA8C',
  },
  mainContent: {
    alignItems: 'center',
    marginBottom: 48,
  },
  headline: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1A1A1A',
    textAlign: 'center',
    marginBottom: 16,
  },
  subheadline: {
    fontSize: 18,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 12,
    maxWidth: width - 80,
  },
  supportingText: {
    fontSize: 14,
    color: '#FF7F50',
    textAlign: 'center',
    fontWeight: '500',
  },
  benefitsContainer: {
    width: '100%',
    marginBottom: 48,
  },
  benefitCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 3,
  },
  benefitIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#FFF7F4',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  benefitContent: {
    flex: 1,
  },
  benefitTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  benefitDescription: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  ctaContainer: {
    width: '100%',
    marginBottom: 24,
  },
  legalFooter: {
    paddingHorizontal: 16,
  },
  legalText: {
    fontSize: 12,
    color: '#9CA3AF',
    textAlign: 'center',
    lineHeight: 16,
  },
  signInButton: {
    marginTop: 16,
    alignItems: 'center',
    paddingVertical: 12,
  },
  signInButtonText: {
    fontSize: 16,
    color: '#FF6B35',
    fontWeight: '500',
  },
});