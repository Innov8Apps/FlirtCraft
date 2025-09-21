# FlirtCraft Technical Architecture Blueprint

## 1. Executive Summary

FlirtCraft is an AI-powered conversation training platform designed for mobile-first deployment. The architecture emphasizes real-time AI interactions, scalable data management, and cross-platform compatibility through React Native/Expo with a modern, performance-optimized technology stack.

### Key Architectural Decisions
- **Mobile-First**: React Native 0.72+ via Expo 52+ for cross-platform deployment
- **AI-Centric**: OpenRouter API with Google Gemini 2.5 Flash-Lite model for superior character consistency and 1.5x faster responses
- **Database Strategy**: Supabase PostgreSQL with Row Level Security for user data isolation
- **State Management**: 3-tier approach - React Query for server state, Zustand for client state (including subscription), React Hook Form for form state
- **UI Framework**: NativeBase with NativeWind 4.1 for Tailwind CSS utilities
- **Chat Interface**: React Native Gifted Chat for optimized conversation UI
- **Subscription Management**: RevenueCat for in-app purchases, subscription lifecycle, and receipt validation
- **Caching Strategy**: React Query for server-side caching, Redis for background job queuing
- **Deployment**: Railway with Docker containers and GitHub Actions CI/CD

### System Component Overview
1. **Mobile Application** (React Native/Expo) - Primary user interface with NativeBase
2. **API Gateway** (FastAPI) - Central request routing and authentication
3. **AI Service** (OpenRouter with Gemini 2.5 Flash-Lite) - Conversation engine with adaptive reasoning and context persistence
4. **Database Layer** (Supabase PostgreSQL) - User data, conversations, analytics with built-in Auth
5. **Subscription Service** (RevenueCat) - In-app purchases, subscription management, receipt validation
6. **Background Processing** (Redis + RQ) - Analytics, notifications, data processing
7. **Monitoring** (Sentry) - Error tracking and performance monitoring

### Technology Stack Summary
**Frontend**: React Native 0.72+, Expo 52+, React Query, Zustand, React Hook Form, NativeBase, React Native Gifted Chat, React Navigation 6.x, RevenueCat SDK, NativeWind 4.1  
**Backend**: FastAPI (Python), Supabase, SQLAlchemy ORM, Redis + RQ, OpenRouter API (Gemini 2.5 Flash-Lite)  
**Subscription**: RevenueCat for App Store/Google Play billing, receipt validation, subscription lifecycle, webhook processing  
**Infrastructure**: Railway deployment, Docker, GitHub Actions, Sentry monitoring

---

## 2. System Architecture Overview

### High-Level Architecture Flow
```
Mobile App (React Native/Expo)
    ↕ (REST API/WebSocket)     ↕ (SDK)
FastAPI Gateway            RevenueCat
    ↕                          ↕
┌─────────────────┬─────────────────┬─────────────────┐
│   AI Service    │  Auth Service   │ Subscription    │
│  (OpenRouter)   │   (Supabase)    │   (Webhooks)    │
└─────────────────┴─────────────────┴─────────────────┘
    ↕                   ↕                   ↕
┌─────────────────┬─────────────────┬─────────────────┐
│     Redis       │   Supabase      │     Sentry      │
│   (Job Queue)   │  (PostgreSQL)   │  (Monitoring)   │
└─────────────────┴─────────────────┴─────────────────┘
```

### Component Interactions
- **Mobile App** communicates with API Gateway via REST endpoints and WebSocket for real-time features
- **React Query** manages server state caching and synchronization automatically
- **Zustand** handles global client state (onboarding progress, app preferences, subscription status, feature access)
- **React Hook Form** manages form state with validation
- **API Gateway** routes requests to appropriate services and handles authentication via Supabase
- **AI Service** processes conversation logic and maintains context state
- **Supabase** provides PostgreSQL database with built-in authentication and real-time subscriptions
- **Background Jobs** handle analytics processing, notifications, and data cleanup via Redis + RQ

### Core App Features
The application implements 8 core features:

1. **Onboarding**: Multi-step form with Zustand state persistence
2. **Profile**: User settings with React Hook Form validation and privacy controls
3. **Scenario Selection**: Grid-based scenario picker with 8 scenarios and difficulty levels
4. **Pre-conversation Context**: 4-category context system (appearance, environment, body language, suggestions)
5. **Conversation**: Real-time AI chat with WebSocket updates and live feedback
6. **Feedback**: 6-metric evaluation system post-conversation (confidence, engagement, authenticity, flow, outcome, overall)
7. **Gamification**: XP system, achievements, streak tracking with Supabase storage
8. **Navigation**: Tab-based navigation with conditional rendering based on auth state

---

## 3. Technology Stack

### Frontend Architecture

**Core Framework**:
- React Native 0.72+ via Expo 52+ for cross-platform development
- Expo Router for file-based navigation with type safety
- NativeBase for comprehensive UI components with NativeWind 4.1+ for advanced utility styling
- React Native Gifted Chat for specialized conversation interface with optimized chat UX

**State Management (3-tier approach)**:
- **Server State**: React Query (@tanstack/react-query) for API data caching, synchronization, and background updates
- **Global State**: Zustand 4.4+ for app-wide state (user preferences, onboarding progress, navigation state)
- **Form State**: React Hook Form 7.45+ with validation for all user inputs

**Navigation & UI**:
- React Navigation 6.x with Expo Router for type-safe routing
- React Native Reanimated 3.6+ for 60fps animations
- Expo Vector Icons for iconography
- NativeBase components with built-in theming system and consistent cross-platform behavior
- React Native Gifted Chat for conversation interface with typing indicators and message status

**Storage & Services**:
- Expo SecureStore for sensitive data (auth tokens, user preferences)
- AsyncStorage for general app data and cache
- SQLite (expo-sqlite) for local offline storage (achievements, progress tracking)
- Expo Notifications for push notifications
- Expo Localization for internationalization

**Additional Libraries**:
- React Native Fast Image 8.6+ for optimized image loading in location cards
- React Native Gesture Handler 2.12+ for carousel and swipe interactions
- crypto-js for local data encryption

**Development & Testing**:
- Jest for unit testing
- React Native Testing Library for component testing
- TypeScript for type safety

### Backend Architecture

**Core Framework**:
- FastAPI (Python) for high-performance API with automatic OpenAPI documentation
- SQLAlchemy ORM for database interactions with type safety
- Pydantic for request/response validation and serialization

