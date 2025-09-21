# Card Components

---
title: FlirtCraft Card Components
description: Scenario cards, context cards, achievement cards, and feedback displays
feature: scenario-selection, pre-conversation-context, feedback, gamification
last-updated: 2025-08-30
version: 2.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ../tokens/spacing.md
  - ../tokens/nativebase-theme.md
dependencies:
  - NativeBase Box, Image, VStack, HStack, Badge components
  - React Native Reanimated 3 for animations
  - NativeWind 4.1 utility classes
status: approved
---

## Overview

Card components in FlirtCraft serve as primary containers for scenarios, context information, achievements, and feedback. Built with NativeBase for consistency and enhanced with NativeWind 4.1 utilities for responsive design. Each card type is optimized for its specific content while maintaining visual consistency and accessibility.

## NativeBase Card Implementation

### Base Card Structure
```jsx
import { Box, VStack, HStack, Text, Image, Pressable } from 'native-base';

const BaseCard = ({ children, variant = 'elevated', onPress, ...props }) => {
  return (
    <Pressable onPress={onPress} isDisabled={!onPress}>
      <Box
        borderRadius="16"
        bg="white"
        shadow={variant === 'elevated' ? 4 : 2}
        borderWidth={variant === 'outline' ? 1 : 0}
        borderColor={variant === 'outline' ? 'gray.200' : 'transparent'}
        _dark={{
          bg: 'gray.900',
          borderColor: 'gray.700'
        }}
        {...props}
      >
        {children}
      </Box>
    </Pressable>
  );
};
```

## Card Specifications

### Horizontal Scroll Location Card (Chat Tab)

#### Purpose
Displays location options in a horizontal infinity scroll carousel for the unified selection screen in Chat tab.

#### Visual Specifications

**Container:**
- **Width**: `280px` – Fixed width for consistent carousel behavior
- **Height**: `180px` – Optimized aspect ratio for location imagery
- **Border Radius**: `16px` – Modern, friendly appearance
- **Spacing**: `16px` between cards in carousel
- **Background**: White base with gradient overlay for text readability
- **Shadow**: `0 2px 8px rgba(0, 0, 0, 0.1)` – Subtle elevation
- **Border**: `3px solid transparent` (changes to Primary on selection)

**Background Image:**
- **Aspect Ratio**: 16:10 to fill card bounds optimally
- **Overlay**: Linear gradient from transparent to `rgba(0, 0, 0, 0.4)` bottom third
- **Quality**: High-resolution, professional photography
- **Content**: Contextually appropriate to scenario location

**Text Content:**
- **Title**: H4 typography (18px/24px, 600 weight) in white
- **Position**: Bottom of card with 16px padding from edges
- **Text Shadow**: `0 1px 2px rgba(0, 0, 0, 0.6)` for readability

#### Carousel Behavior

**Scroll Physics:**
- **Momentum Scrolling**: Natural iOS/Android momentum behavior
- **Snap-to-Center**: Cards automatically center after scroll ends
- **Spring Animation**: `tension: 300, friction: 30` for smooth deceleration
- **Peek Preview**: Shows ~20% of adjacent cards for navigation hint
- **Initial State**: First card (Coffee Shop) centered by default

**Selection States:**

**Default State:**
- Clean presentation with subtle shadow
- No border, normal appearance
- Image displays with consistent overlay

**Selected State:**
- **Border**: `3px solid #F97316` (Primary color) with subtle glow
- **Shadow**: Enhanced to `0 4px 16px rgba(249, 115, 22, 0.25)`
- **Scale**: Maintains 1:1 scale (no size change to preserve layout)
- **Animation**: Selection animates in over `200ms ease-out`

**Focus State (Keyboard/Accessibility):**
- **Focus Ring**: `3px solid #F97316` with `2px offset`
- **Announcement**: Screen reader announces location name and selection state

#### Location Content

**Coffee Shop Card:**
- **Title**: "Coffee Shop"
- **Image**: Warm, inviting coffee shop interior with natural lighting

**Bar/Lounge Card:**
- **Title**: "Bar & Lounge"
- **Image**: Upscale bar environment with social atmosphere

**Bookstore Card:**
- **Title**: "Bookstore"
- **Image**: Cozy bookstore with comfortable reading areas

**Gym Card:**
- **Title**: "Gym"
- **Image**: Modern fitness facility with equipment visible

**Park Card:**
- **Title**: "Park"
- **Image**: Beautiful park setting with walking paths and greenery

