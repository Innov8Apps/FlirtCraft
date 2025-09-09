#!/usr/bin/env python3
"""
Apply migration to Supabase database directly
"""
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQL Migration converted from the Alembic file
MIGRATION_SQL = """
-- Create UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    email VARCHAR(255) NOT NULL,
    supabase_user_id VARCHAR(255),
    age INTEGER NOT NULL,
    premium_tier VARCHAR(20) NOT NULL DEFAULT 'free',
    premium_expires_at TIMESTAMPTZ,
    daily_conversations_used INTEGER NOT NULL DEFAULT 0,
    daily_limit_reset_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT true,
    email_verified BOOLEAN NOT NULL DEFAULT false,
    onboarding_completed BOOLEAN NOT NULL DEFAULT false,
    onboarding_completed_at TIMESTAMPTZ,
    
    -- Constraints
    CONSTRAINT valid_age CHECK (age >= 18 AND age <= 100),
    CONSTRAINT non_negative_conversations CHECK (daily_conversations_used >= 0),
    CONSTRAINT unique_email UNIQUE (email),
    CONSTRAINT unique_supabase_user_id UNIQUE (supabase_user_id)
);

-- Create indexes for users
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_premium ON users (premium_tier, premium_expires_at);
CREATE INDEX IF NOT EXISTS idx_users_supabase_id ON users (supabase_user_id);

-- Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    target_gender VARCHAR(20) NOT NULL,
    target_age_min INTEGER NOT NULL,
    target_age_max INTEGER NOT NULL,
    relationship_goal VARCHAR(30) NOT NULL,
    primary_skills TEXT[] NOT NULL DEFAULT '{}',
    specific_challenges TEXT[] NOT NULL DEFAULT '{}',
    experience_level VARCHAR(20) NOT NULL,
    practice_frequency VARCHAR(20) NOT NULL,
    privacy_level VARCHAR(20) NOT NULL DEFAULT 'standard',
    notifications_enabled BOOLEAN NOT NULL DEFAULT true,
    analytics_opt_in BOOLEAN NOT NULL DEFAULT false,
    marketing_opt_in BOOLEAN NOT NULL DEFAULT false,
    persona_detected VARCHAR(30),
    onboarding_metadata JSONB NOT NULL DEFAULT '{}',
    timezone VARCHAR(50),
    locale VARCHAR(10) NOT NULL DEFAULT 'en',
    
    -- Constraints
    CONSTRAINT valid_min_age CHECK (target_age_min >= 18),
    CONSTRAINT valid_max_age CHECK (target_age_max <= 100),
    CONSTRAINT valid_age_range CHECK (target_age_min <= target_age_max),
    CONSTRAINT unique_user_profile UNIQUE (user_id),
    CONSTRAINT fk_user_profiles_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for user_profiles
CREATE INDEX IF NOT EXISTS idx_user_profiles_preferences ON user_profiles (target_gender, experience_level);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles (user_id);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    total_conversations INTEGER NOT NULL DEFAULT 0,
    total_messages_sent INTEGER NOT NULL DEFAULT 0,
    total_practice_time INTEGER NOT NULL DEFAULT 0,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_practice_date DATE,
    xp_points INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    achievements_unlocked TEXT[] NOT NULL DEFAULT '{}',
    average_confidence_score FLOAT,
    average_engagement_score FLOAT,
    average_overall_score FLOAT,
    progress_metadata JSONB NOT NULL DEFAULT '{}',
    
    -- Constraints
    CONSTRAINT valid_confidence_score CHECK (
        average_confidence_score IS NULL OR 
        (average_confidence_score >= 0 AND average_confidence_score <= 100)
    ),
    CONSTRAINT valid_engagement_score CHECK (
        average_engagement_score IS NULL OR 
        (average_engagement_score >= 0 AND average_engagement_score <= 100)
    ),
    CONSTRAINT valid_overall_score CHECK (
        average_overall_score IS NULL OR 
        (average_overall_score >= 0 AND average_overall_score <= 100)
    ),
    CONSTRAINT non_negative_current_streak CHECK (current_streak >= 0),
    CONSTRAINT minimum_level_one CHECK (level >= 1),
    CONSTRAINT non_negative_longest_streak CHECK (longest_streak >= 0),
    CONSTRAINT non_negative_conversations CHECK (total_conversations >= 0),
    CONSTRAINT non_negative_messages CHECK (total_messages_sent >= 0),
    CONSTRAINT non_negative_practice_time CHECK (total_practice_time >= 0),
    CONSTRAINT non_negative_xp CHECK (xp_points >= 0),
    CONSTRAINT unique_user_progress UNIQUE (user_id),
    CONSTRAINT fk_user_progress_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for user_progress
CREATE INDEX IF NOT EXISTS idx_user_progress_level_xp ON user_progress (level, xp_points);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress (user_id);

-- Create onboarding_sessions table
CREATE TABLE IF NOT EXISTS onboarding_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    session_token VARCHAR(255) NOT NULL,
    current_step INTEGER NOT NULL DEFAULT 1,
    total_steps INTEGER NOT NULL DEFAULT 10,
    step_data JSONB NOT NULL DEFAULT '{}',
    is_completed BOOLEAN NOT NULL DEFAULT false,
    completed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '24 hours'),
    
    -- Constraints
    CONSTRAINT valid_step_range CHECK (current_step >= 1 AND current_step <= total_steps),
    CONSTRAINT valid_total_steps CHECK (total_steps > 0),
    CONSTRAINT unique_session_token UNIQUE (session_token),
    CONSTRAINT fk_onboarding_sessions_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for onboarding_sessions
CREATE INDEX IF NOT EXISTS idx_onboarding_sessions_token ON onboarding_sessions (session_token);
CREATE INDEX IF NOT EXISTS idx_onboarding_sessions_user_id ON onboarding_sessions (user_id);
CREATE INDEX IF NOT EXISTS idx_onboarding_sessions_expires ON onboarding_sessions (expires_at);

-- Create updated_at triggers for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON user_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_onboarding_sessions_updated_at BEFORE UPDATE ON onboarding_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""

async def main():
    print("Applying migration to Supabase database...")
    
    try:
        from app.database import get_async_db_context
        from sqlalchemy import text
        
        async with get_async_db_context() as session:
            # Execute the migration SQL
            await session.execute(text(MIGRATION_SQL))
            print("✓ Migration applied successfully!")
            
            # Verify tables were created
            result = await session.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"✓ Created tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())