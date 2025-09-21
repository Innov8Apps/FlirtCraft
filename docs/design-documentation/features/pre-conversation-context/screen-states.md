# Pre-Conversation Context Screen States

---
title: Pre-Conversation Context Screen States and Visual Specifications
description: Complete visual specifications for all screen states in context generation and review
feature: pre-conversation-context
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./interactions.md
  - ./accessibility.md
  - ./implementation.md
  - ../../design-system/components/context-cards.md
  - ../../design-system/components/buttons.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/tokens/spacing.md
dependencies:
  - AI context generation service
  - Context card components
  - Loading state animations
status: approved
---

## Overview

This document specifies all visual states for the pre-conversation context feature, from initial loading through context review and transition to conversation. Each state is designed to build user confidence and provide comprehensive scenario preparation.

## Screen State Hierarchy

### Primary States
1. **Context Generation Loading** - AI is creating scenario details
2. **Context Display** - Four context cards presented for review
3. **Regeneration Loading** - New context being generated
4. **Context Reference Modal** - Quick access during conversation

### Secondary States
5. **Generation Error** - Technical issues with context creation
6. **Empty/Timeout State** - Fallback when generation fails
7. **Help Overlay** - Context interpretation guidance

### Transition States
8. **Cards Entrance Animation** - Context cards appearing
9. **Conversation Transition** - Moving to chat interface
10. **Regeneration Transition** - Cards updating with new content

## State Specifications

### State 1: Context Generation Loading

**Visual Design:**
- **Layout**: Full-screen centered content with subtle background
- **Background**: Light neutral (`#F9FAFB`) with subtle texture
- **Primary Element**: Large loading animation with text
- **Progress Indication**: Animated pulse or spinner, no progress bar
- **Typography**: H2 heading with body text explanation

**Content Structure:**
```tsx
<VStack space={6} alignItems="center" justifyContent="center" flex={1}>
  <Box>
    {/* Animated loading icon */}
    <Icon name="sparkles" size={48} color="orange.500" />
  </Box>
  
  <VStack space={3} alignItems="center">
    <Text fontSize="xl" fontWeight="semibold" color="gray.800">
      Creating your scenario...
    </Text>
    <Text fontSize="md" color="gray.600" textAlign="center" maxW="280px">
      Our AI is crafting the perfect practice situation for you
    </Text>
  </VStack>
  
  <Box w={12} h={1} bg="orange.200" borderRadius="full">
    {/* Animated progress indicator */}
  </Box>
</VStack>
```

**Animation Specifications:**
- **Loading Icon**: Gentle rotation or pulsing animation
- **Text**: Fade in after 500ms delay
- **Progress Bar**: Indeterminate animation, left-to-right flow
- **Duration**: 2-3 seconds typical, 5 seconds maximum

**Responsive Adaptations:**
- **Mobile**: Full screen with comfortable padding
- **Tablet**: Centered with max width constraint
- **Loading States**: Same design scales appropriately

**Accessibility Features:**
- **Screen Reader**: "Creating your scenario, please wait"
- **Reduced Motion**: Static icons replace animations
- **Timeout Handling**: Clear error message if generation fails

### State 2: Context Display (Primary State)

**Overall Layout:**
- **Container**: Full-screen scrollable view with header
- **Background**: Light gray (`#F9FAFB`) for card contrast
- **Header**: Fixed header with progress indicator and controls
- **Content**: Four context cards in vertical scroll
- **Footer**: Action buttons (Start Conversation, Regenerate)

**Header Specifications:**
```tsx
<HStack
  justifyContent="space-between"
  alignItems="center"
  px={4}
  py={3}
  bg="white"
  shadow={1}
>
  <IconButton
    icon={<ArrowLeft size={24} />}
    onPress={navigateBack}
    accessibilityLabel="Return to scenario selection"
  />
  
  <VStack alignItems="center" space={1}>
    <Text fontSize="sm" fontWeight="medium" color="gray.700">
      Review Your Scenario
    </Text>
    <HStack space={1}>
      {[1,2,3,4].map(i => (
        <Box
          key={i}
          w={2}
          h={2}
          bg={reviewedCards >= i ? "orange.500" : "gray.300"}
          borderRadius="full"
        />
      ))}
    </HStack>
  </VStack>
  
  <IconButton
    icon={<HelpCircle size={24} />}
    onPress={showHelp}
    accessibilityLabel="Get help understanding context"
  />
</HStack>
```

