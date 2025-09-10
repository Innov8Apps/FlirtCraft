import { createClient } from '@supabase/supabase-js';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';

// Supabase configuration
const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || 'https://your-project.supabase.co';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || 'your-anon-key';

// Create Supabase client with React Native AsyncStorage
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});

// Auth helper functions
export const authService = {
  // Categorize error types for better handling
  categorizeError(message: string) {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('rate limit') || 
        lowerMessage.includes('too many requests') ||
        lowerMessage.includes('email rate limit exceeded')) {
      return 'rate_limit';
    }
    if (lowerMessage.includes('user already registered') ||
        lowerMessage.includes('email already exists')) {
      return 'email_exists';
    }
    if (lowerMessage.includes('password') && 
        (lowerMessage.includes('weak') || lowerMessage.includes('short'))) {
      return 'weak_password';
    }
    if (lowerMessage.includes('invalid email') || 
        lowerMessage.includes('email format')) {
      return 'invalid_email';
    }
    return 'general';
  },

  // Extract retry-after time from rate limit errors
  extractRetryAfter(error: any) {
    // Check if error has status 429 (Too Many Requests)
    if (error?.status === 429) {
      // Try to extract from headers or error object
      return error.retryAfter || 60; // Default to 60 seconds
    }
    
    // Check error message for time mentions
    const message = error?.message || '';
    const timeMatch = message.match(/(\d+)\s*(second|minute)/i);
    if (timeMatch) {
      const value = parseInt(timeMatch[1]);
      const unit = timeMatch[2].toLowerCase();
      return unit.includes('minute') ? value * 60 : value;
    }
    
    return null;
  },

  // Sign up new user with complete onboarding data
  async signUpWithProfile(email: string, password: string, profileData?: any) {
    try {
      // Step 1: Create auth user
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email,
        password,
      });

      if (authError) {
        const errorType = this.categorizeError(authError.message);
        const retryAfter = this.extractRetryAfter(authError);
        
        return {
          success: false,
          error: authError.message,
          errorType,
          retryAfter,
          errorCode: (authError as any).code || null
        };
      }

      if (!authData.user) {
        return {
          success: false,
          error: 'Failed to create user account',
          errorType: 'unknown',
          retryAfter: null,
          errorCode: null
        };
      }

      // Step 2: Sign in to get session (should work now with email confirmation disabled)
      const { data: signInData, error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (signInError) {
        console.error('Failed to sign in after signup:', signInError);
        return {
          success: false,
          error: 'Account created but could not sign in. Please try signing in manually.',
          errorType: 'auth_error',
          retryAfter: null,
          errorCode: null
        };
      }

      // Make sure we have a session before continuing
      if (!signInData?.session) {
        console.error('No session after sign in');
        return {
          success: false,
          error: 'Account created but session could not be established.',
          errorType: 'session_error',
          retryAfter: null,
          errorCode: null
        };
      }

      // Step 3: Create user record in public.users table (now with active session)
      const { data: userData, error: userError } = await supabase
        .from('users')
        .insert({
          email: email,
          supabase_user_id: authData.user.id,
          birth_date: profileData?.birthDate || null,
          onboarding_completed: true,
          onboarding_completed_at: new Date().toISOString(),
          email_verified: true, // Since email confirmation is disabled
        })
        .select()
        .single();

      if (userError) {
        console.error('Error creating user record:', userError);
        // Don't fail the whole process if user record creation fails
      }

      // Step 4: Create user profile with onboarding data
      if (userData && profileData) {
        const { error: profileError } = await supabase
          .from('user_profiles')
          .insert({
            user_id: userData.id,
            target_gender: profileData.targetGender || 'everyone',
            target_age_min: profileData.targetAgeMin || 18,
            target_age_max: profileData.targetAgeMax || 99,
            relationship_goal: profileData.relationshipGoal || 'dating', // Add default relationship goal
            primary_skills: profileData.primarySkillGoals || [],
            skill_goals: profileData.primarySkillGoals || [],
            experience_level: profileData.experienceLevel || 'beginner',
            practice_frequency: profileData.practiceFrequency || 'weekly',
            onboarding_metadata: {
              userGender: profileData.userGender,
              completedAt: new Date().toISOString(),
              agreedToTerms: profileData.agreedToTerms,
              agreedToPrivacy: profileData.agreedToPrivacy,
            }
          });

        if (profileError) {
          console.error('Error creating user profile:', profileError);
        }

        // Step 5: Create initial progress record
        const { error: progressError } = await supabase
          .from('user_progress')
          .insert({
            user_id: userData.id,
            total_conversations: 0,
            total_messages_sent: 0,
            level: 1,
            xp_points: 0,
          });

        if (progressError) {
          console.error('Error creating progress record:', progressError);
        }
      }

      return { 
        success: true, 
        data: {
          ...authData,
          session: signInData?.session || null,
          user: authData.user,
        }
      };
    } catch (error) {
      console.error('Sign up error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Sign up failed',
        errorType: 'unknown',
        retryAfter: null,
        errorCode: null
      };
    }
  },

  // Original sign up method (keep for backward compatibility)
  async signUp(email: string, password: string) {
    return this.signUpWithProfile(email, password);
  },

  // Sign in existing user
  async signIn(email: string, password: string) {
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;

      return { success: true, data };
    } catch (error) {
      console.error('Sign in error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Sign in failed' 
      };
    }
  },

  // Sign out current user
  async signOut() {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      
      // Clear any local storage
      await AsyncStorage.multiRemove([
        'onboarding-storage',
        'user-preferences',
      ]);

      return { success: true };
    } catch (error) {
      console.error('Sign out error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Sign out failed' 
      };
    }
  },

  // Get current session
  async getSession() {
    try {
      const { data: { session }, error } = await supabase.auth.getSession();
      if (error) throw error;
      return session;
    } catch (error) {
      console.error('Get session error:', error);
      return null;
    }
  },

  // Get current user
  async getCurrentUser() {
    try {
      const { data: { user }, error } = await supabase.auth.getUser();
      if (error) throw error;
      return user;
    } catch (error) {
      console.error('Get user error:', error);
      return null;
    }
  },

  // Reset password
  async resetPassword(email: string) {
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: Platform.OS === 'web' 
          ? `${window.location.origin}/reset-password`
          : 'flirtcraft://reset-password',
      });

      if (error) throw error;

      return { success: true };
    } catch (error) {
      console.error('Reset password error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Password reset failed' 
      };
    }
  },

  // Update user profile
  async updateProfile(updates: {
    age?: number;
    targetGender?: string;
    targetAgeMin?: number;
    targetAgeMax?: number;
    skillGoals?: string[];
  }) {
    try {
      const user = await this.getCurrentUser();
      if (!user) throw new Error('No user logged in');

      const { error } = await supabase
        .from('user_profiles')
        .upsert({
          id: user.id,
          ...updates,
          updated_at: new Date().toISOString(),
        });

      if (error) throw error;

      return { success: true };
    } catch (error) {
      console.error('Update profile error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Profile update failed' 
      };
    }
  },

  // Check if email is already registered using RPC function
  async checkEmailExists(email: string) {
    try {
      // First validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return { exists: false, error: 'Invalid email format' };
      }

      // Use the RPC function to check if email exists
      const { data, error } = await supabase.rpc('check_email_exists', {
        email_input: email.toLowerCase()
      });

      if (error) {
        console.error('Email check RPC error:', error);
        
        // Check for rate limiting
        const errorMessage = error.message.toLowerCase();
        if (errorMessage.includes('rate limit') || 
            errorMessage.includes('too many requests')) {
          return { exists: false, error: 'Too many attempts. Please try again later.' };
        }
        
        // On error, default to allowing the check to not block users
        return { exists: false };
      }

      // The RPC function returns true if email exists, false otherwise
      if (data === true) {
        console.log('Email already registered:', email);
        return { exists: true };
      }
      
      console.log('Email is available:', email);
      return { exists: false };
    } catch (error) {
      console.error('Email check error:', error);
      // Default to available on error to not block registration
      return { exists: false };
    }
  },
};

