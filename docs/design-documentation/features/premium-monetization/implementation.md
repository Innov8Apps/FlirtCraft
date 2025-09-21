# Premium Monetization - Implementation Guide

---
title: Premium Monetization Implementation
description: Technical implementation guide for subscription management and paywall system
feature: premium-monetization
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - accessibility.md
dependencies:
  - React Native 0.72+
  - Expo 52+
  - RevenueCat SDK
  - Supabase Auth & Database
  - React Query
  - Zustand
status: approved
---

## Implementation Overview

The premium monetization system requires careful integration of payment processing, subscription management, feature gating, and analytics. The implementation uses RevenueCat for subscription infrastructure with Supabase for user data persistence.

### Architecture Components
- **Payment Processing**: RevenueCat + Platform Stores
- **Subscription State**: Zustand + React Query
- **Feature Gating**: HOCs and hooks for access control
- **Paywall UI**: Reusable modal and screen components
- **Analytics**: RevenueCat + Custom events

## Data Models

### Subscription Schema (Supabase)
```sql
-- User subscription status table
CREATE TABLE user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_type VARCHAR(20) NOT NULL CHECK (subscription_type IN ('free', 'plus', 'trial')),
    subscription_status VARCHAR(20) NOT NULL CHECK (subscription_status IN ('active', 'cancelled', 'expired', 'grace_period')),
    current_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    current_period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    trial_end TIMESTAMP WITH TIME ZONE,
    cancellation_date TIMESTAMP WITH TIME ZONE,
    
    -- RevenueCat data
    revenue_cat_id VARCHAR(255) UNIQUE,
    original_purchase_date TIMESTAMP WITH TIME ZONE,
    product_id VARCHAR(100),
    
    -- Usage limits
    daily_conversations_limit INTEGER DEFAULT 1,
    daily_conversations_used INTEGER DEFAULT 0,
    last_reset_date DATE DEFAULT CURRENT_DATE,
    
    -- Features access
    has_unlimited_conversations BOOLEAN DEFAULT FALSE,
    has_all_difficulties BOOLEAN DEFAULT FALSE,
    has_premium_scenarios BOOLEAN DEFAULT FALSE,
    has_advanced_analytics BOOLEAN DEFAULT FALSE,
    has_extended_history BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id)
);

-- Premium features usage tracking
CREATE TABLE premium_feature_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL,
    usage_count INTEGER DEFAULT 1,
    first_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, feature_name)
);

-- Paywall impressions for analytics
CREATE TABLE paywall_impressions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    paywall_type VARCHAR(50) NOT NULL, -- 'daily_limit', 'difficulty_locked', 'scenario_locked', etc.
    trigger_source VARCHAR(100),
    shown_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    action_taken VARCHAR(50), -- 'dismissed', 'trial_started', 'purchased', 'learned_more'
    time_on_screen INTEGER, -- milliseconds
    
    INDEX idx_paywall_user_id (user_id),
    INDEX idx_paywall_type (paywall_type),
    INDEX idx_paywall_shown_at (shown_at)
);

-- Subscription events for retention analysis
CREATE TABLE subscription_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- 'trial_started', 'converted', 'renewed', 'cancelled', 'reactivated'
    from_status VARCHAR(20),
    to_status VARCHAR(20),
    product_id VARCHAR(100),
    price_amount DECIMAL(10, 2),
    currency VARCHAR(3),
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB,
    
    INDEX idx_subscription_events_user (user_id),
    INDEX idx_subscription_events_type (event_type)
);

-- Row Level Security Policies
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE premium_feature_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE paywall_impressions ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own subscription" ON user_subscriptions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own feature usage" ON premium_feature_usage
    FOR SELECT USING (auth.uid() = user_id);
```

