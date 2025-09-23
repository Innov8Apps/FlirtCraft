"""
Redis client configuration for FlirtCraft Backend
Caching, session storage, and background job queue management
"""

import redis
import logging
from typing import Optional, Dict, Any, Union
import json
import pickle
from datetime import timedelta

from .config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper with connection management"""

    def __init__(self):
        self._client: Optional[redis.Redis] = None
        self._connected = False

    def _initialize_client(self):
        """Initialize Redis connection"""
        try:
            # Parse Redis URL
            redis_url = settings.redis_url
            if settings.redis_password:
                # Add password to URL if not already present
                if "@" not in redis_url:
                    redis_url = redis_url.replace("://", f"://:{settings.redis_password}@")

            self._client = redis.from_url(
                redis_url,
                decode_responses=True,
                health_check_interval=30,
                socket_keepalive=True,
                socket_keepalive_options={}
            )

            # Test connection
            self._client.ping()
            self._connected = True
            logger.info("✅ Redis connection established")

        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            self._connected = False
            self._client = None

    @property
    def client(self) -> redis.Redis:
        """Get Redis client instance"""
        if not self._client or not self._connected:
            self._initialize_client()
        return self._client

    def health_check(self) -> Dict[str, Any]:
        """Check Redis connection health"""
        try:
            if not self._client:
                self._initialize_client()

            if self._client:
                self._client.ping()
                return {
                    "status": "healthy",
                    "service": "redis",
                    "connected": True,
                    "info": {
                        "memory_usage": self._get_memory_info(),
                        "connected_clients": self._get_client_count()
                    }
                }
            else:
                return {
                    "status": "unhealthy",
                    "service": "redis",
                    "connected": False,
                    "error": "No connection established"
                }

        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "service": "redis",
                "connected": False,
                "error": str(e)
            }

    def _get_memory_info(self) -> str:
        """Get Redis memory usage info"""
        try:
            info = self._client.info("memory")
            used_memory = info.get("used_memory_human", "unknown")
            return used_memory
        except Exception:
            return "unknown"

    def _get_client_count(self) -> int:
        """Get number of connected clients"""
        try:
            info = self._client.info("clients")
            return info.get("connected_clients", 0)
        except Exception:
            return 0

    # Cache operations
    def set_cache(
        self,
        key: str,
        value: Union[str, Dict, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Set cache value with optional TTL"""
        try:
            if not self.client:
                return False

            # Serialize complex objects
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            elif not isinstance(value, str):
                value = str(value)

            if ttl:
                return self.client.setex(key, ttl, value)
            else:
                return self.client.set(key, value)

        except Exception as e:
            logger.error(f"Failed to set cache {key}: {e}")
            return False

    def get_cache(self, key: str, as_json: bool = False) -> Optional[Union[str, Dict]]:
        """Get cache value"""
        try:
            if not self.client:
                return None

            value = self.client.get(key)
            if value is None:
                return None

            if as_json:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value

            return value

        except Exception as e:
            logger.error(f"Failed to get cache {key}: {e}")
            return None

    def delete_cache(self, key: str) -> bool:
        """Delete cache entry"""
        try:
            if not self.client:
                return False
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Failed to delete cache {key}: {e}")
            return False

    def cache_exists(self, key: str) -> bool:
        """Check if cache key exists"""
        try:
            if not self.client:
                return False
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Failed to check cache existence {key}: {e}")
            return False

    # Rate limiting operations
    def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> Dict[str, Any]:
        """Check rate limit using sliding window"""
        try:
            if not self.client:
                return {"allowed": True, "remaining": limit}

            current_time = int(time.time())
            window_start = current_time - window

            # Use pipeline for atomic operations
            pipe = self.client.pipeline()

            # Remove old entries
            pipe.zremrangebyscore(key, 0, window_start)

            # Count current requests
            pipe.zcard(key)

            # Add current request
            pipe.zadd(key, {str(current_time): current_time})

            # Set expiry for the key
            pipe.expire(key, window + 1)

            results = pipe.execute()
            current_count = results[1]

            allowed = current_count < limit
            remaining = max(0, limit - current_count - 1)

            return {
                "allowed": allowed,
                "remaining": remaining,
                "reset_time": current_time + window,
                "current_count": current_count
            }

        except Exception as e:
            logger.error(f"Rate limit check failed for {key}: {e}")
            # Fail open - allow request if Redis is down
            return {"allowed": True, "remaining": limit}

    # Session management
    def set_session(
        self,
        session_id: str,
        session_data: Dict[str, Any],
        ttl: int = 3600
    ) -> bool:
        """Set session data"""
        try:
            session_key = f"session:{session_id}"
            return self.set_cache(session_key, session_data, ttl)
        except Exception as e:
            logger.error(f"Failed to set session {session_id}: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        try:
            session_key = f"session:{session_id}"
            return self.get_cache(session_key, as_json=True)
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {e}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        try:
            session_key = f"session:{session_id}"
            return self.delete_cache(session_key)
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False

    # Background job queue operations
    def enqueue_job(
        self,
        queue_name: str,
        job_data: Dict[str, Any],
        priority: int = 0
    ) -> bool:
        """Enqueue background job"""
        try:
            if not self.client:
                return False

            job_payload = {
                "id": f"{queue_name}:{int(time.time())}:{priority}",
                "queue": queue_name,
                "data": job_data,
                "created_at": int(time.time()),
                "priority": priority
            }

            # Add to sorted set with priority as score
            queue_key = f"queue:{queue_name}"
            return bool(self.client.zadd(
                queue_key,
                {json.dumps(job_payload): priority}
            ))

        except Exception as e:
            logger.error(f"Failed to enqueue job to {queue_name}: {e}")
            return False

    def dequeue_job(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """Dequeue job with highest priority"""
        try:
            if not self.client:
                return None

            queue_key = f"queue:{queue_name}"

            # Get highest priority job (lowest score)
            jobs = self.client.zrange(queue_key, 0, 0, withscores=True)

            if not jobs:
                return None

            job_data, score = jobs[0]

            # Remove from queue atomically
            if self.client.zrem(queue_key, job_data):
                return json.loads(job_data)

            return None

        except Exception as e:
            logger.error(f"Failed to dequeue job from {queue_name}: {e}")
            return None

    def get_queue_size(self, queue_name: str) -> int:
        """Get queue size"""
        try:
            if not self.client:
                return 0

            queue_key = f"queue:{queue_name}"
            return self.client.zcard(queue_key)

        except Exception as e:
            logger.error(f"Failed to get queue size for {queue_name}: {e}")
            return 0

    # Analytics and metrics
    def increment_counter(self, key: str, amount: int = 1, ttl: Optional[int] = None) -> int:
        """Increment counter"""
        try:
            if not self.client:
                return 0

            result = self.client.incr(key, amount)

            if ttl and result == amount:  # First time setting
                self.client.expire(key, ttl)

            return result

        except Exception as e:
            logger.error(f"Failed to increment counter {key}: {e}")
            return 0

    def get_counter(self, key: str) -> int:
        """Get counter value"""
        try:
            if not self.client:
                return 0

            value = self.client.get(key)
            return int(value) if value else 0

        except Exception as e:
            logger.error(f"Failed to get counter {key}: {e}")
            return 0


# Global Redis client instance
redis_client = RedisClient()


# Dependency for FastAPI
def get_redis() -> RedisClient:
    """Dependency to get Redis client"""
    return redis_client


# Background job management
class BackgroundJobManager:
    """Manager for background jobs using Redis"""

    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client

    async def enqueue_email_job(
        self,
        email_type: str,
        recipient: str,
        data: Dict[str, Any],
        priority: int = 0
    ) -> bool:
        """Enqueue email sending job"""
        job_data = {
            "type": "email",
            "email_type": email_type,
            "recipient": recipient,
            "data": data
        }

        return self.redis.enqueue_job("email", job_data, priority)

    async def enqueue_analytics_job(
        self,
        event_type: str,
        user_id: str,
        event_data: Dict[str, Any]
    ) -> bool:
        """Enqueue analytics processing job"""
        job_data = {
            "type": "analytics",
            "event_type": event_type,
            "user_id": user_id,
            "event_data": event_data,
            "timestamp": int(time.time())
        }

        return self.redis.enqueue_job("analytics", job_data)

    async def enqueue_user_progress_job(
        self,
        user_id: str,
        action: str,
        data: Dict[str, Any]
    ) -> bool:
        """Enqueue user progress update job"""
        job_data = {
            "type": "user_progress",
            "user_id": user_id,
            "action": action,
            "data": data
        }

        return self.redis.enqueue_job("user_progress", job_data)


# Global job manager instance
job_manager = BackgroundJobManager(redis_client)


# Import time for timestamp operations
import time