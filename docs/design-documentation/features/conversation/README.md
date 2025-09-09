# Conversation Interface Design

---
title: FlirtCraft Conversation Interface
description: Real-time chat interface with AI partner design specifications  
feature: conversation
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./user-journey.md
  - ./screen-states.md
  - ./interactions.md
  - ../pre-conversation/README.md
  - ../feedback/README.md
dependencies:
  - AI conversation engine
  - Pre-conversation context system
  - Real-time messaging infrastructure
status: approved
---

## Overview

The conversation interface is the core value-delivery mechanism of FlirtCraft, where users practice romantic conversation skills with AI partners in realistic scenarios. The design prioritizes psychological safety, clear communication, and confidence building through supportive interaction patterns.

## Design Goals

### Primary Objectives
- **Extremely Human-Like Practice**: Interface and AI behavior replicate authentic human conversation patterns
- **Confidence Building**: Every interaction element supports user confidence growth
- **Clear Communication**: Messaging is clear, contextual, and encouraging  
- **Stress Reduction**: Design minimizes performance anxiety while maintaining engagement
- **Authentic Personality**: AI embodies specific, realistic personas with human-like response patterns and natural conversation flow

### Success Metrics
- **Conversation Completion**: >85% of started conversations completed
- **User Engagement**: Average 12-15 messages per conversation
- **Response Quality**: <5% negative feedback on AI response appropriateness
- **Confidence Impact**: 40%+ users report feeling more confident after conversations
- **Technical Performance**: <2 second AI response time, 60fps animations

## Core Interface Components

### Chat Message Display

#### User Messages
**Visual Design:**
- **Background**: Primary gradient (`#F97316` to `#EA580C`)
- **Text Color**: White (`#FFFFFF`)
- **Alignment**: Right-aligned with appropriate margins
- **Border Radius**: `16px 16px 4px 16px` (speech bubble effect)
- **Padding**: `12px 16px` for comfortable text spacing
- **Typography**: Body (16px/22px) for optimal readability
- **Max Width**: 80% of screen width to maintain conversation flow
- **Shadow**: Subtle drop shadow for elevation

#### AI Partner Messages  
**Visual Design:**
- **Background**: White (`#FFFFFF`) with subtle border
- **Text Color**: Dark gray (`#374151`) for high contrast
- **Alignment**: Left-aligned with consistent spacing
- **Border Radius**: `16px 16px 16px 4px` (opposite bubble direction)
- **Border**: `1px solid #E5E7EB` for definition
- **Padding**: `12px 16px` matching user messages
- **Typography**: Body (16px/22px) consistent with user text
- **Max Width**: 80% of screen width
- **Avatar**: Optional 32px profile image for personalization

### Message Input Interface

#### Text Input Field
**Visual Design:**
- **Height**: 48px minimum for touch accessibility
- **Background**: White (`#FFFFFF`) with subtle border
- **Border**: `2px solid #E5E7EB` default, `#F97316` on focus
- **Border Radius**: `24px` for modern messaging aesthetic
- **Padding**: `12px 20px` with space for send button
- **Typography**: Body (16px/22px) to prevent iOS zoom
- **Placeholder**: Contextual hints based on conversation state

#### Send Button
**Visual Design:**
- **Size**: 40px × 40px circle within input field
- **Position**: Right-aligned inside input field
- **Background**: Primary gradient when text present, disabled gray when empty
- **Icon**: Send arrow (16px) centered in white
- **Animation**: Scale feedback on press, gradient transition on enable

### Context-Aware Features

#### Conversation Starters Panel
**When Displayed:**
- User hasn't sent first message after 30 seconds
- User types and deletes message 3+ times  
- User explicitly requests help via "Need help?" button

**Visual Design:**
- **Slide-up panel**: Appears from bottom with backdrop blur
- **Height**: 40% of screen height with comfortable scrolling
- **Background**: White with rounded top corners (16px)
- **Suggestions**: 3-4 contextual conversation starters based on pre-conversation context
- **Selection**: Tap to insert into input field, user can edit before sending

#### Typing Indicators
**AI Thinking State:**
- **Duration**: 1-3 seconds based on response complexity
- **Visual**: Three animated dots in AI message bubble position
- **Color**: Muted gray (`#9CA3AF`) for subtle presence
- **Animation**: Gentle pulsing with offset timing for natural feel

**User Typing State:**
- **Trigger**: User actively typing in input field
- **Display**: Small "typing..." indicator near AI's last message
- **Purpose**: Maintains conversation realism