**Database & Authentication**:
- Supabase for PostgreSQL database with built-in authentication
- Row Level Security (RLS) policies for data isolation
- Real-time subscriptions for live conversation updates

**Background Processing**:
- Redis for job queuing and session storage
- RQ (Redis Queue) for background task processing
- Scheduled jobs for streak tracking and notifications
- Real-time feedback calculation during conversations
- Achievement detection and unlock notifications
- Metric history aggregation and analysis

**AI Integration**:
- Primary: OpenRouter API with google/gemini-2.5-flash-lite model for realistic character embodiment
- Fallback: OpenRouter with google/gemini-2.0-flash-lite-001 for reliability when primary is unavailable
- Adaptive reasoning for maintaining complete character consistency
- Optimized request batching for cost reduction and improved performance
- Custom prompt engineering with difficulty-aware reasoning parameters

### Infrastructure & Deployment

**Deployment Platform**:
- Railway for application hosting with automatic scaling
- Docker containers for consistent environments
- GitHub Actions for CI/CD pipeline

**Monitoring & Analytics**:
- Sentry for error tracking and performance monitoring
- Custom analytics via background jobs
- Health checks and uptime monitoring

---

## 4. Data Models & Database

### Core Entities

#### User Entity
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    target_gender VARCHAR(20) NOT NULL CHECK (target_gender IN ('male', 'female', 'randomized')),
    target_age_min INTEGER NOT NULL CHECK (target_age_min >= 18),
    target_age_max INTEGER NOT NULL CHECK (target_age_max <= 100),
    skill_goals TEXT[], -- ['conversation_starters', 'flow_maintenance', 'storytelling']
    premium_tier VARCHAR(20) DEFAULT 'free' CHECK (premium_tier IN ('free', 'premium')),
    premium_expires_at TIMESTAMP WITH TIME ZONE,
    daily_conversations_used INTEGER DEFAULT 0,
    daily_limit_reset_at TIMESTAMP WITH TIME ZONE,
    xp_points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    streak_count INTEGER DEFAULT 0,
    streak_updated_at DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_premium ON users(premium_tier, premium_expires_at);
```

#### Conversation Entity
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scenario_type VARCHAR(50) NOT NULL, -- 'coffee_shop', 'bookstore', etc.
    difficulty_level VARCHAR(10) NOT NULL CHECK (difficulty_level IN ('green', 'yellow', 'red')),
    ai_character_context JSONB NOT NULL, -- Appearance, environment, body language
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'abandoned')),
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_time TIMESTAMP WITH TIME ZONE,
    total_messages INTEGER DEFAULT 0,
    session_score INTEGER, -- 0-100
    outcome VARCHAR(20), -- 'bronze', 'silver', 'gold'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);
```

#### Message Entity
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_type VARCHAR(10) NOT NULL CHECK (sender_type IN ('user', 'ai')),
    content TEXT NOT NULL,
    message_order INTEGER NOT NULL,
    feedback_type VARCHAR(20), -- 'positive', 'neutral', 'warning', 'tip'
    feedback_content TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_order ON messages(conversation_id, message_order);
```

#### Scenario Entity
```sql
CREATE TABLE scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL UNIQUE, -- 'coffee_shop', 'bookstore', etc.
    display_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE,
    context_templates JSONB NOT NULL, -- Templates for AI context generation
    difficulty_modifiers JSONB NOT NULL, -- Behavior changes per difficulty
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Base 8 scenarios
INSERT INTO scenarios (type, display_name, description, is_premium) VALUES
('coffee_shop', 'Coffee Shops & Cafes', 'Practice in relaxed cafe environments', false),
('bookstore', 'Bookstores & Libraries', 'Quiet, intellectual spaces for conversation', false),
('park', 'Parks & Outdoor Spaces', 'Natural settings for casual encounters', false),
('campus', 'University Campus', 'Academic settings with peer interactions', false),
('grocery', 'Grocery Stores & Daily Life', 'Everyday situations and encounters', false),
('gym', 'Gyms & Fitness Centers', 'Active environments with shared interests', true),
('bar', 'Bars & Social Venues', 'Lively social environments', true),
('gallery', 'Art Galleries & Cultural Events', 'Sophisticated cultural environments', true);
```

#### User Achievement Entity
```sql
CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL, -- 'ice_breaker', 'smooth_operator', etc.
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    conversation_id UUID REFERENCES conversations(id),
    UNIQUE(user_id, achievement_type)
);

CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);
```

### SQLAlchemy Model Pattern
```python
from sqlalchemy import Column, String, Integer, Boolean, Text, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    # Additional fields as per schema...
    
    conversations = relationship("Conversation", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
```

---

## 5. API Design

### Authentication Flow
```
User Registration/Login → Supabase Auth → JWT Token → API Requests with Bearer Token
```

### Core API Endpoints

#### Authentication
```
POST /auth/register    # User registration via Supabase
POST /auth/login       # User login via Supabase
POST /auth/refresh     # Token refresh
DELETE /auth/logout    # User logout
```

#### User Management
```
GET /users/profile          # Get current user profile
PUT /users/profile          # Update user profile (React Hook Form)
GET /users/stats           # Get user XP, level, streak data
POST /users/streak         # Update daily streak
```

#### Scenario Management
```
GET /scenarios             # List all scenarios with filtering
GET /scenarios/{type}      # Get specific scenario details
POST /scenarios/{type}/context  # Generate pre-conversation context
```

#### Conversation Flow
```
POST /conversations                    # Start new conversation (premium check: daily limit for free users)
GET /conversations/{id}                # Get conversation details
POST /conversations/{id}/messages      # Send message (real-time via WebSocket)
PUT /conversations/{id}/complete       # End conversation
GET /conversations/{id}/feedback       # Get 6-metric feedback
```

#### Gamification
```
GET /users/achievements    # Get user achievements
GET /users/leaderboard    # Get leaderboard data (if implemented)
POST /users/xp            # Award XP points
```

### API Response Patterns
```json
// Success Response
{
    "success": true,
    "data": { ... },
    "meta": { "timestamp": "2024-01-01T00:00:00Z" }
}

// Error Response
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": { ... }
    }
}
```

### WebSocket Integration
```
WS /conversations/{id}/live

