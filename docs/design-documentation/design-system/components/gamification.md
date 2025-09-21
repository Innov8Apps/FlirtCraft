# Gamification Components

---
title: FlirtCraft Gamification Components
description: XP bars, streaks, badges, achievements, and progress indicators for user motivation
feature: gamification, progress-tracking
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ./cards.md
dependencies:
  - React Native Reanimated for smooth animations
  - React Native SVG for custom progress indicators
  - NativeBase components
status: approved
---

## Overview

Gamification components in FlirtCraft motivate users through positive reinforcement and clear progress visualization. The design emphasizes encouragement over competition, building confidence through achievement recognition and skill development tracking.

## Gamification System Architecture

### Component Types
1. **XP Progress Bars** - Experience point tracking and level progression
2. **Streak Indicators** - Daily practice consistency tracking  
3. **Achievement Badges** - Milestone recognition and unlocked accomplishments
4. **Skill Progress Meters** - Individual skill area development
5. **Level Indicators** - User progression and status display

## Component Specifications

### XP Progress Bar

#### Purpose
Visual representation of experience points earned and progress toward next level.

#### Visual Specifications

**Container:**
- **Width**: Full-width with 16px margins on mobile, fixed 400px on desktop
- **Height**: `8px` progress track + `20px` labels = `28px` total
- **Background**: Transparent container
- **Margin**: 12px vertical spacing

**Progress Track:**
- **Height**: `8px` - prominent but not overwhelming
- **Border Radius**: `4px` - fully rounded ends
- **Background**: `#E5E7EB` (Neutral-200) - subtle unfilled appearance
- **Shadow**: Inset `0 1px 2px rgba(0, 0, 0, 0.05)` - slight depth

**Progress Fill:**
- **Background**: Linear gradient `#F97316` to `#8B5CF6` (Primary to Purple)
- **Border Radius**: `4px` - matches track
- **Animation**: Smooth width transition (500ms ease-out)
- **Glow Effect**: `0 0 8px rgba(99, 102, 241, 0.3)` during animation

**Label System:**
- **Current XP**: Left-aligned, Body Small (14px/20px, 500 weight)
- **Level Info**: Right-aligned, Body Small (14px/20px, 500 weight)
- **Color**: `#374151` (Neutral-700)
- **Spacing**: 4px above progress track

#### XP Bar Variants

**Standard XP Bar:**
```
Level 3 • 350 XP                    650 XP to Level 4
[████████████████████░░░░░░░░░░░░░░░░░░░░]
```

**Level Up Animation:**
- **Sequence**: Fill completes → Brief glow → Level number updates → Celebration
- **Colors**: Progress fill briefly becomes gold gradient
- **Duration**: 1.5 seconds total animation
- **Sound**: Optional level-up sound effect

**Mini XP Bar (Dashboard):**
- **Height**: `6px` track for compact display
- **Labels**: Simplified to just "Level 3" and "54% to Level 4"
- **Usage**: Dashboard widgets and summary views

#### NativeBase Implementation
```jsx
const XPProgressBar = ({ currentXP, currentLevel, xpToNextLevel }) => {
  const progressWidth = useSharedValue(0);
  const progress = currentXP / xpToNextLevel;

  useEffect(() => {
    progressWidth.value = withSpring(progress, {
      tension: 100,
      friction: 8,
    });
  }, [progress]);

  const animatedStyle = useAnimatedStyle(() => ({
    width: `${progressWidth.value * 100}%`,
  }));

  return (
    <VStack space={1}>
      <HStack justifyContent="space-between">
        <Text fontSize="sm" fontWeight="medium" color="gray.700">
          Level {currentLevel} • {currentXP} XP
        </Text>
        <Text fontSize="sm" fontWeight="medium" color="gray.700">
          {xpToNextLevel - currentXP} XP to Level {currentLevel + 1}
        </Text>
      </HStack>
      
      <Box height="8px" bg="gray.200" borderRadius="4">
        <Animated.View
          style={[
            {
              height: '100%',
              borderRadius: 4,
              backgroundColor: '#F97316',
            },
            animatedStyle,
          ]}
        />
      </Box>
    </VStack>
  );
};
```

### Streak Counter

#### Purpose
Display and celebrate daily practice consistency with fire emoji and numerical tracking.

#### Visual Specifications

**Container:**
- **Style**: Horizontal layout with icon and text
- **Background**: Optional pill background for emphasis
- **Alignment**: Can be left, center, or right-aligned based on context

