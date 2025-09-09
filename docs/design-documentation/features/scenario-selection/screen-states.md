# Scenario Selection Screen States

---
title: Scenarios Tab - Pre-built Scenario Selection Screen States
description: Complete visual and interaction specifications for pre-built scenario browsing and selection in the Scenarios tab
feature: scenarios-tab-selection
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./interactions.md
  - ./accessibility.md
  - ./implementation.md
  - ../../design-system/components/cards.md
  - ../../design-system/components/buttons.md
  - ../../design-system/components/modals.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/tokens/spacing.md
dependencies:
  - Scenario content system
  - User preference engine
  - Difficulty calibration system
status: approved
---

## Screen: Scenario Selection Grid

### Purpose
Primary navigation screen where users browse and select conversation practice scenarios from 8 available locations with 3 difficulty levels each. The interface uses an infinity scroll design to create a sense of abundant content while maintaining easy navigation.

### Layout Structure
**Grid System:**
- **Mobile**: Single column with full-width cards
- **Tablet**: 2-column grid with 16px gutters
- **Responsive Padding**: 16px screen margins on mobile, 24px on tablet+
- **Card Spacing**: 16px vertical spacing between cards
- **Header**: Fixed header with user progress and settings access

### Content Strategy
Scenarios ordered by user familiarity and anxiety level:
1. **Coffee Shop** - Most approachable, daily scenario
2. **Bookstore** - Shared interest conversation starter
3. **Park** - Casual, outdoor environment
4. **Grocery Store** - Natural, everyday interaction
5. **Campus** - Relevant for younger users, structured environment  
6. **Gym** - Specific interest-based interaction
7. **Bar** - Social setting, moderate complexity
8. **Art Gallery** - Sophisticated setting, advanced conversation topics

---

## State: Default Grid View

### Visual Design Specifications

#### Header Section
**Layout:**
- **Height**: 64px + safe area top padding
- **Background**: White (`#FFFFFF`) with subtle bottom shadow
- **Content Alignment**: Space-between layout with centered title

**Elements:**
- **Title**: "Choose Your Scene" (H2, `#374151`)
- **Profile Avatar**: 32px circle, right-aligned, shows user progress ring
- **Progress Indicator**: Subtle ring around avatar showing weekly practice goal
- **Settings Icon**: 24px gear icon, accessible touch target

#### Scenario Cards
**Card Dimensions:**
- **Width**: Full-width minus 32px margins (mobile)
- **Height**: 200px fixed height for consistent grid
- **Border Radius**: 16px for modern, friendly appearance
- **Shadow**: `0 2px 8px rgba(0, 0, 0, 0.1)` for subtle elevation

**Background Treatment:**
- **Image**: High-quality lifestyle photography relevant to location
- **Overlay**: Gradient overlay from transparent to `rgba(0, 0, 0, 0.4)`
- **Purpose**: Ensures text readability over varying image backgrounds

**Content Layout:**
- **Location Title**: H3 typography (`20px/28px, 600`) in white
- **Position**: Bottom-left with 20px margins from edges
- **Text Shadow**: `0 1px 2px rgba(0, 0, 0, 0.5)` for readability
- **Description**: Body Small (`14px/20px`) in light gray, below title

**Difficulty Indicator:**
- **Position**: Top-right corner with 16px margins
- **Design**: Three dots representing Green/Yellow/Red difficulties
- **Default State**: All three dots shown in muted colors
- **Interaction**: Tapping expands to difficulty selection

#### Infinity Scroll Implementation
**Scroll Behavior:**
- **Loading**: 3 cards visible initially, more load as user scrolls
- **Performance**: Virtual rendering for smooth scrolling
- **Indicator**: Subtle loading animation at bottom when fetching more
- **End State**: Gentle fade indicating all content loaded

### Interactive Elements

#### Card Selection
**Default State:**
- Clean presentation with no selection indicators
- Subtle hover effect on capable devices (scale 102%)
- Shadow increases slightly on press

**Tap Interaction:**
1. **Initial Tap**: Card scales down to 98% with spring animation
2. **Difficulty Reveal**: Three difficulty buttons slide up from bottom
3. **Card Expansion**: Card height increases to 240px smoothly
4. **Background Dim**: Other cards fade to 70% opacity for focus

#### Difficulty Button Reveal
**Animation Sequence:**
- **Duration**: 300ms with ease-out timing
- **Green Button**: Slides up first with 100ms delay
- **Yellow Button**: Slides up second with 150ms delay  
- **Red Button**: Slides up third with 200ms delay
- **Staggered Effect**: Creates natural, playful reveal animation

**Button Specifications:**
- **Size**: 48px height for touch accessibility
- **Width**: Expands to fit text with 16px padding
- **Border Radius**: 24px for pill shape
- **Typography**: Button Medium (16px/20px, 500)
- **Spacing**: 8px gaps between buttons

---

## State: Difficulty Selection Active

### Visual Design Specifications

#### Expanded Card Layout
**Selected Card:**
- **Height**: 240px (expanded from 200px)
- **Background**: Maintains image with enhanced overlay
- **Border**: 2px solid Primary (`#F97316`) for clear selection indication
- **Shadow**: Enhanced shadow with primary color tint
- **Z-index**: Elevated above other cards

#### Difficulty Buttons

##### Green Button (Friendly)
**Visual Treatment:**
- **Background**: Success color (`#10B981`) with white text
- **Icon**: Smile or thumbs up (16px) preceding text
- **Text**: "🟢 Green (Friendly)"
- **Description**: "Open, welcoming, making eye contact"
- **States**: Default, hover (+10% brightness), active (scale 95%)

