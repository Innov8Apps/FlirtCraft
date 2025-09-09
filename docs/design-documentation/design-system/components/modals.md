# Modal Components

---
title: FlirtCraft Modal Components
description: Difficulty selectors, alerts, premium upsells, help dialogs, and overlay interfaces
feature: scenario-selection, feedback, onboarding, premium
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ./buttons.md
dependencies:
  - React Native Modal
  - NativeBase AlertDialog, ActionSheet
  - React Native Reanimated
status: approved
---

## Overview

Modal components in FlirtCraft provide contextual overlays for secondary actions, confirmations, and focused interactions. Each modal type is designed to maintain user flow while presenting necessary information or choices without full navigation.

## Modal Architecture

### Modal Presentation Types
1. **Bottom Sheet Modals** - Primary choice for mobile-friendly interactions
2. **Center Modals** - Alerts, confirmations, and focused content
3. **Full Screen Modals** - Complex forms and detailed content
4. **Action Sheets** - Quick action selection

## Component Specifications

### Difficulty Selection Modal

#### Purpose
Overlay for selecting conversation difficulty after choosing a scenario location.

#### Visual Specifications

**Backdrop:**
- **Background**: `rgba(0, 0, 0, 0.5)` – Semi-transparent overlay
- **Blur Effect**: `blur(2px)` on background content (iOS) or dim effect (Android)
- **Tap Behavior**: Tap outside modal to dismiss

**Modal Container:**
- **Style**: Bottom sheet presentation
- **Background**: `#FFFFFF` (White)
- **Border Radius**: `16px` top corners only
- **Max Height**: `60%` of screen height
- **Shadow**: `0 -4px 16px rgba(0, 0, 0, 0.15)` – Upward elevation

**Drag Handle:**
- **Width**: `32px`
- **Height**: `4px`
- **Color**: `#D1D5DB` (Neutral-300)
- **Position**: Centered, 12px from top
- **Purpose**: Visual affordance for drag-to-dismiss

**Header Section:**
- **Padding**: `20px 20px 16px 20px`
- **Selected Scenario**: Small scenario preview card
- **Title**: "Choose Your Difficulty Level"
- **Subtitle**: "Each level offers different conversation challenges"

#### Difficulty Option Cards

**Card Layout:**
- **Height**: `80px` per option
- **Margin**: `8px` between cards
- **Padding**: `16px`
- **Border Radius**: `12px`
- **Background**: `#FFFFFF` (White)
- **Border**: `2px solid #E5E7EB` (Neutral-200)

**🟢 Green (Friendly) Option:**
- **Accent Color**: `#10B981` (Success)
- **Icon**: Smiling face or thumbs up (24px)
- **Title**: "Green (Friendly)" in Success color
- **Description**: "They're open and receptive to conversation"
- **Best For**: "Building confidence and practicing basics"
- **AI Behavior Note**: "Welcoming, encouraging, patient responses"

**🟡 Yellow (Real Talk) Option:**
- **Accent Color**: `#F59E0B` (Warning)  
- **Icon**: Neutral face or balance scale (24px)
- **Title**: "Yellow (Real Talk)" in Warning color
- **Description**: "Natural stranger interaction - realistic responses"
- **Best For**: "Practicing real-world scenarios"
- **AI Behavior Note**: "Neutral, authentic, requires genuine engagement"

**🔴 Red (A-Game) Option:**
- **Accent Color**: `#EF4444` (Error)
- **Icon**: Challenging face or target (24px)
- **Title**: "Red (A-Game)" in Error color
- **Description**: "They're busy or reserved - bring your best approach"
- **Best For**: "Challenging yourself and advanced skills"
- **AI Behavior Note**: "Initially disinterested, requires skill to engage"

**Selection States:**
- **Default**: Light border, white background
- **Hover**: Subtle background tint in accent color (5% opacity)
- **Selected**: Border changes to accent color, background to 10% opacity
- **Focus**: Focus ring in accent color

**Footer Actions:**
- **Primary**: "Start Conversation" button (full-width, enabled only after selection)
- **Secondary**: "Back to Scenarios" link
- **Spacing**: 20px padding all around

#### Animation Behavior
- **Entrance**: Slide up from bottom (400ms ease-out)
- **Exit**: Slide down to bottom (300ms ease-in)
- **Selection**: Smooth color transition (200ms ease-out)
- **Drag Dismissal**: Follows finger with spring physics

