# Spacing Tokens

---
title: FlirtCraft Spacing System
description: Mathematical spacing scale, grid system, and layout specifications
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../../accessibility/guidelines.md
dependencies:
  - 4px base unit system
status: approved
---

## Overview

FlirtCraft's spacing system creates consistent, harmonious layouts through a mathematical approach based on a 4px base unit. This system ensures visual rhythm, improves accessibility, and maintains design consistency across all platforms and screen sizes.

## Base Unit System

### Foundation Token

**Token**: `spacing-base`
**Value**: `4px`

**Rationale:**
- **Mathematical**: All spacing derives from this base for perfect mathematical relationships
- **Accessibility**: 4px aligns with common accessibility requirements for touch targets
- **Platform Native**: Works well with both iOS (8-point grid) and Android (4dp grid) systems
- **Scalability**: Easy to scale proportionally for different screen densities

### Calculation Formula

All spacing tokens follow the formula: `spacing-base × multiplier`

## Spacing Scale Tokens

### Micro Spacing

**Token**: `spacing-xs`
**Value**: `2px` (base × 0.5)
**Usage:**
- Fine borders and dividers
- Tight element grouping
- Icon-to-text spacing in compact areas
- Subtle visual separations

**Examples:**
- Border width on input fields
- Spacing between inline elements
- Padding inside small badges

### Small Spacing

**Token**: `spacing-sm`
**Value**: `4px` (base × 1)
**Usage:**
- Internal component padding
- Small element margins
- List item spacing
- Icon padding

**Examples:**
- Padding inside small buttons
- Spacing between form field elements
- Internal card padding for compact content

### Medium Spacing (Default)

**Token**: `spacing-md`
**Value**: `8px` (base × 2)
**Usage:**
- Default spacing between related elements
- Standard margins and padding
- Component internal spacing
- Text-to-element spacing

**Examples:**
- Padding inside standard buttons
- Margin between paragraphs
- Spacing between form fields
- Icon-to-label spacing

### Large Spacing

**Token**: `spacing-lg`
**Value**: `12px` (base × 3)
**Usage:**
- Spacing between component groups
- Section separations
- Card content padding
- Header/footer margins

**Examples:**
- Padding inside cards
- Spacing between different UI sections
- Margin around major page elements

### Extra Large Spacing

**Token**: `spacing-xl`
**Value**: `16px` (base × 4)
**Usage:**
- Major section separation
- Page-level padding and margins
- Large component spacing
- Screen edge margins

**Examples:**
- Screen horizontal margins
- Spacing between major layout sections
- Padding around primary content areas

### Double Extra Large Spacing

**Token**: `spacing-2xl`
**Value**: `24px` (base × 6)
**Usage:**
- Large section separation
- Major layout gaps
- Hero section spacing
- Screen-level margins

**Examples:**
- Spacing between onboarding steps
- Major content block separation
- Large screen content margins

### Triple Extra Large Spacing

**Token**: `spacing-3xl`
**Value**: `32px` (base × 8)
**Usage:**
- Major layout sections
- Hero content spacing
- Large screen adaptations
- Special emphasis areas

**Examples:**
- Hero section internal spacing
- Major page section gaps
- Large tablet/desktop spacing

### Quadruple Extra Large Spacing

**Token**: `spacing-4xl`
**Value**: `48px` (base × 12)
**Usage:**
- Massive layout gaps
- Special content areas
- Large screen optimizations
- Marketing/landing content

**Examples:**
- Welcome screen hero spacing
- Large screen content separation
- Special feature highlighting

### Maximum Spacing

**Token**: `spacing-5xl`
**Value**: `64px` (base × 16)
**Usage:**
- Largest possible spacing
- Desktop-only layouts
- Special brand moments
- Maximum visual impact

**Examples:**
- Large desktop hero sections
- Brand showcase areas
- Maximum emphasis spacing

## Grid System Tokens

### Column Definitions

**Mobile Grid** - `grid-columns-mobile`
```json
{
  "columns": 4,
  "gutters": "16px",
  "margins": "16px",
  "containerWidth": "100%"
}
```

