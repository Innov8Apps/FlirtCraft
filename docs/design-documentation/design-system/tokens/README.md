# Design Tokens

---
title: FlirtCraft Design Tokens Overview
description: Centralized design values for colors, typography, spacing, and animations
last-updated: 2025-08-23
version: 1.0.0
status: approved
---

## Overview

Design tokens are the foundational design decisions of FlirtCraft, stored as platform-agnostic values that can be transformed into any format needed by development teams. They ensure consistency across all platforms while enabling systematic design updates.

## Token Categories

### [Colors](./colors.md)
Comprehensive color palette including semantic colors, difficulty indicators, and accessibility-compliant color combinations.

**Key Features:**
- Primary and secondary brand colors
- Semantic colors (success, warning, error, info)
- Difficulty color system (Green/Yellow/Red)
- Neutral palette with 9 steps
- Light and dark mode values (Phase 2 ready)
- WCAG AA/AAA compliant contrast ratios

### [Typography](./typography.md)
Complete type system with responsive scaling and platform-specific adaptations.

**Key Features:**
- Font family definitions and fallbacks
- Type scale from caption to H1
- Font weight specifications
- Line height and letter spacing values
- Responsive scaling for mobile, tablet, desktop
- Platform-specific optimizations

### [Spacing](./spacing.md)
Mathematical spacing system based on 4px grid for consistent layouts.

**Key Features:**
- Base unit system (4px)
- Spacing scale from xs (2px) to 5xl (64px)
- Grid system specifications
- Breakpoint definitions
- Safe area and margin standards
- Component-specific spacing rules

### [Animations](./animations.md)
Motion design system with timing functions, durations, and easing curves.

**Key Features:**
- Timing function library
- Duration scale for different interaction types
- Animation patterns for common UI elements
- Performance-optimized animation properties
- Reduced motion alternatives
- Platform-specific motion guidelines

## Token Organization

### Naming Convention

FlirtCraft uses a systematic naming convention for all design tokens:

```
[category]-[concept]-[variant]-[state]
```

**Examples:**
- `color-primary-500` - Primary color at 500 weight
- `spacing-lg` - Large spacing value
- `typography-h1-mobile` - H1 typography for mobile
- `animation-duration-short` - Short duration timing

### Token Hierarchy

**Global Tokens** - Core values that rarely change:
```json
{
  "color-blue-500": "#3B82F6",
  "spacing-base": "4px",
  "font-family-primary": "Inter"
}
```

**Alias Tokens** - Semantic tokens that reference global tokens:
```json
{
  "color-primary": "{color-blue-500}",
  "color-success": "{color-green-500}",
  "spacing-md": "{spacing-base} * 2"
}
```

**Component Tokens** - Component-specific overrides:
```json
{
  "button-primary-background": "{color-primary}",
  "button-padding-horizontal": "{spacing-lg}",
  "card-border-radius": "{border-radius-lg}"
}
```

## Platform Outputs

### JSON Export Format

Design tokens are exported as structured JSON for consumption by development tools:

```json
{
  "colors": {
    "primary": {
      "50": "#FFF7ED",
      "100": "#FFEDD5",
      "500": "#F97316",
      "900": "#312E81"
    }
  },
  "spacing": {
    "xs": "2px",
    "sm": "4px",
    "md": "8px"
  },
  "typography": {
    "h1": {
      "fontSize": "28px",
      "lineHeight": "36px",
      "fontWeight": "700"
    }
  }
}
```

### Style Dictionary Configuration

