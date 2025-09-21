# Navigation Components

---
title: FlirtCraft Navigation Components
description: Tab bars, headers, back buttons, and navigation patterns for seamless user flows
feature: all
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ../tokens/spacing.md
dependencies:
  - React Navigation 6
  - NativeBase components
  - React Native Safe Area Context
status: approved
---

## Overview

FlirtCraft's navigation system prioritizes user confidence and flow state maintenance. All navigation patterns minimize cognitive load while providing clear wayfinding and progress indication.

## Navigation Architecture

### Primary Navigation Patterns
1. **Bottom Tab Navigation** - Main app sections
2. **Stack Navigation** - Linear flows (onboarding, conversations)
3. **Modal Presentation** - Contextual actions and settings
4. **Header Navigation** - Screen-level actions and back navigation

## Component Specifications

### Bottom Tab Bar

#### Purpose
Primary navigation for main app sections, always accessible except during conversations.

#### Visual Specifications

**Container:**
- **Height**: `84px` (including safe area padding)
- **Background**: `#FFFFFF` (White) with subtle shadow
- **Border Top**: `1px solid #F3F4F6` (Neutral-100)
- **Safe Area**: Automatic padding for device-specific bottom safe areas
- **Shadow**: `0 -2px 8px rgba(0, 0, 0, 0.04)` – Subtle elevation

**Tab Items:**
- **Touch Target**: Minimum `44x44px` centered in tab area
- **Spacing**: Equal distribution across available width
- **Icon Size**: `24px` for optimal recognition
- **Label Typography**: Caption (12px/16px, 400 weight)
- **Vertical Layout**: Icon above label with `4px` spacing

#### Tab States

**Active State:**
- **Icon Color**: `#F97316` (Primary)
- **Label Color**: `#F97316` (Primary)
- **Weight**: Icon remains same weight, label becomes 500 weight
- **Animation**: 200ms ease-out color transition
- **Scale**: Subtle 1.05 scale increase on icon

**Inactive State:**
- **Icon Color**: `#9CA3AF` (Neutral-400)
- **Label Color**: `#9CA3AF` (Neutral-400)
- **Weight**: Normal icon and label weights
- **Opacity**: No opacity changes (full visibility)

**Focus State (Keyboard):**
- **Focus Ring**: `2px solid #F97316` with `2px` offset
- **Background**: Subtle `rgba(99, 102, 241, 0.1)` highlight

#### Tab Sections

1. **Home Tab**
   - **Icon**: House/home icon (outlined when inactive, filled when active)
   - **Label**: "Home"
   - **Purpose**: Dashboard, daily stats, quick actions, detailed analytics, achievement gallery, skill tracking

2. **Chat Tab**
   - **Icon**: Message bubble/chat icon
   - **Label**: "Chat" 
   - **Purpose**: Custom conversation practice with unified location and difficulty selection

3. **Scenarios Tab**
   - **Icon**: Cards/templates icon
   - **Label**: "Scenarios"
   - **Purpose**: Predefined and trendy conversation templates

4. **Profile Tab**
   - **Icon**: User/person icon
   - **Label**: "Profile"
   - **Purpose**: Personal information, preferences, account settings, app preferences, notifications, privacy, support

#### Responsive Behavior
- **Mobile Portrait**: Full 4-tab layout
- **Mobile Landscape**: Condensed with icon-only if space limited
- **Tablet**: Enhanced spacing with 4-tab layout
- **Web**: Fixed bottom or optional sidebar navigation

#### NativeBase Implementation
```jsx
<Box
  bg="white"
  safeAreaBottom
  shadow={2}
  borderTopWidth={1}
  borderTopColor="gray.100"
>
  <HStack flex={1} safeAreaX>
    {tabs.map((tab, index) => (
      <Pressable
        key={tab.name}
        flex={1}
        py={2}
        alignItems="center"
        onPress={() => navigation.navigate(tab.route)}
        _pressed={{ bg: "primary.50", opacity: 0.8 }}
      >
        <Icon
          as={tab.icon}
          size="6"
          color={isActive ? "primary.500" : "gray.400"}
        />
        <Text
          fontSize="xs"
          color={isActive ? "primary.500" : "gray.400"}
          fontWeight={isActive ? "medium" : "normal"}
          mt={1}
        >
          {tab.label}
        </Text>
      </Pressable>
    ))}
  </HStack>
</Box>
```