**Tablet Grid** - `grid-columns-tablet` 
```json
{
  "columns": 8,
  "gutters": "20px", 
  "margins": "24px",
  "containerWidth": "100%"
}
```

**Desktop Grid** - `grid-columns-desktop`
```json
{
  "columns": 12,
  "gutters": "24px",
  "margins": "32px", 
  "containerWidth": "1200px"
}
```

### Grid Gutter Tokens

**Mobile Gutters** - `spacing-gutter-mobile`: `16px` (base × 4)
**Tablet Gutters** - `spacing-gutter-tablet`: `20px` (base × 5)
**Desktop Gutters** - `spacing-gutter-desktop`: `24px` (base × 6)

## Breakpoint Tokens

### Breakpoint Definitions

**Mobile** - `breakpoint-mobile`
```json
{
  "min": "320px",
  "max": "767px",
  "name": "mobile"
}
```

**Tablet** - `breakpoint-tablet`
```json
{
  "min": "768px", 
  "max": "1023px",
  "name": "tablet"
}
```

**Desktop** - `breakpoint-desktop`
```json
{
  "min": "1024px",
  "max": "1439px", 
  "name": "desktop"
}
```

**Wide Screen** - `breakpoint-wide`
```json
{
  "min": "1440px",
  "name": "wide"
}
```

## Safe Area Tokens

### Device Safe Areas

**Safe Area Top** - `spacing-safe-top`
**Value**: Variable by device
**Usage**: Top safe area for notches, dynamic islands

**Safe Area Bottom** - `spacing-safe-bottom`  
**Value**: Variable by device
**Usage**: Bottom safe area for home indicators

**Safe Area Horizontal** - `spacing-safe-horizontal`
**Value**: Variable by device
**Usage**: Left/right safe areas for curved screens

### Standard Safe Margins

**Screen Margin Mobile** - `spacing-screen-margin-mobile`: `16px`
**Screen Margin Tablet** - `spacing-screen-margin-tablet`: `24px`
**Screen Margin Desktop** - `spacing-screen-margin-desktop`: `32px`

## Component-Specific Spacing Tokens

### Button Spacing Tokens

**Button Padding Horizontal** - `spacing-button-h`
```json
{
  "small": "12px",
  "medium": "16px", 
  "large": "24px"
}
```

**Button Padding Vertical** - `spacing-button-v`
```json
{
  "small": "6px",
  "medium": "8px",
  "large": "12px" 
}
```

**Button Spacing Between** - `spacing-button-gap`: `8px`

### Card Spacing Tokens

**Card Padding** - `spacing-card-padding`
```json
{
  "compact": "12px",
  "standard": "16px",
  "comfortable": "20px"
}
```

**Card Margin** - `spacing-card-margin`: `16px`
**Card Gap** - `spacing-card-gap`: `16px` (between multiple cards)

### Form Spacing Tokens

**Form Field Margin** - `spacing-form-field`: `12px`
**Form Section Gap** - `spacing-form-section`: `24px`
**Form Label Margin** - `spacing-form-label`: `4px`
**Input Padding** - `spacing-input-padding`: `12px 16px`

### Navigation Spacing Tokens

**Tab Bar Height** - `spacing-tab-bar-height`: `84px` (includes safe area)
**Tab Item Padding** - `spacing-tab-padding`: `8px 12px`
**Header Height** - `spacing-header-height`: `64px` (plus safe area)
**Header Content Padding** - `spacing-header-padding`: `0 16px`

## Responsive Spacing Tokens

### Adaptive Spacing

FlirtCraft uses adaptive spacing that scales based on screen size:

**Responsive Padding** - `spacing-responsive-padding`
```json
{
  "mobile": "16px",
  "tablet": "24px", 
  "desktop": "32px",
  "wide": "48px"
}
```

**Responsive Margin** - `spacing-responsive-margin`
```json
{
  "mobile": "12px",
  "tablet": "16px",
  "desktop": "20px", 
  "wide": "24px"
}
```