Events:
- message_received: New AI response
- typing_indicator: AI typing status with realistic delays
- feedback_generated: Live conversation feedback
- conversation_ended: Session completion
- live_feedback: Real-time tips during conversation
- achievement_unlocked: Instant achievement notifications
- metric_update: Live scoring updates
- context_reference: When AI references appearance/environment
```

---

## 6. Frontend Architecture

### State Management Architecture

#### React Query for Server State
```typescript
// hooks/useConversations.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export const useConversations = () => {
  return useQuery({
    queryKey: ['conversations'],
    queryFn: fetchConversations,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useStartConversation = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: startConversation,
    onSuccess: (newConversation) => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
      queryClient.setQueryData(['conversation', newConversation.id], newConversation);
    },
  });
};

// Background sync for user stats
export const useUserStats = () => {
  return useQuery({
    queryKey: ['user', 'stats'],
    queryFn: fetchUserStats,
    refetchInterval: 30000, // Sync every 30 seconds when active
  });
};
```

#### Zustand for Global State
```typescript
// stores/onboardingStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface OnboardingState {
  currentStep: number;
  formData: Partial<OnboardingFormData>;
  isCompleted: boolean;
  setStep: (step: number) => void;
  updateFormData: (data: Partial<OnboardingFormData>) => void;
  completeOnboarding: () => void;
}

export const useOnboardingStore = create<OnboardingState>()(
  persist(
    (set, get) => ({
      currentStep: 0,
      formData: {},
      isCompleted: false,
      setStep: (step) => set({ currentStep: step }),
      updateFormData: (data) => set((state) => ({
        formData: { ...state.formData, ...data }
      })),
      completeOnboarding: () => set({ isCompleted: true, currentStep: 0 }),
    }),
    { name: 'onboarding-storage' }
  )
);

// stores/appStore.ts - Global app state
interface AppState {
  theme: 'light' | 'dark';
  notifications: boolean;
  soundEnabled: boolean;
  hapticEnabled: boolean;
  setPreference: (key: string, value: any) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      theme: 'light',
      notifications: true,
      soundEnabled: true,
      hapticEnabled: true,
      setPreference: (key, value) => set({ [key]: value }),
    }),
    { name: 'app-preferences' }
  )
);
```

#### React Hook Form for Forms
```typescript
// components/ProfileForm.tsx
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const profileSchema = z.object({
  age: z.number().min(18).max(100),
  targetGender: z.enum(['male', 'female', 'randomized']),
  targetAgeMin: z.number().min(18),
  targetAgeMax: z.number().max(100),
  skillGoals: z.array(z.string()).min(1, 'Select at least one skill goal'),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export const ProfileForm = () => {
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      age: 25,
      targetGender: 'randomized',
      targetAgeMin: 18,
      targetAgeMax: 35,
      skillGoals: [],
    }
  });

  const updateProfile = useUpdateProfile();

  const onSubmit = (data: ProfileFormData) => {
    updateProfile.mutate(data);
  };

  return (
    <VStack space={4}>
      <FormControl isInvalid={!!errors.age}>
        <FormControl.Label>Age</FormControl.Label>
        <Controller
          control={control}
          name="age"
          render={({ field: { onChange, onBlur, value } }) => (
            <Input
              onBlur={onBlur}
              onChangeText={(text) => onChange(parseInt(text) || 0)}
              value={value?.toString()}
              keyboardType="numeric"
            />
          )}
        />
        <FormControl.ErrorMessage>
          {errors.age?.message}
        </FormControl.ErrorMessage>
      </FormControl>
      
      <Button onPress={handleSubmit(onSubmit)} isLoading={isSubmitting}>
        Update Profile
      </Button>
    </VStack>
  );
};
```

### Navigation Architecture

#### Expo Router File-based Structure
```
app/
├── (auth)/                    # Auth-protected routes
│   ├── _layout.tsx           # Auth layout with redirect logic
│   ├── login.tsx
│   └── register.tsx
├── (tabs)/                   # Main app tabs
│   ├── _layout.tsx          # Tab navigation layout
│   ├── home.tsx             # Dashboard/stats
│   ├── scenarios/           
│   │   ├── index.tsx        # Scenario grid selection
│   │   └── [type].tsx       # Scenario details
│   ├── conversation/
│   │   └── [id].tsx         # Active conversation
│   └── profile/
│       ├── index.tsx        # Profile settings
│       └── privacy.tsx      # Privacy controls
├── onboarding/              # Onboarding flow
│   ├── _layout.tsx
│   └── [step].tsx           # Dynamic step routing
├── feedback/
│   └── [conversationId].tsx # Post-conversation feedback
└── _layout.tsx              # Root layout
```

### Component Architecture

#### Feature-Based Organization
```
src/
├── components/              # Shared components
│   ├── ui/                 # Base UI components
│   ├── forms/              # Form components with validation
│   └── animations/         # Reanimated components
├── features/               # Feature-specific components
│   ├── onboarding/
│   ├── conversation/
│   ├── scenario-selection/
│   ├── profile/
│   ├── feedback/
│   └── gamification/
├── hooks/                  # Custom hooks (React Query, etc.)
├── stores/                 # Zustand stores
├── services/               # API services
└── utils/                  # Utilities and helpers
```

### Animation Architecture with Reanimated 3

```typescript
// animations/conversationAnimations.ts
import { 
  withSpring, 
  withTiming, 
  useSharedValue, 
  useAnimatedStyle,
  runOnJS
} from 'react-native-reanimated';

export const useMessageAnimation = () => {
  const translateY = useSharedValue(50);
  const opacity = useSharedValue(0);
  const scale = useSharedValue(0.9);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateY: translateY.value },
      { scale: scale.value }
    ],
    opacity: opacity.value,
  }));

  const animateIn = () => {
    translateY.value = withSpring(0, { damping: 12 });
    opacity.value = withTiming(1, { duration: 300 });
    scale.value = withSpring(1, { damping: 10 });
  };

  return { animatedStyle, animateIn };
};

// Typing indicator animation
export const useTypingAnimation = () => {
  const dot1 = useSharedValue(0);
  const dot2 = useSharedValue(0);
  const dot3 = useSharedValue(0);

  const startAnimation = () => {
    dot1.value = withSpring(1, { damping: 8 }, () => {
      dot2.value = withSpring(1, { damping: 8 }, () => {
        dot3.value = withSpring(1, { damping: 8 });
      });
    });
  };

  return { dot1, dot2, dot3, startAnimation };
};
```

---

## 7. AI Integration

### OpenRouter API Integration

#### Environment Configuration and Error Handling
```python
# settings.py - Environment setup for OpenRouter
import os
import logging
from typing import Optional
import requests

