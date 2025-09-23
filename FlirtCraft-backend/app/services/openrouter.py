"""
OpenRouter AI integration service for FlirtCraft Backend
Handles AI conversation generation and context creation
"""

import httpx
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..core.config import settings

logger = logging.getLogger(__name__)


class OpenRouterError(Exception):
    """Custom exception for OpenRouter API errors"""
    pass


class OpenRouterService:
    """Service for interacting with OpenRouter AI API"""

    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://flirtcraft.app",
            "X-Title": "FlirtCraft"
        }

    async def health_check(self) -> Dict[str, Any]:
        """Check OpenRouter API health"""
        try:
            if not self.api_key:
                return {
                    "status": "unhealthy",
                    "service": "openrouter",
                    "connected": False,
                    "error": "API key not configured"
                }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers,
                    timeout=10.0
                )

            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "service": "openrouter",
                    "connected": True,
                    "models_available": len(response.json().get("data", []))
                }
            else:
                return {
                    "status": "unhealthy",
                    "service": "openrouter",
                    "connected": False,
                    "error": f"HTTP {response.status_code}"
                }

        except Exception as e:
            logger.error(f"OpenRouter health check failed: {e}")
            return {
                "status": "unhealthy",
                "service": "openrouter",
                "connected": False,
                "error": str(e)
            }

    async def generate_conversation_character(
        self,
        scenario_type: str,
        difficulty_level: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI character context for conversation scenarios
        """
        try:
            # Build prompt for character generation
            prompt = self._build_character_prompt(scenario_type, difficulty_level, user_preferences)

            # Call OpenRouter API
            response_data = await self._call_openrouter(
                prompt=prompt,
                model="anthropic/claude-3-haiku",
                max_tokens=800,
                temperature=0.7
            )

            # Parse and structure the response
            character_data = self._parse_character_response(response_data, scenario_type, difficulty_level)

            return {
                "success": True,
                "character": character_data,
                "meta": {
                    "scenario_type": scenario_type,
                    "difficulty_level": difficulty_level,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Character generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback": self._get_fallback_character(scenario_type, difficulty_level)
            }

    async def generate_ai_response(
        self,
        conversation_context: Dict[str, Any],
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate AI response to user message in conversation
        """
        try:
            # Build conversation prompt
            prompt = self._build_conversation_prompt(
                conversation_context,
                user_message,
                conversation_history
            )

            # Call OpenRouter API
            response_data = await self._call_openrouter(
                prompt=prompt,
                model="anthropic/claude-3-haiku",
                max_tokens=300,
                temperature=0.8
            )

            # Parse response for conversation elements
            ai_response = self._parse_conversation_response(response_data, conversation_context)

            return {
                "success": True,
                "response": ai_response,
                "meta": {
                    "model_used": "anthropic/claude-3-haiku",
                    "generated_at": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"AI response generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback": self._get_fallback_response(user_message, conversation_context)
            }

    async def generate_feedback(
        self,
        conversation_history: List[Dict[str, str]],
        user_goals: List[str],
        scenario_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized feedback for conversation performance
        """
        try:
            # Build feedback prompt
            prompt = self._build_feedback_prompt(conversation_history, user_goals, scenario_context)

            # Call OpenRouter API
            response_data = await self._call_openrouter(
                prompt=prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=1000,
                temperature=0.3
            )

            # Parse feedback response
            feedback_data = self._parse_feedback_response(response_data, user_goals)

            return {
                "success": True,
                "feedback": feedback_data,
                "meta": {
                    "conversation_length": len(conversation_history),
                    "user_goals": user_goals,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Feedback generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback": self._get_fallback_feedback(conversation_history)
            }

    async def _call_openrouter(
        self,
        prompt: str,
        model: str = "anthropic/claude-3-haiku",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Make API call to OpenRouter"""
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )

            if response.status_code != 200:
                raise OpenRouterError(f"API call failed: {response.status_code} - {response.text}")

            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"OpenRouter API call failed: {e}")
            raise OpenRouterError(f"Failed to call OpenRouter API: {e}")

    def _build_character_prompt(
        self,
        scenario_type: str,
        difficulty_level: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build prompt for character generation"""

        scenario_descriptions = {
            "coffee_shop": "a cozy coffee shop with soft background music",
            "bookstore": "a quiet bookstore with tall shelves and reading nooks",
            "park": "a sunny park with walking paths and outdoor activities",
            "campus": "a university campus with students and academic atmosphere",
            "grocery": "a grocery store during a casual shopping trip",
            "gym": "a fitness center with workout equipment and active atmosphere",
            "bar": "a social bar or pub with lively conversation",
            "gallery": "an art gallery or cultural event with sophisticated atmosphere"
        }

        difficulty_descriptions = {
            "green": "very approachable and clearly interested in conversation",
            "yellow": "polite but neutral, requiring some effort to engage",
            "red": "busy or distracted, requiring skillful and respectful approach"
        }

        scenario_desc = scenario_descriptions.get(scenario_type, "a social setting")
        difficulty_desc = difficulty_descriptions.get(difficulty_level, "moderately approachable")

        # Build gender preference if available
        gender_text = ""
        if user_preferences and user_preferences.get("target_gender"):
            gender = user_preferences["target_gender"]
            if gender == "male":
                gender_text = "Create a male character."
            elif gender == "female":
                gender_text = "Create a female character."

        prompt = f"""You are creating a realistic character for a conversation practice scenario in {scenario_desc}. The character should be {difficulty_desc}.

{gender_text}

Please provide:
1. Physical appearance (age, style, what they're wearing/doing)
2. Body language that matches the {difficulty_level} difficulty level
3. Current activity or what they're focused on
4. Personality traits that would influence how they respond to approaches
5. Potential conversation topics they might be interested in

Keep the description natural and realistic. The character should feel like a real person someone might encounter in this setting.

Format your response as a JSON object with these keys:
- "appearance": Physical description
- "body_language": Current body language and demeanor
- "current_activity": What they're doing right now
- "personality_traits": List of 3-4 key personality traits
- "conversation_interests": List of topics they'd be interested in discussing
- "approach_style": How they typically respond to people approaching them
"""

        return prompt

    def _build_conversation_prompt(
        self,
        conversation_context: Dict[str, Any],
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Build prompt for AI conversation response"""

        # Extract character details
        character = conversation_context.get("character", {})
        scenario = conversation_context.get("scenario_type", "coffee_shop")
        difficulty = conversation_context.get("difficulty_level", "green")

        # Build conversation history text
        history_text = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = "User" if msg["sender"] == "user" else "AI"
                history_text += f"{role}: {msg['content']}\n"

        prompt = f"""You are roleplaying as a character in a {scenario} scenario. Here are your character details:

Character: {character.get('appearance', 'A person in their twenties')}
Body Language: {character.get('body_language', 'Relaxed and approachable')}
Current Activity: {character.get('current_activity', 'Enjoying their time here')}
Personality: {', '.join(character.get('personality_traits', ['Friendly', 'Conversational']))}
Interests: {', '.join(character.get('conversation_interests', ['General topics']))}

Difficulty Level: {difficulty} (this affects how receptive you are to conversation)

Previous conversation:
{history_text}

The user just said: "{user_message}"

Respond as this character would, staying true to their personality and the difficulty level. Your response should:
1. Be natural and realistic for this scenario
2. Match your character's personality and current mood
3. Reflect the appropriate level of interest based on difficulty
4. Include subtle body language cues in [brackets] if relevant
5. Keep responses conversational and not too long (1-3 sentences typically)

Response:"""

        return prompt

    def _build_feedback_prompt(
        self,
        conversation_history: List[Dict[str, str]],
        user_goals: List[str],
        scenario_context: Dict[str, Any]
    ) -> str:
        """Build prompt for feedback generation"""

        # Convert conversation history to text
        conversation_text = ""
        for msg in conversation_history:
            role = "User" if msg["sender"] == "user" else "AI Partner"
            conversation_text += f"{role}: {msg['content']}\n"

        goals_text = ", ".join(user_goals) if user_goals else "general conversation skills"
        scenario = scenario_context.get("scenario_type", "social setting")

        prompt = f"""You are a conversation coach providing feedback on a practice conversation.

Scenario: {scenario}
User's Goals: {goals_text}

Conversation:
{conversation_text}

Please provide detailed feedback in JSON format with these categories:

{{
  "overall_score": (1-100 integer score),
  "strengths": ["strength1", "strength2", "strength3"],
  "areas_for_improvement": ["area1", "area2", "area3"],
  "specific_suggestions": [
    {{"message": "specific user message", "feedback": "how to improve it"}},
    {{"message": "another message", "feedback": "improvement suggestion"}}
  ],
  "conversation_flow_score": (1-100),
  "confidence_level_score": (1-100),
  "engagement_score": (1-100),
  "next_practice_focus": "main area to work on next",
  "encouragement": "positive encouragement message"
}}

Focus on constructive feedback that helps the user improve their conversation skills."""

        return prompt

    def _parse_character_response(self, response: str, scenario_type: str, difficulty_level: str) -> Dict[str, Any]:
        """Parse and structure character generation response"""
        try:
            # Try to parse as JSON first
            character_data = json.loads(response)
            return character_data
        except json.JSONDecodeError:
            # Fall back to text parsing
            return {
                "appearance": "An attractive person in their twenties with a friendly demeanor",
                "body_language": f"{'Open and welcoming' if difficulty_level == 'green' else 'Neutral and focused' if difficulty_level == 'yellow' else 'Busy and distracted'}",
                "current_activity": f"Enjoying their time in this {scenario_type.replace('_', ' ')}",
                "personality_traits": ["Friendly", "Conversational", "Interesting"],
                "conversation_interests": ["Current events", "Hobbies", "Local area"],
                "approach_style": "Responds positively to genuine, friendly conversation"
            }

    def _parse_conversation_response(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI conversation response"""
        # Extract body language cues if present
        body_language = ""
        content = response

        # Look for body language in [brackets]
        import re
        body_language_match = re.search(r'\[(.*?)\]', response)
        if body_language_match:
            body_language = body_language_match.group(1)
            content = re.sub(r'\[.*?\]', '', response).strip()

        return {
            "content": content,
            "body_language": body_language,
            "receptiveness": self._assess_receptiveness(content, context.get("difficulty_level", "green")),
            "response_type": "conversational"
        }

    def _parse_feedback_response(self, response: str, user_goals: List[str]) -> Dict[str, Any]:
        """Parse feedback generation response"""
        try:
            feedback_data = json.loads(response)
            return feedback_data
        except json.JSONDecodeError:
            # Fallback feedback structure
            return {
                "overall_score": 75,
                "strengths": ["Good conversation starter", "Friendly approach"],
                "areas_for_improvement": ["Flow between topics", "Asking follow-up questions"],
                "specific_suggestions": [],
                "conversation_flow_score": 70,
                "confidence_level_score": 75,
                "engagement_score": 80,
                "next_practice_focus": "Maintaining conversation flow",
                "encouragement": "Great job practicing! Keep working on these areas and you'll see improvement."
            }

    def _assess_receptiveness(self, content: str, difficulty_level: str) -> str:
        """Assess AI character's receptiveness level"""
        receptiveness_map = {
            "green": "highly receptive",
            "yellow": "moderately receptive",
            "red": "low receptiveness"
        }
        return receptiveness_map.get(difficulty_level, "moderately receptive")

    def _get_fallback_character(self, scenario_type: str, difficulty_level: str) -> Dict[str, Any]:
        """Get fallback character when AI generation fails"""
        return {
            "appearance": "An attractive person in their twenties with a welcoming presence",
            "body_language": "Relaxed and approachable" if difficulty_level == "green" else "Focused but polite",
            "current_activity": f"Enjoying their time in this {scenario_type.replace('_', ' ')}",
            "personality_traits": ["Friendly", "Interesting", "Conversational"],
            "conversation_interests": ["Travel", "Books", "Local area", "Current events"],
            "approach_style": "Responds well to genuine, respectful conversation"
        }

    def _get_fallback_response(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get fallback response when AI generation fails"""
        return {
            "content": "That's interesting! Tell me more about that.",
            "body_language": "maintains eye contact and leans in slightly",
            "receptiveness": "moderately receptive",
            "response_type": "conversational"
        }

    def _get_fallback_feedback(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Get fallback feedback when AI generation fails"""
        return {
            "overall_score": 75,
            "strengths": ["Good effort in practicing", "Maintaining conversation"],
            "areas_for_improvement": ["Continue practicing", "Work on conversation flow"],
            "specific_suggestions": [],
            "conversation_flow_score": 70,
            "confidence_level_score": 75,
            "engagement_score": 75,
            "next_practice_focus": "Keep practicing regularly",
            "encouragement": "You're doing great! Keep practicing to build your confidence."
        }


# Global service instance
openrouter_service = OpenRouterService()


# Dependency for FastAPI
def get_openrouter_service() -> OpenRouterService:
    """Dependency to get OpenRouter service"""
    return openrouter_service