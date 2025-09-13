import React, { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, ScrollView, Image, Dimensions, Animated, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, Feather } from '@expo/vector-icons';
import { GradientButton } from '../../components/onboarding/GradientButton';
import { useOnboardingStore } from '../../stores/onboardingStore';
import { AnimatedContainer, StaggeredContainer } from '../../components/animations/AnimatedContainer';

const { width: screenWidth } = Dimensions.get('window');

export default function WelcomeScreen() {
  const insets = useSafeAreaInsets();
  const { startOnboarding, setCurrentStepById, nextStep } = useOnboardingStore();
  const [isNavigating, setIsNavigating] = useState(false);
  
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const rotatingWords = ['Game', 'Charm', 'Rizz', 'Vibe'];
  const opacityAnim = useRef(new Animated.Value(1)).current;
  const translateYAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Initialize onboarding when welcome screen loads
    startOnboarding();
    setCurrentStepById('welcome');
  }, [startOnboarding, setCurrentStepById]);

  useEffect(() => {
    const animateWords = () => {
      // Start fade out and slide down animation
      Animated.parallel([
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(translateYAnim, {
          toValue: 20,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start(() => {
        // Change word while invisible
        setCurrentWordIndex((prevIndex) => (prevIndex + 1) % rotatingWords.length);

        // Reset position for slide up effect
        translateYAnim.setValue(-20);

        // Start fade in and slide up animation
        Animated.parallel([
          Animated.timing(opacityAnim, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(translateYAnim, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ]).start();
      });
    };

    const interval = setInterval(animateWords, 2500);
    return () => clearInterval(interval);
  }, [opacityAnim, translateYAnim, rotatingWords.length]);

  const handleGetStarted = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    setIsNavigating(true);
    nextStep();
    router.push('/onboarding/age-verification');
  };

  const handleLogin = () => {
    router.push('/auth/login');
  };

  return (
    <View style={styles.outerContainer}>
      <StatusBar style="dark" />
      <LinearGradient
        colors={['#FFF6F0', '#FFFAF6', '#FFFFFF']}
        locations={[0, 0.4, 1]}
        style={styles.container}
      >
        <View
          style={[
            styles.content,
            { paddingTop: insets.top + 32 }
          ]}
        >
          {/* Logo/Hero Section */}
          <AnimatedContainer animation="fadeSlideUp" delay={50}>
            <View style={styles.heroSection}>
              <View style={styles.iconContainer}>
                <Ionicons name="chatbubbles" size={56} color="#FA7215" />
              </View>
              <View style={styles.titleContainer}>
                <View style={styles.baselineContainer}>
                  <Text style={styles.title}>Level Up Your </Text>
                  <Text style={[styles.title, styles.invisibleBaseline]}>Game</Text>
                </View>
                <View style={styles.animatedWordContainer}>
                  <Text style={[styles.title, styles.invisibleSpacer]}>Level Up Your </Text>
                  <Animated.Text
                    style={[
                      styles.title,
                      styles.rotatingTitle,
                      {
                        opacity: opacityAnim,
                        transform: [{ translateY: translateYAnim }]
                      }
                    ]}
                  >
                    {rotatingWords[currentWordIndex]}
                  </Animated.Text>
                </View>
              </View>
              <Text style={styles.subtitle}>
                Train with AI that actually knows how to turn conversations into chemistry
              </Text>
            </View>
          </AnimatedContainer>

          {/* Features Section */}
          <StaggeredContainer
            baseDelay={120}
            staggerDelay={40}
            animation="fadeSlideUp"
            containerStyle={styles.featuresSection}
          >
            <FeatureCard
              icon="chatbubbles"
              iconType="ionicons"
              title="Smooth Talking, Risk-Free"
              description="Practice your charm with AI that's here to help, not judge"
            />
            <FeatureCard
              icon="trending-up"
              iconType="ionicons"
              title="From Awkward to Magnetic"
              description="Watch yourself evolve from 'um, hi' to 'well, hello there'"
            />
            <FeatureCard
              icon="target"
              iconType="feather"
              title="Your Best Self, Unleashed"
              description="AI coaching that brings out your inner charm (yes, it's there)"
            />
          </StaggeredContainer>

        </View>

        <AnimatedContainer animation="fadeSlideUp" delay={300}>
          <View style={styles.buttonSection}>
            <GradientButton
              title="Get Started"
              onPress={handleGetStarted}
              style={styles.getStartedButton}
            />

            <TouchableOpacity
              style={styles.loginButton}
              onPress={handleLogin}
              activeOpacity={0.7}
            >
              <Text style={styles.loginButtonText}>Log In</Text>
            </TouchableOpacity>
          </View>
        </AnimatedContainer>
      </LinearGradient>
    </View>
  );
}

interface FeatureItemProps {
  icon: string;
  iconType: 'ionicons' | 'feather';
  title: string;
  description: string;
}

const FeatureCard: React.FC<FeatureItemProps> = ({ icon, iconType, title, description }) => {
  const renderIcon = () => {
    const iconProps = {
      name: icon as any,
      size: 28,
      color: '#FF8C42',
    };

    if (iconType === 'feather') {
      return <Feather {...iconProps} />;
    }
    return <Ionicons {...iconProps} />;
  };

  return (
    <View style={styles.featureCard}>
      <View style={styles.featureIconContainer}>
        {renderIcon()}
      </View>
      <View style={styles.featureContent}>
        <Text style={styles.featureTitle}>{title}</Text>
        <Text style={styles.featureDescription}>{description}</Text>
      </View>
    </View>
  );
};

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
    paddingHorizontal: 24,
  },
  heroSection: {
    alignItems: 'center',
    paddingTop: 32,
    paddingBottom: 24,
  },
  iconContainer: {
    marginBottom: 12,
  },
  titleContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  baselineContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  invisibleBaseline: {
    opacity: 0,
  },
  animatedWordContainer: {
    position: 'absolute',
    flexDirection: 'row',
    alignItems: 'center',
    left: 0,
    top: 0,
  },
  invisibleSpacer: {
    opacity: 0,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    textAlign: 'center',
  },
  rotatingTitle: {
    color: '#FF6B35',
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    lineHeight: 24,
    textAlign: 'center',
    paddingHorizontal: 8,
    marginBottom: 20,
  },
  featuresSection: {
    paddingBottom: 16,
  },
  featureCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 12,
    padding: 20,
    marginBottom: 14,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  featureIconContainer: {
    width: 32,
    height: 32,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 15,
    color: '#6b7280',
    lineHeight: 21,
  },
  buttonSection: {
    paddingHorizontal: 24,
    paddingTop: 16,
    paddingBottom: 32,
    backgroundColor: 'transparent',
  },
  getStartedButton: {
    width: '100%',
    marginBottom: 10,
  },
  loginButton: {
    width: '100%',
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#FF6B35',
    borderRadius: 16,
    paddingHorizontal: 30,
    paddingVertical: 14,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 52,
  },
  loginButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FF6B35',
    textAlign: 'center',
  },
});