class OpenRouterConfig:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        # OpenRouter API configuration
        self.base_url = 'https://openrouter.ai/api/v1/chat/completions'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': 'https://flirtcraft.app',
            'X-Title': 'FlirtCraft',
            'Content-Type': 'application/json'
        }

        # Model configurations with fallback
        self.primary_model = 'google/gemini-2.5-flash-lite'
        self.fallback_model = 'google/gemini-2.0-flash-lite-001'
        self.conversation_model = self.primary_model
        self.context_model = self.primary_model
        self.feedback_model = self.primary_model
        
        # Rate limiting settings
        self.requests_per_minute = 60
        self.requests_per_day = 1500
        
        # Safety settings for all models
        self.default_safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

# Custom exceptions for OpenRouter API
class OpenRouterError(Exception):
    """Base exception for OpenRouter API errors."""
    pass

class OpenRouterRateLimitError(OpenRouterError):
    """Raised when rate limit is exceeded."""
    pass

class OpenRouterSafetyError(OpenRouterError):
    """Raised when content is blocked by safety filters."""
    pass

class OpenRouterApiError(OpenRouterError):
    """Raised for general API errors."""
    pass

def handle_openrouter_error(func):
    """Decorator to handle OpenRouter API errors with proper logging."""
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'status_code'):
                if e.response.status_code == 429:
                    logging.error(f"OpenRouter rate limit exceeded: {e}")
                    raise OpenRouterRateLimitError("Rate limit exceeded. Please try again later.") from e
                elif e.response.status_code == 400 and 'blocked' in str(e.response.text).lower():
                    logging.warning(f"Content blocked by safety filters: {e}")
                    raise OpenRouterSafetyError("Content was blocked by safety filters.") from e
            logging.error(f"OpenRouter API error: {e}")
            raise OpenRouterApiError(f"API request failed: {e}") from e
        except Exception as e:
            logging.error(f"Unexpected OpenRouter API error: {e}")
            raise OpenRouterApiError(f"API request failed: {e}") from e

    return wrapper
```

#### Request Optimization Setup
```python
# Request optimization for cost reduction and performance
class OpenRouterOptimizer:
    def __init__(self):
        self.cached_prompts = {}
        self.session_contexts = {}

    def cache_system_prompt(
        self,
        scenario_type: str,
        system_prompt: str
    ) -> str:
        """Cache system prompts for reuse across conversations."""

        cache_key = f"{scenario_type}_context"
        self.cached_prompts[cache_key] = system_prompt
        return cache_key

    def get_cached_prompt(self, cache_key: str) -> str:
        """Retrieve cached system prompt."""
        return self.cached_prompts.get(cache_key, "")

    def store_session_context(
        self,
        session_id: str,
        messages: list
    ) -> None:
        """Store conversation context for session continuity."""
        self.session_contexts[session_id] = messages

    def get_session_context(self, session_id: str) -> list:
        """Retrieve session conversation history."""
        return self.session_contexts.get(session_id, [])
```

#### Conversation Engine
```python
# ai_service.py
import requests
import asyncio
from typing import Dict, List
import json

class ConversationEngine:
    def __init__(self):
        self.config = OpenRouterConfig()
        self.optimizer = OpenRouterOptimizer()
        self.session = requests.Session()
        self.session.headers.update(self.config.headers)

    @handle_openrouter_error
    async def generate_response(
        self, 
        conversation_history: List[Dict],
        character_context: Dict,
        difficulty_level: str,
        user_preferences: Dict
    ) -> Dict:
        
        system_prompt = self._build_system_prompt(character_context, difficulty_level)
        
        # Build conversation messages for OpenRouter
        messages = self._build_openrouter_messages(conversation_history, system_prompt)

        # Prepare request payload
        payload = {
            "model": self.config.primary_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 150,
            "response_format": {"type": "json_object"},
            "reasoning": {"enabled": True}  # Enable reasoning for character consistency
        }

        # Try primary model first
        try:
            response = await asyncio.to_thread(
                self.session.post,
                self.config.base_url,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            # Fallback to alternative model
            logging.warning(f"Primary model failed: {e}, using fallback")
            payload["model"] = self.config.fallback_model
            response = await asyncio.to_thread(
                self.session.post,
                self.config.base_url,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

        # Extract the message content from OpenRouter response
        message_content = result['choices'][0]['message']['content']
        parsed_response = json.loads(message_content)
        
        return {
            "content": parsed_response["message"],
            "body_language": parsed_response.get("body_language", "neutral"),
            "receptiveness": parsed_response.get("receptiveness", "neutral"),
            "feedback": parsed_response.get("feedback")
        }
    
    def _build_openrouter_messages(self, conversation_history: List[Dict], system_prompt: str) -> List[Dict]:
        """Build messages array for OpenRouter API."""
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        for message in conversation_history:
            role = "user" if message["role"] == "user" else "assistant"
            messages.append({
                "role": role,
                "content": message["content"]
            })

        return messages
    
    def _build_system_prompt(self, context: Dict, difficulty: str) -> str:
        personality_traits = self._get_personality_traits(difficulty)
        
        prompt = f"""
You are roleplaying as a person in a {context['scenario']} setting.

CHARACTER PROFILE:
- Appearance: {context['appearance']}
- Environment: {context['environment']}
- Current mood/body language: {context['body_language']}
- Personality traits: {personality_traits}

DIFFICULTY LEVEL: {difficulty}
- Green: Friendly, receptive, easy to talk to
- Yellow: Polite but neutral, requires effort to engage
- Red: Challenging, potentially disinterested or distracted

RESPONSE REQUIREMENTS:
- Stay completely in character throughout
- Respond naturally as this person would
- Include subtle body language cues in your responses
- Provide response as JSON with fields: message, body_language, receptiveness, feedback

BEHAVIOR GUIDELINES:
- Green: Ask follow-up questions, show genuine interest, positive body language
- Yellow: Polite responses but don't lead conversation, mixed signals
- Red: Short responses, show mild disinterest, user must work to engage
"""
        return prompt

    def _get_personality_traits(self, difficulty: str) -> str:
        traits = {
            "green": "Outgoing, curious, good listener, encouraging",
            "yellow": "Polite, somewhat reserved, neutral disposition",
            "red": "Busy mindset, selective with attention, higher standards"
        }
        return traits.get(difficulty, traits["yellow"])
```

#### Pre-Conversation Context Generation
```python
import aiohttp

async def generate_context(
    scenario_type: str,
    difficulty: str,
    user_preferences: Dict
) -> Dict:
    """Generate pre-conversation context for the 4-category system."""
    
    context_prompt = f"""
Generate a realistic scenario context for a {scenario_type} setting 
with {difficulty} difficulty level.

USER PREFERENCES:
- Target gender: {user_preferences['target_gender']}
- Target age range: {user_preferences['target_age_min']}-{user_preferences['target_age_max']}
- Skill goals: {user_preferences['skill_goals']}

GENERATE 4 CATEGORIES:

1. APPEARANCE:
- Age (within target range)
- Physical description (attractive but realistic)
- Style/clothing appropriate for setting

2. ENVIRONMENT:
- Specific location within {scenario_type}
- Atmosphere and crowd level
- Contextual details that affect approach

3. BODY LANGUAGE ({difficulty} difficulty):
- Green: Open posture, eye contact, approachable signals
- Yellow: Neutral posture, occasional glances, mixed signals
- Red: Closed posture, busy/distracted, challenging signals

4. CONVERSATION STARTERS:
- 2-3 contextually relevant opening lines
- Based on environment and situation
- Appropriate for difficulty level

Format as JSON with these exact keys: appearance, environment, body_language, conversation_starters
"""
    
    # Configure OpenRouter request for context generation
    system_instruction = "You are a creative scenario generator for conversation training. Always respond in valid JSON format."

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": context_prompt}
    ]

    payload = {
        "model": "google/gemini-2.5-flash-lite",
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 500,
        "response_format": {"type": "json_object"}
    }

    # Make OpenRouter API request
    config = OpenRouterConfig()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            config.base_url,
            headers=config.headers,
            json=payload
        ) as response:
            response.raise_for_status()
            result = await response.json()

    # Extract and parse the response
    message_content = result['choices'][0]['message']['content']
    context = json.loads(message_content)
    
    # Add scenario metadata
    context["scenario_type"] = scenario_type
    context["difficulty_level"] = difficulty
    context["generated_at"] = datetime.utcnow()
    
    return context
