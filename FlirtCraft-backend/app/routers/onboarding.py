"""
Onboarding routes for FlirtCraft Backend
Multi-step onboarding process with user preferences, skill goals, and profile creation
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging
from datetime import datetime

from ..core.database import get_db
from ..core.auth import get_current_user, get_current_active_user, log_auth_event
from ..models.user import User, UserProfile, UserProgress, Scenario
from ..schemas.user import (
    AgeVerificationRequest,
    UserPreferencesRequest,
    SkillGoalsRequest,
    PrivacySettingsRequest,
    OnboardingProgressRequest,
    UserResponse,
    UserProfileResponse,
    OnboardingFlowResponse,
    OnboardingStepResponse,
    StandardResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


# Onboarding step configuration based on documentation
ONBOARDING_STEPS = [
    {
        "id": "welcome",
        "title": "Welcome",
        "component": "WelcomeIntro",
        "required": True,
        "skippable": False,
        "estimated_duration": 30
    },
    {
        "id": "howItWorks1",
        "title": "Choose Scenario",
        "component": "HowItWorksStep",
        "required": True,
        "skippable": True,
        "estimated_duration": 15
    },
    {
        "id": "howItWorks2",
        "title": "AI Conversation",
        "component": "HowItWorksStep",
        "required": True,
        "skippable": True,
        "estimated_duration": 15
    },
    {
        "id": "howItWorks3",
        "title": "Get Feedback",
        "component": "HowItWorksStep",
        "required": True,
        "skippable": True,
        "estimated_duration": 15
    },
    {
        "id": "privacy",
        "title": "Privacy & Safety",
        "component": "PrivacySafety",
        "required": True,
        "skippable": False,
        "estimated_duration": 30
    },
    {
        "id": "ageVerification",
        "title": "Age Verification",
        "component": "AgeVerification",
        "required": True,
        "skippable": False,
        "estimated_duration": 15
    },
    {
        "id": "preferences",
        "title": "Preferences",
        "component": "PreferenceSetup",
        "required": True,
        "skippable": False,
        "estimated_duration": 60
    },
    {
        "id": "skillGoals",
        "title": "Goals",
        "component": "SkillGoalSelection",
        "required": True,
        "skippable": False,
        "estimated_duration": 45
    },
    {
        "id": "notifications",
        "title": "Notifications",
        "component": "NotificationPermission",
        "required": False,
        "skippable": True,
        "estimated_duration": 30
    },
    {
        "id": "analytics",
        "title": "Help Improve",
        "component": "AnalyticsConsent",
        "required": False,
        "skippable": True,
        "estimated_duration": 20
    },
    {
        "id": "complete",
        "title": "Ready to Start",
        "component": "ReadyToStart",
        "required": True,
        "skippable": False,
        "estimated_duration": 15
    }
]


@router.get("/flow", response_model=OnboardingFlowResponse)
async def get_onboarding_flow(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the complete onboarding flow configuration
    Returns current progress and available steps
    """
    try:
        # Get user's profile to determine progress
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

        completed_steps = []
        if profile:
            completed_steps = profile.onboarding_steps_completed or []

        # Build step responses with completion status
        steps = []
        for step_config in ONBOARDING_STEPS:
            step = OnboardingStepResponse(
                id=step_config["id"],
                title=step_config["title"],
                component=step_config["component"],
                required=step_config["required"],
                completed=step_config["id"] in completed_steps,
                skippable=step_config["skippable"],
                estimated_duration=step_config.get("estimated_duration")
            )
            steps.append(step)

        # Determine current step
        current_step_index = 0
        for i, step in enumerate(steps):
            if not step.completed:
                current_step_index = i
                break
        else:
            # All steps completed
            current_step_index = len(steps) - 1

        return OnboardingFlowResponse(
            current_step_index=current_step_index,
            total_steps=len(steps),
            steps=steps,
            can_go_back=current_step_index > 0,
            can_skip_current=steps[current_step_index].skippable if current_step_index < len(steps) else False,
            is_complete=current_user.onboarding_completed
        )

    except Exception as e:
        logger.error(f"Failed to get onboarding flow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve onboarding flow"
        )