#### NativeBase Implementation
```jsx
<ActionSheet
  isOpen={isOpen}
  onClose={onClose}
  size="lg"
>
  <ActionSheet.Content>
    <ActionSheet.DragIndicator />
    
    <VStack space={4} p={5}>
      <VStack space={2} alignItems="center">
        <Text fontSize="lg" fontWeight="semibold">
          Choose Your Difficulty Level
        </Text>
        <Text fontSize="sm" color="gray.500" textAlign="center">
          Each level offers different conversation challenges
        </Text>
      </VStack>

      <VStack space={3}>
        {difficultyOptions.map((option) => (
          <Pressable
            key={option.level}
            onPress={() => setSelected(option.level)}
            _pressed={{ opacity: 0.8 }}
          >
            <Box
              p={4}
              borderRadius={12}
              borderWidth={2}
              borderColor={selected === option.level ? option.color : "gray.200"}
              bg={selected === option.level ? `${option.colorScheme}.50` : "white"}
            >
              <HStack space={3} alignItems="center">
                <Icon as={option.icon} size="6" color={`${option.colorScheme}.500`} />
                <VStack flex={1} space={1}>
                  <Text fontSize="md" fontWeight="medium" color={`${option.colorScheme}.600`}>
                    {option.title}
                  </Text>
                  <Text fontSize="sm" color="gray.600">
                    {option.description}
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    Best for: {option.bestFor}
                  </Text>
                </VStack>
              </HStack>
            </Box>
          </Pressable>
        ))}
      </VStack>

      <Button
        onPress={onStartConversation}
        isDisabled={!selected}
        size="lg"
        colorScheme="primary"
      >
        Start Conversation
      </Button>
    </VStack>
  </ActionSheet.Content>
</ActionSheet>
```

### Confirmation Dialog

#### Purpose
User confirmation for destructive or significant actions (end conversation, delete data, etc.).

#### Visual Specifications

**Modal Container:**
- **Style**: Center modal presentation
- **Width**: `300px` mobile, `400px` tablet+
- **Background**: `#FFFFFF` (White)
- **Border Radius**: `16px` all corners
- **Shadow**: `0 8px 24px rgba(0, 0, 0, 0.15)` – Strong elevation
- **Position**: Centered on screen

**Content Structure:**
- **Icon**: Contextual icon (48px) at top - warning, question, or info
- **Title**: H3 typography (20px/28px, 600 weight)
- **Description**: Body text (16px/22px, 400 weight) in Neutral-600
- **Spacing**: 16px between elements

**Button Layout:**
- **Style**: Horizontal button pair
- **Primary Action**: Right-aligned, appropriate semantic color
- **Secondary Action**: Left-aligned, usually "Cancel" in neutral color
- **Width**: Equal-width buttons with 12px gap
- **Margin**: 20px from content, 20px from modal edges

#### Confirmation Types

**End Conversation:**
- **Icon**: Warning triangle (Amber)
- **Title**: "End Conversation?"
- **Description**: "Your progress will be saved, but the conversation will stop here."
- **Primary**: "End Conversation" (Error color)
- **Secondary**: "Keep Talking"

**Delete Progress:**
- **Icon**: Trash can (Error)
- **Title**: "Delete All Progress?"
- **Description**: "This will permanently remove your conversation history and achievements. This cannot be undone."
- **Primary**: "Delete" (Error color)
- **Secondary**: "Cancel"

**Account Logout:**
- **Icon**: Sign out (Neutral)
- **Title**: "Sign Out?"
- **Description**: "You can always sign back in to access your progress."
- **Primary**: "Sign Out" (Primary color)
- **Secondary**: "Cancel"

### Premium Upsell Modal

#### Purpose
Encourage premium subscription at strategic moments with clear value proposition.

#### Visual Specifications

**Modal Container:**
- **Style**: Full-screen modal with close button
- **Background**: Linear gradient from Primary to Secondary
- **Content Background**: White content cards over gradient
- **Animation**: Scale up from center (500ms ease-out)

**Header Section:**
- **Close Button**: X icon, white color, top-right
- **Badge**: "Premium" pill badge in white
- **Title**: "Unlock Unlimited Practice" (H2 in white)
- **Subtitle**: "Join 15,000+ members building confidence faster"

**Features List:**
- **Container**: White rounded card with 20px padding
- **Layout**: Vertical list with checkmark icons
- **Spacing**: 16px between feature items

**Feature Items:**
1. ✅ **Unlimited Daily Conversations**
   - "Practice as much as you want, any time"
2. ✅ **Advanced Scenarios** 
   - "Formal events, speed dating, group conversations"
3. ✅ **Detailed Analytics**
   - "Track improvement across specific skills"
4. ✅ **Priority AI Response**
   - "Faster conversation generation"
5. ✅ **Conversation History**
   - "Review and learn from past conversations"

**Social Proof:**
- **Testimonial**: User quote with star rating
- **Stats**: "94% of premium users report faster confidence building"
- **Trust**: "Join thousands of successful users"

**Pricing Section:**
- **Trial Offer**: "7-day free trial, then $9.99/month"
- **Money Back**: "Cancel anytime, 30-day money-back guarantee"
- **Comparison**: "Free: 1 daily conversation vs Premium: Unlimited"

**Action Buttons:**
- **Primary**: "Start Free Trial" (full-width, white background, gradient text)
- **Secondary**: "Maybe Later" (outline button in white)

#### Trigger Points
- After first daily conversation limit reached
- After 5 total conversations completed
- When viewing locked premium scenarios
- After achieving significant milestone

### Help/Tips Modal

#### Purpose
Contextual help during conversations and setup processes.

#### Visual Specifications

