# Typography Tokens

---
title: FlirtCraft Typography System
description: Font families, weights, sizes, line heights, and responsive scaling specifications
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../../accessibility/guidelines.md
dependencies:
  - Inter font family
  - Platform system fonts as fallbacks
status: approved
---

## Overview

FlirtCraft's typography system creates clear information hierarchy while maintaining readability and accessibility across all platforms. The system uses a mathematical type scale that adapts to different screen sizes and user preferences.

## Font Family Tokens

### Primary Font Stack

**Token**: `font-family-primary`
**Value**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif`

**Rationale:**
- **Inter**: Primary typeface chosen for excellent readability and comprehensive character set
- **System Fonts**: Fallbacks provide native feel and performance on each platform
- **Sans-serif**: Clean, modern appearance appropriate for mobile interfaces

### Monospace Font Stack

**Token**: `font-family-mono`
**Value**: `'SF Mono', 'Monaco', 'Cascadia Code', 'Consolas', 'JetBrains Mono', 'Roboto Mono', 'Oxygen Mono', 'Ubuntu Mono', monospace`

**Usage:**
- Code examples in help documentation
- Technical error messages
- API responses in debug modes (development only)

## Font Weight Tokens

### Weight Scale

**Ultra Light** - `font-weight-100`: `100`
- **Usage**: Decorative text, very large display elements
- **Rarely Used**: Not common in FlirtCraft interface

**Light** - `font-weight-300`: `300`
- **Usage**: Large display text, decorative elements
- **Example**: Hero text on welcome screens

**Regular** - `font-weight-400`: `400`
- **Usage**: Body text, standard interface elements
- **Primary**: Most common weight for readable content

**Medium** - `font-weight-500`: `500`
- **Usage**: Emphasized text, secondary headings, important labels
- **Example**: Card titles, form labels, navigation items

**Semibold** - `font-weight-600`: `600`
- **Usage**: Primary headings, button text, important UI labels
- **Example**: Section headers, CTA buttons

**Bold** - `font-weight-700`: `700`
- **Usage**: Primary headings, strong emphasis, brand elements
- **Example**: Screen titles, achievement names

**Extra Bold** - `font-weight-800`: `800`
- **Usage**: Display text, special emphasis
- **Limited Use**: Only for specific brand moments

## Typography Scale Tokens

### Mobile Type Scale (320px - 767px)

Primary target for FlirtCraft's mobile-first design approach.

#### Heading Tokens

**H1** - `typography-h1-mobile`
```json
{
  "fontSize": "28px",
  "lineHeight": "36px", 
  "fontWeight": "700",
  "letterSpacing": "-0.02em",
  "marginBottom": "16px"
}
```
- **Usage**: Screen titles, major section headers
- **Example**: "Choose Your Practice Location", "Conversation Complete!"

**H2** - `typography-h2-mobile`
```json
{
  "fontSize": "24px",
  "lineHeight": "32px",
  "fontWeight": "600", 
  "letterSpacing": "-0.01em",
  "marginBottom": "12px"
}
```
- **Usage**: Section headers, card titles
- **Example**: "Your Practice Partner", "Body Language Signals"

**H3** - `typography-h3-mobile`
```json
{
  "fontSize": "20px",
  "lineHeight": "28px",
  "fontWeight": "600",
  "letterSpacing": "0em",
  "marginBottom": "12px"
}
```
- **Usage**: Subsection headers, feature titles
- **Example**: Scenario names, achievement titles

**H4** - `typography-h4-mobile`
```json
{
  "fontSize": "18px",
  "lineHeight": "24px", 
  "fontWeight": "500",
  "letterSpacing": "0em",
  "marginBottom": "8px"
}
```
- **Usage**: Minor headers, component titles
- **Example**: Form section labels, settings categories

**H5** - `typography-h5-mobile`
```json
{
  "fontSize": "16px",
  "lineHeight": "22px",
  "fontWeight": "500", 
  "letterSpacing": "0em",
  "marginBottom": "8px"
}
```
- **Usage**: List headers, metadata labels
- **Example**: Skill category names, progress section titles

#### Body Text Tokens

**Body Large** - `typography-body-large-mobile`
```json
{
  "fontSize": "18px",
  "lineHeight": "26px",
  "fontWeight": "400",
  "letterSpacing": "0em",
  "marginBottom": "12px"
}
```
- **Usage**: Primary reading text, important descriptions
- **Example**: Onboarding explanations, conversation context

**Body** - `typography-body-mobile`
```json
{
  "fontSize": "16px",
  "lineHeight": "22px",
  "fontWeight": "400", 
  "letterSpacing": "0em",
  "marginBottom": "12px"
}
```
- **Usage**: Standard UI text, form fields, chat messages
- **Example**: Button text, input fields, conversation bubbles

**Body Small** - `typography-body-small-mobile`
```json
{
  "fontSize": "14px",
  "lineHeight": "20px",
  "fontWeight": "400",
  "letterSpacing": "0em", 
  "marginBottom": "8px"
}
```
- **Usage**: Secondary information, captions
- **Example**: Error messages, help text, timestamps

#### Specialized Text Tokens

**Caption** - `typography-caption-mobile`
```json
{
  "fontSize": "12px",
  "lineHeight": "16px",
  "fontWeight": "400",
  "letterSpacing": "0.01em",
  "marginBottom": "4px"
}
```
- **Usage**: Metadata, timestamps, fine print
- **Example**: "2 minutes ago", "Terms and Conditions", copyright

**Label** - `typography-label-mobile`
```json
{
  "fontSize": "14px",
  "lineHeight": "20px",
  "fontWeight": "500",
  "letterSpacing": "0.02em",
  "textTransform": "uppercase",
  "marginBottom": "4px"
}
```
- **Usage**: Form labels, categories, badges
- **Example**: "GREEN", "DIFFICULTY", input field labels

#### Button Text Tokens

**Button Large** - `typography-button-large-mobile`
```json
{
  "fontSize": "18px",
  "lineHeight": "24px",
  "fontWeight": "600",
  "letterSpacing": "0em"
}
```
- **Usage**: Primary action buttons, important CTAs
- **Example**: "Start Conversation", "Continue"

**Button** - `typography-button-mobile`
```json
{
  "fontSize": "16px",
  "lineHeight": "20px", 
  "fontWeight": "600",
  "letterSpacing": "0em"
}
```
- **Usage**: Standard buttons, secondary CTAs
- **Example**: "Back", "Try Again", "Settings"

**Button Small** - `typography-button-small-mobile`
```json
{
  "fontSize": "14px",
  "lineHeight": "18px",
  "fontWeight": "500",
  "letterSpacing": "0em"
}
```
- **Usage**: Minor actions, tertiary buttons
- **Example**: "Skip", "Learn More", icon buttons with text

### Tablet Type Scale (768px - 1023px)

Enhanced sizing for tablet viewing distances and screen real estate.

#### Heading Adjustments

**H1** - `typography-h1-tablet`
- **fontSize**: `32px` (increased from 28px)
- **lineHeight**: `40px` (proportional increase)
- **Other properties**: Inherit from mobile

**H2** - `typography-h2-tablet`  
- **fontSize**: `28px` (increased from 24px)
- **lineHeight**: `36px` (proportional increase)

**Body Large** - `typography-body-large-tablet`
- **fontSize**: `20px` (increased from 18px)
- **lineHeight**: `28px` (enhanced for comfortable reading)

### Desktop Type Scale (1024px+)

Optimized for desktop viewing distances and productivity use cases.

#### Desktop Enhancements

**H1** - `typography-h1-desktop`
- **fontSize**: `36px` (desktop prominence)
- **lineHeight**: `44px` (optimal for large screens)

**H2** - `typography-h2-desktop`
- **fontSize**: `32px` (clear hierarchy)
- **lineHeight**: `40px` (proportional)

**Body Large** - `typography-body-large-desktop` 
- **fontSize**: `20px` (maintained from tablet)
- **lineHeight**: `28px` (optimal reading length)

## Platform-Specific Tokens

### iOS Typography Tokens

**Dynamic Type Support**
- All typography tokens include iOS Dynamic Type categories
- Automatic scaling based on user's text size preference
- Maintains proportional relationships across scale

**iOS Font Mapping:**
```json
{
  "typography-h1-ios": {
    "dynamicTypeCategory": "largeTitle",
    "fontSize": "28px",
    "minimumScaleFactor": 0.8
  },
  "typography-body-ios": {
    "dynamicTypeCategory": "body", 
    "fontSize": "16px",
    "minimumScaleFactor": 0.8
  }
}
```

### Android Typography Tokens

**Material Design Alignment**
- Typography tokens align with Material Design 3 specifications
- Support for Android's font scale preferences
- Roboto font optimization where available

**Android Font Mapping:**
```json
{
  "typography-h1-android": {
    "materialCategory": "headlineLarge",
    "fontSize": "28px", 
    "scaleCategory": "large"
  },
  "typography-body-android": {
    "materialCategory": "bodyMedium",
    "fontSize": "16px",
    "scaleCategory": "medium"
  }
}
```

## Accessibility Typography Tokens

### High Contrast Tokens

Enhanced typography for high contrast mode and low vision accessibility.

**High Contrast Body** - `typography-body-high-contrast`
```json
{
  "fontSize": "18px",
  "lineHeight": "26px", 
  "fontWeight": "500",
  "letterSpacing": "0.01em"
}
```

**High Contrast Small** - `typography-small-high-contrast`
```json
{
  "fontSize": "16px",
  "lineHeight": "24px",
  "fontWeight": "500", 
  "letterSpacing": "0.02em"
}
```

### Large Text Tokens

Typography tokens for users who require larger text sizes.

**Large Text Scale Multiplier** - `typography-scale-large`: `1.25`
- Applies 25% increase to all font sizes
- Maintains proportional line height increases
- Preserves design hierarchy relationships

### Reduced Motion Tokens

Typography behavior for users who prefer reduced motion.

**Static Text** - `typography-reduced-motion`
```json
{
  "animationDuration": "0s",
  "transitionDuration": "0s",
  "transform": "none"
}
```

## Usage Guidelines

### Hierarchy Best Practices

**Information Architecture:**
- Use heading levels sequentially (H1 → H2 → H3)
- Don't skip heading levels for visual effect
- Maintain consistent heading usage across similar content

**Content Relationships:**
- Related content uses consistent typography tokens
- Vary weight rather than size for subtle emphasis
- Use color and spacing to support typography hierarchy

### Performance Considerations

**Font Loading:**
- Inter font loaded with `font-display: swap`
- System font fallbacks prevent layout shift
- Critical text uses system fonts during load

**Rendering Optimization:**
- Avoid excessive font weight variations
- Minimize custom font variations to reduce load
- Use system font features where appropriate

### Responsive Typography

**Breakpoint Behavior:**
- Typography scales smoothly between breakpoints
- No abrupt size changes at breakpoint boundaries
- Maintains readability at all screen sizes

**Container Query Support (Future):**
- Typography tokens prepared for container-based scaling
- Component-level responsive typography
- Context-aware text sizing

## Implementation Examples

### React Native Implementation

```jsx
// Typography token usage in React Native with NativeBase
import { Text, VStack } from 'native-base';

