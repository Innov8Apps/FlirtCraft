// User and Authentication Types
export interface User {
  id: string;
  email: string;
  age: number;
  target_gender: 'male' | 'female' | 'randomized';
  target_age_min: number;
  target_age_max: number;
  skill_goals: string[];
  premium_tier: 'free' | 'premium';
  premium_expires_at?: string;
  daily_conversations_used: number;
  daily_limit_reset_at?: string;
  xp_points: number;
  level: number;
  streak_count: number;
  streak_updated_at: string;
  created_at: string;
  updated_at: string;
}

export interface UserProfile {
  age: number;
  target_gender: 'male' | 'female' | 'randomized';
  target_age_min: number;
  target_age_max: number;
  skill_goals: string[];
}

export interface UserStats {
  xp_points: number;
  level: number;
  streak_count: number;
  conversations_completed: number;
  achievements_earned: number;
}

// Scenario Types
export interface Scenario {
  id: string;
  type: string;
  display_name: string;
  description: string;
  is_premium: boolean;
  context_templates: any;
  difficulty_modifiers: any;
  created_at: string;
}

export interface ConversationContext {
  appearance: string;
  environment: string;
  body_language: string;
  conversation_starters: string[];
  scenario_type: string;
  difficulty_level: 'green' | 'yellow' | 'red';
  generated_at: string;
}

// Conversation Types
export interface Conversation {
  id: string;
  user_id: string;
  scenario_type: string;
  difficulty_level: 'green' | 'yellow' | 'red';
  ai_character_context: any;
  status: 'active' | 'completed' | 'abandoned';
  start_time: string;
  end_time?: string;
  total_messages: number;
  session_score?: number;
  outcome?: 'bronze' | 'silver' | 'gold';
  created_at: string;
  messages?: Message[];
}

export interface Message {
  id: string;
  conversation_id: string;
  sender_type: 'user' | 'ai';
  content: string;
  message_order: number;
  feedback_type?: 'positive' | 'neutral' | 'warning' | 'tip';
  feedback_content?: string;
  timestamp: string;
}

export interface SendMessageRequest {
  content: string;
}

export interface SendMessageResponse {
  message: Message;
  ai_response?: Message;
  live_feedback?: {
    confidence: number;
    appropriateness: number;
    engagement: number;
    suggestion?: string;
  };
}

// Feedback Types
export interface FeedbackMetrics {
  id: string;
  conversation_id: string;
  engagement_score: number;
  responsiveness_score: number;
  storytelling_score: number;
  emotional_intelligence_score: number;
  momentum_score: number;
  flirtation_score?: number; // Only for red difficulty
  overall_score: number;
  feedback_text: string;
  created_at: string;
}

// Achievement Types
export interface Achievement {
  id: string;
  achievement_type: string;
  title: string;
  description: string;
  icon: string;
  xp_reward: number;
  requirements: any;
}

export interface UserAchievement {
  id: string;
  user_id: string;
  achievement_type: string;
  earned_at: string;
  conversation_id?: string;
}

// Request/Response Types
export interface CreateConversationRequest {
  scenario_type: string;
  difficulty_level: 'green' | 'yellow' | 'red';
}

export interface GenerateContextRequest {
  scenario_type: string;
  difficulty_level: 'green' | 'yellow' | 'red';
}

export interface CompleteConversationRequest {
  outcome?: 'bronze' | 'silver' | 'gold';
}

// Error Types
export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}