# FlirtCraft Premium Architecture - RevenueCat Integration

---
**Document**: Technical Architecture for Premium Monetization  
**Stack**: React Native/Expo + Supabase + FastAPI + RevenueCat  
**Focus**: Subscription management and feature gating implementation  
**Version**: 1.0.0  
**Last Updated**: 2025-08-26
---

## Executive Summary

This document provides implementation-ready architecture for integrating RevenueCat subscription management with FlirtCraft's existing React Native/Expo + Supabase + FastAPI stack. The architecture supports a freemium model with Free (1 conversation/day, Green difficulty only) and Premium ($9.99/month, unlimited conversations, all features) tiers.

### Key Integration Points
- **RevenueCat SDK**: Subscription lifecycle management  
- **Supabase Extensions**: User subscription state persistence  
- **FastAPI Webhooks**: Server-side subscription validation  
- **Feature Gating**: Real-time premium access control  
- **Daily Limits**: Automatic reset and enforcement  

## Technology Stack Decisions

### Frontend Architecture
**React Native/Expo Framework**: Maintains existing setup
- **RevenueCat SDK**: `react-native-purchases` for subscription management
- **State Management**: Zustand for subscription state with React Query for server sync
- **Feature Gating**: Higher-order components and custom hooks
- **UI Components**: Existing Native Base components extended for paywalls

**Rationale**: Leverages existing infrastructure while adding minimal complexity. RevenueCat's React Native SDK provides robust subscription handling with App Store/Google Play integration.

### Backend Architecture  
**Supabase Extensions**: Database schema extensions for subscription tracking
- **User Subscriptions Table**: Centralized subscription state
- **Daily Usage Tracking**: Conversation limits and reset logic
- **Premium Feature Usage**: Analytics and feature adoption tracking

**FastAPI Webhook Handler**: Server-side subscription event processing
- **RevenueCat Webhooks**: Real-time subscription status updates
- **Supabase Integration**: Automatic user state synchronization
- **Event Logging**: Comprehensive subscription event tracking

**Rationale**: Extends existing Supabase architecture without requiring new services. FastAPI webhook handler ensures reliable server-side validation and state consistency.

## System Component Architecture

### Core Components

#### 1. Subscription Management Layer
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React Native)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │ Subscription    │  │ Feature Gating  │  │ Paywall UI      ││
│  │ Store (Zustand) │  │ Components      │  │ Components      ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │ RevenueCat SDK  │  │ Supabase Client │  │ React Query     ││
│  │ (Purchases)     │  │ (Auth + DB)     │  │ (Data Sync)     ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend Services                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │ FastAPI         │  │ Supabase        │  │ RevenueCat      ││
│  │ Webhook Handler │  │ Database        │  │ Webhooks        ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

#### 2. Data Flow Architecture
```
User Action (Purchase) → RevenueCat → App Store/Google Play
                           │              │
                           ▼              ▼
                    Webhook Event   Receipt Validation
                           │              │
                           ▼              ▼
                  FastAPI Handler ← → RevenueCat API
                           │
                           ▼
                  Supabase Database Update
                           │
                           ▼
                  Frontend State Refresh
```

#### 3. Feature Access Control
```
User Request → Feature Gate Check → Subscription Store
                       │                    │
                       ▼                    ▼
               Feature Enabled?    ← Subscription Status
                       │                    │
               ┌───────┴───────┐           ▼
               ▼               ▼    Daily Usage Check
        Allow Access    Show Paywall        │
                                           ▼
                                    Usage Limits OK?
```

## Data Architecture Specifications

### Database Schema Extensions (Supabase)

#### User Subscriptions Table
```sql
-- Extend existing users table with subscription tracking
ALTER TABLE users ADD COLUMN IF NOT EXISTS revenue_cat_id VARCHAR(255) UNIQUE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'free';
ALTER TABLE users ADD COLUMN IF NOT EXISTS daily_conversations_used INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_reset_date DATE DEFAULT CURRENT_DATE;

-- Dedicated subscription management table
CREATE TABLE user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Subscription details
    subscription_type VARCHAR(20) NOT NULL CHECK (subscription_type IN ('free', 'premium', 'trial')),
    subscription_status VARCHAR(20) NOT NULL CHECK (subscription_status IN ('active', 'cancelled', 'expired', 'grace_period')),
    product_id VARCHAR(100), -- flirtcraft_plus_monthly, flirtcraft_plus_annual
    
    -- RevenueCat integration
    revenue_cat_customer_id VARCHAR(255) UNIQUE NOT NULL,
    original_purchase_date TIMESTAMP WITH TIME ZONE,
    expires_date TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    
    -- Usage tracking
    daily_conversations_limit INTEGER DEFAULT 1,
    daily_conversations_used INTEGER DEFAULT 0,
    last_reset_date DATE DEFAULT CURRENT_DATE,
    
    -- Feature access flags
    has_unlimited_conversations BOOLEAN DEFAULT FALSE,
    has_all_difficulties BOOLEAN DEFAULT FALSE,
    has_premium_scenarios BOOLEAN DEFAULT FALSE,
    has_advanced_analytics BOOLEAN DEFAULT FALSE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT unique_user_subscription UNIQUE(user_id)
);

-- Premium feature usage analytics
CREATE TABLE premium_feature_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL, -- 'difficulty_yellow', 'scenario_premium', 'unlimited_conversations'
    usage_count INTEGER DEFAULT 1,
    first_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscription events for analytics
CREATE TABLE subscription_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- 'trial_started', 'purchased', 'renewed', 'cancelled'
    revenue_cat_event_id VARCHAR(255),
    product_id VARCHAR(100),
    price_amount_cents INTEGER,
    currency VARCHAR(3),
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- Indexes for performance
CREATE INDEX idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX idx_user_subscriptions_revenue_cat ON user_subscriptions(revenue_cat_customer_id);
CREATE INDEX idx_premium_feature_usage_user ON premium_feature_usage(user_id, feature_name);
CREATE INDEX idx_subscription_events_user ON subscription_events(user_id);

-- Row Level Security
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE premium_feature_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own subscription" ON user_subscriptions
    FOR SELECT USING (auth.uid() = user_id);
    
CREATE POLICY "Users can view own feature usage" ON premium_feature_usage
    FOR SELECT USING (auth.uid() = user_id);
```

