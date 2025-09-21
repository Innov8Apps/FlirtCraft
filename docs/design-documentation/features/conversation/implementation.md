# Conversation Interface Implementation Guide

---
title: Conversation Interface Implementation
description: Technical implementation guide for real-time chat interface with AI integration
feature: conversation
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ./interactions.md
  - ./accessibility.md
  - ../../design-system/components/chat-bubbles.md
  - ../../design-system/components/forms.md
  - ../../design-system/components/buttons.md
  - ../../design-system/components/navigation.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native with Expo
  - NativeBase components
  - React Native Gifted Chat for chat interface
  - NativeWind 4.1 styling
  - Zustand state management
  - OpenRouter API with google/gemini-2.5-flash-lite
  - WebSocket connection
status: approved
---

## Overview

This implementation guide provides comprehensive technical specifications for building FlirtCraft's conversation interface with extremely human-like AI partners. The system handles real-time chat where AI partners fully embody their personas, strictly adhere to location context and difficulty levels, respond with natural message length variation, and maintain complete awareness of user demographics. The implementation ensures smooth, performant user experience across iOS and Android platforms.

## Architecture Overview

### Technology Stack

**Frontend Framework:**
- **React Native**: 0.72+ with Expo 52+
- **UI Library**: NativeBase for modern, performant components (40% faster than NativeBase)
- **Chat Interface**: React Native Gifted Chat for specialized conversation UX with optimized list rendering
- **Styling**: NativeWind 4.1+ for advanced utility-first styling with compile-time optimization
- **Navigation**: Expo Router for type-safe navigation
- **Animations**: React Native Reanimated 3.0+ for smooth interactions

**State Management:**
- **Global State**: Zustand 4.0+ for conversation state
- **Local State**: React hooks for component-specific state
- **Persistence**: AsyncStorage for conversation history caching
- **Context**: React Context for theme and accessibility preferences

**AI Integration:**
- **Primary**: OpenRouter API with google/gemini-2.5-flash-lite model for character consistency
- **Fallback**: OpenRouter with google/gemini-2.0-flash-lite-001 for reliability when primary is unavailable
- **Processing**: Custom prompt engineering for context awareness
- **Streaming**: Real-time response streaming for better UX

## State Management Implementation

### Zustand Store Structure

```typescript
// stores/conversationStore.ts
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  status: 'sending' | 'sent' | 'delivered' | 'failed';
  metadata?: {
    responseTime?: number;
    contextUsed?: string[];
  };
}

interface ConversationState {
  // Current conversation state
  messages: Message[];
  isTyping: boolean;
  conversationId: string;
  startTime: Date;
  
  // Context from pre-conversation
  scenarioContext: ScenarioContext;
  difficulty: 'green' | 'yellow' | 'red';
  
  // User input state
  inputText: string;
  isInputFocused: boolean;
  showSuggestions: boolean;
  
  // AI response state
  isAiTyping: boolean;
  aiResponseQueue: string[];
  
  // Conversation limits
  messageCount: number;
  maxMessages: number; // 50 total (25 each) for both free and premium
  // No time limits - conversations flow naturally
  
  // Actions
  sendMessage: (content: string) => void;
  receiveAiMessage: (content: string, metadata?: any) => void;
  updateInputText: (text: string) => void;
  setTyping: (isTyping: boolean) => void;
  showConversationStarters: () => void;
  clearConversation: () => void;
  pauseConversation: () => void;
  resumeConversation: () => void;
}

export const useConversationStore = create<ConversationState>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    messages: [],
    isTyping: false,
    conversationId: '',
    startTime: new Date(),
    scenarioContext: null,
    difficulty: 'green',
    inputText: '',
    isInputFocused: false,
    showSuggestions: false,
    isAiTyping: false,
    aiResponseQueue: [],
    messageCount: 0,
    maxMessages: 50, // Same for free and premium users
    
    // Actions implementation
    sendMessage: (content: string) => {
      const newMessage: Message = {
        id: generateMessageId(),
        content: content.trim(),
        sender: 'user',
        timestamp: new Date(),
        status: 'sending',
      };
      
      set((state) => ({
        messages: [...state.messages, newMessage],
        inputText: '',
        messageCount: state.messageCount + 1,
        isTyping: false,
      }));
      
      // Trigger AI response
      get().triggerAiResponse(content);
    },
    
    receiveAiMessage: (content: string, metadata = {}) => {
      const newMessage: Message = {
        id: generateMessageId(),
        content,
        sender: 'ai',
        timestamp: new Date(),
        status: 'delivered',
        metadata,
      };
      
      set((state) => ({
        messages: [...state.messages, newMessage],
        messageCount: state.messageCount + 1,
        isAiTyping: false,
      }));
    },
    
    updateInputText: (text: string) => {
      set({ inputText: text });
      
      // Show suggestions if user is struggling
      if (text.length === 0 && get().messages.length === 0) {
        setTimeout(() => {
          if (get().inputText === '' && get().messages.length === 0) {
            set({ showSuggestions: true });
          }
        }, 30000); // 30 seconds of inactivity
      }
    },
    
    setTyping: (isTyping: boolean) => set({ isTyping }),
    
    // Additional actions...
  }))
);
```

