# Gamification Interactions

---
title: FlirtCraft Gamification Animation and Interaction Patterns
description: Complete specifications for XP gain animations, achievement celebrations, streak effects, and progress interactions
feature: gamification
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./user-journey.md
  - ./screen-states.md
  - ./accessibility.md
  - ./implementation.md
dependencies:
  - Animation system components
  - Haptic feedback integration
  - Audio feedback system
  - Particle effect library
status: planned-phase-2
---

## Overview

This document defines all animation patterns, micro-interactions, and feedback systems for FlirtCraft's gamification features, ensuring delightful, purposeful animations that enhance user engagement while supporting learning goals and maintaining accessibility standards.

## Table of Contents

1. [XP Gain Animations](#xp-gain-animations)
2. [Level Up Celebrations](#level-up-celebrations)
3. [Achievement Unlock Animations](#achievement-unlock-animations)
4. [Streak Fire Effects](#streak-fire-effects)
5. [Progress Chart Interactions](#progress-chart-interactions)
6. [Micro-interactions](#micro-interactions)
7. [Accessibility Considerations](#accessibility-considerations)

## XP Gain Animations

### Primary XP Award Animation

#### XP Counter Roll-Up Effect
**Animation Specifications**:
- **Duration**: 1.2 seconds total animation
- **Easing**: `cubic-bezier(0.4, 0.0, 0.2, 1)` (ease-in-out)
- **Number Animation**: Counter incrementally rolls from current to new XP value
- **Visual Feedback**: Subtle glow effect around XP display during animation
- **Audio**: Gentle "ding" sound on completion (respects user audio preferences)

**Technical Implementation**:
```css
/* XP Counter Animation */
@keyframes xpCounterRoll {
  0% { 
    transform: scale(1);
    color: var(--neutral-900);
  }
  20% {
    transform: scale(1.05);
    color: var(--primary);
  }
  100% {
    transform: scale(1);
    color: var(--neutral-900);
  }
}

.xp-counter-animation {
  animation: xpCounterRoll 1.2s ease-in-out;
}
```

**JavaScript Counter Logic**:
```javascript
function animateXPCounter(startValue, endValue, duration = 1200) {
  const increment = (endValue - startValue) / (duration / 16);
  let currentValue = startValue;
  
  const updateCounter = () => {
    currentValue += increment;
    if (currentValue >= endValue) {
      currentValue = endValue;
      // Animation complete - trigger completion callbacks
    }
    
    display.textContent = Math.floor(currentValue);
    
    if (currentValue < endValue) {
      requestAnimationFrame(updateCounter);
    }
  };
  
  requestAnimationFrame(updateCounter);
}
```

#### XP Bar Fill Animation
**Progress Bar Animation**:
- **Fill Duration**: 800ms for bar progression
- **Easing**: `cubic-bezier(0.0, 0.0, 0.2, 1)` (ease-out)
- **Glow Effect**: Golden glow follows fill progress
- **Particle Trail**: Small sparkle particles trail behind fill progress
- **Overflow Handling**: Smooth transition to next level if XP exceeds current level

**CSS Animation Keyframes**:
```css
@keyframes xpBarFill {
  0% {
    width: var(--start-progress);
    box-shadow: 0 0 0 rgba(249, 115, 22, 0);
  }
  50% {
    box-shadow: 0 0 8px rgba(249, 115, 22, 0.4);
  }
  100% {
    width: var(--end-progress);
    box-shadow: 0 0 0 rgba(249, 115, 22, 0);
  }
}
```

#### Bonus XP Stacking Animation
**Sequential Bonus Display**:
- **Timing**: 0.3s delay between each bonus appearance
- **Individual Animation**: Each bonus floats up with unique trajectory
- **Stacking Logic**: Bonuses appear in order of significance
- **Accumulation Effect**: Running total updates as each bonus appears

**Floating Bonus Animation**:
```css
@keyframes bonusXPFloat {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
  }
  20% {
    opacity: 1;
    transform: translateY(0) scale(1.1);
  }
  80% {
    opacity: 1;
    transform: translateY(-30px) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
}
```

### XP Milestone Animations

#### Near Level-Up Pulse Effect
**Anticipation Animation**:
- **Trigger**: When XP progress reaches 90% of current level
- **Effect**: Gentle pulsing glow around XP bar and level indicator
- **Duration**: 1.5s cycle with continuous loop
- **Colors**: Enhanced orange gradient with golden highlights
- **Purpose**: Creates excitement and anticipation for upcoming level-up

**Pulse Animation Implementation**:
```css
@keyframes levelUpPulse {
  0%, 100% {
    box-shadow: 0 0 0 rgba(249, 115, 22, 0);
  }
  50% {
    box-shadow: 0 0 12px rgba(249, 115, 22, 0.6);
  }
}

.near-levelup {
  animation: levelUpPulse 1.5s ease-in-out infinite;
}
```

## Level Up Celebrations

### Level Up Animation Sequence

#### Mobile Full-Screen Celebration
**Complete Animation Timeline**:

**Phase 1: Screen Preparation (0-0.3s)**:
- Current interface dims with dark overlay fade-in
- Particle generation begins from screen center
- Audio preparation (if enabled)

**Phase 2: Particle Burst (0.3-0.8s)**:
- Golden particles explode from center in radial pattern
- Particle colors: Orange (#F97316), Gold (#F59E0B), Amber (#FBB043)
- Particle count: 24 particles with varied sizes and velocities

**Phase 3: Level Badge Entrance (0.5-1.2s)**:
- Level badge scales up from 0 to full size with bounce effect
- Badge design: Circular badge with new level number
- Animation: Scale with overshoot (1.2x) then settle to 1.0x
- Rotation: Subtle 5-degree rotation during scale-up

**Phase 4: Typography Reveal (0.8-1.5s)**:
- "Level Up!" text slides down from top
- Level number and description fade in
- Typography effects: Subtle golden glow and shadow

**Phase 5: Benefits Display (1.2-2.0s)**:
- New level benefits list animates in with staggered timing
- Each benefit item appears with slide-left animation
- XP multiplier and unlock notifications display

**Phase 6: Return Transition (2.5-3.2s)**:
- Celebration elements fade out gracefully
- Interface returns to normal with updated level display
- New level badge remains visible in ongoing UI

#### Desktop Modal Celebration
**Centered Modal Animation**:
- **Entrance**: Modal slides up from bottom with spring physics
- **Background**: Backdrop blurs with particle overlay
- **Content**: Same celebration sequence adapted for modal container
- **Interaction**: Click anywhere or press Escape to dismiss early
- **Exit**: Modal slides down with fade-out effect

**Spring Physics Parameters**:
```javascript
const springConfig = {
  tension: 200,
  friction: 20,
  overshoot: 1.1,
  restDelta: 0.01
};
```

### Level Badge Design Evolution

#### Progressive Badge Styling
**Level 1-3 (Beginner)**:
- **Colors**: Orange gradient with silver accents
- **Style**: Simple circular design with clean typography
- **Effects**: Subtle glow on level-up, minimal particle effects

**Level 4-6 (Intermediate)**:
- **Colors**: Enhanced orange with gold accents
- **Style**: Hexagonal border with inner circle
- **Effects**: More prominent glow, increased particle count
- **Extras**: Small crown icon appears above badge

**Level 7-10 (Advanced)**:
- **Colors**: Gold gradient with platinum highlights
- **Style**: Star-shaped outer border with ornate details
- **Effects**: Intense glow, multi-colored particles
- **Extras**: Animated crown with gems, prestige indicators

**Animation Complexity Scaling**:
- Beginner: Simple scale and fade animations
- Intermediate: Scale, rotation, and particle effects
- Advanced: Complex multi-stage animations with physics

## Achievement Unlock Animations

### Achievement Unlock Sequence

#### Achievement Badge Materialization
**Animation Stages**:

**Stage 1: Discovery Effect (0-0.5s)**:
- Achievement area highlights with golden outline
- Subtle particle generation around achievement location
- Anticipation build-up with gentle pulsing

**Stage 2: Badge Formation (0.5-1.2s)**:
- Achievement icon materializes with scale animation
- Icon starts as light particles that coalesce into final form
- Background badge fades in behind icon with soft glow

**Stage 3: Text Revelation (1.0-1.8s)**:
- Achievement title types in with typewriter effect
- Description text fades in with upward slide
- XP reward badge bounces in from right side

**Stage 4: Integration (1.8-2.5s)**:
- Achievement settles into final position
- Added to achievement gallery with smooth transition
- Profile integration updates visible

**Particle System Details**:
```javascript
const achievementParticles = {
  count: 16,
  colors: ['#F97316', '#F59E0B', '#FBB043'],
  size: { min: 2, max: 6 },
  velocity: { min: 50, max: 120 },
  lifespan: 2000,
  gravity: 0.3
};
```

#### Achievement Category Celebrations

**Getting Started Achievements**:
- **Colors**: Soft orange and yellow tones
- **Particles**: Gentle floating sparkles
- **Audio**: Light, encouraging chime
- **Message**: "Great first step!" type encouragement

**Skill Development Achievements**:
- **Colors**: Vibrant orange with blue accents
- **Particles**: Directed burst toward skill icon
- **Audio**: Confident success tone
- **Message**: "Skill unlocked!" with specific skill recognition

**Milestone Achievements**:
- **Colors**: Gold and orange with white highlights
- **Particles**: Large burst with star-shaped particles
- **Audio**: Triumphant fanfare (brief)
- **Message**: "Major milestone reached!" celebration

### Achievement Gallery Interactions

#### Achievement Card Hover Effects
**Desktop Hover Animation**:
- **Lift Effect**: Subtle 2px vertical translation
- **Shadow Enhancement**: Shadow depth increases from 2px to 8px
- **Glow Addition**: Achievement border gains soft colored glow
- **Icon Animation**: Achievement icon scales up by 5% (1.05x)
- **Transition**: All effects use 200ms ease-out timing

**Achievement Card Tap/Click**:
- **Immediate Feedback**: 0.95x scale down for 100ms
- **Haptic Feedback**: Light haptic pulse on mobile devices
- **Audio Feedback**: Subtle click sound
- **Modal Trigger**: Opens achievement detail modal

#### Achievement Progress Visualization
**Progress Bar Animation in Cards**:
- **Fill Animation**: Progress bar fills to current completion percentage
- **Color Transition**: Bar color transitions from grey to orange as progress increases
- **Milestone Indicators**: Small notches or markers show key progress points
- **Near Completion**: Progress bar pulses when 80%+ complete

## Streak Fire Effects

### Streak Flame Animation

#### Base Flame Animation
**Flame Dynamics**:
- **Movement**: Organic flickering motion using Perlin noise
- **Colors**: Orange base (#F97316) with yellow tips (#FBB043)
- **Scale Variation**: 0.95x to 1.05x size variation in 2.3s cycles
- **Opacity Pulses**: Subtle opacity changes (0.9 to 1.0) for liveliness

**CSS Animation Implementation**:
```css
@keyframes flameFlicker {
  0%, 100% { transform: scaleY(1) scaleX(1); }
  25% { transform: scaleY(1.05) scaleX(0.98); }
  50% { transform: scaleY(0.95) scaleX(1.02); }
  75% { transform: scaleY(1.02) scaleX(0.97); }
}

.streak-flame {
  animation: flameFlicker 2.3s ease-in-out infinite;
}
```

#### Streak Intensity Progression
**Days 1-2: Ember Stage**:
- **Size**: Small flame (20px height)
- **Color**: Orange with minimal yellow
- **Animation**: Gentle flicker, low intensity
- **Particles**: No additional particle effects

**Days 3-6: Growing Flame**:
- **Size**: Medium flame (28px height)
- **Color**: Orange with yellow tips
- **Animation**: More pronounced flicker
- **Particles**: Occasional small sparkles

**Days 7-13: Strong Fire**:
- **Size**: Large flame (36px height)
- **Color**: Orange, yellow, with white-hot center
- **Animation**: Dynamic flicker with scale variations
- **Particles**: Regular sparkle generation
- **Glow**: Subtle orange glow around flame

**Days 14+: Inferno**:
- **Size**: Extra large flame (44px height)
- **Color**: Full spectrum with blue accents at base
- **Animation**: Complex multi-layer flicker
- **Particles**: Continuous particle generation
- **Glow**: Prominent multi-color glow effect
- **Crown**: Small crown icon appears above flame

### Streak Progress Ring Animation

#### Daily Progress Ring
**Ring Fill Animation**:
- **Progress Timing**: Ring gradually fills throughout day based on time
- **Color Gradient**: Orange to yellow to white as ring completes
- **Completion Celebration**: Ring pulses with light burst when conversation completed
- **Reset Animation**: Smooth reset to empty at midnight (user timezone)

**Ring Physics**:
```css
.streak-progress-ring {
  stroke-dasharray: 188; /* Circumference for 60px diameter */
  stroke-dashoffset: calc(188 - (188 * var(--progress-percentage)));
  transition: stroke-dashoffset 0.5s ease-out;
}
```

#### Streak Completion Celebration
**Daily Goal Achievement**:
- **Ring Completion**: Final segment fills with particle burst
- **Flame Enhancement**: Flame temporarily grows 20% larger
- **Glow Pulse**: Bright glow pulse emanates from completed ring
- **Audio**: Satisfying completion sound
- **Haptic**: Success haptic pattern (iOS: .success, Android: medium)

### Streak Milestone Celebrations

#### Weekly Milestone (7 days)
**Celebration Sequence**:
- **Duration**: 3-second celebration
- **Flame Transformation**: Flame grows to "Strong Fire" level instantly
- **Particle Burst**: Golden particles radiate from flame
- **Badge Appearance**: "Weekly Warrior" badge materializes
- **Multiplier Display**: "1.25x XP Multiplier Unlocked!" notification

#### Monthly Milestone (30 days)
**Epic Celebration**:
- **Duration**: 4-second celebration
- **Flame Evolution**: Transform to full "Inferno" level
- **Crown Addition**: Golden crown appears above flame
- **Particle Show**: Multi-colored particle explosion
- **Achievement Stack**: Multiple achievements may unlock simultaneously
- **Special Audio**: Extended fanfare sound

## Progress Chart Interactions

### Chart Hover and Selection

#### XP Trend Chart Interactions
**Data Point Hover**:
- **Highlight**: Data point scales up 1.3x with glow effect
- **Tooltip**: Detailed information appears above point
- **Connected Line**: Line segment highlights leading to/from point
- **Animation**: Smooth 150ms transition for all hover effects

**Tooltip Content**:
- Date and day of week
- XP earned that day with breakdown
- Conversations completed
- Any achievements unlocked
- Streak status for that day

#### Progress Dashboard Animations
**Card Entry Animation**:
- **Staggered Timing**: Cards appear with 100ms delays between each
- **Entrance**: Slide up from bottom with fade-in effect
- **Bounce**: Subtle bounce effect on final positioning
- **Chart Drawing**: Charts animate in after cards settle

**Chart Data Animation**:
- **Bar Charts**: Bars grow from bottom to full height over 800ms
- **Line Charts**: Line draws from left to right over 1000ms
- **Pie Charts**: Segments fill clockwise starting from top
- **Easing**: All chart animations use ease-out timing

### Interactive Chart Elements

#### Skill Development Rings
**Progress Ring Interactions**:
- **Tap/Click**: Ring expands temporarily (1.1x) and shows detailed breakdown
- **Progress Fill**: Animated progress fill when data updates
- **Skill Comparison**: Multiple rings can be compared side-by-side
- **Color Coding**: Each skill has distinct color with semantic meaning

#### Achievement Progress Bars
**Micro-interactions**:
- **Hover**: Progress bar gains subtle glow and shows exact progress numbers
- **Near Completion**: Progress bars pulse when 80%+ complete
- **Completion**: Bar fills completely and briefly pulses with success color
- **Tip Integration**: Achievement tips appear on hover/tap

## Micro-interactions

### Button and Control Interactions

#### Primary Action Buttons
**Button Press Animation**:
- **Press Down**: 0.95x scale with 100ms duration
- **Release**: Return to 1.0x scale with gentle overshoot (1.02x)
- **Haptic**: Light haptic feedback on mobile devices
- **Color Shift**: Slight darkening of button color during press

**Button Hover (Desktop)**:
- **Color Transition**: Smooth transition to hover color over 150ms
- **Elevation**: Shadow depth increases subtly
- **Icon Animation**: Icons within buttons may scale or rotate slightly
- **Cursor**: Cursor changes to pointer with smooth transition

#### Achievement Filter Tabs
**Tab Selection Animation**:
- **Background Transition**: Active background slides to selected tab
- **Text Color**: Text color transitions from neutral to white
- **Scale Effect**: Active tab scales up slightly (1.05x)
- **Badge Updates**: Achievement count badges update with number animation

### Loading and State Transitions

#### Progress Data Loading
**Skeleton Screens**:
- **Wave Animation**: Subtle shimmer effect moves across loading placeholders
- **Timing**: 1.5s wave cycle with 0.3s delay between waves
- **Colors**: Neutral gradient from light to lighter grey
- **Graceful Reveal**: Real content fades in as data loads

**Error State Transitions**:
- **Shake Animation**: Brief shake animation for error states
- **Color Transition**: Elements transition to error colors smoothly
- **Recovery Animation**: Smooth transition back to normal state when error resolves

### Notification Interactions

#### Achievement Notification Banners
**Banner Entrance**:
- **Slide Down**: Banner slides down from top edge with spring physics
- **Bounce Effect**: Gentle bounce when banner reaches final position
- **Auto Dismiss**: Automatically slides up after 4 seconds
- **Manual Dismiss**: Tap anywhere to trigger immediate slide-up dismissal

**Toast Notifications**:
- **Slide Up**: Toast slides up from bottom with ease-out animation
- **Fade Out**: Gradual fade out over final second
- **Stack Management**: Multiple toasts stack with proper spacing

## Accessibility Considerations

### Motion and Animation Accessibility

#### Reduced Motion Support
**CSS Media Query Implementation**:
```css
@media (prefers-reduced-motion: reduce) {
  .xp-counter-animation,
  .achievement-celebration,
  .level-up-particles {
    animation: none;
  }
  
  .progress-bar-fill {
    transition: none;
  }
  
  .flame-flicker {
    animation: none;
  }
}
```

**Alternative Static States**:
- XP gains show final value immediately
- Achievement unlocks appear without animation
- Progress bars jump to final state
- Streak indicators show static flame icon
- Level-up shows immediate state change

#### Cognitive Accessibility
**Animation Simplification**:
- **Essential Information**: Critical information never depends on animation
- **Clear States**: All UI states are clearly defined without motion
- **Optional Enhancement**: Animation enhances but doesn't replace core information
- **Pause Controls**: Long animations can be paused or skipped

### Audio and Haptic Accessibility

#### Sound Preferences
**Audio Feedback Respect**:
- **System Settings**: Respect device sound and notification settings
- **In-App Controls**: Optional audio toggle in app settings
- **Alternative Feedback**: Visual feedback replaces audio when disabled
- **Volume Levels**: All sounds respect system volume controls

#### Haptic Feedback Guidelines
**Appropriate Usage**:
- **Meaningful Actions**: Haptic feedback only for significant interactions
- **System Respect**: Respect device haptic settings
- **Battery Consideration**: Minimal battery impact from haptic usage
- **Alternative Indication**: Visual feedback accompanies all haptic feedback

### Screen Reader Support

#### Animation Announcements
**Proper ARIA Integration**:
- **Live Regions**: Progress updates announced through aria-live regions
- **Achievement Announcements**: Screen reader announces achievement unlocks
- **Progress Description**: XP and level changes described textually
- **Streak Updates**: Daily streak progress announced appropriately

**Animation-Independent Content**:
- All gamification information accessible without visual animation
- Achievement descriptions include progress and requirements
- Progress data available through accessible HTML structure
- Interactive elements have proper focus management

---

## Performance Optimization

### Animation Performance

#### Hardware Acceleration
**GPU-Accelerated Properties**:
- Transform animations use translateZ(0) for hardware acceleration
- Opacity changes optimized for GPU rendering
- Particle systems use efficient rendering techniques
- Complex animations degrade gracefully on low-end devices

#### Memory Management
**Efficient Animation Handling**:
- Particle systems are pooled and recycled
- Animations clean up event listeners on completion
- Large particle counts reduced on mobile devices
- Animation loops properly terminated to prevent memory leaks

### Battery Optimization
**Power-Efficient Animations**:
- Reduce particle counts on mobile devices
- Pause animations when app is backgrounded
- Use CSS animations over JavaScript where possible
- Implement frame rate limiting for complex animations

---

## Related Documentation

- [Gamification Feature Overview](./README.md) - Complete system design and philosophy
- [Gamification User Journey](./user-journey.md) - User experience flow through gamification
- [Gamification Screen States](./screen-states.md) - Visual specifications for all interface states
- [Gamification Accessibility](./accessibility.md) - Inclusive interaction design
- [Gamification Implementation](./implementation.md) - Technical implementation details

## Implementation Dependencies

### Animation Libraries
- **Spring Physics**: For natural movement animations
- **Particle System**: For celebration and achievement effects
- **Chart Animation**: For progress visualization animations
- **Gesture Recognition**: For touch and swipe interactions

### Platform Integration
- **Haptic Feedback**: Native haptic APIs for iOS and Android
- **Audio System**: Platform audio integration with respect for user settings
- **Performance Monitoring**: Animation performance tracking and optimization
- **Accessibility APIs**: Screen reader and reduced motion integration

---

*These interaction specifications ensure FlirtCraft's gamification system provides delightful, meaningful animations that enhance the learning experience while maintaining accessibility and performance standards across all supported platforms.*