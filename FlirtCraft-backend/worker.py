#!/usr/bin/env python3
"""
FlirtCraft RQ Worker for Background Tasks
=========================================
Handles background job processing for AI conversations, analytics, and notifications.
"""

import os
import sys
import redis
from rq import Worker, Queue, Connection

# Redis connection using environment variable
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_conn = redis.from_url(redis_url)

def main():
    """Start the RQ worker with multiple queues."""
    print("=" * 50)
    print("FlirtCraft RQ Worker Starting...")
    print(f"Redis URL: {redis_url}")
    print("Queues: default, high, low")
    print("=" * 50)
    
    try:
        with Connection(redis_conn):
            # Create worker with multiple priority queues
            worker = Worker(['high', 'default', 'low'], connection=redis_conn)
            
            print("RQ Worker started successfully!")
            print("Listening for jobs...")
            worker.work()
            
    except KeyboardInterrupt:
        print("\nShutting down worker gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting worker: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()