**Context Cards Layout:**
- **Spacing**: 16px between cards, 20px margins
- **Card Design**: White background, rounded corners, subtle shadow
- **Card Order**: Practice Partner → Environment → Body Language → Conversation Starters
- **Animation**: Staggered entrance with 200ms delays

#### Card 1: Practice Partner Context

**Visual Structure:**
```tsx
<Box
  bg="white"
  borderRadius="xl"
  p={5}
  shadow={2}
  mb={4}
>
  <HStack space={4} alignItems="flex-start">
    <Box
      w={12}
      h={12}
      bg="orange.100"
      borderRadius="full"
      alignItems="center"
      justifyContent="center"
    >
      <Icon name="user" size={24} color="orange.600" />
    </Box>
    
    <VStack flex={1} space={3}>
      <Text fontSize="lg" fontWeight="semibold" color="gray.800">
        Your Practice Partner
      </Text>
      
      <VStack space={2}>
        <Text fontSize="md" color="gray.700">
          {partnerContext.ageRange} • {partnerContext.style}
        </Text>
        
        <Text fontSize="md" color="gray.600" lineHeight={22}>
          {partnerContext.activity}
        </Text>
        
        {partnerContext.details.map((detail, index) => (
          <Text key={index} fontSize="sm" color="gray.600">
            • {detail}
          </Text>
        ))}
      </VStack>
    </VStack>
  </HStack>
</Box>
```

**Content Elements:**
- **Icon Area**: Orange background with user icon
- **Header**: "Your Practice Partner" with clear hierarchy
- **Age/Style**: Quick demographic and style overview
- **Current Activity**: What they're doing right now
- **Observable Details**: 3-4 specific details user can reference

**Color Treatment:**
- **Icon Background**: Orange (`#FED7AA`) with darker icon (`#EA580C`)
- **Text Hierarchy**: Dark gray headings, medium gray body text
- **Details**: Lighter gray for supplementary information

#### Card 2: Environment Context

**Visual Structure:**
```tsx
<Box
  bg="white"
  borderRadius="xl"
  p={5}
  shadow={2}
  mb={4}
>
  <HStack space={4} alignItems="flex-start">
    <Box
      w={12}
      h={12}
      bg="green.100"
      borderRadius="full"
      alignItems="center"
      justifyContent="center"
    >
      <Icon name="map-pin" size={24} color="green.600" />
    </Box>
    
    <VStack flex={1} space={3}>
      <Text fontSize="lg" fontWeight="semibold" color="gray.800">
        Environment & Setting
      </Text>
      
      <VStack space={2}>
        <HStack justifyContent="space-between" alignItems="center">
          <Text fontSize="md" color="gray.700">
            {environmentContext.timeContext}
          </Text>
          <Badge colorScheme={crowdLevelColor} variant="subtle">
            {environmentContext.crowdLevel}
          </Badge>
        </HStack>
        
        <Text fontSize="md" color="gray.600" lineHeight={22}>
          {environmentContext.atmosphere}
        </Text>
        
        {environmentContext.details.map((detail, index) => (
          <Text key={index} fontSize="sm" color="gray.600">
            • {detail}
          </Text>
        ))}
      </VStack>
    </VStack>
  </HStack>
</Box>
```

**Content Elements:**
- **Icon Area**: Green background with location icon
- **Time Context**: Day/time with crowd level indicator
- **Atmosphere**: Overall mood and environment description
- **Environmental Details**: Sounds, lighting, general vibe elements

**Color Treatment:**
- **Icon Background**: Green (`#DCFCE7`) with darker icon (`#16A34A`)
- **Crowd Level Badge**: Dynamic color based on busy level
- **Hierarchy**: Consistent with Partner card structure

#### Card 3: Body Language Signals

