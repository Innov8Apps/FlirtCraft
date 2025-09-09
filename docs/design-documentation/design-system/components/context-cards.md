# Context Cards Components

---
title: FlirtCraft Context Cards
description: Pre-conversation context display cards for appearance, environment, body language, and conversation starters
feature: pre-conversation-context
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ./cards.md
dependencies:
  - NativeBase components
  - React Native Reanimated
status: approved
---

## Overview

Context cards provide users with detailed scenario information before starting practice conversations. These cards are designed to build confidence by giving users comprehensive preparation materials while maintaining visual appeal and readability.

## Context Card Architecture

### Card Types
1. **Practice Partner Card** - Appearance and personality details
2. **Environment Card** - Scene setting and atmospheric details
3. **Body Language Card** - Non-verbal cues and receptiveness signals
4. **Conversation Starters Card** - AI-suggested opening lines

## Component Specifications

### Base Context Card

#### Purpose
Foundation component for all context card types with consistent styling and behavior.

#### Visual Specifications

**Container:**
- **Width**: Full-width with 16px horizontal margins
- **Min Height**: `120px` - adapts to content length
- **Border Radius**: `12px` - friendly, approachable corners
- **Background**: `#FFFFFF` (White)
- **Border**: `1px solid #E5E7EB` (Neutral-200)
- **Shadow**: `0 2px 4px rgba(0, 0, 0, 0.06)` - subtle depth
- **Margin Bottom**: `16px` - consistent spacing between cards

**Header Section:**
- **Height**: `52px` - comfortable touch target if interactive
- **Background**: `#F9FAFB` (Neutral-50) - subtle differentiation
- **Border Bottom**: `1px solid #E5E7EB` (Neutral-200)
- **Padding**: `16px` - generous touch-friendly spacing

**Header Content:**
- **Icon**: 20px icon in card-specific color
- **Title**: Body Medium (16px/22px, 500 weight)
- **Layout**: Horizontal with 12px icon-to-text spacing
- **Alignment**: Vertically centered

**Content Section:**
- **Padding**: `16px` - consistent with header padding
- **Typography**: Body (16px/22px, 400 weight) for primary content
- **Color**: `#374151` (Neutral-700) - high readability
- **Spacing**: 12px between content sections

#### Card Animation
- **Entrance**: Fade in with slight scale (300ms ease-out)
- **Stagger**: 100ms delay between sequential cards
- **Scroll**: Subtle parallax effect during page scroll
- **Selection**: Subtle highlight animation if interactive

### Practice Partner Card

#### Purpose
Display AI partner's appearance, style, and observable characteristics.

#### Visual Specifications

**Header:**
- **Icon**: Person silhouette icon in `#E65100` (Secondary/Deep Orange)
- **Title**: "Your Practice Partner"
- **Background**: Subtle pink tint `#FCE7F3` (Pink-50)

**Content Structure:**

*Age & Basic Info:*
- **Typography**: Body Medium (16px/22px, 500 weight)
- **Content**: Age range matching user preferences
- **Example**: "Mid-20s, appears around your preferred age range"

*Style Description:*
- **Typography**: Body (16px/22px, 400 weight)
- **Content**: General appearance and style overview
- **Example**: "Casual-professional look"

*Observable Details (Bulleted List):*
- **Format**: Unordered list with custom bullet points
- **Bullet Style**: Small circles in Secondary color
- **Spacing**: 8px between list items
- **Content**: 3-4 specific, contextual details

**Example Content:**
```
Mid-20s, appears around your preferred age range

Casual-professional style with a relaxed, approachable demeanor. Currently settled in with a laptop bag and what looks like study materials.

• Reading a paperback novel while occasionally sipping an iced coffee
• Wearing comfortable jeans and a soft sweater - approachable style  
• Has earbuds draped around neck but not currently listening to music
• Occasionally glances up from book, seems content but not rushed
```

### Environment Card

#### Purpose
Set the scene with detailed environmental context and atmospheric details.

#### Visual Specifications

**Header:**
- **Icon**: Location pin icon in `#10B981` (Success/Green)
- **Title**: "The Environment"  
- **Background**: Subtle green tint `#F0FDF4` (Green-50)

**Content Structure:**

*Time & Context:*
- **Typography**: Body Medium (16px/22px, 500 weight)
- **Content**: Specific time and day context
- **Example**: "Tuesday afternoon, 2:30 PM - perfect coffee shop energy"

