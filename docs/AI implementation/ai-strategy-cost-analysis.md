# FlirtCraft AI Strategy & Cost Analysis Document

## 🚨 CRITICAL UPDATE - August 2025
**Major Update: Gemini 2.5 Flash-Lite chosen as optimal model - 1.5x faster performance with thinking model capabilities for superior character consistency at same cost as 2.0 Flash.**

## Executive Summary (Updated August 2025)
FlirtCraft requires AI for 4 critical touchpoints. After extensive analysis, **Google Gemini 2.5 Flash-Lite** is the optimal choice, offering 1.5x faster responses with advanced thinking capabilities, costing only **$0.0004 per conversation** with caching, enabling a highly profitable $9.99/month subscription with 99.6% gross margins.

### Why Gemini 2.5 Flash-Lite is Perfect for FlirtCraft:
- ✅ **$0.10/$0.40 per 1M tokens** (same price as 2.0 Flash)
- ✅ **Context caching** at $0.025 per 1M tokens (75% discount)
- ✅ **Thinking model** with adaptive reasoning for character consistency
- ✅ **1.5x faster** than Gemini 2.0 Flash  
- ✅ **1M token context window** with superior memory
- ✅ **Free tier**: 1,500 daily requests for testing
- ✅ **Native tools** and multimodal capabilities
- ✅ **Released July 2025** - Latest thinking model technology

---