### TypeScript Types
```typescript
// types/subscription.ts
export interface Subscription {
  id: string;
  userId: string;
  type: 'free' | 'plus' | 'trial';
  status: 'active' | 'cancelled' | 'expired' | 'grace_period';
  currentPeriodStart: Date;
  currentPeriodEnd: Date;
  trialEnd?: Date;
  cancellationDate?: Date;
  
  // Feature access
  features: {
    unlimitedConversations: boolean;
    allDifficulties: boolean;
    premiumScenarios: boolean;
    advancedAnalytics: boolean;
    extendedHistory: boolean;
    prioritySupport: boolean;
  };
  
  // Usage tracking
  usage: {
    dailyConversationsLimit: number;
    dailyConversationsUsed: number;
    lastResetDate: string;
  };
}

export interface Product {
  id: string;
  identifier: string;
  price: string;
  priceAmount: number;
  currency: string;
  period: 'monthly' | 'annual';
  trialDays: number;
  features: string[];
}

export interface PaywallConfig {
  type: 'daily_limit' | 'difficulty_locked' | 'scenario_locked' | 'soft_sell';
  trigger: string;
  title: string;
  subtitle: string;
  benefits: string[];
  primaryCTA: string;
  secondaryCTA: string;
  dismissable: boolean;
  analyticsProperties: Record<string, any>;
}
```

## State Management

