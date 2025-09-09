"""
User profile and progress endpoints.
"""

from typing import Dict, Any, List
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from uuid import UUID

from ..database import get_async_db
from ..models import User, UserProfile, UserProgress, Conversation, UserAchievement
from ..schemas.user import (
    UserProfileResponse, UserProfileUpdate, UserPreferencesUpdate,
    UserProgressResponse, UserStatsResponse, UserDashboardResponse,
    UserSettingsResponse, UserSettingsUpdate, SkillGoalsUpdate
)
from ..schemas.base import SuccessResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/profile", response_model=SuccessResponse)
async def get_user_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get complete user profile information.
    """
    try:
        stmt = select(User).options(
            selectinload(User.profile)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        profile = user.profile
        
        response_data = UserProfileResponse(
            user_id=user.id,
            email=user.email,
            age=user.age,
            is_active=user.is_active,
            email_verified=user.email_verified,
            onboarding_completed=user.onboarding_completed,
            premium_tier=user.premium_tier,
            is_premium=user.is_premium,
            premium_expires_at=user.premium_expires_at,
            target_gender=profile.target_gender,
            target_age_min=profile.target_age_min,
            target_age_max=profile.target_age_max,
            relationship_goal=profile.relationship_goal,
            primary_skills=profile.primary_skills,
            specific_challenges=profile.specific_challenges,
            skill_goals=profile.skill_goals,
            experience_level=profile.experience_level,
            practice_frequency=profile.practice_frequency,
            persona_detected=profile.persona_detected,
            privacy_level=profile.privacy_level,
            notifications_enabled=profile.notifications_enabled,
            analytics_opt_in=profile.analytics_opt_in,
            marketing_opt_in=profile.marketing_opt_in,
            timezone=profile.timezone,
            locale=profile.locale,
            created_at=user.created_at,
            updated_at=user.updated_at,
            onboarding_completed_at=user.onboarding_completed_at
        )
        
        return SuccessResponse(
            data=response_data,
            message="User profile retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user profile: {str(e)}"
        )


@router.put("/{user_id}/profile", response_model=SuccessResponse)
async def update_user_profile(
    user_id: UUID,
    profile_update: UserProfileUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update user profile information.
    """
    try:
        stmt = select(User).options(
            selectinload(User.profile)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        profile = user.profile
        
        # Update profile fields
        update_data = profile_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(profile)
        
        return SuccessResponse(
            data={"updated": True, "updated_at": profile.updated_at},
            message="User profile updated successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {str(e)}"
        )


@router.put("/{user_id}/preferences", response_model=SuccessResponse)
async def update_user_preferences(
    user_id: UUID,
    preferences_update: UserPreferencesUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update user preferences and privacy settings.
    """
    try:
        stmt = select(User).options(
            selectinload(User.profile)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        profile = user.profile
        
        # Update preference fields
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.utcnow()
        
        await db.commit()
        
        return SuccessResponse(
            data={"updated": True, "updated_at": profile.updated_at},
            message="User preferences updated successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user preferences: {str(e)}"
        )


@router.get("/{user_id}/progress", response_model=SuccessResponse)
async def get_user_progress(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get user progress and statistics.
    """
    try:
        stmt = select(UserProgress).where(UserProgress.user_id == user_id)
        result = await db.execute(stmt)
        progress = result.scalar_one_or_none()
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User progress not found"
            )
        
        response_data = UserProgressResponse(
            user_id=progress.user_id,
            total_conversations=progress.total_conversations,
            total_messages_sent=progress.total_messages_sent,
            total_practice_time=progress.total_practice_time,
            current_streak=progress.current_streak,
            longest_streak=progress.longest_streak,
            last_practice_date=progress.last_practice_date,
            xp_points=progress.xp_points,
            level=progress.level,
            xp_for_next_level=progress.xp_for_next_level,
            xp_progress_percent=progress.xp_progress_percent,
            achievements_unlocked=progress.achievements_unlocked,
            total_achievements=len(progress.achievements_unlocked),
            average_confidence_score=progress.average_confidence_score,
            average_engagement_score=progress.average_engagement_score,
            average_overall_score=progress.average_overall_score,
            progress_metadata=progress.progress_metadata,
            created_at=progress.created_at,
            updated_at=progress.updated_at
        )
        
        return SuccessResponse(
            data=response_data,
            message="User progress retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user progress: {str(e)}"
        )


@router.get("/{user_id}/stats", response_model=SuccessResponse)
async def get_user_stats(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get user statistics and insights for dashboard display.
    """
    try:
        # Get user and progress
        user_stmt = select(User).options(
            selectinload(User.progress),
            selectinload(User.achievements)
        ).where(User.id == user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        progress = user.progress
        if not progress:
            # Create default progress if it doesn't exist
            progress = UserProgress(user_id=user_id)
            db.add(progress)
            await db.commit()
            await db.refresh(progress)
        
        # Get recent activity stats (conversations this week)
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        conversations_this_week_stmt = select(func.count(Conversation.id)).where(
            Conversation.user_id == user_id,
            Conversation.created_at >= week_ago
        )
        conversations_this_week_result = await db.execute(conversations_this_week_stmt)
        conversations_this_week = conversations_this_week_result.scalar() or 0
        
        # Calculate practice time this week
        practice_time_stmt = select(func.sum(Conversation.end_time - Conversation.start_time)).where(
            Conversation.user_id == user_id,
            Conversation.created_at >= week_ago,
            Conversation.end_time.is_not(None)
        )
        practice_time_result = await db.execute(practice_time_stmt)
        practice_time_delta = practice_time_result.scalar()
        practice_time_this_week = int(practice_time_delta.total_seconds() / 60) if practice_time_delta else 0
        
        # Get recent achievements (last 5)
        recent_achievements = []
        if user.achievements:
            sorted_achievements = sorted(user.achievements, key=lambda x: x.earned_at, reverse=True)[:5]
            recent_achievements = [
                {
                    "achievement_type": ach.achievement.achievement_type,
                    "title": ach.achievement.title,
                    "earned_at": ach.earned_at.isoformat()
                }
                for ach in sorted_achievements if ach.achievement
            ]
        
        # Calculate improvement metrics (placeholder logic)
        improvement_rate = None
        strongest_skill = None
        skill_to_work_on = None
        
        if progress.total_conversations > 5:
            # Simple improvement calculation based on score trends
            improvement_rate = 2.5  # Placeholder
            strongest_skill = "conversation_starters"  # Placeholder
            skill_to_work_on = "storytelling"  # Placeholder
        
        response_data = UserStatsResponse(
            user_id=user_id,
            level=progress.level,
            xp_points=progress.xp_points,
            total_conversations=progress.total_conversations,
            current_streak=progress.current_streak,
            is_premium=user.is_premium,
            daily_conversations_used=user.daily_conversations_used,
            conversation_limit_exceeded=user.conversation_limit_exceeded,
            conversations_this_week=conversations_this_week,
            practice_time_this_week=practice_time_this_week,
            improvement_rate=improvement_rate,
            strongest_skill=strongest_skill,
            skill_to_work_on=skill_to_work_on,
            recent_achievements=recent_achievements,
            next_achievement=None  # TODO: Implement next achievement logic
        )
        
        return SuccessResponse(
            data=response_data,
            message="User stats retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user stats: {str(e)}"
        )


@router.get("/{user_id}/dashboard", response_model=SuccessResponse)
async def get_user_dashboard(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get comprehensive dashboard data for user home screen.
    """
    try:
        # Get user with all related data
        stmt = select(User).options(
            selectinload(User.progress),
            selectinload(User.conversations),
            selectinload(User.achievements)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        progress = user.progress or UserProgress(user_id=user_id)
        
        # Calculate daily limit remaining
        daily_limit = 3 if not user.is_premium else 999  # Free users get 3, premium unlimited
        daily_limit_remaining = max(0, daily_limit - user.daily_conversations_used)
        
        # Get recent conversations (last 5)
        recent_conversations = []
        if user.conversations:
            sorted_convs = sorted(user.conversations, key=lambda x: x.created_at, reverse=True)[:5]
            recent_conversations = [
                {
                    "id": str(conv.id),
                    "scenario_type": conv.scenario.scenario_type if conv.scenario else "unknown",
                    "created_at": conv.created_at.isoformat(),
                    "status": conv.status,
                    "score": conv.session_score
                }
                for conv in sorted_convs
            ]
        
        # Get recent achievements
        recent_achievements = []
        if user.achievements:
            sorted_achievements = sorted(user.achievements, key=lambda x: x.earned_at, reverse=True)[:3]
            recent_achievements = [
                {
                    "achievement_type": ach.achievement.achievement_type,
                    "title": ach.achievement.title,
                    "earned_at": ach.earned_at.isoformat(),
                    "is_viewed": ach.is_viewed
                }
                for ach in sorted_achievements if ach.achievement
            ]
        
        # TODO: Get recommended scenarios based on user preferences and progress
        recommended_scenarios = [
            {"scenario_type": "coffee_shop", "difficulty": "green", "reason": "Great for beginners"},
            {"scenario_type": "park", "difficulty": "yellow", "reason": "Practice outdoor conversations"}
        ]
        
        # TODO: Determine skill focus areas based on feedback metrics
        skill_focus_areas = ["conversation_starters", "keeping_flow"]
        
        # Calculate weekly goal progress (placeholder)
        weekly_goal_progress = min(100.0, (progress.total_conversations % 7) * 20)
        
        # Generate personalized encouragement message
        encouragement_messages = [
            "You're making great progress! Keep practicing.",
            "Every conversation makes you more confident.",
            "You've got this! Time for another practice session.",
            "Your communication skills are improving steadily."
        ]
        encouragement_message = encouragement_messages[progress.level % len(encouragement_messages)]
        
        response_data = UserDashboardResponse(
            user_id=user_id,
            email=user.email,
            level=progress.level,
            xp_points=progress.xp_points,
            current_streak=progress.current_streak,
            conversations_today=user.daily_conversations_used,
            daily_limit_remaining=daily_limit_remaining,
            recent_conversations=recent_conversations,
            recent_achievements=recent_achievements,
            recommended_scenarios=recommended_scenarios,
            skill_focus_areas=skill_focus_areas,
            weekly_goal_progress=weekly_goal_progress,
            encouragement_message=encouragement_message
        )
        
        return SuccessResponse(
            data=response_data,
            message="User dashboard data retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user dashboard: {str(e)}"
        )


@router.get("/{user_id}/settings", response_model=SuccessResponse)
async def get_user_settings(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get user settings and preferences.
    """
    try:
        stmt = select(User).options(
            selectinload(User.profile)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User or profile not found"
            )
        
        profile = user.profile
        
        response_data = UserSettingsResponse(
            notifications_enabled=profile.notifications_enabled,
            email_notifications=profile.notifications_enabled,  # Assuming same for now
            push_notifications=profile.notifications_enabled,
            privacy_level=profile.privacy_level,
            analytics_opt_in=profile.analytics_opt_in,
            marketing_opt_in=profile.marketing_opt_in,
            practice_reminders=profile.notifications_enabled,  # Assuming same for now
            achievement_notifications=profile.notifications_enabled,
            timezone=profile.timezone,
            locale=profile.locale,
            email_verified=user.email_verified,
            two_factor_enabled=False  # TODO: Implement 2FA
        )
        
        return SuccessResponse(
            data=response_data,
            message="User settings retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user settings: {str(e)}"
        )


@router.put("/{user_id}/settings", response_model=SuccessResponse)
async def update_user_settings(
    user_id: UUID,
    settings_update: UserSettingsUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update user settings and preferences.
    """
    try:
        stmt = select(User).options(
            selectinload(User.profile)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User or profile not found"
            )
        
        profile = user.profile
        
        # Update settings fields
        update_data = settings_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            # Map settings fields to profile fields
            if field == "notifications_enabled":
                profile.notifications_enabled = value
            elif field in ["email_notifications", "push_notifications", "practice_reminders", "achievement_notifications"]:
                # For now, all notification settings map to the same field
                if value is not None:
                    profile.notifications_enabled = value
            elif hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.utcnow()
        
        await db.commit()
        
        return SuccessResponse(
            data={"updated": True, "updated_at": profile.updated_at},
            message="User settings updated successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user settings: {str(e)}"
        )


@router.put("/{user_id}/skill-goals", response_model=SuccessResponse)
async def update_user_skill_goals(
    user_id: UUID,
    skill_goals_update: SkillGoalsUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update user skill goals selected during onboarding.
    
    This endpoint allows users to modify their skill goals selection
    post-onboarding to refine their learning focus areas.
    """
    try:
        stmt = select(User).options(
            selectinload(User.profile)
        ).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        profile = user.profile
        
        # Update skill goals
        profile.skill_goals = skill_goals_update.skill_goals
        profile.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(profile)
        
        return SuccessResponse(
            data={
                "updated": True, 
                "skill_goals": profile.skill_goals,
                "updated_at": profile.updated_at
            },
            message="Skill goals updated successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update skill goals: {str(e)}"
        )