**Visual Structure:**
```tsx
<Box
  bg="white"
  borderRadius="xl"
  p={5}
  shadow={2}
  mb={4}
>
  <HStack space={4} alignItems="flex-start">
    <Box
      w={12}
      h={12}
      bg="blue.100"
      borderRadius="full"
      alignItems="center"
      justifyContent="center"
    >
      <Icon name="eye" size={24} color="blue.600" />
    </Box>
    
    <VStack flex={1} space={3}>
      <Text fontSize="lg" fontWeight="semibold" color="gray.800">
        Body Language Signals
      </Text>
      
      <VStack space={3}>
        {bodyLanguageSignals.map((signal, index) => (
          <HStack key={index} space={3} alignItems="flex-start">
            <Box
              w={3}
              h={3}
              bg={getSignalColor(signal.type)}
              borderRadius="full"
              mt={2}
            />
            <VStack flex={1} space={1}>
              <Text fontSize="sm" fontWeight="medium" color="gray.700">
                {getSignalLabel(signal.type)}
              </Text>
              <Text fontSize="sm" color="gray.600" lineHeight={18}>
                {signal.description}
              </Text>
            </VStack>
          </HStack>
        ))}
        
        <Box
          bg="gray.50"
          borderRadius="lg"
          p={3}
          borderLeftWidth={3}
          borderLeftColor={getOverallReceptivenessColor()}
        >
          <Text fontSize="sm" fontWeight="medium" color="gray.700">
            Overall Assessment
          </Text>
          <Text fontSize="sm" color="gray.600" mt={1}>
            {bodyLanguageContext.overall}
          </Text>
        </Box>
      </VStack>
    </VStack>
  </HStack>
</Box>
```

**Content Elements:**
- **Icon Area**: Blue background with eye icon
- **Signal Indicators**: Color-coded dots (Green/Yellow/Red)
- **Signal Descriptions**: Clear explanation of each observed behavior
- **Overall Assessment**: Summary sidebar with receptiveness level

**Color Coding System:**
- **Green Signals**: Positive receptiveness (`#10B981`)
- **Yellow Signals**: Neutral/mixed (`#F59E0B`)
- **Red Signals**: Challenging/distracted (`#EF4444`)
- **Assessment Bar**: Color matches overall difficulty level

**Signal Types and Colors:**
```tsx
const getSignalColor = (type: string) => {
  switch (type) {
    case 'positive': return 'green.500';
    case 'neutral': return 'yellow.500';
    case 'challenging': return 'red.500';
    default: return 'gray.400';
  }
};

const getSignalLabel = (type: string) => {
  switch (type) {
    case 'positive': return 'Encouraging Signal';
    case 'neutral': return 'Neutral Signal';
    case 'challenging': return 'Cautious Signal';
    default: return 'Mixed Signal';
  }
};
```

#### Card 4: Conversation Starters

**Visual Structure:**
```tsx
<Box
  bg="white"
  borderRadius="xl"
  p={5}
  shadow={2}
  mb={4}
>
  <HStack space={4} alignItems="flex-start">
    <Box
      w={12}
      h={12}
      bg="purple.100"
      borderRadius="full"
      alignItems="center"
      justifyContent="center"
    >
      <Icon name="message-circle" size={24} color="purple.600" />
    </Box>
    
    <VStack flex={1} space={3}>
      <Text fontSize="lg" fontWeight="semibold" color="gray.800">
        Conversation Starters
      </Text>
      
      <Text fontSize="sm" color="gray.600" mb={2}>
        Choose one to break the ice, or use as inspiration:
      </Text>
      
      <VStack space={3}>
        {conversationStarters.map((starter, index) => (
          <Pressable
            key={index}
            onPress={() => selectStarter(starter)}
          >
            {({ isPressed }) => (
              <Box
                bg={isPressed ? "purple.50" : "gray.50"}
                borderRadius="lg"
                p={4}
                borderWidth={1}
                borderColor={isPressed ? "purple.200" : "gray.200"}
              >
                <HStack space={3} alignItems="center">
                  <Box
                    w={6}
                    h={6}
                    bg="purple.100"
                    borderRadius="full"
                    alignItems="center"
                    justifyContent="center"
                  >
                    <Text fontSize="xs" fontWeight="bold" color="purple.600">
                      {index + 1}
                    </Text>
                  </Box>
                  <Text flex={1} fontSize="md" color="gray.700" lineHeight={20}>
                    "{starter}"
                  </Text>
                </HStack>
              </Box>
            )}
          </Pressable>
        ))}
      </VStack>
      
      <Box bg="purple.50" borderRadius="lg" p={3} mt={2}>
        <Text fontSize="xs" color="purple.700" textAlign="center">
          💡 Tap any starter to use it in conversation, or create your own!
        </Text>
      </Box>
    </VStack>
  </HStack>
</Box>
```

