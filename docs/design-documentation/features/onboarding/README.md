# Onboarding Experience Design

---
title: FlirtCraft Onboarding Experience
description: First-time user setup and preference collection design specifications
feature: onboarding
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./premium-redesign.md
  - ./implementation-guide.md
  - ./user-journey.md
  - ./screen-states.md
  - ../../design-system/style-guide.md
  - ../../design-system/tokens/premium-animations.md
  - ../../design-system/components/premium-buttons.md
dependencies:
  - User Profile creation system
  - Main app navigation system
  - React Native Reanimated 3.6+
  - PremiumButton component system
  - ParticleSystem celebration effects
status: approved
---

## Overview

The premium onboarding experience represents FlirtCraft's commitment to FANG-level design excellence, combining sophisticated animations with confidence-building psychology. This redesigned experience eliminates all teal references in favor of a pure orange system that creates warmth, energy, and optimism while reducing user anxiety and building genuine confidence in the app's value proposition.

## Design Goals

### Primary Objectives (Premium Redesign)
- **Build Confidence Through Design**: Every visual element, animation, and micro-interaction reinforces user capability and progress
- **Pure Orange Psychology**: Completely eliminated teal (#14B8A6) for consistent warm, energetic, and optimistic branding using orange gradients and complements
- **FANG-Level Polish**: React Native Reanimated 3 sophisticated animations, PremiumButton components, ParticleSystem celebration effects, and glass morphism details
- **Reduce Initial Anxiety**: Confidence-building design language with gentle animations and supportive micro-copy
- **Demonstrate Value Quickly**: Show concrete benefits within first 60 seconds through premium presentation and celebration effects
- **Establish Trust**: Premium design cues with subtle particle effects and smooth transitions create professional confidence

### Success Metrics (Premium Targets)
- **Completion Rate**: >90% of users complete full onboarding flow (increased from 85% due to premium UX)
- **Time to Value**: Users experience first "wow moment" within 60 seconds (improved from 90 seconds)
- **Retention**: >85% of users who complete onboarding return within 24 hours (increased from 75%)
- **Confidence**: Pre/post onboarding confidence survey shows 30%+ improvement (increased from 20%)
- **User Delight**: Post-onboarding experience rating >4.7/5 (new premium metric)
- **Animation Performance**: Maintain 60fps during all interactions on supported devices

## User Journey Summary

### 5-Screen Streamlined Flow
1. **Welcome & Value Proposition** (30 seconds) - Establish trust and excitement (with a log in button at the bottom)
2. **Age Verification** (15 seconds) - Legal compliance with friendly design
3. **Registration/Sign In** (45 seconds) - Secure account creation with Supabase Auth
4. **Preference Setup** (60 seconds) - Personalize experience without overwhelm
5. **Skill Goal Selection** (45 seconds) - Align app to user's specific needs

Also do the auth log in screen

### Total Experience Time
**Target**: 3-4 minutes for thoughtful completion
**Minimum**: 2 minutes for users who move quickly
**Maximum**: 5 minutes for users who explore all options

## Persona-Specific Adaptations

### Anxious Alex (Needs: Reassurance & Detailed Preparation)
- **Extended context explanations** for each step with "Why we ask this" details
- **Privacy reassurances** prominently displayed throughout flow
- **Optional advanced settings** for fine-tuning preferences
- **Progress tracking** to show completion and reduce anxiety about commitment

### Comeback Catherine (Needs: Modern Relevance & Confidence Rebuild)
- **Modern dating context references** in copy and examples
- **"Getting back out there" messaging** that acknowledges her situation
- **Intermediate difficulty options** highlighted as good starting points
- **Progress framing** as "skill refreshing" rather than learning from scratch

### Confident Carlos (Needs: Efficiency & Advanced Features)  
- **Quick setup options** with "Express Setup" path available
- **Advanced goal selection** including specific skill refinement areas
- **Challenge-focused messaging** about optimization and improvement
- **Competitive elements** hinted at without fully exposing gamification system

### Shy Sarah (Needs: Safe Environment & Gentle Progression)
- **Extensive reassurance** about safe practice environment
- **Step-by-step guidance** with clear next actions at each stage
- **Beginner-friendly language** avoiding intimidating dating terminology
- **Campus-relevant examples** and scenarios in explanations

## Key Features

### Progressive Disclosure
Information revealed gradually to prevent cognitive overload:
- **Screen 1**: Core value proposition only (with a button also to log in at the bottom)
- **Screen 2**: Simple age verification  
- **Screen 3**: Secure account creation with email/password
- **Screen 4**: Basic preferences (gender, age range)
- **Screen 5**: Skill goals with explanations
Feature demonstration happens naturally in main app during first practice session

### Personalization Engine
Setup choices immediately customize experience:
- **AI personality matching** based on user's anxiety level and goals
- **Scenario recommendations** aligned with user demographics and preferences
- **Difficulty calibration** starting at appropriate challenge level
- **Content filtering** ensuring age-appropriate and preference-aligned practice

### Value Demonstration
After onboarding, users immediately experience core app benefits:
- **Direct access to practice sessions** through intuitive navigation
- **Real-time AI conversation** with context-aware responses in first practice
- **Immediate feedback** showing how improvement suggestions work
- **Progress tracking** starting from their very first conversation

## Technical Requirements

### Data Collection
**Required Information:**
- User age (18+ verification)
- Email address (for account creation and communication)
- Secure password (minimum 8 chars, 1 uppercase, 1 number, 1 special char)
- Target gender preference (male/female/randomized)
- Age range preference (±5 years default)
- Primary skill goal (conversation starters/flow maintenance/storytelling)

**Optional Information:**
- Specific anxiety areas (approach, rejection, escalation)
- Experience level (complete beginner/some experience/returning to dating)
- Preferred conversation style (direct/playful/thoughtful)

### Privacy Implementation
- **Minimal data collection** during onboarding
- **Clear privacy explanations** at each data collection point
- **Temporary local storage** for preferences until full onboarding completion
- **Supabase Auth security** with encrypted password storage
- **Delayed account creation** - database instance only created after complete onboarding
- **Email verification** required before app access
- **Opt-in tracking** for analytics and improvement suggestions

### Performance Requirements
- **Screen load times**: <500ms between onboarding screens
- **AI service connectivity**: <2 seconds for initial setup validation
- **Smooth animations**: 60fps transitions between screens
- **Offline capability**: Onboarding preference collection works without internet

## Design System Integration

### Components Used
- [PremiumButton](../../design-system/components/premium-buttons.md#premium-button) - "Start Building Confidence", "Confirm Age", "Continue Setup" with celebration effects
- [ParticleSystem](../../design-system/components/premium-buttons.md#particle-system) - Success celebrations and confidence-building feedback
- [Form Input Fields](../../design-system/components/forms.md#premium-text-input) - Enhanced inputs with orange accent colors and smooth animations
- [Form Select Components](../../design-system/components/forms.md#premium-select-dropdown) - Preference selection with orange highlights
- [Radio Button Groups](../../design-system/components/forms.md#premium-radio-group) - Skill goal selection with animated selections
- [Progress Indicators](../../design-system/components/navigation.md#premium-progress) - Step progression with orange gradient fills
- [Glass Morphism Cards](../../design-system/components/cards.md#premium-glass-card) - Confidence-building benefit displays with subtle glass effects

### Design Tokens (Premium Orange System)
- [Primary Orange](../../design-system/tokens/colors.md#primary-palette) - Pure orange (#F97316) for main CTAs, progress indicators, and focus states
- [Orange Gradients](../../design-system/tokens/colors.md#orange-gradients) - Orange-to-orange variations replacing all teal gradients
- [Warm Complements](../../design-system/tokens/colors.md#warm-palette) - Peach (#FDBA8C) and amber accents replacing teal usage
- [Typography Scale](../../design-system/tokens/typography.md#premium-typography) - Enhanced hierarchy with confidence-building messaging
- [Premium Spacing](../../design-system/tokens/spacing.md#premium-spacing) - 4px base unit with enhanced breathing room
- [Reanimated 3 Timings](../../design-system/tokens/animations.md#reanimated-presets) - Confidence-building animation curves and celebration effects

### Platform Adaptations
- [iOS Guidelines](../../design-system/platform-adaptations/ios.md) - Safe area handling and native navigation
- [Android Guidelines](../../design-system/platform-adaptations/android.md) - Material design button behaviors
- [Web Guidelines](../../design-system/platform-adaptations/web.md) - Progressive enhancement and keyboard navigation

## Quality Assurance

### Usability Testing
- **A/B testing** of messaging and flow order
- **User interviews** with each persona type during beta
- **Completion funnel analysis** identifying drop-off points
- **Post-onboarding surveys** measuring confidence and value perception

### Technical Validation
- **Cross-platform consistency** between iOS and Android
- **Accessibility compliance** verified with screen readers
- **Performance monitoring** of load times and animations
- **Error handling** for network issues and invalid inputs

---

## Development & Testing

### Placeholder Main App
After onboarding completion in development builds, users are directed to a placeholder main app interface for testing purposes. This temporary implementation provides:

#### 4-Tab Structure
- **Home**: Welcome screen with development notice
- **Chat**: Placeholder for conversation feature
- **Scenarios**: Placeholder for scenarios feature
- **Profile**: Development tools including reset functionality

#### Reset Functionality
The Profile tab includes a "Reset App & Clear Data" button that:
1. Signs out from Supabase Auth
2. Clears all AsyncStorage data
3. Resets onboarding state
4. Returns to onboarding start

This allows developers to test the registration flow multiple times without needing to create new accounts or manually clear data.

#### Testing Workflow
1. Complete onboarding including registration
2. Land on placeholder interface
3. Navigate to Profile tab
4. Use reset button to test again
5. Repeat as needed for development

**Important**: The placeholder interface and reset functionality are only available in development builds (`__DEV__` flag). In production, users will be directed to the actual main app implementation.

### Integration Notes
- The `navigateToMainApp()` function handles the conditional navigation
- Placeholder component is in `components/MainAppPlaceholder.tsx`
- Reset functionality uses `useOnboardingStore.resetOnboarding()`
- All placeholder screens use FlirtCraft design system and colors

---

*The onboarding experience sets the tone for the entire FlirtCraft journey. Every design decision prioritizes user comfort and confidence-building while efficiently demonstrating the app's value proposition.*