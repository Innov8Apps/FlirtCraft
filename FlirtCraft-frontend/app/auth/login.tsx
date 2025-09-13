import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Platform,
  Animated
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { StatusBar } from 'expo-status-bar';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useForm, Controller } from 'react-hook-form';
import { GradientButton } from '../../components/onboarding/GradientButton';
import { authService } from '../../services/supabase';
import { useError } from '../../lib/contexts/ErrorContext';
import { loginRateLimitService } from '../../lib/services/loginRateLimitService';
import { AnimatedContainer } from '../../components/animations/AnimatedContainer';

interface LoginFormData {
  email: string;
  password: string;
}

export default function LoginScreen() {
  const { showError, dismissErrorOnNavigation } = useError();
  const insets = useSafeAreaInsets();

  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isNavigating, setIsNavigating] = useState(false);
  const [isProcessingSubmit, setIsProcessingSubmit] = useState(false);

  // Carousel animation states
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const rotatingWords = ['Game', 'Charm', 'Rizz', 'Flow'];
  const opacityAnim = useRef(new Animated.Value(1)).current;
  const translateYAnim = useRef(new Animated.Value(0)).current;

  // Rate limiting states
  const [isInCooldown, setIsInCooldown] = useState(false);
  const [countdownSeconds, setCountdownSeconds] = useState(0);
  const countdownCleanupRef = useRef<(() => void) | null>(null);

  const {
    control,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm<LoginFormData>({
    defaultValues: {
      email: '',
      password: '',
    }
  });

  const watchedEmail = watch('email');
  const watchedPassword = watch('password');

  // Check rate limit status on component mount
  useEffect(() => {
    const checkRateLimitStatus = async () => {
      const status = await loginRateLimitService.getRateLimitStatus();
      setIsInCooldown(status.isInCooldown);
      setCountdownSeconds(status.countdownSeconds);

      if (status.isInCooldown) {
        startCountdownTimer();
      }
    };

    checkRateLimitStatus();

    // Cleanup countdown on unmount
    return () => {
      if (countdownCleanupRef.current) {
        countdownCleanupRef.current();
      }
    };
  }, []);

  // Carousel animation effect
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

  // Start countdown timer
  const startCountdownTimer = () => {
    // Clear any existing timer
    if (countdownCleanupRef.current) {
      countdownCleanupRef.current();
    }

    countdownCleanupRef.current = loginRateLimitService.startCountdownTimer(
      (secondsRemaining) => {
        setCountdownSeconds(secondsRemaining);
      },
      () => {
        setIsInCooldown(false);
        setCountdownSeconds(0);
        countdownCleanupRef.current = null;
      }
    );
  };

  // Helper function to check if field is valid
  const isFieldValid = (fieldName: keyof LoginFormData, value: string) => {
    switch (fieldName) {
      case 'email':
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(value);
      case 'password':
        return value && value.length > 0;
      default:
        return false;
    }
  };

  // Complete form validation
  const isFormValid = () => {
    // Check if in cooldown or processing
    if (isInCooldown || isProcessingSubmit) {
      return false;
    }

    // Check email validity
    const emailValid = watchedEmail &&
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(watchedEmail) &&
      !errors.email;

    // Check password validity
    const passwordValid = watchedPassword && watchedPassword.length > 0 && !errors.password;

    // Check for any form errors
    const noFormErrors = !Object.keys(errors).length;

    return emailValid && passwordValid && noFormErrors;
  };

  const onSubmit = async (data: LoginFormData) => {
    if (isNavigating || isProcessingSubmit) return; // Prevent multiple rapid taps

    // Dismiss any existing error notifications
    dismissErrorOnNavigation();

    setIsProcessingSubmit(true);
    setIsLoading(true);

    try {
      // Check rate limit before proceeding
      const isAllowed = await loginRateLimitService.isActionAllowed();
      if (!isAllowed) {
        setIsProcessingSubmit(false);
        setIsLoading(false);
        const message = await loginRateLimitService.getRateLimitMessage();
        showError(message, 'warning', 20000);
        return;
      }

      // Additional validation with user-friendly error messages
      if (!data.email || !data.password) {
        setIsProcessingSubmit(false);
        setIsLoading(false);
        showError('Please enter both email and password', 'warning');
        return;
      }

      // Attempt to sign in
      const result = await authService.signIn(
        data.email.trim().toLowerCase(),
        data.password
      );

      if (!result.success) {
        // Track failed attempt for rate limiting
        await loginRateLimitService.trackFailedAttempt();

        // Check rate limit status after tracking the attempt
        const status = await loginRateLimitService.getRateLimitStatus();
        setIsInCooldown(status.isInCooldown);
        setCountdownSeconds(status.countdownSeconds);

        // Show login failed error
        showError(result.error || 'Invalid email or password. Please try again.', 'error');

        // Only show rate limit message and start timer if now in cooldown (after 5 attempts)
        if (status.isInCooldown) {
          startCountdownTimer();
          const rateLimitMessage = await loginRateLimitService.getRateLimitMessage();
          showError(rateLimitMessage, 'warning', 20000);
        }

        setIsProcessingSubmit(false);
        setIsLoading(false);
        return;
      }

      // Clear rate limit on successful login
      await loginRateLimitService.resetRateLimit();
      setIsInCooldown(false);
      setCountdownSeconds(0);

      // Navigate to main app
      setIsNavigating(true);
      router.replace('/main');

    } catch (error) {
      console.error('Login error:', error);
      showError('Something went wrong. Please try again.', 'error');
      setIsProcessingSubmit(false);
      setIsLoading(false);
    }
  };


  const handleForgotPassword = () => {
    showError('Password reset functionality will be available soon. Please contact support if you need help.', 'info', 8000);
  };

  const handleGoogleLogin = () => {
    showError('Google login coming soon! We\'re working on integrating this feature.', 'info', 5000);
  };

  const handleAppleLogin = () => {
    showError('Apple login coming soon! We\'re working on integrating this feature.', 'info', 5000);
  };

  return (
    <View style={styles.outerContainer}>
      <StatusBar style="dark" />
      <LinearGradient
        colors={['#FFF6F0', '#FFFAF6', '#FFFFFF']}
        locations={[0, 0.4, 1]}
        style={styles.container}
      >

        <ScrollView
          style={styles.content}
          contentContainerStyle={[styles.contentContainer, { paddingTop: insets.top + 40 }]}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          <AnimatedContainer animation="fadeSlideUp" delay={40}>
            <View style={styles.textSection}>
              <View style={styles.titleIcon}>
                <Ionicons name="log-in" size={56} color="#FA7215" />
              </View>
              <View style={styles.titleContainer}>
                <View style={styles.baselineContainer}>
                  <Text style={styles.title}>Time to Flex Your </Text>
                  <Text style={[styles.title, styles.invisibleBaseline]}>Game</Text>
                </View>
                <View style={styles.animatedWordContainer}>
                  <Text style={[styles.title, styles.invisibleSpacer]}>Time to Flex Your </Text>
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

              {/* Social Login Buttons */}
              <View style={styles.socialLoginSection}>
                <TouchableOpacity
                  style={styles.googleButton}
                  onPress={handleGoogleLogin}
                  activeOpacity={0.8}
                >
                  <View style={styles.socialButtonContent}>
                    <View style={styles.googleIconContainer}>
                      <Ionicons name="logo-google" size={20} color="#FF6B35" />
                    </View>
                    <Text style={styles.googleButtonText}>Continue with Google</Text>
                  </View>
                </TouchableOpacity>

                {Platform.OS === 'ios' && (
                  <TouchableOpacity
                    style={styles.appleButton}
                    onPress={handleAppleLogin}
                    activeOpacity={0.8}
                  >
                    <View style={styles.socialButtonContent}>
                      <View style={styles.appleIconContainer}>
                        <Ionicons name="logo-apple" size={20} color="#FFFFFF" />
                      </View>
                      <Text style={styles.appleButtonText}>Continue with Apple</Text>
                    </View>
                  </TouchableOpacity>
                )}
              </View>

              {/* OR Divider */}
              <View style={styles.dividerContainer}>
                <View style={styles.dividerLine} />
                <Text style={styles.dividerText}>OR</Text>
                <View style={styles.dividerLine} />
              </View>
            </View>

            <View style={styles.formSection}>
              {/* Email Field */}
              <View style={styles.inputGroup}>
                <Text style={styles.label}>Email Address</Text>
                <View style={styles.inputContainer}>
                  <Controller
                    control={control}
                    name="email"
                    rules={{
                      required: 'Email is required',
                      pattern: {
                        value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                        message: 'Enter a valid email address'
                      }
                    }}
                    render={({ field: { onChange, onBlur, value } }) => (
                      <>
                        <View style={styles.iconContainer}>
                          <Ionicons name="mail" size={20} color="#FF6B35" />
                        </View>
                        <TextInput
                          style={[
                            styles.textInput,
                            styles.textInputWithIcon,
                            errors.email && styles.textInputError,
                            !errors.email && isFieldValid('email', value) && styles.textInputValid,
                          ]}
                          value={value}
                          onChangeText={onChange}
                          onBlur={onBlur}
                          placeholder="your.email@example.com"
                          placeholderTextColor="#9CA3AF"
                          keyboardType="email-address"
                          autoCapitalize="none"
                          autoComplete="email"
                        />
                      </>
                    )}
                  />
                </View>
                {errors.email && (
                  <Text style={styles.errorText}>{errors.email.message}</Text>
                )}
              </View>

              {/* Password Field */}
              <View style={styles.inputGroup}>
                <Text style={styles.label}>Password</Text>
                <View style={styles.inputContainer}>
                  <Controller
                    control={control}
                    name="password"
                    rules={{
                      required: 'Password is required',
                    }}
                    render={({ field: { onChange, onBlur, value } }) => (
                      <>
                        <View style={styles.iconContainer}>
                          <Ionicons name="lock-closed" size={20} color="#FF6B35" />
                        </View>
                        <TextInput
                          style={[
                            styles.textInput,
                            styles.textInputWithIcon,
                            styles.passwordInput,
                            errors.password && styles.textInputError,
                            !errors.password && isFieldValid('password', value) && styles.textInputValid,
                          ]}
                          value={value}
                          onChangeText={onChange}
                          onBlur={onBlur}
                          placeholder="Enter your password"
                          placeholderTextColor="#9CA3AF"
                          secureTextEntry={!showPassword}
                          autoComplete="current-password"
                        />
                        <TouchableOpacity
                          style={styles.eyeButton}
                          onPress={() => setShowPassword(!showPassword)}
                        >
                          <Ionicons
                            name={showPassword ? 'eye-off' : 'eye'}
                            size={20}
                            color="#FF6B35"
                          />
                        </TouchableOpacity>
                      </>
                    )}
                  />
                </View>
                {errors.password && (
                  <Text style={styles.errorText}>{errors.password.message}</Text>
                )}
              </View>

              {/* Forgot Password */}
              <TouchableOpacity
                onPress={handleForgotPassword}
                style={styles.forgotPasswordContainer}
              >
                <Text style={styles.forgotPasswordText}>
                  Forgot your password?
                </Text>
              </TouchableOpacity>
            </View>
          </AnimatedContainer>
        </ScrollView>

        <View style={styles.buttonSection}>
          <GradientButton
            title={isInCooldown
              ? `Wait ${Math.floor(countdownSeconds / 60)}:${(countdownSeconds % 60).toString().padStart(2, '0')}`
              : "Sign In"
            }
            onPress={handleSubmit(onSubmit)}
            loading={isLoading}
            disabled={!isFormValid() || isLoading || isInCooldown || isProcessingSubmit}
            cooldown={isInCooldown}
            style={styles.signInButton}
          />

          <TouchableOpacity
            style={styles.createAccountButton}
            onPress={() => {
              dismissErrorOnNavigation();
              router.push('/onboarding/welcome');
            }}
            activeOpacity={0.7}
          >
            <Text style={styles.createAccountButtonText}>Create Account</Text>
          </TouchableOpacity>
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
    flexGrow: 1,
    paddingHorizontal: 24,
    paddingTop: 8,
  },
  textSection: {
    alignItems: 'center',
    paddingTop: 8,
    marginBottom: 24,
  },
  socialLoginSection: {
    width: '100%',
    marginTop: 20,
    marginBottom: 2,
  },
  googleButton: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#E5E7EB',
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  appleButton: {
    backgroundColor: '#000000',
    borderWidth: 2,
    borderColor: '#000000',
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  socialButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 20,
    minHeight: 52,
  },
  googleIconContainer: {
    marginRight: 12,
  },
  appleIconContainer: {
    marginRight: 12,
  },
  googleButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
    textAlign: 'center',
  },
  appleButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    textAlign: 'center',
  },
  dividerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 4,
    paddingHorizontal: 16,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: '#E5E7EB',
  },
  dividerText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#9CA3AF',
    marginHorizontal: 16,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 8,
  },
  titleIcon: {
    marginBottom: 12,
  },
  iconContainer: {
    position: 'absolute',
    left: 16,
    top: '50%',
    marginTop: -10,
    width: 20,
    height: 20,
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1,
  },
  titleContainer: {
    alignItems: 'center',
    marginBottom: 12,
    position: 'relative',
  },
  baselineContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    justifyContent: 'flex-start',
  },
  animatedWordContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    justifyContent: 'flex-start',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  invisibleBaseline: {
    opacity: 0,
  },
  invisibleSpacer: {
    opacity: 0,
  },
  rotatingTitle: {
    color: '#FA7215',
  },
  description: {
    fontSize: 16,
    color: '#6b7280',
    lineHeight: 24,
    textAlign: 'center',
    paddingHorizontal: 8,
  },
  formSection: {
    flex: 1,
  },
  inputGroup: {
    marginBottom: 12,
  },
  label: {
    fontSize: 13,
    fontWeight: '500',
    color: '#FF6B35',
    marginBottom: 6,
  },
  textInput: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 15,
    color: '#1f2937',
    minHeight: 48,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  textInputError: {
    borderColor: '#ef4444',
    backgroundColor: '#FFF5F5',
    shadowColor: '#ef4444',
  },
  textInputValid: {
    borderColor: '#FF6B35',
    backgroundColor: '#FFFFFF',
    shadowColor: '#FF6B35',
  },
  inputContainer: {
    position: 'relative',
  },
  textInputWithIcon: {
    paddingLeft: 50,
  },
  passwordInput: {
    paddingRight: 84,
  },
  eyeButton: {
    position: 'absolute',
    right: 16,
    top: '50%',
    marginTop: -10,
    width: 20,
    height: 20,
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1,
  },
  errorText: {
    fontSize: 14,
    color: '#ef4444',
    marginTop: 8,
    marginLeft: 4,
  },
  forgotPasswordContainer: {
    alignItems: 'center',
    marginTop: 4,
  },
  forgotPasswordText: {
    fontSize: 16,
    color: '#FF6B35',
    fontWeight: '500',
  },
  buttonSection: {
    paddingHorizontal: 24,
    paddingTop: 12,
    paddingBottom: 20,
    backgroundColor: 'transparent',
  },
  signInButton: {
    width: '100%',
    marginBottom: 10,
  },
  createAccountButton: {
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
  createAccountButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FF6B35',
    textAlign: 'center',
  },
});