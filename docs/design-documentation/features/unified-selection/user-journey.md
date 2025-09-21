I# Unified Selection Feature - User Journey

---
title: Chat Tab - Unified Selection User Journey
description: Complete user flow for creating custom conversations with unified location and difficulty selection in the Chat tab
feature: chat-unified-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - screen-states.md
  - interactions.md
  - accessibility.md
  - implementation.md
dependencies:
  - pre-conversation-context feature
  - chat-context-creation feature
status: approved
---

## User Journey Overview

**Tab Location**: Chat Tab (Custom Conversation Creation)

The unified selection journey in the **Chat tab** provides users with an elegant, streamlined way to create custom conversation practice sessions. Users select both location and difficulty on a single screen, with options for small tweaks and customizations. After selection, AI generates randomized context based on these choices. This is distinct from the Scenarios tab's pre-built template approach.

## Entry Point

### Primary Entry Point: Chat Tab Navigation
**Trigger**: User taps the Chat tab from bottom navigation  
**Context**: User wants to create a custom conversation with AI-generated randomized context based on their selections  
**Emotional State**: Motivated to practice, wants personalized experience with some control  
**Success Criteria**: Select location and difficulty, make any small tweaks, then receive AI-generated context for practice  

## Core User Journey Flow

### Phase 1: Initial Screen Orientation (2-3 seconds)

#### Step 1: Screen Recognition and Layout Understanding
**User Experience**:
- Immediate visual understanding of two distinct selection areas
- Top section shows beautiful location carousel with peek preview of adjacent cards
- Bottom section displays three color-coded difficulty options
- Clear "Create Your Practice Session" title provides context
- Progress indicator shows "Step 1 of 2" providing journey awareness

**User Mental Model**: "I need to choose where I want to practice and how challenging I want it to be"
**Emotional State**: Oriented and ready to make selections
**Key Success Factor**: Instant recognition of the two required selections

**Visual Hierarchy Recognition**:
- Location carousel draws primary attention with large, beautiful imagery
- Difficulty cards provide secondary focus with clear color differentiation
- Disabled "Create Scenario" button indicates completion requirement
- Header context sets appropriate expectations

### Phase 2: Location Exploration and Selection (10-20 seconds)

#### Step 2: Location Discovery Through Carousel Browsing  
**User Experience**:
- Natural scroll gesture reveals all 8 location options
- Smooth momentum scrolling with satisfying snap-to-center behavior
- Peek preview creates curiosity about next/previous options
- High-quality imagery immediately communicates location atmosphere
- Cards automatically center after scroll, reducing user effort

**User Mental Model**: "I'm exploring different places where I could practice conversations"
**Emotional State**: Engaged browsing, considering options based on personal comfort and goals
**Key Success Factor**: User feels empowered to explore all options without friction

**Exploration Patterns**:
- **Visual Browsers**: Rely primarily on imagery to assess location appeal
- **Systematic Browsers**: Scroll through all options before making decision
- **Quick Deciders**: Select familiar/comfortable location immediately
- **Adventurous Browsers**: Seek new or challenging location options

#### Step 3: Location Selection Decision
**User Experience**:
- Tap selected location card for immediate selection feedback
- Card gains prominent 3px Primary color border with subtle glow
- Enhanced shadow provides depth and confirmation of selection
- Location name becomes more prominent with selection state
- Carousel maintains position without jarring movements

**User Mental Model**: "This is the place where I want to practice today"
**Emotional State**: Committed to location choice, ready for difficulty decision
**Key Success Factor**: Clear, satisfying selection feedback builds confidence

**Persona-Specific Selection Patterns**:
- **Anxious Alex**: Gravitates toward Coffee Shop, Bookstore (low-pressure environments)
- **Comeback Catherine**: Prefers Bar/Lounge, Art Gallery (age-appropriate social settings)
- **Confident Carlos**: Chooses Gym, Bar/Lounge (confident, challenge-seeking environments)  
- **Shy Sarah**: Selects Coffee Shop, Park (quiet, comfortable spaces)