### Subscription Store (Zustand)
```typescript
// stores/subscriptionStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Purchases, { PurchasesPackage } from 'react-native-purchases';

interface SubscriptionState {
  // Current subscription
  subscription: Subscription | null;
  isLoading: boolean;
  error: string | null;
  
  // Products and offerings
  products: Product[];
  offerings: PurchasesPackage[];
  
  // Daily usage
  conversationsToday: number;
  canStartConversation: boolean;
  timeUntilReset: number;
  
  // UI State
  paywallVisible: boolean;
  paywallType: PaywallConfig['type'] | null;
  
  // Actions
  initializeSubscription: () => Promise<void>;
  checkSubscriptionStatus: () => Promise<void>;
  purchaseSubscription: (productId: string) => Promise<void>;
  restorePurchases: () => Promise<void>;
  cancelSubscription: () => Promise<void>;
  
  // Usage tracking
  incrementDailyUsage: () => void;
  resetDailyUsage: () => void;
  checkCanStartConversation: () => boolean;
  
  // Paywall management
  showPaywall: (type: PaywallConfig['type'], trigger?: string) => void;
  hidePaywall: () => void;
  
  // Feature checks
  hasFeature: (feature: keyof Subscription['features']) => boolean;
  canAccessDifficulty: (difficulty: 'green' | 'yellow' | 'red') => boolean;
  canAccessScenario: (scenarioId: string) => boolean;
}

export const useSubscriptionStore = create<SubscriptionState>()(
  persist(
    (set, get) => ({
      subscription: null,
      isLoading: true,
      error: null,
      products: [],
      offerings: [],
      conversationsToday: 0,
      canStartConversation: true,
      timeUntilReset: 0,
      paywallVisible: false,
      paywallType: null,
      
      initializeSubscription: async () => {
        set({ isLoading: true, error: null });
        
        try {
          // Initialize RevenueCat
          await Purchases.configure({
            apiKey: process.env.REVENUE_CAT_API_KEY!,
          });
          
          // Get customer info
          const customerInfo = await Purchases.getCustomerInfo();
          
          // Check active subscriptions
          const isActive = customerInfo.entitlements.active['premium'] !== undefined;
          const isTrialActive = customerInfo.entitlements.active['premium']?.isActive && 
                               customerInfo.entitlements.active['premium']?.willRenew === false;
          
          // Fetch subscription from database
          const subscription = await fetchSubscriptionFromSupabase();
          
          // Sync with RevenueCat
          if (isActive && !subscription?.features.unlimitedConversations) {
            await activatePremiumFeatures();
          }
          
          // Load products
          const offerings = await Purchases.getOfferings();
          
          set({
            subscription: subscription || createDefaultSubscription(),
            offerings: offerings.current?.availablePackages || [],
            products: parseProducts(offerings),
            isLoading: false,
          });
          
          // Check daily usage
          get().checkCanStartConversation();
          
        } catch (error) {
          set({ 
            error: 'Failed to initialize subscription', 
            isLoading: false 
          });
          console.error('Subscription initialization error:', error);
        }
      },
      
      checkSubscriptionStatus: async () => {
        try {
          const customerInfo = await Purchases.getCustomerInfo();
          const subscription = await fetchSubscriptionFromSupabase();
          
          // Update local state
          set({ subscription });
          
          // Check if we need to reset daily usage
          const today = new Date().toDateString();
          const lastReset = subscription?.usage.lastResetDate;
          
          if (lastReset !== today) {
            get().resetDailyUsage();
          }
          
        } catch (error) {
          console.error('Failed to check subscription status:', error);
        }
      },
      
      purchaseSubscription: async (productId: string) => {
        set({ isLoading: true, error: null });
        
        try {
          // Find the package
          const offerings = get().offerings;
          const packageToPurchase = offerings.find(p => p.product.identifier === productId);
          
          if (!packageToPurchase) {
            throw new Error('Product not found');
          }
          
          // Make purchase
          const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
          
          // Update subscription in database
          await updateSubscriptionInSupabase({
            type: 'plus',
            status: 'active',
            productId,
            customerInfo,
          });
          
          // Refresh subscription state
          await get().checkSubscriptionStatus();
          
          // Track conversion
          trackEvent('subscription_purchased', {
            product_id: productId,
            price: packageToPurchase.product.price,
            trigger: get().paywallType,
          });
          
          // Hide paywall
          get().hidePaywall();
          
          // Show success message
          showSuccessToast('Welcome to Premium! 🎉');
          
        } catch (error: any) {
          if (error.code === 'USER_CANCELLED') {
            trackEvent('purchase_cancelled', { product_id: productId });
          } else {
            set({ error: 'Purchase failed. Please try again.' });
            console.error('Purchase error:', error);
          }
        } finally {
          set({ isLoading: false });
        }
      },
      
      restorePurchases: async () => {
        set({ isLoading: true, error: null });
        
        try {
          const customerInfo = await Purchases.restorePurchases();
          
          if (customerInfo.entitlements.active['premium']) {
            await updateSubscriptionInSupabase({
              type: 'plus',
              status: 'active',
              customerInfo,
            });
            
            await get().checkSubscriptionStatus();
            showSuccessToast('Purchases restored successfully!');
          } else {
            showInfoToast('No previous purchases found');
          }
          
        } catch (error) {
          set({ error: 'Failed to restore purchases' });
          console.error('Restore error:', error);
        } finally {
          set({ isLoading: false });
        }
      },
      
      cancelSubscription: async () => {
        // Note: Actual cancellation happens through app stores
        // This just tracks the intent
        try {
          await updateSubscriptionInSupabase({
            status: 'cancelled',
            cancellationDate: new Date(),
          });
          
          trackEvent('subscription_cancelled', {
            subscription_days: calculateSubscriptionDays(),
            reason: 'user_initiated',
          });
          
        } catch (error) {
          console.error('Failed to track cancellation:', error);
        }
      },
      
      incrementDailyUsage: () => {
        const current = get().conversationsToday;
        set({ conversationsToday: current + 1 });
        
        // Update in database
        updateDailyUsageInSupabase(current + 1);
        
        // Check if limit reached
        get().checkCanStartConversation();
      },
      
      resetDailyUsage: () => {
        set({ conversationsToday: 0 });
        updateDailyUsageInSupabase(0);
      },
      
      checkCanStartConversation: () => {
        const { subscription, conversationsToday } = get();
        
        if (subscription?.features.unlimitedConversations) {
          set({ canStartConversation: true });
          return true;
        }
        
        const limit = subscription?.usage.dailyConversationsLimit || 1;
        const canStart = conversationsToday < limit;
        
        set({ canStartConversation: canStart });
        
        // Calculate time until reset
        if (!canStart) {
          const now = new Date();
          const tomorrow = new Date();
          tomorrow.setDate(tomorrow.getDate() + 1);
          tomorrow.setHours(0, 0, 0, 0);
          
          const timeUntilReset = tomorrow.getTime() - now.getTime();
          set({ timeUntilReset });
        }
        
        return canStart;
      },
      
      showPaywall: (type, trigger = 'unknown') => {
        set({ 
          paywallVisible: true, 
          paywallType: type 
        });
        
        // Track impression
        trackEvent('paywall_shown', {
          paywall_type: type,
          trigger_source: trigger,
          conversations_today: get().conversationsToday,
          subscription_type: get().subscription?.type || 'free',
        });
        
        // Record in database
        recordPaywallImpression(type, trigger);
      },
      
      hidePaywall: () => {
        const startTime = Date.now();
        
        set({ 
          paywallVisible: false,
          paywallType: null 
        });
        
        // Track dismissal
        trackEvent('paywall_dismissed', {
          paywall_type: get().paywallType,
          time_on_screen: Date.now() - startTime,
        });
      },
      
      hasFeature: (feature) => {
        const subscription = get().subscription;
        return subscription?.features[feature] || false;
      },
      
      canAccessDifficulty: (difficulty) => {
        const subscription = get().subscription;
        
        if (difficulty === 'green') return true;
        
        return subscription?.features.allDifficulties || false;
      },
      
      canAccessScenario: (scenarioId) => {
        const premiumScenarios = ['gym', 'bar', 'gallery'];
        
        if (!premiumScenarios.includes(scenarioId)) {
          return true; // Free scenario
        }
        
        const subscription = get().subscription;
        return subscription?.features.premiumScenarios || false;
      },
    }),
    {
      name: 'subscription-store',
      storage: {
        getItem: async (name) => {
          const value = await AsyncStorage.getItem(name);
          return value ? JSON.parse(value) : null;
        },
        setItem: async (name, value) => {
          await AsyncStorage.setItem(name, JSON.stringify(value));
        },
        removeItem: async (name) => {
          await AsyncStorage.removeItem(name);
        },
      },
      partialize: (state) => ({
        conversationsToday: state.conversationsToday,
        subscription: state.subscription,
      }),
    }
  )
);
```