**Content Elements:**
- **Icon Area**: Purple background with message icon
- **Usage Instructions**: Clear guidance on how to use starters
- **Starter Options**: 3-4 contextually appropriate conversation openers
- **Selection Interaction**: Tap to select and use in conversation
- **Helpful Tip**: Encouragement about customization

**Interactive Features:**
- **Tap Feedback**: Visual feedback when starter is selected
- **Copy Functionality**: Selected starter available in conversation input
- **Customization**: Users can edit selected starter before sending

**Color Treatment:**
- **Icon Background**: Purple (`#EDE9FE`) with darker icon (`#9333EA`)
- **Starter Bubbles**: Light gray background with purple accent on selection
- **Tip Box**: Purple background with complementary text

### Action Buttons Area

**Button Layout:**
```tsx
<VStack
  space={3}
  px={4}
  py={4}
  bg="white"
  borderTopWidth={1}
  borderTopColor="gray.200"
>
  <Button
    size="lg"
    bg="orange.500"
    _pressed={{ bg: "orange.600" }}
    _disabled={{ bg: "gray.400" }}
    disabled={!allCardsReviewed}
    onPress={startConversation}
  >
    <Text fontSize="md" fontWeight="semibold" color="white">
      Start Conversation
    </Text>
  </Button>
  
  <HStack space={3}>
    <Button
      flex={1}
      variant="outline"
      borderColor="orange.200"
      _pressed={{ bg: "orange.50" }}
      onPress={regenerateContext}
    >
      <Text fontSize="sm" color="orange.600">
        Generate New Context
      </Text>
    </Button>
    
    <Button
      flex={1}
      variant="ghost"
      _pressed={{ bg: "gray.100" }}
      onPress={navigateBack}
    >
      <Text fontSize="sm" color="gray.600">
        Back to Scenarios
      </Text>
    </Button>
  </HStack>
</VStack>
```

**Button States:**
- **Primary Action**: Orange gradient, full width, prominent
- **Secondary Actions**: Outline and ghost styles, equal width
- **Disabled State**: Gray background when cards not fully reviewed
- **Loading State**: Spinner replaces text during actions

### State 3: Regeneration Loading

**Visual Changes from Context Display:**
- **Cards**: Fade out with scale animation
- **Loading Overlay**: Semi-transparent overlay with spinner
- **Button State**: "Generate New Context" shows loading spinner
- **Duration**: 1-2 seconds for regeneration (faster than initial)

**Animation Sequence:**
1. Cards scale down and fade (300ms)
2. Loading overlay appears (200ms)
3. New cards scale up and fade in (400ms with stagger)
4. Action buttons re-enable

**User Feedback:**
```tsx
<Box
  position="absolute"
  top={0}
  left={0}
  right={0}
  bottom={0}
  bg="rgba(255,255,255,0.9)"
  alignItems="center"
  justifyContent="center"
>
  <VStack space={4} alignItems="center">
    <Spinner size="lg" color="orange.500" />
    <Text fontSize="md" color="gray.700">
      Creating new scenario...
    </Text>
  </VStack>
</Box>
```

### State 4: Context Reference Modal (During Conversation)

**Modal Design:**
- **Presentation**: Slide up from bottom, 60% screen height
- **Background**: White with rounded top corners
- **Content**: Condensed version of context cards
- **Navigation**: Swipe between context categories
- **Dismissal**: Tap backdrop, swipe down, or close button

