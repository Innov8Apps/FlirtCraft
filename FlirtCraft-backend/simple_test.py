#!/usr/bin/env python3
"""
Simple test to verify database models work with Supabase
"""
import asyncio
import uuid
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

async def main():
    print("Testing database models with Supabase...")
    
    try:
        from app.database import get_async_db_context
        from app.models.user import User
        from sqlalchemy import select, text
        
        async with get_async_db_context() as session:
            # Test database connection
            result = await session.execute(text("SELECT NOW() as current_time"))
            current_time = result.fetchone()[0]
            print(f"SUCCESS: Database connection works! Current time: {current_time}")
            
            # Test creating a user
            new_user = User(
                email="test@flirtcraft.com",
                age=25,
                supabase_user_id="test_user_123",
                premium_tier="free",
                is_active=True,
                email_verified=False,
                onboarding_completed=False
            )
            
            session.add(new_user)
            await session.flush()  # Get the ID
            
            print(f"SUCCESS: User created with ID: {new_user.id}")
            print(f"  Email: {new_user.email}")
            print(f"  Age: {new_user.age}")
            print(f"  Premium Tier: {new_user.premium_tier}")
            
            # Test querying the user
            stmt = select(User).where(User.email == "test@flirtcraft.com")
            result = await session.execute(stmt)
            fetched_user = result.scalar_one_or_none()
            
            if fetched_user:
                print(f"SUCCESS: User queried successfully!")
                print(f"  Found user: {fetched_user.email} (ID: {fetched_user.id})")
            else:
                print("ERROR: Could not query the created user")
                
            # Clean up - delete test user
            await session.delete(fetched_user)
            print("SUCCESS: Test user cleaned up")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    print("SUCCESS: All database tests passed!")
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)