### Message Queue System

```typescript
// services/messageQueue.ts
class MessageQueue {
  private queue: Message[] = [];
  private isProcessing = false;
  
  async addMessage(message: Message): Promise<void> {
    this.queue.push(message);
    if (!this.isProcessing) {
      await this.processQueue();
    }
  }
  
  private async processQueue(): Promise<void> {
    this.isProcessing = true;
    
    while (this.queue.length > 0) {
      const message = this.queue.shift();
      if (!message) continue;
      
      try {
        if (message.sender === 'user') {
          await this.sendUserMessage(message);
        }
        // Update message status
        useConversationStore.getState().updateMessageStatus(message.id, 'sent');
      } catch (error) {
        useConversationStore.getState().updateMessageStatus(message.id, 'failed');
        console.error('Message sending failed:', error);
      }
    }
    
    this.isProcessing = false;
  }
  
  private async sendUserMessage(message: Message): Promise<void> {
    // WebSocket or HTTP implementation for message sending
    // This would integrate with your backend/AI service
  }
}

export const messageQueue = new MessageQueue();
```

## AI Integration Implementation

### OpenRouter API Integration

```typescript
// services/aiService.ts
import axios from 'axios';
import { useConversationStore } from '../stores/conversationStore';

class AIConversationService {
  private apiKey: string;
  private baseUrl: string;
  private primaryModel: string; // google/gemini-2.5-flash-lite
  private fallbackModel: string; // google/gemini-2.0-flash-lite-001

  constructor() {
    this.apiKey = process.env.EXPO_PUBLIC_OPENROUTER_API_KEY;
    this.baseUrl = 'https://openrouter.ai/api/v1/chat/completions';
    this.primaryModel = 'google/gemini-2.5-flash-lite';
    this.fallbackModel = 'google/gemini-2.0-flash-lite-001';
  }

  async generateResponse(userMessage: string): Promise<string> {
    const state = useConversationStore.getState();
    const messages = this.buildMessages(state.messages, state.scenarioContext, state.difficulty, userMessage);

    try {
      const startTime = Date.now();

      // Try primary model first (google/gemini-2.5-flash-lite)
      try {
        const response = await axios.post(this.baseUrl, {
          model: this.primaryModel,
          messages: messages,
          temperature: 0.8,
          max_tokens: 150,
          reasoning: { enabled: true }, // Enable reasoning for character consistency
          response_format: { type: 'json_object' }
        }, {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'HTTP-Referer': 'https://flirtcraft.app',
            'X-Title': 'FlirtCraft',
            'Content-Type': 'application/json'
          }
        });

        const responseTime = Date.now() - startTime;
        const aiResponse = JSON.parse(response.data.choices[0].message.content);

        // Add slight delay for realism if response was too fast
        const minDelay = 1500; // 1.5 seconds minimum
        if (responseTime < minDelay) {
          await new Promise(resolve => setTimeout(resolve, minDelay - responseTime));
        }

        return aiResponse.message;
      } catch (primaryError) {
        // Fallback to google/gemini-2.0-flash-lite-001
        console.log('Primary model failed, using fallback');
        const response = await axios.post(this.baseUrl, {
          model: this.fallbackModel,
          messages: messages,
          temperature: 0.7,
          max_tokens: 150,
          response_format: { type: 'json_object' }
        }, {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'HTTP-Referer': 'https://flirtcraft.app',
            'X-Title': 'FlirtCraft',
            'Content-Type': 'application/json'
          }
        });

        const aiResponse = JSON.parse(response.data.choices[0].message.content);
        return aiResponse.message;
      }
    } catch (error) {
      console.error('AI response generation failed:', error);
      return this.getFallbackResponse(userMessage);
    }
  }
  
  private buildContextPrompt(context: ScenarioContext, difficulty: string): string {
    return `You are playing a romantic interest in a dating scenario practice app called FlirtCraft. 

