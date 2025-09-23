"""
Analytics service for FlirtCraft Backend
User behavior tracking, performance monitoring, and business metrics
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..core.database import get_db
from ..core.redis_client import redis_client
from ..models.user import User, UserProfile, Conversation, ConversationMessage

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for tracking user analytics and app performance"""

    def __init__(self):
        self.redis = redis_client

    # Event tracking
    async def track_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        event_data: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """Track user event with metadata"""
        try:
            event_record = {
                "event_type": event_type,
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": event_data or {}
            }

            # Store in Redis for real-time processing
            event_key = f"analytics:events:{datetime.utcnow().strftime('%Y%m%d')}"
            self.redis.client.lpush(event_key, str(event_record))
            self.redis.client.expire(event_key, 86400 * 7)  # 7 days retention

            # Update real-time counters
            await self._update_realtime_metrics(event_type, user_id)

            return True

        except Exception as e:
            logger.error(f"Failed to track event {event_type}: {e}")
            return False

    async def _update_realtime_metrics(self, event_type: str, user_id: Optional[str]):
        """Update real-time metrics counters"""
        try:
            today = datetime.utcnow().strftime('%Y%m%d')

            # Global counters
            self.redis.increment_counter(f"metrics:events:{event_type}:{today}", ttl=86400)
            self.redis.increment_counter(f"metrics:events:total:{today}", ttl=86400)

            # User-specific counters
            if user_id:
                self.redis.increment_counter(f"metrics:user:{user_id}:{event_type}:{today}", ttl=86400)

            # Hourly metrics
            current_hour = datetime.utcnow().strftime('%Y%m%d%H')
            self.redis.increment_counter(f"metrics:hourly:{event_type}:{current_hour}", ttl=86400)

        except Exception as e:
            logger.error(f"Failed to update realtime metrics: {e}")

    # Onboarding analytics
    async def track_onboarding_event(
        self,
        user_id: str,
        step_id: str,
        action: str,  # started, completed, skipped, abandoned
        step_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Track onboarding step events"""
        event_data = {
            "step_id": step_id,
            "action": action,
            "step_data": step_data or {}
        }

        return await self.track_event(
            event_type=f"onboarding_{action}",
            user_id=user_id,
            event_data=event_data
        )

    async def get_onboarding_funnel(self, date_range: int = 7) -> Dict[str, Any]:
        """Get onboarding funnel metrics"""
        try:
            from sqlalchemy import func
            from ..core.database import SessionLocal

            db = SessionLocal()

            # Get user registrations in date range
            start_date = datetime.utcnow() - timedelta(days=date_range)

            registrations = db.query(func.count(User.id)).filter(
                User.created_at >= start_date
            ).scalar()

            completed_onboarding = db.query(func.count(User.id)).filter(
                User.created_at >= start_date,
                User.onboarding_completed == True
            ).scalar()

            # Get step completion rates from Redis
            steps = [
                "welcome", "ageVerification", "preferences",
                "skillGoals", "notifications", "analytics"
            ]

            step_metrics = {}
            for step in steps:
                completed_key = f"metrics:events:onboarding_completed:{step}"
                started_key = f"metrics:events:onboarding_started:{step}"

                completed = self.redis.get_counter(completed_key)
                started = self.redis.get_counter(started_key)

                step_metrics[step] = {
                    "started": started,
                    "completed": completed,
                    "completion_rate": (completed / started * 100) if started > 0 else 0
                }

            db.close()

            return {
                "date_range_days": date_range,
                "total_registrations": registrations,
                "completed_onboarding": completed_onboarding,
                "onboarding_completion_rate": (completed_onboarding / registrations * 100) if registrations > 0 else 0,
                "step_metrics": step_metrics,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get onboarding funnel: {e}")
            return {"error": str(e)}

    # Conversation analytics
    async def track_conversation_event(
        self,
        user_id: str,
        conversation_id: str,
        event_type: str,  # started, message_sent, completed, abandoned
        event_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Track conversation events"""
        event_data = event_data or {}
        event_data.update({
            "conversation_id": conversation_id
        })

        return await self.track_event(
            event_type=f"conversation_{event_type}",
            user_id=user_id,
            event_data=event_data
        )

    async def get_conversation_metrics(self, date_range: int = 7) -> Dict[str, Any]:
        """Get conversation usage metrics"""
        try:
            from sqlalchemy import func
            from ..core.database import SessionLocal

            db = SessionLocal()
            start_date = datetime.utcnow() - timedelta(days=date_range)

            # Total conversations
            total_conversations = db.query(func.count(Conversation.id)).filter(
                Conversation.start_time >= start_date
            ).scalar()

            # Completed conversations
            completed_conversations = db.query(func.count(Conversation.id)).filter(
                Conversation.start_time >= start_date,
                Conversation.status == "completed"
            ).scalar()

            # Average session score
            avg_score = db.query(func.avg(Conversation.session_score)).filter(
                Conversation.start_time >= start_date,
                Conversation.session_score.isnot(None)
            ).scalar()

            # Messages per conversation
            avg_messages = db.query(func.avg(Conversation.total_messages)).filter(
                Conversation.start_time >= start_date,
                Conversation.total_messages > 0
            ).scalar()

            # Popular scenarios
            scenario_stats = db.query(
                Conversation.scenario_type,
                func.count(Conversation.id).label('count')
            ).filter(
                Conversation.start_time >= start_date
            ).group_by(Conversation.scenario_type).all()

            # Difficulty distribution
            difficulty_stats = db.query(
                Conversation.difficulty_level,
                func.count(Conversation.id).label('count')
            ).filter(
                Conversation.start_time >= start_date
            ).group_by(Conversation.difficulty_level).all()

            db.close()

            return {
                "date_range_days": date_range,
                "total_conversations": total_conversations,
                "completed_conversations": completed_conversations,
                "completion_rate": (completed_conversations / total_conversations * 100) if total_conversations > 0 else 0,
                "average_session_score": float(avg_score) if avg_score else 0,
                "average_messages_per_conversation": float(avg_messages) if avg_messages else 0,
                "scenario_distribution": {
                    scenario: count for scenario, count in scenario_stats
                },
                "difficulty_distribution": {
                    level: count for level, count in difficulty_stats
                },
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get conversation metrics: {e}")
            return {"error": str(e)}

    # User engagement analytics
    async def get_user_engagement_metrics(self, date_range: int = 7) -> Dict[str, Any]:
        """Get user engagement and retention metrics"""
        try:
            from sqlalchemy import func
            from ..core.database import SessionLocal

            db = SessionLocal()
            start_date = datetime.utcnow() - timedelta(days=date_range)

            # Daily active users
            dau = db.query(func.count(func.distinct(Conversation.user_id))).filter(
                Conversation.start_time >= datetime.utcnow() - timedelta(days=1)
            ).scalar()

            # Weekly active users
            wau = db.query(func.count(func.distinct(Conversation.user_id))).filter(
                Conversation.start_time >= datetime.utcnow() - timedelta(days=7)
            ).scalar()

            # Monthly active users
            mau = db.query(func.count(func.distinct(Conversation.user_id))).filter(
                Conversation.start_time >= datetime.utcnow() - timedelta(days=30)
            ).scalar()

            # User retention (users who had conversations in multiple days)
            retention_query = text("""
                SELECT COUNT(DISTINCT user_id) as retained_users
                FROM (
                    SELECT user_id, COUNT(DISTINCT DATE(start_time)) as active_days
                    FROM conversations
                    WHERE start_time >= :start_date
                    GROUP BY user_id
                    HAVING active_days > 1
                ) as user_activity
            """)

            retained_users = db.execute(retention_query, {"start_date": start_date}).scalar()

            # Premium conversion rate
            total_users = db.query(func.count(User.id)).filter(
                User.created_at >= start_date
            ).scalar()

            premium_users = db.query(func.count(User.id)).filter(
                User.created_at >= start_date,
                User.is_premium == True
            ).scalar()

            db.close()

            return {
                "date_range_days": date_range,
                "daily_active_users": dau,
                "weekly_active_users": wau,
                "monthly_active_users": mau,
                "retention": {
                    "retained_users": retained_users,
                    "retention_rate": (retained_users / wau * 100) if wau > 0 else 0
                },
                "premium_conversion": {
                    "total_users": total_users,
                    "premium_users": premium_users,
                    "conversion_rate": (premium_users / total_users * 100) if total_users > 0 else 0
                },
                "engagement_ratio": {
                    "dau_wau": (dau / wau * 100) if wau > 0 else 0,
                    "wau_mau": (wau / mau * 100) if mau > 0 else 0
                },
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get engagement metrics: {e}")
            return {"error": str(e)}

    # Performance analytics
    async def track_performance_metric(
        self,
        metric_name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> bool:
        """Track performance metrics"""
        try:
            metric_key = f"performance:{metric_name}:{datetime.utcnow().strftime('%Y%m%d%H')}"

            # Store as time series data
            self.redis.client.lpush(metric_key, f"{datetime.utcnow().timestamp()}:{value}")
            self.redis.client.expire(metric_key, 86400)  # 24 hours

            # Update aggregated metrics
            daily_key = f"performance:daily:{metric_name}:{datetime.utcnow().strftime('%Y%m%d')}"
            self.redis.client.lpush(daily_key, str(value))
            self.redis.client.expire(daily_key, 86400 * 7)  # 7 days

            return True

        except Exception as e:
            logger.error(f"Failed to track performance metric {metric_name}: {e}")
            return False

    async def get_performance_metrics(self, metric_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics for specified time range"""
        try:
            metrics = []
            for hour in range(hours):
                hour_ago = datetime.utcnow() - timedelta(hours=hour)
                metric_key = f"performance:{metric_name}:{hour_ago.strftime('%Y%m%d%H')}"

                values = self.redis.client.lrange(metric_key, 0, -1)
                if values:
                    # Parse timestamp:value pairs
                    hour_metrics = []
                    for value in values:
                        try:
                            timestamp, metric_value = value.split(':')
                            hour_metrics.append({
                                "timestamp": float(timestamp),
                                "value": float(metric_value)
                            })
                        except (ValueError, IndexError):
                            continue

                    if hour_metrics:
                        avg_value = sum(m["value"] for m in hour_metrics) / len(hour_metrics)
                        metrics.append({
                            "hour": hour_ago.strftime('%Y%m%d%H'),
                            "average": avg_value,
                            "count": len(hour_metrics),
                            "values": hour_metrics
                        })

            return {
                "metric_name": metric_name,
                "time_range_hours": hours,
                "data_points": len(metrics),
                "metrics": metrics,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get performance metrics for {metric_name}: {e}")
            return {"error": str(e)}

    # Real-time dashboard data
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get real-time dashboard metrics"""
        try:
            today = datetime.utcnow().strftime('%Y%m%d')

            # Get today's key metrics
            today_events = self.redis.get_counter(f"metrics:events:total:{today}")
            today_registrations = self.redis.get_counter(f"metrics:events:user_registered:{today}")
            today_conversations = self.redis.get_counter(f"metrics:events:conversation_started:{today}")
            today_completions = self.redis.get_counter(f"metrics:events:onboarding_completed:{today}")

            # Get last 24 hours by hour
            hourly_data = []
            for hour in range(24):
                hour_ago = datetime.utcnow() - timedelta(hours=hour)
                hour_key = hour_ago.strftime('%Y%m%d%H')

                hourly_data.append({
                    "hour": hour_key,
                    "events": self.redis.get_counter(f"metrics:hourly:total:{hour_key}"),
                    "conversations": self.redis.get_counter(f"metrics:hourly:conversation_started:{hour_key}"),
                    "registrations": self.redis.get_counter(f"metrics:hourly:user_registered:{hour_key}")
                })

            return {
                "today": {
                    "total_events": today_events,
                    "registrations": today_registrations,
                    "conversations": today_conversations,
                    "onboarding_completions": today_completions
                },
                "hourly_trends": hourly_data,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {"error": str(e)}


# Global analytics service instance
analytics_service = AnalyticsService()


# Dependency for FastAPI
def get_analytics_service() -> AnalyticsService:
    """Dependency to get analytics service"""
    return analytics_service