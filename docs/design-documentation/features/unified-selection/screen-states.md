# Unified Selection Feature - Screen States

---
title: Chat Tab - Unified Selection Screen States and Visual Specifications
description: Complete visual specifications for all states of the unified location and difficulty selection screen in the Chat tab
feature: chat-unified-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - interactions.md
  - accessibility.md
  - implementation.md
dependencies:
  - design-system/components/cards.md
  - design-system/tokens/colors.md
  - design-system/tokens/spacing.md
status: approved
---

## Screen Overview

**Tab Location**: Chat Tab

The unified selection screen in the Chat tab combines location browsing and difficulty selection in a single, elegant interface. This screen allows users to make selections and small customizations before AI generates randomized context. This document specifies all visual states, responsive behavior, and component interactions for comprehensive implementation guidance.

## Base Screen Layout

### Screen Structure
- **Total Height**: Full screen height minus safe areas and tab bar
- **Header Section**: 80px fixed height
- **Location Section**: 60% of remaining screen height
- **Difficulty Section**: 30% of remaining screen height  
- **Action Section**: 10% of remaining screen height (minimum 60px)

### Responsive Breakpoints
- **Mobile Portrait** (320-480px width): Single column, full-width components
- **Mobile Landscape** (481-767px width): Adjusted proportions, maintains single column
- **Tablet Portrait** (768-1024px width): Enhanced spacing, centered content
- **Tablet Landscape** (1025px+ width): Maximum width constraints, centered layout

## Header Section States

### Default Header State
**Layout**:
- **Background**: #FFFFFF (White) with 1px bottom border in #F3F4F6 (Neutral-100)
- **Height**: 80px including safe area padding
- **Content Padding**: 16px horizontal, 12px vertical

**Elements**:
- **Back Button**: 
  - Position: 16px from left edge, vertically centered
  - Icon: Left chevron, 24px size, #374151 (Neutral-700)
  - Touch Target: 44×44px
- **Title**: 
  - Text: "Create Your Practice Session"
  - Typography: H3 (20px/28px, 600 weight)
  - Color: #1F2937 (Neutral-800)
  - Position: Centered horizontally
- **Subtitle**:
  - Text: "Choose location and difficulty level"
  - Typography: Body Small (14px/20px, 400 weight)
  - Color: #6B7280 (Neutral-500)
  - Position: Centered, 4px below title

### Progress Indicator State
**Visual Design**:
- **Position**: Below subtitle, centered
- **Layout**: "Step 1 of 2" with progress dots
- **Active Dot**: 8px diameter circle in #F97316 (Primary)
- **Inactive Dot**: 8px diameter circle in #E5E7EB (Neutral-200)
- **Connection**: 2px line connecting dots in Neutral-200
- **Spacing**: 12px between dots, 24px from subtitle

## Location Selection Section States

### Section Container
**Layout**:
- **Background**: #F9FAFB (Neutral-50)
- **Height**: 60% of available screen height (minimum 240px)
- **Padding**: 24px top, 16px horizontal, 12px bottom
- **Border Radius**: None (full width section)

### Location Carousel States

#### Default Carousel State
**Container Specifications**:
- **ScrollView Height**: 180px (card height)
- **Horizontal Padding**: 48px (centers first/last cards)
- **Content Spacing**: 16px between cards
- **Scroll Behavior**: Horizontal only, momentum enabled, snap to center

**Individual Card Default State**:
- **Dimensions**: 280px × 180px
- **Border Radius**: 16px
- **Background**: White with image overlay
- **Shadow**: 0 2px 8px rgba(0, 0, 0, 0.1)
- **Border**: 3px solid transparent

**Card Image Specifications**:
- **Aspect Ratio**: 16:10 (fits 280×180 perfectly)
- **Overlay**: Linear gradient from transparent to rgba(0, 0, 0, 0.4) bottom 40%
- **Loading State**: Skeleton shimmer animation in #E5E7EB

**Card Text Specifications**:
- **Position**: Bottom-left with 16px padding from edges
- **Title**: H4 (18px/24px, 600 weight) in white
- **Text Shadow**: 0 1px 2px rgba(0, 0, 0, 0.6)

#### Location Card Selected State
**Visual Changes**:
- **Border**: 3px solid #F97316 (Primary) 
- **Shadow**: 0 4px 16px rgba(249, 115, 22, 0.25) (Primary shadow with opacity)
- **Scale**: Maintains 1:1 (no size change to preserve carousel layout)
- **Z-Index**: Elevated above adjacent cards

**Animation Specifications**:
- **Duration**: 200ms ease-out
- **Properties**: Border color, shadow values
- **Sequence**: Border appears first, shadow enhances simultaneously

#### Location Card Focus State (Accessibility)
**Visual Indicators**:
- **Focus Ring**: 3px solid #F97316 with 2px offset (total 5px from card edge)
- **Background**: Subtle highlight rgba(249, 115, 22, 0.1) over entire card
- **Announcement**: Screen reader announces location name and selection state