### Entity Relationships
```
users (existing)
  ├── user_subscriptions (1:1)
  ├── premium_feature_usage (1:many)
  └── subscription_events (1:many)

user_subscriptions
  ├── revenue_cat_customer_id (unique identifier)
  ├── subscription_status (active/cancelled/expired)
  ├── daily usage tracking
  └── feature access flags
```

## RevenueCat Configuration

### Product Configuration
```typescript
// RevenueCat Dashboard Configuration
const PRODUCTS = {
  monthly: {
    identifier: 'flirtcraft_plus_monthly',
    price: '$9.99',
    period: 'P1M', // 1 month
    trial_period: 'P3D', // 3 days
  },
  annual: {
    identifier: 'flirtcraft_plus_annual', 
    price: '$95.99',
    period: 'P1Y', // 1 year
    trial_period: 'P3D', // 3 days
    discount: '20% off monthly'
  }
};

// Entitlement Configuration
const ENTITLEMENTS = {
  premium: {
    identifier: 'premium',
    products: ['flirtcraft_plus_monthly', 'flirtcraft_plus_annual'],
    description: 'Premium FlirtCraft features'
  }
};

// Offerings Setup
const OFFERINGS = {
  default: {
    identifier: 'default',
    description: 'FlirtCraft Plus Subscription',
    packages: [
      {
        identifier: 'monthly',
        product_identifier: 'flirtcraft_plus_monthly'
      },
      {
        identifier: 'annual', 
        product_identifier: 'flirtcraft_plus_annual'
      }
    ]
  }
};
```

### SDK Initialization
```typescript
// app/config/revenueCat.ts
import Purchases, { LOG_LEVEL } from 'react-native-purchases';
import { Platform } from 'react-native';

const REVENUE_CAT_CONFIG = {
  apiKey: Platform.select({
    ios: process.env.EXPO_PUBLIC_REVENUE_CAT_IOS_KEY!,
    android: process.env.EXPO_PUBLIC_REVENUE_CAT_ANDROID_KEY!,
  })!,
  appUserId: null, // Will be set after Supabase auth
  observerMode: false, // Full RevenueCat mode
  userDefaultsSuiteName: null,
  shouldShowInAppMessagesAutomatically: false,
};

export const initializeRevenueCat = async (userId: string) => {
  try {
    if (Platform.OS === 'ios') {
      await Purchases.configure({
        apiKey: REVENUE_CAT_CONFIG.apiKey,
        appUserId: userId,
      });
    } else {
      await Purchases.configure({
        apiKey: REVENUE_CAT_CONFIG.apiKey,
        appUserId: userId,
      });
    }

    // Set debug logging in development
    if (__DEV__) {
      Purchases.setLogLevel(LOG_LEVEL.DEBUG);
    }

    // Set user attributes for analytics
    Purchases.setAttributes({
      user_id: userId,
      platform: Platform.OS,
      app_version: process.env.EXPO_PUBLIC_VERSION,
    });

    console.log('RevenueCat initialized successfully');
  } catch (error) {
    console.error('RevenueCat initialization failed:', error);
    throw error;
  }
};
```

## React Native Integration