## Feature Gating Components

### Premium Gate HOC
```typescript
// components/PremiumGate.tsx
import React from 'react';
import { useSubscriptionStore } from '@/stores/subscriptionStore';

interface PremiumGateProps {
  feature: keyof Subscription['features'];
  fallback?: React.ReactNode;
  children: React.ReactNode;
  onGatedAccess?: () => void;
}

export const PremiumGate: React.FC<PremiumGateProps> = ({
  feature,
  fallback = null,
  children,
  onGatedAccess,
}) => {
  const { hasFeature, showPaywall } = useSubscriptionStore();
  
  if (!hasFeature(feature)) {
    if (onGatedAccess) {
      onGatedAccess();
    } else {
      // Default behavior: show paywall
      showPaywall('soft_sell', `feature_${feature}`);
    }
    
    return <>{fallback}</>;
  }
  
  return <>{children}</>;
};

// Usage example:
// <PremiumGate feature="advancedAnalytics">
//   <AdvancedAnalyticsView />
// </PremiumGate>
```

### Difficulty Gate Component
```typescript
// components/DifficultyGate.tsx
import React from 'react';
import { Pressable } from 'react-native';
import { Box, Text, Icon } from 'native-base';
import { useSubscriptionStore } from '@/stores/subscriptionStore';

interface DifficultyGateProps {
  difficulty: 'green' | 'yellow' | 'red';
  onPress: () => void;
  isSelected: boolean;
}

export const DifficultyGate: React.FC<DifficultyGateProps> = ({
  difficulty,
  onPress,
  isSelected,
}) => {
  const { canAccessDifficulty, showPaywall } = useSubscriptionStore();
  const canAccess = canAccessDifficulty(difficulty);
  
  const handlePress = () => {
    if (!canAccess) {
      showPaywall('difficulty_locked', difficulty);
      return;
    }
    
    onPress();
  };
  
  const difficultyConfig = {
    green: { 
      color: '#22C55E', 
      name: 'Friendly', 
      emoji: '🟢',
      description: 'Open and receptive'
    },
    yellow: { 
      color: '#F59E0B', 
      name: 'Real Talk', 
      emoji: '🟡',
      description: 'Realistic stranger',
      locked: !canAccess
    },
    red: { 
      color: '#EF4444', 
      name: 'A-Game', 
      emoji: '🔴',
      description: 'Challenging',
      locked: !canAccess
    },
  };
  
  const config = difficultyConfig[difficulty];
  
  return (
    <Pressable onPress={handlePress}>
      <Box
        borderWidth={3}
        borderColor={isSelected ? config.color : 'gray.300'}
        borderRadius="xl"
        p={4}
        opacity={config.locked ? 0.6 : 1}
        position="relative"
      >
        {config.locked && (
          <Box
            position="absolute"
            top={2}
            right={2}
            bg="orange.500"
            px={2}
            py={1}
            borderRadius="full"
          >
            <HStack space={1} alignItems="center">
              <Icon name="lock" size="xs" color="white" />
              <Text fontSize="xs" color="white" fontWeight="600">
                Premium
              </Text>
            </HStack>
          </Box>
        )}
        
        <HStack space={3} alignItems="center">
          <Text fontSize="2xl">{config.emoji}</Text>
          <VStack flex={1}>
            <Text fontSize="lg" fontWeight="600">
              {config.name}
            </Text>
            <Text fontSize="sm" color="gray.600">
              {config.description}
            </Text>
          </VStack>
        </HStack>
      </Box>
    </Pressable>
  );
};
```