SCENARIO CONTEXT:
- Location: ${context.environment.location}
- Time: ${context.environment.timeContext}
- Your Character: ${context.partner.description}
- Current Activity: ${context.partner.activity}
- Body Language: ${context.bodyLanguage.overall}
- Difficulty: ${difficulty} (green=receptive, yellow=neutral, red=challenging)

RESPONSE GUIDELINES FOR HUMAN-LIKE BEHAVIOR:
- CRITICAL: Vary message length naturally like real people - sometimes just "lol" or "yeah", sometimes 2-3 sentences, sometimes a full paragraph
- Fully embody the specific character from the pre-conversation context - you ARE this person
- Maintain complete awareness of user's age (${userProfile.age}) and gender (${userProfile.gender})
- Stay 100% consistent with difficulty level: ${this.getDifficultyInstructions(difficulty)}
- Reference location, environment, and your current activity naturally throughout conversation
- React authentically based on your persona - enthusiastic if that's your character, reserved if that's who you are
- Use realistic texting patterns - typos occasionally, emojis when appropriate to character age/style
- Remember everything from earlier in the conversation and reference it naturally
- Show realistic emotional responses - get excited, curious, bored, or distracted based on context
- NEVER break character or give generic responses

MESSAGE LENGTH VARIATION EXAMPLES:
- Short: "haha", "oh really?", "nice", "for sure"
- Medium: "That's actually pretty interesting. What made you get into that?"
- Long: "Oh wow, I totally know what you mean! Last week I was at this place downtown and had the exact same experience. It's funny how these things happen when you least expect them, right?"

Remember: You are a real person in a real location having a real conversation. Act exactly as that person would.`;
  }
  
  private getDifficultyInstructions(difficulty: string): string {
    switch (difficulty) {
      case 'green':
        return 'Be genuinely warm and interested like someone who finds the user attractive. Laugh at their jokes, ask follow-up questions, share personal stories. Make eye contact (mention looking at them). Be flirty if it feels natural.';
      case 'yellow':
        return 'Act like a real stranger - sometimes engaged, sometimes distracted. Mix enthusiasm with normal human reserve. Check your phone occasionally, have moments of genuine interest and moments of polite distance. Exactly how real people act when meeting someone new.';
      case 'red':
        return 'You are genuinely busy/distracted. Give realistic short responses like "yeah" or "mm-hmm" when not engaged. Take longer to respond. Occasionally show brief interest then return to your activity. Act exactly like someone who is polite but has other priorities.';
      default:
        return 'Respond as a real human would in this exact situation with natural variation in interest and engagement.';
  }
  
  private buildConversationHistory(messages: Message[]): any[] {
    return messages.slice(-10).map(msg => ({ // Last 10 messages for context
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.content
    }));
  }
  
  private getFallbackResponse(userMessage: string): string {
    const fallbacks = [
      "That's interesting! Tell me more about that.",
      "I like your perspective on this.",
      "You seem really thoughtful about things.",
      "That caught my attention - what made you think of that?",
      "I appreciate you sharing that with me."
    ];
    
    return fallbacks[Math.floor(Math.random() * fallbacks.length)];
  }
}

export const aiService = new AIConversationService();
```

### Real-time Response Streaming