**Campus Card:**
- **Title**: "Campus"
- **Image**: University campus with students and academic buildings

**Grocery Store Card:**
- **Title**: "Grocery Store"
- **Image**: Modern grocery store with well-lit aisles

**Art Gallery Card:**
- **Title**: "Art Gallery"
- **Image**: Contemporary gallery space with artwork displays

#### React Native Implementation
```jsx
<ScrollView
  horizontal
  showsHorizontalScrollIndicator={false}
  snapToInterval={296} // 280px width + 16px spacing
  snapToAlignment="center"
  decelerationRate="fast"
  contentInset={{left: 48, right: 48}} // Center first/last items
  contentOffset={{x: -48}} // Offset for initial centering
>
  {locations.map((location, index) => (
    <Pressable
      key={location.id}
      onPress={() => onLocationSelect(location)}
      style={{
        width: 280,
        height: 180,
        marginRight: index === locations.length - 1 ? 0 : 16,
        borderRadius: 16,
        borderWidth: selectedLocation?.id === location.id ? 3 : 0,
        borderColor: selectedLocation?.id === location.id ? '#F97316' : 'transparent',
        overflow: 'hidden',
        shadowColor: selectedLocation?.id === location.id ? '#F97316' : '#000',
        shadowOffset: { width: 0, height: selectedLocation?.id === location.id ? 4 : 2 },
        shadowOpacity: selectedLocation?.id === location.id ? 0.25 : 0.1,
        shadowRadius: selectedLocation?.id === location.id ? 16 : 8,
        elevation: selectedLocation?.id === location.id ? 8 : 4,
      }}
    >
      <Image
        source={{ uri: location.imageUrl }}
        style={{
          width: '100%',
          height: '100%',
          position: 'absolute',
        }}
        resizeMode="cover"
      />
      <LinearGradient
        colors={['transparent', 'rgba(0,0,0,0.4)']}
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '50%',
        }}
      />
      <View
        style={{
          position: 'absolute',
          bottom: 16,
          left: 16,
          right: 16,
        }}
      >
        <Text
          style={{
            fontSize: 18,
            fontWeight: '600',
            color: 'white',
            textShadowColor: 'rgba(0,0,0,0.6)',
            textShadowOffset: { width: 0, height: 1 },
            textShadowRadius: 2,
          }}
        >
          {location.title}
        </Text>
      </View>
    </Pressable>
  ))}
</ScrollView>
```

### Scenario Selection Card (Scenarios Tab)

#### Purpose
Displays predefined practice scenarios with difficulty indicators and selection states for the Scenarios tab.

#### Visual Specifications

**Container:**
- **Width**: Full-width mobile (with 16px margins), 320px fixed tablet+
- **Height**: `240px` – Consistent aspect ratio across all scenarios
- **Border Radius**: `16px` – Modern, friendly appearance
- **Background**: White base with gradient overlay for text readability
- **Shadow**: `0 2px 8px rgba(0, 0, 0, 0.1)` – Subtle elevation
- **Border**: `2px solid transparent` (changes on selection)

**Background Image:**
- **Aspect Ratio**: 16:9 within card bounds
- **Overlay**: Linear gradient from transparent to `rgba(0, 0, 0, 0.4)` bottom
- **Quality**: High-resolution, professional photography
- **Content**: Contextually appropriate to scenario location

**Text Content:**
- **Title**: H3 typography (20px/28px, 600 weight) in white
- **Description**: Body text (16px/22px, 400 weight) in white with 90% opacity
- **Position**: Bottom of card over gradient overlay
- **Padding**: `20px` from card edges
- **Text Shadow**: `0 1px 2px rgba(0, 0, 0, 0.5)` for readability

**Difficulty Indicator:**
- **Position**: Top-right corner with 12px margin
- **Design**: Pill-shaped badge with rounded corners
- **Size**: Auto-width with 8px horizontal padding, 24px height
- **Colors**: 
  - Green: `#10B981` background, white text
  - Yellow: `#F59E0B` background, white text  
  - Red: `#EF4444` background, white text
- **Typography**: Caption Bold (12px/16px, 600 weight)

#### Card States

**Default State:**
- Clean presentation with subtle shadow
- No border or selection indicators
- Image displays with consistent overlay

**Hover State (Non-touch devices):**
- **Shadow**: Increases to `0 4px 16px rgba(0, 0, 0, 0.15)`
- **Transform**: Slight lift with `translateY(-2px)`
- **Transition**: `200ms ease-out` for smooth interaction

