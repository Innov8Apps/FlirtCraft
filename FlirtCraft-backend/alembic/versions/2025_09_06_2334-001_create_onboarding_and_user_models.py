"""Create onboarding and user models

Revision ID: 001
Revises: 
Create Date: 2025-09-06 23:34:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create all onboarding and user related tables."""
    
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('supabase_user_id', sa.String(length=255), nullable=True),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('premium_tier', sa.String(length=20), nullable=False),
        sa.Column('premium_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('daily_conversations_used', sa.Integer(), nullable=False),
        sa.Column('daily_limit_reset_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('email_verified', sa.Boolean(), nullable=False),
        sa.Column('onboarding_completed', sa.Boolean(), nullable=False),
        sa.Column('onboarding_completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('age >= 18 AND age <= 100', name='valid_age'),
        sa.CheckConstraint('daily_conversations_used >= 0', name='non_negative_conversations'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('supabase_user_id')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=False)
    op.create_index('idx_users_premium', 'users', ['premium_tier', 'premium_expires_at'], unique=False)
    op.create_index('idx_users_supabase_id', 'users', ['supabase_user_id'], unique=False)

    # Create user_profiles table
    op.create_table('user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('target_gender', sa.String(length=20), nullable=False),
        sa.Column('target_age_min', sa.Integer(), nullable=False),
        sa.Column('target_age_max', sa.Integer(), nullable=False),
        sa.Column('relationship_goal', sa.String(length=30), nullable=False),
        sa.Column('primary_skills', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('specific_challenges', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('experience_level', sa.String(length=20), nullable=False),
        sa.Column('practice_frequency', sa.String(length=20), nullable=False),
        sa.Column('privacy_level', sa.String(length=20), nullable=False),
        sa.Column('notifications_enabled', sa.Boolean(), nullable=False),
        sa.Column('analytics_opt_in', sa.Boolean(), nullable=False),
        sa.Column('marketing_opt_in', sa.Boolean(), nullable=False),
        sa.Column('persona_detected', sa.String(length=30), nullable=True),
        sa.Column('onboarding_metadata', postgresql.JSONB(), nullable=False),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('locale', sa.String(length=10), nullable=False),
        sa.CheckConstraint('target_age_min >= 18', name='valid_min_age'),
        sa.CheckConstraint('target_age_max <= 100', name='valid_max_age'),
        sa.CheckConstraint('target_age_min <= target_age_max', name='valid_age_range'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_profiles_preferences', 'user_profiles', ['target_gender', 'experience_level'], unique=False)
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'], unique=False)

    # Create user_progress table
    op.create_table('user_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('total_conversations', sa.Integer(), nullable=False),
        sa.Column('total_messages_sent', sa.Integer(), nullable=False),
        sa.Column('total_practice_time', sa.Integer(), nullable=False),
        sa.Column('current_streak', sa.Integer(), nullable=False),
        sa.Column('longest_streak', sa.Integer(), nullable=False),
        sa.Column('last_practice_date', sa.Date(), nullable=True),
        sa.Column('xp_points', sa.Integer(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('achievements_unlocked', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('average_confidence_score', sa.Float(), nullable=True),
        sa.Column('average_engagement_score', sa.Float(), nullable=True),
        sa.Column('average_overall_score', sa.Float(), nullable=True),
        sa.Column('progress_metadata', postgresql.JSONB(), nullable=False),
        sa.CheckConstraint('average_confidence_score >= 0 AND average_confidence_score <= 100 OR average_confidence_score IS NULL', name='valid_confidence_score'),
        sa.CheckConstraint('average_engagement_score >= 0 AND average_engagement_score <= 100 OR average_engagement_score IS NULL', name='valid_engagement_score'),
        sa.CheckConstraint('average_overall_score >= 0 AND average_overall_score <= 100 OR average_overall_score IS NULL', name='valid_overall_score'),
        sa.CheckConstraint('current_streak >= 0', name='non_negative_current_streak'),
        sa.CheckConstraint('level >= 1', name='minimum_level_one'),
        sa.CheckConstraint('longest_streak >= 0', name='non_negative_longest_streak'),
        sa.CheckConstraint('total_conversations >= 0', name='non_negative_conversations'),
        sa.CheckConstraint('total_messages_sent >= 0', name='non_negative_messages'),
        sa.CheckConstraint('total_practice_time >= 0', name='non_negative_practice_time'),
        sa.CheckConstraint('xp_points >= 0', name='non_negative_xp'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_progress_level_xp', 'user_progress', ['level', 'xp_points'], unique=False)
    op.create_index('idx_user_progress_user_id', 'user_progress', ['user_id'], unique=False)

    # Create onboarding_sessions table
    op.create_table('onboarding_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('session_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('current_step_index', sa.Integer(), nullable=False),
        sa.Column('total_steps', sa.Integer(), nullable=False),
        sa.Column('steps_completed', sa.Integer(), nullable=False),
        sa.Column('steps_skipped', sa.Integer(), nullable=False),
        sa.Column('device_info', postgresql.JSONB(), nullable=False),
        sa.Column('experiment_variants', postgresql.JSONB(), nullable=False),
        sa.Column('referral_source', sa.String(length=100), nullable=True),
        sa.Column('collected_data', postgresql.JSONB(), nullable=False),
        sa.Column('last_active_step', sa.String(length=50), nullable=True),
        sa.Column('abandonment_reason', sa.String(length=100), nullable=True),
        sa.Column('total_duration_seconds', sa.Integer(), nullable=True),
        sa.CheckConstraint('completed_in_range', name='completed_in_range'),
        sa.CheckConstraint('current_step_index >= 0', name='non_negative_step_index'),
        sa.CheckConstraint('current_step_index <= total_steps', name='step_index_in_range'),
        sa.CheckConstraint('skipped_in_range', name='skipped_in_range'),
        sa.CheckConstraint('steps_completed >= 0', name='non_negative_completed'),
        sa.CheckConstraint('steps_completed <= total_steps', name='completed_in_range'),
        sa.CheckConstraint('steps_skipped >= 0', name='non_negative_skipped'),
        sa.CheckConstraint('steps_skipped <= total_steps', name='skipped_in_range'),
        sa.CheckConstraint('total_duration_seconds >= 0 OR total_duration_seconds IS NULL', name='non_negative_duration'),
        sa.CheckConstraint('total_steps > 0', name='positive_total_steps'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_onboarding_sessions_completed', 'onboarding_sessions', ['is_completed', 'session_end'], unique=False)
    op.create_index('idx_onboarding_sessions_progress', 'onboarding_sessions', ['current_step_index', 'steps_completed'], unique=False)
    op.create_index('idx_onboarding_sessions_user_id', 'onboarding_sessions', ['user_id'], unique=False)

    # Create onboarding_steps table
    op.create_table('onboarding_steps',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('step_id', sa.String(length=50), nullable=False),
        sa.Column('step_name', sa.String(length=100), nullable=False),
        sa.Column('step_index', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('step_started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('step_completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('form_data', postgresql.JSONB(), nullable=False),
        sa.Column('validation_errors', postgresql.JSONB(), nullable=False),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
        sa.Column('attempts_count', sa.Integer(), nullable=False),
        sa.Column('interaction_events', postgresql.JSONB(), nullable=False),
        sa.Column('completion_reason', sa.String(length=50), nullable=True),
        sa.Column('skip_reason', sa.String(length=100), nullable=True),
        sa.CheckConstraint('attempts_count > 0', name='positive_attempts'),
        sa.CheckConstraint('step_index >= 0', name='non_negative_step_index'),
        sa.CheckConstraint('time_spent_seconds >= 0 OR time_spent_seconds IS NULL', name='non_negative_time_spent'),
        sa.CheckConstraint('(session_id, step_id)', name='unique_step_per_session'),
        sa.ForeignKeyConstraint(['session_id'], ['onboarding_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_onboarding_steps_session_id', 'onboarding_steps', ['session_id'], unique=False)
    op.create_index('idx_onboarding_steps_status', 'onboarding_steps', ['status', 'step_completed_at'], unique=False)
    op.create_index('idx_onboarding_steps_step_id', 'onboarding_steps', ['step_id'], unique=False)
    op.create_index('idx_onboarding_steps_timing', 'onboarding_steps', ['step_started_at', 'step_completed_at'], unique=False)

    # Create scenarios table
    op.create_table('scenarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('scenario_type', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('is_premium', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('context_templates', postgresql.JSONB(), nullable=False),
        sa.Column('difficulty_modifiers', postgresql.JSONB(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('tags', postgresql.JSONB(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('usage_count', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scenario_type')
    )
    op.create_index('idx_scenarios_category', 'scenarios', ['category'], unique=False)
    op.create_index('idx_scenarios_premium_active', 'scenarios', ['is_premium', 'is_active'], unique=False)
    op.create_index('idx_scenarios_type', 'scenarios', ['scenario_type'], unique=False)

    # Create conversations table
    op.create_table('conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scenario_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('difficulty_level', sa.String(length=10), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('ai_character_context', postgresql.JSONB(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_messages', sa.Integer(), nullable=False),
        sa.Column('user_messages_count', sa.Integer(), nullable=False),
        sa.Column('ai_messages_count', sa.Integer(), nullable=False),
        sa.Column('session_score', sa.Integer(), nullable=True),
        sa.Column('outcome', sa.String(length=20), nullable=True),
        sa.Column('conversation_metadata', postgresql.JSONB(), nullable=False),
        sa.CheckConstraint('ai_messages_count >= 0', name='non_negative_ai_messages'),
        sa.CheckConstraint('session_score >= 0 AND session_score <= 100 OR session_score IS NULL', name='valid_session_score'),
        sa.CheckConstraint('total_messages >= 0', name='non_negative_total_messages'),
        sa.CheckConstraint('user_messages_count >= 0', name='non_negative_user_messages'),
        sa.CheckConstraint('user_messages_count + ai_messages_count <= total_messages', name='valid_message_counts'),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'], unique=False)
    op.create_index('idx_conversations_difficulty', 'conversations', ['difficulty_level'], unique=False)
    op.create_index('idx_conversations_scenario_id', 'conversations', ['scenario_id'], unique=False)
    op.create_index('idx_conversations_status', 'conversations', ['status'], unique=False)
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'], unique=False)

    # Create messages table
    op.create_table('messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender_type', sa.String(length=10), nullable=False),
        sa.Column('message_order', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('ai_response_data', postgresql.JSONB(), nullable=True),
        sa.Column('feedback_type', sa.String(length=20), nullable=True),
        sa.Column('feedback_content', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('message_metadata', postgresql.JSONB(), nullable=False),
        sa.CheckConstraint('LENGTH(content) > 0', name='non_empty_content'),
        sa.CheckConstraint('message_order >= 0', name='non_negative_message_order'),
        sa.CheckConstraint('(conversation_id, message_order)', name='unique_message_order'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'], unique=False)
    op.create_index('idx_messages_order', 'messages', ['conversation_id', 'message_order'], unique=False)
    op.create_index('idx_messages_sender', 'messages', ['sender_type'], unique=False)
    op.create_index('idx_messages_timestamp', 'messages', ['timestamp'], unique=False)

    # Create achievements table
    op.create_table('achievements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('achievement_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=30), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('xp_reward', sa.Integer(), nullable=False),
        sa.Column('badge_icon', sa.String(length=100), nullable=True),
        sa.Column('unlock_criteria', postgresql.JSONB(), nullable=False),
        sa.Column('is_hidden', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('total_unlocks', sa.Integer(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.CheckConstraint('non_negative_unlocks', name='non_negative_unlocks'),
        sa.CheckConstraint('non_negative_xp_reward', name='non_negative_xp_reward'),
        sa.CheckConstraint('total_unlocks >= 0', name='non_negative_unlocks'),
        sa.CheckConstraint('xp_reward >= 0', name='non_negative_xp_reward'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('achievement_type')
    )
    op.create_index('idx_achievements_active', 'achievements', ['is_active', 'is_hidden'], unique=False)
    op.create_index('idx_achievements_category', 'achievements', ['category', 'difficulty'], unique=False)
    op.create_index('idx_achievements_type', 'achievements', ['achievement_type'], unique=False)

    # Create feedback_metrics table
    op.create_table('feedback_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('engagement_score', sa.Integer(), nullable=True),
        sa.Column('responsiveness_score', sa.Integer(), nullable=True),
        sa.Column('storytelling_score', sa.Integer(), nullable=True),
        sa.Column('emotional_intelligence_score', sa.Integer(), nullable=True),
        sa.Column('momentum_score', sa.Integer(), nullable=True),
        sa.Column('flirtation_score', sa.Integer(), nullable=True),
        sa.Column('overall_score', sa.Integer(), nullable=True),
        sa.Column('feedback_text', sa.Text(), nullable=True),
        sa.Column('improvement_suggestions', postgresql.JSONB(), nullable=False),
        sa.Column('positive_highlights', postgresql.JSONB(), nullable=False),
        sa.Column('metric_breakdown', postgresql.JSONB(), nullable=False),
        sa.Column('evaluation_metadata', postgresql.JSONB(), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('evaluation_confidence', sa.Float(), nullable=True),
        sa.Column('human_reviewed', sa.Boolean(), nullable=False),
        sa.CheckConstraint('emotional_intelligence_score >= 0 AND emotional_intelligence_score <= 100 OR emotional_intelligence_score IS NULL', name='valid_emotional_intelligence_score'),
        sa.CheckConstraint('engagement_score >= 0 AND engagement_score <= 100 OR engagement_score IS NULL', name='valid_engagement_score'),
        sa.CheckConstraint('evaluation_confidence >= 0.0 AND evaluation_confidence <= 1.0 OR evaluation_confidence IS NULL', name='valid_confidence'),
        sa.CheckConstraint('flirtation_score >= 0 AND flirtation_score <= 100 OR flirtation_score IS NULL', name='valid_flirtation_score'),
        sa.CheckConstraint('momentum_score >= 0 AND momentum_score <= 100 OR momentum_score IS NULL', name='valid_momentum_score'),
        sa.CheckConstraint('overall_score >= 0 AND overall_score <= 100 OR overall_score IS NULL', name='valid_overall_score'),
        sa.CheckConstraint('responsiveness_score >= 0 AND responsiveness_score <= 100 OR responsiveness_score IS NULL', name='valid_responsiveness_score'),
        sa.CheckConstraint('storytelling_score >= 0 AND storytelling_score <= 100 OR storytelling_score IS NULL', name='valid_storytelling_score'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('conversation_id')
    )
    op.create_index('idx_feedback_metrics_conversation', 'feedback_metrics', ['conversation_id'], unique=False)
    op.create_index('idx_feedback_metrics_human_reviewed', 'feedback_metrics', ['human_reviewed'], unique=False)
    op.create_index('idx_feedback_metrics_scores', 'feedback_metrics', ['overall_score', 'generated_at'], unique=False)

    # Create user_achievements table
    op.create_table('user_achievements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('achievement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('earned_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('progress_data', postgresql.JSONB(), nullable=False),
        sa.Column('is_viewed', sa.Boolean(), nullable=False),
        sa.Column('viewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_shared', sa.Boolean(), nullable=False),
        sa.Column('shared_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement')
    )
    op.create_index('idx_user_achievements_earned_at', 'user_achievements', ['earned_at'], unique=False)
    op.create_index('idx_user_achievements_user_id', 'user_achievements', ['user_id'], unique=False)
    op.create_index('idx_user_achievements_viewed', 'user_achievements', ['is_viewed', 'viewed_at'], unique=False)

    # Insert default scenarios
    scenarios_data = [
        ('coffee_shop', 'Coffee Shops & Cafes', 'Practice in relaxed cafe environments', False, True),
        ('bookstore', 'Bookstores & Libraries', 'Quiet, intellectual spaces for conversation', False, True),
        ('park', 'Parks & Outdoor Spaces', 'Natural settings for casual encounters', False, True),
        ('campus', 'University Campus', 'Academic settings with peer interactions', False, True),
        ('grocery', 'Grocery Stores & Daily Life', 'Everyday situations and encounters', False, True),
        ('gym', 'Gyms & Fitness Centers', 'Active environments with shared interests', True, True),
        ('bar', 'Bars & Social Venues', 'Lively social environments', True, True),
        ('gallery', 'Art Galleries & Cultural Events', 'Sophisticated cultural environments', True, True),
    ]
    
    for i, (scenario_type, display_name, description, is_premium, is_active) in enumerate(scenarios_data):
        op.execute(f"""
            INSERT INTO scenarios (id, created_at, updated_at, scenario_type, display_name, description, is_premium, is_active, context_templates, difficulty_modifiers, tags, sort_order, usage_count)
            VALUES (gen_random_uuid(), NOW(), NOW(), '{scenario_type}', '{display_name}', '{description}', {is_premium}, {is_active}, '{{}}', '{{}}', '[]', {i}, 0)
        """)

    # Insert default achievements
    achievements_data = [
        ('onboarding_complete', 'Welcome to FlirtCraft!', 'Complete your first onboarding session', 'onboarding', 'bronze', 100),
        ('first_conversation', 'Breaking the Ice', 'Complete your first practice conversation', 'conversation', 'bronze', 150),
        ('streak_3_days', 'Getting Consistent', 'Practice for 3 days in a row', 'streak', 'bronze', 200),
        ('streak_7_days', 'Week Warrior', 'Practice for 7 days in a row', 'streak', 'silver', 500),
        ('smooth_operator', 'Smooth Operator', 'Get a Gold rating in any conversation', 'skill', 'silver', 300),
        ('conversationalist', 'Natural Conversationalist', 'Complete 10 practice conversations', 'conversation', 'silver', 400),
    ]
    
    for achievement_type, title, description, category, difficulty, xp_reward in achievements_data:
        op.execute(f"""
            INSERT INTO achievements (id, created_at, updated_at, achievement_type, title, description, category, difficulty, xp_reward, unlock_criteria, is_hidden, is_active, total_unlocks, sort_order)
            VALUES (gen_random_uuid(), NOW(), NOW(), '{achievement_type}', '{title}', '{description}', '{category}', '{difficulty}', {xp_reward}, '{{}}', false, true, 0, 0)
        """)


def downgrade():
    """Drop all tables created in upgrade."""
    op.drop_table('user_achievements')
    op.drop_table('feedback_metrics')
    op.drop_table('achievements')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('scenarios')
    op.drop_table('onboarding_steps')
    op.drop_table('onboarding_sessions')
    op.drop_table('user_progress')
    op.drop_table('user_profiles')
    op.drop_table('users')