```typescript
// services/streamingService.ts
import axios from 'axios';

class StreamingResponseService {
  private apiKey: string;
  private baseUrl: string;
  private primaryModel: string;
  private fallbackModel: string;

  constructor() {
    this.apiKey = process.env.EXPO_PUBLIC_OPENROUTER_API_KEY;
    this.baseUrl = 'https://openrouter.ai/api/v1/chat/completions';
    this.primaryModel = 'google/gemini-2.5-flash-lite';
    this.fallbackModel = 'google/gemini-2.0-flash-lite-001';
  }

  async streamAiResponse(messages: any[], onChunk: (chunk: string) => void): Promise<string> {
    try {
      // Try primary model first (google/gemini-2.5-flash-lite)
      let fullResponse: string;

      const headers = {
        'Authorization': `Bearer ${this.apiKey}`,
        'HTTP-Referer': 'https://flirtcraft.app',
        'X-Title': 'FlirtCraft',
        'Content-Type': 'application/json'
      };

      try {
        const response = await axios.post(this.baseUrl, {
          model: this.primaryModel,
          messages: messages,
          temperature: 0.8,
          max_tokens: 150,
          reasoning: { enabled: true },
          response_format: { type: 'json_object' }
        }, { headers });

        fullResponse = JSON.parse(response.data.choices[0].message.content).message;
      } catch (primaryError) {
        console.log('Primary model failed, using fallback');
        // Fallback to google/gemini-2.0-flash-lite-001
        const response = await axios.post(this.baseUrl, {
          model: this.fallbackModel,
          messages: messages,
          temperature: 0.7,
          max_tokens: 150,
          response_format: { type: 'json_object' }
        }, { headers });

        fullResponse = JSON.parse(response.data.choices[0].message.content).message;
      }
      
      // Simulate streaming by chunking the response
      const words = fullResponse.split(' ');
      
      for (let i = 0; i < words.length; i++) {
        const chunk = words[i] + ' ';
        onChunk(chunk); // Real-time UI updates
        await new Promise(resolve => setTimeout(resolve, 50)); // Small delay between words
      }
      
      return fullResponse;
    } catch (error) {
      console.error('Streaming failed:', error);
      throw error;
    }
  }
}

export const streamingService = new StreamingResponseService();
```

## Component Implementation

### Main Conversation Screen with React Native Gifted Chat

```tsx
// screens/ConversationScreen.tsx
import React, { useCallback, useState, useEffect } from 'react';
import { View, Platform } from 'react-native';
import { GiftedChat, IMessage, Bubble, InputToolbar, Send } from 'react-native-gifted-chat';
import { Box, Text, Button, ButtonText, HStack } from 'native-base';
import { useConversationStore } from '../stores/conversationStore';
import { ConversationHeader } from '../components/ConversationHeader';
import { aiService } from '../services/aiService';

export const ConversationScreen: React.FC = () => {
  const { scenarioContext, difficulty } = useConversationStore();
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  
  // Convert messages to Gifted Chat format
  const formatMessages = useCallback((msgs: Message[]): IMessage[] => {
    return msgs.map(msg => ({
      _id: msg.id,
      text: msg.content,
      createdAt: new Date(msg.timestamp),
      user: {
        _id: msg.sender === 'user' ? 1 : 2,
        name: msg.sender === 'user' ? 'You' : 'AI Partner',
        avatar: msg.sender === 'ai' ? 'https://placeholder.com/avatar.png' : undefined,
      },
    }));
  }, []);
  
  // Handle sending messages
  const onSend = useCallback(async (newMessages: IMessage[] = []) => {
    setMessages(previousMessages => GiftedChat.append(previousMessages, newMessages));
    
    // Show AI typing indicator
    setIsTyping(true);
    
    // Get AI response
    const userMessage = newMessages[0].text;
    const aiResponse = await aiService.generateResponse(userMessage);
    
    // Add AI message
    const aiMessage: IMessage = {
      _id: Math.random().toString(),
      text: aiResponse,
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'AI Partner',
      },
    };
    
    setIsTyping(false);
    setMessages(previousMessages => GiftedChat.append(previousMessages, [aiMessage]));
  }, []);
  
  // Custom bubble with FlirtCraft colors
  const renderBubble = (props: any) => {
    return (
      <Bubble
        {...props}
        wrapperStyle={{
          left: {
            backgroundColor: '#FFFFFF',
            borderColor: '#E5E7EB',
            borderWidth: 1,
          },
          right: {
            backgroundColor: '#F97316', // FlirtCraft primary orange
          },
        }}
        textStyle={{
          left: {
            color: '#374151',
          },
          right: {
            color: '#FFFFFF',
          },
        }}
      />
    );
  };
  
  // Custom input toolbar with "Stuck?" helper
  const renderInputToolbar = (props: any) => {
    return (
      <View className="flex-row items-end px-4 py-3 bg-white border-t border-gray-200 dark:bg-gray-900 dark:border-gray-700">
        <InputToolbar
          {...props}
          containerStyle={{
            backgroundColor: 'transparent',
            borderTopWidth: 0,
            paddingHorizontal: 0,
          }}
        />
        <Button
          size="sm"
          className="ml-2 bg-orange-600 hover:bg-orange-700"
          onPress={() => {/* Show suggestions */}}
        >
          <ButtonText>Stuck?</ButtonText>
        </Button>
      </View>
    );
  };
  
  return (
    <View className="flex-1 bg-gray-50 dark:bg-gray-900">
      <ConversationHeader />
      
      <GiftedChat
        messages={messages}
        onSend={onSend}
        user={{
          _id: 1,
          name: 'User',
        }}
        isTyping={isTyping}
        renderBubble={renderBubble}
        renderInputToolbar={renderInputToolbar}
        placeholder="Type your message..."
        alwaysShowSend
        scrollToBottom
        renderUsernameOnMessage={false}
        maxComposerHeight={120}
        minComposerHeight={48}
        keyboardShouldPersistTaps="handled"
        listViewProps={{
          style: { backgroundColor: 'transparent' },
        }}
      />
    </View>
  );
};
```