```

### AI Behavior Patterns

#### Difficulty-Based Personality Modulation
- **Green Difficulty**: Enthusiastic responses, asks follow-up questions, positive body language feedback, encouraging tone
- **Yellow Difficulty**: Polite but neutral responses, requires user to drive conversation, mixed signals, moderate engagement
- **Red Difficulty**: Short responses, shows mild disinterest, challenges user to be more engaging, selective attention

#### Context Persistence and Awareness
- AI maintains full awareness of generated context throughout conversation
- References environmental details naturally ("This bookstore has such a cozy atmosphere")
- Adjusts responses based on generated personality traits and current mood
- Remembers conversation history and builds on previous exchanges

#### Real-time Feedback Generation
```python
async def generate_live_feedback(message: str, conversation_context: Dict) -> Dict:
    """Generate real-time feedback for user messages."""
    
    feedback_prompt = f"""
Analyze this user message in a {conversation_context['scenario']} context:
Message: "{message}"

Rate on a scale of 1-5 and provide brief feedback:
1. Confidence level of the message
2. Appropriateness for the context
3. Engagement potential
4. Suggestion for improvement (if needed)

Keep feedback constructive and encouraging.
Format as JSON: confidence, appropriateness, engagement, suggestion
"""
    
    # Use OpenRouter for feedback generation
    system_instruction = "You are a conversation coach providing constructive feedback. Always respond in valid JSON format with scores 1-5 and helpful suggestions."

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": feedback_prompt}
    ]

    payload = {
        "model": "google/gemini-2.5-flash-lite",
        "messages": messages,
        "temperature": 0.3,  # Lower temperature for more consistent feedback
        "max_tokens": 200,
        "response_format": {"type": "json_object"}
    }

    config = OpenRouterConfig()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            config.base_url,
            headers=config.headers,
            json=payload
        ) as response:
            response.raise_for_status()
            result = await response.json()

    message_content = result['choices'][0]['message']['content']
    return json.loads(message_content)
```

---

## 8. AI Conversation Requirements

### Critical Behavior Specifications

The AI conversation partners MUST behave in an extremely human-like manner. This is the core differentiator of the product.

#### Message Length Variation System
**Required Distribution**:
- **Ultra-short (1-5 words)**: 30% - "lol", "yeah totally", "oh really?"
- **Short (6-20 words)**: 35% - "That's actually pretty cool! What got you into that?"
- **Medium (21-50 words)**: 25% - Full sentences with context and personality
- **Long (50+ words)**: 10% - Stories, explanations, or excited rambling

#### Complete Context Awareness
The AI MUST maintain full awareness throughout conversation:
- **Appearance Details**: Hair, clothing, accessories from pre-conversation context
- **Current Activity**: Reading specific book, working on laptop, etc.
- **Environmental Context**: Crowded/quiet, time of day, weather if relevant
- **User Profile Integration**: Age, gender, preferences, conversation goals
- **Body Language Signals**: Green/yellow/red difficulty indicators

#### Difficulty-Specific Behavior

**Green Difficulty (Friendly & Receptive)**:
- Maintains eye contact (mentions looking at user)
- Asks follow-up questions enthusiastically
- Shows clear romantic interest
- Response time: 1-2 seconds consistently

**Yellow Difficulty (Realistic Stranger)**:
- Alternates between engaged and reserved
- Sometimes checks phone mid-conversation
- Natural conversation flow with realistic hesitations
- Response time: 2-3 seconds sometimes

**Red Difficulty (Challenging/Busy)**:
- Genuinely distracted with their activity
- Frequent ultra-short responses: "yeah", "mm-hmm"
- Takes 3-4 seconds to respond
- May end conversation if user isn't engaging

#### Realistic Texting Patterns
- Occasional typos (1-2% of messages)
- Age-appropriate emoji usage
- Natural conversation fillers: "um", "like", "idk"
- Double-texting when excited
- Typing indicators matching message length

---

## 9. 6-Metric Feedback System

### Post-Conversation Evaluation Engine

The feedback system evaluates conversations across six sophisticated metrics to provide actionable learning insights.

#### Evaluation Metrics

1. **AI Engagement Quality** (0-100)
   - Measures context integration and appearance cue usage
   - Evaluates creative use of AI suggestions
   - Tracks environmental detail incorporation

2. **Responsiveness & Active Listening** (0-100)
   - Follow-up question quality
   - Topic building and expansion
   - Acknowledgment of AI's statements

3. **Storytelling & Narrative Building** (0-100)
   - Personal anecdote sharing
   - Conversation depth creation
   - Narrative flow maintenance

4. **Emotional Intelligence** (0-100)
   - Empathy demonstration
   - Emotional awareness and response
   - Mood matching and adjustment

5. **Conversation Momentum & Flow** (0-100)
   - Natural topic transitions
   - Conversation pacing
   - Dead-end avoidance

6. **Creative Flirtation** (0-100, Red difficulty only)
   - Playful banter quality
   - Subtle romantic escalation
   - Chemistry building

#### Database Schema Addition

```sql
CREATE TABLE feedback_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    engagement_score INTEGER CHECK (engagement_score >= 0 AND engagement_score <= 100),
    responsiveness_score INTEGER CHECK (responsiveness_score >= 0 AND responsiveness_score <= 100),
    storytelling_score INTEGER CHECK (storytelling_score >= 0 AND storytelling_score <= 100),
    emotional_intelligence_score INTEGER CHECK (emotional_intelligence_score >= 0 AND emotional_intelligence_score <= 100),
    momentum_score INTEGER CHECK (momentum_score >= 0 AND momentum_score <= 100),
    flirtation_score INTEGER, -- NULL for green/yellow difficulties
    overall_score INTEGER GENERATED ALWAYS AS (
        (engagement_score + responsiveness_score + storytelling_score + 
         emotional_intelligence_score + momentum_score + COALESCE(flirtation_score, 0)) / 
        CASE WHEN flirtation_score IS NULL THEN 5 ELSE 6 END
    ) STORED,
    feedback_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_feedback_metrics_conversation ON feedback_metrics(conversation_id);
