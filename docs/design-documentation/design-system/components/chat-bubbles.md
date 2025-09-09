# Chat Bubble Components

---
title: FlirtCraft Chat Bubble Components
description: User and AI message bubbles, typing indicators, and conversation interface elements
feature: conversation
last-updated: 2025-08-30
version: 2.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ../tokens/typography.md
dependencies:
  - React Native Gifted Chat
  - React Native Reanimated 3 for typing animations
  - NativeBase components
  - NativeWind 4.1 utilities
status: approved
---

## Overview

Chat bubble components create the core conversation interface where users practice with AI partners. Built on React Native Gifted Chat for robust functionality, with custom styling using NativeBase and NativeWind 4.1. The design emphasizes clarity, natural conversation flow, and subtle feedback mechanisms that support learning without interruption.

## React Native Gifted Chat Integration

### Base GiftedChat Setup
```jsx
import { GiftedChat, Bubble, InputToolbar, Send } from 'react-native-gifted-chat';
import { Button } from 'native-base';
import { Pressable } from 'react-native';

const ConversationScreen = () => {
  const [messages, setMessages] = useState([]);

  const onSend = useCallback((messages = []) => {
    setMessages(previousMessages =>
      GiftedChat.append(previousMessages, messages)
    );
  }, []);

  return (
    <GiftedChat
      messages={messages}
      onSend={onSend}
      user={{
        _id: 1,
        name: 'User',
        avatar: 'https://placeimg.com/140/140/any',
      }}
      renderBubble={renderBubble}
      renderInputToolbar={renderInputToolbar}
      renderSend={renderSend}
      renderAvatar={renderAvatar}
    />
  );
};
```

## Chat Bubble Architecture

### Message Types
1. **User Messages** - Right-aligned, primary color bubbles
2. **AI Messages** - Left-aligned, neutral color bubbles  
3. **System Messages** - Centered, minimal styling for flow updates
4. **Typing Indicators** - Animated dots showing AI is composing response

## Component Specifications

### User Message Bubble

#### Purpose
Display user's messages in conversation with visual feedback on message quality.

#### Visual Specifications

**Container:**
- **Alignment**: Right-aligned with 16px right margin
- **Max Width**: 75% of screen width to prevent overly long lines
- **Min Height**: `40px` for single-line messages
- **Margin**: 8px vertical spacing between messages
- **Animation**: Slide in from right (200ms ease-out) when sent

**Bubble Styling:**
- **Background**: `#F97316` (Primary) - confident, user-centric color
- **Border Radius**: `16px 16px 4px 16px` - chat-style with pointer
- **Padding**: `12px 16px` - comfortable text spacing
- **Shadow**: `0 1px 2px rgba(99, 102, 241, 0.15)` - subtle depth

**Typography:**
- **Font**: Body (16px/22px, 400 weight) - optimal for reading
- **Color**: `#FFFFFF` (White) for contrast against primary background
- **Text Alignment**: Left-aligned within bubble for natural reading

**Quality Feedback Border (Subtle):**
- **Excellent Response**: Very subtle `#10B981` (Success) thin border
- **Good Response**: Standard appearance, no additional border
- **Needs Improvement**: Very subtle `#F59E0B` (Warning) thin border
- **Border Width**: 1px maximum to avoid being distracting
- **Animation**: Border fades in over 300ms after AI processes response

#### Message States

**Sending State:**
- **Opacity**: 70% while message is being sent
- **Icon**: Small sending spinner (12px) in bottom-right
- **Duration**: Until server confirms receipt

**Sent State:**
- **Opacity**: 100% full opacity
- **Timestamp**: Available on tap, fade in below bubble
- **Confirmation**: Subtle checkmark animation (optional)

**Failed State:**
- **Opacity**: 50% with retry option
- **Icon**: Warning icon with tap-to-retry
- **Border**: Subtle error color indication

### AI Message Bubble

#### Purpose
Display AI partner responses that adapt to conversation context and difficulty level.