**Responsive Gap** - `spacing-responsive-gap`  
```json
{
  "mobile": "16px",
  "tablet": "20px",
  "desktop": "24px",
  "wide": "32px"
}
```

### Container Width Tokens

**Container Max Width** - `spacing-container-max`: `1200px`
**Container Padding** - `spacing-container-padding`
```json
{
  "mobile": "16px",
  "tablet": "24px", 
  "desktop": "32px"
}
```

## Touch Target Spacing Tokens

### Accessibility-Compliant Touch Targets

**Minimum Touch Target** - `spacing-touch-min`: `44px`
**Recommended Touch Target** - `spacing-touch-recommended`: `48px`
**Large Touch Target** - `spacing-touch-large`: `56px`

**Touch Target Spacing** - `spacing-touch-gap`: `8px`
- Minimum spacing between adjacent touch targets
- Prevents accidental taps on nearby elements

## Layout Pattern Tokens

### Common Layout Patterns

**List Item Spacing** - `spacing-list-item`
```json
{
  "compact": "8px",
  "standard": "12px", 
  "comfortable": "16px"
}
```

**Section Spacing** - `spacing-section`
```json
{
  "tight": "16px",
  "standard": "24px",
  "loose": "32px" 
}
```

**Content Block Spacing** - `spacing-content-block`
```json
{
  "paragraph": "12px",
  "section": "24px",
  "chapter": "32px"
}
```

## Platform-Specific Spacing Tokens

### iOS Spacing Adaptations

**iOS Safe Area Integration**
```json
{
  "spacing-ios-safe-top": "env(safe-area-inset-top)",
  "spacing-ios-safe-bottom": "env(safe-area-inset-bottom)",
  "spacing-ios-safe-left": "env(safe-area-inset-left)", 
  "spacing-ios-safe-right": "env(safe-area-inset-right)"
}
```

**iOS Navigation Spacing**
```json
{
  "spacing-ios-nav-bar": "44px",
  "spacing-ios-tab-bar": "49px",
  "spacing-ios-status-bar": "20px"
}
```

### Android Spacing Adaptations

**Material Design Alignment**
```json
{
  "spacing-android-keyline-1": "16dp",
  "spacing-android-keyline-2": "72dp", 
  "spacing-android-app-bar": "56dp",
  "spacing-android-fab": "16dp"
}
```

**Android Navigation Spacing**
```json
{
  "spacing-android-nav-bar": "56dp",
  "spacing-android-bottom-nav": "56dp",
  "spacing-android-status-bar": "24dp"
}
```

## Accessibility Spacing Considerations

### WCAG Compliance

**Focus Indicator Spacing** - `spacing-focus-offset`: `2px`
- Minimum offset for focus indicators
- Ensures visibility against various backgrounds

**Interactive Element Spacing** - `spacing-interactive-gap`: `8px`
- Minimum spacing between interactive elements
- Prevents accidental activation

### Motor Accessibility

**Large Touch Spacing** - `spacing-touch-accessible`: `56px`
- Enhanced spacing for users with motor difficulties
- Optional enhancement for accessibility modes

## Usage Guidelines

### When to Use Each Spacing Token

**Micro (xs - 2px):**
- Borders, dividers, very tight groupings
- Use sparingly, mainly for visual details

**Small (sm - 4px):**  
- Internal component spacing
- Tight relationships between elements

**Medium (md - 8px):**
- Default spacing choice for most situations
- Element-to-element relationships

**Large (lg - 12px):**
- Group-to-group spacing
- Card and component internal padding

**Extra Large (xl - 16px):**
- Major element separation
- Screen-level margins

**Larger tokens (2xl+):**
- Special layouts and large screen adaptations
- Use judiciously to avoid excessive whitespace on mobile

### Spacing Combination Principles

**Additive Spacing:**
- Combine smaller tokens rather than creating custom values
- Example: Use `spacing-md + spacing-sm` (12px) instead of custom 12px

**Consistent Application:**
- Use same token consistently for similar relationships
- Don't mix arbitrary spacing with token-based spacing