### Subscription Store (Zustand)
```typescript
// stores/subscriptionStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Purchases, { CustomerInfo, PurchasesOffering } from 'react-native-purchases';
import { supabase } from '@/lib/supabase';

interface SubscriptionFeatures {
  unlimitedConversations: boolean;
  allDifficulties: boolean;
  premiumScenarios: boolean;
  advancedAnalytics: boolean;
}

interface SubscriptionState {
  // Subscription status
  isPremium: boolean;
  isTrialActive: boolean;
  subscriptionType: 'free' | 'premium' | 'trial';
  expirationDate: Date | null;
  
  // Daily usage
  dailyConversationsUsed: number;
  dailyLimit: number;
  canStartConversation: boolean;
  resetTime: Date | null;
  
  // Features
  features: SubscriptionFeatures;
  
  // RevenueCat data
  customerInfo: CustomerInfo | null;
  offerings: PurchasesOffering | null;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  
  // Actions
  initializeSubscription: () => Promise<void>;
  checkSubscriptionStatus: () => Promise<void>;
  purchaseSubscription: (packageType: string) => Promise<boolean>;
  restorePurchases: () => Promise<boolean>;
  incrementDailyUsage: () => Promise<void>;
  resetDailyUsage: () => void;
  
  // Feature checks
  canAccessDifficulty: (difficulty: 'green' | 'yellow' | 'red') => boolean;
  canAccessScenario: (scenarioId: string) => boolean;
  hasFeature: (feature: keyof SubscriptionFeatures) => boolean;
}

export const useSubscriptionStore = create<SubscriptionState>()(
  persist(
    (set, get) => ({
      // Initial state
      isPremium: false,
      isTrialActive: false,
      subscriptionType: 'free',
      expirationDate: null,
      dailyConversationsUsed: 0,
      dailyLimit: 1,
      canStartConversation: true,
      resetTime: null,
      features: {
        unlimitedConversations: false,
        allDifficulties: false,
        premiumScenarios: false,
        advancedAnalytics: false,
      },
      customerInfo: null,
      offerings: null,
      isLoading: false,
      error: null,
      
      initializeSubscription: async () => {
        set({ isLoading: true, error: null });
        
        try {
          // Get current user
          const { data: { user }, error: authError } = await supabase.auth.getUser();
          if (authError || !user) {
            throw new Error('User not authenticated');
          }
          
          // Initialize RevenueCat with user ID
          await initializeRevenueCat(user.id);
          
          // Get customer info
          const customerInfo = await Purchases.getCustomerInfo();
          
          // Get offerings
          const offerings = await Purchases.getOfferings();
          
          // Check subscription status
          const isPremium = customerInfo.entitlements.active['premium'] !== undefined;
          const isTrialActive = customerInfo.entitlements.active['premium']?.isActive && 
                               !customerInfo.entitlements.active['premium']?.willRenew;
          
          // Get subscription from database
          const { data: subscription } = await supabase
            .from('user_subscriptions')
            .select('*')
            .eq('user_id', user.id)
            .single();
          
          // Create subscription record if it doesn't exist
          if (!subscription && isPremium) {
            await supabase
              .from('user_subscriptions')
              .insert({
                user_id: user.id,
                revenue_cat_customer_id: customerInfo.originalAppUserId,
                subscription_type: isTrialActive ? 'trial' : 'premium',
                subscription_status: 'active',
                has_unlimited_conversations: true,
                has_all_difficulties: true,
                has_premium_scenarios: true,
                has_advanced_analytics: true,
              });
          }
          
          // Update state
          set({
            isPremium,
            isTrialActive,
            subscriptionType: isPremium ? (isTrialActive ? 'trial' : 'premium') : 'free',
            customerInfo,
            offerings: offerings.current,
            features: {
              unlimitedConversations: isPremium,
              allDifficulties: isPremium,
              premiumScenarios: isPremium,
              advancedAnalytics: isPremium,
            },
            dailyLimit: isPremium ? 999 : 1,
            isLoading: false,
          });
          
          // Check daily usage
          await get().checkDailyUsage();
          
        } catch (error) {
          console.error('Subscription initialization failed:', error);
          set({ 
            error: error.message,
            isLoading: false,
            subscriptionType: 'free',
            features: {
              unlimitedConversations: false,
              allDifficulties: false, 
              premiumScenarios: false,
              advancedAnalytics: false,
            }
          });
        }
      },
      
      checkSubscriptionStatus: async () => {
        try {
          const customerInfo = await Purchases.getCustomerInfo();
          const isPremium = customerInfo.entitlements.active['premium'] !== undefined;
          
          if (get().isPremium !== isPremium) {
            // Subscription status changed, reinitialize
            await get().initializeSubscription();
          }
        } catch (error) {
          console.error('Failed to check subscription status:', error);
        }
      },
      
      purchaseSubscription: async (packageType: string) => {
        set({ isLoading: true, error: null });
        
        try {
          const offerings = get().offerings;
          if (!offerings) {
            throw new Error('No offerings available');
          }
          
          const packageToPurchase = offerings.availablePackages.find(
            pkg => pkg.identifier === packageType
          );
          
          if (!packageToPurchase) {
            throw new Error('Package not found');
          }
          
          const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
          
          // Check if purchase was successful
          const isPremium = customerInfo.entitlements.active['premium'] !== undefined;
          
          if (isPremium) {
            // Update subscription in database
            const { data: { user } } = await supabase.auth.getUser();
            if (user) {
              await supabase
                .from('user_subscriptions')
                .upsert({
                  user_id: user.id,
                  revenue_cat_customer_id: customerInfo.originalAppUserId,
                  subscription_type: 'premium',
                  subscription_status: 'active',
                  product_id: packageToPurchase.product.identifier,
                  has_unlimited_conversations: true,
                  has_all_difficulties: true,
                  has_premium_scenarios: true,
                  has_advanced_analytics: true,
                });
              
              // Log subscription event
              await supabase
                .from('subscription_events')
                .insert({
                  user_id: user.id,
                  event_type: 'purchased',
                  product_id: packageToPurchase.product.identifier,
                  price_amount_cents: Math.round(packageToPurchase.product.price * 100),
                  currency: packageToPurchase.product.currencyCode,
                });
            }
            
            // Update local state
            set({
              isPremium: true,
              subscriptionType: 'premium',
              features: {
                unlimitedConversations: true,
                allDifficulties: true,
                premiumScenarios: true,
                advancedAnalytics: true,
              },
              dailyLimit: 999,
              customerInfo,
              isLoading: false,
            });
            
            return true;
          }
          
          throw new Error('Purchase did not activate subscription');
          
        } catch (error) {
          console.error('Purchase failed:', error);
          set({ 
            error: error.code === 'USER_CANCELLED' ? null : error.message,
            isLoading: false 
          });
          return false;
        }
      },
      
      restorePurchases: async () => {
        set({ isLoading: true, error: null });
        
        try {
          const customerInfo = await Purchases.restorePurchases();
          const isPremium = customerInfo.entitlements.active['premium'] !== undefined;
          
          if (isPremium) {
            await get().initializeSubscription();
            return true;
          }
          
          set({ isLoading: false });
          return false;
          
        } catch (error) {
          console.error('Restore failed:', error);
          set({ error: error.message, isLoading: false });
          return false;
        }
      },
      
      incrementDailyUsage: async () => {
        const current = get().dailyConversationsUsed;
        const newCount = current + 1;
        
        set({ dailyConversationsUsed: newCount });
        
        // Update in database
        const { data: { user } } = await supabase.auth.getUser();
        if (user) {
          await supabase
            .from('user_subscriptions')
            .update({ 
              daily_conversations_used: newCount,
              last_reset_date: new Date().toDateString()
            })
            .eq('user_id', user.id);
        }
        
        // Check if can start another conversation
        const canStart = get().isPremium || newCount < get().dailyLimit;
        set({ canStartConversation: canStart });
      },
      
      resetDailyUsage: () => {
        set({ 
          dailyConversationsUsed: 0, 
          canStartConversation: true 
        });
      },
      
      checkDailyUsage: async () => {
        const { data: { user } } = await supabase.auth.getUser();
        if (!user) return;
        
        const { data: subscription } = await supabase
          .from('user_subscriptions')
          .select('daily_conversations_used, last_reset_date')
          .eq('user_id', user.id)
          .single();
        
        if (subscription) {
          const today = new Date().toDateString();
          const lastReset = subscription.last_reset_date;
          
          if (lastReset !== today) {
            // Reset for new day
            get().resetDailyUsage();
            await supabase
              .from('user_subscriptions')
              .update({ 
                daily_conversations_used: 0,
                last_reset_date: today
              })
              .eq('user_id', user.id);
          } else {
            // Use existing count
            const canStart = get().isPremium || subscription.daily_conversations_used < get().dailyLimit;
            set({ 
              dailyConversationsUsed: subscription.daily_conversations_used,
              canStartConversation: canStart
            });
          }
        }
      },
      
      canAccessDifficulty: (difficulty) => {
        if (difficulty === 'green') return true;
        return get().features.allDifficulties;
      },
      
      canAccessScenario: (scenarioId) => {
        const premiumScenarios = ['gym', 'bar', 'gallery'];
        if (!premiumScenarios.includes(scenarioId)) return true;
        return get().features.premiumScenarios;
      },
      
      hasFeature: (feature) => {
        return get().features[feature];
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
        dailyConversationsUsed: state.dailyConversationsUsed,
        isPremium: state.isPremium,
        subscriptionType: state.subscriptionType,
        features: state.features,
      }),
    }
  )
);
```