**Fire Icon:**
- **Emoji**: 🔥 (fire emoji) or custom fire icon
- **Size**: `20px` - prominent but proportional
- **Color**: `#F59E0B` (Amber) if using custom icon
- **Animation**: Subtle flicker animation when streak is active

**Streak Number:**
- **Typography**: Body Medium (16px/22px, 500 weight)
- **Color**: `#F59E0B` (Amber) - matches fire theme
- **Format**: Just the number (e.g., "7") or "7-day streak"

**Background Variants:**

*Minimal (Default):*
- **Background**: Transparent
- **Layout**: Icon + number horizontally
- **Usage**: Dashboard summary, header areas

*Emphasized:*
- **Background**: `#FFFBEB` (Amber-50) pill shape
- **Padding**: 8px horizontal, 4px vertical
- **Border**: 1px solid `#FDE68A` (Amber-200)
- **Border Radius**: 16px
- **Usage**: Achievement celebrations, milestone displays

#### Streak States

**Active Streak (1+ days):**
```
🔥 7
```

**No Streak:**
```
🔥 Start your streak today!
```

**Milestone Streak (7, 14, 30, 100 days):**
- **Special Animation**: Burst effect with sparkles
- **Color Enhancement**: Golden gradient instead of standard amber
- **Notification**: Achievement modal with celebration

**Streak at Risk:**
- **Context**: Near midnight without completing daily goal
- **Visual**: Pulsing animation on fire icon
- **Color**: Slight red tint to indicate urgency
- **Message**: "Complete 1 more conversation to keep your 5-day streak!"

### Achievement Badge

#### Purpose
Celebrate specific accomplishments with collectible badges that recognize different aspects of progress.

#### Visual Specifications

**Badge Container:**
- **Size**: `64px` diameter (standard), `80px` (featured), `48px` (compact)
- **Shape**: Circle with optional decorative elements
- **Shadow**: `0 2px 8px rgba(0, 0, 0, 0.15)` - prominent elevation
- **Border**: 2px solid based on achievement tier

**Achievement Tiers:**

*Bronze Tier:*
- **Gradient**: `#D97706` to `#F59E0B` (Orange to Amber)
- **Border**: `#D97706` (Orange)
- **Icon Color**: White with subtle drop shadow
- **Usage**: Basic milestones, participation achievements

*Silver Tier:*
- **Gradient**: `#6B7280` to `#9CA3AF` (Neutral grays)
- **Border**: `#6B7280` (Neutral)
- **Icon Color**: White with drop shadow
- **Usage**: Skill improvements, consistency achievements

*Gold Tier:*
- **Gradient**: `#D97706` to `#FBBF24` (Orange to Yellow)
- **Border**: `#D97706` (Orange)
- **Icon Color**: White with strong contrast
- **Usage**: Exceptional performance, rare accomplishments

*Diamond Tier (Premium):*
- **Gradient**: `#F97316` to `#EA580C` (Primary to Deep Orange)
- **Border**: `#F97316` (Primary)
- **Icon Color**: White with premium styling
- **Usage**: Premium achievements, community recognition

#### Badge Icon System

**Icon Design:**
- **Size**: 50% of badge diameter (32px for standard 64px badge)
- **Style**: Simple, recognizable symbols
- **Color**: White with 1px drop shadow for definition
- **Background**: Semi-transparent white circle (optional)

**Common Achievement Icons:**
- **First Steps**: Footprint or flag
- **Conversation Starter**: Chat bubble
- **Smooth Talker**: Star or sparkle
- **Daily Dedication**: Calendar
- **Skill Master**: Trophy or target
- **Helper**: Heart or helping hand
- **Explorer**: Compass or map
- **Perfectionist**: Diamond or crown

#### Achievement Examples

**First Steps (Bronze):**
- **Icon**: 👣 footprint
- **Title**: "First Steps"
- **Description**: "Completed your first practice conversation"
- **Unlock**: Onboarding completion

**Conversation Starter (Silver):**
- **Icon**: 💬 chat bubble
- **Title**: "Conversation Starter"
- **Description**: "Started 10 conversations confidently"
- **Progress**: "7/10 conversations"

**Smooth Talker (Gold):**
- **Icon**: ⭐ star
- **Title**: "Smooth Talker"
- **Description**: "Achieved 90+ conversation score"
- **Rarity**: "Only 5% of users unlock this!"

