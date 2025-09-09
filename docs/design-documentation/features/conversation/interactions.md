---
title: Conversation Feature Interaction Specifications
description: Comprehensive interaction patterns, animations, and micro-interactions for the conversation experience
feature: conversation
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ../../design-system/tokens/animations.md
dependencies:
  - React Native Reanimated 3.x
  - React Native Gesture Handler
  - Expo Haptics
status: approved
---

# Conversation Feature Interaction Specifications

## Overview
This document defines all interaction patterns, animations, and micro-interactions for the conversation feature, ensuring smooth, responsive, and delightful user experiences across all human-like AI conversation flows. The AI partners demonstrate authentic persona embodiment with natural conversation rhythms and realistic message length variation.

## Table of Contents
1. [Message Send Animations](#message-send-animations)
2. [Typing Indicator Behaviors](#typing-indicator-behaviors)
3. [Scroll Interactions](#scroll-interactions)
4. [Pull-to-Refresh Patterns](#pull-to-refresh-patterns)
5. [Timer and Counter Animations](#timer-and-counter-animations)
6. [End Conversation Interactions](#end-conversation-interactions)
7. [Micro-interactions](#micro-interactions)
8. [Gesture Handling](#gesture-handling)

## Message Send Animations

### Send Button Interaction
**Component**: Message Send Button  
**States**: Default, Pressed, Sending, Sent, Error

#### Default to Pressed
```javascript
// Animation specifications
duration: 150ms
easing: cubic-bezier(0.4, 0, 0.6, 1)
transform: scale(0.95)
backgroundColor: primary-600 → primary-700
```

**Visual Changes:**
- Scale: 100% → 95%
- Background: Orange 500 (#F97316) → Orange 600 (#EA580C)
- Haptic Feedback: Light impact (iOS) / Short vibration (Android)

#### Pressed to Sending
```javascript
// Animation specifications
duration: 300ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
transform: scale(0.95) → scale(1.05) → scale(1.0)
```

**Visual Changes:**
- Icon transition: Send icon → Loading spinner
- Spinner animation: 360° rotation, infinite, 1200ms duration
- Background: Maintains orange 600 color
- Button disabled state active

#### Sending to Sent (Success)
```javascript
// Animation specifications
duration: 500ms
easing: cubic-bezier(0.0, 0, 0.2, 1)
```

**Visual Changes:**
- Spinner → Checkmark icon (200ms fade)
- Checkmark scale animation: 0 → 1.2 → 1.0
- Background: Orange 600 → Success 500 (#22C55E)
- Auto-reset to default after 800ms

#### Sending to Error
```javascript
// Animation specifications
duration: 400ms
easing: cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

**Visual Changes:**
- Spinner → Error icon with shake animation
- Shake: translateX(-4px, 4px, -2px, 2px, 0)
- Background: Orange 600 → Error 500 (#EF4444)
- Manual reset required via user tap

### Message Bubble Animation
**Component**: Message Bubble  
**Trigger**: Message send success

#### Entry Animation (User Messages)
```javascript
// From bottom-right, scaling up
duration: 400ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
initialTransform: {
  translateY: 20,
  translateX: 10,
  scale: 0.8,
  opacity: 0
}
finalTransform: {
  translateY: 0,
  translateX: 0,
  scale: 1,
  opacity: 1
}
```

#### Entry Animation (AI Messages)
```javascript
// From bottom-left, scaling up
duration: 400ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
initialTransform: {
  translateY: 20,
  translateX: -10,
  scale: 0.8,
  opacity: 0
}
finalTransform: {
  translateY: 0,
  translateX: 0,
  scale: 1,
  opacity: 1
}
```

#### Sequence Timing
1. **Message Send**: Button animation starts
2. **Optimistic Update**: User message appears immediately (300ms after send)
3. **AI Response Delay**: Typing indicator appears (800ms after user message)
4. **AI Message**: Response bubble appears (realistic delay, 2-5 seconds)

## Typing Indicator Behaviors

### Typing Indicator Animation
**Component**: Three-dot typing indicator  
**Pattern**: Wave animation with staggered dots

```javascript
// Dot animation specifications
dot1: {
  delay: 0ms,
  duration: 1200ms,
  easing: 'ease-in-out',
  transform: 'translateY(-8px) → translateY(0px)'
}
dot2: {
  delay: 200ms,
  duration: 1200ms,
  easing: 'ease-in-out',
  transform: 'translateY(-8px) → translateY(0px)'
}
dot3: {
  delay: 400ms,
  duration: 1200ms,
  easing: 'ease-in-out',
  transform: 'translateY(-8px) → translateY(0px)'
}
```

**Visual Specifications:**
- Dot size: 4px diameter
- Dot color: Secondary 400 (#94A3B8)
- Dot spacing: 4px between centers
- Container padding: 12px horizontal, 8px vertical
- Container background: Secondary 100 (#F1F5F9)
- Container border radius: 16px

### Typing Indicator States

#### Appear Animation
```javascript
duration: 300ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
initialState: {
  opacity: 0,
  scale: 0.8,
  translateY: 10
}
finalState: {
  opacity: 1,
  scale: 1,
  translateY: 0
}
```

#### Disappear Animation
```javascript
duration: 200ms
easing: cubic-bezier(0.4, 0, 1, 1)
finalState: {
  opacity: 0,
  scale: 0.9,
  translateY: -5
}
```

#### Typing Duration Logic
```javascript
// Dynamic typing duration based on response length
baseDelay: 1500ms
characterMultiplier: 50ms // per character
maxDelay: 5000ms
minDelay: 2000ms

calculateTypingDelay = (responseLength) => {
  const calculatedDelay = baseDelay + (responseLength * characterMultiplier)
  return Math.min(Math.max(calculatedDelay, minDelay), maxDelay)
}
```

## Scroll Interactions

### Auto-scroll Behavior
**Trigger**: New message received or sent  
**Behavior**: Smooth scroll to bottom

```javascript
// Scroll animation specifications
duration: 400ms
easing: cubic-bezier(0.25, 0.46, 0.45, 0.94)
behavior: 'smooth'
```

**Implementation Logic:**
```javascript
// Auto-scroll conditions
shouldAutoScroll = () => {
  const scrollThreshold = 100 // pixels from bottom
  const currentScrollBottom = scrollHeight - scrollTop - clientHeight
  return currentScrollBottom <= scrollThreshold
}

// Scroll with momentum preservation
scrollToBottom = (animated = true) => {
  if (shouldAutoScroll()) {
    scrollView.scrollToEnd({ animated, duration: 400 })
  }
}
```

### Manual Scroll Interactions
**Component**: Message list scroll view

#### Scroll Momentum
```javascript
// React Native ScrollView props
decelerationRate: 0.95 // iOS
decelerationRate: 0.985 // Android
showsVerticalScrollIndicator: false
overScrollMode: 'never' // Android
bounces: true // iOS
bouncesZoom: false // iOS
```

#### Scroll-to-top Gesture
**Trigger**: Status bar tap (iOS) / ScrollView top tap  
**Animation**: Smooth scroll to conversation start

```javascript
duration: 600ms
easing: cubic-bezier(0.25, 0.46, 0.45, 0.94)
```

### Scroll Position Memory
**Feature**: Maintain scroll position during state updates

```javascript
// Scroll position preservation
maintainScrollPosition = () => {
  const scrollOffset = getScrollOffset()
  const contentHeight = getContentHeight()
  
  // Restore position after render
  requestAnimationFrame(() => {
    if (scrollOffset > 0) {
      scrollToOffset(scrollOffset, false)
    }
  })
}
```

## Pull-to-Refresh Patterns

### Pull-to-Refresh Animation
**Component**: Conversation history refresh  
**Pattern**: Custom pull-to-refresh with orange branding

#### Pull Phase
```javascript
// Pull distance thresholds
activationThreshold: 60px
maxPullDistance: 120px

// Visual feedback during pull
pullProgress = pullDistance / activationThreshold
opacity: Math.min(pullProgress, 1)
rotation: pullProgress * 180 // degrees
scale: 0.8 + (pullProgress * 0.2)
```

#### Release Animation
```javascript
// Snap back to refresh position
duration: 250ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
```

#### Refresh Active State
```javascript
// Loading spinner animation
duration: 1200ms
easing: 'linear'
rotation: 360 // degrees
iterations: 'infinite'
```

**Visual Specifications:**
- Pull indicator: Orange circular progress (Primary 500 #F97316)
- Background: Secondary 50 (#F8FAFC)
- Icon: Refresh arrow, 20px size
- Text: "Pull to refresh conversation" → "Release to refresh"

### Refresh Content Logic
```javascript
// Refresh actions
refreshActions = [
  'fetchOlderMessages', // Load conversation history
  'syncMessageStatus', // Update delivery/read status
  'refreshUserProfile', // Update AI persona if changed
  'cleanupLocalCache' // Clear temporary message data
]

// Refresh completion
refreshDuration = 1500ms // Minimum loading time
maxRefreshTime = 5000ms // Timeout threshold
```

## Timer and Counter Animations

### Conversation Timer Display
**Component**: Active conversation timer  
**Location**: Header/status area

#### Timer Format Animation
```javascript
// Time format transitions
shortFormat: "5:23" // under 10 minutes
mediumFormat: "15:42" // under 1 hour  
longFormat: "1:23:45" // over 1 hour

// Format transition animation
duration: 200ms
easing: 'ease-out'
```

#### Timer Color Progression
```javascript
// Color changes based on remaining time
timeRemaining > 600s: Secondary 600 (#475569) // Normal
300s < timeRemaining <= 600s: Warning 500 (#F59E0B) // Warning
timeRemaining <= 300s: Error 500 (#EF4444) // Critical

// Color transition
duration: 300ms
easing: 'ease-in-out'
```

#### Pulse Animation (Critical Time)
```javascript
// When < 60 seconds remaining
duration: 1000ms
easing: 'ease-in-out'
scale: 1.0 → 1.05 → 1.0
opacity: 1.0 → 0.8 → 1.0
iterations: 'infinite'
```

### Message Count Animation
**Component**: Message counter (if applicable)  
**Trigger**: New message sent/received

#### Count Update Animation
```javascript
// Number change animation
duration: 300ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)

// Sequence
phase1: scale(1.0 → 1.15) // 150ms
phase2: scale(1.15 → 1.0) // 150ms
```

#### Milestone Celebrations
```javascript
// Special animations for message milestones (10, 25, 50, 100)
duration: 800ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)

// Celebration effect
particles: true
color: Primary 500 (#F97316)
hapticFeedback: 'medium' // iOS: .medium, Android: 100ms
```

## End Conversation Interactions

### End Conversation Button
**Component**: End/Leave conversation button  
**States**: Default, Warning, Confirming, Ending

#### Warning State Transition
```javascript
// Color transition to warning
duration: 300ms
easing: 'ease-out'
backgroundColor: Secondary 200 → Warning 100
borderColor: Secondary 300 → Warning 300
textColor: Secondary 700 → Warning 700
```

#### Confirmation Modal
**Animation**: Modal slide-up from bottom

```javascript
// Modal appearance
duration: 400ms
easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
initialTransform: {
  translateY: '100%',
  opacity: 0
}
finalTransform: {
  translateY: 0,
  opacity: 1
}
```

#### End Action Animation
```javascript
// Ending in progress
duration: 500ms
easing: 'ease-out'

// Visual sequence
phase1: Button text → "Ending..." (100ms)
phase2: Loading spinner appears (200ms)
phase3: Screen transition preparation (200ms)
```

### Conversation Exit Transition
**Pattern**: Fade out conversation, slide to results

#### Exit Animation Sequence
```javascript
// Step 1: Message fade out (staggered)
messagesFadeOut: {
  duration: 400ms,
  easing: 'ease-in',
  stagger: 50ms, // each message 50ms after previous
  direction: 'bottom-to-top'
}

// Step 2: UI elements fade
interfaceFadeOut: {
  duration: 200ms,
  easing: 'ease-in',
  delay: 200ms // after messages start fading
}

// Step 3: Transition to next screen
screenTransition: {
  duration: 300ms,
  easing: cubic-bezier(0.25, 0.46, 0.45, 0.94),
  delay: 400ms
}
```

## Micro-interactions

### Haptic Feedback Patterns
**Platform Integration**: iOS Haptic Feedback / Android Vibration

```javascript
// Haptic feedback mapping
interactions: {
  messageSend: 'light', // Successful send
  messageReceive: 'soft', // New message arrival
  buttonPress: 'light', // General button presses
  errorOccurred: 'error', // Error states
  timerWarning: 'warning', // Time running low
  conversationEnd: 'success', // Successful completion
  milestone: 'medium' // Message count milestones
}

// iOS Implementation
impactLight: UIImpactFeedbackGenerator.light
impactMedium: UIImpactFeedbackGenerator.medium  
notificationSuccess: UINotificationFeedbackGenerator.success
notificationWarning: UINotificationFeedbackGenerator.warning
notificationError: UINotificationFeedbackGenerator.error

// Android Implementation
vibrationShort: 50ms
vibrationMedium: 100ms
vibrationLong: 200ms
```

### Focus and Selection States
**Pattern**: Visual feedback for interactive elements

#### Button Focus (Accessibility)
```javascript
// Focus indicator animation
duration: 150ms
easing: 'ease-out'
borderWidth: 0 → 2px
borderColor: Primary 500 (#F97316)
shadowRadius: 0 → 4px
shadowColor: Primary 500 at 0.3 opacity
```

#### Text Selection
```javascript
// Text selection highlight
backgroundColor: Primary 100 (#FFEDD5)
borderRadius: 4px
padding: 2px 4px
```

### Loading States
**Pattern**: Skeleton screens and progressive loading

#### Message Skeleton
```javascript
// Skeleton animation
duration: 1500ms
easing: 'ease-in-out'
iterations: 'infinite'

// Shimmer effect
gradientAnimation: {
  start: { x: -1, y: 0 },
  end: { x: 2, y: 0 },
  colors: ['transparent', 'rgba(255,255,255,0.5)', 'transparent']
}
```

## Gesture Handling

### Swipe Gestures
**Implementation**: React Native Gesture Handler

#### Message Bubble Swipe
**Purpose**: Quick actions (reply, react)  
**Direction**: Left swipe on message

```javascript
// Swipe detection
activationDistance: 60px
maxSwipeDistance: 120px

// Visual feedback
swipeProgress = swipeDistance / activationDistance
actionOpacity: Math.min(swipeProgress, 1)
messageTranslateX: Math.min(swipeDistance, maxSwipeDistance)
```

#### Conversation Navigation
**Purpose**: Navigate between conversations  
**Direction**: Horizontal swipes on conversation area

```javascript
// Swipe thresholds
activationVelocity: 500 // pixels/second
activationDistance: 100px
snapBackDistance: 50px

// Visual preview
previewScale: 0.9
previewOpacity: 0.7
```

### Long Press Interactions
**Pattern**: Context menus and additional actions

#### Message Long Press
```javascript
// Long press detection
minimumPressDuration: 500ms
allowableMovement: 10px

// Feedback animation
pressAnimation: {
  duration: 500ms,
  easing: 'ease-out',
  scale: 1.0 → 1.02,
  shadow: elevation 0 → elevation 2
}
```

## Related Documentation
- [Conversation User Journey](user-journey.md)
- [Screen States](screen-states.md)
- [Design System Animation Tokens](../../design-system/tokens/animations.md)
- [Component Specifications](../../design-system/components/)

## Implementation Notes
All animations are implemented using React Native Reanimated 3.x for optimal performance. Haptic feedback respects user system preferences and accessibility settings. All gesture interactions include keyboard navigation alternatives for accessibility compliance.

## Last Updated
**Version 1.0.0** - Initial interaction specifications  
**Next Review:** October 23, 2025  
**Responsible Team:** UX Design & Frontend Development