## Paywall Components

### Main Paywall Modal
```typescript
// components/PaywallModal.tsx
import React, { useEffect, useRef } from 'react';
import { Modal, Dimensions, ScrollView, Platform } from 'react-native';
import { Box, VStack, HStack, Text, Button, IconButton } from 'native-base';
import Animated, { 
  FadeIn, 
  SlideInUp,
  FadeOut,
  SlideOutDown,
} from 'react-native-reanimated';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { BenefitsComparison } from './BenefitsComparison';
import { PricingSelector } from './PricingSelector';
import { TestimonialCarousel } from './TestimonialCarousel';

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

export const PaywallModal: React.FC = () => {
  const { 
    paywallVisible, 
    paywallType,
    hidePaywall,
    products,
    purchaseSubscription,
    isLoading,
  } = useSubscriptionStore();
  
  const impressionStartTime = useRef<number>(0);
  const [selectedProduct, setSelectedProduct] = React.useState<string>('monthly');
  
  useEffect(() => {
    if (paywallVisible) {
      impressionStartTime.current = Date.now();
    }
  }, [paywallVisible]);
  
  const getPaywallContent = () => {
    switch (paywallType) {
      case 'daily_limit':
        return {
          title: "You're on fire! 🔥",
          subtitle: "Keep practicing with unlimited conversations",
          primaryBenefit: "Never wait again - practice anytime",
          icon: "🎯",
        };
      
      case 'difficulty_locked':
        return {
          title: "Ready for the next level? 🚀",
          subtitle: "Unlock Yellow and Red difficulties",
          primaryBenefit: "Challenge yourself with realistic scenarios",
          icon: "💪",
        };
      
      case 'scenario_locked':
        return {
          title: "Explore premium scenarios 🎨",
          subtitle: "Master conversations in exclusive environments",
          primaryBenefit: "Practice in gyms, bars, and galleries",
          icon: "🏆",
        };
      
      default:
        return {
          title: "Unlock your full potential 💫",
          subtitle: "Get FlirtCraft Plus for unlimited practice",
          primaryBenefit: "Become confident in any social situation",
          icon: "⭐",
        };
    }
  };
  
  const content = getPaywallContent();
  
  const handlePurchase = async () => {
    const product = products.find(p => 
      selectedProduct === 'monthly' 
        ? p.period === 'monthly' 
        : p.period === 'annual'
    );
    
    if (product) {
      await purchaseSubscription(product.id);
    }
  };
  
  const handleClose = () => {
    const timeOnScreen = Date.now() - impressionStartTime.current;
    
    trackEvent('paywall_dismissed', {
      paywall_type: paywallType,
      time_on_screen_ms: timeOnScreen,
      selected_product: selectedProduct,
    });
    
    hidePaywall();
  };
  
  return (
    <Modal
      visible={paywallVisible}
      animationType="none"
      transparent={true}
      onRequestClose={handleClose}
    >
      <Animated.View
        entering={FadeIn}
        exiting={FadeOut}
        style={{
          flex: 1,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
        }}
      >
        <Animated.View
          entering={SlideInUp.springify()}
          exiting={SlideOutDown}
          style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            maxHeight: SCREEN_HEIGHT * 0.9,
            backgroundColor: 'white',
            borderTopLeftRadius: 24,
            borderTopRightRadius: 24,
          }}
        >
          <ScrollView showsVerticalScrollIndicator={false}>
            <VStack space={6} p={6}>
              {/* Header */}
              <HStack justifyContent="space-between" alignItems="center">
                <Box flex={1} />
                <Text fontSize="4xl">{content.icon}</Text>
                <IconButton
                  icon={<Icon name="close" />}
                  onPress={handleClose}
                  position="absolute"
                  right={-12}
                  top={-12}
                />
              </HStack>
              
              {/* Title Section */}
              <VStack space={2} alignItems="center">
                <Text 
                  fontSize="2xl" 
                  fontWeight="bold" 
                  textAlign="center"
                  color="gray.800"
                >
                  {content.title}
                </Text>
                <Text 
                  fontSize="md" 
                  textAlign="center"
                  color="gray.600"
                >
                  {content.subtitle}
                </Text>
                <Box
                  bg="orange.100"
                  px={3}
                  py={2}
                  borderRadius="full"
                  mt={2}
                >
                  <Text fontSize="sm" color="orange.700" fontWeight="600">
                    {content.primaryBenefit}
                  </Text>
                </Box>
              </VStack>
              
              {/* Benefits Comparison */}
              <BenefitsComparison />
              
              {/* Testimonials */}
              <TestimonialCarousel />
              
              {/* Pricing Selector */}
              <PricingSelector
                products={products}
                selectedProduct={selectedProduct}
                onSelectProduct={setSelectedProduct}
              />
              
              {/* CTA Buttons */}
              <VStack space={3}>
                <Button
                  size="lg"
                  colorScheme="orange"
                  onPress={handlePurchase}
                  isLoading={isLoading}
                  _text={{ fontWeight: '600' }}
                >
                  Start 3-Day Free Trial
                </Button>
                
                <Text 
                  fontSize="xs" 
                  color="gray.500" 
                  textAlign="center"
                >
                  Cancel anytime. Renews automatically.
                </Text>
                
                <Button
                  variant="ghost"
                  onPress={handleClose}
                  _text={{ color: 'gray.600' }}
                >
                  Maybe Later
                </Button>
              </VStack>
              
              {/* Trust Badges */}
              <HStack justifyContent="center" space={4} pt={2}>
                <Image 
                  source={require('@/assets/secure-payment.png')} 
                  h={8} 
                  alt="Secure Payment"
                />
                <Image 
                  source={require('@/assets/app-store.png')} 
                  h={8} 
                  alt="App Store"
                />
                <Image 
                  source={require('@/assets/google-play.png')} 
                  h={8} 
                  alt="Google Play"
                />
              </HStack>
            </VStack>
          </ScrollView>
        </Animated.View>
      </Animated.View>
    </Modal>
  );
};
```

