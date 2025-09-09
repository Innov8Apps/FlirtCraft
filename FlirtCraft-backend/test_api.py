#!/usr/bin/env python3
"""
Test API endpoints with Supabase
"""
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

async def test_user_creation():
    """Test creating a user through the API"""
    try:
        from app.database import get_async_db_context
        from app.services.user_service import create_user
        from app.models.user import UserCreate
        
        # Test data
        user_data = UserCreate(
            email="test@example.com",
            age=25,
            supabase_user_id="test_123",
            premium_tier="free"
        )
        
        async with get_async_db_context() as session:
            user = await create_user(session, user_data)
            print(f"✓ User created successfully!")
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Age: {user.age}")
            print(f"  Premium Tier: {user.premium_tier}")
            return user.id
            
    except Exception as e:
        print(f"✗ User creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_onboarding_session():
    """Test creating an onboarding session"""
    try:
        from app.database import get_async_db_context
        from app.services.onboarding_service import start_onboarding_session
        
        # First create a user
        user_id = await test_user_creation()
        if not user_id:
            return
            
        async with get_async_db_context() as session:
            session_data = await start_onboarding_session(session, user_id)
            print(f"✓ Onboarding session created!")
            print(f"  Session Token: {session_data.session_token}")
            print(f"  Current Step: {session_data.current_step}")
            print(f"  Total Steps: {session_data.total_steps}")
            
    except Exception as e:
        print(f"✗ Onboarding session failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    print("Testing API functionality with Supabase...")
    
    # Test user creation
    await test_user_creation()
    
    # Test onboarding session
    await test_onboarding_session()
    
    print("✓ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())