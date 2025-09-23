"""
Analytics routes for FlirtCraft Backend
Business metrics, performance monitoring, and usage analytics
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
import logging

from ..core.auth import get_current_user
from ..models.user import User
from ..services.analytics import get_analytics_service, AnalyticsService
from ..schemas.user import StandardResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=StandardResponse)
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get real-time dashboard metrics
    Note: In production, this should have admin-only access control
    """
    try:
        dashboard_data = await analytics.get_dashboard_data()

        return StandardResponse(
            success=True,
            data=dashboard_data,
            message="Dashboard metrics retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard metrics"
        )


@router.get("/onboarding-funnel", response_model=StandardResponse)
async def get_onboarding_funnel(
    date_range: int = 7,
    current_user: User = Depends(get_current_user),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get onboarding funnel metrics
    """
    try:
        funnel_data = await analytics.get_onboarding_funnel(date_range)

        return StandardResponse(
            success=True,
            data=funnel_data,
            message=f"Onboarding funnel data for {date_range} days retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to get onboarding funnel: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve onboarding funnel data"
        )


@router.get("/conversations", response_model=StandardResponse)
async def get_conversation_analytics(
    date_range: int = 7,
    current_user: User = Depends(get_current_user),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get conversation usage analytics
    """
    try:
        conversation_data = await analytics.get_conversation_metrics(date_range)

        return StandardResponse(
            success=True,
            data=conversation_data,
            message=f"Conversation analytics for {date_range} days retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to get conversation analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation analytics"
        )


@router.get("/engagement", response_model=StandardResponse)
async def get_engagement_metrics(
    date_range: int = 7,
    current_user: User = Depends(get_current_user),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get user engagement and retention metrics
    """
    try:
        engagement_data = await analytics.get_user_engagement_metrics(date_range)

        return StandardResponse(
            success=True,
            data=engagement_data,
            message=f"User engagement metrics for {date_range} days retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to get engagement metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve engagement metrics"
        )


@router.get("/performance/{metric_name}", response_model=StandardResponse)
async def get_performance_metrics(
    metric_name: str,
    hours: int = 24,
    current_user: User = Depends(get_current_user),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get performance metrics for specific metric
    """
    try:
        performance_data = await analytics.get_performance_metrics(metric_name, hours)

        return StandardResponse(
            success=True,
            data=performance_data,
            message=f"Performance metrics for {metric_name} retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Failed to get performance metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve performance metrics"
        )


@router.post("/track", response_model=StandardResponse)
async def track_custom_event(
    event_type: str,
    event_data: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Track custom analytics event
    """
    try:
        success = await analytics.track_event(
            event_type=event_type,
            user_id=str(current_user.id),
            event_data=event_data
        )

        if success:
            return StandardResponse(
                success=True,
                message="Event tracked successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to track event"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to track event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track event"
        )


# Development-only endpoints
from ..core.config import settings

if settings.environment == "development":
    @router.get("/dev/events", response_model=StandardResponse)
    async def get_recent_events(
        limit: int = 100,
        current_user: User = Depends(get_current_user),
        analytics: AnalyticsService = Depends(get_analytics_service)
    ):
        """
        Get recent events for development debugging
        """
        try:
            from datetime import datetime

            # Get today's events from Redis
            today = datetime.utcnow().strftime('%Y%m%d')
            event_key = f"analytics:events:{today}"

            events = analytics.redis.client.lrange(event_key, 0, limit - 1)

            event_data = []
            for event in events:
                try:
                    # Parse event string back to dict
                    import ast
                    event_dict = ast.literal_eval(event)
                    event_data.append(event_dict)
                except Exception:
                    continue

            return StandardResponse(
                success=True,
                data={
                    "events": event_data,
                    "total_shown": len(event_data),
                    "date": today
                },
                message="Recent events retrieved for development"
            )

        except Exception as e:
            logger.error(f"Failed to get recent events: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve recent events"
            )

    @router.post("/dev/simulate-events", response_model=StandardResponse)
    async def simulate_analytics_events(
        event_count: int = 10,
        current_user: User = Depends(get_current_user),
        analytics: AnalyticsService = Depends(get_analytics_service)
    ):
        """
        Simulate analytics events for development testing
        """
        try:
            import random
            from datetime import datetime, timedelta

            events = [
                "user_registered",
                "onboarding_started",
                "onboarding_completed",
                "conversation_started",
                "conversation_completed",
                "message_sent"
            ]

            scenarios = ["coffee_shop", "bookstore", "park", "campus"]
            difficulties = ["green", "yellow", "red"]

            simulated_events = []

            for i in range(event_count):
                event_type = random.choice(events)

                event_data = {
                    "simulated": True,
                    "simulation_id": i
                }

                if "conversation" in event_type:
                    event_data.update({
                        "scenario_type": random.choice(scenarios),
                        "difficulty_level": random.choice(difficulties)
                    })

                success = await analytics.track_event(
                    event_type=event_type,
                    user_id=str(current_user.id),
                    event_data=event_data
                )

                if success:
                    simulated_events.append({
                        "event_type": event_type,
                        "data": event_data
                    })

            return StandardResponse(
                success=True,
                data={
                    "simulated_events": simulated_events,
                    "total_simulated": len(simulated_events)
                },
                message=f"Simulated {len(simulated_events)} analytics events"
            )

        except Exception as e:
            logger.error(f"Failed to simulate events: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to simulate analytics events"
            )