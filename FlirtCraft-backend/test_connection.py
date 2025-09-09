#!/usr/bin/env python3
"""
Test script for Supabase database connection
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def main():
    print("Testing Supabase database connection...")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'not set')}")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'not set')[:50]}...")
    print(f"ASYNC_DATABASE_URL: {os.getenv('ASYNC_DATABASE_URL', 'not set')[:50]}...")
    
    try:
        # Import after loading env vars
        from app.database import check_async_database_connection, get_database_health
        
        # Test async connection
        connection_result = await check_async_database_connection()
        print(f"Async database connection: {'SUCCESS' if connection_result else 'FAILED'}")
        
        # Get health info
        health = await get_database_health()
        print(f"Database health: {health}")
        
    except Exception as e:
        print(f"Error testing connection: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())