CREATE INDEX idx_feedback_metrics_scores ON feedback_metrics(overall_score);
```

#### Scoring Rubrics
- **90-100**: Exceptional - Mastery level performance
- **80-89**: Excellent - Strong skill demonstration  
- **70-79**: Good - Solid competency shown
- **60-69**: Developing - Basic skills with room for growth
- **50-59**: Needs Practice - Fundamental skills emerging
- **0-49**: Learning Mode - Focus on foundational development

---

## 10. Security & Privacy

### Authentication & Authorization

#### Supabase Integration
```javascript
// Automatic JWT handling
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.EXPO_PUBLIC_SUPABASE_URL,
  process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY
);

// Auth state management
export const useAuth = () => {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  return { user, signIn, signOut, signUp };
};
```

#### Row Level Security Policies
```sql
-- Users can only access their own data
CREATE POLICY "Users can view own profile" ON users
FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
FOR UPDATE USING (auth.uid() = id);

-- Conversations are private to users
CREATE POLICY "Users can view own conversations" ON conversations
FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own conversations" ON conversations
FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Messages follow conversation ownership
CREATE POLICY "Users can view own messages" ON messages
FOR SELECT USING (
  conversation_id IN (
    SELECT id FROM conversations WHERE user_id = auth.uid()
  )
);

-- Achievements are user-specific
CREATE POLICY "Users can view own achievements" ON user_achievements
FOR SELECT USING (auth.uid() = user_id);
```

### Data Privacy & Protection

#### Sensitive Data Handling
```typescript
// Secure storage for sensitive data
import * as SecureStore from 'expo-secure-store';

export const secureStorage = {
  setItem: async (key: string, value: string) => {
    await SecureStore.setItemAsync(key, value);
  },
  
  getItem: async (key: string): Promise<string | null> => {
    return await SecureStore.getItemAsync(key);
  },
  
  removeItem: async (key: string) => {
    await SecureStore.deleteItemAsync(key);
  }
};

// Store auth tokens securely
const storeAuthTokens = async (tokens: AuthTokens) => {
  await secureStorage.setItem('access_token', tokens.access);
  await secureStorage.setItem('refresh_token', tokens.refresh);
};
```

#### Privacy Controls in Profile
- **Data Collection Consent**: Clear opt-in for analytics and conversation storage
- **Conversation Retention**: User-controlled retention period for conversation history
- **Data Export**: GDPR-compliant data export functionality
- **Account Deletion**: Complete data purge on account termination
- **Anonymous Analytics**: Aggregated usage analytics without personal identifiers

### API Security

#### Input Validation & Sanitization
```python
from pydantic import BaseModel, validator
from typing import List
import re

class MessageRequest(BaseModel):
    content: str
    conversation_id: str
    
    @validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 500:
            raise ValueError('Message too long (max 500 characters)')
        # Remove potentially malicious content
        cleaned = re.sub(r'[<>"\']', '', v)
        return cleaned.strip()

class ConversationRequest(BaseModel):
    scenario_type: str
    difficulty_level: str
    
    @validator('scenario_type')
    def validate_scenario(cls, v):
        allowed_scenarios = [
            'coffee_shop', 'bookstore', 'gym', 'park',
            'bar', 'campus', 'grocery', 'gallery'
        ]
        if v not in allowed_scenarios:
            raise ValueError(f'Invalid scenario type: {v}')
        return v
```

#### Rate Limiting
```python
from fastapi import HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@app.post("/conversations/{conversation_id}/messages")
@limiter.limit("30/minute")  # 30 messages per minute max
async def send_message(
    request: Request, 
    conversation_id: str, 
    message_data: MessageRequest
):
    # Message handling logic
    pass

@app.post("/conversations")
@limiter.limit("10/hour")  # Max 10 new conversations per hour
async def start_conversation(
    request: Request,
    conversation_data: ConversationRequest
):
    # Conversation creation logic
    pass
```

---

## 9. Deployment & Infrastructure

### Railway Deployment Configuration

#### Docker Setup
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

#### Railway Configuration
```toml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers $RAILWAY_WORKERS"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[env]
RAILWAY_WORKERS = "2"
```

#### Environment Variables
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Redis
    redis_url: str
    
    # External APIs
    openrouter_api_key: str
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # Monitoring
    sentry_dsn: str = None
    
    # App settings
    environment: str = "production"
    debug: bool = False
    
    # Railway auto-injected
    port: int = 8000
    railway_environment: str = None
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### GitHub Actions CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
          
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ env.PYTHON_VERSION }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: Run linting
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          black --check .
          
      - name: Run type checking
        run: mypy .
        
      - name: Run tests
        run: |
          pytest tests/ -v --cov=./src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Railway
        uses: railwayapp/railway-deploy@v1
        with:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          service: flirtcraft-api
          
      - name: Wait for deployment
        run: sleep 30
        
      - name: Health check
        run: |
          curl -f ${{ secrets.RAILWAY_APP_URL }}/health || exit 1
```

