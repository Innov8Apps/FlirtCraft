"""
Conversation routes for FlirtCraft Backend
AI-powered conversation practice sessions with real-time feedback
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json

from ..core.database import get_db
from ..core.auth import get_current_user, require_onboarding_completed, check_conversation_limit
from ..core.redis_client import get_redis, job_manager
from ..models.user import User, Conversation, ConversationMessage, UserProfile, UserProgress
from ..services.openrouter import get_openrouter_service, OpenRouterService
from ..schemas.user import StandardResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["Conversations"])


# Pydantic schemas for conversation endpoints
from pydantic import BaseModel, Field

class ConversationCreateRequest(BaseModel):
    scenario_type: str = Field(..., description="Type of scenario for the conversation")
    difficulty_level: str = Field(..., description="Difficulty level: green, yellow, or red")

class MessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Message content")

class ConversationResponse(BaseModel):
    id: str
    scenario_type: str
    difficulty_level: str
    status: str
    ai_character_context: Optional[Dict[str, Any]]
    start_time: datetime
    total_messages: int

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: str
    content: str
    sender_type: str
    message_order: int
    ai_body_language: Optional[str]
    ai_receptiveness: Optional[str]
    feedback_type: Optional[str]
    feedback_content: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=StandardResponse)
async def create_conversation(
    request: ConversationCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_onboarding_completed),
    db: Session = Depends(get_db),
    openrouter: OpenRouterService = Depends(get_openrouter_service),
    redis = Depends(get_redis)
):
    """
    Create a new conversation practice session
    """
    try:
        # Check conversation limits
        if not check_conversation_limit(current_user):
            limit = 50 if current_user.is_premium else 3
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Daily conversation limit reached ({limit} conversations per day). "
                       f"{'Try again tomorrow.' if not current_user.is_premium else 'Premium users get 50 conversations per day.'}"
            )

        # Validate inputs
        if request.difficulty_level not in ["green", "yellow", "red"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid difficulty level. Must be 'green', 'yellow', or 'red'"
            )

        # Get user profile for personalization
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User profile not found. Please complete onboarding first."
            )

        # Generate AI character context
        user_preferences = {
            "target_gender": profile.target_gender,
            "target_age_min": profile.target_age_min,
            "target_age_max": profile.target_age_max,
            "experience_level": profile.experience_level
        }

        character_result = await openrouter.generate_conversation_character(
            scenario_type=request.scenario_type,
            difficulty_level=request.difficulty_level,
            user_preferences=user_preferences
        )

        if not character_result["success"]:
            logger.warning(f"Character generation failed, using fallback: {character_result.get('error')}")
            character_context = character_result.get("fallback", {})
        else:
            character_context = character_result["character"]

        # Create conversation record
        conversation = Conversation(
            user_id=current_user.id,
            scenario_type=request.scenario_type,
            difficulty_level=request.difficulty_level,
            ai_character_context=character_context,
            status="active"
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        # Update user's daily conversation count
        current_user.daily_conversations_used += 1
        db.commit()

        # Cache conversation context for faster access
        cache_key = f"conversation:{conversation.id}:context"
        redis.set_cache(cache_key, character_context, ttl=3600)  # 1 hour TTL

        # Queue analytics job
        background_tasks.add_task(
            job_manager.enqueue_analytics_job,
            "conversation_created",
            str(current_user.id),
            {
                "conversation_id": str(conversation.id),
                "scenario_type": request.scenario_type,
                "difficulty_level": request.difficulty_level,
                "user_experience_level": profile.experience_level
            }
        )

        response_data = {
            "id": str(conversation.id),
            "scenario_type": conversation.scenario_type,
            "difficulty_level": conversation.difficulty_level,
            "status": conversation.status,
            "ai_character_context": character_context,
            "start_time": conversation.start_time,
            "total_messages": 0,
            "conversation_tips": character_context.get("context_tips", []),
            "available_starters": character_context.get("conversation_starters", [])
        }

        return StandardResponse(
            success=True,
            data=response_data,
            message="Conversation session created successfully!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create conversation: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation session"
        )


@router.get("/{conversation_id}", response_model=StandardResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get conversation details and message history
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Get messages
        messages = db.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(ConversationMessage.message_order).all()

        # Format response
        conversation_data = {
            "id": str(conversation.id),
            "scenario_type": conversation.scenario_type,
            "difficulty_level": conversation.difficulty_level,
            "status": conversation.status,
            "ai_character_context": conversation.ai_character_context,
            "start_time": conversation.start_time,
            "end_time": conversation.end_time,
            "total_messages": conversation.total_messages,
            "session_score": conversation.session_score,
            "outcome_level": conversation.outcome_level,
            "messages": [
                {
                    "id": str(msg.id),
                    "content": msg.content,
                    "sender_type": msg.sender_type,
                    "message_order": msg.message_order,
                    "ai_body_language": msg.ai_body_language,
                    "ai_receptiveness": msg.ai_receptiveness,
                    "feedback_type": msg.feedback_type,
                    "feedback_content": msg.feedback_content,
                    "timestamp": msg.timestamp
                }
                for msg in messages
            ]
        }

        return StandardResponse(
            success=True,
            data=conversation_data
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation"
        )


@router.post("/{conversation_id}/messages", response_model=StandardResponse)
async def send_message(
    conversation_id: str,
    message_request: MessageRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    openrouter: OpenRouterService = Depends(get_openrouter_service),
    redis = Depends(get_redis)
):
    """
    Send a message in the conversation and get AI response
    """
    try:
        # Get conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
            Conversation.status == "active"
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active conversation not found"
            )

        # Get conversation history
        messages = db.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(ConversationMessage.message_order).all()

        # Create user message
        user_message = ConversationMessage(
            conversation_id=conversation.id,
            sender_type="user",
            content=message_request.content,
            message_order=len(messages) + 1
        )

        db.add(user_message)
        db.flush()  # Get the ID

        # Build conversation history for AI
        conversation_history = [
            {
                "sender": msg.sender_type,
                "content": msg.content
            }
            for msg in messages
        ]

        # Get cached character context or use stored context
        cache_key = f"conversation:{conversation.id}:context"
        character_context = redis.get_cache(cache_key, as_json=True)
        if not character_context:
            character_context = conversation.ai_character_context or {}

        # Generate AI response
        ai_response_result = await openrouter.generate_ai_response(
            conversation_context={
                "scenario_type": conversation.scenario_type,
                "difficulty_level": conversation.difficulty_level,
                "character": character_context
            },
            user_message=message_request.content,
            conversation_history=conversation_history
        )

        if not ai_response_result["success"]:
            logger.warning(f"AI response generation failed: {ai_response_result.get('error')}")
            ai_response_data = ai_response_result.get("fallback", {
                "content": "That's interesting! Could you tell me more?",
                "body_language": "looks engaged",
                "receptiveness": "moderately receptive"
            })
        else:
            ai_response_data = ai_response_result["response"]

        # Create AI message
        ai_message = ConversationMessage(
            conversation_id=conversation.id,
            sender_type="ai",
            content=ai_response_data["content"],
            message_order=len(messages) + 2,
            ai_body_language=ai_response_data.get("body_language"),
            ai_receptiveness=ai_response_data.get("receptiveness")
        )

        db.add(ai_message)

        # Update conversation stats
        conversation.total_messages = len(messages) + 2

        db.commit()
        db.refresh(user_message)
        db.refresh(ai_message)

        # Queue background jobs
        background_tasks.add_task(
            job_manager.enqueue_analytics_job,
            "message_sent",
            str(current_user.id),
            {
                "conversation_id": str(conversation.id),
                "message_length": len(message_request.content),
                "total_messages": conversation.total_messages
            }
        )

        # Return both messages
        response_data = {
            "user_message": {
                "id": str(user_message.id),
                "content": user_message.content,
                "sender_type": "user",
                "message_order": user_message.message_order,
                "timestamp": user_message.timestamp
            },
            "ai_response": {
                "id": str(ai_message.id),
                "content": ai_message.content,
                "sender_type": "ai",
                "message_order": ai_message.message_order,
                "ai_body_language": ai_message.ai_body_language,
                "ai_receptiveness": ai_message.ai_receptiveness,
                "timestamp": ai_message.timestamp
            },
            "conversation_status": {
                "total_messages": conversation.total_messages,
                "can_continue": conversation.total_messages < 20  # Limit conversation length
            }
        }

        return StandardResponse(
            success=True,
            data=response_data,
            message="Message sent and AI response generated"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )


@router.post("/{conversation_id}/end", response_model=StandardResponse)
async def end_conversation(
    conversation_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    openrouter: OpenRouterService = Depends(get_openrouter_service)
):
    """
    End conversation and generate feedback
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
            Conversation.status == "active"
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active conversation not found"
            )

        # Get conversation messages
        messages = db.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(ConversationMessage.message_order).all()

        if len(messages) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conversation must have at least one exchange before ending"
            )

        # Get user profile for feedback context
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        user_goals = profile.primary_skills if profile else ["general_conversation"]

        # Generate feedback
        conversation_history = [
            {
                "sender": msg.sender_type,
                "content": msg.content
            }
            for msg in messages
        ]

        feedback_result = await openrouter.generate_feedback(
            conversation_history=conversation_history,
            user_goals=user_goals,
            scenario_context={
                "scenario_type": conversation.scenario_type,
                "difficulty_level": conversation.difficulty_level
            }
        )

        if not feedback_result["success"]:
            logger.warning(f"Feedback generation failed: {feedback_result.get('error')}")
            feedback_data = feedback_result.get("fallback", {
                "overall_score": 75,
                "encouragement": "Great job practicing! Keep it up!"
            })
        else:
            feedback_data = feedback_result["feedback"]

        # Update conversation
        conversation.status = "completed"
        conversation.end_time = datetime.utcnow()
        conversation.session_score = feedback_data.get("overall_score", 75)
        conversation.feedback_metrics = feedback_data

        # Determine outcome level
        score = conversation.session_score
        if score >= 80:
            conversation.outcome_level = "gold"
        elif score >= 60:
            conversation.outcome_level = "silver"
        else:
            conversation.outcome_level = "bronze"

        db.commit()

        # Update user progress
        background_tasks.add_task(
            update_user_progress,
            current_user.id,
            conversation.session_score,
            conversation.scenario_type,
            len(messages)
        )

        # Queue analytics
        background_tasks.add_task(
            job_manager.enqueue_analytics_job,
            "conversation_completed",
            str(current_user.id),
            {
                "conversation_id": str(conversation.id),
                "final_score": conversation.session_score,
                "outcome_level": conversation.outcome_level,
                "total_messages": len(messages),
                "duration_minutes": (conversation.end_time - conversation.start_time).total_seconds() / 60
            }
        )

        response_data = {
            "conversation_id": str(conversation.id),
            "session_score": conversation.session_score,
            "outcome_level": conversation.outcome_level,
            "feedback": feedback_data,
            "total_messages": len(messages),
            "duration": str(conversation.end_time - conversation.start_time)
        }

        return StandardResponse(
            success=True,
            data=response_data,
            message=f"Conversation completed! You earned {conversation.outcome_level} level performance."
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to end conversation: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to end conversation"
        )


