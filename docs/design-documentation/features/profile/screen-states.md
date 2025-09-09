# Profile Feature - Screen States

---
title: Profile Feature Screen States and Visual Specifications
description: Complete screen-by-screen visual design specifications for all profile management states
feature: profile
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - interactions.md
  - accessibility.md
  - implementation.md
  - ../../design-system/components/forms.md
  - ../../design-system/components/cards.md
  - ../../design-system/components/gamification.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/components/forms.md
  - ../../design-system/components/cards.md
  - ../../design-system/components/gamification.md
dependencies:
  - design-system/components
  - form components
  - gamification components
status: approved
---

## Screen States Overview

The profile feature includes 12 primary screen states covering profile creation, management, progress tracking, and privacy controls. Each state prioritizes user control, transparency, and clear value communication.

## Table of Contents

1. [Profile Creation States](#profile-creation-states)
2. [Profile Dashboard State](#profile-dashboard-state)  
3. [Preference Management States](#preference-management-states)
4. [Progress & Analytics States](#progress--analytics-states)
5. [Privacy & Settings States](#privacy--settings-states)
6. [Error & Edge Case States](#error--edge-case-states)

---

## Profile Creation States

### Purpose
Guide new users through profile setup with clear value proposition and privacy transparency.

### Layout Structure
- **Container**: Full screen with step indicator and progress tracking
- **Grid**: Form-focused layout with supporting visual previews
- **Spacing**: Generous whitespace (24px sections) for comfortable form completion

---

### State: Profile Introduction

#### Visual Design Specifications

**Header Section**:
- **Progress Indicator**: Step 1 of 5, subtle progress bar at top
- **Title**: "Let's personalize your practice" in H1, Neutral-900
- **Subtitle**: "Your preferences help create realistic conversation scenarios" in Body, Neutral-700

**Content Section**:
- **Value Proposition Card**: Light background (Primary-50) with border
  - **Icon**: Personalization icon (24px) in Primary-500
  - **Headline**: "Why we ask for this information"
  - **Benefits List**: 3 key benefits with checkmark icons
    - "Create age-appropriate conversation partners"
    - "Match scenarios to your dating goals"
    - "Personalize feedback to your learning style"

**Privacy Assurance**:
- **Security Badge**: Shield icon with "Your privacy matters" text
- **Privacy Summary**: Brief, clear explanation of data usage
- **Link**: "Full privacy policy" accessible link

**Action Buttons**:
- **Primary**: "Set up my profile" (Primary-500 button, full width)
- **Secondary**: "Skip for now" (text link, Neutral-600)

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Single Column**: All content stacked vertically
- **Card Padding**: 16px internal padding
- **Button Spacing**: 12px between primary and secondary actions
- **Text Scaling**: H1 scales to H2 size, Body remains readable

**Tablet (768-1023px)**:
- **Content Width**: Max 600px centered
- **Enhanced Spacing**: 20px card padding, 32px section margins
- **Side Illustrations**: Optional visual elements alongside content

**Desktop (1024px+)**:
- **Two Column Layout**: Content left, preview/illustration right
- **Fixed Width**: 800px max container for optimal reading
- **Enhanced Graphics**: More prominent visual elements showing personalization benefits

---

### State: Basic Demographics

#### Visual Design Specifications

**Form Structure**:
- **Progress**: Step 2 of 5, updated progress indicator
- **Form Container**: White background with subtle border (Neutral-200)
- **Field Spacing**: 20px between form fields for easy touch interaction

**Age Selection Field**:
- **Field Type**: Dropdown/picker with age range options
- **Label**: "Your age" with info icon explaining age-appropriate matching
- **Validation**: Real-time validation with helpful error messages
- **Design**: Uses design-system/components/forms.md specifications

**Location Field**:
- **Field Type**: City/region selector with type-ahead search
- **Label**: "Your general area" with privacy note "City level only - not shared publicly"
- **Placeholder**: "Type your city or region"
- **Privacy Indicator**: Lock icon showing data protection

**Visual Preview Section**:
- **Real-time Preview**: Shows how demographics affect AI partner generation
- **Example Cards**: 2-3 mini cards showing "Partners you might practice with"
- **Dynamic Content**: Updates based on user selections

#### Form Validation & Feedback

**Age Field Validation**:
- **Minimum Age**: 18+ required for dating-focused content
- **Error Message**: "You must be 18 or older to use FlirtCraft"
- **Alternative**: Link to general social skills resources for younger users

**Location Validation**:
- **Required Status**: Optional field with clear benefits explanation
- **Format Validation**: City/region format checking
- **Privacy Reassurance**: Visible privacy protection indicators

---

### State: Dating Preferences

#### Visual Design Specifications

**Preference Categories**:

**Gender Preferences Section**:
- **Layout**: Card-based selection with visual icons
- **Options**: 
  - "Men" (male icon)
  - "Women" (female icon) 
  - "Everyone" (inclusive icon)
- **Selection Style**: Radio button cards with clear selected state
- **Colors**: Selected cards show Primary-100 background, Primary-500 border

**Age Range Section**:
- **Component**: Dual-thumb range slider
- **Visual Style**: Primary-500 slider track with clear thumb indicators
- **Display**: Live updating text showing "Ages 22 to 35"
- **Constraints**: Reasonable ranges based on user's age

**Relationship Goals Section**:
- **Layout**: Multi-select cards (can choose multiple)
- **Options**:
  - "Casual dating" with coffee/drinks icon
  - "Serious relationships" with heart icon  
  - "General social skills" with conversation icon
- **Selection**: Multiple selections allowed with checkbox indicators

**Scenario Preview**:
- **Live Preview**: Real-time examples of conversation scenarios
- **Context Cards**: Mini context cards showing how preferences shape scenarios
- **Update Animation**: Smooth transitions when preferences change

#### Interaction Specifications

**Selection Feedback**:
- **Visual State Changes**: Clear selected/unselected states
- **Haptic Feedback**: Light haptic response on mobile for selections
- **Animation**: Subtle scale animation (1.02x) on selection
- **Preview Updates**: 300ms delay then smooth transition to new preview content

---

### State: Learning Goals & Skills

#### Visual Design Specifications

**Skills Selection Interface**:
- **Layout**: Grid of skill cards (2 columns on mobile, 3+ on larger screens)
- **Card Design**: Uses design-system/components/cards.md with skill-specific icons

**Skill Categories**:
1. **Conversation Starters**
   - Icon: Chat bubble with spark
   - Description: "Learn natural ways to begin conversations"
   
2. **Maintaining Flow**
   - Icon: Connected dots/flow lines
   - Description: "Keep conversations engaging and natural"
   
3. **Storytelling**
   - Icon: Book/story icon
   - Description: "Share experiences in compelling ways"
   
4. **Reading Signals**
   - Icon: Eye/awareness icon
   - Description: "Understand body language and social cues"
   
5. **Building Rapport**
   - Icon: Connected people
   - Description: "Create genuine connections quickly"

**Selection Mechanics**:
- **Multi-select**: Users can choose multiple skills
- **Priority Ranking**: Option to rank top 3 goals
- **Visual Hierarchy**: Selected skills show Primary-500 accent colors

**Progress Preview**:
- **Learning Path Visualization**: Timeline showing progression through selected skills
- **Estimated Timeline**: "Typically takes 3-4 weeks to see improvement"
- **Personalization Note**: How goals affect practice recommendations

---

### State: Progression Preferences

#### Visual Design Specifications

**Difficulty Progression Settings**:

**Progression Style Options**:
- **Conservative**: "Take it slow - I want to build confidence gradually"
  - Visual: Gentle slope chart
  - Color: Success-200 background
  
- **Balanced**: "Steady progress - challenge me when I'm ready"
  - Visual: Moderate slope chart  
  - Color: Primary-200 background
  
- **Aggressive**: "Push me - I want rapid improvement"
  - Visual: Steep slope chart
  - Color: Warning-200 background

**Feedback Preferences**:
- **Concise**: "Quick tips and scores"
- **Standard**: "Balanced feedback with specific suggestions" 
- **Detailed**: "In-depth analysis and conversation breakdown"

**Practice Frequency Goals** (Optional):
- **Casual**: "2-3 times per week"
- **Regular**: "Daily practice"
- **Intensive**: "Multiple sessions daily"

**Settings Preview**:
- **Simulation**: Shows example feedback style based on selections
- **Progression Chart**: Visual representation of chosen advancement pace
- **Reminder Settings**: Notification preferences aligned with frequency goals

---

## Profile Dashboard State

### Purpose
Central hub for profile overview, quick edits, and progress summary.

### State: Profile Overview Dashboard

#### Visual Design Specifications

**Header Section**:
- **User Summary**: Avatar placeholder, age, location (if provided)
- **Quick Stats**: Conversations completed, current streak, level indicator
- **Edit Button**: Prominent edit icon leading to preference updates

**Preference Summary Cards**:
- **Dating Preferences Card**: Gender, age range, relationship goals summary
- **Learning Goals Card**: Selected skills with progress indicators
- **Progression Settings Card**: Current difficulty level and advancement style
- **Privacy Settings Card**: Data sharing and privacy status overview

**Recent Activity Section**:
- **Practice Summary**: Last few conversation scores with trend indicators
- **Achievement Highlights**: Recent unlocks or milestones reached
- **Goal Progress**: Visual progress toward selected learning objectives

**Quick Actions**:
- **Start Practice**: Prominent CTA button leading to conversation
- **View Full Progress**: Link to detailed analytics
- **Update Preferences**: Quick access to preference editing

#### Responsive Layout

**Mobile (320-767px)**:
- **Single Column**: Cards stack vertically with 16px spacing
- **Collapsible Sections**: Advanced stats collapse behind "Show more"
- **Touch-Optimized**: Large touch targets for all interactive elements

**Tablet & Desktop (768px+)**:
- **Multi-Column Grid**: 2-3 column layout for preference cards
- **Sidebar Navigation**: Quick navigation to different profile sections
- **Enhanced Data Visualization**: Larger charts and progress indicators

---

## Preference Management States

### Purpose
Allow detailed editing of individual preference categories with immediate preview.

### State: Individual Preference Editing

#### Visual Design Specifications

**Edit Form Layout**:
- **Section Header**: Clear title, breadcrumb navigation, save/cancel options
- **Form Fields**: Match original creation forms with current values pre-filled
- **Live Preview**: Real-time examples of how changes affect AI generation
- **Change Detection**: Visual indicators of unsaved changes

**Dating Preferences Edit**:
- **Current Settings Display**: Clear showing of existing preferences
- **Modification Interface**: Same UI as creation flow but with existing data
- **Impact Preview**: Examples of how changes will affect future conversations
- **Revert Option**: Easy way to undo changes before saving

**Learning Goals Edit**:
- **Current Goals**: Visual display of selected skills with progress
- **Add/Remove Interface**: Easy skill addition/removal with drag-and-drop
- **Priority Adjustment**: Reorder goals by importance
- **Progress Impact Warning**: Note about how goal changes affect tracking

**Progression Settings Edit**:
- **Current Difficulty**: Display of current level and recent performance
- **Adjustment Options**: Recommendations based on recent performance
- **Preview of Changes**: How adjustment affects future conversation difficulty
- **Rollback Safety**: Option to revert if new settings don't work well

---

## Progress & Analytics States

### Purpose
Detailed progress visualization and achievement tracking for motivation and goal adjustment.

### State: Progress Overview

#### Visual Design Specifications

**Performance Dashboard**:
- **Overall Progress Chart**: Line graph showing score trends over time
- **Skill Breakdown**: Radar/spider chart showing progress in each skill area
- **Achievement Timeline**: Chronological display of unlocked achievements
- **Goal Progress**: Visual progress bars toward each learning objective

**Key Metrics Display**:
- **Total Conversations**: Count with trend indicator
- **Average Score**: Current average with improvement percentage
- **Streak Information**: Current and longest streaks
- **Time Invested**: Total practice time with weekly breakdown

**Trend Analysis**:
- **Performance Patterns**: Identification of improvement areas and plateaus
- **Difficulty Progression**: Chart showing advancement through difficulty levels
- **Goal Achievement Rate**: Progress toward learning objectives with timeline estimates

#### Interactive Elements

**Time Range Selector**:
- **Options**: Last week, month, 3 months, all time
- **Chart Updates**: Smooth transitions between time ranges
- **Comparative Data**: Option to compare periods

**Skill Deep Dive**:
- **Expandable Sections**: Click to see detailed breakdown of each skill
- **Sub-skill Tracking**: Individual components within each major skill
- **Improvement Recommendations**: Personalized suggestions based on data

---

### State: Achievement Gallery

#### Visual Design Specifications

**Achievement Layout**:
- **Grid Display**: Masonry/grid layout of achievement cards
- **Visual Hierarchy**: Recently unlocked achievements prominently displayed
- **Progress Indicators**: Partial progress toward locked achievements

**Achievement Card Design**:
- **Badge/Icon**: Unique visual identifier for each achievement
- **Title & Description**: Clear accomplishment description
- **Unlock Date**: When achievement was earned
- **Rarity Indicator**: How many users have unlocked this achievement

**Categories**:
- **Conversation Milestones**: Practice frequency and total conversation achievements
- **Skill Mastery**: Achievements for improving specific conversation skills
- **Progress Achievements**: Streak maintenance and consistency rewards
- **Special Recognition**: Unique or seasonal achievements

**Sharing Options** (Optional):
- **Social Sharing**: Ability to share achievements (with privacy controls)
- **Anonymous Leaderboards**: Optional competitive elements for motivated users
- **Personal Celebration**: Private achievement celebration animations

---

## Privacy & Settings States

### Purpose
Comprehensive privacy controls and data management with transparency and user control.

### State: Privacy Dashboard

#### Visual Design Specifications

**Data Usage Overview**:
- **What We Collect**: Clear categorization of collected data types
- **How It's Used**: Specific explanations of data usage for each category
- **Who Has Access**: Transparency about data access (user only, anonymized analytics, etc.)
- **Retention Periods**: How long different data types are kept

**Privacy Controls**:
- **Data Sharing Settings**: Granular controls for analytics, improvement research
- **Personalization Level**: Trade-off controls between privacy and personalization
- **Third-Party Integration**: Controls for any external service connections
- **Marketing Communications**: Opt-in/out controls for different communication types

**Account Management**:
- **Data Export**: Download all personal data in readable format
- **Account Deletion**: Clear process for account and data deletion
- **Data Portability**: Options for moving data to other services if available
- **Audit Log**: History of data access and modifications

#### User Control Specifications

**Granular Privacy Settings**:
- **Conversation Data**: Control over conversation history retention
- **Progress Analytics**: Opt-in for anonymized performance data sharing
- **Feature Improvement**: Participation in app improvement research
- **Personalization Data**: Control over AI personalization data usage

**Transparency Features**:
- **Data Impact Indicators**: Show how privacy choices affect app functionality
- **Regular Privacy Reviews**: Scheduled prompts to review and update privacy settings
- **Change Notifications**: Alerts when privacy policies or data usage changes
- **Clear Language**: Avoid legal jargon, use plain language explanations

---

## Error & Edge Case States

### Purpose
Handle various error conditions and edge cases gracefully while maintaining user trust.

### State: Profile Creation Errors

#### Visual Design Specifications

**Age Verification Failure**:
- **Clear Message**: "You must be 18 or older to use FlirtCraft's dating features"
- **Alternative Options**: Links to general social skills resources
- **Contact Information**: Support contact for edge cases or appeals
- **Design**: Non-punitive, helpful tone with constructive alternatives

**Network Connection Issues**:
- **Offline Indicator**: Clear indication that profile changes will sync when online
- **Local Storage**: Ability to continue with limited functionality offline
- **Sync Status**: Visual indicator of what's synced and what's pending
- **Retry Options**: Easy retry mechanisms when connectivity returns

**Data Validation Errors**:
- **Field-Specific Errors**: Clear, actionable error messages next to problematic fields
- **Format Examples**: Show correct format when validation fails
- **Progressive Validation**: Real-time validation that doesn't block user flow
- **Error Recovery**: Easy correction paths without losing other entered data

### State: Data Migration & Recovery

#### Visual Design Specifications

**Account Recovery Flow**:
- **Identity Verification**: Secure but user-friendly identity confirmation
- **Data Restoration**: Clear indication of what data is being restored
- **Conflict Resolution**: Handling conflicts between local and cloud data
- **Progress Indication**: Clear steps and progress through recovery process

**Device Migration**:
- **Export Process**: Step-by-step guide for backing up profile data
- **Import Process**: Easy restoration on new device
- **Verification Steps**: Ensuring data integrity during migration
- **Fallback Options**: Manual entry if automated migration fails

---

## Accessibility Specifications

### Screen Reader Experience

**Form Navigation**:
- **Logical Tab Order**: All forms follow visual layout for screen reader navigation
- **Field Labels**: Clear, descriptive labels for all form fields
- **Error Announcements**: Screen reader announcements for validation errors
- **Progress Indicators**: Accessible progress communication for multi-step forms

**Data Visualization Accessibility**:
- **Chart Alt Text**: Descriptive alternative text for all charts and graphs
- **Data Tables**: Accessible table alternatives to visual charts
- **Progress Descriptions**: Text descriptions of progress indicators
- **Achievement Descriptions**: Clear descriptions of visual achievement elements

### Keyboard Navigation

**Form Accessibility**:
- **Tab Navigation**: All interactive elements accessible via keyboard
- **Skip Links**: Quick navigation options for long forms
- **Keyboard Shortcuts**: Shortcut keys for common actions (save, cancel, next)
- **Focus Indicators**: Clear visual focus indicators throughout forms

### Motor Accessibility

**Touch Targets**:
- **Minimum Size**: 44×44px minimum for all interactive elements
- **Spacing**: Adequate spacing between touch targets
- **Alternative Inputs**: Voice input options for form fields where possible
- **Gesture Alternatives**: All gesture interactions have button/link alternatives

## Performance Specifications

### Loading Performance
- **Form Rendering**: <300ms for form appearance
- **Data Loading**: <1s for profile data retrieval
- **Preview Updates**: <200ms for real-time preview changes
- **Save Operations**: <500ms for preference updates with immediate UI feedback

### Data Management
- **Local Caching**: Recent profile data cached for offline viewing
- **Incremental Sync**: Only changed data synced to reduce bandwidth
- **Background Updates**: Non-critical updates happen in background
- **Conflict Resolution**: Smart merging of local and server changes

## Implementation Notes

### Component Usage
- **Form Fields**: Standard form components from design-system/components/forms.md
- **Cards**: Progress and preference cards from design-system/components/cards.md
- **Charts**: Progress visualization using gamification components
- **Buttons**: All button variants from design system with consistent styling

### State Management Integration
- **Profile Store**: Central profile data management with Zustand
- **Form State**: Local form state with optimistic updates
- **Sync Management**: Background synchronization with conflict resolution
- **Privacy Enforcement**: Real-time privacy setting enforcement

### API Integration Points
- **Profile CRUD**: Create, read, update, delete profile data
- **Progress Calculation**: Server-side progress and achievement calculation
- **Privacy Compliance**: GDPR/CCPA compliance for data requests
- **Analytics Integration**: Privacy-compliant analytics data collection

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete user flow and decision points
- **[Interactions](./interactions.md)** - Form interactions and animations
- **[Accessibility](./accessibility.md)** - Complete accessibility implementation
- **[Implementation](./implementation.md)** - Technical specifications and handoff

## Last Updated
- **Version 1.0.0**: Complete screen state specifications with accessibility and responsive design
- **Focus**: User control, privacy transparency, and clear personalization value
- **Next**: Technical implementation and form validation specifications