### Phase 3: Difficulty Calibration (5-10 seconds)

#### Step 4: Difficulty Level Assessment
**User Experience**:
- Three distinct difficulty cards with clear visual differentiation
- Color coding immediately communicates challenge level (Green/Yellow/Red)
- Brief, clear descriptions help calibrate appropriate challenge
- Equal visual weight encourages consideration of all options
- Success rate information helps set appropriate expectations

**User Mental Model**: "How challenging do I want this conversation to be?"
**Emotional State**: Calibrating confidence level against desired growth
**Key Success Factor**: Accurate difficulty selection for optimal learning experience

**Difficulty Consideration Factors**:
- **Current Confidence Level**: How prepared they feel today
- **Recent Performance**: Success in previous conversations
- **Personal Goals**: Whether seeking comfort or growth
- **Available Energy**: Mental readiness for challenge

#### Step 5: Difficulty Selection and Validation
**User Experience**:
- Tap difficulty card for immediate selection animation (1.05x scale)
- Color-appropriate border confirmation with enhanced shadow
- Previously selected card (if any) smoothly returns to default state  
- "Create Scenario" button becomes enabled with subtle animation
- Both selections remain visually confirmed

**User Mental Model**: "I've made my choices and I'm ready to create my practice scenario"
**Emotional State**: Committed to choices, anticipating practice session
**Key Success Factor**: Confidence in combined location and difficulty selection

### Phase 4: Action and Transition (2-3 seconds)

#### Step 6: Scenario Creation Initiation
**User Experience**:
- "Create Scenario" button becomes prominent and inviting
- Button tap provides immediate feedback with loading state
- Brief loading message: "Creating your practice session..."
- Smooth transition maintains visual continuity
- Selected choices are preserved and passed to context creation

**User Mental Model**: "The app is setting up my custom practice scenario"
**Emotional State**: Anticipation for upcoming practice session
**Key Success Factor**: Seamless transition maintains momentum and engagement

## Advanced User Behaviors

### Efficient Selection Path
**Behavior**: Users who quickly know what they want
**Experience**: Location selection → immediate difficulty selection → create scenario
**Optimization**: Quick selection shouldn't feel rushed, still allow for reconsideration
**Target Time**: 15-25 seconds from entry to completion

### Exploration-Heavy Path  
**Behavior**: Users who want to consider all options carefully
**Experience**: Full location carousel browse → difficulty comparison → potential re-selection
**Optimization**: Provide satisfying browsing experience without fatigue
**Target Time**: 30-60 seconds with high engagement throughout

### Indecisive User Path
**Behavior**: Users who struggle with choice commitment
**Experience**: Multiple location selections → difficulty changes → final decision
**Optimization**: No penalty for changing selections, maintain selection state
**Support**: Gentle guidance without pressure

### Return User Path
**Behavior**: Users returning to create additional scenarios
**Experience**: Quick recognition → efficient selection → familiar flow
**Optimization**: Remember recent patterns while encouraging variety
**Enhancement**: Quick access to recently used combinations

## Edge Cases and Error Recovery

### Single Selection Made
**Scenario**: User selects location OR difficulty but not both
**User Experience**:
- "Create Scenario" button remains disabled with subtle visual feedback
- Helpful micro-copy: "Select both location and difficulty to continue"
- No error states or negative messaging
- Clear visual indication of what's still needed

### Selection Changing
**Scenario**: User changes location or difficulty after initial selection
**User Experience**:
- Smooth animation between selection states
- No confirmation required for changes
- "Create Scenario" button remains enabled if both selections still valid
- Previous selection cleanly deselects before new selection appears

### Carousel Navigation Issues  
**Scenario**: User has difficulty with horizontal scrolling
**User Experience**:
- All locations remain accessible through standard scrolling
- No gestures required beyond tap for selection
- Clear visual indicators of scroll capability (peek preview)
- Alternative: Swipe gestures work but aren't required