### Progress and Navigation

#### Conversation Progress
**Visual Elements:**
- **Message Counter**: Subtle indicator showing "8 of ~15 messages" in header
- **Time Indicator**: Optional elapsed time for users who want structure
- **Progress Bar**: Thin linear progress showing conversation advancement
- **Context**: Persistent access to pre-conversation context via small icon

#### Navigation Controls
**Header Elements:**
- **Back Button**: Left-aligned with confirmation dialog for active conversations
- **Context Button**: Quick access to original scenario context
- **Help Button**: Access to conversation starters and tips
- **Settings**: Audio toggle, conversation speed controls (advanced users)

## Interaction Patterns

### Message Flow Mechanics

#### User Message Sending
1. **Input Validation**: Basic appropriateness check, length validation
2. **Send Animation**: Message slides in from input field to conversation
3. **Status Indication**: Delivered checkmark appears
4. **AI Response Trigger**: Typing indicator appears after brief delay
5. **Response Animation**: AI message slides in from left

#### AI Response Patterns
**Response Timing:**
- **Immediate**: Simple acknowledgments (1-2 seconds)
- **Thoughtful**: Complex responses requiring context (2-4 seconds)  
- **Reactive**: Emotional responses to user content (1-3 seconds)
- **Conversational**: Natural back-and-forth timing variance

**Human-Like Response Characteristics:**
- **Variable Message Length**: Sometimes 1-5 words, sometimes full paragraphs, exactly like real people text
- **Context Mastery**: Full utilization of pre-generated context throughout entire conversation
- **Persona Embodiment**: AI completely understands and embodies their specific character traits and background
- **Location Adherence**: Strict adherence to selected location context and environmental details
- **Difficulty Consistency**: Unwavering commitment to Green/Yellow/Red difficulty level behavior
- **User Awareness**: Complete understanding of user's age, gender, and profile preferences
- **Authentic Reactions**: Responses feel genuinely human, never generic or robotic
- **Natural Pacing**: Realistic conversation rhythm with appropriate pauses and enthusiasm shifts

### Conversation Conclusion

#### Natural Ending Detection
**AI Conversation Wrap-up:**
- Recognizes natural conversation endpoints
- Offers graceful conclusion options
- Maintains positive tone regardless of conversation quality
- Provides transition to feedback screen

#### User-Initiated Ending
**Exit Options:**
- **Continue Button**: Keep conversation going if under message limit
- **Wrap Up**: Ask AI to conclude conversation naturally
- **End Now**: Immediate transition to feedback with confirmation
- **Save & Exit**: Resume conversation later (Phase 2 feature)

## Responsive Design Adaptations

### Mobile Portrait (Primary)
- **Layout**: Standard vertical chat interface
- **Input**: Bottom-fixed input with keyboard handling
- **Messages**: Full-width bubbles with appropriate margins
- **Context**: Slide-over panel for pre-conversation details

### Mobile Landscape
- **Layout**: Optimized for horizontal viewing
- **Input**: Maintains bottom position with adjusted padding
- **Messages**: Adjusted max-width for better text flow
- **Context**: Sidebar panel for easier access

### Tablet Adaptations
- **Layout**: Wider message bubbles with more comfortable margins
- **Input**: Centered with maximum width constraints
- **Context**: Persistent sidebar showing conversation context
- **Navigation**: Enhanced header with more control options

## Accessibility Specifications

### Screen Reader Support
**Message Announcements:**
- New AI messages announced with sender identification
- User messages confirmed as sent
- Typing indicators communicated clearly
- Conversation progress updates announced

**Navigation:**
- Header controls properly labeled and accessible
- Input field labeled with current context
- Message history navigable via screen reader
- Focus management during modal appearances

### Keyboard Navigation
**Input Focus:**
- Input field maintains focus during conversation
- Tab navigation through header controls available
- Keyboard shortcuts for common actions
- Enter key sends messages, Shift+Enter for new lines

### Visual Accessibility
**Contrast and Clarity:**
- All text meets WCAG AA contrast requirements
- Message bubbles clearly distinguishable
- Focus indicators visible and consistent
- Color-independent status indication

## Technical Implementation Notes

### Performance Optimization
**Smooth Scrolling:**
- Virtual list rendering for long conversations
- Smooth scroll to bottom on new messages
- Optimized animations using React Native Reanimated
- Memory management for message history

