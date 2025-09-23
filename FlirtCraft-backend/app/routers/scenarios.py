"""
Scenario routes for FlirtCraft Backend
Conversation scenario management and context generation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging

from ..core.database import get_db
from ..core.auth import get_current_user, get_optional_user
from ..models.user import User, Scenario
from ..schemas.user import StandardResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.get("/", response_model=StandardResponse)
async def get_scenarios(
    include_premium: bool = False,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Get available conversation scenarios
    Filters based on user's premium status
    """
    try:
        # Query scenarios
        query = db.query(Scenario).filter(Scenario.is_active == True)

        # Filter by premium status
        if not include_premium or (current_user and not current_user.is_premium):
            query = query.filter(Scenario.is_premium == False)

        scenarios = query.all()

        # Convert to response format
        scenario_data = []
        for scenario in scenarios:
            scenario_info = {
                "type": scenario.type,
                "display_name": scenario.display_name,
                "description": scenario.description,
                "is_premium": scenario.is_premium,
                "is_active": scenario.is_active
            }
            scenario_data.append(scenario_info)

        # Add default scenarios if none exist in database
        if not scenario_data:
            scenario_data = get_default_scenarios()

        return StandardResponse(
            success=True,
            data=scenario_data,
            meta={
                "total_scenarios": len(scenario_data),
                "premium_user": current_user.is_premium if current_user else False,
                "includes_premium": include_premium
            }
        )

    except Exception as e:
        logger.error(f"Failed to get scenarios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scenarios"
        )