@router.get("/", response_model=StandardResponse)
async def get_user_conversations(
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's conversation history
    """
    try:
        query = db.query(Conversation).filter(Conversation.user_id == current_user.id)

        if status:
            query = query.filter(Conversation.status == status)

        conversations = query.order_by(
            Conversation.start_time.desc()
        ).offset(offset).limit(limit).all()

        conversation_data = [
            {
                "id": str(conv.id),
                "scenario_type": conv.scenario_type,
                "difficulty_level": conv.difficulty_level,
                "status": conv.status,
                "start_time": conv.start_time,
                "end_time": conv.end_time,
                "total_messages": conv.total_messages,
                "session_score": conv.session_score,
                "outcome_level": conv.outcome_level
            }
            for conv in conversations
        ]

        return StandardResponse(
            success=True,
            data={
                "conversations": conversation_data,
                "total": len(conversation_data),
                "offset": offset,
                "limit": limit
            }
        )

    except Exception as e:
        logger.error(f"Failed to get conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


# Background task functions
async def update_user_progress(
    user_id: str,
    session_score: int,
    scenario_type: str,
    message_count: int
):
    """Update user progress after conversation"""
    try:
        # This would be implemented to update user progress
        # XP, streaks, achievements, etc.
        logger.info(f"Updating progress for user {user_id}: score={session_score}")
    except Exception as e:
        logger.error(f"Failed to update user progress: {e}")