#### Visual Specifications

**Container:**
- **Alignment**: Left-aligned with 16px left margin
- **Max Width**: 75% of screen width for readability
- **Avatar**: Small circle (32px) with AI partner representation
- **Avatar Positioning**: Top-left, 8px margin from bubble

**Bubble Styling:**
- **Background**: `#F3F4F6` (Neutral-100) - neutral, friendly appearance
- **Border Radius**: `16px 16px 16px 4px` - mirror of user bubble
- **Padding**: `12px 16px` - matching user message spacing
- **Shadow**: `0 1px 2px rgba(0, 0, 0, 0.05)` - very subtle elevation

**Typography:**
- **Font**: Body (16px/22px, 400 weight) - consistent with user messages
- **Color**: `#374151` (Neutral-700) - high contrast for readability
- **Text Alignment**: Left-aligned for natural reading flow

**AI Avatar Design:**
- **Background**: Subtle gradient based on scenario difficulty
  - Green Difficulty: `#E6FFFA` (Emerald-50) to `#A7F3D0` (Emerald-200)
  - Yellow Difficulty: `#FFFBEB` (Amber-50) to `#FDE68A` (Amber-200)
  - Red Difficulty: `#FEF2F2` (Red-50) to `#FECACA` (Red-200)
- **Icon**: Simple geometric or initial-based representation
- **Size**: 32px circle with 2px border in matching difficulty color

#### AI Response Characteristics by Difficulty

**Green (Friendly) Responses:**
- **Tone**: Warm, encouraging, patient
- **Length**: Moderate length with follow-up questions
- **Engagement**: High interest, asks about user's interests
- **Example Timing**: 1-2 second response delay for natural feel

**Yellow (Real Talk) Responses:**
- **Tone**: Neutral, authentic, realistic stranger behavior
- **Length**: Varied based on conversation quality
- **Engagement**: Moderate, requires genuine engagement to maintain
- **Example Timing**: 2-3 second delay with natural hesitation

**Red (A-Game) Responses:**
- **Tone**: Initially reserved, brief, requires skill to warm up
- **Length**: Short initially, longer as user demonstrates skill
- **Engagement**: Low initially, increases with quality conversation
- **Example Timing**: 1.5-2 second delay, sometimes longer pauses

### Typing Indicator

#### Purpose
Show AI partner is composing a response, maintaining conversation flow.

#### Visual Specifications

**Container:**
- **Position**: Left-aligned, same positioning as AI messages
- **Avatar**: Same AI avatar as regular messages
- **Animation**: Gentle bounce indicating active thinking

**Bubble Design:**
- **Background**: `#F3F4F6` (Neutral-100) - matching AI messages
- **Size**: `60px width × 40px height` - compact, unobtrusive
- **Border Radius**: `16px 16px 16px 4px` - consistent with AI bubbles
- **Padding**: `12px` - centered dot animation

**Typing Animation:**
- **Dots**: Three dots (•••) with staggered bounce animation
- **Color**: `#9CA3AF` (Neutral-400) - subtle, not attention-grabbing
- **Timing**: 
  - Each dot bounces with 200ms intervals
  - Total animation cycle: 1.2 seconds
  - Continuous loop until response appears
- **Physics**: Subtle bounce with ease-in-out timing

**Duration Logic:**
- **Green Difficulty**: 1-2 seconds (enthusiastic response)
- **Yellow Difficulty**: 2-3 seconds (realistic thinking time)
- **Red Difficulty**: 1.5-3 seconds (considering if worth responding)
- **Long Messages**: Additional 0.5 seconds per 20 characters

