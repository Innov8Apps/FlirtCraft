import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  Alert,
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
import { OnboardingHeader } from '../../components/onboarding/OnboardingHeader';
import { GradientButton } from '../../components/onboarding/GradientButton';
import { PasswordRequirementsChecklist } from '../../components/onboarding/PasswordRequirementsChecklist';
import { useOnboardingStore } from '../../stores/onboardingStore';
import { authService, rateLimitService } from '../../services/supabase';
import { useError } from '../../lib/contexts/ErrorContext';
import { rateLimitService as emailRateLimitService } from '../../lib/services/rateLimitService';
import { AnimatedContainer, StaggeredContainer } from '../../components/animations/AnimatedContainer';

interface RegistrationFormData {
  email: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: boolean;
  agreedToPrivacy: boolean;
}

export default function RegisterScreen() {
  const {
    formData,
    progress,
    updateFormData,
    setCurrentStepById,
    nextStep,
    previousStep,
    setLoading,
    isLoading,
    setError,
    error,
  } = useOnboardingStore();

  const { showError, dismissErrorOnNavigation } = useError();
  const insets = useSafeAreaInsets();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [emailExists, setEmailExists] = useState(false);
  const [isNavigating, setIsNavigating] = useState(false);
  const [showPasswordRequirements, setShowPasswordRequirements] = useState(false);
  const [isProcessingSubmit, setIsProcessingSubmit] = useState(false);
  const termsWiggleAnim = useRef(new Animated.Value(0)).current;
  const privacyWiggleAnim = useRef(new Animated.Value(0)).current;
  const passwordTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Rate limiting states
  const [isInCooldown, setIsInCooldown] = useState(false);
  const [countdownSeconds, setCountdownSeconds] = useState(0);
  const countdownCleanupRef = useRef<(() => void) | null>(null);

  const {
    control,
    handleSubmit,
    watch,
    setValue,
    formState: { errors }
  } = useForm<RegistrationFormData>({
    defaultValues: {
      email: formData.email || '',
      password: formData.password || '',
      confirmPassword: formData.confirmPassword || '',
      agreedToTerms: formData.agreedToTerms || false,
      agreedToPrivacy: formData.agreedToPrivacy || false,
    }
  });

  const watchedPassword = watch('password');
  const watchedEmail = watch('email');
  const watchedConfirmPassword = watch('confirmPassword');
  const watchedAgreedToTerms = watch('agreedToTerms');
  const watchedAgreedToPrivacy = watch('agreedToPrivacy');

  // Check rate limit status on component mount
  useEffect(() => {
    const checkRateLimitStatus = async () => {
      const status = await emailRateLimitService.getRateLimitStatus();
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

  // Start countdown timer
  const startCountdownTimer = () => {
    // Clear any existing timer
    if (countdownCleanupRef.current) {
      countdownCleanupRef.current();
    }

    countdownCleanupRef.current = emailRateLimitService.startCountdownTimer(
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

  // Debounced effect to show password requirements after user stops typing
  useEffect(() => {
    // Clear existing timeout
    if (passwordTimeoutRef.current) {
      clearTimeout(passwordTimeoutRef.current);
    }

    if (watchedPassword && watchedPassword.length > 0) {
      // Set a new timeout to show requirements after 600ms of no typing
      passwordTimeoutRef.current = setTimeout(() => {
        setShowPasswordRequirements(true);
      }, 600);
    } else {
      // Hide requirements immediately if password is empty
      setShowPasswordRequirements(false);
    }

    // Cleanup timeout on unmount or when watchedPassword changes
    return () => {
      if (passwordTimeoutRef.current) {
        clearTimeout(passwordTimeoutRef.current);
      }
    };
  }, [watchedPassword]);

  // Helper function to check if field is valid
  const isFieldValid = (fieldName: keyof RegistrationFormData, value: string) => {
    switch (fieldName) {
      case 'email':
        // Basic email format validation - check for @ and common domain patterns
        const emailPattern = /^[^\s@]+@[^\s@]+\.(com|org|net|edu|gov|mil|co|io|app|dev|tech|info|biz|me|us|uk|ca|au|de|fr|jp|cn|in|br|ru|it|es|mx|nl|se|no|dk|fi|pl|tr|za|ng|eg|ma|gh|ke|tz|ug|zw|zm|mw|bw|sz|ls|na|ao|mz|mg|mu|sc|re|yt|tf|cc|tv|fm|ws|to|nu|tk|pw|mp|gu|as|vi|pr|vg|ai|ms|tc|ky|bm|gd|lc|vc|bb|ag|kn|dm|jm|ht|do|cu|bs|tt|sr|gy|fk|pe|ec|co|ve|bo|py|uy|ar|cl|br|gf|pf|nc|vu|sb|fj|ki|nr|tv|wf|ck|nu|to|tk|pw|fm|mh|mp|gu|as|vi|pr|vg)$/i;
        return emailPattern.test(value);
      case 'password':
        return isPasswordValid(value);
      case 'confirmPassword':
        return value && value === watchedPassword && !errors.confirmPassword;
      default:
        return false;
    }
  };

  // Comprehensive password validation
  const isPasswordValid = (password: string) => {
    if (!password) return false;

    const requirements = [
      password.length >= 8,
      /[A-Z]/.test(password),
      /[a-z]/.test(password),
      /\d/.test(password)
    ];

    return requirements.every(req => req);
  };

  // Complete form validation
  const isFormValid = () => {
    // Check if in cooldown or processing
    if (isInCooldown || isProcessingSubmit) {
      return false;
    }

    // Check email validity (format only, existence will be checked on submit)
    const emailValid = watchedEmail &&
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(watchedEmail) &&
      !errors.email;

    // Check password validity
    const passwordValid = isPasswordValid(watchedPassword);

    // Check confirm password matches
    const confirmPasswordValid = watchedConfirmPassword &&
      watchedConfirmPassword === watchedPassword &&
      !errors.confirmPassword;

    // Check agreements
    const agreementsValid = watchedAgreedToTerms && watchedAgreedToPrivacy;

    // Check for any form errors
    const noFormErrors = !Object.keys(errors).length;

    return emailValid && passwordValid && confirmPasswordValid && agreementsValid && noFormErrors;
  };


  // DISABLED: Real-time email checking removed to prevent information disclosure
  // Email existence is now only checked on form submission
  /*
  const checkEmail = async (email: string) => {
    if (email && email.includes('@')) {
      // Check if we're in cooldown before making API call
      const isAllowed = await emailRateLimitService.isActionAllowed();
      if (!isAllowed) {
        return; // Skip API call if in cooldown
      }

      const result = await authService.checkEmailExists(email);
      if (result.error) {
        // Handle rate limiting or other errors silently
        console.log('Email check error:', result.error);
      } else {
        setEmailExists(result.exists);

        // Track failed attempt if email exists
        if (result.exists) {
          await emailRateLimitService.trackFailedAttempt();

          // Update rate limit state
          const status = await emailRateLimitService.getRateLimitStatus();
          setIsInCooldown(status.isInCooldown);
          setCountdownSeconds(status.countdownSeconds);

          if (status.isInCooldown) {
            startCountdownTimer();

            // Show rate limit message
            const message = await emailRateLimitService.getRateLimitMessage();
            showError(message, 'warning', 20000);
          }
        } else {
          // Reset rate limit on successful email validation (email doesn't exist)
          await emailRateLimitService.resetRateLimit();
          setIsInCooldown(false);
          setCountdownSeconds(0);
        }
      }
    }
  };
  */

  // Wiggle animation function
  const triggerWiggle = (animValue: Animated.Value) => {
    Animated.sequence([
      Animated.timing(animValue, {
        toValue: 10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(animValue, {
        toValue: -10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(animValue, {
        toValue: 10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(animValue, {
        toValue: 0,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const handleGoogleSignUp = () => {
    showError('Google sign-up coming soon! We\'re working on integrating this feature.', 'info', 5000);
  };

  const handleAppleSignUp = () => {
    showError('Apple sign-up coming soon! We\'re working on integrating this feature.', 'info', 5000);
  };

  const onSubmit = async (data: RegistrationFormData) => {
    if (isNavigating || isProcessingSubmit) return; // Prevent multiple rapid taps

    // Dismiss any existing error notifications
    dismissErrorOnNavigation();

    setIsProcessingSubmit(true);

    // Check terms and privacy agreements with wiggle animation
    if (!data.agreedToTerms || !data.agreedToPrivacy) {
      setIsProcessingSubmit(false);
      if (!data.agreedToTerms) {
        triggerWiggle(termsWiggleAnim);
      }
      if (!data.agreedToPrivacy) {
        triggerWiggle(privacyWiggleAnim);
      }
      return;
    }

    // Additional validation with user-friendly error messages
    if (!isPasswordValid(data.password)) {
      setIsProcessingSubmit(false);
      showError('Please ensure your password meets all requirements', 'warning');
      return;
    }

    if (data.password !== data.confirmPassword) {
      setIsProcessingSubmit(false);
      showError('Passwords do not match', 'error');
      return;
    }

    // Check rate limit before proceeding
    const isAllowed = await emailRateLimitService.isActionAllowed();
    if (!isAllowed) {
      setIsProcessingSubmit(false);
      const message = await emailRateLimitService.getRateLimitMessage();
      showError(message, 'warning', 20000);
      return;
    }

    // Check email existence before creating account
    const emailCheck = await authService.checkEmailExists(data.email);
    if (emailCheck.error) {
      setIsProcessingSubmit(false);
      showError('Unable to verify email. Please try again.', 'error');
      return;
    }
    if (emailCheck.exists) {
      setEmailExists(true);

      // Always show error popup when existing email is found
      showError('This email is already registered. Please try logging in instead.', 'warning');

      // Track failed attempt for rate limiting
      await emailRateLimitService.trackFailedAttempt();

      // Check rate limit status after tracking the attempt
      const status = await emailRateLimitService.getRateLimitStatus();
      setIsInCooldown(status.isInCooldown);
      setCountdownSeconds(status.countdownSeconds);

      // Only show rate limit message and start timer if now in cooldown (after 3 attempts)
      if (status.isInCooldown) {
        startCountdownTimer();
        const rateLimitMessage = await emailRateLimitService.getRateLimitMessage();
        showError(rateLimitMessage, 'warning', 20000);
      }

      setIsProcessingSubmit(false);
      return;
    }

    // Immediate navigation after validation - no account creation yet
    setIsNavigating(true);

    // Update form data for later use in final account creation
    updateFormData({
      email: data.email.trim().toLowerCase(),
      password: data.password,
      confirmPassword: data.confirmPassword,
      agreedToTerms: data.agreedToTerms,
      agreedToPrivacy: data.agreedToPrivacy,
    });

    // Clear rate limit on successful validation (email doesn't exist)
    await emailRateLimitService.resetRateLimit();
    setIsInCooldown(false);
    setCountdownSeconds(0);

    // Move to next step immediately - account will be created after all 5 steps
    nextStep();
    router.push('/onboarding/preferences');

    setIsProcessingSubmit(false);
  };

  const handleBack = () => {
    if (isNavigating) return; // Prevent multiple rapid taps

    // Dismiss any existing error notifications
    dismissErrorOnNavigation();

    setIsNavigating(true);
    previousStep();
    router.push('/onboarding/age-verification');
  };

  const toggleAgreement = (field: 'agreedToTerms' | 'agreedToPrivacy') => {
    const currentValue = watch(field);
    setValue(field, !currentValue);
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
        title="Sign Up"
        onBackPress={handleBack}
        rightIcon={{
          name: 'person-add',
          type: 'ionicons',
          color: '#FF6B35',
          size: 24,
        }}
      />

      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        <AnimatedContainer animation="fadeSlideUp" delay={40}>
          <View style={styles.textSection}>
            <View style={styles.titleIcon}>
              <Ionicons name="person-add" size={56} color="#FA7215" />
            </View>
            <Text style={styles.title}>Create Your Account</Text>

            {/* Social Login Buttons */}
            <View style={styles.socialLoginSection}>
              <TouchableOpacity
                style={styles.googleButton}
                onPress={handleGoogleSignUp}
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
                  onPress={handleAppleSignUp}
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
                        emailExists && styles.textInputError,
                        !errors.email && !emailExists && isFieldValid('email', value) && styles.textInputValid,
                      ]}
                      value={value}
                      onChangeText={(text) => {
                        onChange(text);
                        // Reset emailExists state when user changes email
                        if (emailExists) {
                          setEmailExists(false);
                        }
                      }}
                      onBlur={onBlur}
                      placeholder="your.email@example.com"
                      placeholderTextColor="#9CA3AF"
                      keyboardType="email-address"
                      autoCapitalize="none"
                      autoComplete="email"
                    />
                    {/* No checkmark display for email to prevent information disclosure */}
                  </>
                )}
              />
            </View>
            {/* Email errors are now handled by popup notifications only */}
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
                  validate: value => isPasswordValid(value) || 'Please meet all password requirements'
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
                      onChangeText={(text) => {
                        onChange(text);
                        // Password requirements display is now handled by debounced useEffect
                      }}
                      onBlur={onBlur}
                      placeholder="Enter your password"
                      placeholderTextColor="#9CA3AF"
                      secureTextEntry={!showPassword}
                      autoComplete="new-password"
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
            {/* Show password requirements checklist */}
            {showPasswordRequirements && (
              <PasswordRequirementsChecklist
                password={watchedPassword || ''}
                style={styles.passwordRequirements}
              />
            )}
            {/* Only show generic error if there's a system error, not validation errors */}
            {errors.password && !showPasswordRequirements && (
              <Text style={styles.errorText}>{errors.password.message}</Text>
            )}
          </View>

          {/* Confirm Password Field */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Confirm Password</Text>
            <View style={styles.inputContainer}>
              <Controller
                control={control}
                name="confirmPassword"
                rules={{
                  required: 'Please confirm your password',
                  validate: value =>
                    value === watchedPassword || 'Passwords do not match'
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
                        errors.confirmPassword && styles.textInputError,
                        !errors.confirmPassword && isFieldValid('confirmPassword', value) && styles.textInputValid,
                      ]}
                      value={value}
                      onChangeText={onChange}
                      onBlur={onBlur}
                      placeholder="Confirm your password"
                      placeholderTextColor="#9CA3AF"
                      secureTextEntry={!showConfirmPassword}
                      autoComplete="new-password"
                    />
                    <TouchableOpacity
                      style={styles.eyeButton}
                      onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                    >
                      <Ionicons
                        name={showConfirmPassword ? 'eye-off' : 'eye'}
                        size={20}
                        color="#FF6B35"
                      />
                    </TouchableOpacity>
                  </>
                )}
              />
            </View>
            {/* Show confirm password error only when there's input but passwords don't match */}
            {watchedConfirmPassword && watchedConfirmPassword !== watchedPassword && (
              <View style={styles.confirmPasswordError}>
                <Ionicons name="alert-circle" size={16} color="#EF4444" />
                <Text style={[styles.errorText, styles.inlineErrorText]}>
                  Passwords do not match
                </Text>
              </View>
            )}
          </View>

          {/* Terms and Privacy Agreements */}
          <View style={styles.agreementSection}>
            <Controller
              control={control}
              name="agreedToTerms"
              render={({ field: { value } }) => (
                <Animated.View
                  style={{
                    transform: [{ translateX: termsWiggleAnim }]
                  }}
                >
                  <TouchableOpacity
                    style={styles.checkboxContainer}
                    onPress={() => toggleAgreement('agreedToTerms')}
                  >
                    <View style={[styles.checkbox, value && styles.checkboxChecked]}>
                      {value && (
                        <Ionicons name="checkmark" size={16} color="#ffffff" />
                      )}
                    </View>
                    <Text style={styles.checkboxText}>
                      I agree to the{' '}
                      <Text style={styles.linkText}>Terms of Service</Text>
                    </Text>
                  </TouchableOpacity>
                </Animated.View>
              )}
            />

            <Controller
              control={control}
              name="agreedToPrivacy"
              render={({ field: { value } }) => (
                <Animated.View
                  style={{
                    transform: [{ translateX: privacyWiggleAnim }]
                  }}
                >
                  <TouchableOpacity
                    style={styles.checkboxContainer}
                    onPress={() => toggleAgreement('agreedToPrivacy')}
                  >
                    <View style={[styles.checkbox, value && styles.checkboxChecked]}>
                      {value && (
                        <Ionicons name="checkmark" size={16} color="#ffffff" />
                      )}
                    </View>
                    <Text style={styles.checkboxText}>
                      I agree to the{' '}
                      <Text style={styles.linkText}>Privacy Policy</Text>
                    </Text>
                  </TouchableOpacity>
                </Animated.View>
              )}
            />
          </View>
          </View>
        </AnimatedContainer>

      </ScrollView>

        <View style={styles.buttonSection}>
          <GradientButton
            title={isInCooldown
              ? `Wait ${Math.floor(countdownSeconds / 60)}:${(countdownSeconds % 60).toString().padStart(2, '0')}`
              : "Create Account"
            }
            onPress={handleSubmit(onSubmit)}
            loading={isLoading}
            disabled={!isFormValid() || isLoading || isInCooldown || isProcessingSubmit}
            cooldown={isInCooldown}
            style={styles.createAccountButton}
          />

          <TouchableOpacity
            style={styles.loginButton}
            onPress={() => {
              dismissErrorOnNavigation();
              router.push('/auth/login');
            }}
            activeOpacity={0.7}
          >
            <Text style={styles.loginButtonText}>Log In</Text>
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
    paddingTop: 4,
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
  checkmarkContainer: {
    position: 'absolute',
    right: 16,
    top: '50%',
    marginTop: -10,
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#FF6B35',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 2,
  },
  emojiIcon: {
    fontSize: 18,
  },
  checkmarkEmoji: {
    fontSize: 18,
  },
  passwordContainer: {
    position: 'relative',
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
  agreementSection: {
    marginTop: 4,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: '#FF8C42',
    backgroundColor: '#FFFFFF',
    marginRight: 12,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  checkboxChecked: {
    backgroundColor: '#FF6B35',
    borderColor: '#FF6B35',
    shadowColor: '#FF6B35',
    shadowOpacity: 0.15,
  },
  checkboxText: {
    fontSize: 13,
    color: '#6b7280',
    flex: 1,
    lineHeight: 18,
  },
  linkText: {
    color: '#FF6B35',
    fontWeight: '500',
  },
  buttonSection: {
    paddingHorizontal: 24,
    paddingTop: 12,
    paddingBottom: 20,
    backgroundColor: 'transparent',
  },
  createAccountButton: {
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
  passwordRequirements: {
    marginTop: 12,
  },
  confirmPasswordError: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
    paddingLeft: 4,
  },
  inlineErrorText: {
    marginTop: 0,
    marginLeft: 6,
  },
});