**Real-time Features:**
- WebSocket connection for AI responses
- Offline message queuing with retry logic
- Progressive loading of conversation history
- Background sync for resumed conversations

### AI Integration
**Context Management:**
- Full conversation context maintained throughout session with complete memory retention
- Pre-conversation context actively utilized and referenced naturally throughout dialogue
- Complete user preference integration (difficulty, goals, age, gender) influencing every response
- Real-time response quality monitoring and human-like adjustment patterns

**Human-Like AI Behavior:**
- **Realistic Message Patterns**: AI varies message length naturally - short reactions, medium responses, longer storytelling
- **Persona Consistency**: AI maintains authentic character personality from context generation through conversation end
- **Environmental Awareness**: AI behaves as if actually present in selected location with appropriate contextual responses
- **Difficulty Adherence**: AI strictly follows selected difficulty level without deviation or inconsistency
- **Age/Gender Sensitivity**: AI responses appropriately calibrated for user's demographic and preference settings
- **Authentic Emotional Range**: AI displays realistic emotional responses, enthusiasm, curiosity, and social cues
- **Natural Conversation Flow**: AI maintains human-like pacing, topic transitions, and conversational reciprocity

### Data Handling
**Message Storage:**
- Local caching for conversation continuity  
- Encrypted storage for privacy protection
- Automatic cleanup of old conversation data
- Export options for user's own messages

## Quality Assurance

### User Testing Protocol
**Conversation Flow Testing:**
- Message sending and receiving functionality
- AI response quality and timing
- Conversation conclusion handling
- Context panel accessibility

**Performance Testing:**
- Message rendering speed
- Keyboard responsiveness
- Animation smoothness
- Memory usage during long conversations

### AI Response Quality
**Content Validation:**
- Appropriate response matching
- Context awareness verification
- Personality consistency checking
- Safety and appropriateness filtering

**User Feedback Integration:**
- Response rating system for AI quality
- User preference learning from interactions
- Conversation quality improvement tracking
- Content flagging and review process

## Design System Integration

### Components Used
- [Chat Bubbles](../../design-system/components/chat-bubbles.md#user-message-bubble) - User and AI message display containers
- [Message Input Field](../../design-system/components/forms.md#chat-input-field) - Text input with send button integration
- [Send Button](../../design-system/components/buttons.md#send-button) - Circular send action within input field
- [Typing Indicators](../../design-system/components/chat-bubbles.md#typing-indicator) - AI thinking animation
- [Conversation Starters Panel](../../design-system/components/modals.md#slide-up-panel) - Help suggestions overlay
- [Navigation Header](../../design-system/components/navigation.md#conversation-header) - Back, context, help, and settings controls
- [Progress Indicator](../../design-system/components/navigation.md#conversation-progress) - Message counter and time display

### Design Tokens
- [Message Colors](../../design-system/tokens/colors.md#message-palette) - User gradient (#F97316 to #EA580C), AI white background
- [Chat Typography](../../design-system/tokens/typography.md#message-text) - 16px/22px body text for optimal mobile readability
- [Message Spacing](../../design-system/tokens/spacing.md#message-spacing) - Bubble padding, margins, and max-width constraints
- [Animation Timing](../../design-system/tokens/animations.md#message-animations) - Send animations, typing indicators, scroll behavior
- [Input Field Colors](../../design-system/tokens/colors.md#form-colors) - Focus states and border treatments

### Interaction Patterns
- [Message Send Animation](../../design-system/tokens/animations.md#message-send) - Message transition from input to conversation
- [Typing Indicator Animation](../../design-system/tokens/animations.md#typing-dots) - Pulsing dots with offset timing
- [Scroll Behavior](../../design-system/tokens/animations.md#smooth-scroll) - Auto-scroll to new messages
- [Keyboard Handling](../../design-system/components/forms.md#keyboard-behavior) - Input field focus and keyboard avoidance
- [Send Button States](../../design-system/components/buttons.md#send-button-states) - Enabled/disabled gradient transitions

### Responsive Adaptations
- [Mobile Portrait](../../design-system/platform-adaptations/ios.md#chat-interface) - Primary vertical chat layout
- [Mobile Landscape](../../design-system/platform-adaptations/android.md#landscape-chat) - Horizontal optimization
- [Tablet Layout](../../design-system/platform-adaptations/web.md#tablet-chat) - Wider bubbles and enhanced headers

---

*The conversation interface represents the core value proposition of FlirtCraft. Every design decision prioritizes user confidence building while maintaining the authenticity needed for effective practice.*