#### React Native Gifted Chat + NativeBase Implementation
```jsx
import { TypingAnimation } from 'react-native-gifted-chat';
import { Box, HStack, Text } from 'native-base';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle,
  withRepeat,
  withSequence,
  withSpring,
  withDelay
} from 'react-native-reanimated';

const CustomTypingIndicator = () => {
  const dot1 = useSharedValue(0);
  const dot2 = useSharedValue(0);
  const dot3 = useSharedValue(0);

  useEffect(() => {
    const animateDot = (dot, delay) => {
      dot.value = withDelay(
        delay,
        withRepeat(
          withSequence(
            withSpring(1, { damping: 15, stiffness: 200 }),
            withSpring(0, { damping: 15, stiffness: 200 })
          ),
          -1,
          false
        )
      );
    };

    animateDot(dot1, 0);
    animateDot(dot2, 200);
    animateDot(dot3, 400);
  }, []);

  const dot1Style = useAnimatedStyle(() => ({
    transform: [{ translateY: dot1.value * -4 }]
  }));
  
  const dot2Style = useAnimatedStyle(() => ({
    transform: [{ translateY: dot2.value * -4 }]
  }));
  
  const dot3Style = useAnimatedStyle(() => ({
    transform: [{ translateY: dot3.value * -4 }]
  }));

  return (
    <HStack alignItems="flex-end" ml={4} mb={2}>
      <Box w={8} h={8} borderRadius="full" bg="gray.200" mr={2} />
      <Box 
        bg={"gray.100"} 
        _dark={{ bg: "gray.800" }} 
        borderRadius={16} 
        borderBottomLeftRadius={4}
        px={3} 
        py={2} 
        minH={10} 
        justifyContent="center"
      >
        <HStack space={1} alignItems="center">
          <Animated.View style={dot1Style}>
            <Text color="gray.400" fontSize="lg">•</Text>
          </Animated.View>
          <Animated.View style={dot2Style}>
            <Text color="gray.400" fontSize="lg">•</Text>
          </Animated.View>
          <Animated.View style={dot3Style}>
            <Text color="gray.400" fontSize="lg">•</Text>
          </Animated.View>
        </HStack>
      </Box>
    </HStack>
  );
};

// Integration with GiftedChat
const renderTyping = () => {
  if (isTyping) {
    return <CustomTypingIndicator />;
  }
  return null;
};
```

### System Messages

#### Purpose
Non-intrusive conversation flow updates and guidance messages.

#### Visual Specifications

**Container:**
- **Alignment**: Center-aligned with equal margins
- **Width**: Auto-sizing based on content
- **Margin**: 16px vertical spacing from regular messages
- **Background**: Transparent to minimize visual interruption

**Message Styling:**
- **Background**: `rgba(107, 114, 128, 0.1)` (Neutral-500 at 10% opacity)
- **Border Radius**: `12px` - fully rounded for pill appearance
- **Padding**: `8px 16px` - compact but readable
- **Border**: None - relies on subtle background

**Typography:**
- **Font**: Body Small (14px/20px, 400 weight) - less prominent than messages
- **Color**: `#6B7280` (Neutral-500) - understated
- **Text Alignment**: Center-aligned
- **Style**: Italics for differentiation from conversation content

#### System Message Types

**Conversation Start:**
- **Text**: "Conversation started - good luck!"
- **Color**: `#10B981` (Success) background tint

**Time Updates:**
- **Text**: "5 minutes in - great conversation flow!"
- **Color**: `#3B82F6` (Info) background tint

**Message Limit Warning:**
- **Text**: "10 messages remaining"
- **Color**: `#F59E0B` (Warning) background tint

**Conversation End:**
- **Text**: "Conversation completed"
- **Color**: `#F97316` (Primary) background tint

### Custom Message Input with React Native Gifted Chat

#### Purpose
Customized GiftedChat input toolbar with FlirtCraft styling and helper features.

#### GiftedChat InputToolbar Customization