### Feature Gating Components
```typescript
// components/PremiumGate.tsx
import React from 'react';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { PaywallModal } from './PaywallModal';

interface PremiumGateProps {
  feature: 'unlimitedConversations' | 'allDifficulties' | 'premiumScenarios' | 'advancedAnalytics';
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onBlocked?: () => void;
}

export const PremiumGate: React.FC<PremiumGateProps> = ({
  feature,
  children,
  fallback = null,
  onBlocked,
}) => {
  const hasFeature = useSubscriptionStore(state => state.hasFeature(feature));
  const [showPaywall, setShowPaywall] = React.useState(false);
  
  if (!hasFeature) {
    React.useEffect(() => {
      if (onBlocked) {
        onBlocked();
      } else {
        setShowPaywall(true);
      }
    }, [onBlocked]);
    
    return (
      <>
        {fallback}
        {showPaywall && (
          <PaywallModal
            visible={showPaywall}
            onClose={() => setShowPaywall(false)}
            trigger={`feature_${feature}`}
          />
        )}
      </>
    );
  }
  
  return <>{children}</>;
};

// components/ConversationGate.tsx
import React from 'react';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { DailyLimitReachedScreen } from '@/screens/DailyLimitReachedScreen';

interface ConversationGateProps {
  children: React.ReactNode;
}

export const ConversationGate: React.FC<ConversationGateProps> = ({ children }) => {
  const canStartConversation = useSubscriptionStore(state => state.canStartConversation);
  const incrementDailyUsage = useSubscriptionStore(state => state.incrementDailyUsage);
  
  React.useEffect(() => {
    if (canStartConversation) {
      // Mark conversation as started
      incrementDailyUsage();
    }
  }, [canStartConversation, incrementDailyUsage]);
  
  if (!canStartConversation) {
    return <DailyLimitReachedScreen />;
  }
  
  return <>{children}</>;
};
```