**Responsive Scaling:**
- Use responsive spacing tokens for adaptive layouts
- Maintain proportional relationships across breakpoints

## Implementation Examples

### React Native/NativeBase Usage

```jsx
import { VStack, HStack, Box } from 'native-base';

const ConversationCard = () => (
  <Box 
    p="spacing-lg"        // 12px padding
    m="spacing-md"        // 8px margin
    mb="spacing-xl"       // 16px bottom margin
  >
    <VStack space="spacing-md">  {/* 8px between elements */}
      <Text fontSize="h2">Coffee Shop</Text>
      <Text fontSize="body">Casual conversations...</Text>
      
      <HStack 
        space="spacing-sm"    // 4px between buttons
        mt="spacing-lg"       // 12px top margin
      >
        <Button flex={1}>Green</Button>
        <Button flex={1}>Yellow</Button>
        <Button flex={1}>Red</Button>
      </HStack>
    </VStack>
  </Box>
);
```

### CSS Custom Properties

```css
/* Generated spacing custom properties */
:root {
  --spacing-xs: 2px;
  --spacing-sm: 4px;
  --spacing-md: 8px;
  --spacing-lg: 12px;
  --spacing-xl: 16px;
  --spacing-2xl: 24px;
  --spacing-3xl: 32px;
  
  /* Grid system */
  --spacing-gutter-mobile: 16px;
  --spacing-gutter-tablet: 20px;
  --spacing-gutter-desktop: 24px;
  
  /* Safe areas */ 
  --spacing-safe-top: env(safe-area-inset-top);
  --spacing-safe-bottom: env(safe-area-inset-bottom);
}

/* Usage examples */
.card {
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-md);
}

.button-group {
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

.screen-content {
  padding: var(--spacing-xl);
  padding-top: calc(var(--spacing-xl) + var(--spacing-safe-top));
}
```

### NativeWind Classes

```jsx
// Using spacing tokens through NativeWind utility classes
<View className="p-lg m-md mb-xl">
  <View className="space-y-md">
    <Text className="text-h2">Coffee Shop</Text>
    <Text className="text-body">Casual conversations...</Text>
    
    <View className="flex-row space-x-sm mt-lg">
      <Button className="flex-1">Green</Button>
      <Button className="flex-1">Yellow</Button> 
      <Button className="flex-1">Red</Button>
    </View>
  </View>
</View>
```

## Token Export Format

### JSON Export Structure

```json
{
  "spacing": {
    "base": "4px",
    "scale": {
      "xs": "2px",
      "sm": "4px", 
      "md": "8px",
      "lg": "12px",
      "xl": "16px",
      "2xl": "24px",
      "3xl": "32px",
      "4xl": "48px",
      "5xl": "64px"
    },
    "grid": {
      "mobile": {
        "columns": 4,
        "gutters": "16px",
        "margins": "16px"
      },
      "tablet": {
        "columns": 8,
        "gutters": "20px", 
        "margins": "24px"
      },
      "desktop": {
        "columns": 12,
        "gutters": "24px",
        "margins": "32px"
      }
    },
    "breakpoints": {
      "mobile": { "min": "320px", "max": "767px" },
      "tablet": { "min": "768px", "max": "1023px" },
      "desktop": { "min": "1024px", "max": "1439px" },
      "wide": { "min": "1440px" }
    },
    "components": {
      "button": {
        "paddingHorizontal": {
          "small": "12px",
          "medium": "16px",
          "large": "24px"
        }
      },
      "card": {
        "padding": "16px",
        "margin": "16px"
      }
    },
    "accessibility": {
      "touchTarget": {
        "minimum": "44px",
        "recommended": "48px"
      },
      "focusOffset": "2px"
    }
  }
}
```

---

## Related Documentation

- [Typography Tokens](./typography.md) - Text spacing and line heights
- [Color Tokens](./colors.md) - Border and background colors for spacing
- [Style Guide](../style-guide.md) - Spacing usage in design system
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Accessible spacing requirements

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*