// Session management
export const sessionManager = {
  // Listen to auth state changes
  onAuthStateChange(callback: (event: string, session: any) => void) {
    return supabase.auth.onAuthStateChange(callback);
  },

  // Check if user is authenticated
  async isAuthenticated() {
    const session = await authService.getSession();
    return !!session;
  },

  // Refresh session
  async refreshSession() {
    try {
      const { data: { session }, error } = await supabase.auth.refreshSession();
      if (error) throw error;
      return session;
    } catch (error) {
      console.error('Refresh session error:', error);
      return null;
    }
  },
};

// User data service
export const userDataService = {
  // Save onboarding data
  async saveOnboardingData(data: any) {
    try {
      const user = await authService.getCurrentUser();
      if (!user) throw new Error('No user logged in');

      const { error } = await supabase
        .from('onboarding_data')
        .upsert({
          user_id: user.id,
          data,
          completed_at: new Date().toISOString(),
        });

      if (error) throw error;

      return { success: true };
    } catch (error) {
      console.error('Save onboarding data error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Failed to save data' 
      };
    }
  },

  // Get user profile
  async getUserProfile() {
    try {
      const user = await authService.getCurrentUser();
      if (!user) throw new Error('No user logged in');

      const { data, error } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('id', user.id)
        .single();

      if (error) throw error;

      return { success: true, data };
    } catch (error) {
      console.error('Get profile error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Failed to get profile' 
      };
    }
  },
};