### Custom Message Components with NativeBase

```tsx
// components/CustomMessageComponents.tsx
import React from 'react';
import { Box, Text, HStack, VStack } from 'native-base';
import { Pressable } from 'react-native';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring,
  Layout,
  FadeInRight,
  FadeInLeft 
} from 'react-native-reanimated';

interface MessageBubbleProps {
  message: Message;
  showTimestamp?: boolean;
  onPress?: () => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  message, 
  showTimestamp = false,
  onPress 
}) => {
  const isUser = message.sender === 'user';
  const scale = useSharedValue(1);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  
  const handlePressIn = () => {
    scale.value = withSpring(0.95);
  };
  
  const handlePressOut = () => {
    scale.value = withSpring(1);
  };
  
  return (
    <Animated.View
      entering={isUser ? FadeInRight.delay(100) : FadeInLeft.delay(100)}
      layout={Layout.springify()}
    >
      <HStack
        justifyContent={isUser ? 'flex-end' : 'flex-start'}
        mb={3}
        px={2}
      >
        <Animated.View style={animatedStyle}>
          <Pressable
            onPress={onPress}
            onPressIn={handlePressIn}
            onPressOut={handlePressOut}
            accessible={true}
            accessibilityRole="text"
            accessibilityLabel={`${isUser ? 'Your' : 'AI'} message: ${message.content}`}
          >
            <Box
              maxW="80%"
              bg={isUser ? "orange.500" : "white"}
              borderRadius={16}
              borderBottomRightRadius={isUser ? 4 : 16}
              borderBottomLeftRadius={isUser ? 16 : 4}
              px={4}
              py={3}
              shadow={isUser ? 2 : 0}
              borderWidth={isUser ? 0 : 1}
              borderColor="gray.200"
            >
              <Text
                color={isUser ? "white" : "gray.800"}
                fontSize={16}
                lineHeight={22}
              >
                {message.content}
              </Text>
              
              {showTimestamp && (
                <Text
                  color={isUser ? "orange.100" : "gray.500"}
                  fontSize={12}
                  mt={1}
                  textAlign={isUser ? "right" : "left"}
                >
                  {message.timestamp.toLocaleTimeString()}
                </Text>
              )}
            </Box>
          </Pressable>
        </Animated.View>
      </HStack>
    </Animated.View>
  );
};
```

### Typing Indicator Component