### Header Bar (Screen Headers)

#### Purpose
Screen-level navigation with titles, back buttons, and contextual actions.

#### Visual Specifications

**Container:**
- **Height**: `64px` plus safe area top padding
- **Background**: `#FFFFFF` (White)
- **Border Bottom**: `1px solid #F3F4F6` (Neutral-100) 
- **Shadow**: `0 1px 3px rgba(0, 0, 0, 0.04)` – Subtle depth

**Content Layout:**
- **Left Zone**: Back button or hamburger (44x44px touch target)
- **Center Zone**: Screen title, expandable for longer titles
- **Right Zone**: Action buttons (44x44px each, max 2 buttons)

#### Header Elements

**Back Button:**
- **Icon**: Left arrow, 24px size
- **Color**: `#374151` (Neutral-700)
- **Touch Target**: `44x44px` minimum
- **Position**: 16px from left edge, vertically centered
- **Hover/Focus**: `rgba(55, 65, 81, 0.1)` background circle

**Screen Title:**
- **Typography**: H3 (20px/28px, 600 weight)
- **Color**: `#1F2937` (Neutral-800)
- **Alignment**: Center (default), left-aligned if too long
- **Truncation**: Ellipsis after 20 characters on mobile

**Action Buttons:**
- **Size**: 24px icons in 44x44px touch targets
- **Color**: `#F97316` (Primary) for primary actions, Neutral-700 for secondary
- **Spacing**: 8px between multiple action buttons
- **Position**: 16px from right edge

#### Header Variants

**Default Header:**
```jsx
// Standard screen header with back navigation
<Header>
  <BackButton />
  <Title>Screen Name</Title>
  <ActionButton icon="settings" />
</Header>
```

**Conversation Header:**
```jsx
// Conversation-specific header with timer and counter
<Header>
  <EndButton />
  <VStack alignItems="center">
    <Title>Coffee Shop 🟢</Title>
    <HStack space={4}>
      <Text fontSize="sm">2:15</Text>
      <Text fontSize="sm">6/50</Text>
    </HStack>
  </VStack>
  <HelpButton />
</Header>
```

**Modal Header:**
```jsx
// Modal presentation header
<Header>
  <CancelButton />
  <Title>Modal Title</Title>
  <DoneButton />
</Header>
```

### Modal Navigation

#### Purpose
Contextual overlays for settings, help, and secondary flows that don't require full navigation.

#### Visual Specifications

**Modal Container:**
- **Background**: `rgba(0, 0, 0, 0.5)` backdrop
- **Content Background**: `#FFFFFF` (White)
- **Border Radius**: `16px` top corners only (bottom sheet style)
- **Shadow**: `0 -4px 16px rgba(0, 0, 0, 0.1)`

**Modal Header:**
- **Height**: `56px`
- **Drag Handle**: Optional 4px wide, 24px long rounded indicator
- **Title**: H4 typography (18px/24px, 500 weight)
- **Close Button**: X icon, top-right, 44x44px touch target

**Animation Behavior:**
- **Entrance**: Slide up from bottom (400ms ease-out)
- **Exit**: Slide down to bottom (300ms ease-in)
- **Backdrop**: Fade in/out coordinated with slide

#### Modal Types

**Settings Modal:**
- Full-height overlay with scrollable content
- Multiple sections with clear visual separation
- Primary and secondary action buttons at bottom

**Help/Tips Modal:**
- Medium-height overlay (~60% of screen)
- Focused content with illustrations
- Single primary action (typically "Got it!")

