# Unified Selection Feature - Interactions

---
title: Chat Tab - Unified Selection Interaction Patterns and Animations
description: Detailed specifications for animations, gestures, and micro-interactions in the Chat tab unified selection screen
feature: chat-unified-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - accessibility.md
  - implementation.md
dependencies:
  - design-system/tokens/animations.md
  - design-system/components/cards.md
status: approved
---

## Interaction Design Overview

**Tab Location**: Chat Tab

The unified selection screen in the Chat tab prioritizes fluid, intuitive interactions that encourage exploration while providing clear feedback for all user actions. This screen supports location and difficulty selection with small customization options before AI generates randomized context. Every interaction is designed to feel responsive and delightful.

## Core Interaction Patterns

### Location Carousel Interactions

#### Horizontal Scrolling Behavior
**Physics Specifications**:
- **Momentum**: Natural iOS/Android platform momentum behavior
- **Deceleration**: Platform-specific deceleration curves
- **Friction**: Medium friction for controlled scrolling
- **Bounce**: iOS-style bounce at start/end, Android-style edge glow

**Scroll Performance Requirements**:
- **Frame Rate**: Consistent 60fps during all scroll operations
- **Input Latency**: <16ms between touch input and visual response
- **Momentum Transfer**: Smooth velocity transfer from gesture to momentum
- **Interruption**: Smooth handling of scroll interruption via touch

#### Snap-to-Center Mechanics
**Snap Behavior**:
- **Trigger**: Automatic after momentum scroll ends
- **Target**: Nearest card center aligns with screen center
- **Animation**: Spring-based animation with natural feel
- **Duration**: 300-500ms depending on distance to snap

**Spring Animation Specifications**:
```javascript
// React Native Reanimated spring config
{
  tension: 300,          // Moderate tension for natural feel
  friction: 30,          // Balanced friction prevents overshoot
  mass: 1,              // Standard mass for responsive feel
  useNativeDriver: true  // Hardware acceleration
}
```

**Snap Tolerance**:
- **Minimum Velocity**: Below 0.5 points/ms triggers immediate snap
- **Distance Threshold**: >50% to next card centers that card
- **Direction Bias**: Slight preference for forward direction on ambiguous snaps

#### Location Card Selection Interaction
**Touch Target Specifications**:
- **Active Area**: Full card area (280×180px) is touchable
- **Touch Response**: Immediate visual feedback on touch down
- **Gesture Recognition**: Differentiate between tap and scroll gestures
- **Selection Threshold**: 150ms minimum touch for selection (prevents accidental selection during scroll)

**Selection Animation Sequence**:
1. **Touch Down** (0ms): Immediate subtle scale to 0.98x
2. **Touch Recognition** (150ms): Determine if tap vs scroll intent
3. **Selection Decision** (150-200ms): If tap, begin selection animation
4. **Border Animation** (200-300ms): 3px Primary border animates in
5. **Shadow Enhancement** (250-350ms): Shadow intensifies with border
6. **Completion** (400ms): Animation complete, selection state stable

**Animation Implementation**:
```javascript
// Border animation
borderWidth: withSpring(isSelected ? 3 : 0, springConfig),
borderColor: withTiming(isSelected ? '#F97316' : 'transparent', {
  duration: 200,
  easing: Easing.out(Easing.quad)
}),

// Shadow animation
shadowOpacity: withSpring(isSelected ? 0.25 : 0.1, springConfig),
shadowRadius: withSpring(isSelected ? 16 : 8, springConfig)
```

#### Deselection Behavior
**Previous Selection Handling**:
- **Trigger**: When user selects different location card
- **Sequence**: Previous card deselects before new card selects
- **Timing**: 200ms deselection, 100ms gap, 200ms new selection
- **Visual**: Smooth transition prevents jarring state changes

**Deselection Animation**:
- **Border Fade**: Border fades from Primary to transparent
- **Shadow Reduction**: Shadow smoothly reduces to default state
- **Scale Return**: If applicable, returns from selected scale
- **Duration**: 200ms with ease-in timing function

