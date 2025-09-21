# FlirtCraft Complete Screen Inventory

---
title: Complete Screen Inventory and Navigation Map
description: Comprehensive listing of all screens across MVP, Phase 2, and Phase 3 with navigation flows
feature: complete-app
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - ../design-system/style-guide.md
  - ./navigation/navigation-architecture.md
dependencies:
  - All feature modules
status: approved
---

## Overview

This document provides a complete inventory of every screen required for FlirtCraft across all development phases, with detailed specifications for layout, interactions, and state variations. Each screen is mapped to user personas and business requirements from the product specification.

## Core App Architecture

### Navigation Structure
- **Tab-based Navigation**: Primary app structure with 4 main tabs
  - **Home Tab**: Dashboard, daily stats, quick actions, detailed analytics, achievement gallery, skill tracking
  - **Chat Tab**: Custom conversation creation - unified location and difficulty selection with small tweaks → AI generates randomized context → chat
  - **Scenarios Tab**: Pre-built trending scenarios → select from curated options → AI generates templated context with variation → chat
  - **Profile Tab**: Personal info, preferences, account settings, app preferences, notifications, privacy, support
- **Stack Navigation**: Within each tab for deep navigation
- **Modal Overlay**: For critical flows (payments, settings)
- **Gesture Navigation**: Swipe between scenarios, pull-to-refresh

### Screen Categories
- **MVP Screens (P0)**: Essential for launch - 15 screens
- **Phase 2 Screens (P1)**: Post-launch enhancements - 8 screens  
- **Phase 3 Screens (P2)**: Growth features - 6 screens
- **Supporting Screens**: Error states, loading, transitions - 12 screens

## MVP Screens (Phase 1 - P0 Priority)

### 1. App Launch Sequence

#### 1.1 Splash Screen
**Purpose**: App initialization and brand impression
**Duration**: 1-3 seconds depending on load time
**Elements**:
- FlirtCraft logo (animated entrance)
- Tagline: "Build Confidence. Start Conversations."
- Loading indicator (subtle animation)
- App version number (corner)
**Success States**: 
- Cold start: Show logo animation then fade to onboarding/home
- Returning user: Quick flash then direct to home
**Error States**: 
- Network error: "Connect to continue" message with retry
- App update required: Direct to update prompt

#### 1.2 Age Verification Modal
**Purpose**: Legal compliance (18+ requirement)
**Trigger**: First app launch or cleared data
**Elements**:
- Clear title: "Age Verification Required"
- Explanation text about 18+ requirement
- Date picker (month/year sufficient for privacy)
- "I am 18 or older" checkbox
- "Continue" button (disabled until verified)
- "Exit App" option
**Validation**: 
- Must be 18+ to proceed
- Invalid age shows supportive message and app exit
**Accessibility**: Full screen reader support, keyboard navigation

### 2. Onboarding Flow (4 Screens)

#### 2.1 Welcome & Value Proposition
**Purpose**: Hook users with clear value and build initial trust
**Layout**: 
- Hero illustration (people chatting confidently)
- Primary headline: "Practice Makes Confident"
- Subheadline: "Master conversation starters in a safe, supportive environment"
- 3 key benefits (icon + text):
  - "Practice with AI partners"
  - "Build real confidence"  
  - "Safe, judgment-free space"
- Primary button: "Get Started"
- Secondary link: "Sign In" (for returning users)

#### 2.2 User Preferences Setup
**Purpose**: Collect essential targeting information for AI generation
**Form Elements**:
- **Your Age**: Number input (18-99 range)
- **Location Type**: Multi-select chips (Urban/Suburban/Campus/Rural)
- **Conversation Style**: 
  - Casual & Friendly
  - Confident & Direct
  - Thoughtful & Deep
  - Fun & Playful
- **Primary Goal**: Radio selection
  - Learn conversation starters
  - Practice maintaining conversations
  - Build overall confidence
  - Improve dating success
**Progress**: 2 of 5 indicator at top
**Navigation**: Back button, Continue button (validation required)

#### 2.3 Target Preferences
**Purpose**: AI partner generation parameters
**Sections**:
- **Practice Partner Gender**:
  - Men
  - Women  
  - Both (randomized)
  - Prefer not to specify