```jsx
import { InputToolbar, Composer, Send } from 'react-native-gifted-chat';
import { Box, Button } from 'native-base';
import { Pressable, View, Text } from 'react-native';

const renderInputToolbar = (props) => {
  return (
    <InputToolbar
      {...props}
      containerStyle={{
        backgroundColor: '#FFFFFF',
        borderTopWidth: 1,
        borderTopColor: '#E5E7EB',
        paddingHorizontal: 16,
        paddingTop: 8,
        paddingBottom: 8,
        shadowColor: '#000000',
        shadowOffset: { width: 0, height: -2 },
        shadowOpacity: 0.04,
        shadowRadius: 8,
        elevation: 4,
      }}
      renderActions={renderActions}
    />
  );
};

const renderComposer = (props) => {
  return (
    <Composer
      {...props}
      textInputStyle={{
        backgroundColor: '#F9FAFB',
        borderRadius: 20,
        borderWidth: 1,
        borderColor: '#E5E7EB',
        paddingHorizontal: 16,
        paddingVertical: 10,
        marginRight: 8,
        fontSize: 16,
        lineHeight: 22,
        color: '#1F2937',
        maxHeight: 120,
        minHeight: 40,
      }}
      placeholder="Type your message..."
      placeholderTextColor="#9CA3AF"
      multiline
    />
  );
};

const renderSend = (props) => {
  return (
    <Send {...props}>
      <Pressable 
        className={`w-8 h-8 rounded-full items-center justify-center ${props.text ? 'bg-primary' : 'bg-gray-300'}`}
        disabled={!props.text}
      >
        <Text className="text-white text-lg">→</Text>
      </Pressable>
    </Send>
  );
};

// Helper "Stuck?" button
const renderActions = () => {
  return (
    <Button 
      variant="ghost" 
      size="sm" 
      onPress={handleStuckPressed}
      mr={2}
      colorScheme="primary"
    >
      💡
    </Button>
  );
};
```

#### NativeWind 4.1 Styling Alternative
```jsx
const renderInputToolbar = (props) => {
  return (
    <InputToolbar
      {...props}
      containerStyle={{
        backgroundColor: 'white',
        borderTopWidth: 1,
        borderTopColor: '#E5E7EB',
      }}
      className="px-4 pt-2 pb-2 shadow-sm border-t border-gray-200 dark:bg-gray-900 dark:border-gray-700"
    />
  );
};

const renderSend = (props) => {
  return (
    <Send {...props}>
      <View className="w-8 h-8 rounded-full bg-primary items-center justify-center opacity-100 disabled:opacity-50 dark:bg-primary-light">
        <Text className="text-white text-lg font-medium">→</Text>
      </View>
    </Send>
  );
};
```

#### Input States

**Empty State:**
- **Send Button**: Gray background, disabled
- **Placeholder**: Visible and guiding
- **Helper**: "Stuck?" button available

**Typing State:**
- **Send Button**: Primary color, enabled
- **Character Count**: Shows when approaching limits
- **Auto-expand**: Grows with content

**Sending State:**
- **Input**: Disabled while sending
- **Send Button**: Spinner animation
- **Duration**: Until message confirmed sent

### Message Interaction Features

#### Long-Press Actions

**User Messages:**
- **Copy Text**: Copy message content to clipboard
- **Rephrase**: Get alternative ways to say the same thing (limited uses)
- **Delete**: Remove message (with confirmation for significant messages)

**AI Messages:**
- **Copy Text**: Copy AI response
- **Report**: Report inappropriate content (rare but available)
- **Context**: "Why did they respond this way?" educational tip

#### Timestamp Display
- **Trigger**: Single tap on any message bubble
- **Appearance**: Fade in below message
- **Format**: "2:34 PM" or relative time "5 minutes ago"
- **Duration**: Fade out after 3 seconds
- **Multiple Messages**: Only one timestamp visible at a time

### Accessibility Features

#### Screen Reader Support
- **Message Announcements**: "You said: [message content]" and "They replied: [message content]"
- **Typing Indicator**: "They are typing" announcement
- **Send Button**: "Send message" with state information
- **Input Field**: Proper labeling and content description