const ConversationCard = () => (
  <VStack space={3}>
    <Text 
      fontSize="h2" 
      fontWeight="semibold"
      color="neutral.800"
    >
      Coffee Shop
    </Text>
    <Text 
      fontSize="body"
      lineHeight="22px"
      color="neutral.700"  
    >
      Casual and relaxed conversations in a welcoming atmosphere.
    </Text>
    <Text
      fontSize="caption"
      color="neutral.500"
      letterSpacing="0.01em"
    >
      Last visited 2 hours ago
    </Text>
  </VStack>
);
```

### CSS Implementation

```css
/* Generated CSS custom properties from typography tokens */
:root {
  --typography-h1-font-size: 28px;
  --typography-h1-line-height: 36px;
  --typography-h1-font-weight: 700;
  --typography-h1-letter-spacing: -0.02em;
  
  --typography-body-font-size: 16px;
  --typography-body-line-height: 22px;
  --typography-body-font-weight: 400;
}

/* Usage in components */
.screen-title {
  font-size: var(--typography-h1-font-size);
  line-height: var(--typography-h1-line-height);
  font-weight: var(--typography-h1-font-weight);
  letter-spacing: var(--typography-h1-letter-spacing);
}

.body-text {
  font-size: var(--typography-body-font-size);
  line-height: var(--typography-body-line-height);
  font-weight: var(--typography-body-font-weight);
}
```

### NativeWind Implementation

```jsx
// Using typography tokens through NativeWind classes
<View className="p-4">
  <Text className="text-h1 font-bold text-neutral-800 mb-4">
    Welcome to FlirtCraft
  </Text>
  <Text className="text-body text-neutral-700 leading-relaxed">
    Practice conversations in a safe, supportive environment.
  </Text>
  <Text className="text-caption text-neutral-500 mt-2 tracking-wide">
    Join thousands building confidence daily
  </Text>
</View>
```

## Token Export Format

### JSON Export Structure

```json
{
  "typography": {
    "fontFamilies": {
      "primary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      "mono": "'SF Mono', 'Consolas', 'JetBrains Mono', monospace"
    },
    "fontWeights": {
      "light": 300,
      "regular": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    },
    "fontSizes": {
      "mobile": {
        "h1": "28px",
        "h2": "24px", 
        "body": "16px",
        "caption": "12px"
      },
      "tablet": {
        "h1": "32px",
        "h2": "28px",
        "body": "16px" 
      },
      "desktop": {
        "h1": "36px",
        "h2": "32px",
        "body": "16px"
      }
    },
    "lineHeights": {
      "mobile": {
        "h1": "36px",
        "h2": "32px",
        "body": "22px",
        "caption": "16px"
      }
    },
    "letterSpacing": {
      "h1": "-0.02em",
      "h2": "-0.01em", 
      "body": "0em",
      "caption": "0.01em",
      "label": "0.02em"
    }
  }
}
```

---

## Related Documentation

- [Color Tokens](./colors.md) - Text color specifications
- [Spacing Tokens](./spacing.md) - Text spacing and margins
- [Style Guide](../style-guide.md) - Typography usage in design system
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Typography accessibility requirements

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*