```tsx
// components/TypingIndicator.tsx
import React, { useEffect } from 'react';
import { Box, HStack, Text } from 'native-base';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withSequence,
  withDelay,
  withTiming,
} from 'react-native-reanimated';

export const TypingIndicator: React.FC = () => {
  const dot1Opacity = useSharedValue(0.3);
  const dot2Opacity = useSharedValue(0.3);
  const dot3Opacity = useSharedValue(0.3);
  
  useEffect(() => {
    // Staggered animation for the three dots
    dot1Opacity.value = withRepeat(
      withSequence(
        withTiming(1, { duration: 400 }),
        withTiming(0.3, { duration: 400 })
      ),
      -1,
      false
    );
    
    dot2Opacity.value = withDelay(
      200,
      withRepeat(
        withSequence(
          withTiming(1, { duration: 400 }),
          withTiming(0.3, { duration: 400 })
        ),
        -1,
        false
      )
    );
    
    dot3Opacity.value = withDelay(
      400,
      withRepeat(
        withSequence(
          withTiming(1, { duration: 400 }),
          withTiming(0.3, { duration: 400 })
        ),
        -1,
        false
      )
    );
  }, []);
  
  const dot1Style = useAnimatedStyle(() => ({ opacity: dot1Opacity.value }));
  const dot2Style = useAnimatedStyle(() => ({ opacity: dot2Opacity.value }));
  const dot3Style = useAnimatedStyle(() => ({ opacity: dot3Opacity.value }));
  
  return (
    <HStack justifyContent="flex-start" mb={3} px={2}>
      <Box
        bg="white"
        borderRadius={16}
        borderBottomLeftRadius={4}
        px={4}
        py={3}
        borderWidth={1}
        borderColor="gray.200"
      >
        <HStack space={1} alignItems="center">
          <Animated.View style={dot1Style}>
            <Box w={2} h={2} bg="gray.400" borderRadius="full" />
          </Animated.View>
          <Animated.View style={dot2Style}>
            <Box w={2} h={2} bg="gray.400" borderRadius="full" />
          </Animated.View>
          <Animated.View style={dot3Style}>
            <Box w={2} h={2} bg="gray.400" borderRadius="full" />
          </Animated.View>
        </HStack>
      </Box>
    </HStack>
  );
};
```

## Performance Optimization

### Memory Management

```typescript
// hooks/useConversationOptimization.ts
import { useMemo, useCallback } from 'react';
import { useConversationStore } from '../stores/conversationStore';

export const useConversationOptimization = () => {
  const messages = useConversationStore(state => state.messages);
  
  // Optimize message list for large conversations
  const optimizedMessages = useMemo(() => {
    // Keep only recent messages in memory for rendering
    const maxVisibleMessages = 100;
    return messages.length > maxVisibleMessages 
      ? messages.slice(-maxVisibleMessages)
      : messages;
  }, [messages]);
  
  // Debounced input handling
  const debouncedUpdateInput = useCallback(
    debounce((text: string) => {
      useConversationStore.getState().updateInputText(text);
    }, 300),
    []
  );
  
  return {
    optimizedMessages,
    debouncedUpdateInput,
  };
};

// Utility function
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
```

### Virtual List Implementation

```tsx
// components/VirtualizedMessageList.tsx
import React from 'react';
import { FlatList, ViewToken } from 'react-native';
import { Box } from 'native-base';
import { MessageBubble } from './MessageBubble';

interface VirtualizedMessageListProps {
  messages: Message[];
  onEndReached?: () => void;
  onScrollToEnd?: () => void;
}

export const VirtualizedMessageList: React.FC<VirtualizedMessageListProps> = ({
  messages,
  onEndReached,
  onScrollToEnd,
}) => {
  const renderItem = useCallback(({ item }: { item: Message }) => (
    <MessageBubble message={item} />
  ), []);
  
  const keyExtractor = useCallback((item: Message) => item.id, []);
  
  const getItemLayout = useCallback((data: Message[] | null | undefined, index: number) => ({
    length: 80, // Estimated item height
    offset: 80 * index,
    index,
  }), []);
  
  return (
    <FlatList
      data={messages}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      getItemLayout={getItemLayout}
      onEndReached={onEndReached}
      onEndReachedThreshold={0.1}
      showsVerticalScrollIndicator={false}
      windowSize={10}
      maxToRenderPerBatch={5}
      updateCellsBatchingPeriod={100}
      removeClippedSubviews={true}
      contentContainerStyle={{ paddingVertical: 16 }}
    />
  );
};
```

## Testing Implementation

### Unit Testing

```typescript
// __tests__/conversationStore.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useConversationStore } from '../stores/conversationStore';

describe('ConversationStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useConversationStore.getState().clearConversation();
  });
  
  it('should send user message correctly', () => {
    const { result } = renderHook(() => useConversationStore());
    
    act(() => {
      result.current.sendMessage('Hello there!');
    });
    
    expect(result.current.messages).toHaveLength(1);
    expect(result.current.messages[0]).toMatchObject({
      content: 'Hello there!',
      sender: 'user',
      status: 'sending',
    });
  });
  
  it('should enforce message limits', () => {
    const { result } = renderHook(() => useConversationStore());
    
    // Send maximum number of messages
    act(() => {
      for (let i = 0; i < 25; i++) {
        result.current.sendMessage(`Message ${i}`);
      }
    });
    
    expect(result.current.messageCount).toBe(25);
    expect(result.current.canSendMessage).toBe(false);
  });
});
```