FlirtCraft uses [Style Dictionary](https://amzn.github.io/style-dictionary/) to transform design tokens into platform-specific formats:

**React Native/NativeBase:**
```javascript
// Generated theme object
const theme = {
  colors: {
    primary: {
      500: '#F97316',
      600: '#C2410C',
    }
  },
  fontSizes: {
    h1: 28,
    body: 16,
  }
};
```

**CSS Custom Properties:**
```css
:root {
  --color-primary-500: #F97316;
  --color-primary-600: #C2410C;
  --font-size-h1: 28px;
  --font-size-body: 16px;
}
```

**Tailwind CSS Config:**
```javascript
module.exports = {
  theme: {
    colors: {
      primary: {
        500: '#F97316',
        600: '#C2410C',
      }
    }
  }
};
```

## Token Usage Guidelines

### When to Create New Tokens

**Create tokens for:**
- Values used in 3+ places
- Values that might change systematically
- Platform-specific adaptations
- Semantic meaning beyond literal values

**Don't create tokens for:**
- One-off, component-specific values
- Calculated values that derive from existing tokens
- Platform capabilities (like hardware-specific features)

### Token Maintenance

**Version Control:**
- All token changes are versioned
- Breaking changes require major version increment
- Backward compatibility maintained where possible

**Documentation Requirements:**
- All tokens include usage descriptions
- Examples provided for complex token usage
- Migration guides for token changes

**Review Process:**
- Design team reviews all token additions
- Development team reviews technical implications
- Accessibility team reviews color/contrast tokens

## Integration with Development

### NativeBase Integration

FlirtCraft's design tokens integrate directly with NativeBase theming:

```jsx
// Custom theme extending default NativeBase tokens
const customTheme = extendTheme({
  colors: {
    primary: flirtCraftTokens.colors.primary,
    secondary: flirtCraftTokens.colors.secondary,
  },
  fontSizes: flirtCraftTokens.typography.sizes,
  space: flirtCraftTokens.spacing,
});

// Usage in components
<Button colorScheme="primary" size="lg">
  Start Conversation
</Button>
```

### NativeWind Integration

Design tokens also power NativeWind utility classes:

```jsx
// Using design token values through NativeWind
<View className="bg-primary-500 p-lg rounded-xl">
  <Text className="text-white text-h3 font-semibold">
    Welcome to FlirtCraft
  </Text>
</View>
```

## Accessibility Considerations

### Color Contrast Validation

All color tokens include contrast validation:
- **AA Compliance**: Minimum 4.5:1 for normal text, 3:1 for large text
- **AAA Compliance**: 7:1 ratios for critical interface elements
- **Color Blindness**: Tested with deuteranopia, protanopia, and tritanopia

### Motion and Animation

Animation tokens respect user preferences:
- **Reduced Motion**: Alternative values for users who prefer reduced motion
- **High Performance**: Optimized values for smooth 60fps animations
- **Platform Standards**: Timing that feels natural on each platform

### Typography Scaling

Typography tokens support accessibility requirements:
- **Dynamic Type**: iOS Dynamic Type compatibility
- **Large Text**: Android large text preference support
- **Scaling Ratios**: Proportional scaling up to 200% text size

## Future Considerations

### Dark Mode Support (Phase 2)

Design tokens are structured to support dark mode:

```json
{
  "colors": {
    "background": {
      "light": "#FFFFFF",
      "dark": "#1F2937"
    },
    "text": {
      "light": "#1F2937", 
      "dark": "#F9FAFB"
    }
  }
}
```

### Theming System (Phase 3)

Token structure supports user customization:
- Premium users can select color themes
- Accessibility themes for specific needs
- Cultural/regional color preferences

### Multi-Brand Support

Token architecture enables multiple brand variations:
- White-label versions for partners
- Regional brand adaptations
- Co-branded experiences

---

## Related Documentation

- [Complete Style Guide](../style-guide.md) - How tokens compose into design system
- [Component Library](../components/) - Token usage in components
- [Platform Adaptations](../platform-adaptations/) - Platform-specific token usage
- [Implementation Guide](../../implementation-summary.md) - Developer integration

## Token Files

- **[colors.md](./colors.md)** - Complete color system and semantic colors
- **[typography.md](./typography.md)** - Type scale and font specifications
- **[spacing.md](./spacing.md)** - Layout spacing and grid system
- **[animations.md](./animations.md)** - Motion design and timing system

## Exportable Assets

- **[design-tokens.json](../../assets/design-tokens.json)** - Complete token export
- **[style-dictionary/](../../assets/style-dictionary/)** - Build configuration
- **Platform Outputs** - Generated files for React Native, CSS, and Tailwind

---

*Last Updated: 2025-08-23*
*Status: Complete foundation ready for platform implementation*