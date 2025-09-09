# Scenario Selection Feature - User Journey

---
title: Scenarios Tab - Pre-built Scenario Selection User Journey
description: Complete user flow for choosing pre-built practice scenarios with templates in the Scenarios tab
feature: scenarios-tab-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - screen-states.md
  - interactions.md
  - accessibility.md
  - implementation.md
dependencies:
  - profile feature integration
  - pre-conversation-context feature
status: approved
---

## User Journey Overview

**Tab Location**: Scenarios Tab

The scenario selection journey in the **Scenarios tab** empowers users to choose from pre-built, curated practice scenarios with professional templates. These trending scenarios provide quick-start options with pre-filled contexts that users can use as-is or modify. This journey is distinct from the Chat tab's custom conversation creation.

## Entry Points

### Primary Entry Point: Scenarios Tab Navigation
**Trigger**: User taps the Scenarios tab from bottom navigation
**Context**: User wants to practice with pre-built, trending scenarios that include templates
**Emotional State**: Seeking quick practice with professional guidance, wants curated experiences
**Success Criteria**: Browse trending scenarios, select one with pre-filled template, start practicing quickly

**Note**: The Chat tab provides a different experience with custom conversation creation, where users select location and difficulty then write their own context from scratch

### Secondary Entry Point: Post-Feedback Navigation
**Trigger**: User completes conversation and selects "Try Different Scenario"
**Context**: User just finished practice session and wants to try something new
**Emotional State**: Energized by recent practice, ready for new challenge
**Success Criteria**: Smooth transition to new scenario selection

### Tertiary Entry Point: Recommendation Flow
**Trigger**: AI or profile system suggests specific scenario for user
**Context**: Based on user goals, progress, or identified skill gaps
**Emotional State**: Open to guidance, trusting app recommendations
**Success Criteria**: Accept and engage with recommended scenario

## Core User Journey Flow

### Phase 1: Initial Orientation (3-5 seconds)

#### Step 1: Scenario Overview (Scenarios Tab)
**User Experience**:
- Two main sections: Predefined Scenarios and Trending Scenarios
- Clean grid view of curated conversation contexts
- Visual previews showing scenario environments
- Clear indication of user's progress/history in each scenario
- Quick access to recently practiced scenarios
- Each scenario designed for specific skill practice

**User Mental Model**: "What situation do I want to practice today?"
**Emotional State**: Browsing mindset, evaluating options
**Key Success Factor**: Quick visual scanning to identify appealing scenarios

**Persona-Specific Adaptations**:
- **Anxious Alex**: Emphasis on low-pressure scenarios, success indicators
- **Comeback Catherine**: Age-appropriate scenarios highlighted
- **Confident Carlos**: Advanced/challenging scenarios prominently featured
- **Shy Sarah**: Safe, quiet scenarios emphasized with encouragement

#### Step 2: Scenario Exploration
**User Experience**:
- Hover/tap preview of scenario details
- Brief description of scenario context
- Visual indicators of difficulty levels available
- Success rate information (if user has history)

**User Mental Model**: "What would this practice session be like?"
**Emotional State**: Evaluating fit with current mood and goals
**Key Success Factor**: Clear understanding of what each scenario entails

### Phase 2: Scenario Selection (10-15 seconds)

#### Step 3: Primary Scenario Choice
**User Experience**:
- Tap to select desired predefined or trending scenario
- Modal opens with scenario details and difficulty options
- Brief scenario context and learning objectives
- Option to preview what the template includes
- Smooth transition to context creation with pre-filled template

**User Mental Model**: "This scenario matches what I want to practice"
**Emotional State**: Committing to practice direction
**Key Success Factor**: Confidence in scenario relevance to real-world goals

#### Step 4: Difficulty Level Selection
**User Experience**:
- Clear visual representation of three difficulty levels
- 🟢 Green: "Friendly atmosphere, welcoming people"
- 🟡 Yellow: "Realistic interactions, mixed responses"
- 🔴 Red: "Challenging environment, requires your A-game"
- Personal success rates displayed for each level (if available)

**User Mental Model**: "How challenging do I want this practice to be?"
**Emotional State**: Calibrating challenge level to current confidence
**Key Success Factor**: Appropriate difficulty selection for optimal learning

### Phase 3: Pre-Practice Preparation (8-12 seconds)

#### Step 5: Scenario Confirmation
**User Experience**:
- Confirmation of selected scenario and difficulty
- Brief preview of what to expect
- Final context details (location, time of day, etc.)
- "Start Practice" button with anticipation-building messaging

**User Mental Model**: "I understand what I'm about to practice"
**Emotional State**: Anticipation mixed with appropriate nervousness
**Key Success Factor**: Clear expectations set for practice session

#### Step 6: Context Transition
**User Experience**:
- Smooth transition to pre-conversation context screen
- Maintain selected scenario and difficulty information
- Brief loading/preparation messaging
- Continuity in visual design and user flow

**User Mental Model**: "Now I'm seeing the specific details of my practice session"
**Emotional State**: Focused preparation for conversation
**Key Success Factor**: Seamless flow maintains momentum and engagement

## Advanced User Paths

### Quick Practice Path
**Behavior**: Users who want to quickly repeat recent scenarios
**Solution**: "Quick Practice" section with recent scenarios prominently displayed
**Key Elements**:
- Recently used scenarios at top of selection
- One-tap access to repeat previous scenario/difficulty combinations
- Progress indicators showing improvement in familiar scenarios

**Flow**: Main Menu → Quick Practice → Same Scenario/Difficulty → Start

### Exploration Mode
**Behavior**: Users who want to browse all available scenarios
**Solution**: Enhanced exploration interface with detailed previews
**Key Elements**:
- Detailed scenario previews with example context
- Comparison view between scenarios
- "Random" option for adventurous users
- Scenario recommendation based on goals and progress