### Paywall Components
```typescript
// components/PaywallModal.tsx
import React from 'react';
import { Modal, ScrollView, Dimensions } from 'react-native';
import { Box, VStack, HStack, Text, Button, IconButton, Center } from 'native-base';
import Animated, { FadeIn, SlideInUp } from 'react-native-reanimated';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { PricingCard } from './PricingCard';

interface PaywallModalProps {
  visible: boolean;
  onClose: () => void;
  trigger: string;
}

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

export const PaywallModal: React.FC<PaywallModalProps> = ({ visible, onClose, trigger }) => {
  const { offerings, purchaseSubscription, isLoading } = useSubscriptionStore();
  const [selectedPackage, setSelectedPackage] = React.useState('monthly');
  
  const handlePurchase = async () => {
    const success = await purchaseSubscription(selectedPackage);
    if (success) {
      onClose();
    }
  };
  
  return (
    <Modal visible={visible} animationType="none" transparent onRequestClose={onClose}>
      <Animated.View
        entering={FadeIn}
        style={{ 
          flex: 1, 
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          justifyContent: 'flex-end'
        }}
      >
        <Animated.View
          entering={SlideInUp.springify()}
          style={{
            backgroundColor: 'white',
            borderTopLeftRadius: 24,
            borderTopRightRadius: 24,
            maxHeight: SCREEN_HEIGHT * 0.85,
          }}
        >
          <ScrollView>
            <VStack space={6} p={6}>
              {/* Header */}
              <HStack justifyContent="space-between" alignItems="center">
                <Box />
                <Text fontSize="3xl">🚀</Text>
                <IconButton 
                  icon={<Text>✕</Text>}
                  onPress={onClose}
                />
              </HStack>
              
              {/* Title */}
              <VStack alignItems="center" space={3}>
                <Text fontSize="2xl" fontWeight="bold" textAlign="center">
                  Unlock FlirtCraft Plus
                </Text>
                <Text fontSize="md" color="gray.600" textAlign="center">
                  Get unlimited conversations and premium features
                </Text>
              </VStack>
              
              {/* Features */}
              <VStack space={3}>
                <FeatureItem 
                  icon="💬" 
                  title="Unlimited Conversations" 
                  subtitle="Practice anytime, no daily limits"
                />
                <FeatureItem 
                  icon="🎯" 
                  title="All Difficulty Levels" 
                  subtitle="Yellow and Red challenges unlocked"
                />
                <FeatureItem 
                  icon="🏆" 
                  title="Premium Scenarios" 
                  subtitle="Gyms, bars, galleries and more"
                />
                <FeatureItem 
                  icon="📊" 
                  title="Advanced Analytics" 
                  subtitle="Detailed feedback and progress tracking"
                />
              </VStack>
              
              {/* Pricing */}
              <VStack space={3}>
                <Text fontSize="lg" fontWeight="600" textAlign="center">
                  Choose Your Plan
                </Text>
                
                <PricingCard
                  title="Monthly"
                  price="$9.99"
                  period="per month"
                  isSelected={selectedPackage === 'monthly'}
                  onSelect={() => setSelectedPackage('monthly')}
                  badge="3-day free trial"
                />
                
                <PricingCard
                  title="Annual"
                  price="$95.99"
                  period="per year"
                  originalPrice="$119.88"
                  isSelected={selectedPackage === 'annual'}
                  onSelect={() => setSelectedPackage('annual')}
                  badge="Save 20%"
                />
              </VStack>
              
              {/* CTA */}
              <VStack space={3}>
                <Button
                  size="lg"
                  colorScheme="orange"
                  onPress={handlePurchase}
                  isLoading={isLoading}
                  _text={{ fontWeight: '600' }}
                >
                  Start Free Trial
                </Button>
                
                <Text fontSize="xs" color="gray.500" textAlign="center">
                  Cancel anytime. Auto-renews after trial.
                </Text>
              </VStack>
            </VStack>
          </ScrollView>
        </Animated.View>
      </Animated.View>
    </Modal>
  );
};

const FeatureItem: React.FC<{ icon: string; title: string; subtitle: string }> = ({
  icon, title, subtitle
}) => (
  <HStack space={3} alignItems="center">
    <Text fontSize="2xl">{icon}</Text>
    <VStack flex={1}>
      <Text fontSize="md" fontWeight="600">{title}</Text>
      <Text fontSize="sm" color="gray.600">{subtitle}</Text>
    </VStack>
  </HStack>
);
```

## FastAPI Webhook Handler

