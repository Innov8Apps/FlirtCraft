# Scenario Selection Feature - Design Overview

---
title: Scenarios Tab - Pre-built Scenario Selection  
description: Complete specification for selecting pre-built practice scenarios with templates in the Scenarios tab
feature: scenarios-tab-selection
last-updated: 2025-09-07
version: 2.0.0
tab: Scenarios
related-files: 
  - user-journey.md
  - screen-states.md
  - interactions.md
  - accessibility.md
  - implementation.md
  - ../../design-system/components/cards.md
dependencies:
  - profile feature integration
  - pre-conversation-context feature (with templates)
  - conversation feature
status: approved
---

## Feature Overview

**Tab Location**: Scenarios Tab (Pre-built Scenarios with Templates)

The Scenario Selection feature is specifically for the **Scenarios tab**, offering users pre-built, trendy scenarios with templated contexts. Unlike the Chat tab's custom conversation creation, these scenarios come with predefined templates and trending topics. This is a **P0 MVP feature** that provides quick-start practice options.

**Note**: This feature is distinct from the Chat tab's unified selection for custom conversations.

## Key User Needs Addressed

### Primary Goals
- **Relevant Practice**: Users can practice in scenarios they'll actually encounter
- **Progressive Learning**: Difficulty levels allow gradual skill building
- **Choice and Control**: Users feel empowered to choose their practice experience
- **Context Preparation**: Clear understanding of what to expect before starting

### User Value Proposition
"Choose practice scenarios that match your real-world dating situations, with difficulty levels that challenge you appropriately as you build confidence."

## Success Metrics

### Engagement Metrics
- **Scenario Completion Rate**: >75% of selected scenarios are completed
- **Difficulty Progression**: Users advance through difficulty levels within 3-4 weeks
- **Variety Usage**: Users try multiple scenario types within first month
- **Return Rate**: 80%+ users return to scenario selection within 24 hours

### Learning Effectiveness
- **Appropriate Challenge**: Users select difficulty levels that optimize learning
- **Real-World Application**: 60%+ users report practicing scenarios they've selected
- **Confidence Building**: Progressive difficulty selection correlates with confidence growth

## 8 Core Scenarios

### Social Scenarios
1. **Coffee Shops** - Green: Friendly barista/customer, Yellow: Busy coffee shop, Red: Popular cafe with lines
2. **Bookstores** - Green: Quiet browsing, Yellow: Book recommendation seeking, Red: Crowded book signing event
3. **Parks** - Green: Dog walking encounter, Yellow: Jogging path conversation, Red: Busy weekend festival
4. **Art Galleries** - Green: Quiet exhibition, Yellow: Opening night mixer, Red: Crowded popular exhibition

### Activity-Based Scenarios
5. **Gyms** - Green: Equipment sharing, Yellow: Fitness class interaction, Red: Peak hour busy gym
6. **Bars** - Green: Quiet happy hour, Yellow: Friday night social scene, Red: Crowded weekend nightlife
7. **Grocery Stores** - Green: Produce section help, Yellow: Checkout line chat, Red: Busy Saturday shopping
8. **Campus** - Green: Library study group, Yellow: Campus event, Red: Busy student union

## Difficulty Levels

### 🟢 Green (Friendly)
- **AI Personality**: Open, receptive, making eye contact
- **Context**: Positive body language, welcoming environment
- **Challenge Level**: Beginner-friendly, forgiving of mistakes
- **Success Rate**: 85%+ for users to build initial confidence

### 🟡 Yellow (Real Talk)
- **AI Personality**: Neutral, realistic stranger behavior
- **Context**: Mixed signals, natural hesitation and interest
- **Challenge Level**: Moderate, represents typical real-world interactions
- **Success Rate**: 60-75% - realistic but achievable

### 🔴 Red (A-Game)
- **AI Personality**: Reserved, busy, requires genuine skill
- **Context**: Challenging environment, distractions, higher stakes
- **Challenge Level**: Advanced, requires developed conversation skills
- **Success Rate**: 40-60% - challenging but not discouraging

## Dependencies on Other Features

### Required Integration Points
- **Profile Feature**: User preferences inform scenario personalization
- **Pre-Conversation Context**: Selected scenario drives context generation
- **Conversation Feature**: Scenario choice affects AI behavior and responses
- **Feedback Feature**: Scenario difficulty influences feedback and scoring

### Component Dependencies
- **Card Components**: Scenario selection cards
- **Button Components**: Difficulty selection and action buttons
- **Navigation Components**: Flow between scenario selection and conversation
- **Modal Components**: Scenario preview and information displays

## User Persona Alignment