### Difficulty Card Interactions

#### Selection Mechanics
**Touch Recognition**:
- **Touch Target**: Full card area (minimum 100×120px)
- **Response Time**: <50ms visual feedback on touch
- **Multi-touch**: Only single selection allowed, latest touch wins
- **Gesture Type**: Tap only, no long-press or complex gestures

**Selection Animation Choreography**:
1. **Touch Down** (0ms): Scale to 0.98x for immediate feedback
2. **Touch Hold** (0-100ms): Maintain pressed state visual
3. **Touch Release** (100ms): Begin selection sequence
4. **Scale Animation** (100-300ms): Scale to 1.05x with spring
5. **Border Animation** (100-300ms): 2px border appears
6. **Shadow Enhancement** (150-350ms): Shadow intensifies
7. **Completion** (400ms): Final selected state achieved

**Spring Animation Specifications**:
```javascript
// Scale animation for difficulty cards
transform: [
  {
    scale: withSpring(isSelected ? 1.05 : 1, {
      tension: 400,
      friction: 40,
      useNativeDriver: true
    })
  }
]
```

#### Difficulty-Specific Visual Feedback
**Green (Friendly) Card**:
- **Selection Color**: #065F46 (darker green border)
- **Shadow Color**: Green-tinted shadow rgba(16, 185, 129, 0.3)
- **Hover Enhancement**: Subtle brightness increase

**Yellow (Real Talk) Card**:
- **Selection Color**: #92400E (darker amber border)  
- **Shadow Color**: Amber-tinted shadow rgba(245, 158, 11, 0.3)
- **Hover Enhancement**: Subtle brightness increase

**Red (A-Game) Card**:
- **Selection Color**: #991B1B (darker red border)
- **Shadow Color**: Red-tinted shadow rgba(239, 68, 68, 0.3)
- **Hover Enhancement**: Subtle brightness increase

#### Multi-Card Selection Logic
**Exclusive Selection**:
- **Previous Deselection**: Previous card immediately begins deselection animation
- **New Selection**: New card begins selection after 50ms delay
- **Timing Coordination**: Prevents multiple cards appearing selected simultaneously
- **State Management**: Only one difficulty can be selected at any time

### Action Button Interactions

#### Enable/Disable State Transition
**Validation Logic**:
- **Requirements**: Both location AND difficulty must be selected
- **Check Frequency**: Real-time validation on each selection change
- **State Update**: Immediate state change, animation follows

**Enable Animation Sequence**:
1. **Validation Pass** (0ms): Both selections confirmed valid
2. **Background Change** (0-300ms): Neutral-200 to Primary color
3. **Text Update** (100ms): Color change from Neutral-400 to White
4. **Shadow Addition** (200-400ms): Shadow animates in for elevation
5. **Helper Text Fade** (0-200ms): Helper text fades out
6. **Completion** (400ms): Full enabled state achieved

**Animation Implementation**:
```javascript
// Button enable animation
backgroundColor: withTiming(isEnabled ? '#F97316' : '#E5E7EB', {
  duration: 300,
  easing: Easing.out(Easing.quad)
}),
shadowOpacity: withSpring(isEnabled ? 0.2 : 0, springConfig),
textColor: withTiming(isEnabled ? '#FFFFFF' : '#9CA3AF', {
  duration: 200,
  easing: Easing.out(Easing.quad)
})
```

#### Button Press Interaction
**Press Sequence**:
1. **Touch Down** (0ms): Scale to 0.98x immediately
2. **Background Darken** (0ms): Darken to EA580C (darker primary)
3. **Hold State** (0-duration): Maintain pressed appearance
4. **Touch Release** (release): Begin action sequence
5. **Scale Return** (50ms): Return to normal scale
6. **Loading State** (100ms): Transition to loading appearance

**Loading State Animation**:
- **Content Replacement**: Text fades out, spinner fades in
- **Spinner**: 16px white spinner with rotation animation
- **Loading Text**: "Creating..." appears beside spinner
- **Duration**: Indefinite until context creation completes
- **User Interaction**: Button becomes non-interactive