### Webhook Endpoint
```python
# api/webhooks/revenuecat.py
from fastapi import APIRouter, HTTPException, Request, Header, Depends
from fastapi.responses import JSONResponse
import hmac
import hashlib
import json
from datetime import datetime
from typing import Optional
from supabase import create_client
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Environment variables
REVENUE_CAT_WEBHOOK_SECRET = os.getenv("REVENUE_CAT_WEBHOOK_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize Supabase client with service role key
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class RevenueCatWebhookEvent(BaseModel):
    event_type: str
    app_user_id: str
    product_id: str
    period_type: str
    purchased_at_ms: int
    expiration_at_ms: Optional[int]
    environment: str
    presented_offering_identifier: Optional[str]
    transaction_id: str
    original_transaction_id: str
    is_family_share: bool
    country_code: str
    app_id: str
    entitlement_id: Optional[str]
    entitlement_ids: list[str]
    currency: str
    price: float
    price_in_purchased_currency: float
    subscriber_attributes: dict

def verify_webhook_signature(request_body: bytes, signature: str) -> bool:
    """Verify RevenueCat webhook signature"""
    if not REVENUE_CAT_WEBHOOK_SECRET:
        logging.warning("RevenueCat webhook secret not configured")
        return False
    
    expected_signature = hmac.new(
        REVENUE_CAT_WEBHOOK_SECRET.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@router.post("/revenuecat")
async def handle_revenuecat_webhook(
    request: Request,
    x_revenuecat_signature: str = Header(..., alias="X-RevenueCat-Signature")
):
    """Handle RevenueCat webhook events"""
    
    # Get request body
    body = await request.body()
    
    # Verify signature
    if not verify_webhook_signature(body, x_revenuecat_signature):
        logging.error("Invalid webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse webhook data
    try:
        webhook_data = json.loads(body)
        event = RevenueCatWebhookEvent(**webhook_data["event"])
    except Exception as e:
        logging.error(f"Failed to parse webhook data: {e}")
        raise HTTPException(status_code=400, detail="Invalid webhook data")
    
    # Skip sandbox events in production
    if event.environment == "SANDBOX" and os.getenv("ENVIRONMENT") == "production":
        return JSONResponse({"status": "ignored_sandbox"})
    
    # Process event based on type
    try:
        await process_subscription_event(event)
        
        # Log successful processing
        logging.info(f"Successfully processed {event.event_type} for user {event.app_user_id}")
        
        return JSONResponse({"status": "success"})
        
    except Exception as e:
        logging.error(f"Failed to process webhook event: {e}")
        raise HTTPException(status_code=500, detail="Failed to process event")

async def process_subscription_event(event: RevenueCatWebhookEvent):
    """Process subscription events and update database"""
    
    user_id = event.app_user_id
    
    # Get user from database
    user_result = await supabase.table("users").select("*").eq("id", user_id).execute()
    if not user_result.data:
        logging.error(f"User {user_id} not found")
        return
    
    user = user_result.data[0]
    
    # Process different event types
    if event.event_type in ["INITIAL_PURCHASE", "RENEWAL", "UNCANCELLATION"]:
        await handle_subscription_activation(event, user)
    
    elif event.event_type == "CANCELLATION":
        await handle_subscription_cancellation(event, user)
    
    elif event.event_type == "EXPIRATION":
        await handle_subscription_expiration(event, user)
    
    elif event.event_type == "BILLING_ISSUE":
        await handle_billing_issue(event, user)
    
    elif event.event_type in ["NON_RENEWING_PURCHASE", "PRODUCT_CHANGE"]:
        await handle_subscription_change(event, user)

async def handle_subscription_activation(event: RevenueCatWebhookEvent, user: dict):
    """Handle subscription activation events"""
    
    # Determine subscription type
    is_trial = event.event_type == "INITIAL_PURCHASE" and event.entitlement_ids
    subscription_type = "trial" if is_trial else "premium"
    
    # Calculate expiration date
    expiration_date = None
    if event.expiration_at_ms:
        expiration_date = datetime.fromtimestamp(event.expiration_at_ms / 1000)
    
    # Upsert subscription record
    subscription_data = {
        "user_id": user["id"],
        "revenue_cat_customer_id": event.app_user_id,
        "subscription_type": subscription_type,
        "subscription_status": "active",
        "product_id": event.product_id,
        "original_purchase_date": datetime.fromtimestamp(event.purchased_at_ms / 1000),
        "expires_date": expiration_date,
        "has_unlimited_conversations": True,
        "has_all_difficulties": True,
        "has_premium_scenarios": True,
        "has_advanced_analytics": True,
        "updated_at": datetime.utcnow()
    }
    
    await supabase.table("user_subscriptions").upsert(subscription_data).execute()
    
    # Log subscription event
    event_data = {
        "user_id": user["id"],
        "event_type": event.event_type.lower(),
        "revenue_cat_event_id": event.transaction_id,
        "product_id": event.product_id,
        "price_amount_cents": int(event.price * 100),
        "currency": event.currency,
        "metadata": {
            "environment": event.environment,
            "country_code": event.country_code,
            "is_family_share": event.is_family_share,
        }
    }
    
    await supabase.table("subscription_events").insert(event_data).execute()
    
    # Send activation email or push notification here
    # await send_subscription_welcome_email(user["email"])

async def handle_subscription_cancellation(event: RevenueCatWebhookEvent, user: dict):
    """Handle subscription cancellation"""
    
    # Update subscription status
    await supabase.table("user_subscriptions").update({
        "subscription_status": "cancelled",
        "updated_at": datetime.utcnow()
    }).eq("user_id", user["id"]).execute()
    
    # Log cancellation event
    event_data = {
        "user_id": user["id"],
        "event_type": "cancelled",
        "revenue_cat_event_id": event.transaction_id,
        "product_id": event.product_id,
    }
    
    await supabase.table("subscription_events").insert(event_data).execute()
    
    # Note: Don't immediately revoke access - wait until expiration

async def handle_subscription_expiration(event: RevenueCatWebhookEvent, user: dict):
    """Handle subscription expiration"""
    
    # Update subscription to expired and revoke premium features
    await supabase.table("user_subscriptions").update({
        "subscription_type": "free",
        "subscription_status": "expired", 
        "has_unlimited_conversations": False,
        "has_all_difficulties": False,
        "has_premium_scenarios": False,
        "has_advanced_analytics": False,
        "daily_conversations_limit": 1,
        "daily_conversations_used": 0,
        "updated_at": datetime.utcnow()
    }).eq("user_id", user["id"]).execute()
    
    # Log expiration event
    event_data = {
        "user_id": user["id"],
        "event_type": "expired",
        "revenue_cat_event_id": event.transaction_id,
        "product_id": event.product_id,
    }
    
    await supabase.table("subscription_events").insert(event_data).execute()

async def handle_billing_issue(event: RevenueCatWebhookEvent, user: dict):
    """Handle billing issues"""
    
    # Update subscription to grace period
    await supabase.table("user_subscriptions").update({
        "subscription_status": "grace_period",
        "updated_at": datetime.utcnow()
    }).eq("user_id", user["id"]).execute()
    
    # Send billing issue notification
    # await send_billing_issue_email(user["email"])

# Health check endpoint
@router.get("/revenuecat/health")
async def webhook_health():
    """Health check for webhook endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### Environment Configuration
```python
# .env
REVENUE_CAT_WEBHOOK_SECRET=your_webhook_secret_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
REVENUE_CAT_API_KEY=your_api_key_here