**Confirmation Modal:**
- Small, centered modal
- Clear title, description, and action buttons
- Destructive actions use Error color (Red)

### Progress Indicators

#### Purpose
Navigation aids showing user position in multi-step flows.

#### Visual Specifications

**Step Indicator (Onboarding):**
- **Container**: Horizontal bar, full width with 16px margins
- **Steps**: Circles (12px diameter) connected by 2px lines
- **Colors**: 
  - Completed: `#10B981` (Success) 
  - Current: `#F97316` (Primary)
  - Upcoming: `#E5E7EB` (Neutral-200)
- **Animation**: Progress fills on step completion (300ms ease-out)

**Progress Bar (Loading):**
- **Height**: `4px`
- **Background**: `#E5E7EB` (Neutral-200)
- **Fill Color**: `#F97316` (Primary)
- **Animation**: Smooth progress advancement with spring easing

### Conversation Navigation

#### Purpose
Specialized navigation for active conversation sessions.

#### Visual Specifications

**End Conversation Button:**
- **Position**: Top-left in conversation header
- **Icon**: X or "End" text
- **Color**: `#EF4444` (Error) to indicate session termination
- **Confirmation**: Requires confirmation modal before ending

**Help/Stuck Button:**
- **Position**: Bottom-right floating action or input area
- **Icon**: Lightbulb or question mark
- **Color**: `#F59E0B` (Warning/Amber)
- **Behavior**: Opens contextual help without leaving conversation

**Context Reference Button:**
- **Position**: Top-right in conversation header
- **Icon**: Information (i) icon
- **Purpose**: Quick reference to pre-conversation context
- **Behavior**: Slides down context summary sheet

### Accessibility Requirements

#### Screen Reader Support
- **Tab Navigation**: Proper role announcements ("Tab 1 of 3: Home")
- **Header Navigation**: "Back button" and clear action descriptions
- **Progress Indicators**: "Step 2 of 5: Set Preferences"
- **Modal Context**: Proper focus management and escape behavior

#### Keyboard Navigation
- **Tab Order**: Logical left-to-right, top-to-bottom progression
- **Tab Switching**: Arrow keys for tab navigation, Enter to activate
- **Modal Dismissal**: Escape key closes modals and returns focus
- **Focus Management**: Focus returns to appropriate element after navigation

#### Touch/Motor Accessibility
- **Target Sizes**: All interactive elements minimum 44x44px
- **Spacing**: Adequate space between adjacent controls
- **Gesture Alternatives**: All swipe actions have button alternatives
- **Error Recovery**: Clear undo options for navigation mistakes

## Usage Guidelines

### When to Use Each Pattern

**Bottom Tabs:**
- Main app sections that users access regularly
- Content areas that benefit from quick switching
- Maximum 5 tabs to prevent overcrowding

**Stack Navigation:**
- Linear flows with clear start/end points
- Chat flow: Difficulty → Context Creation → Chat
- Scenarios flow: Selection → Context Creation (with template) → Chat
- Processes where back navigation makes sense
- Detail views launched from list screens

**Modal Presentation:**
- Secondary actions that don't require full navigation
- Settings and preferences that overlay current context
- Confirmation dialogs and alerts

### Navigation State Management

**Deep Linking:**
- All major screens accessible via URL structure
- Conversation sessions can be resumed via deep links
- Proper handling of expired or invalid links

**State Preservation:**
- Tab navigation preserves scroll position and form data
- Conversation state survives app backgrounding
- Onboarding progress saved at each major step

**Back Button Behavior:**
- Android: Hardware back button handled appropriately
- iOS: Swipe back gesture supported where relevant
- Conversation: Requires confirmation before exit

## Implementation Notes