### Integration Testing

```typescript
// __tests__/ConversationScreen.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { ConversationScreen } from '../screens/ConversationScreen';
import { useConversationStore } from '../stores/conversationStore';

// Mock AI service
jest.mock('../services/aiService', () => ({
  aiService: {
    generateResponse: jest.fn(() => Promise.resolve('AI response')),
  },
}));

describe('ConversationScreen', () => {
  it('should send message when send button is pressed', async () => {
    const { getByPlaceholderText, getByRole } = render(<ConversationScreen />);
    
    const input = getByPlaceholderText('Type your message...');
    const sendButton = getByRole('button', { name: /send/i });
    
    fireEvent.changeText(input, 'Test message');
    fireEvent.press(sendButton);
    
    await waitFor(() => {
      expect(useConversationStore.getState().messages).toHaveLength(1);
    });
  });
  
  it('should display typing indicator when AI is responding', async () => {
    const { getByTestId } = render(<ConversationScreen />);
    
    // Simulate AI typing
    act(() => {
      useConversationStore.getState().setAiTyping(true);
    });
    
    expect(getByTestId('typing-indicator')).toBeTruthy();
  });
});
```

## Deployment Configuration

### Environment Configuration

```typescript
// config/environment.ts
const Config = {
  development: {
    OPENROUTER_API_KEY: process.env.EXPO_PUBLIC_OPENROUTER_API_KEY_DEV,
    API_BASE_URL: 'http://localhost:3000',
    WEBSOCKET_URL: 'ws://localhost:3001',
    ENABLE_WEBSOCKET_FALLBACK: true, // Auto-fallback to polling if WebSocket fails
    DEBUG_MODE: true,
  },
  production: {
    OPENROUTER_API_KEY: process.env.EXPO_PUBLIC_OPENROUTER_API_KEY,
    API_BASE_URL: 'https://api.flirtcraft.app',
    WEBSOCKET_URL: 'wss://ws.flirtcraft.app',
    ENABLE_WEBSOCKET_FALLBACK: true, // Auto-fallback to polling if WebSocket fails
    DEBUG_MODE: false,
  },
};

export default Config[process.env.NODE_ENV || 'development'];
```

### Performance Monitoring

```typescript
// services/performanceMonitoring.ts
class PerformanceMonitor {
  trackMessageSendTime(startTime: number, endTime: number) {
    const duration = endTime - startTime;
    console.log(`Message send time: ${duration}ms`);
    
    // Report to analytics service
    this.reportMetric('message_send_time', duration);
  }
  
  trackAIResponseTime(startTime: number, endTime: number) {
    const duration = endTime - startTime;
    console.log(`AI response time: ${duration}ms`);
    
    this.reportMetric('ai_response_time', duration);
  }
  
  private reportMetric(event: string, value: number) {
    // Integration with analytics service (Firebase, Mixpanel, etc.)
  }
}

export const performanceMonitor = new PerformanceMonitor();
```

## Security Implementation

### Input Sanitization

```typescript
// utils/inputSanitization.ts
export const sanitizeUserInput = (input: string): string => {
  // Remove potentially harmful characters
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+="[^"]*"/gi, '')
    .trim()
    .substring(0, 1000); // Limit length
};

export const validateMessageContent = (content: string): boolean => {
  if (content.length === 0 || content.length > 1000) return false;
  
  // Check for inappropriate content patterns
  const inappropriatePatterns = [
    // Add patterns as needed
  ];
  
  return !inappropriatePatterns.some(pattern => 
    new RegExp(pattern, 'i').test(content)
  );
};
```

### Data Encryption