# Webhook URL to configure in RevenueCat dashboard
WEBHOOK_URL=https://your-api.com/webhooks/revenuecat
```

## Key Integration Points

### 1. Authentication Flow Integration
```typescript
// hooks/useAuthSubscription.ts
import { useEffect } from 'react';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { useAuth } from '@/contexts/AuthContext';

export const useAuthSubscription = () => {
  const { user } = useAuth();
  const { initializeSubscription } = useSubscriptionStore();
  
  useEffect(() => {
    if (user) {
      // Initialize subscription when user logs in
      initializeSubscription();
    }
  }, [user, initializeSubscription]);
};

// Usage in App.tsx
function App() {
  useAuthSubscription();
  
  return (
    // Your app components
  );
}
```

### 2. Daily Limit Enforcement
```typescript
// screens/ConversationScreen.tsx
import React from 'react';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { ConversationGate } from '@/components/ConversationGate';

export const ConversationScreen = () => {
  return (
    <ConversationGate>
      {/* Conversation UI only renders if user can start conversation */}
      <ConversationInterface />
    </ConversationGate>
  );
};
```

### 3. Premium Scenario Gating
```typescript
// screens/ScenarioSelectionScreen.tsx
import React from 'react';
import { FlatList } from 'react-native';
import { Box, Text, Pressable, Badge } from 'native-base';
import { useSubscriptionStore } from '@/stores/subscriptionStore';

const SCENARIOS = [
  { id: 'coffee', name: 'Coffee Shops', premium: false },
  { id: 'bookstore', name: 'Bookstores', premium: false },
  { id: 'gym', name: 'Gyms', premium: true },
  { id: 'bar', name: 'Bars', premium: true },
  { id: 'gallery', name: 'Galleries', premium: true },
];

export const ScenarioSelectionScreen = () => {
  const canAccessScenario = useSubscriptionStore(state => state.canAccessScenario);
  
  const renderScenario = ({ item }) => {
    const canAccess = canAccessScenario(item.id);
    
    return (
      <Pressable
        onPress={() => {
          if (!canAccess) {
            // Show paywall
            showPaywall('scenario_locked', item.id);
          } else {
            // Navigate to scenario
            navigation.navigate('PreConversation', { scenarioId: item.id });
          }
        }}
        opacity={canAccess ? 1 : 0.6}
      >
        <Box p={4} borderWidth={1} borderRadius="lg">
          <Text fontSize="lg" fontWeight="600">{item.name}</Text>
          {item.premium && !canAccess && (
            <Badge colorScheme="orange" position="absolute" top={2} right={2}>
              Premium
            </Badge>
          )}
        </Box>
      </Pressable>
    );
  };
  
  return (
    <FlatList
      data={SCENARIOS}
      renderItem={renderScenario}
      keyExtractor={item => item.id}
    />
  );
};
```

### 4. Real-time Subscription Sync
```typescript
// utils/subscriptionSync.ts
import { useEffect } from 'react';
import { AppState } from 'react-native';
import { useSubscriptionStore } from '@/stores/subscriptionStore';

export const useSubscriptionSync = () => {
  const checkSubscriptionStatus = useSubscriptionStore(state => state.checkSubscriptionStatus);
  
  useEffect(() => {
    const handleAppStateChange = (nextAppState: string) => {
      if (nextAppState === 'active') {
        // Check subscription status when app becomes active
        checkSubscriptionStatus();
      }
    };
    
    const subscription = AppState.addEventListener('change', handleAppStateChange);
    
    return () => subscription?.remove();
  }, [checkSubscriptionStatus]);
  
  // Also check periodically
  useEffect(() => {
    const interval = setInterval(() => {
      checkSubscriptionStatus();
    }, 5 * 60 * 1000); // Every 5 minutes
    
    return () => clearInterval(interval);
  }, [checkSubscriptionStatus]);
};
```

## Security and Performance Foundations

### Security Architecture
```typescript
// Security measures implemented:

// 1. Webhook signature verification
const verifyWebhookSignature = (body: string, signature: string) => {
  const expectedSignature = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(body)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature, 'hex'),
    Buffer.from(expectedSignature, 'hex')
  );
};

// 2. Row Level Security on subscription tables
CREATE POLICY "Users can only access own subscription" 
ON user_subscriptions FOR ALL 
USING (auth.uid() = user_id);

// 3. Server-side subscription validation
const validateSubscription = async (userId: string) => {
  const customerInfo = await Purchases.getCustomerInfo();
  const dbSubscription = await getSubscriptionFromDB(userId);
  
  // Verify RevenueCat and database are in sync
  const isValid = customerInfo.entitlements.active.premium !== undefined;
  const dbIsValid = dbSubscription?.subscription_status === 'active';
  
  if (isValid !== dbIsValid) {
    // Sync discrepancy - trigger reconciliation
    await reconcileSubscription(userId, customerInfo);
  }
  
  return isValid;
};
```

### Performance Architecture
```typescript
// Performance optimizations implemented:

// 1. Subscription state caching
const subscriptionCache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

// 2. Lazy loading of subscription data
const useSubscription = () => {
  const [subscription, setSubscription] = useState(null);
  
  useEffect(() => {
    // Only load subscription when actually needed
    const loadSubscription = async () => {
      const cached = subscriptionCache.get(userId);
      if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
        setSubscription(cached.data);
        return;
      }
      
      const fresh = await fetchSubscription(userId);
      subscriptionCache.set(userId, {
        data: fresh,
        timestamp: Date.now()
      });
      setSubscription(fresh);
    };
    
    loadSubscription();
  }, [userId]);
  
  return subscription;
};