// Rate limit tracking service
export const rateLimitService = {
  SIGNUP_RATE_LIMIT_KEY: 'signup_attempts',
  SIGNIN_RATE_LIMIT_KEY: 'signin_attempts',
  MAX_ATTEMPTS_PER_BLOCK: 3,
  
  // Progressive wait times after each block: 60s, 120s, 300s (5 min)
  WAIT_TIMES: [60, 120, 300],

  // Get progressive wait time based on which block we're in
  getWaitTime(blockNumber: number): number {
    // blockNumber starts at 0 for first block
    const index = Math.min(blockNumber, this.WAIT_TIMES.length - 1);
    return this.WAIT_TIMES[index];
  },

  // Check if rate limited (supports both signup and signin)
  async checkRateLimit(type: 'signup' | 'signin' = 'signup') {
    try {
      const key = type === 'signin' ? this.SIGNIN_RATE_LIMIT_KEY : this.SIGNUP_RATE_LIMIT_KEY;
      const attempts = await AsyncStorage.getItem(key);
      
      if (attempts) {
        const { 
          currentBlockAttempts = 0, 
          blockNumber = 0, 
          blockedUntil 
        } = JSON.parse(attempts);
        const now = Date.now();
        
        // Check if currently blocked
        if (blockedUntil && blockedUntil > now) {
          const waitTime = Math.ceil((blockedUntil - now) / 1000);
          return { 
            allowed: false, 
            waitTime,
            message: `Too many attempts. Please wait ${waitTime} seconds.`
          };
        }
        
        // If block period has passed, move to next block with reset counter
        if (blockedUntil && blockedUntil <= now) {
          await AsyncStorage.setItem(key, JSON.stringify({
            currentBlockAttempts: 0,
            blockNumber: blockNumber + 1, // Move to next block
            blockedUntil: null
          }));
          return { allowed: true };
        }
        
        // Check if we've reached the limit for this block
        if (currentBlockAttempts >= this.MAX_ATTEMPTS_PER_BLOCK) {
          // Calculate progressive wait time based on which block we're in
          const waitTime = this.getWaitTime(blockNumber);
          
          // Set the block time with the correct type parameter
          await this.setRateLimitBlock(waitTime, type);
          
          return { 
            allowed: false, 
            waitTime,
            message: `Maximum attempts reached. Please wait ${waitTime} seconds.`
          };
        }
      }
      
      return { allowed: true };
    } catch (error) {
      console.error('Rate limit check error:', error);
      return { allowed: true }; // Allow on error to not block user
    }
  },

  // Track an attempt (supports both signup and signin)
  async trackAttempt(type: 'signup' | 'signin' = 'signup') {
    try {
      const key = type === 'signin' ? this.SIGNIN_RATE_LIMIT_KEY : this.SIGNUP_RATE_LIMIT_KEY;
      const attempts = await AsyncStorage.getItem(key);
      
      let data;
      if (attempts) {
        data = JSON.parse(attempts);
        // Increment attempts in current block
        data.currentBlockAttempts = (data.currentBlockAttempts || 0) + 1;
      } else {
        // First attempt ever
        data = { 
          currentBlockAttempts: 1,
          blockNumber: 0, // Start at block 0
          blockedUntil: null
        };
      }
      
      await AsyncStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error('Rate limit tracking error:', error);
    }
  },

  // Set rate limit block (supports both signup and signin)
  async setRateLimitBlock(seconds: number, type: 'signup' | 'signin' = 'signup') {
    try {
      const key = type === 'signin' ? this.SIGNIN_RATE_LIMIT_KEY : this.SIGNUP_RATE_LIMIT_KEY;
      const attempts = await AsyncStorage.getItem(key);
      const now = Date.now();
      
      let data;
      if (attempts) {
        data = JSON.parse(attempts);
      } else {
        data = { 
          currentBlockAttempts: 0, 
          blockNumber: 0,
          blockedUntil: null
        };
      }
      
      // Set the block time
      data.blockedUntil = now + (seconds * 1000);
      await AsyncStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error('Set rate limit block error:', error);
    }
  },

  // Clear rate limit data (supports both signup and signin)
  async clearRateLimit(type: 'signup' | 'signin' = 'signup') {
    try {
      const key = type === 'signin' ? this.SIGNIN_RATE_LIMIT_KEY : this.SIGNUP_RATE_LIMIT_KEY;
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Clear rate limit error:', error);
    }
  },

  // Reset rate limit (for testing/debugging)
  async resetRateLimit(type?: 'signup' | 'signin') {
    try {
      if (type) {
        const key = type === 'signin' ? this.SIGNIN_RATE_LIMIT_KEY : this.SIGNUP_RATE_LIMIT_KEY;
        await AsyncStorage.removeItem(key);
        console.log(`${type} rate limit has been reset`);
      } else {
        // Reset both
        await AsyncStorage.removeItem(this.SIGNUP_RATE_LIMIT_KEY);
        await AsyncStorage.removeItem(this.SIGNIN_RATE_LIMIT_KEY);
        console.log('All rate limits have been reset');
      }
    } catch (error) {
      console.error('Reset rate limit error:', error);
    }
  }
};

export default supabase;