### Anxious Alex (Beginner)
**Scenario Preferences**:
- **Favorites**: Coffee shops, bookstores, parks (low-pressure environments)
- **Difficulty**: Primarily Green level with occasional Yellow
- **Support Needs**: Clear descriptions, success rate indicators, encouragement

### Comeback Catherine (Intermediate)
**Scenario Preferences**:
- **Favorites**: Bars, art galleries, campus (age-appropriate social settings)
- **Difficulty**: Mix of Yellow and Red levels for realistic practice
- **Support Needs**: Modern context accuracy, practical application tips

### Confident Carlos (Advanced)
**Scenario Preferences**:
- **Favorites**: Gyms, bars, busy environments (challenging situations)
- **Difficulty**: Primarily Red level with variety for skill refinement
- **Support Needs**: Advanced challenges, optimization insights, competitive elements

### Shy Sarah (Anxious Beginner)
**Scenario Preferences**:
- **Favorites**: Bookstores, coffee shops, quiet environments
- **Difficulty**: Green level with very gradual progression
- **Support Needs**: Safe environment emphasis, private practice, gentle encouragement

## Key Interaction Points

### Entry Points
1. **Main Menu**: Primary access point from app navigation
2. **Post-Feedback**: "Try Different Scenario" option after conversation
3. **Profile Recommendations**: AI-suggested scenarios based on goals
4. **Quick Practice**: Recently used scenarios for fast access

### Core Interactions
1. **Scenario Browsing**: Grid or carousel view of available scenarios
2. **Difficulty Selection**: Clear visual indicators for challenge levels
3. **Scenario Preview**: Detailed information before commitment
4. **Context Preparation**: Transition to pre-conversation context
5. **Quick Restart**: Easy access to repeat scenarios

### Exit Points
- **Primary**: Continue to Pre-Conversation Context → Conversation
- **Secondary**: Return to main menu/dashboard
- **Tertiary**: Profile access to adjust preferences

## Design System Integration

### Components Used
- [Scenario Cards](../../design-system/components/cards.md#scenario-card) - Primary scenario selection cards with images and descriptions
- [Difficulty Selector Buttons](../../design-system/components/buttons.md#chip-button) - Green/Yellow/Red difficulty selection
- [Modal Components](../../design-system/components/modals.md#info-modal) - Scenario preview and detailed information displays
- [Primary Button](../../design-system/components/buttons.md#primary-button) - "Start Practice" main action
- [Icon Button](../../design-system/components/buttons.md#icon-button) - Quick access and navigation controls
- [Navigation Header](../../design-system/components/navigation.md#header-navigation) - Back navigation and title display
- [Tab Navigation](../../design-system/components/navigation.md#tab-bar) - Bottom navigation integration

### Design Tokens
- [Difficulty Colors](../../design-system/tokens/colors.md#semantic-colors) - Green (#10B981), Yellow (#F59E0B), Red (#EF4444)
- [Card Shadows](../../design-system/tokens/colors.md#elevation-system) - Consistent card elevation and depth
- [Typography Hierarchy](../../design-system/tokens/typography.md#heading-system) - Card titles, descriptions, and metadata
- [Spacing Grid](../../design-system/tokens/spacing.md#grid-system) - Card layout, margins, and gutters
- [Animation Presets](../../design-system/tokens/animations.md#interaction-animations) - Card selection, difficulty overlay, transitions

### Interaction Patterns
- [Card Selection Animations](../../design-system/tokens/animations.md#selection-feedback) - Visual feedback for scenario selection
- [Difficulty Overlay Transitions](../../design-system/tokens/animations.md#modal-transitions) - Smooth difficulty selector appearance
- [Loading States](../../design-system/components/cards.md#loading-states) - Scenario loading and context generation

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete scenario selection flow
- **[Screen States](./screen-states.md)** - All visual states and responsive design
- **[Interactions](./interactions.md)** - Selection animations and micro-interactions
- **[Accessibility](./accessibility.md)** - Inclusive design for scenario selection
- **[Implementation](./implementation.md)** - Technical specifications and handoff

## Implementation Notes

### State Management
- **Current Selection**: Track user's scenario and difficulty choices
- **History Tracking**: Remember recently used scenarios for quick access
- **Progress Integration**: Show user's success rates per scenario/difficulty
- **Recommendation Engine**: AI suggestions based on user patterns

### Performance Considerations
- **Image Loading**: Optimized scenario images with lazy loading
- **Quick Selection**: Fast transitions between selection and practice
- **Offline Support**: Cached scenario information for offline browsing
- **Memory Management**: Efficient handling of scenario data and images

## Last Updated
- **Version 1.0.0**: Initial comprehensive feature specification
- **Focus**: MVP scenario selection with 8 scenarios and 3 difficulty levels
- **Next**: Implementation-ready specifications in related files