// 3. Database query optimization
CREATE INDEX CONCURRENTLY idx_user_subscriptions_status 
ON user_subscriptions(user_id, subscription_status) 
WHERE subscription_status = 'active';

// 4. Batch daily usage updates
const batchUsageUpdates = new Map();
const flushUsageUpdates = async () => {
  const updates = Array.from(batchUsageUpdates.entries());
  batchUsageUpdates.clear();
  
  await supabase
    .from('user_subscriptions')
    .upsert(updates.map(([userId, usage]) => ({
      user_id: userId,
      daily_conversations_used: usage,
      last_reset_date: new Date().toDateString()
    })));
};

// Flush every 30 seconds
setInterval(flushUsageUpdates, 30000);
```

## Implementation Checklist

### Development Phase (Week 1-2)
- [ ] **Database Setup**
  - [ ] Run subscription schema migrations
  - [ ] Set up Row Level Security policies
  - [ ] Create database indexes for performance
  - [ ] Test database queries and constraints

- [ ] **RevenueCat Configuration**
  - [ ] Create RevenueCat account and configure products
  - [ ] Set up iOS and Android app configurations
  - [ ] Configure webhooks with proper secrets
  - [ ] Test sandbox purchases and webhooks

### Integration Phase (Week 3-4)
- [ ] **Frontend Implementation**
  - [ ] Install and configure RevenueCat SDK
  - [ ] Implement subscription store with Zustand
  - [ ] Create feature gating components
  - [ ] Build paywall UI components
  - [ ] Add subscription initialization to auth flow

- [ ] **Backend Implementation**
  - [ ] Create FastAPI webhook endpoint
  - [ ] Implement webhook signature verification
  - [ ] Add subscription event processing
  - [ ] Set up database synchronization
  - [ ] Configure environment variables

### Testing Phase (Week 5)
- [ ] **Functionality Testing**
  - [ ] Test subscription purchase flow
  - [ ] Verify webhook processing
  - [ ] Test daily limit enforcement
  - [ ] Verify feature gating works correctly
  - [ ] Test subscription restoration

- [ ] **Edge Case Testing**
  - [ ] Test network disconnection scenarios
  - [ ] Verify graceful degradation
  - [ ] Test subscription expiration handling
  - [ ] Verify billing issue processing

### Production Deployment (Week 6)
- [ ] **Production Setup**
  - [ ] Configure production RevenueCat environment
  - [ ] Set up production webhook endpoints
  - [ ] Configure monitoring and alerting
  - [ ] Set up analytics tracking

- [ ] **Launch Preparation**
  - [ ] Create App Store/Google Play subscription products
  - [ ] Submit for app store review
  - [ ] Prepare customer support documentation
  - [ ] Set up subscription analytics dashboards

## Analytics and Monitoring

### Key Metrics to Track
```typescript
// Analytics events for subscription funnel
const subscriptionAnalytics = {
  // Paywall interactions
  'paywall_shown': { trigger, paywall_type, user_days_active },
  'paywall_dismissed': { trigger, time_on_screen_ms },
  'trial_started': { trigger_point, time_to_trial_minutes },
  
  // Purchase events
  'subscription_purchased': { product_id, price, is_trial_conversion },
  'purchase_failed': { error_code, error_message, product_id },
  'subscription_restored': { products_restored },
  
  // Usage events
  'premium_feature_used': { feature_name, days_as_premium },
  'daily_limit_reached': { conversations_today, time_of_day },
  'difficulty_upgraded': { from_difficulty, to_difficulty },
  
  // Retention events
  'subscription_renewed': { renewal_count, total_revenue },
  'subscription_cancelled': { reason, days_subscribed, ltv },
  'subscription_reactivated': { days_cancelled, reactivation_trigger },
};

// Revenue tracking
const revenueMetrics = {
  // Financial metrics
  monthly_recurring_revenue: 'SUM(monthly_price) for active subscriptions',
  annual_recurring_revenue: 'MRR * 12',
  average_revenue_per_user: 'Total revenue / Total users',
  lifetime_value: 'Average revenue per user * Average subscription length',
  
  // Conversion metrics
  trial_conversion_rate: 'Paid subscriptions / Trial starts',
  paywall_conversion_rate: 'Trial starts / Paywall impressions',
  overall_conversion_rate: 'Paid subscriptions / Total users',
  
  // Retention metrics
  monthly_churn_rate: 'Cancelled subscriptions / Active subscriptions',
  retention_by_cohort: 'Active users by signup month',
  days_to_conversion: 'Average time from signup to subscription',
};
```

---

## Summary

This architecture provides a comprehensive, implementation-ready foundation for integrating RevenueCat with FlirtCraft's existing stack. The design emphasizes:

1. **Seamless Integration**: Builds on existing React Native/Expo + Supabase + FastAPI architecture
2. **Robust Feature Gating**: Real-time subscription validation with graceful fallbacks
3. **Reliable Webhook Processing**: Server-side validation and database synchronization
4. **Performance Optimization**: Caching, batch operations, and optimized queries
5. **Security Foundation**: Webhook verification, RLS policies, and server-side validation
6. **Comprehensive Analytics**: Detailed tracking for conversion optimization

The implementation supports the freemium model with clear value differentiation between Free (1 conversation/day, Green difficulty) and Premium ($9.99/month, unlimited access) tiers, while maintaining excellent user experience and reliable subscription management.

**File Location**: `D:\Code Journey\FlirtCraft v2\docs\premium-architecture-revenuecat.md`