**Selected State:**
- **Border**: `2px solid #F97316` (Primary color)
- **Shadow**: Enhanced to `0 6px 20px rgba(99, 102, 241, 0.25)`
- **Scale**: Subtle `1.02` scale increase
- **Animation**: Selection animates in over `300ms ease-out`

**Focus State (Keyboard):**
- **Focus Ring**: `3px solid #F97316` with `2px offset`
- **Announcement**: Screen reader announces scenario and difficulty

#### Scenario Content

**Coffee Shop Card:**
- **Title**: "Coffee Shop"
- **Description**: "Casual and relaxed conversations"
- **Image**: Warm, inviting coffee shop interior
- **Context**: Books, laptops, comfortable seating

**Bar/Lounge Card:**
- **Title**: "Bar & Lounge"
- **Description**: "Social nightlife interactions"  
- **Image**: Upscale bar with social atmosphere
- **Context**: Happy hour, social mixing

**Bookstore Card:**
- **Title**: "Bookstore"
- **Description**: "Intellectual and thoughtful exchanges"
- **Image**: Cozy bookstore with browsing areas
- **Context**: Reading nooks, literary atmosphere

**Gym Card:**
- **Title**: "Gym"
- **Description**: "Active lifestyle conversations"
- **Image**: Modern fitness facility
- **Context**: Equipment, active people

**Park Card:**
- **Title**: "Park"
- **Description**: "Outdoor and recreational chats"
- **Image**: Beautiful park with walking paths
- **Context**: Nature, outdoor activities

**Campus Card:**
- **Title**: "Campus"
- **Description**: "Student life and academic discussions"
- **Image**: University campus environment
- **Context**: Students, academic buildings

**Grocery Store Card:**
- **Title**: "Grocery Store"
- **Description**: "Everyday life encounters"
- **Image**: Modern grocery store aisles
- **Context**: Shopping, everyday interactions

**Art Gallery Card:**
- **Title**: "Art Gallery"
- **Description**: "Creative and cultural conversations"
- **Image**: Contemporary art gallery space
- **Context**: Artwork, cultural atmosphere

#### NativeBase Implementation
```jsx
import { Box, Image, Text, VStack, Badge, Pressable } from 'native-base';
import { LinearGradient } from 'expo-linear-gradient';

<Pressable
  onPress={() => onScenarioSelect(scenario)}
  _pressed={{ opacity: 0.8 }}
>
  <Box
    width="100%"
    height={240}
    borderRadius={16}
    borderWidth={selected ? 2 : 0}
    borderColor={selected ? "primary.500" : "transparent"}
    shadow={selected ? 5 : 2}
    overflow="hidden"
    position="relative"
  >
    <Image
      source={{ uri: scenario.imageUrl }}
      alt={scenario.title}
      width="100%"
      height="100%"
      position="absolute"
    />
    <Box
      position="absolute"
      bottom={0}
      left={0}
      right={0}
      height="60%"
      bg={{
        linearGradient: {
          colors: ['transparent', 'rgba(0,0,0,0.4)'],
          start: [0, 0],
          end: [0, 1]
        }
      }}
    />
    <VStack
      position="absolute"
      bottom={0}
      left={0}
      right={0}
      p={5}
      space={1}
    >
      <Text fontSize="xl" fontWeight="semibold" color="white">
        {scenario.title}
      </Text>
      <Text fontSize="md" color="white" opacity={0.9}>
        {scenario.description}
      </Text>
    </VStack>
    <Badge
      position="absolute"
      top={3}
      right={3}
      bg={getDifficultyColor(scenario.difficulty)}
      _text={{ color: 'white', fontSize: 'xs', fontWeight: 'semibold' }}
      px={2}
      py={1}
      borderRadius={12}
    >
      {scenario.difficulty}
    </Badge>
  </Box>
</Pressable>
```

### Difficulty Selection Card (Chat Tab)

#### Purpose
Displays difficulty options in the bottom section of the unified selection screen.

#### Visual Specifications

**Container:**
- **Width**: Equal distribution across screen width with 12px spacing between cards
- **Height**: `120px` – Adequate for content and touch target
- **Border Radius**: `12px` – Consistent with location cards but smaller scale
- **Background**: Color-coded based on difficulty level
- **Border**: `2px solid transparent` (changes on selection)
- **Shadow**: `0 2px 6px rgba(0, 0, 0, 0.1)` – Subtle elevation

**Layout Structure:**
- **Top Section**: Icon and title (60% of card height)
- **Bottom Section**: Description text (40% of card height)
- **Padding**: `16px` all sides