- **Age Range for Practice**: Dual slider (18-65 range)
- **Conversation Difficulty Preference**:
  - Start Easy (Green scenarios)
  - Balanced Mix (Green + Yellow)
  - Challenge Me (All difficulty levels)
**Privacy Note**: "This information stays private and is only used to create realistic practice scenarios"
**Progress**: 3 of 5 indicator
**Validation**: All sections required to continue

#### 2.4 Skill Goals & Interests
**Purpose**: Personalization for AI behavior and content recommendations
**Multi-Select Categories**:
- **Conversation Skills**:
  - Opening lines/ice breakers
  - Asking engaging questions
  - Reading social cues
  - Maintaining conversation flow
  - Showing genuine interest
  - Confident body language discussion
- **Scenario Interests** (affects scenario recommendations):
  - Coffee shops & cafes
  - Social gatherings & parties
  - Academic settings
  - Fitness & outdoor activities
  - Cultural events
  - Professional networking
**Selection**: Minimum 3, maximum 8 selections
**Progress**: 4 of 5 indicator


### 3. Core Experience Screens

#### 3.1 Home Dashboard
**Purpose**: Central hub combining dashboard, stats, and progress tracking
**Header Section**:
- Personalized greeting: "Good morning, [Name]!"
- Current streak indicator (flame icon + number)
- Today's progress toward daily goal
- XP/Level display with progress bar
**Quick Stats Cards** (horizontal scroll):
- Conversations completed this week
- Current confidence level (progress bar)
- New achievements (badge icons)
- Next recommended scenario
**Action Sections**:
- **Continue Practice**: Large primary button to scenario selection
- **Recent Conversations**: Last 3 with scores, tap to review feedback
- **Daily Challenge**: Special scenario with bonus XP
- **Progress This Week**: Visual chart of conversations and improvements
- **Detailed Analytics**: Performance trends, time spent practicing
- **Achievement Gallery**: Recent unlocks and progress toward next
- **Skill Tracking**: Individual skill progress bars with recommendations
**Bottom Navigation**: Home (active), Chat, Scenarios, Profile

#### 3.2 Chat Tab - Unified Selection Screen
**Purpose**: Combined location and difficulty selection for custom conversations
**Layout**:
- Header: "Create Your Practice Session"
- Subtitle: "Choose location and difficulty level"

**Location Selection (Top Section)**:
- **Horizontal Infinity Scroll**: Smooth momentum scrolling with snap-to-center
- **Visual Cards** (280px × 180px each):
  - Background image representing location
  - Location name overlay with gradient background
  - 16px spacing between cards
  - Peek preview showing ~20% of adjacent cards
  - Selected state with 3px Primary color border glow
- **8 Locations**: Coffee Shop, Bar/Lounge, Bookstore, Gym, Park, Campus, Grocery Store, Art Gallery

**Difficulty Selection (Bottom Section)**:
- **Three Cards**: Equal-width horizontal layout with 12px spacing
- **Card Design** (120px height):
  - Color-coded backgrounds (Green/Yellow/Red)
  - Icon, title, description, and success rate
  - Selection state with border highlight
- **Create Scenario Button**: Enabled only when both location and difficulty selected

#### 3.3 Scenarios Tab - Scenario Selection
**Purpose**: Choose from predefined practice scenarios  
**Layout**: 
- Header: "Practice Scenarios"
- Search bar: "Search scenarios..." (Phase 2 feature)
- Filter chips: All Difficulties, Green, Yellow, Red
**Scenario Grid** (infinity scroll):
Each scenario card shows:
- Background image (coffee shop, bookstore, etc.)
- Scenario name overlay
- Difficulty badges (🟢🟡🔴)
- Brief context preview: "Busy morning crowd, relaxed atmosphere"
- "Practice Here" button

**8 MVP Scenarios**:
1. **Coffee Shop**: Morning rush or quiet afternoon vibes
2. **Bookstore**: Literary atmosphere, intellectual conversations
3. **Park**: Outdoor setting, dog walking, exercise contexts
4. **Grocery Store**: Everyday errands, practical interactions
5. **Campus**: Academic environment, student life contexts
6. **Gym**: Fitness setting, health-focused conversations
7. **Bar/Lounge**: Evening social setting, more confident atmosphere
8. **Art Gallery**: Cultural setting, creative conversation starters

**Interaction Flow**:
Tap scenario → Difficulty selector slides up → Selection confirms → Pre-conversation context