### Daily Limit Reached Screen
```typescript
// screens/DailyLimitScreen.tsx
import React from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Box, VStack, Text, Button, Center } from 'native-base';
import { CountdownTimer } from '@/components/CountdownTimer';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import LottieView from 'lottie-react-native';

export const DailyLimitScreen: React.FC = () => {
  const { 
    timeUntilReset, 
    showPaywall,
    conversationsToday 
  } = useSubscriptionStore();
  
  const handleUpgrade = () => {
    showPaywall('daily_limit', 'limit_screen');
  };
  
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#F9FAFB' }}>
      <VStack flex={1} justifyContent="center" alignItems="center" px={8}>
        {/* Animation */}
        <LottieView
          source={require('@/assets/animations/hourglass.json')}
          autoPlay
          loop
          style={{ width: 200, height: 200 }}
        />
        
        {/* Message */}
        <VStack space={4} alignItems="center" mt={8}>
          <Text fontSize="2xl" fontWeight="bold" color="gray.800">
            Daily Limit Reached
          </Text>
          
          <Text fontSize="md" color="gray.600" textAlign="center">
            You've used your free conversation for today.
            Come back tomorrow or upgrade for unlimited practice!
          </Text>
          
          {/* Countdown Timer */}
          <Box
            bg="gray.100"
            px={6}
            py={4}
            borderRadius="xl"
            mt={4}
          >
            <VStack alignItems="center" space={2}>
              <Text fontSize="sm" color="gray.600">
                Next free conversation in:
              </Text>
              <CountdownTimer 
                targetTime={Date.now() + timeUntilReset}
                onComplete={() => {
                  // Refresh subscription status
                  checkSubscriptionStatus();
                }}
              />
            </VStack>
          </Box>
          
          {/* Stats */}
          <HStack space={8} mt={6}>
            <VStack alignItems="center">
              <Text fontSize="2xl" fontWeight="bold" color="orange.500">
                {conversationsToday}
              </Text>
              <Text fontSize="sm" color="gray.600">
                Today
              </Text>
            </VStack>
            
            <VStack alignItems="center">
              <Text fontSize="2xl" fontWeight="bold" color="gray.400">
                1
              </Text>
              <Text fontSize="sm" color="gray.600">
                Daily Limit
              </Text>
            </VStack>
          </HStack>
          
          {/* CTA */}
          <VStack space={3} w="100%" mt={8}>
            <Button
              size="lg"
              colorScheme="orange"
              onPress={handleUpgrade}
              _text={{ fontWeight: '600' }}
            >
              Get Unlimited Conversations
            </Button>
            
            <Button
              variant="outline"
              onPress={() => navigation.goBack()}
            >
              Set Reminder for Tomorrow
            </Button>
          </VStack>
        </VStack>
      </VStack>
    </SafeAreaView>
  );
};
```