##### Yellow Button (Real Talk)  
**Visual Treatment:**
- **Background**: Warning color (`#F59E0B`) with dark text
- **Icon**: Neutral face or conversation bubble (16px)
- **Text**: "🟡 Yellow (Real Talk)"
- **Description**: "Realistic stranger behavior, neutral mood"
- **States**: Consistent with Green button interaction patterns

##### Red Button (A-Game)
**Visual Treatment:**
- **Background**: Error color (`#EF4444`) with white text
- **Icon**: Star or lightning bolt (16px) for challenge indication
- **Text**: "🔴 Red (A-Game)"  
- **Description**: "Reserved, busy, requires genuine skill"
- **States**: Consistent interaction patterns with slight red glow on active

#### Background Treatment
**Other Cards:**
- **Opacity**: Reduced to 60% to focus attention on selected card
- **Blur**: Subtle 2px blur effect for depth of field
- **Interaction**: Tapping other cards smoothly transitions selection
- **Animation**: Fade transition over 200ms

### Interaction Specifications

#### Difficulty Button Selection
**Selection Flow:**
1. **Button Press**: Scale to 95% with haptic feedback
2. **Confirmation**: Brief loading state (500ms) showing selection processing
3. **Transition**: Slide to pre-conversation context screen
4. **State Preservation**: Selected scenario and difficulty remembered for back navigation

#### Collapse Behavior
**Trigger Conditions:**
- User taps outside expanded card area
- User scrolls significantly (>50px)
- User taps system back button
- Auto-collapse after 30 seconds of inactivity

**Collapse Animation:**
- **Duration**: 250ms with ease-in timing
- **Sequence**: Difficulty buttons slide down in reverse order
- **Card**: Returns to 200px height smoothly
- **Background**: Other cards return to full opacity
- **Focus**: Returns to normal scroll state

---

## State: Loading and Error States

### Loading State
**Initial Page Load:**
- **Skeleton Cards**: 3 cards with animated shimmer effect
- **Colors**: Light gray placeholder with moving highlight
- **Duration**: Targets <2 seconds for scenario content loading
- **Accessibility**: Screen reader announcement of loading status

**Scenario Content Loading:**
- **Individual Cards**: Fade in as content loads with staggered timing
- **Images**: Placeholder to actual image crossfade
- **Progressive Enhancement**: Text loads first, images second

### Error States

#### Network Error
**Visual Treatment:**
- **Icon**: Wifi-off icon (48px) in muted color
- **Headline**: "Connection Issue" (H3)
- **Description**: "Check your internet connection and try again"
- **Action**: "Retry" button with primary styling
- **Layout**: Centered in screen with comfortable spacing

#### Content Loading Error
**Visual Treatment:**
- **Icon**: Alert triangle (48px) in warning color
- **Headline**: "Couldn't Load Scenarios" (H3)
- **Description**: "We're having trouble loading practice scenarios"
- **Actions**: "Retry" primary button, "Use Offline Mode" secondary
- **Fallback**: Local scenarios available for practice

#### Empty State (Future)
**For search or filtering results:**
- **Icon**: Search icon (48px) in muted color
- **Headline**: "No Scenarios Found" (H3)
- **Description**: "Try adjusting your search or preferences"
- **Action**: "Clear Filters" or "Browse All Scenarios"

---

## State: Accessibility and Navigation

### Screen Reader Optimization

#### Card Descriptions
**Semantic Structure:**
```jsx
<TouchableOpacity 
  role="button"
  accessibilityLabel="Coffee shop scenario. Choose difficulty level to practice conversation."
  accessibilityHint="Tap to see difficulty options: friendly, realistic, or challenging."
  onPress={handleCardSelection}
>
  <View role="img" accessibilityLabel="Coffee shop interior with people chatting">
    <Text role="heading" aria-level="3">Coffee Shop</Text>
    <Text>Practice casual conversation in a relaxed environment</Text>
  </View>
</TouchableOpacity>
```

#### Difficulty Button Accessibility
**Enhanced Labels:**
```jsx
<TouchableOpacity 
  accessibilityLabel="Green difficulty: Friendly and welcoming conversation partner"
  accessibilityHint="Best for beginners or building confidence"
  accessibilityRole="button"
>
  <Text>🟢 Green (Friendly)</Text>
</TouchableOpacity>
```

### Keyboard Navigation

#### Focus Management
**Tab Order:**
1. Header settings button
2. Profile/progress indicator  
3. First scenario card
4. Subsequent scenario cards in reading order
5. When expanded: difficulty buttons left to right

**Focus Indicators:**
- **Card Focus**: 2px outline in Primary color with 2px offset
- **Button Focus**: Consistent outline pattern
- **Skip Links**: "Skip to main content" for screen reader users

### Voice Control Support
**Voice Commands:**
- "Select [location name]" - Opens difficulty selection
- "Choose green difficulty" - Selects easiest option
- "Go back" - Collapses expanded card or navigates back
- "Show settings" - Opens user settings panel

---

## Performance Specifications

### Animation Performance
**60fps Target:**
- Use transform and opacity changes for animations
- Avoid layout thrashing during difficulty reveal
- Optimize blur effects for older devices
- Provide reduced motion alternatives

### Memory Management
**Image Loading:**
- Progressive JPEG loading for scenario backgrounds
- Image caching with LRU eviction
- Placeholder-to-actual smooth transitions
- Responsive image serving based on screen density

### Network Optimization
**Content Loading:**
- Scenario metadata loads first (fast)
- Images load progressively with placeholders
- Offline caching for repeated scenarios
- Bandwidth-appropriate image quality

---

*These screen states ensure the scenario selection experience is smooth, accessible, and confidence-building for all user types while maintaining technical performance standards.*