*Crowd & Energy Level:*
- **Typography**: Body (16px/22px, 400 weight)
- **Content**: Social context and energy assessment
- **Example**: "Moderately busy - good energy without being overwhelming"

*Atmospheric Details (Bulleted List):*
- **Format**: Unordered list with environment-themed bullets
- **Bullet Style**: Small squares in Success color
- **Content**: Sensory and contextual scene details

**Example Content:**
```
Tuesday afternoon, 2:30 PM - perfect coffee shop energy

Moderately busy with a comfortable mix of students and professionals. The atmosphere feels relaxed and social without being overwhelming.

• Soft indie music playing at conversation-friendly volume
• Natural lighting streaming through large windows  
• Pleasant aroma of fresh coffee and pastries in the air
• Mix of people working, chatting, and reading - social but not loud
```

### Body Language Card

#### Purpose
Display non-verbal cues and receptiveness signals with difficulty-appropriate feedback.

#### Visual Specifications

**Header:**
- **Icon**: Eye icon in `#F59E0B` (Warning/Amber)
- **Title**: "Body Language Signals"
- **Background**: Subtle amber tint `#FFFBEB` (Amber-50)

**Content Structure:**

*Signal Indicators:*
- **Format**: List with colored circle indicators
- **Circle Size**: 12px diameter
- **Colors**: Traffic light system (🟢🟡🔴)
- **Spacing**: 16px vertical between signals
- **Layout**: Circle + 8px spacing + text description

*Signal Colors:*
- **🟢 Green (Positive)**: `#10B981` (Success) - receptive, welcoming
- **🟡 Yellow (Neutral)**: `#F59E0B` (Warning) - neutral, realistic  
- **🔴 Red (Negative)**: `#EF4444` (Error) - challenging, requires skill

#### Difficulty-Based Signals

**Green Difficulty Signals:**
```
🟢 Making brief but friendly eye contact when you look their way
🟢 Relaxed, open posture with arms uncrossed  
🟡 Occasionally checks phone but seems approachable
🟢 Body language suggests they're content and not in a rush
```

**Yellow Difficulty Signals:**
```
🟡 Focused on their book with occasional glances around the room
🟡 Neutral expression - not particularly inviting but not closed off
🟡 Has been settled in same spot for a while, seems comfortable
🟡 Body language suggests openness to brief interactions
```

**Red Difficulty Signals:**
```
🔴 Very focused on book with minimal awareness of surroundings
🟡 Checking phone frequently - might be expecting someone
🔴 Body language suggests they might leave soon
🟡 Not actively discouraging interaction but clearly absorbed in tasks
```

### Conversation Starters Card

#### Purpose
Provide AI-generated, contextually appropriate conversation opening suggestions.

#### Visual Specifications

**Header:**
- **Icon**: Chat bubble icon in `#3B82F6` (Info/Blue)
- **Title**: "AI Starter Suggestions"
- **Background**: Subtle blue tint `#EFF6FF` (Blue-50)

**Content Structure:**

*Suggestion List:*
- **Format**: Numbered list (1, 2, 3)
- **Number Style**: Circles with Info color background
- **Spacing**: 16px between suggestions
- **Typography**: Body (16px/22px, 400 weight) with slight indentation

*Additional Options:*
- **Custom Option**: Link-styled text for user creativity
- **Help Option**: Secondary link for conversation tips

**Example Content:**
```
1. "That book looks interesting - I've been looking for something new to read. How are you liking it?"

2. "This place has such a great atmosphere for reading. Do you come here often to study?"

3. "I couldn't help but notice you seem really absorbed in your book. Any chance it's worth recommending?"

Or create your own approach!
Need help crafting an opener? →
```

#### Interactive Features

**Suggestion Selection:**
- **Tap Behavior**: Copies suggestion to conversation input
- **Visual Feedback**: Subtle highlight on tap
- **Animation**: Brief scale animation on selection

**Custom Opener Link:**
- **Behavior**: Opens tip modal with opener crafting advice
- **Style**: Underlined link in Info color
- **Accessibility**: Screen reader friendly

### Card Collection Behavior

#### Scrollable Layout

**Container:**
- **Style**: Vertical scroll view
- **Padding**: 16px horizontal margins
- **Spacing**: 16px between cards
- **Background**: `#F9FAFB` (Neutral-50) page background

**Scroll Indicators:**
- **Progress**: Subtle scroll progress indicator
- **Position**: Small dots or progress bar
- **Location**: Bottom of screen, centered

