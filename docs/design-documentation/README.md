# FlirtCraft Design Documentation

## Overview
This directory contains comprehensive design specifications for FlirtCraft, an AI-powered dating conversation training app. The design system prioritizes psychological safety, accessibility, and user confidence building through thoughtful visual design and interaction patterns.

## Target Platform
- **Primary**: Mobile-first design (iOS/Android)
- **Framework**: React Native with Expo
- **UI Library**: NativeBase foundation with NativeWind styling
- **Key Audiences**: Adults 18-35 experiencing social anxiety in romantic situations

## Design Philosophy
FlirtCraft's design embodies supportive confidence-building through:
- **Warm, encouraging visual language** that reduces anxiety
- **Progressive complexity** that builds user comfort gradually  
- **Clear information hierarchy** that prevents cognitive overload
- **Accessible design** meeting WCAG 2.1 AA standards
- **Gamification elements** that motivate without pressure

## Documentation Structure

### Core Design System
- [Complete Style Guide](./design-system/style-guide.md) - Colors, typography, spacing, components
- [Design Tokens](./design-system/tokens/) - Exportable values for development  
- [Component Library](./design-system/components/) - Reusable UI component specifications
- [Platform Adaptations](./design-system/platform-adaptations/) - iOS, Android, and web considerations

#### Design System Components
- [Buttons](./design-system/components/buttons.md) - Primary, secondary, and ghost button specifications
- [Forms](./design-system/components/forms.md) - Input fields, selectors, checkboxes for preferences  
- [Navigation](./design-system/components/navigation.md) - Tab bars, headers, back buttons
- [Cards](./design-system/components/cards.md) - Scenario cards, context cards, achievement cards
- [Modals](./design-system/components/modals.md) - Difficulty selector, alerts, premium upsell
- [Chat Bubbles](./design-system/components/chat-bubbles.md) - User/AI messages, typing indicators
- [Context Cards](./design-system/components/context-cards.md) - Appearance, environment, body language displays
- [Gamification](./design-system/components/gamification.md) - XP bars, streaks, badges, achievements

#### Design Tokens
- [Colors](./design-system/tokens/colors.md) - Complete color palette and semantic colors
- [Typography](./design-system/tokens/typography.md) - Font scales, line heights, weights
- [Spacing](./design-system/tokens/spacing.md) - 4px base unit system and responsive spacing
- [Animations](./design-system/tokens/animations.md) - Timing, easing, transitions

#### Platform Adaptations  
- [iOS Guidelines](./design-system/platform-adaptations/ios.md) - iOS Human Interface Guidelines compliance
- [Android Guidelines](./design-system/platform-adaptations/android.md) - Material Design adaptations

### Feature Specifications

#### Core Navigation Structure (4 Tabs)
FlirtCraft uses a 4-tab navigation system providing clear separation of functionality:

**1. [Home Tab](./user-journey-overall.md#home-tab)** - Unified Dashboard & Progress Hub
- Dashboard with daily stats, streaks, XP tracking
- Quick action access to practice sessions
- Integrated progress visualization and achievement previews
- Comprehensive analytics in expandable sections

**2. [Chat Tab](./user-journey-overall.md#chat-tab)** - Custom Conversation Practice
- **Flow**: Difficulty Selection → Context Creation (Blank) → Chat Interface
- User creates fully custom scenarios from scratch
- Complete control over partner, environment, and situation setup
- Ideal for experienced users wanting tailored practice

**3. [Scenarios Tab](./user-journey-overall.md#scenarios-tab)** - Guided Practice Templates  
- **Flow**: Browse Scenarios → Select Template → Context Creation (Pre-filled) → Chat Interface
- Curated practice situations with predefined templates
- Templates can still be customized but provide starting structure
- Perfect for users wanting guided practice in specific situations

**4. [Profile Tab](./user-journey-overall.md#profile-tab)** - Unified Settings Center
- Personal information and dating preferences
- Practice settings and notification preferences  
- Account management and premium features
- App preferences, privacy settings, and support

#### Detailed Feature Documentation
- [Onboarding Experience](./features/onboarding/) - First-time user setup and preference collection
- [Pre-Conversation Context](./features/pre-conversation-context/) - AI-generated context display (shared by both Chat and Scenarios)
- [Conversation Interface](./features/conversation/) - Real-time chat with AI partner (identical for both flows)
- [Post-Conversation Feedback](./features/feedback/) - Scoring and improvement tips
- [User Profile](./features/profile/) - Settings and progress tracking
- [Gamification System](./features/gamification/) - XP, achievements, and progress tracking (Phase 2)

### Accessibility & Standards
- [Accessibility Strategy](./accessibility/) - Complete accessibility approach and guidelines
- [Accessibility Guidelines](./accessibility/guidelines.md) - WCAG compliance and inclusive design
- [Testing Procedures](./accessibility/testing.md) - Quality assurance and validation  
- [Implementation Standards](./accessibility/compliance.md) - Developer requirements

## Key User Personas
Our design serves four primary personas:
- **Anxious Alex** (24): Needs gentle confidence building and detailed feedback
- **Comeback Catherine** (32): Wants realistic practice after time away from dating
- **Confident Carlos** (28): Seeks skill optimization and challenging scenarios
- **Shy Sarah** (21): Requires extensive context and supportive guidance

## Success Metrics
Design decisions support business goals:
- **70%+ weekly retention** through engaging, supportive experience
- **60%+ confidence improvement** via clear progress visualization
- **15%+ premium conversion** through value-demonstrating design
- **4.5+ app store rating** via polished, accessible interface

## Implementation Assets

### Exportable Design Tokens
- [Design Tokens JSON](./assets/design-tokens.json) - Complete token export for development
- [Style Dictionary Config](./assets/style-dictionary/) - Build configuration for platform outputs
- Platform-specific outputs for React Native, CSS, and Tailwind CSS

### Complete User Journey
- [Overall User Journey](./user-journey-overall.md) - Comprehensive 945-line user experience documentation

### Technical Integration
- [Implementation Summary](./implementation-summary.md) - Developer handoff and technical requirements

## Implementation Notes
- Built with React Native/Expo for cross-platform consistency
- NativeBase provides foundation components with custom theming
- NativeWind enables Tailwind-like styling for rapid development
- React Native Reanimated powers smooth, performant animations
- Design tokens exported as JSON for developer consumption

## Getting Started
1. Review the [Complete Style Guide](./design-system/style-guide.md) for design system foundation
2. Examine [User Journey](./user-journey-overall.md) for complete app experience flow
3. Reference [Component Library](./design-system/components/) for implementation details
4. Follow [Accessibility Guidelines](./accessibility/) for inclusive design requirements
5. Use [Design Tokens](./assets/design-tokens.json) for consistent implementation
6. Check [Platform Adaptations](./design-system/platform-adaptations/) for iOS/Android specifics

---

*Last updated: 2025-08-24*
*Version: 2.0 - Updated for 4-Tab Navigation Structure*
*Status: Complete foundation ready for development*