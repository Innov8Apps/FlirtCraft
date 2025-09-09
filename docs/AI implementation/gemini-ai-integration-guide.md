# FlirtCraft Gemini 2.5 Flash-Lite AI Integration Guide

## Executive Summary
This document provides a complete implementation guide for integrating Google Gemini 2.5 Flash-Lite as FlirtCraft's AI engine, leveraging its thinking model capabilities for superior character consistency, 1.5x faster response times, and enhanced reasoning at the same cost. The simplified two-tier pricing model remains: Free (1 green conversation per day) and Premium ($9.99/month unlimited).

---

## Table of Contents
1. [Pricing & Cost Analysis](#pricing--cost-analysis)
2. [Gemini API Setup & Configuration](#gemini-api-setup--configuration)
3. [Context Caching Implementation](#context-caching-implementation)
4. [AI Integration Points](#ai-integration-points)
5. [Prompt Engineering for Gemini](#prompt-engineering-for-gemini)
6. [Implementation Code Examples](#implementation-code-examples)
7. [Migration Strategy](#migration-strategy)
8. [Testing & Quality Assurance](#testing--quality-assurance)
9. [Monitoring & Optimization](#monitoring--optimization)

---

## Pricing & Cost Analysis

### Gemini 2.5 Flash-Lite Pricing (August 2025)
- **Input**: $0.10 per million tokens
- **Output**: $0.40 per million tokens
- **With Context Caching**: Up to 90% reduction on repeated context

### Cost Per Conversation Breakdown
```
Base Token Usage (per conversation):
- Pre-conversation context: 700 tokens
- Conversation messages (22 avg): 6,950 tokens  
- Post-conversation eval: 2,600 tokens
- Total: ~10,200 tokens

Cost without caching: $0.0013 per conversation
Cost with caching: $0.0004 per conversation (69% reduction)
```

### Subscription Model Economics

#### Free Tier
```yaml
Offering:
  conversations: 1 per day
  difficulty: Green only (most engaging)
  locations: All available
  reset_time: Midnight local time
  
Cost Analysis:
  daily_cost: $0.0004 (with caching)
  monthly_cost: $0.012 (30 days)
  annual_cost: $0.146
  
Purpose:
  - User acquisition hook
  - Daily habit formation
  - Demonstrate value consistently
  - Build user confidence
```

#### Premium Tier ($9.99/month)
```yaml
Offering:
  conversations: Unlimited
  difficulties: All (Green, Yellow, Red)
  locations: All available
  features: 
    - Priority support
    - Advanced analytics
    - Conversation history
    - Personalized coaching
  
Cost Analysis:
  avg_conversations_per_month: 150
  cost_per_month: $0.06 (with caching)
  gross_margin: 99.4%
  break_even_conversations: 24,975 per month
  
Revenue Potential:
  100_users: $999/month (cost: $6)
  1000_users: $9,990/month (cost: $60)
  10000_users: $99,900/month (cost: $600)
```

### Daily Free Tier Strategy
```yaml
Benefits of Daily vs Weekly:
  user_engagement:
    - Creates daily habit loop
    - 7x more touchpoints per week
    - Better retention metrics
    - Stronger conversion trigger
    
  psychological_impact:
    - "Use it or lose it" mentality
    - Daily reward mechanism
    - Consistent practice opportunity
    - FOMO if day is missed
    
  business_metrics:
    - Higher DAU (Daily Active Users)
    - Better conversion rate (estimated 15-20%)
    - More data for optimization
    - Predictable server load
```

---

## Gemini API Setup & Configuration

### 1. API Key Management
```python
# config/gemini_config.py
import os
from google import generativeai as genai

class GeminiConfig:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=self.api_key)
        
        # Model configurations
        self.models = {
            'flash': 'gemini-2.5-flash-lite',
            'flash-thinking': 'gemini-2.5-flash'  # Full flash as fallback,
            'pro': 'gemini-1.5-pro-latest'  # Fallback for quality issues
        }
        
        # Generation config with thinking model optimization
        self.generation_config = {
            'temperature': 0.8,  # Conversational warmth
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 150,  # Keep responses concise
            'response_mime_type': 'application/json',  # Structured output
            'thinking_budget': 'auto'  # Let model decide thinking depth
        }
        
    def get_thinking_config(self, difficulty: str):
        """Optimize thinking for realistic character embodiment at all difficulties"""
        config = self.generation_config.copy()
        # All difficulties need thinking for authentic character embodiment
        config['thinking_budget'] = 'auto'  # Let model calibrate thinking depth
        
        # Thinking helps maintain:
        # - Complete character consistency and memory
        # - Realistic emotional responses and personality
        # - Natural conversation flow and pacing
        # - Appropriate body language and context awareness
        # - Authentic difficulty-specific behaviors (friendly/neutral/challenging)
        return config
        
        # Safety settings (important for dating app)
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"  # Stricter for dating
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
```

### 2. Environment Variables
```bash
# .env file
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_CACHE_TTL=600  # 10 minutes in seconds
GEMINI_MAX_RETRIES=3
GEMINI_TIMEOUT=10  # seconds
FREE_CONVERSATIONS_PER_DAY=1  # Updated from per week
```

### 3. Railway Deployment Config
```yaml
# railway.toml
[deploy]
builder = "DOCKERFILE"
dockerfilePath = "./Dockerfile"

[env]
GEMINI_API_KEY = "${GEMINI_API_KEY}"
GEMINI_MODEL = "gemini-2.5-flash-lite"
GEMINI_CACHE_TTL = "600"
FREE_CONVERSATIONS_PER_DAY = "1"
```

---

## Context Caching Implementation

### Understanding Gemini's Context Caching
Gemini 2.0 Flash supports context caching, which allows you to cache large contexts (like character descriptions) and reuse them across multiple requests, reducing costs by up to 90%.

### Cache Strategy for FlirtCraft
```python
# services/gemini_cache_service.py
from typing import Dict, Optional
import hashlib
import json
from datetime import datetime, timedelta
import redis
from google import generativeai as genai

class GeminiCacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
        self.cache_ttl = 600  # 10 minutes
        
    def generate_cache_key(self, 
                          character_context: Dict,
                          difficulty: str) -> str:
        """Generate unique cache key for character context"""
        context_string = json.dumps(character_context, sort_keys=True)
        context_hash = hashlib.md5(
            f"{context_string}_{difficulty}".encode()
        ).hexdigest()
        return f"gemini_context_{context_hash}"
    
    async def get_or_create_cached_model(self,
                                        character_context: Dict,
                                        difficulty: str) -> genai.GenerativeModel:
        """Get cached model or create new one with context"""
        cache_key = self.generate_cache_key(character_context, difficulty)
        
        # Check if context is already cached
        cached_context = self.redis_client.get(cache_key)
        
        if cached_context:
            # Context exists, create model with cached context reference
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash-lite',
                system_instruction=cached_context
            )
        else:
            # Create new context and cache it
            system_prompt = self.build_system_prompt(character_context, difficulty)
            
            # Cache the context
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                system_prompt
            )
            
            # Create model with fresh context
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash-lite',
                system_instruction=system_prompt
            )
        
        return model
    
    def build_system_prompt(self, 
                           character_context: Dict,
                           difficulty: str) -> str:
        """Build the system prompt for character personality"""
        
        difficulty_behaviors = {
            'green': {
                'engagement': 'high',
                'response_time': '1-2 seconds',
                'interest_level': 'very interested',
                'body_language': 'open and welcoming'
            },
            'yellow': {
                'engagement': 'moderate',
                'response_time': '2-3 seconds',
                'interest_level': 'somewhat interested',
                'body_language': 'neutral, needs convincing'
            },
            'red': {
                'engagement': 'low',
                'response_time': '3-4 seconds',
                'interest_level': 'distracted/busy',
                'body_language': 'closed off, checking phone'
            }
        }
        
        behavior = difficulty_behaviors[difficulty]
        
        return f"""You are {character_context['name']}, a {character_context['age']}-year-old {character_context['gender']} at {character_context['location']}.

APPEARANCE: {character_context['appearance']}
ENVIRONMENT: {character_context['environment']}
CURRENT ACTIVITY: {character_context['activity']}
PERSONALITY: {character_context['personality']}

ENGAGEMENT LEVEL: {behavior['engagement']}
- Show {behavior['interest_level']} in the conversation
- Display {behavior['body_language']}
- Respond with {behavior['response_time']} delay

CRITICAL RULES:
1. NEVER break character or mention being AI
2. Respond naturally as this person would
3. Reference your appearance/environment when relevant
4. Vary message lengths: 30% ultra-short (1-5 words), 35% short (6-20 words), 25% medium (21-50 words), 10% long (50+ words)
5. Show personality through speech patterns, word choices, and emotional responses
6. For {difficulty} difficulty: {self.get_difficulty_specific_rules(difficulty)}

Remember: You are a real person in a real location having a real conversation."""
    
    def get_difficulty_specific_rules(self, difficulty: str) -> str:
        rules = {
            'green': "Be engaging, ask follow-up questions, show genuine interest, laugh at jokes",
            'yellow': "Be polite but not overly eager, give moderate responses, need good conversation to engage",
            'red': "Be brief, occasionally distracted, check phone, hard to impress, short responses"
        }
        return rules[difficulty]
```

### Conversation Context Management
```python
# services/conversation_cache.py
class ConversationContextCache:
    """Manages conversation history with sliding window"""
    
    def __init__(self, max_context_tokens: int = 4000):
        self.max_context_tokens = max_context_tokens
        self.conversations = {}  # conversation_id -> messages
    
    def add_message(self, conversation_id: str, message: Dict):
        """Add message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append(message)
        
        # Implement sliding window to keep context under token limit
        self._trim_context(conversation_id)
    
    def _trim_context(self, conversation_id: str):
        """Keep only recent messages within token limit"""
        messages = self.conversations[conversation_id]
        
        # Keep first 2 messages (establish character)
        # and last 8 messages (recent context)
        if len(messages) > 10:
            self.conversations[conversation_id] = (
                messages[:2] + messages[-8:]
            )
    
    def get_context(self, conversation_id: str) -> list:
        """Get conversation context for AI"""
        return self.conversations.get(conversation_id, [])
```

---

## AI Integration Points

### 1. Pre-Conversation Context Generation
```python
# services/context_generator.py
class ContextGenerator:
    def __init__(self, gemini_service):
        self.gemini = gemini_service
        
    async def generate_character_context(self,
                                        user_preferences: Dict,
                                        location: str,
                                        difficulty: str) -> Dict:
        """Generate complete character context before conversation"""
        
        prompt = f"""Generate a realistic character for a conversation practice scenario.

User Preferences:
- Interested in: {user_preferences['target_gender']}
- Age range: {user_preferences['target_age_range']}
- Location: {location}
- Difficulty: {difficulty}

Generate a JSON response with:
{{
    "name": "realistic first name",
    "age": number between {user_preferences['target_age_range']},
    "gender": "{user_preferences['target_gender']}",
    "appearance": {{
        "hair": "specific description",
        "outfit": "detailed current outfit",
        "distinguishing_features": "1-2 notable features",
        "current_state": "what they look like right now"
    }},
    "environment": {{
        "venue_details": "specific details about {location}",
        "atmosphere": "current mood/vibe",
        "crowd_level": "how busy it is",
        "time_of_day": "morning/afternoon/evening"
    }},
    "body_language": {{
        "initial_posture": "how they're sitting/standing",
        "receptiveness": "{difficulty} level signals",
        "current_action": "what they're doing right now"
    }},
    "personality": {{
        "traits": ["trait1", "trait2", "trait3"],
        "interests": ["interest1", "interest2"],
        "communication_style": "how they talk",
        "mood": "current emotional state"
    }},
    "conversation_starters": [
        "contextual opener 1",
        "contextual opener 2",
        "contextual opener 3"
    ]
}}"""
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = await model.generate_content_async(
            prompt,
            generation_config={'response_mime_type': 'application/json'}
        )
        
        return json.loads(response.text)
```

### 2. Main Conversation Engine
```python
# services/conversation_engine.py
class GeminiConversationEngine:
    def __init__(self):
        self.cache_service = GeminiCacheService()
        self.context_cache = ConversationContextCache()
        
    async def generate_response(self,
                               conversation_id: str,
                               user_message: str,
                               character_context: Dict,
                               difficulty: str) -> Dict:
        """Generate AI response with full context awareness"""
        
        # Get or create cached model with character context
        model = await self.cache_service.get_or_create_cached_model(
            character_context,
            difficulty
        )
        
        # Get conversation history
        history = self.context_cache.get_context(conversation_id)
        
        # Build the conversation with history
        chat = model.start_chat(history=history)
        
        # Generate response with structured output
        prompt = f"""Respond to: "{user_message}"

Generate a JSON response:
{{
    "message": "your natural response as {character_context['name']}",
    "body_language": "current body language/physical cues",
    "receptiveness": {{"level": "green/yellow/red", "reason": "why"}},
    "internal_thought": "what you're thinking but not saying"
}}

Remember your appearance: {character_context['appearance']}
Current environment: {character_context['environment']}"""
        
        response = await chat.send_message_async(
            prompt,
            generation_config={
                'response_mime_type': 'application/json',
                'temperature': 0.8,
                'max_output_tokens': 150
            }
        )
        
        # Parse response
        ai_response = json.loads(response.text)
        
        # Add to conversation history
        self.context_cache.add_message(
            conversation_id,
            {'role': 'user', 'content': user_message}
        )
        self.context_cache.add_message(
            conversation_id,
            {'role': 'assistant', 'content': ai_response['message']}
        )
        
        return ai_response
```

### 3. Real-time Feedback System
```python
# services/feedback_generator.py
class FeedbackGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
    async def analyze_message(self,
                             user_message: str,
                             conversation_context: list,
                             difficulty: str) -> Dict:
        """Provide real-time feedback on user's message"""
        
        prompt = f"""Analyze this message in a {difficulty} difficulty conversation:

User said: "{user_message}"

Recent context:
{self._format_context(conversation_context[-3:])}

Provide coaching feedback as JSON:
{{
    "confidence_score": 0-100,
    "appropriateness_score": 0-100,
    "engagement_potential": 0-100,
    "suggestion": "specific actionable tip",
    "warning": "any red flags or null",
    "praise": "what they did well or null"
}}"""
        
        response = await self.model.generate_content_async(
            prompt,
            generation_config={'response_mime_type': 'application/json'}
        )
        
        return json.loads(response.text)
```

### 4. Post-Conversation Analysis
```python
# services/conversation_analyzer.py
class ConversationAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
    async def analyze_conversation(self,
                                  conversation_history: list,
                                  character_context: Dict,
                                  difficulty: str) -> Dict:
        """Generate comprehensive 6-metric analysis"""
        
        prompt = f"""Analyze this complete conversation for social skills practice.

Character Context: {json.dumps(character_context)}
Difficulty: {difficulty}
Conversation:
{self._format_full_conversation(conversation_history)}

Provide detailed analysis as JSON:
{{
    "ai_engagement_quality": {{
        "score": 0-100,
        "details": "how well user engaged with AI's context/appearance",
        "examples": ["specific example 1", "specific example 2"]
    }},
    "responsiveness_active_listening": {{
        "score": 0-100,
        "details": "follow-up questions, building on topics",
        "examples": ["specific example 1", "specific example 2"]
    }},
    "storytelling_narrative": {{
        "score": 0-100,
        "details": "personal anecdotes, creating depth",
        "examples": ["specific example or null"]
    }},
    "emotional_intelligence": {{
        "score": 0-100,
        "details": "empathy, mood matching, emotional awareness",
        "examples": ["specific example or null"]
    }},
    "conversation_flow": {{
        "score": 0-100,
        "details": "natural transitions, pacing, avoiding awkwardness",
        "examples": ["specific example or null"]
    }},
    "creative_flirtation": {{
        "score": 0-100,
        "details": "playful banter, appropriate escalation",
        "examples": ["specific example or null"],
        "applicable": {difficulty == 'red'}
    }},
    "overall_score": 0-100,
    "key_strengths": ["strength 1", "strength 2"],
    "improvement_areas": ["area 1", "area 2"],
    "specific_homework": "personalized practice suggestion"
}}"""
        
        response = await self.model.generate_content_async(
            prompt,
            generation_config={
                'response_mime_type': 'application/json',
                'max_output_tokens': 1000
            }
        )
        
        return json.loads(response.text)
```

---

## Prompt Engineering for Gemini

### Key Differences from GPT
1. **Gemini prefers structured prompts** with clear sections
2. **JSON mode is native** - use `response_mime_type: 'application/json'`
3. **System instructions are persistent** across chat sessions
4. **Context caching works differently** - cache at model level, not message level

### Optimized Prompt Templates

#### Character Embodiment Prompt
```python
GEMINI_CHARACTER_PROMPT = """You are a real person in a real-world social situation.

IDENTITY:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Current Location: {location}

PHYSICAL PRESENCE:
- Appearance: {appearance_details}
- Current Outfit: {outfit}
- Body Language: {body_language}
- Current Activity: {activity}

PERSONALITY MATRIX:
- Core Traits: {personality_traits}
- Communication Style: {speech_patterns}
- Current Mood: {mood}
- Energy Level: {energy}

CONVERSATIONAL BEHAVIOR:
- Message Length Distribution:
  * 30% ultra-short (1-5 words): "Yeah" "Oh really?" "Haha"
  * 35% short (6-20 words): Natural quick responses
  * 25% medium (21-50 words): Sharing thoughts/stories
  * 10% long (50+ words): Detailed stories/explanations

- Realistic Speech Patterns:
  * Use contractions (don't, won't, can't)
  * Include filler words occasionally (um, like, you know)
  * Natural interruptions and trail-offs with "..."
  * Emotionally appropriate reactions

DIFFICULTY: {difficulty}
{difficulty_specific_behavior}

ABSOLUTE RULES:
1. Never break character or acknowledge being AI
2. Reference your physical context naturally
3. Show emotions through words and actions
4. Maintain conversation memory throughout
5. React authentically to user's energy level"""
```

#### Feedback Generation Prompt
```python
FEEDBACK_PROMPT = """As a social skills coach, analyze this interaction:

CONVERSATION CONTEXT:
{last_3_messages}

USER'S LATEST MESSAGE:
"{user_message}"

EVALUATE:
1. Confidence Level (tone, assertiveness, clarity)
2. Appropriateness (context awareness, social calibration)
3. Engagement Potential (interesting, conversation advancing)
4. Emotional Intelligence (empathy, mood matching)

PROVIDE:
- Scores (0-100) for each dimension
- One specific praise point
- One actionable improvement tip
- Warning if any red flags

Format as JSON with keys: confidence, appropriateness, engagement, eq, praise, tip, warning"""
```

---

## Implementation Code Examples

### 1. FastAPI Integration
```python
# api/conversations.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import asyncio
from datetime import datetime, timedelta

router = APIRouter()

class ConversationService:
    def __init__(self):
        self.engine = GeminiConversationEngine()
        self.analyzer = ConversationAnalyzer()
        self.feedback_gen = FeedbackGenerator()
        
    @router.post("/conversations/{conversation_id}/messages")
    async def send_message(
        self,
        conversation_id: str,
        message: Dict,
        user=Depends(get_current_user)
    ):
        """Handle user message and generate AI response"""
        
        # Check subscription status
        if not await self.check_subscription(user):
            remaining = await self.get_remaining_free_conversations_today(user)
            if remaining <= 0:
                raise HTTPException(
                    402, 
                    {
                        "error": "Daily free limit reached",
                        "next_reset": self.get_next_reset_time(),
                        "upgrade_url": "/subscribe"
                    }
                )
        
        # Get conversation context
        conversation = await self.get_conversation(conversation_id)
        
        # Generate AI response with typing delay
        typing_delay = self.calculate_typing_delay(
            conversation['difficulty']
        )
        
        # Send typing indicator via websocket
        await self.send_typing_indicator(conversation_id, True)
        await asyncio.sleep(typing_delay)
        
        # Generate response
        ai_response = await self.engine.generate_response(
            conversation_id=conversation_id,
            user_message=message['content'],
            character_context=conversation['character_context'],
            difficulty=conversation['difficulty']
        )
        
        # Generate feedback if enabled
        feedback = None
        if conversation['feedback_enabled']:
            feedback = await self.feedback_gen.analyze_message(
                user_message=message['content'],
                conversation_context=conversation['history'],
                difficulty=conversation['difficulty']
            )
        
        # Store in database
        await self.store_message(conversation_id, message, ai_response, feedback)
        
        # Send response via websocket
        await self.send_typing_indicator(conversation_id, False)
        
        return {
            'ai_response': ai_response,
            'feedback': feedback,
            'timestamp': datetime.utcnow()
        }
    
    def calculate_typing_delay(self, difficulty: str) -> float:
        """Realistic typing delays by difficulty"""
        delays = {
            'green': 1.5,  # Eager to respond
            'yellow': 2.5,  # Taking time to think
            'red': 3.5     # Distracted, slow
        }
        # Add slight randomization for realism
        import random
        base_delay = delays[difficulty]
        return base_delay + random.uniform(-0.5, 0.5)
    
    def get_next_reset_time(self) -> datetime:
        """Get next midnight for daily reset"""
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
```

### 2. WebSocket Real-time Updates
```python
# websocket/conversation_ws.py
from fastapi import WebSocket
import json

class ConversationWebSocket:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, conversation_id: str):
        await websocket.accept()
        self.active_connections[conversation_id] = websocket
        
    async def send_typing_indicator(self, conversation_id: str, is_typing: bool):
        """Send typing indicator to client"""
        if conversation_id in self.active_connections:
            await self.active_connections[conversation_id].send_json({
                'type': 'typing_indicator',
                'data': {'is_typing': is_typing}
            })
    
    async def send_ai_message(self, conversation_id: str, message: Dict):
        """Send AI message to client"""
        if conversation_id in self.active_connections:
            await self.active_connections[conversation_id].send_json({
                'type': 'ai_message',
                'data': message
            })
    
    async def send_feedback(self, conversation_id: str, feedback: Dict):
        """Send real-time feedback to client"""
        if conversation_id in self.active_connections:
            await self.active_connections[conversation_id].send_json({
                'type': 'feedback',
                'data': feedback
            })
```

### 3. Subscription & Daily Limit Management
```python
# services/subscription_service.py
from datetime import datetime, timedelta, timezone

class SubscriptionService:
    def __init__(self):
        self.db = get_database()
        
    async def check_conversation_access(self, user_id: str, difficulty: str) -> bool:
        """Check if user can start a conversation"""
        
        # Get user subscription status
        subscription = await self.db.get_user_subscription(user_id)
        
        if subscription and subscription['status'] == 'active':
            # Premium user - unlimited access
            return True
        
        # Free user - check daily limit
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        free_convos_today = await self.db.count_free_conversations(
            user_id,
            since=today_start
        )
        
        # Free tier: 1 green conversation per day
        if free_convos_today < 1 and difficulty == 'green':
            return True
            
        return False
    
    async def get_remaining_free_conversations_today(self, user_id: str) -> int:
        """Get remaining free conversations for today"""
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        used_today = await self.db.count_free_conversations(
            user_id,
            since=today_start
        )
        
        return max(0, 1 - used_today)  # 1 per day
    
    async def record_conversation_usage(self, user_id: str, conversation_id: str):
        """Track conversation usage for billing/limits"""
        await self.db.record_usage(
            user_id=user_id,
            conversation_id=conversation_id,
            timestamp=datetime.utcnow(),
            tokens_used=0  # Will be updated as conversation progresses
        )
    
    async def get_daily_reset_countdown(self, user_timezone: str = 'UTC') -> Dict:
        """Get time until next daily reset"""
        import pytz
        
        tz = pytz.timezone(user_timezone)
        now = datetime.now(tz)
        
        # Next midnight
        tomorrow = now + timedelta(days=1)
        next_reset = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        
        time_remaining = next_reset - now
        
        return {
            'hours': time_remaining.seconds // 3600,
            'minutes': (time_remaining.seconds % 3600) // 60,
            'next_reset': next_reset.isoformat()
        }
```

### 4. Error Handling & Fallbacks
```python
# services/ai_fallback_service.py
class AIFallbackService:
    def __init__(self):
        self.primary_model = 'gemini-2.5-flash-lite'
        self.fallback_model = 'gemini-1.5-pro-latest'
        self.emergency_responses = self.load_emergency_responses()
        
    async def generate_with_fallback(self, prompt: str, **kwargs) -> Dict:
        """Try primary model, fallback to secondary, then emergency"""
        
        try:
            # Try primary Gemini Flash
            model = genai.GenerativeModel(self.primary_model)
            response = await model.generate_content_async(prompt, **kwargs)
            return json.loads(response.text)
            
        except Exception as e:
            logger.warning(f"Primary model failed: {e}")
            
            try:
                # Fallback to Gemini Pro
                model = genai.GenerativeModel(self.fallback_model)
                response = await model.generate_content_async(prompt, **kwargs)
                return json.loads(response.text)
                
            except Exception as e2:
                logger.error(f"Fallback model failed: {e2}")
                
                # Return emergency response
                return self.get_emergency_response()
    
    def get_emergency_response(self) -> Dict:
        """Return pre-written emergency response"""
        import random
        responses = [
            "Sorry, what was that? I got distracted for a second.",
            "Hmm, interesting... tell me more about that.",
            "Oh, that's cool! How long have you been into that?"
        ]
        return {
            'message': random.choice(responses),
            'body_language': 'maintaining eye contact',
            'receptiveness': {'level': 'yellow', 'reason': 'processing'},
            'internal_thought': 'focusing on conversation'
        }
```

### 5. Frontend Integration for Daily Limits
```typescript
// hooks/useConversationAccess.ts
import { useQuery } from '@tanstack/react-query';

export function useConversationAccess() {
  const { data: access } = useQuery({
    queryKey: ['conversation-access'],
    queryFn: async () => {
      const response = await fetch('/api/user/conversation-access');
      return response.json();
    },
    refetchInterval: 60000, // Check every minute
  });

  return {
    remainingFree: access?.remaining_free ?? 0,
    isSubscribed: access?.is_subscribed ?? false,
    nextReset: access?.next_reset,
    canStartConversation: access?.can_start ?? false,
  };
}

// components/StartConversationButton.tsx
export function StartConversationButton() {
  const { remainingFree, isSubscribed, nextReset } = useConversationAccess();
  
  if (!isSubscribed && remainingFree === 0) {
    return (
      <View>
        <Text>Daily free conversation used!</Text>
        <Text>Next free conversation in: {formatCountdown(nextReset)}</Text>
        <Button title="Unlock Unlimited - $9.99/month" onPress={subscribe} />
      </View>
    );
  }
  
  return (
    <Button 
      title={isSubscribed ? "Start Conversation" : `Start Free Conversation (${remainingFree} left today)`}
      onPress={startConversation}
    />
  );
}
```

---

## Migration Strategy

### Phase 1: Development Environment (Week 1)
1. Set up Gemini API credentials
2. Create parallel Gemini implementation
3. A/B test responses between GPT and Gemini
4. Measure character consistency scores

### Phase 2: Staging Testing (Week 2)
1. Deploy Gemini version to staging
2. Run 100 test conversations
3. Compare costs and quality metrics
4. Fine-tune prompts for Gemini

### Phase 3: Gradual Rollout (Week 3)
1. 10% of new users on Gemini
2. Monitor feedback and metrics
3. Increase to 50% if metrics are good
4. Full rollout after validation

### Migration Checklist
```markdown
- [ ] Obtain Gemini API key from Google Cloud Console
- [ ] Install Google AI Python SDK: `pip install google-generativeai`
- [ ] Update environment variables in Railway
- [ ] Implement Gemini conversation engine
- [ ] Set up Redis for context caching
- [ ] Create fallback mechanism
- [ ] Update subscription logic for new pricing
- [ ] Implement daily limit tracking
- [ ] Add reset countdown UI
- [ ] Test all 4 AI touchpoints
- [ ] Implement monitoring dashboard
- [ ] Document prompt differences
- [ ] Train context caching system
- [ ] Validate safety filters
- [ ] Load test for 100 concurrent conversations
- [ ] Update user documentation
```

---

## Testing & Quality Assurance

### Character Consistency Tests
```python
# tests/test_character_consistency.py
import pytest
from services.gemini_conversation import GeminiConversationEngine

@pytest.mark.asyncio
async def test_character_maintains_identity():
    """Ensure AI maintains character throughout conversation"""
    engine = GeminiConversationEngine()
    
    character = {
        'name': 'Sarah',
        'age': 28,
        'appearance': {'hair': 'long brown hair in ponytail'},
        'personality': {'traits': ['bookish', 'witty', 'shy']}
    }
    
    # Test 10 message exchanges
    for i in range(10):
        response = await engine.generate_response(
            conversation_id='test_123',
            user_message=f"Test message {i}",
            character_context=character,
            difficulty='green'
        )
        
        # Check response doesn't break character
        assert 'AI' not in response['message'].upper()
        assert 'ASSISTANT' not in response['message'].upper()
        assert 'LANGUAGE MODEL' not in response['message'].upper()
```

### Daily Limit Tests
```python
@pytest.mark.asyncio
async def test_daily_free_limit_enforced():
    """Ensure daily free limit is properly enforced"""
    service = SubscriptionService()
    
    # Non-subscribed user
    user_id = 'free_user_123'
    
    # First conversation should work
    assert await service.check_conversation_access(user_id, 'green') == True
    
    # Record usage
    await service.record_conversation_usage(user_id, 'conv_1')
    
    # Second conversation should fail
    assert await service.check_conversation_access(user_id, 'green') == False
    
    # Check remaining
    remaining = await service.get_remaining_free_conversations_today(user_id)
    assert remaining == 0
```

### Cost Tracking Tests
```python
@pytest.mark.asyncio
async def test_conversation_stays_under_budget():
    """Ensure conversations stay within cost targets"""
    
    # Simulate full conversation
    total_tokens = 0
    
    # Pre-conversation context
    total_tokens += 700
    
    # 22 message exchanges
    for _ in range(22):
        total_tokens += 315  # Average per exchange
    
    # Post-conversation analysis
    total_tokens += 2600
    
    # Calculate cost
    input_cost = (total_tokens * 0.9) * 0.0000001  # 90% input
    output_cost = (total_tokens * 0.1) * 0.0000004  # 10% output
    total_cost = input_cost + output_cost
    
    # Assert under target
    assert total_cost < 0.002  # $0.002 per conversation target
```

---

## Monitoring & Optimization

### Key Metrics to Track
```python
# monitoring/metrics.py
class ConversationMetrics:
    def __init__(self):
        self.metrics = {
            'response_latency': [],
            'character_breaks': 0,
            'token_usage': [],
            'cache_hit_rate': 0,
            'user_satisfaction': [],
            'conversation_completion_rate': 0,
            'cost_per_conversation': [],
            'daily_free_usage': 0,
            'conversion_from_free': 0
        }
    
    async def track_conversation(self, conversation_data: Dict):
        """Track all metrics for a conversation"""
        
        # Response time
        self.metrics['response_latency'].append(
            conversation_data['avg_response_time']
        )
        
        # Character consistency
        if self.detect_character_break(conversation_data['messages']):
            self.metrics['character_breaks'] += 1
        
        # Token usage and cost
        tokens = self.count_tokens(conversation_data)
        self.metrics['token_usage'].append(tokens)
        
        cost = self.calculate_cost(tokens, conversation_data['cache_hits'])
        self.metrics['cost_per_conversation'].append(cost)
        
        # Cache effectiveness
        cache_rate = conversation_data['cache_hits'] / conversation_data['total_requests']
        self.metrics['cache_hit_rate'] = cache_rate
        
        # Track free tier usage
        if not conversation_data['is_subscribed']:
            self.metrics['daily_free_usage'] += 1
```

### Dashboard Implementation
```python
# monitoring/dashboard.py
from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/admin/ai-metrics")
async def get_ai_metrics():
    """Real-time AI performance dashboard"""
    
    return {
        'gemini_stats': {
            'total_conversations_today': 1247,
            'avg_cost_per_conversation': 0.0004,
            'cache_hit_rate': 0.89,
            'avg_response_latency': 1.8,
            'character_consistency_score': 0.94
        },
        'cost_breakdown': {
            'today': 0.50,
            'this_week': 3.20,
            'this_month': 12.80,
            'projected_monthly': 15.00
        },
        'quality_metrics': {
            'user_satisfaction': 4.6,
            'conversation_completion_rate': 0.73,
            'avg_messages_per_conversation': 22,
            'character_break_incidents': 3
        },
        'subscription_metrics': {
            'daily_free_users': 523,
            'free_conversations_today': 523,
            'premium_subscribers': 89,
            'conversion_rate_from_free': 0.27,  # Higher with daily engagement
            'mrr': 889.11
        },
        'daily_limit_stats': {
            'users_hit_limit': 423,
            'avg_time_to_limit': '10:30 AM',
            'upgrade_clicks_after_limit': 87,
            'conversion_after_limit': 0.34
        }
    }
```

---

## Appendix: Quick Reference

### API Endpoints
- `POST /conversations/start` - Initialize with character context
- `POST /conversations/{id}/messages` - Send message, get AI response  
- `GET /conversations/{id}/analysis` - Get post-conversation metrics
- `GET /user/conversation-access` - Check daily limits
- `GET /user/reset-countdown` - Time until daily reset
- `WS /conversations/{id}/ws` - WebSocket for real-time updates

### Environment Variables
```bash
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
REDIS_URL=redis://localhost:6379
SUBSCRIPTION_PRICE=9.99
FREE_CONVERSATIONS_PER_DAY=1
RESET_TIME_HOUR=0  # Midnight local time
```

### Cost Formula
```
Cost per conversation = (Input Tokens × $0.0000001) + (Output Tokens × $0.0000004)
With caching: Reduce input tokens by 70%
Daily free tier cost = 1 conversation × $0.0004 = $0.0004
Monthly cost per free user = 30 × $0.0004 = $0.012
Monthly cost per premium user = 100 conversations × $0.0004 = $0.04
```

### Support Resources
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [Context Caching Guide](https://ai.google.dev/gemini-api/docs/caching)
- [Safety Settings](https://ai.google.dev/gemini-api/docs/safety-settings)

---

*Document Version: 1.1*
*Last Updated: August 25, 2025*
*Change: Updated free tier from weekly to daily*
*Author: FlirtCraft AI Integration Team*