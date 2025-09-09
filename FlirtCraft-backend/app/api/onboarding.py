"""
Onboarding flow endpoints for managing user onboarding sessions and steps.
"""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from uuid import UUID

from ..database import get_async_db
from ..models import OnboardingSession, OnboardingStep, User
from ..schemas.onboarding import (
    OnboardingSessionCreate, OnboardingSessionResponse, OnboardingStepUpdate,
    OnboardingStepResponse, OnboardingCompleteRequest, OnboardingProgressResponse,
    OnboardingAnalyticsResponse
)
from ..schemas.base import SuccessResponse, ErrorResponse


router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.post("/sessions", response_model=SuccessResponse)
async def create_onboarding_session(
    session_data: OnboardingSessionCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create a new onboarding session.
    
    This endpoint starts a new onboarding session for tracking user progress
    through the onboarding flow. Sessions are created before user registration
    to capture the complete onboarding journey.
    """
    try:
        # Create new onboarding session
        session = OnboardingSession(
            # user_id will be set when user account is created
            session_start=datetime.utcnow(),
            device_info=session_data.device_info or {},
            experiment_variants=session_data.experiment_variants or {},
            referral_source=session_data.referral_source
        )
        
        db.add(session)
        await db.commit()
        await db.refresh(session)
        
        # Prepare response
        response_data = OnboardingSessionResponse(
            session_id=session.id,
            user_id=session.user_id,
            is_completed=session.is_completed,
            current_step_index=session.current_step_index,
            total_steps=session.total_steps,
            steps_completed=session.steps_completed,
            steps_skipped=session.steps_skipped,
            session_start=session.session_start,
            session_end=session.session_end,
            duration_minutes=session.duration_minutes,
            completion_rate=session.completion_rate,
            skip_rate=session.skip_rate,
            referral_source=session.referral_source,
            experiment_variants=session.experiment_variants
        )
        
        return SuccessResponse(
            data=response_data,
            message="Onboarding session created successfully"
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create onboarding session: {str(e)}"
        )


@router.get("/sessions/{session_id}", response_model=SuccessResponse)
async def get_onboarding_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get onboarding session details by ID.
    """
    try:
        stmt = select(OnboardingSession).where(OnboardingSession.id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding session not found"
            )
        
        response_data = OnboardingSessionResponse(
            session_id=session.id,
            user_id=session.user_id,
            is_completed=session.is_completed,
            current_step_index=session.current_step_index,
            total_steps=session.total_steps,
            steps_completed=session.steps_completed,
            steps_skipped=session.steps_skipped,
            session_start=session.session_start,
            session_end=session.session_end,
            duration_minutes=session.duration_minutes,
            completion_rate=session.completion_rate,
            skip_rate=session.skip_rate,
            referral_source=session.referral_source,
            experiment_variants=session.experiment_variants
        )
        
        return SuccessResponse(
            data=response_data,
            message="Onboarding session retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get onboarding session: {str(e)}"
        )


@router.post("/sessions/{session_id}/steps", response_model=SuccessResponse)
async def update_onboarding_step(
    session_id: UUID,
    step_data: OnboardingStepUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update or create an onboarding step within a session.
    """
    try:
        # Verify session exists
        session_stmt = select(OnboardingSession).where(OnboardingSession.id == session_id)
        session_result = await db.execute(session_stmt)
        session = session_result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding session not found"
            )
        
        # Check if step already exists
        step_stmt = select(OnboardingStep).where(
            OnboardingStep.session_id == session_id,
            OnboardingStep.step_id == step_data.step_id
        )
        step_result = await db.execute(step_stmt)
        step = step_result.scalar_one_or_none()
        
        if step:
            # Update existing step
            step.step_name = step_data.step_name
            step.step_index = step_data.step_index
            step.status = step_data.status
            step.completion_reason = step_data.completion_reason
            step.skip_reason = step_data.skip_reason
            
            if step_data.form_data:
                step.form_data.update(step_data.form_data)
            
            if step_data.interaction_events:
                if not isinstance(step.interaction_events, list):
                    step.interaction_events = []
                step.interaction_events.extend(step_data.interaction_events)
            
            if step_data.validation_errors:
                step.validation_errors = step_data.validation_errors
            
            # Update step timing if completing
            if step_data.status in ["completed", "skipped"]:
                step.step_completed_at = datetime.utcnow()
                if step.step_started_at:
                    duration = step.step_completed_at - step.step_started_at
                    step.time_spent_seconds = int(duration.total_seconds())
            elif step_data.status == "in_progress" and not step.step_started_at:
                step.step_started_at = datetime.utcnow()
        else:
            # Create new step
            step = OnboardingStep(
                session_id=session_id,
                step_id=step_data.step_id,
                step_name=step_data.step_name,
                step_index=step_data.step_index,
                status=step_data.status,
                form_data=step_data.form_data or {},
                validation_errors=step_data.validation_errors or [],
                interaction_events=step_data.interaction_events or [],
                completion_reason=step_data.completion_reason,
                skip_reason=step_data.skip_reason
            )
            
            if step_data.status == "in_progress":
                step.step_started_at = datetime.utcnow()
            elif step_data.status in ["completed", "skipped"]:
                step.step_started_at = datetime.utcnow()
                step.step_completed_at = datetime.utcnow()
                step.time_spent_seconds = 0
            
            db.add(step)
        
        # Update session progress
        if step_data.status == "completed":
            if step_data.step_id not in [s.step_id for s in session.steps if s.is_completed]:
                session.steps_completed += 1
        elif step_data.status == "skipped":
            if step_data.step_id not in [s.step_id for s in session.steps if s.is_skipped]:
                session.steps_skipped += 1
        
        session.current_step_index = step_data.step_index
        session.last_active_step = step_data.step_id
        
        await db.commit()
        await db.refresh(step)
        
        # Prepare response
        response_data = OnboardingStepResponse(
            step_id=step.id,
            session_id=step.session_id,
            step_identifier=step.step_id,
            step_name=step.step_name,
            step_index=step.step_index,
            status=step.status,
            step_started_at=step.step_started_at,
            step_completed_at=step.step_completed_at,
            time_spent_minutes=step.time_spent_minutes,
            form_data=step.form_data,
            validation_errors=step.validation_errors,
            attempts_count=step.attempts_count,
            completion_reason=step.completion_reason,
            skip_reason=step.skip_reason
        )
        
        return SuccessResponse(
            data=response_data,
            message="Onboarding step updated successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update onboarding step: {str(e)}"
        )


@router.get("/sessions/{session_id}/progress", response_model=SuccessResponse)
async def get_onboarding_progress(
    session_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get detailed progress information for an onboarding session.
    """
    try:
        stmt = select(OnboardingSession).options(
            selectinload(OnboardingSession.steps)
        ).where(OnboardingSession.id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding session not found"
            )
        
        # Calculate progress metrics
        steps_remaining = session.total_steps - session.steps_completed
        
        # Get current and next step info
        current_step = None
        next_step = None
        
        sorted_steps = sorted(session.steps, key=lambda x: x.step_index)
        current_index = session.current_step_index
        
        for step in sorted_steps:
            if step.step_index == current_index:
                current_step = {
                    "step_id": step.step_id,
                    "step_name": step.step_name,
                    "status": step.status
                }
            elif step.step_index == current_index + 1:
                next_step = {
                    "step_id": step.step_id,
                    "step_name": step.step_name
                }
                break
        
        # Calculate timing metrics
        total_duration = 0
        if session.session_start:
            if session.session_end:
                total_duration = int((session.session_end - session.session_start).total_seconds())
            else:
                total_duration = int((datetime.utcnow() - session.session_start).total_seconds())
        
        completed_steps = [s for s in session.steps if s.is_completed]
        avg_step_time = None
        if completed_steps:
            total_step_time = sum(s.time_spent_seconds or 0 for s in completed_steps)
            avg_step_time = (total_step_time / len(completed_steps)) / 60  # Convert to minutes
        
        response_data = OnboardingProgressResponse(
            session_id=session.id,
            completion_rate=session.completion_rate,
            steps_remaining=steps_remaining,
            estimated_time_remaining=int(avg_step_time * steps_remaining) if avg_step_time else None,
            current_step=current_step,
            next_step=next_step,
            can_skip_current=True,  # TODO: Implement logic based on step configuration
            can_go_back=session.current_step_index > 0,
            time_spent_total=total_duration,
            average_step_time=avg_step_time
        )
        
        return SuccessResponse(
            data=response_data,
            message="Onboarding progress retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get onboarding progress: {str(e)}"
        )


@router.post("/complete", response_model=SuccessResponse)
async def complete_onboarding(
    completion_data: OnboardingCompleteRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Complete the onboarding process and create user account.
    
    This endpoint marks the onboarding session as complete and triggers
    user account creation with all collected data.
    """
    try:
        # Get the onboarding session
        stmt = select(OnboardingSession).where(OnboardingSession.id == completion_data.session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding session not found"
            )
        
        if session.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Onboarding session already completed"
            )
        
        # Mark session as completed
        session.mark_completed()
        
        # Store the collected data in the session
        session.collected_data.update({
            "registration_data": completion_data.registration_data,
            "preferences_data": completion_data.preferences_data,
            "skill_goals_data": completion_data.skill_goals_data,
            "final_persona": completion_data.final_persona.value if completion_data.final_persona else None,
            "completion_reason": completion_data.completion_reason
        })
        
        await db.commit()
        
        return SuccessResponse(
            data={
                "session_id": session.id,
                "completed": True,
                "duration_minutes": session.duration_minutes,
                "completion_rate": session.completion_rate,
                "ready_for_registration": True
            },
            message="Onboarding completed successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete onboarding: {str(e)}"
        )


@router.post("/sessions/{session_id}/abandon", response_model=SuccessResponse)
async def abandon_onboarding(
    session_id: UUID,
    reason: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Mark an onboarding session as abandoned.
    """
    try:
        stmt = select(OnboardingSession).where(OnboardingSession.id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding session not found"
            )
        
        if session.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot abandon completed onboarding session"
            )
        
        session.mark_abandoned(reason)
        await db.commit()
        
        return SuccessResponse(
            data={
                "session_id": session.id,
                "abandoned": True,
                "reason": reason,
                "duration_minutes": session.duration_minutes
            },
            message="Onboarding session marked as abandoned"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to abandon onboarding session: {str(e)}"
        )


@router.get("/analytics", response_model=SuccessResponse)
async def get_onboarding_analytics(
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get onboarding analytics and metrics.
    
    This endpoint provides aggregate analytics about onboarding performance,
    completion rates, and user behavior patterns.
    """
    try:
        # Get session counts
        total_sessions_stmt = select(func.count(OnboardingSession.id))
        total_sessions_result = await db.execute(total_sessions_stmt)
        total_sessions = total_sessions_result.scalar() or 0
        
        completed_sessions_stmt = select(func.count(OnboardingSession.id)).where(
            OnboardingSession.is_completed == True
        )
        completed_sessions_result = await db.execute(completed_sessions_stmt)
        completed_sessions = completed_sessions_result.scalar() or 0
        
        abandoned_sessions = total_sessions - completed_sessions
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Get timing metrics for completed sessions
        avg_duration_stmt = select(func.avg(OnboardingSession.total_duration_seconds)).where(
            OnboardingSession.is_completed == True
        )
        avg_duration_result = await db.execute(avg_duration_stmt)
        avg_duration_seconds = avg_duration_result.scalar() or 0
        avg_duration_minutes = avg_duration_seconds / 60 if avg_duration_seconds else None
        
        # TODO: Add more detailed analytics queries
        # - Step completion rates
        # - Step skip rates  
        # - Drop-off analysis
        # - Persona-based analytics
        
        response_data = OnboardingAnalyticsResponse(
            total_sessions=total_sessions,
            completed_sessions=completed_sessions,
            abandoned_sessions=abandoned_sessions,
            completion_rate=completion_rate,
            average_completion_time=avg_duration_minutes,
            median_completion_time=avg_duration_minutes,  # Placeholder
            step_completion_rates={},  # TODO: Implement
            step_skip_rates={},  # TODO: Implement
            step_average_times={},  # TODO: Implement
            common_drop_off_points=[],  # TODO: Implement
            completion_by_persona={},  # TODO: Implement
            completion_by_source={}  # TODO: Implement
        )
        
        return SuccessResponse(
            data=response_data,
            message="Onboarding analytics retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get onboarding analytics: {str(e)}"
        )