```typescript
// services/encryption.ts
import CryptoJS from 'crypto-js';
import AsyncStorage from '@react-native-async-storage/async-storage';

class EncryptionService {
  private secretKey = process.env.EXPO_PUBLIC_ENCRYPTION_KEY || 'fallback-key';
  
  encrypt(data: string): string {
    return CryptoJS.AES.encrypt(data, this.secretKey).toString();
  }
  
  decrypt(encryptedData: string): string {
    const bytes = CryptoJS.AES.decrypt(encryptedData, this.secretKey);
    return bytes.toString(CryptoJS.enc.Utf8);
  }
  
  async storeSecureData(key: string, data: any): Promise<void> {
    const encryptedData = this.encrypt(JSON.stringify(data));
    await AsyncStorage.setItem(key, encryptedData);
  }
  
  async getSecureData(key: string): Promise<any | null> {
    const encryptedData = await AsyncStorage.getItem(key);
    if (!encryptedData) return null;
    
    try {
      const decryptedData = this.decrypt(encryptedData);
      return JSON.parse(decryptedData);
    } catch (error) {
      console.error('Data decryption failed:', error);
      return null;
    }
  }
}

export const encryptionService = new EncryptionService();
```

---

## Premium Integration

### Conversation Usage Tracking

The conversation feature tracks daily usage and increments counters after starting a conversation:

```typescript
// src/features/conversation/hooks/useConversationTracking.ts
import { useSubscriptionStore } from '../../../stores/subscriptionStore';

export const useConversationTracking = () => {
  const { incrementDailyUsage } = useSubscriptionStore();
  
  const trackConversationStart = () => {
    // Increment daily usage counter when conversation actually starts
    // (not when context is generated)
    incrementDailyUsage('conversations');
    
    // Track analytics
    analytics.track('conversation_started', {
      timestamp: new Date().toISOString(),
      source: 'post_context_review'
    });
  };
  
  return { trackConversationStart };
};
```

### Conversation Screen Usage Integration

```typescript
// Update ConversationScreen to track usage on conversation start
export const ConversationScreen: React.FC = ({ route }) => {
  const { trackConversationStart } = useConversationTracking();
  const { contextData } = route.params;
  
  // Track conversation start on component mount
  useEffect(() => {
    // Only track once when conversation actually begins
    trackConversationStart();
  }, []);
  
  // Rest of conversation logic remains unchanged
  return (
    <Box flex={1} bg="gray.50" safeArea>
      <ConversationHeader />
      
      <KeyboardAvoidingView style={{ flex: 1 }}>
        <VStack flex={1}>
          {/* Message List - no changes needed */}
          <Box flex={1} px={4}>
            <FlatList
              ref={flatListRef}
              data={messages}
              renderItem={renderMessage}
              keyExtractor={(item) => item.id}
            />
            {isAiTyping && <TypingIndicator />}
          </Box>
          
          {/* Message Input - no changes needed */}
          <MessageInput />
        </VStack>
      </KeyboardAvoidingView>
    </Box>
  );
};
```

### No Additional Premium Logic Required

The conversation feature itself has no premium restrictions once started. All premium gating occurs in the pre-conversation phase through:

1. **Daily Limit Check**: Handled in pre-conversation-context feature
2. **Scenario Access**: Handled in scenario-selection feature  
3. **Difficulty Access**: Handled in scenario-selection feature

The conversation flows identically for both free and premium users once they've gained access to start it.

---

## Related Documentation

- [Conversation Feature README](./README.md) - Complete feature overview and design specifications
- [User Journey](./user-journey.md) - Detailed user flow through conversation interface
- [Screen States](./screen-states.md) - All possible interface states and transitions
- [Accessibility Implementation](./accessibility.md) - Complete accessibility compliance guide

## Implementation Checklist

### Core Features
- [ ] Zustand store implementation with message management
- [ ] OpenRouter API integration with fallback models
- [ ] Real-time message rendering with animations
- [ ] Input field with validation and character limits
- [ ] WebSocket integration for real-time features

### Performance Features
- [ ] Virtual list rendering for large conversations
- [ ] Memory optimization with message cleanup
- [ ] Debounced input handling
- [ ] Optimized animation performance
- [ ] Background sync capabilities

### Security Features
- [ ] Input sanitization and validation
- [ ] Encrypted local storage for sensitive data
- [ ] API key security implementation
- [ ] Content filtering for inappropriate messages

### Testing Complete
- [ ] Unit tests for store and utilities
- [ ] Integration tests for main components
- [ ] Performance testing under load
- [ ] Security testing for input validation
- [ ] End-to-end user flow testing

---

*This implementation guide provides the technical foundation for FlirtCraft's conversation interface, ensuring a smooth, secure, and performant user experience across all supported platforms.*