#### 3.4 Scenarios Tab - Difficulty Selector (Modal Overlay)
**Purpose**: Choose conversation challenge level for selected predefined scenario
**Triggered**: From scenario card tap in Scenarios tab
**Layout**: Bottom sheet modal (40% screen height)
**Header**: "Select Difficulty Level"
**Options**:
- **🟢 Green - Friendly & Welcoming**
  - "Great for building confidence"
  - "Partner is open and encouraging"
  - "Perfect for beginners"
- **🟡 Yellow - Real Talk**
  - "Realistic stranger interactions"
  - "Practice authentic conversations"
  - "Most similar to real situations"
- **🔴 Red - Bring Your A-Game**
  - "Advanced conversation skills required"
  - "Partner is busy or reserved"
  - "Challenge yourself to improve"

**User Selection**: Tap difficulty → "Start Conversation" button appears
**Progress Indicators**: Show user's completion stats for each level

#### 3.5 Pre-Conversation Context
**Purpose**: Provide realistic scenario context for conversation preparation
**Loading State**: 
- "AI is creating your practice scenario..."
- Progress indicator (2-4 seconds)
- Animated illustration showing scenario setup

**Context Display** (4 sections):
- **Appearance Cues**: 
  - Age range and style description
  - No names (privacy/safety)
  - Respectful, observable details only
  - Example: "Mid-20s, casual athletic wear, reading while waiting for coffee"

- **Environment Details**:
  - Time context and crowd level
  - Ambient details that affect conversation
  - Example: "Tuesday morning, moderately busy, soft jazz playing, line is short"

- **Body Language Signals**:
  - Color-coded receptiveness indicators
  - 🟢 "Open posture, making brief eye contact, smiling occasionally"
  - 🟡 "Focused on task, neutral expression, approachable if engaged naturally"
  - 🔴 "Busy, checking phone, earbuds in, quick interaction window"

- **AI Conversation Starters**:
  - 3-4 contextual conversation openers
  - User can tap to use directly or modify
  - Example: "That book looks interesting - how are you liking it?"

**Actions**:
- "Start Conversation" (primary button)
- "Get Different Context" (regenerate - limited uses)
- Back to scenario selection

#### 3.6 Active Conversation Interface
**Purpose**: Real-time practice conversation with AI partner
*Note: Already comprehensively documented in existing conversation/README.md*
**Key Additional Specifications**:

**Conversation Limits**:
- Maximum 12 minutes OR 50 total messages (25 each)
- Progress indicators show approaching limits
- Natural wrap-up suggestions as limits approach

**Context Integration**:AI 
- AI maintains full awareness of pre-conversation context
- References environment and appearance cues naturally
- Body language affects AI response enthusiasm/receptiveness

**Help Features**:
- "Need help?" button reveals conversation starter panel
- Triggers after 30 seconds of inactivity or multiple deletions
- Context-aware suggestions based on current conversation state

#### 3.7 Post-Conversation Feedback
**Purpose**: Provide encouraging feedback and improvement guidance
**Score Presentation**:
- Animated circular progress showing score (1-100)
- Color-coded: Green (80+), Yellow (60-79), Red (below 60)
- Celebration animation for high scores

**Feedback Categories**:
- **Conversation Flow**: How natural the interaction felt
- **Confidence Level**: Boldness and assertiveness displayed  
- **Engagement**: How well you kept the conversation interesting
- **Appropriateness**: Staying within comfortable boundaries

**Specific Feedback**:
- 3-5 specific tips per conversation
- Positive reinforcement for successful elements
- Constructive suggestions for improvement
- Example: "Great opening! Your book comment felt natural and showed genuine interest."

**Progress Tracking**:
- Improvement compared to previous conversations
- Skill-specific progress bars
- New achievements unlocked

**Next Steps**:
- "Practice Again" (same scenario/difficulty)
- "Try Different Scenario" → scenario selection
- "View Progress" → progress dashboard
- "Share Success" (social features - Phase 2)

### 4. User Management Screens

#### 4.1 User Profile
**Purpose**: Personal information, preferences, and account management
**Profile Section**:
- Profile avatar (initials or uploaded image)
- Display name and basic info
- Member since date
- Account type (Free/Premium)