### Health Monitoring & Observability

#### Health Check Endpoints
```python
from fastapi import FastAPI, HTTPException
from datetime import datetime
import asyncio

@app.get("/health")
async def health_check():
    """Comprehensive health check for Railway monitoring."""
    try:
        # Database connectivity
        db_healthy = await check_database_health()
        
        # Redis connectivity
        redis_healthy = await check_redis_health()
        
        # OpenRouter API availability
        openrouter_healthy = await check_openrouter_health()
        
        # Overall health status
        is_healthy = all([db_healthy, redis_healthy, openrouter_healthy])
        
        health_data = {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": settings.environment,
            "services": {
                "database": "healthy" if db_healthy else "unhealthy",
                "redis": "healthy" if redis_healthy else "unhealthy",
                "openrouter": "healthy" if openrouter_healthy else "unhealthy"
            }
        }
        
        if not is_healthy:
            raise HTTPException(status_code=503, detail=health_data)
            
        return health_data
        
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

async def check_database_health() -> bool:
    try:
        await database.execute("SELECT 1")
        return True
    except Exception:
        return False

async def check_redis_health() -> bool:
    try:
        await redis.ping()
        return True
    except Exception:
        return False

async def check_openrouter_health() -> bool:
    try:
        config = OpenRouterConfig()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://openrouter.ai/api/v1/models",
                headers={'Authorization': f'Bearer {config.api_key}'},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return response.status == 200
    except Exception:
        return False
```

#### Sentry Error Monitoring
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            FastApiIntegration(auto_enabling_integrations=False),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1,
        environment=settings.environment,
        before_send=filter_sensitive_data,
    )

def filter_sensitive_data(event, hint):
    """Remove sensitive data from Sentry events."""
    if event.get('request'):
        # Remove auth headers
        headers = event['request'].get('headers', {})
        if 'authorization' in headers:
            headers['authorization'] = '[Filtered]'
    return event
```

---

## 10. Testing Strategy

### Frontend Testing Architecture

#### Jest & React Native Testing Library Setup
```javascript
// jest.config.js
module.exports = {
  preset: 'jest-expo',
  testEnvironment: 'jsdom',
  transformIgnorePatterns: [
    'node_modules/(?!(jest-)?@?react-native|react-clone-referenced-element|@react-native-community|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)'
  ],
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  testMatch: ['**/__tests__/**/*.test.{ts,tsx}'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/test/**/*',
  ],
  coverageReporters: ['text', 'lcov', 'html'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};

// src/test/setup.ts
import 'react-native-gesture-handler/jestSetup';
import '@testing-library/jest-native/extend-expect';

// Mock React Query
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode } from 'react';

export const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

export const TestWrapper = ({ children }: { children: ReactNode }) => {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};
```

#### Component Testing Patterns
```typescript
// __tests__/components/ConversationScreen.test.tsx
import { render, fireEvent, waitFor, screen } from '@testing-library/react-native';
import { ConversationScreen } from '../../features/conversation/ConversationScreen';
import { TestWrapper } from '../setup';

// Mock the API calls
jest.mock('../../services/api', () => ({
  sendMessage: jest.fn(),
  getConversation: jest.fn(),
}));

describe('ConversationScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('sends message when submit button is pressed', async () => {
    const mockSendMessage = require('../../services/api').sendMessage;
    mockSendMessage.mockResolvedValue({ id: '1', content: 'Hello!' });

    render(
      <TestWrapper>
        <ConversationScreen conversationId="test-id" />
      </TestWrapper>
    );
    
    const input = screen.getByTestId('message-input');
    const submitButton = screen.getByTestId('send-button');
    
    fireEvent.changeText(input, 'Hello there!');
    fireEvent.press(submitButton);
    
    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith('test-id', 'Hello there!');
    });
    
    expect(screen.getByText('Hello there!')).toBeTruthy();
  });

  it('displays typing indicator when AI is responding', async () => {
    render(
      <TestWrapper>
        <ConversationScreen conversationId="test-id" />
      </TestWrapper>
    );
    
    // Trigger message send
    fireEvent.changeText(screen.getByTestId('message-input'), 'Test');
    fireEvent.press(screen.getByTestId('send-button'));
    
    // Should show typing indicator
    await waitFor(() => {
      expect(screen.getByTestId('typing-indicator')).toBeTruthy();
    });
  });
});
```

#### Hook Testing
```typescript
// __tests__/hooks/useConversation.test.ts
import { renderHook, waitFor } from '@testing-library/react-native';
import { TestWrapper } from '../setup';
import { useConversation } from '../../hooks/useConversation';

describe('useConversation', () => {
  it('loads conversation data correctly', async () => {
    const { result } = renderHook(
      () => useConversation('test-conversation-id'),
      { wrapper: TestWrapper }
    );

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.conversation).toBeDefined();
  });
});
```

### Backend Testing Architecture

#### FastAPI Test Configuration
```python
# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from models import Base
from auth import get_current_user

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"id": "test-user-id", "email": "test@example.com"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}
```

#### API Endpoint Testing
```python
# tests/test_conversations.py
import pytest
from fastapi.testclient import TestClient