### React Navigation Configuration
```jsx
// Tab Navigator Configuration
const TabNavigator = () => (
  <Tab.Navigator
    screenOptions={{
      tabBarStyle: {
        height: 84,
        backgroundColor: 'white',
        borderTopWidth: 1,
        borderTopColor: '#F3F4F6',
        elevation: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -2 },
        shadowOpacity: 0.04,
        shadowRadius: 8,
      },
      tabBarActiveTintColor: '#F97316',
      tabBarInactiveTintColor: '#9CA3AF',
      tabBarLabelStyle: {
        fontSize: 10, // Reduced for 4-tab layout
        fontWeight: '400',
        marginTop: 2, // Tighter spacing
      },
      tabBarIconStyle: {
        marginBottom: 2,
      },
    }}
  >
    <Tab.Screen 
      name="Home" 
      component={HomeScreen}
      options={{
        tabBarIcon: ({ color, focused }) => (
          <HomeIcon 
            size={22} 
            color={color} 
            filled={focused}
            badge={streakCount > 0 ? `🔥${streakCount}` : null}
          />
        ),
      }}
    />
    <Tab.Screen 
      name="Chat" 
      component={ChatFlowNavigator}
      options={{
        tabBarIcon: ({ color, focused }) => (
          <ChatIcon 
            size={22} 
            color={color} 
            filled={focused}
            badge={hasNewDifficulty ? 'New' : null}
          />
        ),
      }}
    />
    <Tab.Screen 
      name="Scenarios" 
      component={ScenariosFlowNavigator}
      options={{
        tabBarIcon: ({ color, focused }) => (
          <ScenariosIcon 
            size={22} 
            color={color} 
            filled={focused}
            badge={newScenariosCount > 0 ? newScenariosCount : null}
          />
        ),
      }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileScreen}
      options={{
        tabBarIcon: ({ color, focused }) => (
          <ProfileIcon 
            size={22} 
            color={color} 
            filled={focused}
            badge={hasNotifications ? '!' : null}
          />
        ),
      }}
    />
  </Tab.Navigator>
);

// Stack Navigators for Chat and Scenarios flows
const ChatFlowNavigator = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="ChatUnifiedSelection" component={ChatUnifiedSelectionScreen} />
    <Stack.Screen name="ChatContext" component={ChatContextScreen} />
    <Stack.Screen name="PreConversation" component={PreConversationScreen} />
    <Stack.Screen name="Conversation" component={ConversationScreen} />
    <Stack.Screen name="ConversationFeedback" component={FeedbackScreen} />
  </Stack.Navigator>
);

const ScenariosFlowNavigator = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="ScenariosList" component={ScenariosListScreen} />
    <Stack.Screen name="ScenarioDetails" component={ScenarioDetailsScreen} />
    <Stack.Screen name="ScenarioContext" component={ScenarioContextScreen} />
    <Stack.Screen name="PreConversation" component={PreConversationScreen} />
    <Stack.Screen name="Conversation" component={ConversationScreen} />
    <Stack.Screen name="ConversationFeedback" component={FeedbackScreen} />
  </Stack.Navigator>
);
```

### Performance Considerations
- **Lazy Loading**: Secondary screens load on first access
- **Tab Persistence**: Active tabs maintain state in memory
- **Memory Management**: Inactive conversation sessions cleaned up
- **Animation Performance**: Use native driver for smooth 60fps

### Platform-Specific Adaptations

**iOS Specific:**
- **Large Title Headers**: Use iOS large title style where appropriate
- **Safe Area Insets**: Proper handling of notch and home indicator
- **Back Gesture**: Enable iOS swipe-back gesture
- **Haptic Feedback**: Subtle haptics on tab selection

**Android Specific:**
- **Material Design**: Follow Material Design tab and header patterns
- **Hardware Back Button**: Proper back button handling
- **Status Bar**: Coordinate status bar style with header appearance
- **Navigation Bar**: Handle Android navigation bar spacing

---

## Related Documentation
- [Button Components](./buttons.md) - Navigation button styling
- [Color Tokens](../tokens/colors.md) - Navigation color specifications
- [Spacing Tokens](../tokens/spacing.md) - Navigation layout spacing
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Navigation accessibility

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*