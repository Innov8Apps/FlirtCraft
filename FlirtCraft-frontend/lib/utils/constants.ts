// App Configuration
export const APP_CONFIG = {
  name: 'FlirtCraft',
  version: '1.0.0',
  environment: process.env.NODE_ENV || 'development',
} as const;

// API Configuration
export const API_CONFIG = {
  baseUrl: process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds
  retryAttempts: 3,
} as const;

// Supabase Configuration
export const SUPABASE_CONFIG = {
  url: process.env.EXPO_PUBLIC_SUPABASE_URL || '',
  anonKey: process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '',
} as const;

// Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'user_preferences',
  ONBOARDING_STATE: 'onboarding_state',
  CACHED_CONVERSATIONS: 'cached_conversations',
  OFFLINE_QUEUE: 'offline_queue',
  STREAK_DATA: 'streak_data',
  ACHIEVEMENT_CACHE: 'achievement_cache',
} as const;

// User Limits
export const USER_LIMITS = {
  FREE_DAILY_CONVERSATIONS: 3,
  PREMIUM_DAILY_CONVERSATIONS: 50,
  MESSAGE_MAX_LENGTH: 500,
  USERNAME_MAX_LENGTH: 30,
  USERNAME_MIN_LENGTH: 3,
} as const;

// Scenario Types
export const SCENARIO_TYPES = {
  COFFEE_SHOP: 'coffee_shop',
  BOOKSTORE: 'bookstore',
  PARK: 'park',
  CAMPUS: 'campus',
  GROCERY: 'grocery',
  GYM: 'gym',
  BAR: 'bar',
  GALLERY: 'gallery',
} as const;

// Difficulty Levels
export const DIFFICULTY_LEVELS = {
  GREEN: 'green',
  YELLOW: 'yellow',
  RED: 'red',
} as const;

// XP Rewards
export const XP_REWARDS = {
  CONVERSATION_COMPLETED: 50,
  DAILY_STREAK: 25,
  ACHIEVEMENT_EARNED: 100,
  PERFECT_CONVERSATION: 100,
  FIRST_CONVERSATION: 25,
} as const;

// Animation Durations (in milliseconds)
export const ANIMATION_DURATION = {
  FAST: 200,
  NORMAL: 300,
  SLOW: 500,
  EXTRA_SLOW: 800,
} as const;

// Theme Colors (matching NativeBase theme)
export const COLORS = {
  PRIMARY: '#f59e0b',
  SECONDARY: '#64748b',
  SUCCESS: '#22c55e',
  WARNING: '#f59e0b',
  ERROR: '#ef4444',
  WHITE: '#ffffff',
  BLACK: '#000000',
  GRAY_50: '#f8fafc',
  GRAY_100: '#f1f5f9',
  GRAY_200: '#e2e8f0',
  GRAY_300: '#cbd5e1',
  GRAY_400: '#94a3b8',
  GRAY_500: '#64748b',
  GRAY_600: '#475569',
  GRAY_700: '#334155',
  GRAY_800: '#1e293b',
  GRAY_900: '#0f172a',
} as const;

// Screen Sizes
export const SCREEN_SIZES = {
  SMALL: 320,
  MEDIUM: 768,
  LARGE: 1024,
  EXTRA_LARGE: 1280,
} as const;

// Feedback Types
export const FEEDBACK_TYPES = {
  POSITIVE: 'positive',
  NEUTRAL: 'neutral',
  WARNING: 'warning',
  TIP: 'tip',
} as const;

// Achievement Types
export const ACHIEVEMENT_TYPES = {
  ICE_BREAKER: 'ice_breaker',
  SMOOTH_OPERATOR: 'smooth_operator',
  CONVERSATION_MASTER: 'conversation_master',
  STREAK_WARRIOR: 'streak_warrior',
  SCENARIO_EXPLORER: 'scenario_explorer',
  LEVEL_UP: 'level_up',
} as const;

// Conversation Outcomes
export const CONVERSATION_OUTCOMES = {
  BRONZE: 'bronze',
  SILVER: 'silver',
  GOLD: 'gold',
} as const;

// Regular Expressions
export const REGEX = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^\+?[\d\s\-\(\)]+$/,
  ALPHANUMERIC: /^[a-zA-Z0-9]+$/,
  USERNAME: /^[a-zA-Z0-9_]{3,30}$/,
} as const;