**Icon Specifications:**
- **Size**: `24px` – Prominent but not overwhelming
- **Color**: White for visibility against colored backgrounds
- **Position**: Center-aligned with 8px spacing from title

**Typography:**
- **Title**: Body Medium (16px/22px, 600 weight) in white
- **Description**: Caption (12px/16px, 400 weight) in white with 90% opacity
- **Text Shadow**: `0 1px 2px rgba(0, 0, 0, 0.3)` for readability

#### Difficulty Card Variants

**Green (Friendly) Card:**
- **Background**: Linear gradient from `#10B981` to `#047857`
- **Icon**: Smiling face or thumbs up icon
- **Title**: "Friendly"
- **Description**: "Open and encouraging"
- **Selection State**: `2px solid #065F46` (darker green)

**Yellow (Real Talk) Card:**
- **Background**: Linear gradient from `#F59E0B` to `#D97706`
- **Icon**: Balance scale or conversation icon
- **Title**: "Real Talk"
- **Description**: "Realistic interactions"
- **Selection State**: `2px solid #92400E` (darker amber)

**Red (A-Game) Card:**
- **Background**: Linear gradient from `#EF4444` to `#DC2626`
- **Icon**: Fire or challenge icon
- **Title**: "A-Game"
- **Description**: "Challenge yourself"
- **Selection State**: `2px solid #991B1B` (darker red)

#### Card States

**Default State:**
- Color-coded background with no border
- Standard shadow and no scale changes
- Icon and text clearly visible

**Selected State:**
- **Border**: `2px solid` in darker shade of primary color
- **Shadow**: Enhanced to `0 4px 12px rgba(0, 0, 0, 0.2)`
- **Scale**: Subtle `1.05` scale increase
- **Animation**: Selection animates in over `200ms ease-out`

**Pressed State:**
- **Scale**: `0.98` scale decrease for immediate feedback
- **Opacity**: `0.9` opacity during press

#### NativeBase Implementation
```jsx
import { HStack, VStack, Box, Text, Icon, Pressable } from 'native-base';

<HStack space={3} flex={1} px={4}>
  {difficulties.map((difficulty) => (
    <Pressable
      key={difficulty.id}
      flex={1}
      onPress={() => onDifficultySelect(difficulty)}
      _pressed={{ opacity: 0.9, transform: [{ scale: 0.98 }] }}
    >
      <Box
        height={120}
        borderRadius={12}
        borderWidth={selectedDifficulty?.id === difficulty.id ? 2 : 0}
        borderColor={difficulty.selectionColor}
        bg={{
          linearGradient: {
            colors: difficulty.gradientColors,
            start: [0, 0],
            end: [0, 1]
          }
        }}
        shadow={selectedDifficulty?.id === difficulty.id ? 4 : 2}
        p={4}
        alignItems="center"
        justifyContent="center"
        transform={selectedDifficulty?.id === difficulty.id ? 
          [{ scale: 1.05 }] : [{ scale: 1 }]}
      >
        <VStack space={2} alignItems="center" flex={1}>
          <Icon
            as={difficulty.icon}
            size="6"
            color="white"
          />
          <Text
            fontSize="md"
            fontWeight="semibold"
            color="white"
            textAlign="center"
          >
            {difficulty.title}
          </Text>
          <Text
            fontSize="xs"
            color="white"
            opacity={0.9}
            textAlign="center"
          >
            {difficulty.description}
          </Text>
        </VStack>
      </Box>
    </Pressable>
  ))}
</HStack>
```

### Context Information Card

#### Purpose
Displays pre-conversation context information (appearance, environment, body language, starters).

#### Visual Specifications

**Container:**
- **Width**: Full-width with 16px side margins
- **Min Height**: `120px` – Adapts to content length
- **Border Radius**: `12px` – Subtle rounding for approachable feel
- **Background**: `#FFFFFF` (White)
- **Border**: `1px solid #E5E7EB` (Neutral-200)
- **Shadow**: `0 1px 3px rgba(0, 0, 0, 0.05)` – Very subtle depth
- **Margin**: `12px` vertical spacing between cards

**Header Section:**
- **Height**: `48px` fixed
- **Background**: `#F9FAFB` (Neutral-50)
- **Border Bottom**: `1px solid #E5E7EB` (Neutral-200)
- **Padding**: `12px 16px`
- **Content**: Icon + title layout