**Preferences**:
- Practice partner preferences (gender, age range)
- Conversation style preferences
- Notification settings
- Difficulty level recommendations

**Privacy & Data**:
- Data usage overview
- Conversation history settings
- Privacy policy access
- Delete account option

**App Settings**:
- Dark mode toggle
- Sound effects toggle  
- Haptic feedback toggle
- Language selection (future)

#### 4.2 Settings Dashboard
**Purpose**: App configuration and user preferences management
**Categories**:

**Practice Settings**:
- Default difficulty preference
- Practice reminders schedule
- Daily goal setting (conversations per day)
- Auto-advance to next difficulty

**Privacy & Security**:
- Conversation data retention
- Analytics participation
- Biometric authentication (future)
- Two-factor authentication (future)

**Accessibility**:
- Text size adjustment
- Color contrast options
- Reduced motion toggle
- Screen reader optimizations

**Notifications**:
- Daily practice reminders
- Achievement notifications
- New feature announcements
- Streak maintenance reminders

### 5. Supporting Screens

#### 5.1 Loading States
**App Launch**: Splash screen with progress indicator
**Context Generation**: "Creating your practice scenario..." with animation
**AI Response**: Typing indicator in conversation
**Screen Transitions**: Smooth animations between screens

#### 5.2 Error States
**Network Error**: "Connection lost" with retry options
**AI Service Error**: "Practice partner temporarily unavailable"
**Age Verification Failed**: Supportive message with app exit option
**Invalid Input**: Helpful validation messages with correction guidance

## Phase 2 Screens (P1 Priority)

### 1. Advanced Progress & Analytics

#### 1.1 Progress Dashboard
**Purpose**: Detailed analytics and improvement tracking
**Overview Cards**:
- Weekly conversation count with trend
- Average confidence score progression
- Streak counter with historical best
- Skill improvement percentages

**Detailed Analytics**:
- Line charts showing score improvements over time
- Skill breakdown radar chart
- Scenario-specific performance
- Difficulty level progression

**Achievement Gallery**:
- Earned badges display
- Progress toward next achievements
- Rare achievement highlights
- Social sharing options

#### 1.2 Advanced Feedback Analytics
**Purpose**: Deep-dive conversation analysis
**Conversation History**:
- Calendar view of practice sessions
- Filterable by scenario, difficulty, score
- Tap to review specific conversation feedback

**Skill Progression Charts**:
- Individual skill tracking over time
- Comparison to user average
- Benchmarking against community (anonymous)
- Improvement rate calculations

**Personalized Insights**:
- AI-generated improvement suggestions
- Pattern recognition in conversation strengths/weaknesses
- Personalized practice recommendations
- Goal setting and tracking

### 2. Premium Features

#### 2.1 Premium Upgrade Screen
**Purpose**: Convert free users to premium subscription
**Value Proposition**:
- Unlimited daily conversations (vs 1 free)
- Advanced scenarios (formal events, speed dating)
- Detailed analytics and insights
- Priority AI response times
- Custom scenario creation

**Pricing Tiers**:
- Monthly subscription option
- Annual subscription (discount highlighted)
- Lifetime purchase option
- Free trial period

**Social Proof**:
- User testimonials
- Success statistics
- "Most popular" plan highlighting

#### 2.2 Subscription Management
**Purpose**: Manage premium subscription settings
**Current Plan**:
- Subscription status and next billing date
- Usage statistics (conversations used)
- Plan benefits overview

**Account Actions**:
- Upgrade/downgrade plan
- Cancel subscription
- Update payment method
- View billing history

### 3. Social & Community Features

#### 3.1 Achievement Gallery
**Purpose**: Showcase user progress and motivate continued use
**Achievement Categories**:
- Conversation milestones (10, 50, 100 conversations)
- Skill achievements (confidence master, conversation starter)
- Streak achievements (7-day, 30-day streaks)
- Scenario completion (all locations mastered)

**Display Format**:
- Badge grid with progress indicators
- Achievement details on tap
- Earning date and rarity information
- Share achievement option

## Phase 3 Screens (P2 Priority)

### 1. Community Features

#### 1.1 Community Forum
**Purpose**: Anonymous peer support and advice sharing
**Feed Structure**:
- Recent discussions (newest first)
- Popular topics (engagement-based)
- Category filters (beginner tips, success stories, challenges)