### Loading States

#### Initial Load State
**Carousel Container**:
- **Height**: 180px maintained
- **Background**: #F9FAFB (Neutral-50)

**Skeleton Cards**:
- **Count**: 3 visible skeleton cards
- **Dimensions**: 280px × 180px matching actual cards
- **Animation**: Shimmer effect from left to right every 2 seconds
- **Color**: Base #E5E7EB, highlight #F3F4F6

#### Image Loading State  
**Per Card**:
- **Background**: #E5E7EB (Neutral-200) base color
- **Loading Animation**: Shimmer effect over card area
- **Text**: "Location name" appears immediately, image loads progressively
- **Fallback**: Color-coded background if image fails (each location has unique color)

## Difficulty Selection Section States

### Section Container  
**Layout**:
- **Background**: #FFFFFF (White)
- **Height**: 30% of available screen height (minimum 140px, maximum 200px)
- **Padding**: 16px horizontal, 20px vertical
- **Border Top**: 1px solid #F3F4F6 (Neutral-100) separator from location section

### Difficulty Cards Layout
**Container**:
- **Display**: Horizontal flex with equal distribution
- **Gap**: 12px between cards
- **Alignment**: Center-aligned within container

**Individual Card Specifications**:
- **Width**: (Container width - 24px gap) / 3 (equal distribution)
- **Height**: 120px fixed
- **Border Radius**: 12px
- **Min Width**: 100px (prevents overcrowding on small screens)

### Difficulty Card States

#### Green (Friendly) Card States
**Default State**:
- **Background**: Linear gradient from #10B981 to #047857
- **Border**: None (transparent)
- **Shadow**: 0 2px 6px rgba(0, 0, 0, 0.1)
- **Content**: Icon (smile/thumbs up), "Friendly", "Open and encouraging"

**Selected State**:
- **Border**: 2px solid #065F46 (darker green)
- **Shadow**: 0 4px 12px rgba(0, 0, 0, 0.2)
- **Scale**: 1.05x with smooth animation
- **Duration**: 200ms ease-out

**Pressed State**:
- **Scale**: 0.98x (temporary during touch)
- **Opacity**: 0.9 (temporary during touch)
- **Duration**: 100ms immediate response

#### Yellow (Real Talk) Card States
**Default State**:
- **Background**: Linear gradient from #F59E0B to #D97706
- **Border**: None (transparent)
- **Shadow**: 0 2px 6px rgba(0, 0, 0, 0.1)
- **Content**: Icon (balance/conversation), "Real Talk", "Realistic interactions"

**Selected State**:
- **Border**: 2px solid #92400E (darker amber)
- **Shadow**: 0 4px 12px rgba(0, 0, 0, 0.2)
- **Scale**: 1.05x with smooth animation
- **Duration**: 200ms ease-out

**Pressed State**: Same as Green card

#### Red (A-Game) Card States  
**Default State**:
- **Background**: Linear gradient from #EF4444 to #DC2626
- **Border**: None (transparent)
- **Shadow**: 0 2px 6px rgba(0, 0, 0, 0.1)
- **Content**: Icon (fire/challenge), "A-Game", "Challenge yourself"

**Selected State**:
- **Border**: 2px solid #991B1B (darker red)
- **Shadow**: 0 4px 12px rgba(0, 0, 0, 0.2)
- **Scale**: 1.05x with smooth animation
- **Duration**: 200ms ease-out

**Pressed State**: Same as Green card