## Analytics Implementation

### Event Tracking
```typescript
// analytics/subscriptionEvents.ts
export const subscriptionAnalytics = {
  // Paywall events
  paywallShown: (type: string, trigger: string) => {
    trackEvent('paywall_shown', {
      paywall_type: type,
      trigger_source: trigger,
      user_days_active: getUserDaysActive(),
      conversations_completed: getConversationsCount(),
      time_since_install: getTimeSinceInstall(),
    });
  },
  
  trialStarted: (trigger: string) => {
    trackEvent('trial_started', {
      trigger_point: trigger,
      time_to_trial_minutes: getTimeToTrial(),
      conversations_before_trial: getConversationsCount(),
    });
    
    // RevenueCat attribution
    Purchases.setAttributes({
      trial_start_trigger: trigger,
      trial_start_date: new Date().toISOString(),
    });
  },
  
  subscriptionPurchased: (productId: string, price: number) => {
    trackEvent('subscription_purchased', {
      product_id: productId,
      price_amount: price,
      is_trial_conversion: isTrialUser(),
      days_since_install: getDaysSinceInstall(),
    });
    
    // Revenue tracking
    trackRevenue(price, 'subscription', { product_id: productId });
  },
  
  // Feature usage
  premiumFeatureUsed: (feature: string) => {
    trackEvent('premium_feature_used', {
      feature_name: feature,
      subscription_type: getSubscriptionType(),
      days_as_premium: getDaysAsPremium(),
    });
  },
  
  // Retention events  
  subscriptionRenewed: () => {
    trackEvent('subscription_renewed', {
      renewal_count: getRenewalCount(),
      total_revenue: getTotalRevenue(),
      days_subscribed: getDaysSubscribed(),
    });
  },
  
  subscriptionCancelled: (reason?: string) => {
    trackEvent('subscription_cancelled', {
      cancellation_reason: reason,
      days_subscribed: getDaysSubscribed(),
      lifetime_value: getLifetimeValue(),
      will_expire_date: getExpirationDate(),
    });
  },
};
```