**Flow**: Main Menu → Explore Scenarios → Preview Details → Compare Options → Select

### Skill-Focused Selection
**Behavior**: Users targeting specific conversation skills
**Solution**: Scenario filtering and recommendations based on skill development
**Key Elements**:
- Filter scenarios by skill focus (conversation starters, flow, storytelling)
- AI recommendations for skill gap improvement
- Progress tracking for specific skills across scenarios
- Integration with profile learning goals

**Flow**: Main Menu → Filter by Skill → View Recommended Scenarios → Select Best Match

### Progressive Challenge Path
**Behavior**: Users ready to advance difficulty levels
**Solution**: Clear progression indicators and guided difficulty advancement
**Key Elements**:
- "Ready for next level?" prompts based on success rates
- Graduated difficulty progression suggestions
- Achievement unlocks for difficulty advancement
- Encouragement messaging for taking on challenges

**Flow**: Scenario Selection → Difficulty Choice → "Try Next Level?" Prompt → Confirm Challenge

## Edge Cases and Error Recovery

### Scenario Unavailable
**Scenario**: Selected scenario temporarily unavailable due to technical issues
**User Experience**:
- Clear explanation of temporary unavailability
- Alternative scenario suggestions
- Option to be notified when available
- Smooth redirect to similar scenarios

### Difficulty Mismatch
**Scenario**: User consistently struggles or succeeds too easily at selected difficulty
**User Experience**:
- Gentle suggestion to adjust difficulty after multiple sessions
- Clear explanation of benefits of different difficulty levels
- No pressure - user maintains full control
- Option to try different difficulty as "experiment"

### Profile Integration Issues
**Scenario**: User profile preferences don't align with scenario choices
**User Experience**:
- Scenarios work regardless of profile completeness
- Gentle prompts to complete profile for better recommendations
- Clear indication of how profile affects scenario personalization
- Full functionality without complete profile

## Success Metrics for Journey

### Selection Efficiency
- **Time to Selection**: Average 15-30 seconds from entry to scenario start
- **Selection Confidence**: >90% of users complete selected scenarios
- **Exploration Rate**: 60%+ users try multiple scenario types within first week
- **Return Patterns**: Users develop preferred scenarios with occasional variety

### Learning Progression
- **Difficulty Advancement**: Users progress through difficulty levels within 3-4 weeks
- **Appropriate Challenge**: 70-80% success rate indicates optimal difficulty selection
- **Skill Development**: Scenario variety correlates with broader skill improvement
- **Real-World Application**: Users report practicing selected scenario types in real life

### User Satisfaction
- **Choice Satisfaction**: >85% users rate their scenario selections as appropriate
- **Variety Appreciation**: Users express satisfaction with available scenario options
- **Difficulty Balance**: Users find difficulty levels appropriately calibrated
- **Recommendation Quality**: AI scenario suggestions meet user needs

## Persona-Specific Journey Variations

### Anxious Alex Journey Adaptations
- **Comfort Zone Emphasis**: Green scenarios prominently featured with success encouragement
- **Gentle Progression**: Subtle suggestions for difficulty advancement when ready
- **Safety Indicators**: Clear messaging about practice being in safe environment
- **Success Building**: Focus on scenarios where Alex can build confidence gradually

### Comeback Catherine Journey Adaptations  
- **Age-Appropriate Focus**: Scenarios relevant to 30s dating highlighted
- **Modern Context**: Scenarios reflect contemporary dating landscape
- **Practical Application**: Clear connection between practice and real-world dating success
- **Balanced Challenge**: Mix of Yellow and Red difficulty levels for realistic preparation

### Confident Carlos Journey Adaptations
- **Challenge Seeking**: Red difficulty levels and complex scenarios emphasized
- **Optimization Focus**: Analytics on success rates and improvement opportunities
- **Variety Encouragement**: Prompts to try different scenarios for skill breadth
- **Competitive Elements**: Achievement tracking and milestone celebrations

### Shy Sarah Journey Adaptations
- **Ultra-Gentle Approach**: Green scenarios with extra encouragement and safety emphasis
- **Private Practice**: No social comparison or competitive elements
- **Gradual Exposure**: Very slow progression through comfort zones
- **Safe Spaces**: Emphasis on quiet, low-pressure scenarios (bookstores, coffee shops)

## Related Documentation

- **[Screen States](./screen-states.md)** - Visual specifications for scenario selection interface
- **[Interactions](./interactions.md)** - Animation and interaction details
- **[Accessibility](./accessibility.md)** - Inclusive design for scenario selection
- **[Implementation](./implementation.md)** - Technical specifications for developers

## Implementation Notes

### State Management Flow
1. **Entry** → Load available scenarios and user history
2. **Browse** → Track scenario previews and user interest patterns
3. **Select** → Store scenario choice and prepare difficulty selection
4. **Difficulty** → Store complete selection and prepare context generation
5. **Transition** → Pass selection data to pre-conversation context system

### Analytics Tracking
- **Scenario Browsing Patterns**: Which scenarios get the most preview attention
- **Selection Preferences**: User patterns in scenario and difficulty choices
- **Completion Rates**: Success rates for different scenario/difficulty combinations
- **Progression Tracking**: How users advance through difficulty levels over time

### Performance Considerations
- **Fast Loading**: Scenario previews and images load quickly
- **Smooth Transitions**: No lag between selection and preparation phases
- **Offline Browsing**: Cached scenario information available offline
- **Quick Restart**: Recently used scenarios accessible with minimal loading

## Last Updated
- **Version 1.0.0**: Complete user journey mapping with persona variations and edge cases
- **Focus**: Empowering choice with appropriate challenge calibration
- **Next**: Technical implementation with performance optimization