**Daily Dedication (Bronze):**
- **Icon**: 📅 calendar
- **Title**: "Daily Dedication"
- **Description**: "Maintained a 7-day practice streak"
- **Progress**: "Day 5 of 7"

### Skill Progress Meter

#### Purpose
Track development in specific conversation skill areas with individual progress indicators.

#### Visual Specifications

**Container:**
- **Layout**: Horizontal bar with skill name and level
- **Height**: `40px` total (20px label + 16px progress + 4px spacing)
- **Width**: Full-width with 16px margins
- **Spacing**: 8px between different skill meters

**Skill Label:**
- **Typography**: Body Small (14px/20px, 500 weight)
- **Color**: `#374151` (Neutral-700)
- **Content**: Skill name + level (e.g., "Conversation Flow • Level 2")

**Progress Track:**
- **Height**: `6px` - thinner than XP bar for differentiation
- **Background**: `#F3F4F6` (Neutral-100)
- **Border Radius**: `3px` - proportional to height

**Progress Fill:**
- **Colors**: Skill-specific colors for differentiation
- **Animation**: Smooth progress advancement (400ms ease-out)
- **Border Radius**: `3px` - matches track

#### Skill Categories & Colors

**Conversation Starters:**
- **Color**: `#10B981` (Success/Green)
- **Description**: Opening conversations naturally and confidently

**Flow Maintenance:**
- **Color**: `#3B82F6` (Info/Blue) 
- **Description**: Keeping conversations engaging and reciprocal

**Confidence Building:**
- **Color**: `#8B5CF6` (Purple)
- **Description**: Expressing yourself with authenticity and charm

**Social Cue Reading:**
- **Color**: `#F59E0B` (Warning/Amber)
- **Description**: Understanding non-verbal communication

**Storytelling:**
- **Color**: `#E65100` (Secondary/Deep Orange)
- **Description**: Sharing engaging personal experiences

#### Skill Level System

**Beginner (Level 1-2):**
- **Progress**: 0-20% filled
- **Color**: Full intensity of skill color
- **Label**: "Beginner • Level 1"

**Intermediate (Level 3-5):**
- **Progress**: 21-60% filled
- **Color**: Slightly darker shade of skill color
- **Label**: "Intermediate • Level 4"

**Advanced (Level 6-8):**
- **Progress**: 61-85% filled
- **Color**: Darker shade with subtle glow
- **Label**: "Advanced • Level 7"

**Expert (Level 9-10):**
- **Progress**: 86-100% filled
- **Color**: Darkest shade with gold accent
- **Label**: "Expert • Level 10"

### Level Indicator

#### Purpose
Display user's overall level prominently in profile areas and achievements.

#### Visual Specifications

**Circular Level Badge:**
- **Size**: `60px` diameter (large), `40px` (medium), `24px` (small)
- **Background**: Gradient based on level tier
- **Border**: 3px solid white with 1px outer border in tier color
- **Shadow**: `0 2px 6px rgba(0, 0, 0, 0.15)`

**Level Number:**
- **Typography**: Based on badge size
  - Large: H3 (20px/28px, 600 weight)
  - Medium: Body Medium (16px/22px, 500 weight)  
  - Small: Body Small (14px/20px, 500 weight)
- **Color**: White with slight text shadow
- **Position**: Centered in badge

**Level Tiers:**

*Novice (Levels 1-5):*
- **Gradient**: `#6B7280` to `#9CA3AF` (Neutral grays)
- **Theme**: Learning the basics

*Practitioner (Levels 6-15):*
- **Gradient**: `#3B82F6` to `#1D4ED8` (Blue range)
- **Theme**: Developing skills

*Confident (Levels 16-30):*
- **Gradient**: `#10B981` to `#047857` (Green range)
- **Theme**: Building confidence

*Expert (Levels 31-50):*
- **Gradient**: `#8B5CF6` to `#6D28D9` (Purple range)
- **Theme**: Mastering techniques

*Master (Levels 51+):*
- **Gradient**: `#F59E0B` to `#D97706` (Gold range)
- **Theme**: Teaching others

### Progress Celebration Animations

#### Level Up Animation

**Sequence:**
1. **Progress Fill**: XP bar fills completely (500ms)
2. **Flash Effect**: Brief golden glow on bar (200ms)
3. **Level Update**: Number increments with scale animation (300ms)
4. **Particle Effect**: Sparkles emanate from level badge (800ms)
5. **Modal Presentation**: Achievement modal appears (400ms)