**Modal Container:**
- **Style**: Bottom sheet, 50% screen height
- **Background**: `#FFFFFF` (White)
- **Header**: Gradient bar in Primary color (4px height)

**Content Types:**

**Conversation Help ("Stuck?" button):**
- **Title**: "Need inspiration?"
- **Content**: 3 contextually-appropriate response suggestions
- **Format**: Tappable suggestion cards
- **Additional**: "Tips for better conversations" expandable section

**Onboarding Help:**
- **Title**: "How this works"
- **Content**: Step-by-step explanation with illustrations
- **Format**: Scrollable content with visual aids
- **Navigation**: Previous/Next buttons for multi-step help

**Feature Explanation:**
- **Title**: Feature-specific title
- **Content**: Benefits, usage instructions, examples
- **Format**: Mixed text, images, and interaction examples

### Settings Modal

#### Purpose
App preferences, account settings, and configuration options.

#### Visual Specifications

**Modal Container:**
- **Style**: Full-screen modal on mobile, large center modal on tablet+
- **Background**: `#F9FAFB` (Neutral-50)
- **Header**: White header with title and close button

**Content Sections:**
- **Account**: Profile, preferences, data export
- **Notifications**: Push preferences, frequency settings
- **Privacy**: Data handling, analytics opt-out
- **Support**: Help center, contact, feedback
- **About**: Version, terms, privacy policy

**Section Design:**
- **Background**: White cards with subtle shadows
- **Spacing**: 12px between sections
- **Item Height**: 48px for touch accessibility
- **Icons**: 20px icons in Primary color

### Alert Messages

#### Purpose
System notifications, errors, and status updates.

#### Visual Specifications

**Toast Style (Non-blocking):**
- **Position**: Top of screen with safe area respect
- **Width**: Full-width with 16px margins
- **Height**: Auto-sizing based on content
- **Background**: Semantic color based on message type
- **Duration**: 4 seconds auto-dismiss
- **Animation**: Slide down from top

**Alert Types:**

**Success Toast:**
- **Background**: `#10B981` (Success)
- **Icon**: Checkmark circle (white)
- **Text**: White text
- **Example**: "Conversation completed successfully!"

**Error Toast:**
- **Background**: `#EF4444` (Error)
- **Icon**: Warning triangle (white)
- **Text**: White text
- **Example**: "Connection lost. Please check your internet."

**Info Toast:**
- **Background**: `#3B82F6` (Info)
- **Icon**: Information circle (white)
- **Text**: White text
- **Example**: "New achievement unlocked!"

## Accessibility Considerations

### Screen Reader Support
- **Modal Announcements**: "Dialog opened" and content description
- **Focus Management**: Focus moves to modal on open, returns on close
- **Role Definitions**: Proper ARIA roles for different modal types
- **Content Structure**: Logical heading hierarchy within modals

### Keyboard Navigation
- **Focus Trapping**: Focus stays within modal while open
- **Escape Key**: Closes dismissible modals
- **Tab Order**: Logical progression through interactive elements
- **Enter/Space**: Activates focused buttons and options

### Motor Accessibility
- **Touch Targets**: All interactive elements 44x44px minimum
- **Close Affordances**: Multiple ways to close modals
- **Drag Indicators**: Clear visual cues for draggable modals
- **Error Recovery**: Easy undo for modal actions

## Usage Guidelines

### When to Use Each Modal Type

**Bottom Sheets:**
- Mobile-first interactions
- Option selection with moderate complexity
- Quick actions that don't require full attention

**Center Modals:**
- Confirmations and alerts
- Critical decisions requiring focus
- Simple forms and inputs

**Full-Screen Modals:**
- Complex forms and multi-step processes
- Content that benefits from full attention
- Settings and detailed configuration

### Modal Hierarchy
- **Maximum 1 modal** visible at a time
- **Clear dismissal paths** for all modals
- **Consistent animation timing** across modal types
- **Appropriate backdrop handling** for each modal style

## Implementation Notes

### Performance Considerations
- **Lazy Loading**: Complex modals load content on demand
- **Animation Performance**: Use native driver for 60fps
- **Memory Management**: Clean up modal content when dismissed
- **Background Handling**: Pause expensive operations when modal open

### Platform-Specific Features

**iOS:**
- **Native Feel**: Use iOS-style action sheets and alerts where appropriate
- **Haptic Feedback**: Subtle haptics on modal presentation
- **Safe Area**: Proper handling of notch and home indicator
- **Blur Effects**: Native blur on backdrop when supported

**Android:**
- **Material Design**: Follow Material modal patterns
- **Hardware Back**: Proper back button handling in modals
- **Elevation**: Correct elevation values for modal hierarchy
- **Ripple Effects**: Android-style touch feedback

---

## Related Documentation
- [Button Components](./buttons.md) - Modal action buttons
- [Form Components](./forms.md) - Modal form elements
- [Color Tokens](../tokens/colors.md) - Modal color specifications
- [Animation Tokens](../tokens/animations.md) - Modal animation timing

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*