## Table of Contents
1. [Complete AI Usage Map](#complete-ai-usage-map)
2. [Gemini 2.5 Flash Complete Integration Guide](#gemini-25-flash-complete-integration-guide)
3. [Cost Analysis & Optimization](#cost-analysis--optimization)
4. [Implementation Code & Best Practices](#implementation-code--best-practices)
5. [Prompt Engineering for Character Consistency](#prompt-engineering-for-character-consistency)
6. [Caching & Performance Optimization](#caching--performance-optimization)
7. [Subscription Pricing Models](#subscription-pricing-models)
8. [Risk Mitigation & Fallback Strategies](#risk-mitigation--fallback-strategies)
9. [System Architecture Requirements](#system-architecture-requirements)
10. [Monitoring & Analytics](#monitoring--analytics)

---

## Complete AI Usage Map

### 1. Pre-Conversation Context Generation
**Purpose**: Generate realistic scenario details (appearance, environment, body language, conversation starters)  
**When**: Once before each conversation starts  
**Why AI Needed**: Must create unique, coherent personas that feel real

#### Token Breakdown:
```
Input:  400 tokens (user preferences + scenario parameters)
Output: 300 tokens (detailed JSON context)
Total:  700 tokens per generation
Cost:   $0.00004 (input) + $0.00012 (output) = $0.00016
```

### 2. Main Conversation Engine (CORE FEATURE)
**Purpose**: Generate human-like responses maintaining character consistency  
**When**: Every message exchange (avg 22 per conversation)  
**Why AI Needed**: CRITICAL - Must maintain context, personality, and natural flow

#### Token Breakdown Per Message:
```
First Message:
- System prompt: 750 tokens (cached after first use)
- Output: 25 tokens average
- Cost: $0.000075 (first) + $0.00001 (output) = $0.000085

Messages 2-22 (with implicit caching):
- Cached context: 75% discount
- Conversation history: 100 tokens
- Output: 25 tokens
- Cost per message: $0.000015
```

### 3. Real-Time Feedback (Optional)
**Purpose**: Provide tips during conversation  
**When**: Every 3-4 user messages  
**Token Cost**: 200 tokens × $0.00001 = $0.000002

### 4. Post-Conversation 6-Metric Evaluation
**Purpose**: Score performance with actionable feedback  
**When**: Once after conversation ends  
**Token Cost**: 2,600 tokens × $0.00014 = $0.00036

**Total Cost Per Conversation: $0.0004 with caching**

---

## Gemini 2.5 Flash-Lite Complete Integration Guide

### Quick Start Setup (< 2 minutes)

#### Step 1: Get API Key
1. Navigate to [Google AI Studio](https://ai.google.dev)
2. Click "Get API key" in the left sidebar
3. No credit card required for free tier (1,500 requests/day)

#### Step 2: Install SDK

**Python (3.9+)**:
```bash
pip install google-generativeai
```

**JavaScript/TypeScript (Node.js 18+)**:
```bash
npm install @google/genai
```

**React Native (Expo)**:
```bash
npx expo install @google/genai expo-secure-store
```

#### Step 3: Environment Setup
```bash
# .env file
GEMINI_API_KEY=your_api_key_here
# Alternative (GOOGLE_API_KEY takes precedence if both set)
GOOGLE_API_KEY=your_api_key_here
```

### Authentication Best Practices

```python
# Python Implementation
from google import genai
import os

# Secure key management
class GeminiClient:
    def __init__(self):
        # API key automatically picked up from environment
        self.client = genai.Client(
            api_key=os.getenv('GEMINI_API_KEY'),
            # Optional: Set custom timeout
            timeout=30
        )
```

```javascript
// JavaScript/TypeScript Implementation
import { GoogleGenAI } from "@google/genai";

class GeminiService {
    constructor() {
        // Use x-goog-api-key header (NOT URL params)
        this.ai = new GoogleGenAI({
            apiKey: process.env.GEMINI_API_KEY,
        });
        this.model = "gemini-2.5-flash";
    }
}
```

```typescript
// React Native with Expo SecureStore
import * as SecureStore from 'expo-secure-store';
import { GoogleGenAI } from "@google/genai";

class SecureGeminiClient {
    private ai: GoogleGenAI | null = null;
    
    async initialize() {
        const apiKey = await SecureStore.getItemAsync('GEMINI_API_KEY');
        if (!apiKey) throw new Error('API key not found');
        
        this.ai = new GoogleGenAI({ apiKey });
    }
}
```

---

## Cost Analysis & Optimization

### Pricing Breakdown (December 2025)

#### Gemini 2.5 Flash-Lite Pricing
```yaml
Standard Rates:
  input: $0.10 per million tokens
  output: $0.40 per million tokens
  
With Context Caching:
  cached_input: $0.025 per million tokens (75% discount)
  output: $0.40 per million tokens
  cache_storage: $1.00 per million tokens per hour
  
Free Tier:
  requests: 1,500 per day
  rate_limits: Lower than paid tier
  cost: $0 (free)
```

#### Cost Comparison with Competitors
```yaml
Gemini 2.5 Flash-Lite:
  per_conversation: $0.0004 (with caching)
  monthly_cost: $0.008 (20 conversations)
  
GPT-4o-mini:
  per_conversation: $0.0020
  monthly_cost: $0.040
  
Claude 3.5 Haiku:
  per_conversation: $0.0112
  monthly_cost: $0.224
  
Claude Sonnet 4:
  per_conversation: $0.019
  monthly_cost: $0.380
```

### Optimization Strategies

#### 1. Implicit Caching (75% Savings)
```python
# Gemini 2.5 Flash-Lite with context caching and thinking model
# Place common elements at the beginning for better cache hits

def optimize_prompt_for_caching(character_context, conversation_history):
    # Static context first (cached automatically)
    static_context = f"""
    SYSTEM: FlirtCraft Conversation Engine v2.0
    CHARACTER_PROFILE: {character_context['profile']}
    DIFFICULTY: {character_context['difficulty']}
    RULES: {get_standard_rules()}
    """
    
    # Dynamic context last (not cached)
    dynamic_context = f"""
    RECENT_HISTORY: {conversation_history[-5:]}
    USER_MESSAGE: {current_message}
    """
    
    return static_context + dynamic_context
```

#### 2. Batch Processing (50% Savings)
```python
# For non-real-time operations (analytics, evaluations)
from google import genai

async def batch_process_evaluations(conversations):
    batch_client = genai.BatchClient()
    
    # Submit batch job (50% cheaper)
    job = await batch_client.create_batch(
        model="gemini-2.5-flash",
        requests=[
            {
                "prompt": build_evaluation_prompt(conv),
                "max_tokens": 600
            }
            for conv in conversations
        ],
        # Accept 24-hour turnaround for 50% discount
        processing_time="batch"
    )
    
    return job.id
```

#### 3. Token Reduction Techniques
```python
# Compress prompts without losing quality
class PromptCompressor:
    def __init__(self):
        self.abbreviations = {
            "appearance": "app",
            "environment": "env",
            "personality": "pers",
            "difficulty": "diff",
            "conversation": "conv"
        }
    
    def compress_context(self, full_context):
        # Use structured format instead of verbose descriptions
        return {
            "char": f"{full_context['age']},{full_context['gender']},{full_context['style']}",
            "loc": f"{full_context['venue']},{full_context['time']},{full_context['crowd']}",
            "mood": full_context['body_language'][:20],  # Abbreviate
            "hist": self.compress_history(full_context['history'])
        }
```

---

## Implementation Code & Best Practices

### Complete FlirtCraft Conversation Engine

```python
# gemini_conversation_engine.py
from google import genai
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime

class FlirtCraftConversationEngine:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.5-flash-lite"
        self.conversation_cache = {}
        
    async def generate_pre_conversation_context(
        self,
        scenario_type: str,
        difficulty: str,
        user_preferences: Dict
    ) -> Dict:
        """Generate 4-category context before conversation."""
        
        prompt = f"""
        Generate realistic dating scenario context as JSON.
        
        SCENARIO: {scenario_type}
        DIFFICULTY: {difficulty} (green=friendly, yellow=neutral, red=challenging)
        USER_PREFS: Age {user_preferences['target_age_min']}-{user_preferences['target_age_max']}, 
                   Gender: {user_preferences['target_gender']}
        
        Return JSON with exactly these keys:
        {{
            "appearance": "Age, style, current activity (100 chars)",
            "environment": "Location details, atmosphere (100 chars)",
            "body_language": "Signals matching {difficulty} difficulty",
            "conversation_starters": ["starter1", "starter2", "starter3"]
        }}
        """
        
        response = await self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.8,
                "max_output_tokens": 300
            }
        )
        
        return json.loads(response.text)
    
    async def generate_conversation_response(
        self,
        conversation_id: str,
        character_context: Dict,
        message_history: List[Dict],
        user_message: str,
        difficulty: str
    ) -> Dict:
        """Generate character response maintaining consistency."""
        
        # Build system instruction for character consistency
        system_instruction = self._build_character_system_prompt(
            character_context, 
            difficulty
        )
        
        # Prepare conversation history
        messages = self._format_message_history(message_history)
        
        # Generate response with thinking mode for better consistency
        response = await self.client.models.generate_content(
            model=self.model,
            system_instruction=system_instruction,
            contents=messages + [{"role": "user", "parts": [user_message]}],
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 100,
                "response_mime_type": "application/json"
            }
        )
        
        # Parse response
        ai_response = json.loads(response.text)
        
        # Track token usage for cost monitoring
        self._track_token_usage(response.usage_metadata)
        
        return {
            "message": ai_response.get("message", ""),
            "body_language": ai_response.get("body_language", "neutral"),
            "typing_delay": self._calculate_typing_delay(ai_response["message"]),
            "should_continue": ai_response.get("continue", True)
        }
    
    def _build_character_system_prompt(self, context: Dict, difficulty: str) -> str:
        """Build comprehensive system prompt for character consistency."""
        
        difficulty_behaviors = {
            "green": "Friendly, asks questions, shows interest, positive body language",
            "yellow": "Polite but neutral, doesn't lead conversation, mixed signals",
            "red": "Reserved, busy, short responses, user must work to engage"
        }
        
        return f"""
        You are roleplaying a person in a dating scenario. NEVER break character.
        
        CHARACTER DETAILS:
        - Appearance: {context['appearance']}
        - Currently at: {context['environment']}
        - Body language: {context['body_language']}
        
        PERSONALITY RULES FOR {difficulty.upper()} DIFFICULTY:
        {difficulty_behaviors[difficulty]}
        
        RESPONSE REQUIREMENTS:
        1. Stay 100% in character - you ARE this person
        2. Vary message length naturally:
           - 30% ultra-short (1-5 words): "oh really?", "lol yeah"
           - 35% short (6-20 words): natural responses
           - 25% medium (21-50 words): when engaged
           - 10% long (50+ words): when excited/storytelling
        3. Include realistic texting patterns:
           - Use age-appropriate language
           - Natural fillers: "um", "like", "idk"
           - Occasional typos (1-2% of messages)
        4. Reference your context naturally:
           - Mention what you're doing
           - Reference the environment
           - React based on your mood
        
        ALWAYS respond as JSON:
        {{
            "message": "your response",
            "body_language": "current body language",
            "continue": true/false (based on engagement)
        }}
        """
    
    def _format_message_history(self, history: List[Dict]) -> List[Dict]:
        """Format message history for Gemini API with sliding window."""
        
        # Keep first 2 messages (establish character) + last 8 (recent context)
        if len(history) <= 10:
            formatted = history
        else:
            formatted = history[:2] + history[-8:]
        
        # Convert to Gemini format
        gemini_messages = []
        for msg in formatted:
            role = "user" if msg["sender"] == "user" else "model"
            gemini_messages.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        return gemini_messages
    
    def _calculate_typing_delay(self, message: str) -> float:
        """Calculate realistic typing delay based on message length."""
        base_delay = 1.0
        char_delay = 0.05
        return min(base_delay + (len(message) * char_delay), 4.0)
    
    def _track_token_usage(self, usage_metadata: Dict):
        """Track token usage for cost monitoring."""
        if usage_metadata:
            input_tokens = usage_metadata.get('prompt_token_count', 0)
            output_tokens = usage_metadata.get('candidates_token_count', 0)
            cached_tokens = usage_metadata.get('cached_content_token_count', 0)
            
            # Calculate cost
            input_cost = (input_tokens - cached_tokens) * 0.0000001
            cached_cost = cached_tokens * 0.000000025
            output_cost = output_tokens * 0.0000004
            total_cost = input_cost + cached_cost + output_cost
            
            # Log for monitoring
            print(f"Tokens - Input: {input_tokens}, Cached: {cached_tokens}, "
                  f"Output: {output_tokens}, Cost: ${total_cost:.6f}")
    
    async def generate_post_conversation_feedback(
        self,
        conversation_id: str,
        messages: List[Dict],
        difficulty: str
    ) -> Dict:
        """Generate 6-metric feedback evaluation."""
        
        prompt = f"""
        Analyze this conversation and provide detailed feedback.
        
        CONVERSATION:
        {json.dumps(messages[-20:])}  # Last 20 messages
        
        DIFFICULTY: {difficulty}
        
        Evaluate on these 6 metrics (0-100 score each):
        1. AI Engagement Quality - How well user used context clues
        2. Responsiveness - Active listening and follow-ups
        3. Storytelling - Personal anecdotes and depth
        4. Emotional Intelligence - Empathy and mood matching
        5. Conversation Flow - Natural transitions and pacing
        6. Creative Flirtation - Playful banter (only for 'red' difficulty)
        
        Return as JSON with scores and actionable feedback for each metric.
        """
        
        response = await self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.3,
                "max_output_tokens": 600
            }
        )
        
        return json.loads(response.text)


# FastAPI Integration
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
engine = FlirtCraftConversationEngine()

class ConversationRequest(BaseModel):
    scenario_type: str
    difficulty: str
    user_preferences: Dict

class MessageRequest(BaseModel):
    conversation_id: str
    message: str
    character_context: Dict
    message_history: List[Dict]
    difficulty: str

@app.post("/api/conversations/start")
async def start_conversation(request: ConversationRequest):
    try:
        context = await engine.generate_pre_conversation_context(
            request.scenario_type,
            request.difficulty,
            request.user_preferences
        )
        return {"success": True, "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conversations/message")
async def send_message(request: MessageRequest):
    try:
        response = await engine.generate_conversation_response(
            request.conversation_id,
            request.character_context,
            request.message_history,
            request.message,
            request.difficulty
        )
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### React Native Implementation

```typescript
// geminiService.ts
import { GoogleGenAI } from "@google/genai";
import * as SecureStore from 'expo-secure-store';
import NetInfo from '@react-native-community/netinfo';

export class GeminiConversationService {
    private ai: GoogleGenAI | null = null;
    private conversationCache = new Map<string, any>();
    private offlineQueue: any[] = [];
    
    async initialize() {
        const apiKey = await SecureStore.getItemAsync('GEMINI_API_KEY');
        if (!apiKey) throw new Error('Gemini API key not configured');
        
        this.ai = new GoogleGenAI({ apiKey });
    }
    
    async generateContext(
        scenario: string, 
        difficulty: string, 
        preferences: UserPreferences
    ): Promise<ConversationContext> {
        if (!this.ai) await this.initialize();
        
        const model = this.ai!.getGenerativeModel({ 
            model: "gemini-2.5-flash-lite",
            generationConfig: {
                responseMimeType: "application/json",
                temperature: 0.8,
                maxOutputTokens: 300
            }
        });
        
        const prompt = this.buildContextPrompt(scenario, difficulty, preferences);
        
        try {
            const result = await model.generateContent(prompt);
            const response = await result.response;
            return JSON.parse(response.text());
        } catch (error) {
            // Fallback to cached context if offline
            if (!await this.isOnline()) {
                return this.getCachedContext(scenario, difficulty);
            }
            throw error;
        }
    }
    
    async sendMessage(
        conversationId: string,
        message: string,
        context: ConversationContext,
        history: Message[]
    ): Promise<AIResponse> {
        if (!this.ai) await this.initialize();
        
        const model = this.ai!.getGenerativeModel({
            model: "gemini-2.5-flash-lite",
            systemInstruction: this.buildSystemPrompt(context, difficulty),
            generationConfig: {
                responseMimeType: "application/json",
                temperature: 0.7,
                maxOutputTokens: 100
            }
        });
        
        // Build chat history
        const chat = model.startChat({
            history: this.formatChatHistory(history),
        });
        
        try {
            const result = await chat.sendMessage(message);
            const response = await result.response;
            
            // Track usage for cost monitoring
            this.trackUsage(result.response.usageMetadata);
            
            return JSON.parse(response.text());
        } catch (error) {
            // Queue for later if offline
            if (!await this.isOnline()) {
                this.queueOfflineMessage(conversationId, message);
                return this.generateOfflineResponse();
            }
            throw error;
        }
    }
    
    private buildSystemPrompt(context: ConversationContext, difficulty: string): string {
        // System prompt for character consistency
        return `You are ${context.appearance}. You're at ${context.environment}.
                Current mood: ${context.body_language}. 
                Difficulty: ${difficulty} - be ${this.getDifficultyBehavior(difficulty)}.
                Respond naturally as this person would, never breaking character.
                Format: {"message": "...", "body_language": "...", "continue": true/false}`;
    }
    
    private getDifficultyBehavior(difficulty: string): string {
        const behaviors = {
            green: "friendly, curious, asks questions, positive",
            yellow: "polite but neutral, doesn't lead, mixed signals",
            red: "reserved, busy, short responses, challenging"
        };
        return behaviors[difficulty] || behaviors.yellow;
    }
    
    private async isOnline(): Promise<boolean> {
        const netInfo = await NetInfo.fetch();
        return netInfo.isConnected ?? false;
    }
    
    private trackUsage(metadata: any) {
        if (!metadata) return;
        
        const cost = this.calculateCost(
            metadata.promptTokenCount || 0,
            metadata.candidatesTokenCount || 0,
            metadata.cachedContentTokenCount || 0
        );
        
        // Send to analytics
        analytics.track('ai_usage', {
            input_tokens: metadata.promptTokenCount,
            output_tokens: metadata.candidatesTokenCount,
            cached_tokens: metadata.cachedContentTokenCount,
            cost: cost,
            model: 'gemini-2.5-flash'
        });
    }
    
    private calculateCost(input: number, output: number, cached: number): number {
        const INPUT_RATE = 0.0000001;  // $0.10 per 1M tokens
        const OUTPUT_RATE = 0.0000004; // $0.40 per 1M tokens
        const CACHED_RATE = 0.000000025; // $0.025 per 1M tokens
        
        return (input - cached) * INPUT_RATE + 
               cached * CACHED_RATE + 
               output * OUTPUT_RATE;
    }
}
```

---

## Prompt Engineering for Character Consistency

### Best Practices for Gemini 2.0 Flash

#### 1. System Instructions for Strong Character Definition
```python
def create_character_system_instruction(context: Dict, difficulty: str) -> str:
    """Create comprehensive system instruction for character consistency."""
    
    return f"""
    IMMUTABLE CHARACTER DEFINITION:
    You ARE {context['name']}, not an AI. Never say "I'm an AI" or break character.
    
    PHYSICAL PRESENCE:
    - Age: {context['age']} years old
    - Appearance: {context['appearance']}
    - Current activity: {context['activity']}
    - Location: {context['location']}
    
    PERSONALITY MATRIX:
    - Core traits: {context['personality_traits']}
    - Communication style: {get_style_for_age(context['age'])}
    - Interests: {context['interests']}
    - Energy level: {get_energy_for_difficulty(difficulty)}
    
    BEHAVIORAL RULES:
    1. Reference your physical context naturally
       - "This coffee is getting cold" (coffee shop)
       - "The music here is loud" (bar)
    2. Maintain consistent backstory
       - Remember details you've shared
       - Build on previous statements
    3. Show personality through language
       - Young (18-25): More casual, emojis, "like", "totally"
       - Adult (26-35): Balanced, occasional slang
       - Mature (35+): More formal, complete sentences
    
    CONVERSATION DYNAMICS FOR {difficulty.upper()}:
    {get_difficulty_specific_rules(difficulty)}
    """
```

#### 2. Few-Shot Examples for Consistency
```python
def add_few_shot_examples(prompt: str, difficulty: str) -> str:
    """Add examples to show desired response format and style."""
    
    examples = {
        "green": [
            {"user": "Hi there!", "ai": "Hey! 😊 How's your day going?"},
            {"user": "Pretty good, just grabbed coffee", "ai": "Nice! I'm actually sipping on a latte right now. You a coffee person or just needed the caffeine hit? haha"}
        ],
        "yellow": [
            {"user": "Hi there!", "ai": "Oh, hey. How's it going?"},
            {"user": "Pretty good, just grabbed coffee", "ai": "Cool. This place makes decent coffee."}
        ],
        "red": [
            {"user": "Hi there!", "ai": "Hi."},
            {"user": "Pretty good, just grabbed coffee", "ai": "Mm-hmm. *continues reading*"}
        ]
    }
    
    example_text = "\nEXAMPLES OF APPROPRIATE RESPONSES:\n"
    for ex in examples[difficulty]:
        example_text += f"User: {ex['user']}\nYou: {ex['ai']}\n"
    
    return prompt + example_text
```

#### 3. Hierarchical Prompt Structure (Gemini Strength)
```python
def build_hierarchical_prompt(context: Dict, history: List, current: str) -> str:
    """Gemini excels with hierarchical, structured prompts."""
    
    return f"""
    [LEVEL 1: CORE IDENTITY]
    Character: {context['character']}
    Location: {context['location']}
    Mood: {context['mood']}
    
    [LEVEL 2: CONVERSATION CONTEXT]
    Topic Flow: {analyze_topic_flow(history)}
    Emotional Arc: {analyze_emotional_arc(history)}
    Engagement Level: {calculate_engagement(history)}
    
    [LEVEL 3: CURRENT EXCHANGE]
    Last 3 messages: {history[-3:]}
    User just said: {current}
    
    [LEVEL 4: RESPONSE REQUIREMENTS]
    - Match established tone
    - Reference earlier topics if relevant
    - Vary response length naturally
    - Include subtle body language cues
    
    Generate response maintaining all levels of context.
    """
```

---

## Caching & Performance Optimization

### Gemini's Implicit Caching System

#### How It Works
```python
class GeminiCacheOptimizer:
    """Optimize for Gemini's automatic implicit caching."""
    
    def __init__(self):
        # Minimum tokens for caching
        self.MIN_CACHE_TOKENS = {
            "flash": 1024,  # 2.0 Flash minimum
            "pro": 4096     # 1.5 Pro minimum
        }
    
    def structure_for_caching(self, static_content: str, dynamic_content: str) -> str:
        """
        Place static content first for automatic caching.
        Gemini caches content that appears frequently at prompt beginning.
        """
        
        # Static content (automatically cached after first use)
        cached_section = f"""
        === STATIC CONTEXT (CACHED) ===
        System Version: FlirtCraft v2.0
        Character Profile: {static_content}
        Behavioral Rules: {self.get_standard_rules()}
        Response Format: {self.get_response_format()}
        """
        
        # Dynamic content (not cached)
        dynamic_section = f"""
        === DYNAMIC CONTEXT ===
        Recent Messages: {dynamic_content}
        Current Input: [USER_MESSAGE]
        """
        
        # Ensure we meet minimum token requirement
        if len(cached_section.split()) < 256:  # Rough token estimate
            cached_section += self.get_padding_content()
        
        return cached_section + dynamic_section
    
    def estimate_cache_savings(self, conversations_per_day: int) -> Dict:
        """Calculate cost savings from implicit caching."""
        
        base_tokens_per_conversation = 10000
        cached_tokens = 7500  # 75% typically cached
        
        # Without caching
        uncached_cost = base_tokens_per_conversation * 0.0000001 * conversations_per_day
        
        # With caching (75% discount on cached portions)
        cached_cost = (
            (base_tokens_per_conversation - cached_tokens) * 0.0000001 +
            cached_tokens * 0.000000025
        ) * conversations_per_day
        
        return {
            "daily_uncached_cost": uncached_cost,
            "daily_cached_cost": cached_cost,
            "daily_savings": uncached_cost - cached_cost,
            "savings_percentage": ((uncached_cost - cached_cost) / uncached_cost) * 100
        }
```

### Performance Monitoring

```python
class GeminiPerformanceMonitor:
    """Monitor and optimize Gemini API performance."""
    
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "token_usage": [],
            "cache_hits": [],
            "costs": []
        }
    
    async def track_request(self, func, *args, **kwargs):
        """Wrapper to track API performance."""
        
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            
            # Extract metrics
            response_time = time.time() - start_time
            usage = result.usage_metadata
            
            # Track cache efficiency
            cache_rate = 0
            if usage:
                total_input = usage.prompt_token_count
                cached = usage.cached_content_token_count
                cache_rate = (cached / total_input * 100) if total_input > 0 else 0
            
            # Store metrics
            self.metrics["response_times"].append(response_time)
            self.metrics["cache_hits"].append(cache_rate)
            
            # Alert if performance degrades
            if response_time > 3.0:
                await self.alert_slow_response(response_time)
            
            if cache_rate < 50:
                await self.alert_low_cache_rate(cache_rate)
            
            return result
            
        except Exception as e:
            await self.alert_api_error(str(e))
            raise
    
    def get_performance_summary(self) -> Dict:
        """Get performance metrics summary."""
        
        return {
            "avg_response_time": np.mean(self.metrics["response_times"]),
            "p95_response_time": np.percentile(self.metrics["response_times"], 95),
            "avg_cache_rate": np.mean(self.metrics["cache_hits"]),
            "total_cost": sum(self.metrics["costs"]),
            "requests_count": len(self.metrics["response_times"])
        }
```

---

## Subscription Pricing Models

### Optimized for Gemini 2.0 Flash Costs

```yaml
Free Tier:
  daily_conversations: 1 (green difficulty only)
  limitations:
    - Green difficulty only
    - Basic feedback
    - No conversation history
    - Resets daily at midnight
  cost_to_company: $0.0004/day = $0.012/month
  purpose: User acquisition & habit formation

Premium - $9.99/month:
  conversations: Unlimited
  avg_usage: 100-200/month (estimated)
  features:
    - All difficulties (Green, Yellow, Red)
    - Advanced analytics & feedback
    - Full conversation history
    - Achievement system
    - Priority support
    - Future voice/image features
  cost_to_company: $0.04-$0.08/month
  gross_margin: 99.2-99.6%
  break_even_users: 10
```

### Unit Economics with Gemini

```python
def calculate_unit_economics(tier: str, users: int) -> Dict:
    """Calculate economics for each tier with Gemini costs."""
    
    tiers = {
        "free": {
            "price": 0,
            "conversations": 30,  # 1 per day for 30 days
            "cost_per_conv": 0.0004
        },
        "premium": {
            "price": 9.99,
            "conversations": 150,  # Average estimated usage
            "cost_per_conv": 0.0004
        }
    }
    
    tier_data = tiers[tier]
    
    # Revenue
    monthly_revenue = tier_data["price"] * users
    annual_revenue = monthly_revenue * 12
    
    # Costs
    ai_cost_per_user = tier_data["conversations"] * tier_data["cost_per_conv"]
    total_ai_cost = ai_cost_per_user * users
    
    # Infrastructure (estimated)
    infra_cost = users * 0.05  # $0.05 per user for servers/storage
    
    # Total costs
    total_costs = total_ai_cost + infra_cost
    
    # Profit
    gross_profit = monthly_revenue - total_costs
    gross_margin = (gross_profit / monthly_revenue) * 100
    
    return {
        "monthly_revenue": monthly_revenue,
        "annual_revenue": annual_revenue,
        "ai_costs": total_ai_cost,
        "infra_costs": infra_cost,
        "total_costs": total_costs,
        "gross_profit": gross_profit,
        "gross_margin": gross_margin,
        "cost_per_user": total_costs / users,
        "ltv_6_months": tier_data["price"] * 6,
        "cac_threshold": tier_data["price"] * 2  # Can spend 2 months revenue on acquisition
    }
```

---

## Risk Mitigation & Fallback Strategies

### Multi-Provider Fallback System

```python
class AIProviderFallbackSystem:
    """Fallback system for high availability."""
    
    def __init__(self):
        self.providers = [
            {
                "name": "gemini",
                "client": GeminiClient(),
                "priority": 1,
                "cost_per_token": 0.0000001
            },
            {
                "name": "gpt-4-mini",
                "client": OpenAIClient(),
                "priority": 2,
                "cost_per_token": 0.00000015
            },
            {
                "name": "groq-mixtral",
                "client": GroqClient(),
                "priority": 3,
                "cost_per_token": 0.00000027
            }
        ]
        self.health_status = {}
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict:
        """Try providers in order of priority."""
        
        for provider in sorted(self.providers, key=lambda x: x["priority"]):
            if not self.is_healthy(provider["name"]):
                continue
            
            try:
                response = await provider["client"].generate(prompt, **kwargs)
                
                # Track success
                self.mark_healthy(provider["name"])
                
                # Log cost
                self.log_cost(provider["name"], response.get("tokens", 0))
                
                return response
                
            except Exception as e:
                # Mark unhealthy and try next
                self.mark_unhealthy(provider["name"], str(e))
                continue
        
        # All providers failed - return cached/template response
        return self.get_emergency_response(prompt)
    
    def is_healthy(self, provider: str) -> bool:
        """Check if provider is healthy."""
        
        if provider not in self.health_status:
            return True
        
        status = self.health_status[provider]
        
        # Provider is healthy if no errors in last 5 minutes
        if status["last_error"]:
            time_since_error = time.time() - status["last_error_time"]
            return time_since_error > 300  # 5 minutes
        
        return True
    
    def get_emergency_response(self, prompt: str) -> Dict:
        """Emergency response when all providers fail."""
        
        # Use pre-generated responses for common scenarios
        emergency_responses = {
            "greeting": ["Hey! Sorry, got distracted for a sec. What's up?"],
            "question": ["Hmm, that's interesting... tell me more?"],
            "statement": ["Oh really? That's cool"],
            "default": ["*smiles* So what brings you here today?"]
        }
        
        # Simple classification
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ["hi", "hello", "hey"]):
            response_type = "greeting"
        elif "?" in prompt:
            response_type = "question"
        elif len(prompt.split()) > 10:
            response_type = "statement"
        else:
            response_type = "default"
        
        return {
            "message": random.choice(emergency_responses[response_type]),
            "fallback": True,
            "provider": "emergency_cache"
        }
```

### Rate Limiting & Cost Control

```python
class CostControlManager:
    """Manage costs and prevent overruns."""
    
    def __init__(self):
        self.limits = {
            "user_daily": 0.10,      # $0.10 per user per day max
            "user_monthly": 2.00,     # $2.00 per user per month max
            "global_daily": 100.00,   # $100 daily platform limit
            "global_monthly": 2000.00 # $2000 monthly platform limit
        }
        self.usage = {}
    
    async def check_and_track(self, user_id: str, estimated_cost: float) -> bool:
        """Check if request should be allowed based on cost limits."""
        
        # Get user's current usage
        user_usage = await self.get_user_usage(user_id)
        
        # Check daily limit
        if user_usage["daily"] + estimated_cost > self.limits["user_daily"]:
            await self.alert_user_limit(user_id, "daily")
            return False
        
        # Check monthly limit  
        if user_usage["monthly"] + estimated_cost > self.limits["user_monthly"]:
            await self.alert_user_limit(user_id, "monthly")
            return False
        
        # Check global limits
        global_usage = await self.get_global_usage()
        
        if global_usage["daily"] + estimated_cost > self.limits["global_daily"]:
            await self.alert_global_limit("daily")
            return False
        
        # Track the usage
        await self.track_usage(user_id, estimated_cost)
        
        return True
    
    async def optimize_request(self, request: Dict) -> Dict:
        """Optimize request to reduce costs."""
        
        optimizations = []
        
        # Use batch processing for non-real-time
        if not request.get("real_time", True):
            request["batch_mode"] = True
            optimizations.append("batch_processing")
        
        # Reduce max tokens if possible
        if request.get("max_tokens", 100) > 50:
            request["max_tokens"] = min(request["max_tokens"], 75)
            optimizations.append("reduced_tokens")
        
        # Lower temperature for factual responses
        if request.get("type") == "evaluation":
            request["temperature"] = 0.3
            optimizations.append("lower_temperature")
        
        # Use caching-optimized prompt structure
        if "prompt" in request:
            request["prompt"] = self.optimize_for_caching(request["prompt"])
            optimizations.append("cache_optimized")
        
        print(f"Applied optimizations: {optimizations}")
        return request
```

---

## System Architecture Requirements

### Dependencies for Gemini Integration

```yaml
# Backend (Python/FastAPI)
dependencies:
  core:
    - google-genai>=1.0.0  # Official Gemini SDK
    - fastapi>=0.104.0
    - pydantic>=2.0.0
    - python-dotenv>=1.0.0
    
  database:
    - supabase>=2.0.0
    - sqlalchemy>=2.0.0
    - asyncpg>=0.29.0
    
  monitoring:
    - sentry-sdk>=1.40.0
    - prometheus-client>=0.19.0
    
  optimization:
    - redis>=5.0.0
    - numpy>=1.24.0
    
# Frontend (React Native/Expo)
dependencies:
  core:
    - "@google/genai": "^1.0.0"
    - "expo": "~49.0.0"
    - "react-native": "0.72.0"
    
  state_management:
    - "@tanstack/react-query": "^5.0.0"
    - "zustand": "^4.4.0"
    - "react-hook-form": "^7.45.0"
    
  security:
    - "expo-secure-store": "~12.0.0"
    - "crypto-js": "^4.2.0"
    
  networking:
    - "@react-native-community/netinfo": "^9.0.0"
    - "axios": "^1.6.0"
```

### Environment Configuration

```bash
# .env.production
GEMINI_API_KEY=your_production_key
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_BACKUP_MODEL=gemini-1.5-pro-latest

# Cost limits
MAX_DAILY_COST=100.00
MAX_USER_DAILY_COST=0.10
MAX_CONVERSATION_COST=0.002

# Performance
GEMINI_TIMEOUT=30000
GEMINI_MAX_RETRIES=3
CACHE_TTL=3600

# Monitoring
SENTRY_DSN=your_sentry_dsn
ANALYTICS_ENABLED=true
```

### Infrastructure Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - postgres
    
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: flirtcraft
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  monitoring:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}

volumes:
  redis_data:
  postgres_data:
```

---

## Monitoring & Analytics

### Cost and Performance Dashboard

```python
class GeminiAnalyticsDashboard:
    """Real-time monitoring dashboard for Gemini API usage."""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_cost": 0.0,
            "cache_hit_rate": 0.0,
            "avg_response_time": 0.0,
            "error_rate": 0.0
        }
    
    async def get_dashboard_data(self) -> Dict:
        """Get comprehensive dashboard metrics."""
        
        return {
            "real_time": {
                "active_conversations": await self.get_active_conversations(),
                "requests_per_minute": await self.get_rpm(),
                "current_cost_rate": await self.get_cost_rate()
            },
            "daily": {
                "total_conversations": await self.get_daily_conversations(),
                "total_cost": await self.get_daily_cost(),
                "avg_cost_per_conversation": await self.get_avg_cost(),
                "cache_efficiency": await self.get_cache_stats(),
                "error_count": await self.get_error_count()
            },
            "performance": {
                "p50_latency": await self.get_percentile_latency(50),
                "p95_latency": await self.get_percentile_latency(95),
                "p99_latency": await self.get_percentile_latency(99),
                "success_rate": await self.get_success_rate()
            },
            "optimization": {
                "cache_savings": await self.calculate_cache_savings(),
                "batch_savings": await self.calculate_batch_savings(),
                "total_savings": await self.calculate_total_savings()
            },
            "alerts": await self.get_active_alerts()
        }
    
    async def generate_cost_report(self, period: str = "daily") -> Dict:
        """Generate detailed cost breakdown report."""
        
        report = {
            "period": period,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_cost": 0,
                "total_tokens": 0,
                "total_conversations": 0
            },
            "breakdown": {
                "by_feature": {},
                "by_difficulty": {},
                "by_user_tier": {}
            },
            "optimization_opportunities": []
        }
        
        # Calculate costs by feature
        for feature in ["context_generation", "conversation", "feedback", "evaluation"]:
            feature_cost = await self.get_feature_cost(feature, period)
            report["breakdown"]["by_feature"][feature] = feature_cost
            report["summary"]["total_cost"] += feature_cost["cost"]
        
        # Identify optimization opportunities
        if report["summary"]["total_cost"] > 100:  # Daily threshold
            report["optimization_opportunities"].append({
                "recommendation": "Enable batch processing for evaluations",
                "potential_savings": report["breakdown"]["by_feature"]["evaluation"]["cost"] * 0.5
            })
        
        return report
```

### User Analytics Integration

```typescript
// analytics/geminiAnalytics.ts
export class GeminiAnalytics {
    private events: AnalyticsEvent[] = [];
    
    trackConversation(conversationId: string, metrics: ConversationMetrics) {
        this.events.push({
            type: 'conversation',
            id: conversationId,
            timestamp: Date.now(),
            metrics: {
                messages: metrics.messageCount,
                duration: metrics.duration,
                tokens: metrics.totalTokens,
                cost: metrics.estimatedCost,
                cacheRate: metrics.cacheHitRate,
                difficulty: metrics.difficulty,
                outcome: metrics.outcome
            }
        });
        
        // Send batch every 10 events
        if (this.events.length >= 10) {
            this.flush();
        }
    }
    
    trackError(error: any, context: any) {
        this.events.push({
            type: 'error',
            timestamp: Date.now(),
            error: {
                message: error.message,
                code: error.code,
                provider: 'gemini',
                context: context
            }
        });
        
        // Immediately send errors
        this.flush();
    }
    
    async flush() {
        if (this.events.length === 0) return;
        
        try {
            await api.post('/analytics/events', {
                events: this.events,
                session: getSessionId(),
                user: getUserId()
            });
            
            this.events = [];
        } catch (error) {
            console.error('Failed to send analytics:', error);
        }
    }
}
```

---

## Implementation Timeline

### Week 1: Core Integration
- [ ] Set up Gemini API access and test in AI Studio
- [ ] Implement basic conversation engine
- [ ] Test character consistency across 10+ conversations
- [ ] Verify cost calculations match estimates

### Week 2: Optimization
- [ ] Implement implicit caching optimization
- [ ] Add sliding window for conversation history
- [ ] Set up batch processing for evaluations
- [ ] Create cost monitoring dashboard

### Week 3: Production Readiness
- [ ] Implement multi-provider fallback system
- [ ] Add comprehensive error handling
- [ ] Set up monitoring and alerts
- [ ] Performance testing with 100+ concurrent users

### Week 4: Launch Preparation
- [ ] Final cost optimization review
- [ ] A/B testing different prompt strategies
- [ ] Load testing at expected scale
- [ ] Documentation and team training

---

## Conclusion

Google Gemini 2.5 Flash-Lite provides the optimal balance of cost, performance, and capabilities for FlirtCraft:

1. **Cost Efficiency**: At $0.0004 per conversation with caching, it's 80% cheaper than GPT-4o-mini
2. **Performance**: 10x faster inference than GPT-4 models
3. **Scale Ready**: Free tier supports initial testing (1,500 requests/day)
4. **Latest Technology**: July 2025 thinking model with adaptive reasoning
5. **Developer Friendly**: Excellent documentation, simple integration

With proper implementation of caching and optimization, FlirtCraft can achieve:
- **99%+ gross margins** on all subscription tiers
- **Sub-1 second** response times
- **99.9% uptime** with fallback providers
- **$9.99/month** single premium tier with 99%+ margins

---

## Appendix: Quick Reference

### API Endpoints
- **Google AI Studio**: https://ai.google.dev
- **Get API Key**: https://aistudio.google.com/apikey
- **Documentation**: https://ai.google.dev/gemini-api/docs
- **Pricing**: https://ai.google.dev/gemini-api/docs/pricing
- **Cookbook**: https://github.com/google-gemini/cookbook

### Cost Calculator
```python
def quick_cost_estimate(conversations_per_day: int):
    cost_per_conversation = 0.0004  # With caching
    daily_cost = conversations_per_day * cost_per_conversation
    monthly_cost = daily_cost * 30
    
    print(f"Daily: ${daily_cost:.2f}")
    print(f"Monthly: ${monthly_cost:.2f}")
    print(f"Annual: ${monthly_cost * 12:.2f}")
    
    # Subscription needed to break even
    min_subscription = monthly_cost * 3  # 3x for margin
    print(f"Min subscription price: ${min_subscription:.2f}/month")
```

---

*Last Updated: August 2025*  
*Document Version: 3.1*  
*Major Update: Upgraded to Gemini 2.5 Flash-Lite with thinking model for superior performance  
*Author: FlirtCraft Technical Architecture Team*