### Difficulty Card Content Layout
**Internal Structure** (all cards):
- **Padding**: 16px all sides
- **Icon**: 24px centered at top
- **Title**: Body Medium (16px/22px, 600 weight) centered below icon
- **Description**: Caption (12px/16px, 400 weight) centered at bottom
- **Text Color**: White (#FFFFFF) for all text elements
- **Text Shadow**: 0 1px 2px rgba(0, 0, 0, 0.3) for readability

## Action Section States

### Section Container
**Layout**:
- **Background**: #FFFFFF (White)
- **Height**: Minimum 60px, scales with content
- **Padding**: 16px horizontal, 12px vertical
- **Border Top**: 1px solid #F3F4F6 (Neutral-100) if needed for separation

### Create Scenario Button States

#### Disabled State (Default)
**Visual Design**:
- **Width**: Full width minus 32px margin (16px each side)
- **Height**: 48px
- **Background**: #E5E7EB (Neutral-200)
- **Border**: None
- **Border Radius**: 12px

**Text Specifications**:
- **Content**: "Create Scenario"
- **Typography**: Body Medium (16px/22px, 500 weight)
- **Color**: #9CA3AF (Neutral-400)
- **Alignment**: Center

**Helper Text**:
- **Content**: "Select location and difficulty to continue"
- **Typography**: Caption (12px/16px, 400 weight)
- **Color**: #6B7280 (Neutral-500)
- **Position**: Centered below button with 8px spacing

#### Enabled State
**Visual Design**:
- **Background**: #F97316 (Primary)
- **Border**: None  
- **Shadow**: 0 2px 6px rgba(249, 115, 22, 0.2)

**Text Specifications**:
- **Color**: #FFFFFF (White)
- **Typography**: Body Medium (16px/22px, 600 weight) - slightly bolder

**Animation**:
- **Transition**: 300ms ease-out from disabled to enabled
- **Properties**: Background color, text color, shadow
- **Sequence**: Background color changes first, shadow appears

#### Pressed State
**Visual Feedback**:
- **Scale**: 0.98x temporary scale
- **Background**: #EA580C (Primary darker shade)
- **Duration**: 100ms immediate response

#### Loading State
**Visual Design**:
- **Background**: #F97316 (Primary) maintained
- **Content**: Replaced with loading spinner + "Creating..."
- **Spinner**: 16px white spinner, centered
- **Text**: "Creating..." in white, positioned right of spinner
- **User Interaction**: Disabled during loading

## Error and Edge Case States

### Network Error State
**Location Carousel**:
- **Fallback**: Color-coded cards with location names only
- **Error Message**: "Images loading slowly - tap to select location"
- **Retry**: Pull-to-refresh gesture available

### Single Selection State
**Visual Feedback**:
- **Button**: Remains disabled with helper text
- **Selected Items**: Maintain selection styling
- **Unselected Section**: Subtle highlight around area needing selection

### Selection Change State
**Animation Behavior**:
- **Deselection**: Previous item smoothly returns to default (200ms)
- **New Selection**: New item animates to selected state (200ms)
- **Timing**: Deselection starts, new selection begins 100ms later for clarity

## Responsive Behavior

### Mobile Portrait (320-480px)
- **Location Cards**: 260px × 160px (slightly smaller)
- **Card Spacing**: 12px (reduced from 16px)
- **Difficulty Cards**: Minimum 95px width maintained
- **Font Sizes**: Maintain specified sizes for readability

### Mobile Landscape (481-767px)  
- **Section Heights**: Location 55%, Difficulty 35%, Action 10%
- **Carousel**: More cards visible simultaneously
- **Horizontal Padding**: Reduced to maximize card visibility

### Tablet Portrait (768-1024px)
- **Location Cards**: 320px × 200px (larger for better visual impact)
- **Maximum Width**: 600px centered container
- **Enhanced Spacing**: Increased padding throughout
- **Difficulty Cards**: Minimum 140px width for comfort

### Tablet Landscape (1025px+)
- **Two-Column Layout**: Locations left (60%), difficulty right (40%)
- **Maximum Width**: 800px centered
- **Card Grid**: 2×4 grid for locations, vertical stack for difficulty
- **Enhanced Touch Targets**: Larger interactive areas

## Animation Timing Summary

- **Card Selection**: 200ms ease-out
- **Button State Change**: 300ms ease-out
- **Touch Feedback**: 100ms immediate
- **Carousel Scroll**: Platform-native momentum
- **Screen Transitions**: 250ms ease-in-out
- **Loading States**: 2s shimmer cycle

## Accessibility States

### High Contrast Mode
- **Borders**: All selection borders increase to 4px width
- **Colors**: Enhanced contrast ratios maintain 7:1 minimum
- **Focus Rings**: High contrast mode specific focus indicators

### Large Text Mode
- **Dynamic Scaling**: All text scales with system font size
- **Layout Adaptation**: Cards expand vertically to accommodate larger text
- **Minimum Touch Targets**: Maintain 44×44px even with text scaling

### Reduced Motion Mode
- **Animations**: Scale and rotation animations disabled
- **Carousel**: Immediate snap without momentum scrolling
- **Selection**: Instant state changes without transitions
- **Loading**: Static indicators instead of animated spinners

## Implementation Notes

### State Management Requirements
- **Location Selection**: Single selection with clear deselection of previous choice
- **Difficulty Selection**: Single selection with clear deselection of previous choice  
- **Button Enablement**: Requires both selections to be valid
- **State Persistence**: Selections maintained during component lifecycle
- **Transition Data**: Complete selection data passed to next screen

### Performance Targets
- **Initial Render**: <200ms to first meaningful paint
- **Carousel Scroll**: 60fps smooth scrolling across all devices
- **Selection Feedback**: <50ms response to touch input
- **Image Loading**: Progressive loading without UI blocking
- **Memory Usage**: Efficient image caching and cleanup

## Last Updated
- **Version 1.0.0**: Complete screen state specifications with responsive design
- **Focus**: Comprehensive visual guidance for all user interaction states
- **Next**: Detailed interaction animations and accessibility implementation