@router.get("/{scenario_type}", response_model=StandardResponse)
async def get_scenario_details(
    scenario_type: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific scenario
    """
    try:
        scenario = db.query(Scenario).filter(
            Scenario.type == scenario_type,
            Scenario.is_active == True
        ).first()

        if not scenario:
            # Fall back to default scenarios
            default_scenarios = {s["type"]: s for s in get_default_scenarios()}
            if scenario_type not in default_scenarios:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Scenario '{scenario_type}' not found"
                )
            scenario_data = default_scenarios[scenario_type]
        else:
            # Check premium access
            if scenario.is_premium and (not current_user or not current_user.is_premium):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Premium subscription required for this scenario"
                )

            scenario_data = {
                "type": scenario.type,
                "display_name": scenario.display_name,
                "description": scenario.description,
                "is_premium": scenario.is_premium,
                "is_active": scenario.is_active,
                "context_templates": scenario.context_templates,
                "difficulty_modifiers": scenario.difficulty_modifiers
            }

        return StandardResponse(
            success=True,
            data=scenario_data
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get scenario details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scenario details"
        )


@router.post("/{scenario_type}/context", response_model=StandardResponse)
async def generate_scenario_context(
    scenario_type: str,
    difficulty_level: str = "green",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate pre-conversation context for a scenario
    This would integrate with OpenRouter AI for context generation
    """
    try:
        # Validate difficulty level
        if difficulty_level not in ["green", "yellow", "red"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid difficulty level. Must be 'green', 'yellow', or 'red'"
            )

        # Get scenario
        scenario = db.query(Scenario).filter(
            Scenario.type == scenario_type,
            Scenario.is_active == True
        ).first()

        if not scenario:
            # Use default scenario
            default_scenarios = {s["type"]: s for s in get_default_scenarios()}
            if scenario_type not in default_scenarios:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Scenario '{scenario_type}' not found"
                )

        # Check premium access
        if scenario and scenario.is_premium and not current_user.is_premium:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Premium subscription required for this scenario"
            )

        # Get user profile for personalization
        from ..models.user import UserProfile
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

        # Generate context (this would use OpenRouter in production)
        context_data = generate_mock_context(scenario_type, difficulty_level, profile)

        return StandardResponse(
            success=True,
            data=context_data,
            meta={
                "scenario_type": scenario_type,
                "difficulty_level": difficulty_level,
                "personalized": profile is not None
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate context: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate scenario context"
        )


def get_default_scenarios() -> List[Dict[str, Any]]:
    """Get default scenarios based on architecture documentation"""
    return [
        {
            "type": "coffee_shop",
            "display_name": "Coffee Shops & Cafes",
            "description": "Practice in relaxed cafe environments with casual conversation starters",
            "is_premium": False,
            "is_active": True
        },
        {
            "type": "bookstore",
            "display_name": "Bookstores & Libraries",
            "description": "Quiet, intellectual spaces perfect for thoughtful conversations",
            "is_premium": False,
            "is_active": True
        },
        {
            "type": "park",
            "display_name": "Parks & Outdoor Spaces",
            "description": "Natural settings for casual encounters and relaxed conversations",
            "is_premium": False,
            "is_active": True
        },
        {
            "type": "campus",
            "display_name": "University Campus",
            "description": "Academic settings with peer interactions and study group scenarios",
            "is_premium": False,
            "is_active": True
        },
        {
            "type": "grocery",
            "display_name": "Grocery Stores & Daily Life",
            "description": "Everyday situations and natural conversation opportunities",
            "is_premium": False,
            "is_active": True
        },
        {
            "type": "gym",
            "display_name": "Gyms & Fitness Centers",
            "description": "Active environments with shared interests and fitness topics",
            "is_premium": True,
            "is_active": True
        },
        {
            "type": "bar",
            "display_name": "Bars & Social Venues",
            "description": "Lively social environments with music and group dynamics",
            "is_premium": True,
            "is_active": True
        },
        {
            "type": "gallery",
            "display_name": "Art Galleries & Cultural Events",
            "description": "Sophisticated cultural environments for meaningful conversations",
            "is_premium": True,
            "is_active": True
        }
    ]


def generate_mock_context(scenario_type: str, difficulty_level: str, user_profile=None) -> Dict[str, Any]:
    """
    Generate mock context for development
    In production, this would use OpenRouter AI integration
    """
    # Base context templates
    contexts = {
        "coffee_shop": {
            "environment": "A cozy coffee shop with soft jazz music and the aroma of freshly brewed coffee",
            "time_of_day": "mid-morning",
            "crowd_level": "moderately busy",
            "atmosphere": "relaxed and welcoming"
        },
        "bookstore": {
            "environment": "A quiet bookstore with tall shelves and reading nooks",
            "time_of_day": "afternoon",
            "crowd_level": "peaceful with few people",
            "atmosphere": "intellectual and calm"
        },
        "park": {
            "environment": "A sunny park with walking paths and people enjoying outdoor activities",
            "time_of_day": "late afternoon",
            "crowd_level": "active with joggers and families",
            "atmosphere": "energetic and natural"
        }
    }

    base_context = contexts.get(scenario_type, contexts["coffee_shop"])

    # Character appearance based on user preferences
    appearance = generate_character_appearance(user_profile)

    # Body language based on difficulty
    body_language = {
        "green": "Open posture, making eye contact, smiling occasionally, appears approachable",
        "yellow": "Neutral posture, occasionally checking phone, polite but not overly engaging",
        "red": "Focused on their activity, minimal eye contact, appears busy or distracted"
    }

    # Conversation starters based on scenario and difficulty
    conversation_starters = generate_conversation_starters(scenario_type, difficulty_level)

    return {
        "scenario_type": scenario_type,
        "difficulty_level": difficulty_level,
        "appearance": appearance,
        "environment": base_context,
        "body_language": body_language[difficulty_level],
        "conversation_starters": conversation_starters,
        "character_background": generate_character_background(scenario_type),
        "context_tips": generate_context_tips(scenario_type, difficulty_level)
    }


def generate_character_appearance(user_profile=None) -> str:
    """Generate character appearance based on user preferences"""
    # Default appearance
    appearance = "An attractive person in their mid-twenties with a friendly demeanor"

    if user_profile and user_profile.target_gender:
        gender_appearances = {
            "male": "A handsome man with a confident presence and casual style",
            "female": "A beautiful woman with an engaging smile and approachable energy",
            "everyone": "An attractive person with a warm and welcoming presence"
        }
        appearance = gender_appearances.get(user_profile.target_gender, appearance)

    return appearance


def generate_conversation_starters(scenario_type: str, difficulty_level: str) -> List[str]:
    """Generate appropriate conversation starters"""
    starters = {
        "coffee_shop": {
            "green": [
                "This coffee smells amazing, what did you order?",
                "I love this playlist, do you come here often?",
                "Mind if I ask what you're reading? It looks interesting."
            ],
            "yellow": [
                "Excuse me, do you know if they have good WiFi here?",
                "Sorry to bother you, is this seat taken?",
                "Have you tried their pastries? I'm trying to decide what to order."
            ],
            "red": [
                "Could you watch my laptop for a second while I get a refill?",
                "Do you know what time they close?",
                "Sorry, did you hear if they called out my order?"
            ]
        },
        "bookstore": {
            "green": [
                "I've been looking for a good book recommendation, what are you reading?",
                "This section has such great titles, are you finding anything interesting?",
                "I love this author too! Have you read their latest book?"
            ],
            "yellow": [
                "Excuse me, do you know where the science fiction section is?",
                "Have you been to any of the events they host here?",
                "Sorry, did you see if they have a café area?"
            ],
            "red": [
                "Do you know if they're open late tonight?",
                "Excuse me, where are the restrooms?",
                "Could you help me reach that book on the top shelf?"
            ]
        },
        "park": {
            "green": [
                "Beautiful day for a walk, isn't it?",
                "I love this trail, do you come here often to exercise?",
                "Your dog is adorable! What breed is it?"
            ],
            "yellow": [
                "Do you know how long this trail is?",
                "Have you seen the new playground they built?",
                "Is there a water fountain around here?"
            ],
            "red": [
                "Excuse me, which way is the parking lot?",
                "Do you know what time the park closes?",
                "Have you seen a small brown dog around here?"
            ]
        }
    }

    return starters.get(scenario_type, {}).get(difficulty_level, [
        "Hi there!",
        "How's your day going?",
        "Nice weather we're having!"
    ])


def generate_character_background(scenario_type: str) -> str:
    """Generate character background based on scenario"""
    backgrounds = {
        "coffee_shop": "A local who works nearby and enjoys this coffee shop's atmosphere for relaxing or working",
        "bookstore": "An avid reader who loves discovering new books and enjoys the quiet atmosphere",
        "park": "Someone who values outdoor activities and uses the park for exercise and relaxation"
    }

    return backgrounds.get(scenario_type, "A friendly person enjoying their time in this location")


def generate_context_tips(scenario_type: str, difficulty_level: str) -> List[str]:
    """Generate tips for approaching this scenario"""
    tips = {
        "green": [
            "They seem very approachable and interested in conversation",
            "Look for genuine connection points and shared interests",
            "Feel free to be yourself and let the conversation flow naturally"
        ],
        "yellow": [
            "They're polite but may need a good reason to engage longer",
            "Start with practical questions or observations about the environment",
            "Be patient and don't take neutral responses personally"
        ],
        "red": [
            "They appear busy or focused on something else",
            "Keep initial interactions brief and respectful",
            "Look for genuine opportunities to be helpful or add value"
        ]
    }

    return tips[difficulty_level]