# Gamification Screen States

---
title: FlirtCraft Gamification Interface States
description: Complete visual specifications for XP bars, achievement galleries, streak displays, and progress dashboards
feature: gamification
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./interactions.md
  - ./accessibility.md
  - ./implementation.md
  - ../../design-system/components/gamification.md
  - ../../design-system/components/cards.md
  - ../../design-system/components/modals.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/animations.md
dependencies:
  - Design system components
  - Progress visualization library
  - Animation system
  - Local storage for state persistence
status: planned-phase-2
---

## Overview

This document provides comprehensive visual specifications for all interface states in FlirtCraft's gamification system, covering XP progress bars, achievement galleries, streak counters, leaderboard views, and progress dashboards across all responsive breakpoints and user scenarios.

## Table of Contents

1. [XP Bar States](#xp-bar-states)
2. [Achievement Gallery Screens](#achievement-gallery-screens)
3. [Streak Counter Displays](#streak-counter-displays)
4. [Progress Dashboard Views](#progress-dashboard-views)
5. [Level Up Celebrations](#level-up-celebrations)
6. [Notification States](#notification-states)
7. [Empty and Error States](#empty-and-error-states)

## XP Bar States

### XP Progress Bar Component

#### Default State
**Visual Specifications**:
- **Container**: 280px × 12px (mobile), 320px × 16px (desktop)
- **Background**: `Neutral-100` with `1px solid Neutral-200` border
- **Border Radius**: `8px` (rounded pill shape)
- **Progress Fill**: Linear gradient `#F97316` to `#EA580C`
- **Animation**: Smooth CSS transition `width 0.8s ease-out`

**Content Layout**:
- **Current XP Display**: Above bar, left-aligned, `Body` typography
- **Next Level XP**: Above bar, right-aligned, `Body Small` typography in `Neutral-600`
- **Level Indicator**: Circular badge on left, 32px diameter, `Primary` background
- **Progress Text**: "Level 3: 450 / 1,000 XP" format

**State Variations**:
```
Empty (0% progress):
- Progress bar: Empty background only
- Text: "Level 1: 0 / 200 XP to Level 2"
- Badge: "1" in white on Primary background

Partial Progress (45%):
- Progress bar: 45% filled with gradient
- Text: "Level 3: 450 / 1,000 XP to Level 4"
- Badge: "3" in white on Primary background

Near Full (95%):
- Progress bar: 95% filled, slight glow effect
- Text: "Level 3: 950 / 1,000 XP to Level 4"
- Badge: "3" with subtle pulse animation
- Additional: "50 XP needed!" encouragement text
```

#### XP Gain Animation State
**Visual Specifications**:
- **Fill Animation**: Progress bar fills from current to new position over 1.2s
- **Number Counter**: XP numbers animate with rolling counter effect
- **Glow Effect**: Temporary gold glow around progress during animation
- **Particle Effects**: Small gold sparkles appear at progress bar end

**Animation Sequence**:
1. **0-0.3s**: Preparation glow appears around entire bar
2. **0.3-1.2s**: Progress fill animates to new position with ease-out timing
3. **0.5-1.5s**: Number counter rolls up to new XP value
4. **1.0-1.8s**: Sparkle effects fade out
5. **1.8s+**: Return to default state with new progress

#### Near Level Up State
**Visual Specifications**:
- **Progress Bar**: 90%+ filled, continuous subtle glow pulse
- **Colors**: Enhanced gradient with brighter orange tones
- **Typography**: Level indicator pulses gently (0.8s cycle)
- **Encouragement**: "Almost there! 25 XP to Level 4" text below bar

**Interactive Elements**:
- **Tap Target**: Entire XP bar is tappable for detailed progress view
- **Hover State**: Slight brightness increase (desktop)
- **Active State**: Brief scale down (0.95x) with haptic feedback

### Detailed XP Progress Modal

#### Modal Layout Structure
**Container Specifications**:
- **Mobile**: Full screen overlay with top navigation
- **Tablet/Desktop**: Centered modal 480px × 600px
- **Background**: Blur overlay with `rgba(0, 0, 0, 0.6)`
- **Modal**: White background, `2xl` border radius, `xl` shadow

**Content Sections**:
1. **Header**: Current level and XP with large progress visualization
2. **XP Breakdown**: Sources of XP earned (conversations, bonuses, achievements)
3. **Level Benefits**: What unlocks at current level
4. **Next Level Preview**: Benefits and XP required for next level
5. **Historical Progress**: Last 7 days XP earning chart

#### XP Breakdown Section
**Visual Layout**:
- **Section Header**: "XP Earned This Week" in `H4` typography
- **Breakdown Items**: List format with icon, description, XP value
- **Item Spacing**: `md` vertical spacing between items
- **Icons**: 20px square with `Primary` color
- **XP Values**: Right-aligned with `Accent Primary` color

**Breakdown Item Examples**:
```
🗣️  Conversations Completed (12)        1,200 XP
⭐   First Conversation Daily Bonus (5)    250 XP  
🎯   Context Usage Bonus (8)              120 XP
🏆   Achievements Unlocked (2)            150 XP
📈   Difficulty Challenge Bonus (3)        75 XP
```

#### Historical Progress Chart
**Chart Specifications**:
- **Type**: Line chart with area fill
- **Dimensions**: Full modal width × 200px height
- **Data Points**: Last 7 days of XP earning
- **Colors**: `Primary` line with `Primary` 20% opacity area fill
- **Grid**: Subtle horizontal grid lines in `Neutral-100`
- **Labels**: Day abbreviations on X-axis, XP values on Y-axis

## Achievement Gallery Screens

### Achievement Gallery Overview

#### Grid Layout Structure
**Mobile Layout (320px - 767px)**:
- **Columns**: 2 achievements per row
- **Spacing**: `md` gap between cards
- **Card Size**: 140px × 160px per achievement
- **Margins**: `lg` container margins

**Tablet Layout (768px - 1023px)**:
- **Columns**: 3 achievements per row
- **Spacing**: `lg` gap between cards
- **Card Size**: 160px × 180px per achievement
- **Margins**: `xl` container margins

**Desktop Layout (1024px+)**:
- **Columns**: 4 achievements per row
- **Spacing**: `xl` gap between cards
- **Card Size**: 180px × 200px per achievement
- **Margins**: `2xl` container margins

#### Achievement Card States

**Unlocked Achievement Card**:
- **Background**: White with `sm` border radius and `sm` shadow
- **Border**: `2px solid Success` (green border for completed)
- **Icon**: Full-color achievement icon (48px × 48px)
- **Title**: `H5` typography in `Neutral-900`
- **Description**: `Caption` typography in `Neutral-600`, 2-line max
- **XP Reward**: `+50 XP` in `Success` color
- **Date Badge**: Completion date in top-right corner
- **Animation**: Gentle hover lift (2px translate) on desktop

**Locked Achievement Card**:
- **Background**: `Neutral-50` with `1px solid Neutral-200`
- **Icon**: Silhouette version in `Neutral-400`
- **Title**: `H5` typography in `Neutral-500`
- **Description**: `Caption` typography in `Neutral-400`
- **Progress**: Progress bar showing completion percentage
- **XP Reward**: `+50 XP` in `Neutral-400`
- **Interaction**: Tap to view progress details

**Secret Achievement Card** (Hidden until unlocked):
- **Background**: Gradient from `Neutral-100` to `Neutral-200`
- **Icon**: Question mark symbol in `Neutral-500`
- **Title**: "???" placeholder text
- **Description**: "Complete conversations to discover this achievement"
- **XP Reward**: Hidden until revealed
- **Visual Cue**: Subtle sparkle animation hints at hidden content

#### Category Filter Tabs
**Tab Bar Layout**:
- **Position**: Horizontal scroll above achievement grid
- **Background**: `Neutral-50` pill-shaped container
- **Active Tab**: `Primary` background with white text
- **Inactive Tab**: Transparent background with `Neutral-600` text
- **Spacing**: `sm` padding within tabs, `xs` gap between tabs

**Category Options**:
- All (shows total count badge)
- Getting Started (🌟)
- Consistency (⚡)
- Skill Development (🎯)
- Advanced (👑)
- Milestones (🏆)

### Achievement Detail Modal

#### Modal Structure
**Layout Specifications**:
- **Mobile**: Full-screen takeover with slide-up animation
- **Desktop**: Centered modal 520px × 400px with backdrop blur
- **Header**: Large achievement icon (80px) with title and category
- **Content**: Description, criteria, progress, and tips

**Achievement Progress Section**:
- **Progress Bar**: Current completion percentage with exact numbers
- **Criteria List**: Checkboxes showing individual completion requirements
- **Tips Section**: Helpful advice for completing the achievement
- **Related Achievements**: Suggestions for similar goals

**Visual Hierarchy**:
- **Achievement Icon**: Prominent display with completion glow if unlocked
- **Title**: `H2` typography with achievement category subtitle
- **Progress**: Visual progress bar with "3/10 conversations" format
- **Description**: `Body` typography explaining achievement value
- **XP Reward**: Emphasized reward display with gold accent

## Streak Counter Displays

### Streak Counter Component

#### Active Streak State
**Visual Design**:
- **Flame Icon**: 24px flame graphic in orange gradient
- **Counter**: Large number (current streak) in `H3` typography
- **Label**: "Day Streak" in `Body Small` underneath
- **Background**: Subtle orange glow (2px blur, 20% opacity)
- **Animation**: Gentle flame flicker animation (2s loop)

**Streak Milestone Indicators**:
```
Days 1-2: Small flame, orange color
Days 3-6: Medium flame, brighter orange with sparkles
Days 7-13: Large flame, gold accents, particle effects
Days 14+: Intense flame, multiple colors, crown icon addition
```

#### Streak Progress Ring
**Ring Specifications**:
- **Diameter**: 60px outer ring surrounding flame icon
- **Stroke Width**: 4px progress ring
- **Background Ring**: `Neutral-200` at 20% opacity
- **Progress Ring**: Orange gradient matching streak intensity
- **Animation**: Ring fills as day progresses (based on time of day)

**Daily Progress Logic**:
- Ring starts empty at midnight (user's timezone)
- Gradually fills throughout day as gentle reminder
- Completes when conversation is finished
- Resets at midnight for next day's progress

#### Streak Expiration Warning
**Warning State Visual**:
- **Flame Icon**: Flickers with reduced intensity
- **Counter**: Same large number but orange color fades to amber
- **Warning Text**: "3 hours left to maintain streak" in `Warning` color
- **Background**: Pulsing amber glow to draw attention
- **Action Button**: "Practice Now" CTA below counter

**Grace Period State**:
- **Flame Icon**: Half-intensity with hourglass overlay
- **Counter**: Number remains but with amber tint
- **Grace Text**: "Grace period - 12 hours remaining"
- **Visual Cue**: Gentle pulsing to indicate temporary state

### Streak Calendar View

#### Calendar Layout
**Monthly Calendar Grid**:
- **Grid**: 7×5 layout for days of month
- **Day Cell**: 32px × 32px squares with 2px gap
- **Current Day**: Bold border with `Primary` color
- **Today**: Special indicator if it's current day

**Streak Day Indicators**:
- **Practice Day**: Filled circle in `Success` color
- **Missed Day**: Empty circle with `Neutral-200` border
- **Current Streak**: Consecutive days connected with gradient line
- **Future Days**: Greyed out to indicate upcoming opportunities

**Visual Enhancements**:
- **Streak Lines**: Connect consecutive practice days with gradient line
- **Milestone Badges**: Special icons on 7-day, 14-day, 30-day milestones
- **Monthly Summary**: Stats below calendar (total days, longest streak)

## Progress Dashboard Views

### Weekly Progress Dashboard

#### Dashboard Layout Structure
**Container Organization**:
- **Header Section**: Week selector and summary stats
- **Primary Metrics**: Large cards for XP, conversations, achievements
- **Trend Charts**: Weekly progress visualization
- **Achievement Highlights**: Recently unlocked achievements

#### Primary Metrics Cards
**XP Card**:
- **Layout**: 140px × 100px card with rounded corners
- **Icon**: XP star icon in top-left (20px)
- **Primary Number**: Large XP total in `H2` typography
- **Comparison**: "+15% vs last week" in `Success` color
- **Background**: Subtle `Primary` gradient (5% opacity)

**Conversations Card**:
- **Layout**: Same size as XP card
- **Icon**: Chat bubble icon
- **Primary Number**: Conversation count in `H2`
- **Comparison**: Percentage change from previous week
- **Background**: Subtle `Secondary` gradient

**Achievement Card**:
- **Layout**: Same size as other cards
- **Icon**: Trophy icon
- **Primary Number**: New achievements unlocked
- **Comparison**: Progress toward next achievement
- **Background**: Subtle `Accent Primary` gradient

#### Weekly Trend Chart
**Chart Specifications**:
- **Type**: Combined bar and line chart
- **Dimensions**: Full container width × 200px height
- **Data**: Daily XP (bars) and cumulative progress (line)
- **Colors**: `Primary` for bars, `Secondary` for line
- **Interactive**: Hover to see daily details

### Monthly Analytics Dashboard

#### Comprehensive Analytics Layout
**Dashboard Sections**:
1. **Monthly Summary**: Key metrics and comparisons
2. **Skill Development**: Progress in conversation skill areas
3. **Practice Patterns**: When and how user practices most
4. **Achievement Progress**: Category completion and upcoming goals
5. **Confidence Tracking**: Self-reported improvement trends

#### Skill Development Section
**Skill Category Cards**:
- **Question Asking**: Progress bar with skill level indicator
- **Active Listening**: Visual meter showing improvement trend
- **Story Telling**: Chart showing storytelling frequency in conversations
- **Context Usage**: Percentage of conversations using pre-context effectively

**Visual Design**:
- **Progress Rings**: Circular progress indicators for each skill
- **Trend Lines**: Mini sparkline charts showing improvement over time
- **Skill Badges**: Visual indicators for skill milestones achieved
- **Comparison Metrics**: Month-over-month skill development

#### Practice Pattern Analytics
**Time-Based Insights**:
- **Heatmap**: Best practice times during week
- **Duration Chart**: Average conversation length trends
- **Consistency Metrics**: Practice frequency patterns
- **Optimization Suggestions**: "You're most engaged on Tuesday evenings"

## Level Up Celebrations

### Level Up Animation Sequence

#### Full-Screen Celebration (Mobile)
**Animation Timeline**:
- **0-0.5s**: Screen darkens with particle burst from center
- **0.5-1.5s**: Level badge scales up from center with bounce effect
- **1.0-2.0s**: "Level 4!" text appears with slide-down animation
- **1.5-2.5s**: XP progress bar animates to new level baseline
- **2.0-3.0s**: Achievement unlock notification if applicable
- **3.0s+**: Fade to normal interface with new level displayed

**Visual Elements**:
- **Particle System**: Gold and orange particles burst from center
- **Level Badge**: Large circular badge (120px) with new level number
- **Typography**: "Level Up!" in `H1` with golden glow effect
- **Background**: Dark overlay with subtle pattern texture
- **Audio Cue**: Celebratory sound effect (respects audio preferences)

#### Modal Celebration (Desktop)
**Centered Modal Layout**:
- **Size**: 400px × 500px centered modal
- **Background**: Blur backdrop with celebration theme
- **Animation**: Slides up from bottom with spring effect
- **Content**: Level badge, congratulatory text, new benefits list
- **CTA**: "Continue" button to return to normal interface

**New Level Benefits Display**:
- **Features Unlocked**: List of new app features or scenario types
- **Achievement Access**: New achievements now available to pursue
- **XP Multipliers**: Any XP earning bonuses gained
- **Visual Updates**: New avatar options or profile themes unlocked

## Notification States

### Achievement Unlock Notifications

#### In-App Banner Notification
**Visual Specifications**:
- **Position**: Top of screen, slides down from edge
- **Size**: Full width × 80px height
- **Background**: White with `Success` left border (4px)
- **Duration**: 4 seconds auto-dismiss, tap to dismiss early
- **Animation**: Slide down entrance, slide up exit

**Content Layout**:
- **Achievement Icon**: 40px icon on left side
- **Text Content**: "Achievement Unlocked: Weekly Warrior" title with brief description
- **XP Badge**: "+50 XP" on right side in `Success` color
- **Action**: Tap anywhere to view achievement details

#### Achievement Toast Notification
**Compact Notification Design**:
- **Position**: Bottom of screen with safe area consideration
- **Size**: 320px × 60px rounded pill shape
- **Background**: Semi-transparent dark with blur effect
- **Text**: White typography with achievement name and XP
- **Duration**: 3 seconds auto-dismiss

### XP Gain Notifications

#### Floating XP Counter
**Visual Design**:
- **Trigger**: Appears during conversation completion
- **Animation**: Floats up from XP bar location
- **Style**: "+125 XP" in large, bold typography
- **Color**: `Primary` color with golden glow
- **Duration**: 2-second animation with fade out
- **Physics**: Gentle bounce and float animation

**Bonus XP Stacking**:
- Multiple bonuses appear in sequence
- Each bonus floats up with slight offset
- Creates satisfying accumulation effect
- Final total emphasized with larger animation

## Empty and Error States

### Empty Achievement Gallery
**First-Time User State**:
- **Illustration**: Friendly graphic showing empty trophy case
- **Headline**: "Your achievements will appear here"
- **Description**: "Complete conversations to start unlocking achievements that celebrate your progress"
- **CTA Button**: "Start Your First Conversation"
- **Visual Style**: Light, encouraging with `Primary` color accents

### No Progress Data State
**New User Dashboard**:
- **Message**: "Complete a few conversations to see your progress analytics"
- **Illustration**: Chart icon with dotted lines suggesting future data
- **Encouragement**: "Your journey toward conversation confidence starts with practice"
- **CTA**: "Begin Practice Session"

### Streak Reset State
**After Missing Days**:
- **Flame Icon**: Grey/dormant version of streak flame
- **Message**: "Ready to start a new streak?"
- **Counter**: Shows "0" without discouragement
- **Motivation**: "Every expert was once a beginner"
- **CTA**: "Start New Streak Today"
- **Previous Best**: "Your longest streak was 12 days" as encouragement

### Error States

#### Progress Loading Error
**Visual Treatment**:
- **Icon**: Alert triangle in `Warning` color
- **Message**: "Unable to load progress data"
- **Explanation**: "Please check your connection and try again"
- **Actions**: "Retry" button and "View Offline" option

#### Achievement Sync Error
**Temporary State**:
- **Treatment**: Achievement cards show loading skeletons
- **Fallback**: Cached achievement data if available
- **User Message**: Subtle indicator that sync will continue in background
- **Graceful Degradation**: Core functionality remains available

---

## Responsive Design Specifications

### Mobile First (320px - 767px)
- **Stack Layout**: All dashboard elements in single column
- **Touch Targets**: Minimum 44px height for all interactive elements
- **Typography Scale**: Adjusted for mobile readability
- **Navigation**: Bottom tab bar for main sections
- **Margins**: `md` container margins for optimal content area

### Tablet (768px - 1023px)
- **Grid Layouts**: 2-column for most dashboard elements
- **Achievement Grid**: 3 columns for achievement gallery
- **Modal Sizes**: Larger modal dimensions for better content display
- **Hover States**: Light hover effects for touch-friendly interaction

### Desktop (1024px+)
- **Multi-Column**: Full dashboard layout with sidebar navigation
- **Achievement Grid**: 4-column layout for comprehensive view
- **Detailed Analytics**: Expanded chart sizes and data visualization
- **Keyboard Navigation**: Full keyboard accessibility for all elements
- **Hover Effects**: Rich hover states for enhanced desktop experience

---

## Related Documentation

- [Gamification Feature Overview](./README.md) - Complete system design and philosophy
- [Gamification User Journey](./user-journey.md) - User experience flow through all gamification elements
- [Gamification Interactions](./interactions.md) - Animation and interaction specifications
- [Gamification Accessibility](./accessibility.md) - Inclusive design implementation
- [Gamification Implementation](./implementation.md) - Technical specifications for all visual states

## Implementation Notes

### Performance Considerations
- **Animation Optimization**: Use CSS transforms and hardware acceleration
- **Chart Rendering**: Optimize chart libraries for smooth mobile performance
- **Image Assets**: SVG icons for scalability, optimized raster graphics for illustrations
- **Memory Management**: Efficient state management for progress data

### Platform Adaptations
- **iOS**: Native-feeling progress rings and celebration animations
- **Android**: Material Design elevation and motion principles
- **Web**: Smooth CSS animations with fallbacks for reduced motion preferences

---

*These screen state specifications ensure FlirtCraft's gamification system provides clear, engaging, and accessible progress visualization across all devices while maintaining the supportive, confidence-building experience central to the app's mission.*