## Testing

### Subscription Testing
```typescript
// __tests__/subscription.test.ts
import { renderHook, act } from '@testing-library/react-native';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import Purchases from 'react-native-purchases';

jest.mock('react-native-purchases');

describe('Subscription Management', () => {
  beforeEach(() => {
    useSubscriptionStore.getState().reset();
  });
  
  test('initializes with free tier by default', async () => {
    const { result } = renderHook(() => useSubscriptionStore());
    
    await act(async () => {
      await result.current.initializeSubscription();
    });
    
    expect(result.current.subscription?.type).toBe('free');
    expect(result.current.canStartConversation).toBe(true);
    expect(result.current.hasFeature('unlimitedConversations')).toBe(false);
  });
  
  test('enforces daily limit for free users', () => {
    const { result } = renderHook(() => useSubscriptionStore());
    
    act(() => {
      result.current.incrementDailyUsage();
    });
    
    expect(result.current.conversationsToday).toBe(1);
    expect(result.current.canStartConversation).toBe(false);
  });
  
  test('allows unlimited for premium users', async () => {
    const { result } = renderHook(() => useSubscriptionStore());
    
    // Mock premium subscription
    (Purchases.getCustomerInfo as jest.Mock).mockResolvedValue({
      entitlements: {
        active: {
          premium: { isActive: true, willRenew: true }
        }
      }
    });
    
    await act(async () => {
      await result.current.initializeSubscription();
    });
    
    // Test unlimited usage
    for (let i = 0; i < 10; i++) {
      act(() => {
        result.current.incrementDailyUsage();
      });
    }
    
    expect(result.current.canStartConversation).toBe(true);
  });
  
  test('shows correct paywall based on trigger', () => {
    const { result } = renderHook(() => useSubscriptionStore());
    
    act(() => {
      result.current.showPaywall('daily_limit', 'test_trigger');
    });
    
    expect(result.current.paywallVisible).toBe(true);
    expect(result.current.paywallType).toBe('daily_limit');
  });
});
```

## Performance Optimizations

### Subscription Caching
```typescript
// utils/subscriptionCache.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

const CACHE_KEY = 'subscription_cache';
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

export const subscriptionCache = {
  set: async (data: Subscription) => {
    await AsyncStorage.setItem(CACHE_KEY, JSON.stringify({
      data,
      timestamp: Date.now(),
    }));
  },
  
  get: async (): Promise<Subscription | null> => {
    const cached = await AsyncStorage.getItem(CACHE_KEY);
    if (!cached) return null;
    
    const { data, timestamp } = JSON.parse(cached);
    
    if (Date.now() - timestamp > CACHE_DURATION) {
      await AsyncStorage.removeItem(CACHE_KEY);
      return null;
    }
    
    return data;
  },
  
  clear: async () => {
    await AsyncStorage.removeItem(CACHE_KEY);
  },
};
```

## Last Updated
- **Version 2.0.0**: Complete RevenueCat integration with Supabase backend
- **Focus**: Production-ready subscription management with A/B testing framework
- **Features**: Webhook processing, feature gating, usage tracking, analytics, deployment checklist
- **Products**: flirtcraft_plus_monthly ($9.99), flirtcraft_plus_annual ($95.99) with 3-day trials
- **Architecture**: Seamless integration with existing Supabase infrastructure
- **Next**: Machine learning-based churn prediction and personalized retention campaigns