**Colors:**
- **Golden Glow**: `#FBBF24` (Yellow) overlay
- **Particles**: Mix of Primary and Secondary colors
- **Modal Background**: Celebratory gradient

#### Achievement Unlock Animation

**Sequence:**
1. **Badge Appearance**: Scale up from 0 to 1 with bounce (500ms)
2. **Shine Effect**: Light sweep across badge (300ms)
3. **Particle Burst**: Confetti-style celebration (1000ms)
4. **Text Reveal**: Achievement name and description (400ms)

#### Streak Milestone Animation

**Sequence:**
1. **Fire Growth**: Fire emoji scales up briefly (200ms)
2. **Number Update**: Streak number updates with emphasis (300ms)
3. **Glow Effect**: Amber glow around entire streak indicator (500ms)
4. **Pulse**: Gentle pulsing effect for 2 seconds

## Accessibility Features

### Screen Reader Support

**Progress Indicators:**
- **Announcements**: "Experience: 350 of 650 points to next level"
- **Level Changes**: "Level up! Now level 4"
- **Achievement Unlocks**: "Achievement unlocked: Conversation Starter"

**Streak Information:**
- **Current Streak**: "Current streak: 7 days"
- **Milestone**: "Streak milestone reached: 7 days"
- **At Risk**: "Streak at risk: complete 1 conversation today"

### Visual Accessibility

**High Contrast Support:**
- **Progress Bars**: Maintain contrast ratios in high contrast mode
- **Achievement Badges**: Clear definition without relying solely on color
- **Text Labels**: All text meets WCAG AA standards

**Color Independence:**
- **Progress Indicators**: Include numerical values alongside visual progress
- **Achievements**: Icons and text provide meaning beyond color
- **Skill Categories**: Clear labeling supplements color coding

### Motor Accessibility

**Interactive Elements:**
- **Badge Viewing**: Minimum 44x44px touch targets for achievement details
- **Progress Details**: Easy access to detailed progress information
- **Celebration Dismissal**: Multiple ways to dismiss celebration modals

## Usage Guidelines

### Motivation Psychology

**Positive Reinforcement:**
- **Focus**: Celebrate progress rather than perfection
- **Frequency**: Regular small wins build toward larger achievements
- **Variety**: Multiple types of recognition appeal to different motivations

**Progress Visibility:**
- **Granular**: Show incremental progress to maintain motivation
- **Contextual**: Progress relevant to user's goals and skill level
- **Achievable**: Next milestone should feel within reach

### Performance Considerations

**Animation Performance:**
- **60fps Target**: All animations use hardware-accelerated properties
- **Reduced Motion**: Respect user's motion preferences
- **Battery Efficiency**: Limit continuous animations

**Data Management:**
- **Local Storage**: Achievement and progress data cached locally
- **Sync Strategy**: Background sync with conflict resolution
- **Offline Support**: Progress tracking works offline

## Implementation Notes

### Data Structure

**User Progress Schema:**
```json
{
  "level": 3,
  "totalXP": 1250,
  "currentLevelXP": 350,
  "xpToNextLevel": 650,
  "streak": {
    "current": 7,
    "best": 12,
    "lastActivity": "2025-08-23"
  },
  "skills": {
    "conversationStarters": { "level": 2, "xp": 180 },
    "flowMaintenance": { "level": 3, "xp": 420 }
  },
  "achievements": [
    {
      "id": "first_steps",
      "unlockedAt": "2025-08-15",
      "tier": "bronze"
    }
  ]
}
```

### Platform Integration

**iOS:**
- **Haptic Feedback**: Celebration haptics for achievements and level ups
- **Widget Support**: Streak and progress in home screen widgets
- **Shortcuts**: Siri shortcuts for progress queries

**Android:**
- **Live Tiles**: Progress updates on supported launchers
- **Notifications**: Achievement notifications with rich content
- **Assistant**: Google Assistant integration for progress queries

---

## Related Documentation
- [Achievement Cards](./cards.md) - Detailed achievement card specifications
- [Color Tokens](../tokens/colors.md) - Gamification color system
- [Animation Tokens](../tokens/animations.md) - Progress animation specifications
- [User Journey](../../user-journey-overall.md) - Gamification in user flow

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*