**Card Entrance Animation:**
- **Sequence**: Cards animate in sequentially
- **Timing**: 100ms stagger between cards  
- **Effect**: Fade in with slight upward movement
- **Duration**: 300ms per card with ease-out

#### Refresh Functionality

**Pull-to-Refresh:**
- **Trigger**: Pull down at top of card list
- **Indicator**: Standard platform refresh indicator
- **Action**: Regenerates all context with new AI content
- **Feedback**: "Creating new scenario..." loading message

**Regenerate Button:**
- **Position**: Bottom of card collection
- **Style**: Secondary button styling
- **Text**: "Generate New Context"
- **Behavior**: Maintains scenario + difficulty, creates new context

### Accessibility Features

#### Screen Reader Support

**Card Structure:**
- **Roles**: Each card marked as informational region
- **Headers**: Proper heading hierarchy (h3 level)
- **Content**: Logical reading order through all content
- **Navigation**: Easy jumping between card sections

**Signal Indicators:**
- **Descriptions**: "Positive signal:", "Neutral signal:", "Negative signal:"
- **Context**: Full description beyond just color
- **Meaning**: Explains implication of each signal

#### Visual Accessibility

**High Contrast:**
- **Text**: All text meets WCAG AA contrast requirements
- **Signals**: Color indicators supplemented with icons/text
- **Focus**: Clear focus indicators for keyboard navigation

**Text Scaling:**
- **Responsive**: Cards adapt to user's preferred text size
- **Layout**: Maintains readability at 200% text size
- **Spacing**: Proportional spacing adjustments

#### Motor Accessibility

**Touch Targets:**
- **Interactive Elements**: Minimum 44x44px touch targets
- **Spacing**: Adequate space between tappable areas
- **Error Prevention**: Confirmation for destructive actions (refresh)

## Usage Guidelines

### Content Generation Principles

**Consistency:**
- All four cards must be coherent and non-contradictory
- Details should logically support the scenario and difficulty
- Environmental factors should influence body language signals

**Appropriateness:**
- Content must be respectful and inclusive
- Age-appropriate for the target age range (18+)
- Culturally sensitive and broadly relatable

**Educational Value:**
- Signals should teach actual body language reading
- Environment details should feel realistic and specific
- Conversation starters should model good conversation techniques

### Performance Considerations

**Content Loading:**
- **Generation Time**: Target <3 seconds for complete context
- **Caching**: Cache successful generations for re-use
- **Fallbacks**: Pre-written content for generation failures
- **Progressive Loading**: Show cards as they're generated

**Memory Management:**
- **Context Storage**: Store current context in memory during conversation
- **History**: Limited history of recent contexts for back navigation
- **Cleanup**: Clear old context when new scenarios selected

## Implementation Notes

### AI Integration Points

**Context Generation API:**
- Input: scenario, difficulty, user preferences
- Output: structured context data for all four cards  
- Validation: Coherence and appropriateness checking
- Fallbacks: Default content templates for failures

**Content Structure:**
```json
{
  "partner": {
    "ageRange": "Mid-20s",
    "style": "Casual-professional...",
    "details": ["Reading a paperback novel...", "..."]
  },
  "environment": {
    "timeContext": "Tuesday afternoon...",
    "crowdLevel": "Moderately busy...",
    "details": ["Soft indie music...", "..."]
  },
  "bodyLanguage": {
    "signals": [
      { "type": "positive", "description": "Making brief eye contact..." },
      { "type": "neutral", "description": "Occasionally checks phone..." }
    ]
  },
  "starters": [
    "That book looks interesting...",
    "This place has such great atmosphere...",
    "I couldn't help but notice..."
  ]
}
```

### Platform Adaptations

**iOS:**
- **Native Scrolling**: Use native scroll physics and indicators
- **Haptic Feedback**: Subtle haptics on card interactions
- **Dynamic Type**: Support iOS text scaling preferences
- **Safe Areas**: Proper handling of notch and home indicator

**Android:**
- **Material Design**: Follow Material scroll and card patterns
- **Accessibility**: TalkBack optimization for card content
- **Performance**: Optimize for wide range of Android devices
- **Navigation**: Proper handling of hardware back button

---

## Related Documentation
- [Base Card Components](./cards.md) - Foundation card styling
- [Color Tokens](../tokens/colors.md) - Context card colors
- [Typography Tokens](../tokens/typography.md) - Text styling
- [Pre-Conversation Context Feature](../../features/pre-conversation-context/) - Complete feature specification

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*