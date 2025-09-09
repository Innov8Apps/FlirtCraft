# Feedback Feature - Screen States

---
title: Feedback Feature Screen States and Visual Specifications
description: Complete screen-by-screen visual design specifications for all feedback states
feature: feedback
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - interactions.md
  - accessibility.md
  - implementation.md
  - ../../design-system/components/cards.md
  - ../../design-system/components/buttons.md
  - ../../design-system/components/gamification.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/tokens/animations.md
  - ../../design-system/components/gamification.md
  - ../../design-system/components/buttons.md
dependencies:
  - design-system/components
  - gamification components
status: approved
---

## Screen States Overview

The feedback feature includes 6 primary screen states with multiple sub-states and responsive variations. Each state is designed to maintain user engagement while providing valuable learning insights.

## Table of Contents

1. [Loading State](#loading-state)
2. [Score Reveal State](#score-reveal-state)
3. [Detailed Feedback State](#detailed-feedback-state)
4. [Progress Comparison State](#progress-comparison-state)
5. [Action Selection State](#action-selection-state)
6. [Error States](#error-states)

---

## Loading State

### Purpose
Smooth transition from conversation end to feedback display while AI analyzes conversation data.

### Layout Structure
- **Container**: Full screen with conversation fade-out overlay
- **Grid**: Center-aligned loading content in safe area
- **Spacing**: 24px margins, 16px internal spacing

### State: Default Loading

#### Visual Design Specifications

**Background Treatment**:
- **Base Layer**: Gradient from Primary-50 to Secondary-50 (subtle)
- **Overlay**: Semi-transparent white (Alpha 0.95) for content readability
- **Conversation Fade**: Previous conversation interface fading out over 300ms

**Loading Animation**:
- **Primary Indicator**: Circular progress ring in Primary-500 color
- **Diameter**: 64px with 4px stroke width
- **Animation**: 1.5s rotation with spring easing
- **Center Icon**: Chat analysis icon (24px) in Primary-600

**Typography**:
- **Primary Message**: "Analyzing your conversation..." in H3 style, Neutral-800
- **Secondary Message**: "This will just take a moment" in Body-Small, Neutral-600
- **Positioning**: Center-aligned, 16px spacing between messages

**Micro-copy Variations**:
- **Standard**: "Analyzing your conversation..."
- **First Time**: "Preparing your first feedback session..."
- **High Performer**: "Reviewing your great conversation..."
- **Struggling User**: "Looking for your conversation highlights..."

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Loading Ring**: 56px diameter, maintains center position
- **Typography**: H4 for primary message, Caption for secondary
- **Margins**: 16px side margins, 20% top margin

**Tablet (768-1023px)**:
- **Loading Ring**: 72px diameter for better visibility
- **Typography**: H3 primary, Body-Small secondary
- **Margins**: 32px side margins, center vertical alignment

**Desktop (1024px+)**:
- **Loading Ring**: 80px diameter with enhanced stroke (6px)
- **Typography**: H2 primary, Body secondary
- **Max Width**: 480px container with center alignment

#### Accessibility Specifications

**Screen Reader Support**:
- **Live Region**: `aria-live="polite"` with loading status updates
- **Loading Text**: "Analyzing conversation, please wait"
- **Progress Updates**: Periodic status announcements

**Motion Sensitivity**:
- **Reduced Motion**: Static progress indicator with opacity pulse
- **Alternative**: Simple loading text without animation
- **Preference**: Respects `prefers-reduced-motion` system setting

---

## Score Reveal State

### Purpose
Dramatic reveal of conversation score with context and emotional encouragement.

### Layout Structure
- **Container**: Full screen with celebration-focused design
- **Grid**: Score-centered layout with supporting information
- **Spacing**: Mathematical 4px scale with emphasis on score prominence

### State: Score Animation (In Progress)

#### Visual Design Specifications

**Score Display**:
- **Primary Score**: Large animated counter from 0 to final score
- **Typography**: Custom numeric display, 72px on mobile, 96px on desktop
- **Color**: Dynamic based on score range:
  - 80-100: Success-500 (Green)
  - 60-79: Warning-500 (Yellow) 
  - 40-59: Primary-500 (Orange)
  - 0-39: Error-500 (Red)

**Score Context**:
- **Score Range**: "out of 100" in Body-Small, Neutral-600
- **Performance Label**: Contextual label based on score
  - 90+: "Exceptional conversation!"
  - 80-89: "Great job!"
  - 70-79: "Well done!"
  - 60-69: "Good effort!"
  - 50-59: "Keep practicing!"
  - <50: "Learning opportunity!"

**Visual Enhancement**:
- **Background**: Subtle celebration graphics for high scores (80+)
- **Particles**: Animated success particles for scores 90+
- **Progress Ring**: Circular progress showing score as percentage
- **Color Coding**: Consistent with score performance levels

#### Animation Specifications

**Score Counter Animation**:
- **Duration**: 2000ms total animation time
- **Easing**: Ease-out with spring finish for satisfaction
- **Increment Pattern**: Accelerating then decelerating count
- **Final Impact**: Slight bounce/scale on reaching final number

**Supporting Elements**:
- **Progress Ring**: 1500ms fill animation synchronized with counter
- **Label Fade-in**: 300ms delay after score completes
- **Celebration Effects**: Triggered only for scores 80+

### State: Score Complete (Static Display)

#### Visual Design Specifications

**Layout Organization**:
- **Score Section** (Top 40%): Final score with context
- **Quick Insights** (Middle 40%): 2-3 key performance highlights
- **Action Preview** (Bottom 20%): Hint at detailed feedback available

**Quick Insights Cards**:
- **Card Style**: Uses design-system/components/cards.md specifications
- **Card Type**: Compact insight cards with icon + text
- **Layout**: Horizontal scroll on mobile, 2-3 column grid on larger screens
- **Content**: One strength, one improvement area, one encouraging note

**Example Insights**:
- 💪 "Great conversation starter!"
- 🎯 "Work on maintaining eye contact"  
- ⭐ "Your confidence is improving!"

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Score Size**: 64px numeric display
- **Card Layout**: Single column with horizontal scroll
- **Spacing**: 16px margins, 12px card spacing
- **Vertical Hierarchy**: Score → Insights → Action hint

**Tablet (768-1023px)**:
- **Score Size**: 80px numeric display  
- **Card Layout**: 2-column grid with equal heights
- **Spacing**: 24px margins, 16px card spacing
- **Mixed Layout**: Score prominence with side-by-side insights

**Desktop (1024px+)**:
- **Score Size**: 96px numeric display
- **Card Layout**: 3-column grid with consistent spacing
- **Container Width**: Max 768px for optimal reading
- **Enhanced Graphics**: More prominent celebration elements

---

## Detailed Feedback State

### Purpose
Comprehensive breakdown of conversation performance with specific, actionable improvements.

### Layout Structure
- **Container**: Scrollable content with fixed header
- **Grid**: Card-based layout for different feedback categories
- **Spacing**: Generous whitespace for cognitive breathing room

### State: Feedback Overview

#### Visual Design Specifications

**Header Section**:
- **Score Summary**: Compact score display with edit/share options
- **Navigation**: Tab-style navigation between feedback sections
- **Breadcrumb**: Clear path back to score or forward to actions

**Content Sections**:
1. **Strengths Section** (Green theme)
2. **Improvements Section** (Orange theme) 
3. **Conversation Highlights** (Blue theme)
4. **Suggested Practice** (Purple theme)

**Card Specifications** (References design-system/components/cards.md):
- **Card Type**: Feedback cards with category-specific styling
- **Icon Usage**: Consistent iconography for each feedback type
- **Content Structure**: Title + 2-3 bullet points + optional example

#### Content Organization

**Strengths Section**:
- **Purpose**: Build confidence through specific positive recognition
- **Structure**: 2-3 specific strengths with conversation examples
- **Tone**: Encouraging and validating
- **Visual**: Green accent colors, positive icons

**Example Strengths**:
- "Natural conversation flow - you asked great follow-up questions"
- "Confident opener - your initial approach was friendly and appropriate"
- "Good energy matching - you adapted well to their response style"

**Improvements Section**:
- **Purpose**: Provide actionable, specific areas for growth
- **Structure**: 2-3 improvement areas with practical next steps
- **Tone**: Supportive and constructive, never critical
- **Visual**: Orange accent colors (brand primary), growth-focused icons

**Example Improvements**:
- "Try pausing more - give them space to respond fully"
- "Work on transitioning topics - your pivots felt slightly abrupt"
- "Practice compliments - look for natural opportunities to be positive"

### State: Deep Dive Analysis (Advanced)

#### Visual Design Specifications

**Conversation Timeline**:
- **Layout**: Vertical timeline showing conversation flow
- **Messages**: User messages with AI feedback annotations
- **Scoring**: Turn-by-turn micro-scores for advanced users
- **Highlights**: Key moments with detailed analysis

**Analysis Annotations**:
- **Good Moves**: Green highlights with positive feedback
- **Missed Opportunities**: Yellow highlights with suggestions
- **Learning Moments**: Orange highlights with teaching points
- **Alternative Responses**: Blue highlights with better options

**Interactive Elements**:
- **Expandable Sections**: Tap to see detailed analysis of each turn
- **Alternative Suggestions**: "You could have said..." with examples
- **Context Reminders**: Callbacks to pre-conversation context

#### Advanced User Features

**Carlos (Advanced) Specific Elements**:
- **Success Rate Metrics**: Comparison to similar scenarios
- **Optimization Insights**: "This approach works 78% of the time"
- **Advanced Techniques**: "Try the callback technique next time"
- **Performance Trends**: Week-over-week improvement graphs

**Deep Learning Tools**:
- **Conversation Replay**: Step through conversation with analysis
- **What-If Scenarios**: "If you had said X instead..."
- **Pattern Recognition**: "You tend to do this in most conversations"

---

## Progress Comparison State

### Purpose
Show skill development over time to motivate continued practice.

### State: Progress Overview

#### Visual Design Specifications

**Progress Visualization**:
- **Primary Chart**: Line graph showing score trends over time
- **Time Range**: Last 10 conversations or 2 weeks
- **Skill Breakdown**: Separate trend lines for key skill areas
- **Achievement Markers**: Notable milestones and improvements

**Skill Categories**:
- **Confidence**: Opening strength and overall energy
- **Flow**: Natural conversation progression
- **Appropriateness**: Context-appropriate responses
- **Engagement**: Keeping conversation interesting

**Visual Elements**:
- **Color Coding**: Each skill has consistent color throughout app
- **Trend Indicators**: Up/down arrows with percentage changes
- **Celebration Moments**: Badges for personal bests or breakthroughs
- **Goal Progress**: Progress toward user-defined skill goals

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Chart Style**: Simplified line chart with touch interactions
- **Data Points**: Last 5 conversations for readability
- **Layout**: Vertical stack of skill progress cards
- **Interaction**: Swipe between different skill views

**Tablet & Desktop (768px+)**:
- **Chart Style**: Full multi-line chart with hover details
- **Data Points**: Complete history with zoom/pan controls
- **Layout**: Chart + skill breakdown side-by-side
- **Interaction**: Rich hover states and detailed tooltips

---

## Action Selection State

### Purpose
Guide users to their next practice session based on feedback insights.

### State: Recommended Actions

#### Visual Design Specifications

**Action Cards Layout**:
- **Card Style**: CTA-focused cards using button component system
- **Priority Order**: Most recommended action appears first/largest
- **Visual Hierarchy**: Size and color coding based on recommendation strength

**Primary Recommendations**:
1. **Practice Again** (Same scenario/difficulty)
   - Icon: Repeat/refresh icon
   - Color: Primary-500 background
   - Context: "Master this scenario before moving on"

2. **Try Different Scenario** (Different context, same difficulty)
   - Icon: Explore/map icon  
   - Color: Secondary-500 background
   - Context: "Practice this skill level in a new setting"

3. **Increase Challenge** (Same scenario, higher difficulty)
   - Icon: Arrow up/level up icon
   - Color: Success-500 background
   - Context: "You're ready for the next challenge"

4. **Review Progress** (Go to profile/stats)
   - Icon: Chart/graph icon
   - Color: Info-500 background
   - Context: "See how far you've come"

**Recommendation Logic**:
- **High Score (80+)**: Suggest challenge increase or new scenario
- **Medium Score (60-79)**: Suggest same scenario practice or new context
- **Lower Score (<60)**: Suggest same scenario with tips focus
- **Plateau Pattern**: Suggest difficulty change or new scenarios

#### Interaction Specifications

**Card Interactions**:
- **Hover State**: Subtle scale (1.02x) with shadow enhancement
- **Press State**: Quick scale down (0.98x) with haptic feedback
- **Selection Transition**: Smooth transition to selected next screen
- **Loading State**: Selected card shows loading indicator during transition

**Secondary Actions**:
- **Skip to Menu**: Link to main navigation
- **Settings**: Quick access to user preferences
- **Help**: Feedback system help or support

---

## Error States

### Purpose
Handle technical failures gracefully while maintaining user confidence.

### State: Feedback Generation Failed

#### Visual Design Specifications

**Error Message Structure**:
- **Icon**: Friendly error icon (not alarming)
- **Primary Message**: "We couldn't analyze your conversation right now"
- **Secondary Message**: "But great job on completing the practice session!"
- **Recovery Options**: Retry analysis, skip to next action, or get basic feedback

**Fallback Feedback**:
- **Basic Score**: Simple completion-based score (e.g., "Practice Complete!")
- **Generic Tips**: 2-3 universally helpful conversation tips
- **Encouragement**: Focus on the fact they completed practice
- **Next Steps**: Same action options as normal feedback

### State: Network/Connectivity Issues

#### Visual Design Specifications

**Offline-Friendly Design**:
- **Cached Elements**: Show what feedback data is available locally
- **Sync Indicator**: Clear status of what will sync when online
- **Offline Badge**: Subtle indicator that device is offline
- **Retry Options**: Clear path to retry when connectivity returns

**Progressive Enhancement**:
- **Core Functionality**: Basic feedback always available
- **Enhanced Features**: Advanced analysis requires network
- **Clear Communication**: User understands what's available offline vs online

---

## Accessibility Specifications

### Screen Reader Experience

**Reading Order**:
1. Score announcement with context
2. Key insights in logical order
3. Improvement suggestions
4. Available actions with selection instructions

**ARIA Labels**:
- **Score Display**: "Conversation score: 78 out of 100, Good effort!"
- **Insight Cards**: "Strength: Natural conversation flow. Improvement: Try pausing more"
- **Action Buttons**: Clear action descriptions with context

### Keyboard Navigation

**Tab Order**:
1. Skip to main feedback content
2. Score/summary section (if interactive)
3. Insight cards (left to right, top to bottom)
4. Action buttons (primary to secondary)
5. Navigation options

**Keyboard Shortcuts**:
- **Space/Enter**: Activate focused button or expand focused card
- **Arrow Keys**: Navigate between insight cards
- **Escape**: Return to previous screen or show exit options

### Touch Accessibility

**Target Sizes**:
- **Minimum**: 44×44px for all interactive elements
- **Recommended**: 56×56px for primary actions
- **Card Interactions**: Full card area tappable where appropriate

**Haptic Feedback**:
- **Score Reveal**: Subtle celebration vibration for high scores
- **Button Press**: Standard selection feedback
- **Error States**: Gentle error feedback, not alarming

## Performance Specifications

### Loading Performance
- **Feedback Generation**: <3 seconds for AI analysis
- **Screen Transitions**: <300ms between states
- **Image/Icon Loading**: <200ms for all visual elements

### Animation Performance
- **Frame Rate**: 60fps maintained throughout all animations
- **Memory Usage**: Efficient cleanup of animation objects
- **Battery Impact**: Minimal battery drain from feedback animations

### Data Management
- **Caching**: Recent feedback cached for offline viewing
- **Sync**: Efficient sync of feedback data with server
- **Storage**: Minimal local storage impact

## Implementation Notes

### Component Mapping
- **Score Display**: Custom component with gamification elements
- **Insight Cards**: Standard card component with feedback-specific styling
- **Action Buttons**: Primary/secondary button components
- **Progress Charts**: Gamification component with custom data visualization

### State Management (Zustand)
- **Feedback State**: Score, insights, recommendations
- **Progress State**: Historical data and trend calculations  
- **Navigation State**: Next action routing and screen transitions
- **User Preferences**: Feedback verbosity and display options

### API Integration
- **POST /feedback/analyze**: Generate feedback from conversation data
- **GET /user/progress**: Historical performance for comparisons
- **POST /feedback/helpful**: User rating of feedback quality

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete user flow and decision points
- **[Interactions](./interactions.md)** - Detailed animation and interaction specifications
- **[Accessibility](./accessibility.md)** - Complete accessibility implementation
- **[Implementation](./implementation.md)** - Technical handoff and specifications

## Last Updated
- **Version 1.0.0**: Complete screen state specifications with responsive design
- **Focus**: Implementation-ready visual specifications with accessibility
- **Next**: Technical implementation and animation details