**Content Section:**
- **Padding**: `16px`
- **Spacing**: `8px` between content items
- **Typography**: Body text (16px/22px, 400 weight)
- **Color**: `#374151` (Neutral-700)

#### Context Card Types

**Your Practice Partner Card:**
- **Icon**: Person icon (20px) in Primary color
- **Header**: "Your Practice Partner"
- **Content Structure**:
  - Age range with emphasis styling
  - Style description paragraph
  - Bulleted observable details (3-4 items)
  - Current activity description

**The Scene Card:**
- **Icon**: Location pin icon (20px) in Secondary color  
- **Header**: "The Environment"
- **Content Structure**:
  - Time and day context
  - Crowd level description
  - Atmospheric details list (3-4 items)
  - Overall mood assessment

**Body Language Signals Card:**
- **Icon**: Eye icon (20px) in Accent color
- **Header**: "Non-Verbal Cues"
- **Content Structure**:
  - Color-coded signal indicators
  - 3-4 observational points
  - Receptiveness assessment
  - Interaction likelihood notes

**Conversation Starters Card:**
- **Icon**: Chat bubble icon (20px) in Info color
- **Header**: "AI Starter Suggestions"
- **Content Structure**:
  - 3 contextual opener suggestions
  - "Create your own" option
  - "Need help?" link to tips

#### Body Language Signal Indicators

**Signal Color System:**
- **🟢 Positive**: `#10B981` (Success) background circle with white icon
- **🟡 Neutral**: `#F59E0B` (Warning) background circle with white icon  
- **🔴 Negative**: `#EF4444` (Error) background circle with white icon

**Signal Display Format:**
```
🟢 "Making brief eye contact when you look their way"
🟡 "Focused on their book, occasional glances around"
🔴 "Very focused on book, minimal eye contact"
```

### Achievement Card

#### Purpose
Displays unlocked achievements, badges, and milestone celebrations.

#### Visual Specifications

**Container:**
- **Width**: 160px (mobile), 200px (tablet+)
- **Height**: `180px` – Fixed aspect ratio for grid layout
- **Border Radius**: `16px`
- **Background**: Linear gradient based on achievement tier
- **Shadow**: `0 4px 12px rgba(0, 0, 0, 0.15)` – Prominent elevation
- **Border**: Optional 2px border for premium achievements

**Achievement Tiers:**
- **Bronze**: Gradient from `#D97706` to `#F59E0B` (Amber range)
- **Silver**: Gradient from `#6B7280` to `#9CA3AF` (Neutral range)  
- **Gold**: Gradient from `#D97706` to `#FBBF24` (Yellow range)
- **Premium**: Gradient from `#F97316` to `#EA580C` (Primary to Deep Orange)

**Badge Icon:**
- **Size**: `48px` – Prominent focal point
- **Position**: Center-top with 20px top margin
- **Color**: White with subtle drop shadow
- **Background**: Semi-transparent white circle (60px diameter)

**Text Content:**
- **Title**: Body Medium (16px/22px, 500 weight) in white
- **Description**: Body Small (14px/20px, 400 weight) in white with 90% opacity
- **Position**: Bottom section with 16px padding
- **Alignment**: Center-aligned text

**Progress Indicator (for in-progress achievements):**
- **Position**: Bottom of card
- **Height**: `4px`
- **Background**: `rgba(255, 255, 255, 0.3)`
- **Fill**: White progress bar
- **Animation**: Smooth progress advancement

#### Achievement Examples

**First Steps (Bronze):**
- **Icon**: Footprint or flag icon
- **Title**: "First Steps"
- **Description**: "Completed your first practice conversation"
- **Unlock**: After onboarding completion

**Conversation Starter (Silver):**
- **Icon**: Chat bubble icon
- **Title**: "Conversation Starter"  
- **Description**: "Started 10 conversations confidently"
- **Progress**: "7/10 conversations"

**Smooth Talker (Gold):**
- **Icon**: Star icon
- **Title**: "Smooth Talker"
- **Description**: "Achieved 90+ score in conversation"
- **Rarity**: "Only 5% of users unlock this!"

**Daily Dedication (Bronze):**
- **Icon**: Calendar icon
- **Title**: "Daily Dedication"
- **Description**: "Maintained a 7-day practice streak"
- **Progress**: "Day 5 of 7"

### Feedback Score Card

#### Purpose
Displays post-conversation scoring and performance metrics.

#### Visual Specifications