@router.post("/progress", response_model=StandardResponse)
async def update_onboarding_progress(
    progress_data: OnboardingProgressRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's progress through onboarding steps
    """
    try:
        # Get or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            profile = UserProfile(
                user_id=current_user.id,
                onboarding_steps_completed=[],
                onboarding_steps_skipped=[]
            )
            db.add(profile)

        # Update completed steps
        if progress_data.completed and progress_data.step_id not in profile.onboarding_steps_completed:
            profile.onboarding_steps_completed.append(progress_data.step_id)

        # Update skipped steps
        if progress_data.skipped and progress_data.step_id not in profile.onboarding_steps_skipped:
            profile.onboarding_steps_skipped.append(progress_data.step_id)

        db.commit()

        # Log progress event
        await log_auth_event(
            event_type="onboarding_progress",
            user_id=str(current_user.id),
            details={
                "step_id": progress_data.step_id,
                "completed": progress_data.completed,
                "skipped": progress_data.skipped,
                "step_data": progress_data.step_data
            }
        )

        return StandardResponse(
            success=True,
            message=f"Progress updated for step: {progress_data.step_id}"
        )

    except Exception as e:
        logger.error(f"Failed to update onboarding progress: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update onboarding progress"
        )


@router.post("/age-verification", response_model=StandardResponse)
async def verify_age(
    age_data: AgeVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify user's age (18+ required)
    """
    try:
        # Get or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            profile = UserProfile(user_id=current_user.id)
            db.add(profile)

        # Update age verification
        profile.age_verified = True
        profile.birth_year = age_data.birth_year

        # Mark step as completed
        if "ageVerification" not in (profile.onboarding_steps_completed or []):
            if profile.onboarding_steps_completed is None:
                profile.onboarding_steps_completed = []
            profile.onboarding_steps_completed.append("ageVerification")

        db.commit()

        # Log age verification
        await log_auth_event(
            event_type="age_verified",
            user_id=str(current_user.id),
            details={
                "birth_year": age_data.birth_year,
                "age": datetime.now().year - age_data.birth_year
            }
        )

        return StandardResponse(
            success=True,
            message="Age verification completed successfully"
        )

    except Exception as e:
        logger.error(f"Age verification failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Age verification failed"
        )


@router.post("/preferences", response_model=StandardResponse)
async def set_user_preferences(
    preferences: UserPreferencesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set user's dating preferences
    """
    try:
        # Get or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            profile = UserProfile(user_id=current_user.id)
            db.add(profile)

        # Update preferences
        profile.target_gender = preferences.target_gender.value
        profile.target_age_min = preferences.target_age_min
        profile.target_age_max = preferences.target_age_max
        profile.relationship_goal = preferences.relationship_goal.value

        # Mark step as completed
        if "preferences" not in (profile.onboarding_steps_completed or []):
            if profile.onboarding_steps_completed is None:
                profile.onboarding_steps_completed = []
            profile.onboarding_steps_completed.append("preferences")

        db.commit()

        # Log preferences update
        await log_auth_event(
            event_type="preferences_set",
            user_id=str(current_user.id),
            details={
                "target_gender": preferences.target_gender.value,
                "age_range": f"{preferences.target_age_min}-{preferences.target_age_max}",
                "relationship_goal": preferences.relationship_goal.value
            }
        )

        return StandardResponse(
            success=True,
            message="Preferences saved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to save preferences: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save preferences"
        )


@router.post("/skill-goals", response_model=StandardResponse)
async def set_skill_goals(
    goals: SkillGoalsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set user's skill development goals
    """
    try:
        # Get or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            profile = UserProfile(user_id=current_user.id)
            db.add(profile)

        # Update skill goals
        profile.primary_skills = goals.primary_skills
        profile.specific_challenges = goals.specific_challenges
        profile.experience_level = goals.experience_level.value
        profile.practice_frequency = goals.practice_frequency.value

        # Mark step as completed
        if "skillGoals" not in (profile.onboarding_steps_completed or []):
            if profile.onboarding_steps_completed is None:
                profile.onboarding_steps_completed = []
            profile.onboarding_steps_completed.append("skillGoals")

        db.commit()

        # Log skill goals update
        await log_auth_event(
            event_type="skill_goals_set",
            user_id=str(current_user.id),
            details={
                "primary_skills": goals.primary_skills,
                "experience_level": goals.experience_level.value,
                "practice_frequency": goals.practice_frequency.value,
                "challenges_count": len(goals.specific_challenges)
            }
        )

        return StandardResponse(
            success=True,
            message="Skill goals saved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to save skill goals: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save skill goals"
        )


@router.post("/privacy-settings", response_model=StandardResponse)
async def set_privacy_settings(
    privacy: PrivacySettingsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set user's privacy and notification preferences
    """
    try:
        # Get or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            profile = UserProfile(user_id=current_user.id)
            db.add(profile)

        # Update privacy settings
        profile.notifications_enabled = privacy.notifications_enabled
        profile.analytics_opt_in = privacy.analytics_opt_in
        profile.privacy_level = privacy.privacy_level.value
        profile.marketing_opt_in = privacy.marketing_opt_in

        # Mark relevant steps as completed
        steps_to_complete = []
        if privacy.notifications_enabled is not None:
            steps_to_complete.append("notifications")
        if privacy.analytics_opt_in is not None:
            steps_to_complete.append("analytics")

        if profile.onboarding_steps_completed is None:
            profile.onboarding_steps_completed = []

        for step in steps_to_complete:
            if step not in profile.onboarding_steps_completed:
                profile.onboarding_steps_completed.append(step)

        db.commit()

        # Log privacy settings update
        await log_auth_event(
            event_type="privacy_settings_set",
            user_id=str(current_user.id),
            details={
                "notifications_enabled": privacy.notifications_enabled,
                "analytics_opt_in": privacy.analytics_opt_in,
                "privacy_level": privacy.privacy_level.value,
                "marketing_opt_in": privacy.marketing_opt_in
            }
        )

        return StandardResponse(
            success=True,
            message="Privacy settings saved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to save privacy settings: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save privacy settings"
        )


@router.post("/complete", response_model=StandardResponse)
async def complete_onboarding(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete the onboarding process
    Creates full user profile and initializes progress tracking
    """
    try:
        # Check if onboarding is already completed
        if current_user.onboarding_completed:
            return StandardResponse(
                success=True,
                message="Onboarding already completed"
            )

        # Get user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User profile not found. Please complete required onboarding steps."
            )

        # Validate required steps are completed
        required_steps = [step["id"] for step in ONBOARDING_STEPS if step["required"]]
        completed_steps = profile.onboarding_steps_completed or []

        missing_steps = [step for step in required_steps if step not in completed_steps]
        if missing_steps:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Required onboarding steps not completed: {', '.join(missing_steps)}"
            )

        # Calculate onboarding duration
        onboarding_duration = None
        if profile.created_at:
            duration_delta = datetime.utcnow() - profile.created_at.replace(tzinfo=None)
            onboarding_duration = int(duration_delta.total_seconds())

        # Update profile completion status
        profile.onboarding_duration_seconds = onboarding_duration

        # Mark user onboarding as completed
        current_user.onboarding_completed = True
        current_user.onboarding_completed_at = datetime.utcnow()

        # Create or update user progress record
        progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).first()
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                total_conversations=0,
                xp_points=0,
                level=1,
                achievements_unlocked=["onboarding_complete"]
            )
            db.add(progress)
        else:
            # Add onboarding completion achievement if not already present
            if "onboarding_complete" not in progress.achievements_unlocked:
                progress.achievements_unlocked.append("onboarding_complete")

        db.commit()

        # Log onboarding completion
        await log_auth_event(
            event_type="onboarding_completed",
            user_id=str(current_user.id),
            details={
                "duration_seconds": onboarding_duration,
                "completed_steps": len(completed_steps),
                "skipped_steps": len(profile.onboarding_steps_skipped or []),
                "experience_level": profile.experience_level,
                "primary_skills": profile.primary_skills
            }
        )

        # Send completion email in background
        background_tasks.add_task(send_onboarding_completion_email, current_user.email)

        # Initialize user for first conversation in background
        background_tasks.add_task(initialize_user_for_conversations, current_user.id)

        return StandardResponse(
            success=True,
            message="Onboarding completed successfully! Welcome to FlirtCraft!",
            data={
                "achievements_unlocked": progress.achievements_unlocked,
                "ready_for_conversations": True
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to complete onboarding: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete onboarding"
        )


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's onboarding profile data
    """
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )

        return UserProfileResponse.from_orm(profile)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )


@router.delete("/reset", response_model=StandardResponse)
async def reset_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reset onboarding progress (for development/testing)
    Only available in development environment
    """
    try:
        from ..core.config import settings

        if settings.environment == "production":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Onboarding reset not allowed in production"
            )

        # Reset user onboarding status
        current_user.onboarding_completed = False
        current_user.onboarding_completed_at = None

        # Delete profile if it exists
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if profile:
            db.delete(profile)

        # Reset progress
        progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).first()
        if progress:
            progress.achievements_unlocked = []
            progress.xp_points = 0
            progress.level = 1

        db.commit()

        await log_auth_event(
            event_type="onboarding_reset",
            user_id=str(current_user.id),
            details={"environment": settings.environment}
        )

        return StandardResponse(
            success=True,
            message="Onboarding progress reset successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to reset onboarding: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset onboarding"
        )


# Background task functions
async def send_onboarding_completion_email(email: str):
    """Send onboarding completion email"""
    try:
        logger.info(f"Sending onboarding completion email to {email}")
        # Implementation would use email service
    except Exception as e:
        logger.error(f"Failed to send completion email to {email}: {e}")


async def initialize_user_for_conversations(user_id: str):
    """Initialize user data for first conversations"""
    try:
        logger.info(f"Initializing user {user_id} for conversations")
        # Pre-load scenarios, initialize recommendation engine, etc.
    except Exception as e:
        logger.error(f"Failed to initialize user {user_id}: {e}")