### Advanced Interaction Patterns

#### Gesture Conflict Resolution
**Scroll vs Tap on Location Cards**:
- **Detection Window**: 150ms to determine intent
- **Movement Threshold**: >10px horizontal movement = scroll
- **Time Threshold**: <150ms with <5px movement = tap
- **Fallback**: Ambiguous gestures default to scroll behavior

**Implementation Logic**:
```javascript
const gestureHandler = useGestureHandler({
  onBegin: (event) => {
    gestureStart = { x: event.x, time: Date.now() };
  },
  onEnd: (event) => {
    const deltaX = Math.abs(event.x - gestureStart.x);
    const deltaTime = Date.now() - gestureStart.time;
    
    if (deltaTime < 150 && deltaX < 5) {
      // Treat as tap
      handleCardSelection();
    }
    // Otherwise allow scroll to handle
  }
});
```

#### Multi-Touch Handling
**Multiple Fingers on Carousel**:
- **Primary Finger**: First touch controls scroll
- **Secondary Touches**: Ignored during scroll
- **Selection Priority**: Only single-finger taps register as selections
- **Gesture Interruption**: Multi-touch cancels pending selections

#### Accessibility Gesture Support
**VoiceOver/TalkBack Integration**:
- **Swipe Navigation**: Left/right swipes navigate through location cards
- **Double-Tap Selection**: Standard accessibility selection gesture
- **Focus Management**: Logical tab order through all interactive elements
- **Announcement Timing**: Selection state announced immediately after animation

## Micro-Interactions and Feedback

### Visual Feedback Patterns
**Selection Confirmation**:
- **Immediate Response**: <50ms visual response to touch
- **Progressive Enhancement**: Animation builds confidence in selection
- **State Persistence**: Selected state remains stable and clear
- **Deselection Clarity**: Previous selections clearly release before new ones

**Loading and Processing Feedback**:
- **Anticipation**: Button shows loading state during processing
- **Progress Communication**: Clear indication that action is being processed
- **Success Transition**: Smooth transition to next screen on completion
- **Error Recovery**: Clear feedback and retry options if process fails

### Haptic Feedback Integration

#### iOS Haptic Patterns
**Location Selection**:
- **Type**: UIImpactFeedbackGenerator with medium intensity
- **Timing**: On successful card selection (after 150ms tap detection)
- **Frequency**: Once per selection, not on deselection

**Difficulty Selection**:
- **Type**: UIImpactFeedbackGenerator with light intensity
- **Timing**: On difficulty card selection completion
- **Frequency**: Once per selection change

**Button Activation**:
- **Type**: UIImpactFeedbackGenerator with heavy intensity
- **Timing**: On "Create Scenario" button successful press
- **Frequency**: Once per button activation

#### Android Haptic Patterns
**Vibration Specifications**:
- **Location Selection**: 50ms vibration at 50% intensity
- **Difficulty Selection**: 30ms vibration at 30% intensity
- **Button Activation**: 75ms vibration at 70% intensity
- **Respect Settings**: Honor user's haptic feedback preferences

### Audio Feedback (Optional)

#### Subtle Audio Cues
**Selection Sounds**:
- **Location Selection**: Soft "tick" sound (20ms, 800Hz)
- **Difficulty Selection**: Subtle "click" sound (15ms, 1200Hz)
- **Button Activation**: Satisfying "completion" sound (30ms, 600Hz)
- **Volume**: 40% of system volume, respects silent mode

**Implementation Requirements**:
- **Respect Settings**: Honor user's sound effect preferences
- **Performance**: Sounds don't impact animation performance
- **Platform Integration**: Use appropriate system sound APIs

## Performance Optimization

### Animation Performance
**60fps Guarantee**:
- **Native Driver**: All animations use native driver where possible
- **Property Selection**: Only animate transform and opacity properties
- **Batch Updates**: Coordinate multiple animations to prevent conflicts
- **Memory Management**: Clean up animation resources after completion