**Condensed Card Format:**
```tsx
<ScrollView horizontal showsHorizontalScrollIndicator={false}>
  <HStack space={4} px={4}>
    {contextSummaries.map((summary, index) => (
      <Box
        key={index}
        w={280}
        bg="white"
        borderRadius="lg"
        p={4}
        shadow={1}
      >
        <HStack space={3} alignItems="center" mb={3}>
          <Icon name={summary.icon} size={20} color="orange.500" />
          <Text fontSize="md" fontWeight="semibold">
            {summary.title}
          </Text>
        </HStack>
        
        <Text fontSize="sm" color="gray.600" numberOfLines={4}>
          {summary.content}
        </Text>
      </Box>
    ))}
  </HStack>
</ScrollView>
```

### State 5: Generation Error

**Error Display:**
```tsx
<VStack space={6} alignItems="center" justifyContent="center" flex={1} px={6}>
  <Box
    w={16}
    h={16}
    bg="red.100"
    borderRadius="full"
    alignItems="center"
    justifyContent="center"
  >
    <Icon name="alert-triangle" size={32} color="red.500" />
  </Box>
  
  <VStack space={3} alignItems="center">
    <Text fontSize="xl" fontWeight="semibold" color="gray.800" textAlign="center">
      We're having trouble creating your scenario
    </Text>
    
    <Text fontSize="md" color="gray.600" textAlign="center" lineHeight={22}>
      Don't worry! Let's try again or you can choose a different scenario.
    </Text>
  </VStack>
  
  <VStack space={3} w="100%">
    <Button
      size="lg"
      bg="orange.500"
      onPress={retryGeneration}
    >
      Try Again
    </Button>
    
    <Button
      variant="outline"
      borderColor="gray.300"
      onPress={useFallbackContent}
    >
      Use Quick Scenario
    </Button>
    
    <Button
      variant="ghost"
      onPress={navigateBack}
    >
      Choose Different Scenario
    </Button>
  </VStack>
</VStack>
```

**Error Recovery Options:**
- **Retry**: Attempt generation again with same parameters
- **Fallback**: Use pre-written context for this scenario/difficulty combination  
- **Navigate Back**: Return to scenario selection for different choice

### State 6: Help Overlay

**Overlay Design:**
- **Background**: Semi-transparent backdrop
- **Content**: Centered modal with explanation
- **Dismissal**: Tap backdrop or close button
- **Purpose**: Explain how to interpret context cards

**Help Content Structure:**
```tsx
<Box
  bg="white"
  borderRadius="xl"
  p={6}
  mx={4}
  maxH="80%"
>
  <HStack justifyContent="space-between" alignItems="center" mb={4}>
    <Text fontSize="lg" fontWeight="semibold">
      Understanding Your Context
    </Text>
    <IconButton
      icon={<X size={24} />}
      onPress={closeHelp}
    />
  </HStack>
  
  <ScrollView>
    <VStack space={4}>
      <HelpSection
        icon="user"
        title="Practice Partner"
        description="Details about who you'll be talking to - their appearance, what they're doing, and what you can observe."
      />
      
      <HelpSection
        icon="map-pin"
        title="Environment"
        description="The setting details - time, crowd, atmosphere. Use this to understand the social context."
      />
      
      <HelpSection
        icon="eye"
        title="Body Language"
        description="Signals about receptiveness. Green = encouraging, Yellow = neutral, Red = cautious or distracted."
      />
      
      <HelpSection
        icon="message-circle"
        title="Conversation Starters"
        description="Ready-to-use openers that fit your scenario. Tap any to use it, or create your own!"
      />
    </VStack>
  </ScrollView>
</Box>
```

## Responsive Design Adaptations

### Mobile Portrait (320px - 480px)

**Layout Adjustments:**
- **Cards**: Full width with 16px margins
- **Text Sizing**: Slightly smaller for readability
- **Touch Targets**: Minimum 44px for all interactive elements
- **Scrolling**: Optimized for single-finger scrolling

### Mobile Landscape (568px - 812px)

**Layout Changes:**
- **Cards**: Reduced padding, tighter spacing
- **Header**: More compact with combined elements
- **Buttons**: Horizontal layout for action buttons
- **Modal**: Adjusted height for landscape constraints

