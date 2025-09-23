import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
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
import { supabase } from '@/lib/supabase';

const registrationSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string(),
  agreedToTermsAndPrivacy: z.boolean().refine(val => val, 'You must agree to the Terms of Service and Privacy Policy'),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type RegistrationFormData = z.infer<typeof registrationSchema>;

export default function AuthenticationScreen({ onNext, onBack }: OnboardingStepProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const { updateFormData, authState } = useOnboardingStore();

  const formTranslateY = useSharedValue(30);

  useEffect(() => {
    formTranslateY.value = withSpring(0);
  }, []);

  const registrationForm = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
      agreedToTermsAndPrivacy: false,
    }
  });

  const calculatePasswordStrength = (password: string): number => {
    let strength = 0;
    if (password.length >= 8) strength += 34;
    if (/[A-Z]/.test(password)) strength += 33;
    if (/[0-9]/.test(password)) strength += 33;
    // Special characters are now optional but still contribute to strength
    if (/[!@#$%^&*]/.test(password)) strength += 25;
    return Math.min(strength, 100);
  };

  const getPasswordStrengthColor = (strength: number): string => {
    if (strength < 25) return '#EF4444';
    if (strength < 50) return '#F59E0B';
    if (strength < 75) return '#10B981';
    return '#059669';
  };

  const getPasswordStrengthText = (strength: number): string => {
    if (strength < 25) return 'Weak';
    if (strength < 50) return 'Fair';
    if (strength < 75) return 'Good';
    return 'Strong';
  };

  const handlePasswordChange = (password: string) => {
    const strength = calculatePasswordStrength(password);
    setPasswordStrength(strength);
  };

  const checkEmailAvailability = async (email: string): Promise<boolean> => {
    try {
      const { data, error } = await supabase
        .from('users')
        .select('email')
        .eq('email', email.toLowerCase())
        .single();

      return !data; // Email is available if no data found
    } catch (error) {
      return true; // Assume available if check fails
    }
  };

  const handleRegistration = async (data: RegistrationFormData) => {
    setIsLoading(true);
    try {
      // Check email availability
      const emailAvailable = await checkEmailAvailability(data.email);
      if (!emailAvailable) {
        Alert.alert('Email Taken', 'This email is already registered. Please use a different email or sign in.');
        setIsLoading(false);
        return;
      }

      // Store form data temporarily
      updateFormData('registration', data);

      // We'll create the actual account in the final onboarding step
      await onNext();
    } catch (error) {
      console.error('Registration error:', error);
      Alert.alert('Registration Error', 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };


  const handleGoogleAuth = async () => {
    setIsLoading(true);
    try {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
      });

      if (error) {
        Alert.alert('Google Sign In Error', error.message);
        return;
      }

      // For now, show a message that Google auth will be available in production
      Alert.alert(
        'Google Sign In',
        'Google authentication will be available in the production version. Please use email/password registration for now.',
        [{ text: 'OK' }]
      );
    } catch (error) {
      console.error('Google auth error:', error);
      Alert.alert('Google Sign In Error', 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={['#FFFFFF', '#FFF7F4']}
        style={styles.backgroundGradient}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          <Animated.View style={styles.content}>
            <Animated.View entering={FadeIn.delay(300).duration(600)}>
              <Text style={styles.headline}>
                Create your FlirtCraft account
              </Text>
              <Text style={styles.subheadline}>
                Join thousands who are building their confidence
              </Text>
            </Animated.View>

            <Animated.View entering={FadeIn.delay(700).duration(500)} style={styles.formContainer}>
              {/* Google Sign In Button */}
              <TouchableOpacity
                style={styles.googleButton}
                onPress={handleGoogleAuth}
                disabled={isLoading}
              >
                <View style={styles.googleButtonContent}>
                  <Ionicons name="logo-google" size={20} color="#FF6B35" style={styles.googleIcon} />
                  <Text style={styles.googleButtonText}>
                    Sign up with Google
                  </Text>
                </View>
              </TouchableOpacity>

              {/* Divider */}
              <View style={styles.dividerContainer}>
                <View style={styles.dividerLine} />
                <Text style={styles.dividerText}>or</Text>
                <View style={styles.dividerLine} />
              </View>

              <View style={styles.form}>
                  {/* Email Field */}
                  <Controller
                    control={registrationForm.control}
                    name="email"
                    render={({ field: { onChange, onBlur, value }, fieldState: { error } }) => (
                      <View style={styles.inputContainer}>
                        <Text style={styles.inputLabel}>Email Address</Text>
                        <TextInput
                          style={[styles.textInput, error && styles.textInputError]}
                          value={value}
                          onChangeText={onChange}
                          onBlur={onBlur}
                          placeholder="your@email.com"
                          placeholderTextColor="#9CA3AF"
                          keyboardType="email-address"
                          autoCapitalize="none"
                          autoCorrect={false}
                        />
                        {error && <Text style={styles.errorText}>{error.message}</Text>}
                      </View>
                    )}
                  />

                  {/* Password Field */}
                  <Controller
                    control={registrationForm.control}
                    name="password"
                    render={({ field: { onChange, onBlur, value }, fieldState: { error } }) => (
                      <View style={styles.inputContainer}>
                        <Text style={styles.inputLabel}>Password</Text>
                        <View style={styles.passwordContainer}>
                          <TextInput
                            style={[styles.textInput, styles.passwordInput, error && styles.textInputError]}
                            value={value}
                            onChangeText={(text) => {
                              onChange(text);
                              handlePasswordChange(text);
                            }}
                            onBlur={onBlur}
                            placeholder="Create a strong password"
                            placeholderTextColor="#9CA3AF"
                            secureTextEntry={!showPassword}
                            autoCapitalize="none"
                            autoCorrect={false}
                          />
                          <TouchableOpacity
                            style={styles.passwordToggle}
                            onPress={() => setShowPassword(!showPassword)}
                          >
                            <Ionicons
                              name={showPassword ? 'eye-off-outline' : 'eye-outline'}
                              size={20}
                              color="#6B7280"
                            />
                          </TouchableOpacity>
                        </View>
                        {value.length > 0 && (
                          <View style={styles.passwordStrengthContainer}>
                            <View style={styles.passwordStrengthBar}>
                              <View
                                style={[
                                  styles.passwordStrengthFill,
                                  {
                                    width: `${passwordStrength}%`,
                                    backgroundColor: getPasswordStrengthColor(passwordStrength),
                                  }
                                ]}
                              />
                            </View>
                            <Text
                              style={[
                                styles.passwordStrengthText,
                                { color: getPasswordStrengthColor(passwordStrength) }
                              ]}
                            >
                              {getPasswordStrengthText(passwordStrength)}
                            </Text>
                          </View>
                        )}
                        {error && <Text style={styles.errorText}>{error.message}</Text>}
                      </View>
                    )}
                  />

                  {/* Confirm Password Field */}
                  <Controller
                    control={registrationForm.control}
                    name="confirmPassword"
                    render={({ field: { onChange, onBlur, value }, fieldState: { error } }) => (
                      <View style={styles.inputContainer}>
                        <Text style={styles.inputLabel}>Confirm Password</Text>
                        <View style={styles.passwordContainer}>
                          <TextInput
                            style={[styles.textInput, styles.passwordInput, error && styles.textInputError]}
                            value={value}
                            onChangeText={onChange}
                            onBlur={onBlur}
                            placeholder="Confirm your password"
                            placeholderTextColor="#9CA3AF"
                            secureTextEntry={!showConfirmPassword}
                            autoCapitalize="none"
                            autoCorrect={false}
                          />
                          <TouchableOpacity
                            style={styles.passwordToggle}
                            onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                          >
                            <Ionicons
                              name={showConfirmPassword ? 'eye-off-outline' : 'eye-outline'}
                              size={20}
                              color="#6B7280"
                            />
                          </TouchableOpacity>
                        </View>
                        {error && <Text style={styles.errorText}>{error.message}</Text>}
                      </View>
                    )}
                  />

                  {/* Terms and Privacy Agreement */}
                  <Controller
                    control={registrationForm.control}
                    name="agreedToTermsAndPrivacy"
                    render={({ field: { onChange, value }, fieldState: { error } }) => (
                      <View style={styles.checkboxContainer}>
                        <TouchableOpacity
                          style={styles.checkbox}
                          onPress={() => onChange(!value)}
                        >
                          <View style={[styles.checkboxBox, value && styles.checkboxChecked]}>
                            {value && <Ionicons name="checkmark" size={16} color="#FFFFFF" />}
                          </View>
                          <Text style={styles.checkboxText}>
                            I agree to the <Text style={styles.linkText}>Terms of Service</Text> and <Text style={styles.linkText}>Privacy Policy</Text>
                          </Text>
                        </TouchableOpacity>
                        {error && <Text style={styles.errorText}>{error.message}</Text>}
                      </View>
                    )}
                  />

                  <OnboardingButton
                    title="Create Account"
                    onPress={registrationForm.handleSubmit(handleRegistration)}
                    loading={isLoading}
                    disabled={!registrationForm.formState.isValid}
                  />
                </View>
            </Animated.View>
          </Animated.View>
        </ScrollView>
      </LinearGradient>
    </KeyboardAvoidingView>
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
    flexGrow: 1,
    paddingHorizontal: 24,
    paddingVertical: 32,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
  },
  headline: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1A1A1A',
    textAlign: 'center',
    marginBottom: 8,
  },
  subheadline: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 32,
  },
  toggleButton: {
    alignItems: 'center',
    marginBottom: 32,
  },
  toggleText: {
    fontSize: 16,
    color: '#FF6B35',
    fontWeight: '500',
  },
  formContainer: {
    width: '100%',
  },
  form: {
    width: '100%',
  },
  inputContainer: {
    marginBottom: 20,
  },
  inputLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  textInput: {
    borderWidth: 2,
    borderColor: '#E5E5E5',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: '#1A1A1A',
    backgroundColor: '#FFFFFF',
  },
  textInputError: {
    borderColor: '#EF4444',
  },
  passwordContainer: {
    position: 'relative',
  },
  passwordInput: {
    paddingRight: 50,
  },
  passwordToggle: {
    position: 'absolute',
    right: 16,
    top: 17,
    padding: 4,
  },
  passwordStrengthContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  passwordStrengthBar: {
    flex: 1,
    height: 4,
    backgroundColor: '#E5E5E5',
    borderRadius: 2,
    marginRight: 12,
  },
  passwordStrengthFill: {
    height: '100%',
    borderRadius: 2,
  },
  passwordStrengthText: {
    fontSize: 12,
    fontWeight: '500',
  },
  checkboxContainer: {
    marginBottom: 16,
  },
  checkbox: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkboxBox: {
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: '#E5E5E5',
    borderRadius: 4,
    marginRight: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkboxChecked: {
    backgroundColor: '#FF6B35',
    borderColor: '#FF6B35',
  },
  checkboxText: {
    flex: 1,
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  linkText: {
    color: '#FF6B35',
    fontWeight: '500',
  },
  forgotPassword: {
    alignSelf: 'flex-end',
    marginBottom: 24,
  },
  errorText: {
    fontSize: 12,
    color: '#EF4444',
    marginTop: 4,
  },
  googleButton: {
    borderWidth: 2,
    borderColor: '#E5E5E5',
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
    marginBottom: 24,
    backgroundColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  googleButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  googleIcon: {
    marginRight: 12,
  },
  googleButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
  },
  dividerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: '#E5E5E5',
  },
  dividerText: {
    marginHorizontal: 16,
    fontSize: 14,
    color: '#9CA3AF',
    fontWeight: '500',
  },
});