**Container:**
- **Width**: Full-width with 16px margins
- **Height**: `200px` – Fixed height for consistent layout
- **Border Radius**: `16px`
- **Background**: `#FFFFFF` (White)
- **Border**: `2px solid` based on performance tier
- **Shadow**: `0 4px 16px rgba(0, 0, 0, 0.1)`

**Performance Tier Colors:**
- **Excellent** (80-100): `#10B981` (Success) border
- **Good** (60-79): `#F59E0B` (Warning) border
- **Needs Practice** (0-59): `#EF4444` (Error) border

**Score Display:**
- **Position**: Left side, vertically centered
- **Score Number**: H1 typography (28px/36px, 700 weight)
- **Score Label**: "/100" in Body text
- **Color**: Matches performance tier color

**Circular Progress:**
- **Size**: `80px` diameter
- **Stroke Width**: `6px`
- **Background Circle**: `#E5E7EB` (Neutral-200)
- **Progress Circle**: Performance tier color
- **Animation**: Animated fill on card appearance (1 second duration)

**Metrics Section:**
- **Position**: Right side of card
- **Layout**: Vertical stack of key metrics
- **Spacing**: `8px` between metric items
- **Typography**: Body Small (14px/20px, 400 weight)

**Metric Items:**
- **Duration**: "5:32 conversation"
- **Messages**: "16 exchanges"
- **Flow Rating**: "Excellent flow"
- **Engagement**: "High engagement"

## Usage Guidelines

### When to Use Each Card Type

**Scenario Cards:**
- Primary selection interfaces
- When visual context enhances decision-making
- Grid or list layouts with multiple options

**Context Cards:**
- Information-dense content that needs organization
- Sequential information presentation
- Reference materials during active tasks

**Achievement Cards:**
- Celebrating user accomplishments
- Gamification elements and progress tracking
- Gallery displays of unlocked content

**Feedback Cards:**
- Performance summaries and analytics
- Post-activity result presentation
- Progress tracking and comparison

### Card Layout Patterns

**Single Column (Mobile):**
- Full-width cards with consistent spacing
- Vertical scrolling for multiple cards
- Focus on readability and touch targets

**Grid Layout (Tablet+):**
- 2-column grid for scenario selection
- 3-column grid for achievement galleries
- Maintains aspect ratios across screen sizes

**Horizontal Scrolling:**
- Achievement carousels
- Featured content highlights
- Quick access to card collections

### Accessibility Considerations

**Screen Reader Support:**
- **Role Definitions**: Cards marked as buttons when interactive
- **Content Description**: Complete card content read as single unit
- **State Announcements**: Selection and focus states clearly announced
- **Navigation**: Logical tab order through card grids

**Visual Accessibility:**
- **High Contrast**: All text meets WCAG AA contrast ratios
- **Focus Indicators**: Clear focus rings for keyboard navigation
- **Text Scaling**: Content adapts to user font size preferences
- **Color Independence**: Never relies solely on color for information

**Motor Accessibility:**
- **Touch Targets**: All interactive cards minimum 44x44px
- **Spacing**: Adequate space between adjacent cards
- **Alternative Actions**: Long-press menus for additional options
- **Error Recovery**: Clear undo options for card selections

## Implementation Notes

### Performance Optimization

**Image Loading:**
- **Lazy Loading**: Scenario images load as cards scroll into view
- **Progressive Enhancement**: Low-quality placeholders while loading
- **Caching Strategy**: Cache scenario images for repeated selections
- **Fallback Content**: Text-only display if images fail to load

**Animation Performance:**
- **Hardware Acceleration**: Use transform and opacity properties
- **Reduced Motion**: Respect user's motion preferences
- **60fps Target**: Optimize animations for smooth performance
- **Memory Management**: Clean up animation resources after completion

### Platform-Specific Adaptations

**iOS:**
- **Haptic Feedback**: Subtle feedback on card selection
- **Native Feel**: Follow iOS design patterns for card interactions
- **Dynamic Type**: Support iOS Dynamic Type for text scaling
- **Safe Areas**: Proper margin handling around screen edges

**Android:**
- **Material Design**: Elevation and shadow following Material guidelines
- **Ripple Effects**: Android-style touch feedback
- **Accessibility**: TalkBack optimization for card content
- **Performance**: Optimize for wide range of Android device capabilities

---

## Related Documentation
- [Button Components](./buttons.md) - Card action buttons
- [Typography Tokens](../tokens/typography.md) - Card text styling
- [Color Tokens](../tokens/colors.md) - Card color specifications
- [Animation Specifications](../tokens/animations.md) - Card animation timing

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*