### Rapid Selection Attempts
**Scenario**: User taps rapidly or attempts to select multiple options
**User Experience**:
- Debounced selection prevents double-selection issues
- Clear single-selection behavior for both location and difficulty
- Latest valid selection takes precedence
- No error messages for rapid interaction

## Success Metrics for Journey

### Selection Efficiency
- **Time to Completion**: 15-45 seconds average from entry to "Create Scenario"
- **Exploration Rate**: 70%+ users scroll through multiple locations before selecting
- **Decision Confidence**: <5% users return to change selections after context creation
- **Completion Rate**: >90% users who start selection process complete both choices

### Engagement Quality  
- **Discovery Rate**: 40%+ users select locations they haven't tried before
- **Difficulty Progression**: Users gradually select higher difficulties over time
- **Return Satisfaction**: 80%+ users rate unified selection as preferable to separate screens
- **Flow Satisfaction**: Smooth progression to context creation without friction

### Learning Effectiveness
- **Appropriate Challenge**: Difficulty selection correlates with actual success rates
- **Variety Benefits**: Users who try multiple locations show broader skill development
- **Progressive Difficulty**: Users advance through difficulty levels within 4-6 weeks
- **Real-World Application**: Selected locations correlate with real-life practice attempts

## Persona-Specific Journey Adaptations

### Anxious Alex Journey Optimization
- **Comfort Emphasis**: Coffee Shop and Bookstore positioned prominently in carousel
- **Gentle Guidance**: Green difficulty highlighted as confidence-building option
- **Success Messaging**: Emphasize safe practice environment throughout
- **Gradual Challenge**: Subtle encouragement toward Yellow difficulty when ready

### Comeback Catherine Journey Optimization
- **Relevant Scenarios**: Bar/Lounge and Art Gallery featured prominently
- **Balanced Challenge**: Yellow difficulty positioned as realistic preparation
- **Modern Context**: Contemporary imagery that reflects current social environments
- **Practical Value**: Clear connection between practice and real-world dating success

### Confident Carlos Journey Optimization  
- **Challenge Seeking**: Red difficulty prominently featured with achievement potential
- **Variety Encouragement**: Subtle prompts to try different location types
- **Performance Tracking**: Implied progress tracking through completion states
- **Competitive Elements**: Achievement language in difficulty descriptions

### Shy Sarah Journey Optimization
- **Safe Spaces**: Bookstore and Coffee Shop positioned as comfortable starting points  
- **Ultra-Gentle Approach**: Green difficulty emphasized with extra encouragement
- **Private Practice**: No social comparison elements in interface
- **Gradual Exposure**: Very subtle progression suggestions over multiple sessions

## Related Documentation

- **[Screen States](./screen-states.md)** - Complete visual specifications for all screen states
- **[Interactions](./interactions.md)** - Detailed animation and micro-interaction specifications
- **[Accessibility](./accessibility.md)** - Inclusive design for unified selection
- **[Implementation](./implementation.md)** - Technical specifications and development handoff

## Implementation Notes

### State Management Flow
1. **Entry** → Initialize empty selection state and load location carousel
2. **Location Browse** → Track carousel position and user interaction patterns  
3. **Location Select** → Store location choice and update UI state
4. **Difficulty Consider** → Track difficulty option viewing and consideration
5. **Difficulty Select** → Store difficulty choice and enable action button
6. **Create Scenario** → Pass complete selection data to context creation system

### Analytics Tracking
- **Location Browsing Patterns**: Scroll behavior and exploration time
- **Selection Preferences**: Most/least popular location and difficulty combinations
- **Journey Efficiency**: Time from entry to completion
- **Error Patterns**: Selection changes and abandonment points

### Performance Requirements
- **Carousel Smoothness**: 60fps scrolling performance across all devices
- **Selection Responsiveness**: <100ms feedback for all selection actions
- **Image Loading**: Progressive image loading without blocking interface
- **Transition Speed**: <300ms transition to context creation screen

## Last Updated
- **Version 1.0.0**: Complete user journey mapping with persona adaptations
- **Focus**: Streamlined, engaging selection experience with optimal challenge calibration  
- **Next**: Screen state specifications and interaction design details