def test_create_conversation_success(client, auth_headers):
    response = client.post(
        "/conversations",
        json={
            "scenario_type": "coffee_shop",
            "difficulty_level": "green"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "id" in data["data"]
    assert data["data"]["scenario_type"] == "coffee_shop"

def test_create_conversation_invalid_scenario(client, auth_headers):
    response = client.post(
        "/conversations",
        json={
            "scenario_type": "invalid_scenario",
            "difficulty_level": "green"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
d
def test_send_message(client, auth_headers):
    # First create a conversation
    conv_response = client.post(
        "/conversations",
        json={"scenario_type": "coffee_shop", "difficulty_level": "green"},
        headers=auth_headers
    )
    conversation_id = conv_response.json()["data"]["id"]
    
    # Send a message
    message_response = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "Hello there!"},
        headers=auth_headers
    )
    
    assert message_response.status_code == 201
    data = message_response.json()
    assert data["success"] is True
    assert data["data"]["content"] == "Hello there!"

@pytest.mark.asyncio
async def test_ai_response_generation():
    from ai_service import ConversationEngine
    
    engine = ConversationEngine()
    context = {
        "scenario": "coffee_shop",
        "appearance": "Young professional, friendly demeanor",
        "environment": "Busy morning coffee shop",
        "body_language": "Open, approachable"
    }
    
    response = await engine.generate_response(
        conversation_history=[{"role": "user", "content": "Hi there!"}],
        character_context=context,
        difficulty_level="green",
        user_preferences={}
    )
    
    assert "content" in response
    assert "body_language" in response
    assert len(response["content"]) > 0
```

#### Integration Testing
```python
# tests/test_integration.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_complete_conversation_flow(async_client):
    """Test the entire conversation flow from start to finish."""
    
    # 1. Create conversation
    create_response = await async_client.post(
        "/conversations",
        json={"scenario_type": "coffee_shop", "difficulty_level": "green"}
    )
    assert create_response.status_code == 201
    conversation_id = create_response.json()["data"]["id"]
    
    # 2. Send user message
    message_response = await async_client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "Hi, how's your day going?"}
    )
    assert message_response.status_code == 201
    
    # 3. Get AI response
    conversation_response = await async_client.get(f"/conversations/{conversation_id}")
    assert conversation_response.status_code == 200
    messages = conversation_response.json()["data"]["messages"]
    assert len(messages) >= 2  # User message + AI response
    
    # 4. Complete conversation
    complete_response = await async_client.put(
        f"/conversations/{conversation_id}/complete"
    )
    assert complete_response.status_code == 200
    
    # 5. Get feedback
    feedback_response = await async_client.get(
        f"/conversations/{conversation_id}/feedback"
    )
    assert feedback_response.status_code == 200
    feedback = feedback_response.json()["data"]
    assert "confidence" in feedback
    assert "engagement" in feedback
```

### Performance Testing
```python
# tests/test_performance.py
import pytest
import time
import asyncio

@pytest.mark.asyncio
async def test_conversation_response_time():
    """Test that AI responses are generated within acceptable time."""
    from ai_service import ConversationEngine
    
    engine = ConversationEngine()
    context = {
        "scenario": "coffee_shop",
        "appearance": "Test appearance",
        "environment": "Test environment",
        "body_language": "neutral"
    }
    
    start_time = time.time()
    response = await engine.generate_response(
        conversation_history=[{"role": "user", "content": "Hello"}],
        character_context=context,
        difficulty_level="green",
        user_preferences={}
    )
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response_time < 3.0  # Should respond within 3 seconds
    assert response["content"] is not None

def test_api_response_time(client, auth_headers):
    """Test API endpoint response times."""
    start_time = time.time()
    response = client.get("/scenarios", headers=auth_headers)
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response_time < 1.0  # Should respond within 1 second
    assert response.status_code == 200
```

---

## 11. Local Storage Architecture

### Offline-First Capability

FlirtCraft implements a robust local storage strategy to ensure seamless offline functionality and optimal performance.

#### SQLite for Structured Data
```typescript
// Local database schema using expo-sqlite
import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('flirtcraft.db');

// Achievement progress tracking
db.transaction(tx => {
  tx.executeSql(
    `CREATE TABLE IF NOT EXISTS achievement_progress (
      id TEXT PRIMARY KEY,
      achievement_type TEXT NOT NULL,
      current_progress INTEGER DEFAULT 0,
      target_progress INTEGER NOT NULL,
      unlocked BOOLEAN DEFAULT FALSE,
      unlocked_at DATETIME,
      synced BOOLEAN DEFAULT FALSE
    );`
  );
  
  // Metric history for offline analytics
  tx.executeSql(
    `CREATE TABLE IF NOT EXISTS metric_history (
      id TEXT PRIMARY KEY,
      conversation_id TEXT,
      metric_type TEXT,
      score INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      synced BOOLEAN DEFAULT FALSE
    );`
  );
});
```

#### AsyncStorage for App State
```typescript
// Cached conversations and user preferences
import AsyncStorage from '@react-native-async-storage/async-storage';

const StorageKeys = {
  CACHED_CONVERSATIONS: '@flirtcraft/conversations',
  USER_PREFERENCES: '@flirtcraft/preferences',
  OFFLINE_QUEUE: '@flirtcraft/offline_queue',
  STREAK_DATA: '@flirtcraft/streak'
};
```

#### Encrypted Storage for Sensitive Data
```typescript
import CryptoJS from 'crypto-js';
import * as SecureStore from 'expo-secure-store';

class SecureStorage {
  private encryptionKey: string;
  
  async storeEncrypted(key: string, data: any): Promise<void> {
    const encrypted = CryptoJS.AES.encrypt(
      JSON.stringify(data), 
      this.encryptionKey
    ).toString();
    await SecureStore.setItemAsync(key, encrypted);
  }
  
  async retrieveDecrypted(key: string): Promise<any> {
    const encrypted = await SecureStore.getItemAsync(key);
    if (!encrypted) return null;
    
    const decrypted = CryptoJS.AES.decrypt(encrypted, this.encryptionKey);
    return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
  }
}
```

#### Sync Strategy
```typescript
// Background sync when connection restored
class SyncManager {
  async syncOfflineData(): Promise<void> {
    const hasConnection = await NetInfo.fetch();
    if (!hasConnection.isConnected) return;
    
    // Sync order: user data → conversations → achievements → metrics
    await this.syncUserData();
    await this.syncConversations();
    await this.syncAchievements();
    await this.syncMetrics();
  }
  
  private async syncAchievements(): Promise<void> {
    const unsyncedAchievements = await db.executeSql(
      'SELECT * FROM achievement_progress WHERE synced = FALSE'
    );
    
    for (const achievement of unsyncedAchievements) {
      await api.syncAchievement(achievement);
      await db.executeSql(
        'UPDATE achievement_progress SET synced = TRUE WHERE id = ?',
        [achievement.id]
      );
    }
  }
}
```

### Storage Limits & Management
- **SQLite**: Up to 50MB for achievement and metric data
- **AsyncStorage**: 6MB limit for cached conversations
- **SecureStore**: 2KB per key for auth tokens
- **Automatic cleanup**: Remove data older than 30 days
- **Storage monitoring**: Alert user when approaching limits

---

This comprehensive architecture document provides a solid foundation for the FlirtCraft application with modern technologies, scalable patterns, and thorough testing coverage. The 3-tier state management approach, combined with React Query's intelligent caching and Supabase's real-time capabilities, creates a responsive and efficient user experience while maintaining clean separation of concerns and comprehensive security measures.