### Tablet (768px+)

**Enhanced Layout:**
- **Cards**: Two-column layout for better space usage
- **Sidebar**: Context reference as persistent sidebar option
- **Typography**: Larger text for comfortable reading
- **Interaction**: Mouse hover states for web deployment

## Accessibility Specifications

### Screen Reader Support

**Card Structure:**
```tsx
<Box
  accessible={true}
  accessibilityRole="region"
  accessibilityLabel="Practice partner context card"
>
  {/* Card content with proper headings */}
</Box>
```

**Reading Order:**
1. Header with progress indication
2. Each context card as individual region
3. Action buttons with clear labels
4. Help button with descriptive hint

### Keyboard Navigation

**Tab Order:**
1. Back button
2. Help button  
3. Each context card (focusable for details)
4. Action buttons in priority order
5. Secondary action buttons

**Keyboard Shortcuts:**
- **Space**: Activate focused button
- **Enter**: Primary action (Start Conversation)
- **Escape**: Back navigation or close modal
- **Arrow Keys**: Navigate between cards

### Visual Accessibility

**High Contrast Mode:**
- **Card Borders**: Increased contrast and thickness
- **Text**: Enhanced contrast ratios
- **Icons**: Outlined versions for better definition
- **Focus Indicators**: High contrast focus rings

**Text Scaling Support:**
- **Layout**: Maintains structure up to 200% scaling
- **Cards**: Expand vertically to accommodate larger text
- **Buttons**: Maintain touch target sizes
- **Scrolling**: Horizontal scroll when needed

## Animation Specifications

### Card Entrance Animation

```tsx
const cardVariants = {
  hidden: { 
    opacity: 0, 
    scale: 0.8, 
    y: 20 
  },
  visible: (i: number) => ({
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      delay: i * 0.1,
      duration: 0.4,
      ease: "easeOut"
    }
  })
};
```

**Animation Sequence:**
1. Cards start scaled down and transparent
2. Each card animates in with 100ms stagger
3. Smooth easing for natural feel
4. Action buttons animate in last

### Transition to Conversation

```tsx
const transitionVariants = {
  exit: {
    scale: 0.95,
    opacity: 0,
    transition: { duration: 0.3 }
  }
};
```

**Transition Flow:**
1. Cards scale down slightly and fade
2. New screen slides in from right
3. Context data transfers seamlessly
4. No loading state needed

## Performance Considerations

### Image Optimization

**Icons and Graphics:**
- SVG icons for scalability
- Optimized PNG fallbacks for complex graphics
- Lazy loading for non-critical images
- Proper caching strategies

### Animation Performance

**60fps Targets:**
- Use transform properties for animations
- Avoid animating layout properties
- Implement proper shouldComponentUpdate
- Use React Native Reanimated for complex animations

### Memory Management

**Component Optimization:**
- Lazy load non-visible content
- Proper cleanup of event listeners
- Efficient re-rendering with React.memo
- Context data cleanup on navigation

---

## Related Documentation

- [Pre-Conversation Context README](./README.md) - Feature overview and requirements
- [User Journey](./user-journey.md) - Complete user flow through context review
- [Interactions](./interactions.md) - Detailed interaction and animation specifications
- [Context Cards Component](../../design-system/components/context-cards.md) - Reusable component specifications

## Implementation Checklist

### Core Screen States
- [ ] Context generation loading state implemented
- [ ] Four context cards display correctly
- [ ] Action buttons with proper states
- [ ] Regeneration loading flow
- [ ] Error state with recovery options

### Interactive Features
- [ ] Context card scrolling and review tracking
- [ ] Conversation starter selection
- [ ] Context reference modal during conversation
- [ ] Help overlay with usage guidance
- [ ] Smooth animations between states

### Responsive Design
- [ ] Mobile portrait optimization
- [ ] Mobile landscape adaptations
- [ ] Tablet layout enhancements
- [ ] Accessibility compliance verified
- [ ] Performance testing completed

---

*These screen state specifications ensure a consistent, accessible, and engaging experience as users prepare for their FlirtCraft practice conversations through comprehensive context review.*