**Discussion Features**:
- Anonymous posting with optional personas
- Comment threading
- Voting system (upvote/downvote)
- Report inappropriate content

**Moderation**:
- Community guidelines prominent
- Easy reporting system
- Moderator responses and updates

#### 1.2 Success Stories Feed
**Purpose**: Share and celebrate dating success stories
**Story Format**:
- Title and brief summary
- Before/after confidence scores
- Key techniques used
- Community reactions

**Privacy**:
- Complete anonymization options
- Optional location/age context
- User control over story visibility

### 2. Advanced Practice Features

#### 2.1 Group Challenges
**Purpose**: Social motivation through friendly competition
**Challenge Types**:
- Weekly conversation goals
- Skill-specific challenges
- Scenario completion races
- Streak maintenance

**Social Elements**:
- Team formation (anonymous)
- Progress sharing
- Encouragement system
- Celebration of group achievements

#### 2.2 Voice Practice Mode
**Purpose**: Audio conversation practice
**Interface Adaptations**:
- Voice recording controls
- Audio playback of AI responses
- Speech pattern analysis
- Conversation confidence scoring

**Advanced Features**:
- Accent adaptation options
- Speed variation practice
- Real-time tone feedback
- Phone call simulation mode

## Navigation Architecture

### Tab Structure (Bottom Navigation)
1. **Home**: Dashboard, daily stats, quick actions, detailed analytics, achievement gallery, skill tracking
2. **Chat**: Custom conversation practice (unified selection → AI-generated randomized context → chat)
3. **Scenarios**: Pre-built trending scenarios (selection → AI-generated templated context → chat)
4. **Profile**: Personal information, preferences, account settings, app preferences, notifications, privacy, support

### Stack Navigation Within Tabs
**Home Tab Stack**:
Home Dashboard → Detailed Analytics View → Achievement Details → Skill Progress Details

**Chat Tab Stack**:
Unified Selection (Location + Difficulty) → Context Creation (blank) → Pre-Conversation Context → Active Conversation → Post-Conversation Feedback

**Scenarios Tab Stack**:
Scenarios List → Scenario Details → Context Creation (template) → Pre-Conversation Context → Active Conversation → Post-Conversation Feedback

**Profile Tab Stack**:
Profile Overview → Personal Information → Preferences → Account Settings → App Preferences → Notifications → Privacy → Support

### Modal Overlays
**System-Level Modals**:
- Age verification (app launch)
- Premium upgrade prompts
- Critical error messages
- Onboarding flow

**Feature-Level Modals**:
- Difficulty selector
- Conversation starters panel
- Achievement celebration
- Confirmation dialogs

## Screen State Specifications

### Loading States
**Skeleton Screens**: For content-heavy screens during load
**Progress Indicators**: For processes with known duration
**Spinners**: For quick server requests
**Animated Placeholders**: For AI content generation

### Error States
**Network Errors**: Retry mechanisms with offline mode indications
**Service Errors**: Clear explanations with alternative actions
**User Errors**: Helpful validation with correction guidance
**Critical Errors**: Graceful degradation with support contact

### Empty States
**First Use**: Onboarding guidance and clear next steps
**No Data**: Encouraging messaging with clear actions
**No Results**: Alternative suggestions and search refinement
**Completed States**: Celebration and next challenge presentation

### Success States
**Achievement Unlocks**: Animated celebration with sharing options
**Milestone Completion**: Progress acknowledgment and next goals
**Successful Actions**: Clear confirmation with relevant next steps
**Progress Indicators**: Visual feedback on improvement

## Implementation Priorities

### MVP Implementation Order
1. **Core Onboarding**: Age verification through preference setup (highest impact)
2. **Practice Flow**: Scenario selection through feedback (core value)
3. **Basic Dashboard**: Home screen with essential features
4. **Profile Management**: Basic settings and preferences

### Phase 2 Implementation Order
1. **Progress Analytics**: Detailed tracking and insights
2. **Premium Features**: Subscription and advanced content
3. **Achievement System**: Gamification and motivation

### Phase 3 Implementation Order
1. **Community Features**: Social support and sharing
2. **Voice Practice**: Advanced interaction modes
3. **Advanced Analytics**: Deep learning insights

---

*This complete screen inventory ensures comprehensive coverage of all FlirtCraft features across development phases, providing clear implementation guidance for the development team.*