#### Visual Accessibility
- **High Contrast**: All text meets WCAG AA standards
- **Focus Indicators**: Clear focus rings on interactive elements
- **Text Scaling**: Bubbles adapt to user's preferred text size
- **Color Independence**: Quality feedback uses more than color

#### Motor Accessibility
- **Touch Targets**: Send button and interactive elements 44x44px minimum
- **Input Alternatives**: Voice input supported through system
- **Gesture Alternatives**: All swipe actions have button alternatives
- **Error Recovery**: Easy correction of sending mistakes

## Usage Guidelines

### Message Composition Best Practices

**Length Recommendations:**
- **Optimal**: 10-30 words per message for natural conversation
- **Maximum**: 200 characters before warning appears
- **Minimum**: No minimum, single words allowed

**Quality Indicators:**
- Subtle visual feedback on message quality
- Never block sending based on quality
- Educational rather than restrictive approach

**Flow Management:**
- System messages provide gentle guidance
- Timing creates natural conversation rhythm
- AI responses adapt to user skill level

### Animation Performance

**Hardware Acceleration:**
- All animations use transform and opacity properties
- Native driver enabled for 60fps performance
- Reduced motion alternatives provided

**Memory Management:**
- Old messages virtualized in long conversations
- Typing animations cleaned up when component unmounts
- Image and media messages handled efficiently

### Custom Bubble Rendering

#### FlirtCraft Message Bubbles
```jsx
const renderBubble = (props) => {
  const isUser = props.currentMessage.user._id === 1;
  
  return (
    <Bubble
      {...props}
      wrapperStyle={{
        right: {
          backgroundColor: '#F97316',
          borderRadius: 16,
          borderBottomRightRadius: 4,
          marginRight: 8,
          marginBottom: 8,
          maxWidth: '75%',
          shadowColor: '#F97316',
          shadowOffset: { width: 0, height: 1 },
          shadowOpacity: 0.15,
          shadowRadius: 2,
          elevation: 2,
        },
        left: {
          backgroundColor: '#F3F4F6',
          borderRadius: 16,
          borderBottomLeftRadius: 4,
          marginLeft: 8,
          marginBottom: 8,
          maxWidth: '75%',
          shadowColor: '#000000',
          shadowOffset: { width: 0, height: 1 },
          shadowOpacity: 0.05,
          shadowRadius: 2,
          elevation: 1,
        }
      }}
      textStyle={{
        right: {
          color: '#FFFFFF',
          fontSize: 16,
          lineHeight: 22,
          fontWeight: '400',
        },
        left: {
          color: '#374151',
          fontSize: 16,
          lineHeight: 22,
          fontWeight: '400',
        }
      }}
      containerStyle={{
        right: {
          paddingHorizontal: 16,
          paddingVertical: 12,
        },
        left: {
          paddingHorizontal: 16,
          paddingVertical: 12,
        }
      }}
    />
  );
};
```

#### Custom Avatar with Difficulty Colors
```jsx
const renderAvatar = (props) => {
  const isUser = props.currentMessage.user._id === 1;
  
  if (isUser) return null; // Don't show avatar for user messages
  
  const difficultyColors = {
    green: { bg: '#E6FFFA', border: '#10B981' },
    yellow: { bg: '#FFFBEB', border: '#F59E0B' },
    red: { bg: '#FEF2F2', border: '#EF4444' }
  };
  
  const currentDifficulty = getDifficultyFromContext(); // Your difficulty logic
  const colors = difficultyColors[currentDifficulty] || difficultyColors.green;
  
  return (
    <View 
      className="w-8 h-8 rounded-full items-center justify-center mr-2"
      style={{
        backgroundColor: colors.bg,
        borderWidth: 2,
        borderColor: colors.border,
      }}
    >
      <Text className="text-sm font-medium" style={{ color: colors.border }}>
        AI
      </Text>
    </View>
  );
};
```

## Implementation Notes