### Gesture Performance
**Touch Responsiveness**:
- **Input Latency**: <16ms from touch to visual response
- **Gesture Recognition**: Efficient gesture detection without lag
- **Scroll Performance**: Maintain 60fps during momentum scrolling
- **Memory Efficiency**: Minimal memory allocation during interactions

### Layout Performance
**Efficient Updates**:
- **Selective Re-renders**: Only update changed components
- **Layout Caching**: Cache card layouts to prevent recalculation
- **Image Optimization**: Efficient image loading and caching
- **State Batching**: Batch state updates to minimize re-renders

## Accessibility Interaction Patterns

### Screen Reader Navigation
**VoiceOver/TalkBack Support**:
- **Logical Order**: Tab order flows location carousel → difficulty cards → action button
- **Clear Descriptions**: Each card announces content and selection state
- **Action Descriptions**: Button states clearly communicated
- **State Changes**: Selection changes announced immediately

**Implementation Example**:
```jsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel={`${location.name} location`}
  accessibilityState={{ selected: isSelected }}
  accessibilityHint="Double-tap to select this location for practice"
  onPress={handleLocationSelect}
>
  {/* Card content */}
</Pressable>
```

### Keyboard Navigation
**Focus Management**:
- **Tab Order**: Predictable left-to-right, top-to-bottom order
- **Focus Indicators**: Clear visual focus rings on all interactive elements
- **Activation**: Space/Enter keys activate focused elements
- **Escape Handling**: Escape key returns to previous screen

### Switch Control Support
**Switch Navigation**:
- **Switch Groups**: Logical grouping of location cards and difficulty cards
- **Auto-Scanning**: Configurable scanning speed and patterns
- **Activation Methods**: Multiple activation methods supported
- **Recovery Options**: Clear way to undo selections

## Platform-Specific Interaction Adaptations

### iOS Specific Interactions
**Platform Integration**:
- **Scroll Behavior**: Native iOS momentum and bounce physics
- **Haptic Feedback**: Integration with iOS Haptic Feedback system
- **Gesture Recognition**: iOS-specific gesture recognizers
- **Accessibility**: VoiceOver optimization with iOS patterns

### Android Specific Interactions
**Platform Integration**:
- **Scroll Behavior**: Android overscroll and edge effects
- **Material Ripples**: Material Design ripple effects on card touches
- **Haptic Patterns**: Android vibration system integration
- **Accessibility**: TalkBack optimization with Android patterns

### Web Specific Adaptations
**Browser Compatibility**:
- **Touch Events**: Proper touch event handling for mobile browsers
- **Hover States**: Mouse hover effects for desktop users
- **Keyboard Support**: Full keyboard navigation support
- **Focus Management**: Proper focus management for web accessibility

## Testing and Validation

### Interaction Testing Requirements
**Performance Testing**:
- **Frame Rate**: Consistent 60fps during all interactions
- **Memory Usage**: No memory leaks during extended interaction
- **Battery Impact**: Minimal battery drain from animations
- **Device Coverage**: Testing across low-end to high-end devices

**Usability Testing**:
- **Selection Accuracy**: Users successfully select intended options >95% of time
- **Gesture Recognition**: Scroll vs tap recognition accuracy >98%
- **Accessibility**: Full functionality available through assistive technologies
- **Error Recovery**: Users can easily recover from selection mistakes

## Implementation Guidelines

### Development Best Practices
**Animation Implementation**:
- Use React Native Reanimated for performant animations
- Leverage native driver whenever possible
- Implement proper cleanup for animation resources
- Test animations across different device capabilities

**State Management**:
- Implement proper state synchronization between components
- Handle race conditions in rapid user interactions
- Provide clear state validation and error handling
- Maintain consistent state throughout component lifecycle

**Platform Optimization**:
- Test interactions on actual devices, not just simulators
- Optimize for platform-specific interaction patterns
- Implement proper accessibility support for all platforms
- Handle platform-specific edge cases and limitations

## Last Updated
- **Version 1.0.0**: Complete interaction specifications with platform adaptations
- **Focus**: Fluid, responsive interactions with comprehensive accessibility support
- **Next**: Accessibility implementation details and technical specifications