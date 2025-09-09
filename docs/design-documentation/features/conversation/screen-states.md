# Conversation Feature - Screen States

---
title: Conversation Feature Screen States and Visual Specifications
description: Complete screen-by-screen visual design specifications for AI conversation interface
feature: conversation
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - interactions.md
  - accessibility.md
  - implementation.md
  - ../../design-system/components/chat-bubbles.md
  - ../../design-system/components/forms.md
  - ../../design-system/components/navigation.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/components/buttons.md
dependencies:
  - design-system/components
  - chat bubble components
  - pre-conversation-context feature
status: approved
---

## Screen States Overview

The conversation feature includes 7 primary screen states that create an immersive, extremely human-like AI conversation experience. Each state prioritizes natural dialogue flow with AI partners that fully embody their personas, strictly adhere to location context and difficulty levels, and respond with authentic human conversation patterns including realistic message length variation.

## Table of Contents

1. [Conversation Interface States](#conversation-interface-states)
2. [Input and Response States](#input-and-response-states)
3. [Guidance and Coaching States](#guidance-and-coaching-states)
4. [Progress and Timing States](#progress-and-timing-states)
5. [Error and Recovery States](#error-and-recovery-states)

---

## Conversation Interface States

### Purpose
Create an immersive chat environment that feels authentically human, where AI partners demonstrate complete persona embodiment, context awareness, and realistic conversation patterns while providing subtle coaching and encouragement.

### Layout Structure
- **Container**: Full screen chat interface with message history
- **Grid**: Chat bubbles with user input at bottom, subtle UI controls
- **Spacing**: Natural message spacing with time-based bubble grouping

---

### State: Active Conversation

#### Visual Design Specifications

**Chat Interface Layout**:
- **Message Area**: Scrollable container for conversation history (80% of screen)
- **Input Area**: Fixed bottom area with text input and send button (20% of screen)
- **Header**: Minimal header with AI partner info, timer, and context reminder
- **Background**: Subtle gradient or texture that doesn't compete with text

**Message Bubble System** (References design-system/components/chat-bubbles.md):
- **User Messages**: Right-aligned, Primary-500 background, white text
- **AI Messages**: Left-aligned, Neutral-100 background, dark text
- **System Messages**: Center-aligned, subtle styling for coaching tips
- **Bubble Spacing**: 8px between messages, 16px between different speakers

**AI Partner Display**:
- **Avatar**: Circular avatar representing AI personality (not photos)
- **Name**: Contextual name like "Practice Partner" or scenario-appropriate
- **Status**: Subtle "typing" indicator when AI is responding
- **Context Reminder**: Expandable reminder of current scenario context

**Header Elements**:
- **Scenario Info**: Brief scenario reminder (e.g., "Coffee shop conversation")
- **Timer**: Conversation time remaining (12-minute limit)
- **Progress**: Message count indicator (subtle, not prominent)
- **Exit Option**: Discrete "end conversation" option

#### Message Styling Specifications

**User Message Bubbles**:
- **Background**: Primary-500 (#F97316)
- **Text Color**: White (#FFFFFF)
- **Border Radius**: 18px (top-left), 18px (top-right), 6px (bottom-right), 18px (bottom-left)
- **Padding**: 12px horizontal, 8px vertical
- **Max Width**: 80% of screen width
- **Shadow**: Subtle shadow for depth

**AI Message Bubbles**:
- **Background**: Neutral-100 (#F3F4F6)
- **Text Color**: Neutral-900 (#111827)
- **Border Radius**: 6px (top-left), 18px (top-right), 18px (bottom-right), 18px (bottom-left)
- **Padding**: 12px horizontal, 8px vertical
- **Max Width**: 85% of screen width (slightly wider for AI responses)
- **Border**: 1px subtle border in Neutral-200

**System/Coaching Messages**:
- **Background**: Success-50 (#ECFDF5)
- **Text Color**: Success-700 (#047857)
- **Border Radius**: 12px all corners
- **Padding**: 8px horizontal, 6px vertical
- **Max Width**: 90% of screen width
- **Style**: Italic text with coaching icon

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Message Width**: Max 280px for readability
- **Input Area**: 60px height with padding
- **Font Size**: 16px for messages, 14px for metadata
- **Touch Targets**: 44px minimum for all interactive elements

**Tablet (768-1023px)**:
- **Message Width**: Max 400px for comfortable reading
- **Input Area**: 64px height with enhanced padding
- **Font Size**: 17px for messages, 15px for metadata
- **Layout**: Centered conversation with max 600px width

**Desktop (1024px+)**:
- **Message Width**: Max 500px for optimal reading
- **Input Area**: 72px height with spacious padding
- **Font Size**: 18px for messages, 16px for metadata
- **Layout**: Centered with sidebar for context (if space allows)

---

### State: Conversation Startup

#### Visual Design Specifications

**Startup Animation Sequence**:
- **Context Reminder**: Brief overlay showing scenario details
- **AI Introduction**: AI partner introduces themselves based on context
- **Conversation Starter**: AI provides natural opening based on scenario
- **Input Activation**: Smooth transition to user input readiness

**AI Introduction Message**:
- **Content**: Contextual greeting based on scenario and AI personality
- **Examples**:
  - Coffee shop: "Hi! I'm here getting my usual latte. This place is always so cozy."
  - Bookstore: "Excuse me, have you read anything good lately? I'm looking for recommendations."
  - Gym: "Is this machine free? I haven't seen you here before."
- **Styling**: Uses AI message bubble with gentle entrance animation

**First Message Guidance**:
- **Subtle Prompt**: Light suggestion overlay on input field
- **Examples**: "Try responding naturally..." or "What would you say?"
- **Dismissal**: Fades away after 3 seconds or when user starts typing
- **Color**: Neutral-500 text, very subtle appearance

---

### State: Conversation in Progress

#### Visual Design Specifications

**Message Flow Visualization**:
- **Chronological Order**: Messages appear in time order with smooth animations
- **Message Grouping**: Messages from same speaker group together with reduced spacing
- **Time Stamps**: Subtle timestamps for message groups (every 2-3 messages)
- **Read Indicators**: Subtle "seen" indicators for user messages

**Conversation Momentum Indicators**:
- **Response Time**: AI responds with natural delay (1-3 seconds)
- **Typing Indicator**: "..." animation when AI is composing response
- **Flow Feedback**: Subtle color changes in input area based on conversation quality
- **Engagement Level**: Background subtle color shifts based on conversation success

**Quality Indicators** (Subtle):
- **Good Flow**: Input area has subtle Success-100 background
- **Awkward Moment**: Input area has subtle Warning-50 background
- **Great Response**: Subtle positive animation on message send
- **Missed Opportunity**: Gentle system message with encouragement

#### Message Enhancement Features

**User Message Enhancements**:
- **Send Animation**: Smooth slide animation from input to message area
- **Confidence Indicator**: Subtle visual feedback on message tone/style
- **Edit Option**: Brief window to edit/recall message (3-second window)
- **Response Preview**: Very subtle preview of likely AI response types

**AI Message Enhancements**:
- **Personality Consistency**: Visual cues that maintain AI personality
- **Emotional Tone**: Subtle emoji or color variations based on AI mood
- **Context Awareness**: References to earlier conversation points
- **Natural Delays**: Realistic typing and response times

---

## Input and Response States

### Purpose
Provide intuitive input mechanisms with helpful guidance and error prevention.

---

### State: Text Input Active

#### Visual Design Specifications

**Input Field Design**:
- **Field Style**: Clean, modern text input with subtle border
- **Placeholder**: Context-appropriate placeholder text
- **Character Limit**: 280 characters with subtle counter
- **Background**: White with Neutral-200 border, Primary-500 focus border
- **Height**: Auto-expanding up to 4 lines of text

**Send Button Integration**:
- **Position**: Right side of input field
- **State Changes**: Disabled (gray) → Ready (primary) → Sending (loading)
- **Icon**: Send arrow icon, 20px size
- **Animation**: Smooth state transitions with micro-interactions
- **Size**: 44×44px touch target

**Input Enhancement Features**:
- **Smart Suggestions**: Contextual response suggestions (optional)
- **Grammar Check**: Subtle underlining for obvious errors
- **Confidence Coaching**: Gentle encouragement for shy users
- **Voice Input**: Microphone icon for voice-to-text (platform dependent)

#### Input State Variations

**Empty State**:
- **Placeholder**: "What would you say?" or scenario-specific prompt
- **Send Button**: Disabled state with reduced opacity
- **Border**: Neutral-200 color
- **Background**: Pure white

**Typing State**:
- **Border**: Animated to Primary-500 color
- **Character Counter**: Appears when approaching limit (200+ characters)
- **Send Button**: Activates with Primary-500 background
- **Auto-Height**: Expands smoothly as user types

**Error State**:
- **Border**: Error-500 color with subtle animation
- **Error Message**: Helpful error text below input
- **Send Button**: Disabled state
- **Recovery**: Clear path to resolve error

---

### State: AI Response Generation

#### Visual Design Specifications

**Typing Indicator**:
- **Animation**: Three dots with sequential opacity animation
- **Position**: AI message bubble position
- **Timing**: 1-3 second duration based on response complexity
- **Style**: Same styling as AI messages but with animation

**Response Composition Feedback**:
- **Quality Indicator**: Subtle background animation while AI "thinks"
- **Context Integration**: Visual hint that AI is considering conversation context
- **Personality Consistency**: Indicator that response matches AI personality
- **Natural Timing**: Realistic delays based on message complexity

**Response Delivery**:
- **Animation**: Smooth transition from typing to message
- **Reading Pace**: Messages appear at natural reading speed
- **Character Entrance**: Text animates in naturally (not typewriter effect)
- **Completion**: Subtle audio or visual cue when message complete

---

## Guidance and Coaching States

### Purpose
Provide subtle coaching and encouragement without interrupting conversation flow.

---

### State: Real-time Coaching

#### Visual Design Specifications

**Coaching Message Integration**:
- **Appearance**: Distinct styling from conversation messages
- **Timing**: Appears during natural conversation pauses
- **Content**: Positive reinforcement and gentle suggestions
- **Dismissal**: Auto-fades after reading time or user interaction

**Coaching Message Types**:

**Encouragement Messages**:
- **Background**: Success-50 (#ECFDF5)
- **Icon**: Thumbs up or star icon in Success-500
- **Text**: "Great conversation starter!" or "Nice follow-up question!"
- **Position**: Center-aligned between message groups

**Suggestion Messages**:
- **Background**: Primary-50 (#FFF7ED)
- **Icon**: Lightbulb icon in Primary-500
- **Text**: "Try asking about their interests" or "Share something about yourself"
- **Position**: Floating overlay that doesn't interrupt flow

**Progress Messages**:
- **Background**: Info-50 (#EFF6FF)
- **Icon**: Progress or trophy icon in Info-500
- **Text**: "You're building great rapport!" or "Halfway through - you're doing great!"
- **Position**: Subtle banner at top of screen

#### Coaching Timing and Triggers

**Positive Reinforcement Triggers**:
- User asks open-ended question
- User shows empathy or active listening
- User maintains conversation flow naturally
- User demonstrates confidence in response

**Gentle Guidance Triggers**:
- Conversation stalls for 10+ seconds
- User seems uncertain (multiple deletes/edits)
- Missed opportunity for follow-up question
- Conversation becoming one-sided

**Progress Celebration Triggers**:
- Reaching conversation milestones (5, 10, 15 messages)
- Particularly engaging conversation moments
- Successful topic transitions
- Maintaining conversation for time milestones

---

### State: Conversation Starters Aid

#### Visual Design Specifications

**Starter Suggestions Interface**:
- **Trigger**: Appears if user seems stuck (30+ seconds no input)
- **Layout**: Floating card with 2-3 conversation starter options
- **Styling**: Card-style overlay with subtle shadow
- **Interaction**: Tap to use suggestion or dismiss

**Suggestion Categories**:
- **Questions**: "What brings you here today?"
- **Observations**: "This place has such a nice atmosphere"
- **Compliments**: "I love your style" (context-appropriate)
- **Sharing**: "I'm new to this area, any recommendations?"

**Implementation Details**:
- **Context Awareness**: Suggestions match current scenario
- **Personality Matching**: Aligned with user's conversation style so far
- **Progressive Difficulty**: Suggestions match scenario difficulty level
- **Natural Integration**: Suggestions that fit conversation flow

---

## Progress and Timing States

### Purpose
Keep users informed of conversation progress without creating pressure.

---

### State: Time Management Display

#### Visual Design Specifications

**Timer Integration**:
- **Position**: Subtle indicator in header, not prominently displayed
- **Format**: "8:32 left" or progress bar format
- **Color Coding**: 
  - Green (10+ minutes): Success-500
  - Yellow (5-10 minutes): Warning-500
  - Orange (2-5 minutes): Primary-500
  - Red (0-2 minutes): Error-500

**Time Warning System**:
- **5 Minutes Left**: Subtle notification, "5 minutes remaining"
- **2 Minutes Left**: Gentle reminder, "Conversation wrapping up soon"
- **1 Minute Left**: Final notice, "Last minute - great conversation!"
- **Time Up**: Smooth transition to conclusion

**Progress Without Pressure**:
- **Message Count**: Very subtle indicator (not competitive)
- **Quality Over Quantity**: Focus on conversation quality, not message count
- **Natural Conclusion**: Encouraging progression toward natural ending
- **Extension Option**: For engaging conversations, subtle "continue" option

---

### State: Message Limit Approach

#### Visual Design Specifications

**Approaching Limit (40+ messages)**:
- **Subtle Indicator**: Gentle indication in header
- **Coaching Message**: "You're having a great conversation!"
- **Natural Wrap**: Suggestion to start concluding naturally
- **No Pressure**: Emphasis on quality over quantity

**Limit Reached (50 messages)**:
- **Gentle Conclusion**: "What a wonderful conversation!"
- **Transition Preview**: "Ready to see how you did?"
- **Achievement Focus**: Celebrate the conversation completion
- **Smooth Exit**: Natural transition to feedback screen

---

## Error and Recovery States

### Purpose
Handle technical and conversational errors gracefully while maintaining user confidence.

---

### State: Network Connection Issues

#### Visual Design Specifications

**Connection Lost Indicator**:
- **Banner**: Subtle top banner with connection status
- **Message**: "Connection lost - your conversation is saved"
- **Color**: Warning-100 background, Warning-700 text
- **Icon**: WiFi-off icon in Warning-500
- **Retry**: "Tap to reconnect" button

**Message Queue Management**:
- **Pending Messages**: Clear indication of unsent messages
- **Queue Display**: "Sending..." indicator for queued messages
- **Conflict Resolution**: Handle message order when reconnecting
- **Data Protection**: Assurance that conversation progress is saved

**Recovery Process**:
- **Auto-Retry**: Automatic reconnection attempts
- **Manual Retry**: User-triggered reconnection option
- **Graceful Degradation**: Limited functionality during connection issues
- **Status Updates**: Clear communication of connection status

---

### State: AI Response Errors

#### Visual Design Specifications

**AI Unavailable**:
- **Message**: AI bubble with "I'm having trouble responding right now"
- **Suggestion**: "Let's try that again" or "Can you rephrase?"
- **Styling**: Error state bubble with different color scheme
- **Recovery**: Easy retry mechanism

**Inappropriate Content Detection**:
- **Gentle Redirect**: "Let's keep our conversation friendly"
- **Guidance**: Suggestion for more appropriate response
- **Educational**: Brief explanation without shaming
- **Recovery**: Clear path to continue conversation appropriately

**Context Loss**:
- **AI Confusion**: "I lost track of our conversation"
- **Context Restore**: Brief summary of conversation so far
- **Smooth Continuation**: Seamless return to natural flow
- **Prevention**: Better context preservation in future

---

### State: User Input Errors

#### Visual Design Specifications

**Empty Message Error**:
- **Subtle Indication**: Input field briefly highlights
- **No Harsh Error**: Gentle visual cue without error text
- **Guidance**: Placeholder text reminder
- **Recovery**: Immediate return to normal state

**Message Too Long**:
- **Character Counter**: Red color when over limit
- **Helpful Guidance**: "Try breaking that into two messages"
- **Truncation Option**: "Send first part now" button
- **Recovery**: Easy editing to reduce length

**Repeated Messages**:
- **Gentle Notice**: "You just sent something similar"
- **Confirmation**: "Send anyway?" option
- **Suggestion**: Alternative phrasing suggestion
- **Prevention**: Smart detection without being intrusive

---

## Accessibility Specifications

### Screen Reader Experience

**Message Navigation**:
- **Logical Order**: Messages announced in chronological order
- **Speaker Identification**: Clear "You said" vs "AI said" announcements
- **Message Content**: Full message content read naturally
- **Metadata**: Time stamps and status information when relevant

**Input Accessibility**:
- **Field Labels**: Clear "Message input" label
- **Character Limits**: Count announced periodically
- **Send Button**: "Send message" label with current state
- **Error States**: Clear error announcements and recovery guidance

### Keyboard Navigation

**Tab Order**:
- **Input Field**: Primary focus target
- **Send Button**: Secondary focus target
- **Menu Options**: Settings, end conversation accessible
- **Message History**: Scrollable with keyboard for review

**Keyboard Shortcuts**:
- **Enter**: Send message (with Shift+Enter for new line)
- **Escape**: Show end conversation dialog
- **Up Arrow**: Edit last message (brief window)
- **Alt+R**: Retry last action

### Motor Accessibility

**Touch Targets**:
- **Minimum Size**: 44×44px for all interactive elements
- **Send Button**: Enhanced 48×48px for critical action
- **Message Bubbles**: Long press for additional options
- **Input Field**: Large, easy-to-target area

**Alternative Input**:
- **Voice Input**: Microphone integration where available
- **Switch Control**: Compatible with iOS/Android switch control
- **Gesture Alternatives**: All gestures have button/tap alternatives

## Performance Specifications

### Rendering Performance
- **Message Rendering**: <100ms for new message appearance
- **Scroll Performance**: 60fps during conversation review
- **Animation Performance**: Smooth micro-interactions throughout
- **Memory Management**: Efficient handling of long conversations

### Network Optimization
- **Message Sending**: <2s for typical message transmission
- **AI Response**: <3s for AI response generation
- **Offline Queuing**: Local storage for messages during connection issues
- **Conflict Resolution**: Smart handling of message order and timing

## Implementation Notes

### Component Usage
- **Chat Bubbles**: Standard chat bubble components from design system
- **Input Components**: Form input components with chat-specific styling
- **Buttons**: Standard button variants for send and action buttons
- **Cards**: Coaching and guidance messages use card components

### State Management
- **Real-time Updates**: WebSocket or similar for live conversation
- **Message Queue**: Local queue management for offline functionality
- **Conversation State**: Persistent storage of conversation progress
- **Error Recovery**: Robust error handling and recovery mechanisms

### Analytics Integration
- **Message Timing**: Track response times and conversation flow
- **Quality Metrics**: Monitor conversation engagement and success
- **Error Tracking**: Log and analyze error rates and types
- **User Behavior**: Understand interaction patterns and preferences

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete conversation flow and decision points
- **[Interactions](./interactions.md)** - Animation and interaction specifications
- **[Accessibility](./accessibility.md)** - Complete accessibility implementation
- **[Implementation](./implementation.md)** - Technical specifications and handoff
- **[Chat Bubbles](../../design-system/components/chat-bubbles.md)** - Chat bubble specifications

## Last Updated
- **Version 1.0.0**: Complete screen state specifications with accessibility and real-time features
- **Focus**: Natural conversation flow with subtle coaching and guidance
- **Next**: Technical implementation with real-time messaging and AI integration