### React Native Gifted Chat Configuration
```jsx
const ConversationScreen = () => {
  return (
    <GiftedChat
      messages={messages}
      onSend={onSend}
      user={{ _id: 1 }}
      
      // Custom renderers
      renderBubble={renderBubble}
      renderInputToolbar={renderInputToolbar}
      renderSend={renderSend}
      renderAvatar={renderAvatar}
      renderActions={renderActions}
      renderComposer={renderComposer}
      
      // Styling
      messagesContainerStyle={{
        backgroundColor: '#FFFFFF',
        paddingHorizontal: 8,
      }}
      
      // Behavior
      keyboardShouldPersistTaps="never"
      scrollToBottom
      scrollToBottomStyle={{
        backgroundColor: '#F97316',
        borderRadius: 20,
      }}
      
      // Performance
      listViewProps={{
        style: { backgroundColor: 'white' },
        keyboardShouldPersistTaps: 'handled',
      }}
      
      // Accessibility
      accessible
      accessibilityLabel="Chat messages"
    />
  );
};
```

### React Native Considerations
- **GiftedChat Integration**: Built on proven chat library for reliability
- **Keyboard Avoiding**: GiftedChat handles keyboard avoidance automatically
- **Safe Areas**: Respect device safe areas for chat interface
- **Performance**: GiftedChat includes virtualization for long conversations
- **Memory**: Automatic message management and cleanup

### Platform-Specific Features

**iOS:**
- **Haptic Feedback**: Add on message send with `Haptics.impactAsync()`
- **Native Input**: GiftedChat uses native TextInput behaviors
- **Swipe Actions**: Consider iOS-style message actions
- **Dynamic Type**: Automatic support through React Native

**Android:**
- **Material Design**: Custom styling matches Material patterns
- **Hardware Keyboard**: Full keyboard support through GiftedChat
- **Accessibility**: TalkBack optimization built-in
- **Performance**: Optimized for wide range of Android devices

---

### Dark Mode Support with NativeWind 4.1
```jsx
// Dark mode bubble styling
const renderBubble = (props) => {
  return (
    <Bubble
      {...props}
      wrapperStyle={{
        right: {
          backgroundColor: '#F97316', // Primary stays same in dark mode
        },
        left: {
          backgroundColor: '#374151', // Dark mode: gray-700
        }
      }}
      textStyle={{
        right: {
          color: '#FFFFFF',
        },
        left: {
          color: '#F9FAFB', // Dark mode: gray-50
        }
      }}
    />
  );
};

// Dark mode input styling with NativeWind 4.1
const renderComposer = (props) => {
  return (
    <Composer
      {...props}
      textInputStyle={{
        backgroundColor: '#F9FAFB', // Light mode
        // Dark mode handled by NativeWind classes
      }}
      className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-gray-900 dark:text-gray-50"
    />
  );
};
```

## Related Documentation
- [Button Components](./buttons.md) - Send button and helper buttons
- [Form Components](./forms.md) - Text input specifications 
- [Color Tokens](../tokens/colors.md) - Chat bubble colors
- [Animation Tokens](../tokens/animations.md) - Message and typing animations
- [NativeBase Integration](../style-guide.md) - Theme configuration
- [NativeWind 4.1 Utilities](../style-guide.md) - Utility class patterns

## Migration Notes

### From Custom Chat to Gifted Chat
- **Reliability**: Gifted Chat handles edge cases and platform differences
- **Maintenance**: Reduces custom code maintenance burden
- **Features**: Built-in features like message status, timestamps, and actions
- **Performance**: Optimized virtualization and memory management
- **Accessibility**: Comprehensive screen reader and keyboard support

### Breaking Changes
- Custom message components need to be adapted to GiftedChat render props
- Message data structure follows GiftedChat format
- Animation timings may need adjustment for GiftedChat lifecycle

## Last Updated
*Version 2.0.0 - 2025-08-30*
*Status: Migrated to React Native Gifted Chat with NativeBase and NativeWind 4.1*