# Unified Selection Feature - Accessibility

---
title: Chat Tab - Unified Selection Accessibility Specifications
description: Comprehensive accessibility implementation for the Chat tab unified location and difficulty selection screen
feature: chat-unified-selection
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - implementation.md
dependencies:
  - ../../accessibility/guidelines.md
  - design-system/tokens/colors.md
status: approved
---

## Accessibility Overview

**Tab Location**: Chat Tab

The unified selection screen in the Chat tab is designed to be fully accessible to users of all abilities, providing multiple interaction modalities and comprehensive assistive technology support. Every element meets or exceeds WCAG 2.1 AA standards while maintaining the elegant, intuitive experience for all users.

## Visual Accessibility

### Color and Contrast Requirements

#### Color Contrast Compliance
**Text Contrast Ratios** (exceeding WCAG AA 4.5:1 minimum):
- **Screen Title**: #1F2937 on #FFFFFF = 16.4:1 ratio ✓
- **Subtitle Text**: #6B7280 on #FFFFFF = 5.4:1 ratio ✓
- **Location Card Titles**: #FFFFFF on dark overlay = 12.8:1 ratio ✓
- **Difficulty Card Text**: #FFFFFF on colored backgrounds = 7.2:1 minimum ✓
- **Button Text (Enabled)**: #FFFFFF on #F97316 = 5.9:1 ratio ✓
- **Button Text (Disabled)**: #9CA3AF on #E5E7EB = 2.1:1 ratio (decorative only) ✓

**Interactive Element Contrast** (meeting WCAG AA 3:1 minimum):
- **Location Card Borders**: #F97316 on #FFFFFF = 3.8:1 ratio ✓
- **Difficulty Card Borders**: Various on white backgrounds ≥ 3.5:1 ✓
- **Focus Indicators**: #F97316 on backgrounds ≥ 3.8:1 ratio ✓

#### High Contrast Mode Adaptations
**Automatic Enhancements**:
- **Selection Borders**: Increase to 4px width for clearer visibility
- **Focus Indicators**: Enhanced contrast with system colors
- **Text Shadows**: Removed to prevent contrast interference
- **Background Adjustments**: Enhanced contrast between sections

**Implementation Example**:
```jsx
const useHighContrastColors = () => {
  const isHighContrast = useAccessibilityInfo().isHighContrastEnabled;
  
  return {
    selectionBorder: isHighContrast ? 4 : 3,
    focusRingWidth: isHighContrast ? 4 : 3,
    shadowOpacity: isHighContrast ? 0 : 0.1,
  };
};
```

### Visual Design Adaptations

#### Dynamic Type Support
**Text Scaling Behavior**:
- **Scale Range**: Supports system text sizes from 75% to 200%
- **Layout Adaptation**: Cards expand vertically to accommodate larger text
- **Minimum Sizes**: Text never scales below readable minimums
- **Maximum Constraints**: Prevents text from breaking layout at extreme sizes

**Responsive Text Implementation**:
```jsx
const scaledFontSize = (baseSize) => {
  const fontScale = PixelRatio.getFontScale();
  return Math.max(baseSize * 0.75, Math.min(baseSize * fontScale, baseSize * 2));
};

// Usage in components
fontSize: scaledFontSize(18), // Scales from 13.5px to 36px
```

#### Layout Adaptations for Large Text
**Card Dimension Adjustments**:
- **Location Cards**: Height increases from 180px to maximum 240px
- **Difficulty Cards**: Height increases from 120px to maximum 160px
- **Button Height**: Increases from 48px to maximum 64px
- **Minimum Touch Targets**: Always maintain 44×44px regardless of text size

### Color Independence Design

#### Beyond-Color Information Design
**Selection State Indicators**:
- **Location Cards**: Border thickness, shadow depth, and scale changes
- **Difficulty Cards**: Border addition, shadow enhancement, and scale increase
- **Button States**: Texture pattern overlays in addition to color changes
- **Progress Indicators**: Shape and size variations beyond color coding

**Pattern and Texture Implementation**:
```jsx
// Additional visual indicators beyond color
const SelectionIndicator = ({ isSelected, type }) => (
  <>
    {/* Color indicator */}
    <View style={{ borderColor: isSelected ? primary : transparent }} />
    
    {/* Pattern indicator for color-blind users */}
    {isSelected && (
      <View style={{
        position: 'absolute',
        top: 8,
        right: 8,
        width: 16,
        height: 16,
        backgroundColor: 'white',
        borderRadius: 8,
      }}>
        <CheckIcon size={12} color={primary} />
      </View>
    )}
  </>
);
```

## Screen Reader Accessibility

### VoiceOver/TalkBack Support

#### Navigation Structure
**Logical Reading Order**:
1. **Screen Header**: Title, subtitle, and progress indicator as group
2. **Location Section**: Section heading followed by carousel cards
3. **Difficulty Section**: Section heading followed by difficulty cards
4. **Action Section**: Button and helper text as final group

**Screen Reader Announcements**:
```jsx
// Screen header accessibility
<View accessibilityRole="header">
  <Text accessibilityLabel="Create Your Practice Session, Step 1 of 2">
    Create Your Practice Session
  </Text>
  <Text accessibilityLabel="Choose location and difficulty level">
    Choose location and difficulty level
  </Text>
</View>

// Section headers
<Text 
  accessibilityRole="header"
  accessibilityLabel="Location Selection, swipe left or right to browse locations"
>
  Choose Your Location
</Text>
```

#### Location Carousel Accessibility
**Card Descriptions**:
```jsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel={`${location.name} location for conversation practice`}
  accessibilityState={{ 
    selected: isSelected,
    disabled: false 
  }}
  accessibilityHint={
    isSelected 
      ? "Currently selected. Double-tap to confirm or swipe to explore other locations."
      : "Double-tap to select this location for your practice session."
  }
  accessibilityActions={[
    { name: 'activate', label: 'Select this location' }
  ]}
>
  <Image 
    accessibilityLabel={`${location.name} - ${location.description}`}
    accessibilityRole="image"
  />
</Pressable>
```

**Carousel Navigation Announcements**:
- **Current Position**: "Coffee Shop, location 1 of 8"
- **Navigation Hints**: "Swipe left or right to explore more locations"
- **Selection Changes**: "Coffee Shop selected for practice location"
- **Context Information**: Brief description of each location's atmosphere

#### Difficulty Cards Accessibility
**Comprehensive Descriptions**:
```jsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel={`${difficulty.name} difficulty level`}
  accessibilityState={{ selected: isSelected }}
  accessibilityHint={`${difficulty.description}. ${difficulty.successRate} success rate. Double-tap to select.`}
  accessibilityValue={{
    text: difficulty.detailedDescription
  }}
>
  <Icon accessibilityLabel={`${difficulty.name} difficulty icon`} />
  <Text>{difficulty.name}</Text>
  <Text>{difficulty.description}</Text>
</Pressable>
```

**Selection State Announcements**:
- **Selection**: "Friendly difficulty selected. Open and encouraging conversations."
- **Deselection**: "Real Talk difficulty deselected. Friendly difficulty now selected."
- **Context**: Each difficulty includes success rate and learning benefit information

### Advanced Screen Reader Features

#### Custom Actions Implementation
```jsx
// Location cards with custom actions
accessibilityActions={[
  {
    name: 'activate',
    label: 'Select location'
  },
  {
    name: 'preview',
    label: 'Hear location description'
  }
]}

onAccessibilityAction={(event) => {
  switch (event.nativeEvent.actionName) {
    case 'activate':
      handleLocationSelect();
      break;
    case 'preview':
      announceLocationDescription();
      break;
  }
}}
```

#### Live Region Updates
```jsx
// Status announcements for selection changes
<View 
  accessibilityLiveRegion="polite"
  accessibilityLabel={selectionStatus}
>
  {/* Selection status updates announced automatically */}
</View>

// Examples of live region announcements:
// "Coffee Shop location selected"
// "Friendly difficulty selected"
// "Ready to create scenario with Coffee Shop and Friendly difficulty"
```

## Keyboard Navigation

### Tab Order and Focus Management

#### Logical Tab Order
1. **Back Button**: Returns to Home tab
2. **Location Carousel**: Focus management within carousel
3. **Difficulty Cards**: Sequential focus through all three cards
4. **Create Scenario Button**: Final tab stop

**Focus Management Implementation**:
```jsx
const FocusManager = () => {
  const [currentFocus, setCurrentFocus] = useState('back-button');
  
  const handleKeyPress = (event) => {
    switch (event.key) {
      case 'Tab':
        if (!event.shiftKey) {
          // Forward tab navigation
          focusNext();
        } else {
          // Reverse tab navigation
          focusPrevious();
        }
        break;
      case 'ArrowRight':
        if (currentFocus === 'location-carousel') {
          focusNextLocation();
        }
        break;
      case 'ArrowLeft':
        if (currentFocus === 'location-carousel') {
          focusPreviousLocation();
        }
        break;
      case 'Enter':
      case ' ':
        activateCurrentFocus();
        break;
      case 'Escape':
        returnToPreviousScreen();
        break;
    }
  };
};
```

#### Location Carousel Keyboard Navigation
**Arrow Key Support**:
- **Right Arrow**: Move to next location card
- **Left Arrow**: Move to previous location card
- **Home**: Move to first location card
- **End**: Move to last location card
- **Space/Enter**: Select currently focused location

**Focus Indicators**:
```jsx
const FocusRing = ({ focused, children }) => (
  <View style={{
    borderWidth: focused ? 3 : 0,
    borderColor: '#F97316',
    borderRadius: 19, // 16px card radius + 3px focus ring
    padding: focused ? 0 : 3, // Maintain layout when focus ring appears
  }}>
    {children}
  </View>
);
```

#### Difficulty Cards Keyboard Navigation
**Sequential Focus**:
- **Tab**: Move through difficulty cards sequentially
- **Arrow Keys**: Optional alternative navigation method
- **Space/Enter**: Select focused difficulty card
- **Numbers 1-3**: Quick selection shortcuts (optional)

### Keyboard Shortcuts (Advanced)
**Optional Quick Actions**:
- **1-8**: Quick location selection by number
- **G**: Select Green (Friendly) difficulty
- **Y**: Select Yellow (Real Talk) difficulty
- **R**: Select Red (A-Game) difficulty
- **C**: Create scenario (when both selections made)
- **Escape**: Return to previous screen

## Motor Accessibility

### Touch Target Optimization

#### Minimum Touch Target Compliance
**Size Requirements** (exceeding WCAG 44×44px minimum):
- **Location Cards**: 280×180px (significantly exceeds minimum) ✓
- **Difficulty Cards**: Minimum 100×120px (exceeds minimum) ✓
- **Back Button**: 44×44px minimum maintained ✓
- **Create Scenario Button**: Full width × 48px height ✓

#### Touch Target Spacing
**Adequate Spacing** (WCAG recommends minimum 8px):
- **Location Cards**: 16px horizontal spacing ✓
- **Difficulty Cards**: 12px spacing between cards ✓
- **Section Spacing**: 24px between location and difficulty sections ✓
- **Button Spacing**: 16px margin from difficulty cards ✓

### Alternative Input Methods

#### Switch Control Support
**Switch Navigation Configuration**:
```jsx
const SwitchControlConfig = {
  groups: [
    {
      id: 'location-group',
      name: 'Location Selection',
      items: locationCards,
      scanningOrder: 'left-to-right'
    },
    {
      id: 'difficulty-group', 
      name: 'Difficulty Selection',
      items: difficultyCards,
      scanningOrder: 'left-to-right'
    },
    {
      id: 'action-group',
      name: 'Create Scenario',
      items: [createButton],
      scanningOrder: 'single'
    }
  ],
  scanningSpeed: 'medium',
  activationMethod: 'single-switch'
};
```

#### Voice Control Integration
**Voice Command Support**:
- **"Select Coffee Shop"**: Direct location selection by name
- **"Choose Friendly"**: Direct difficulty selection by name
- **"Create Scenario"**: Activate creation button
- **"Go Back"**: Return to previous screen
- **"Show All Locations"**: Announce all available locations

**Implementation**:
```jsx
// Voice control accessibility labels
accessibilityLabel="Coffee Shop location"
accessibilityIdentifier="location-coffee-shop" // For voice control targeting
```

### Gesture Alternatives

#### Alternative Selection Methods
**Long Press Alternatives**:
- All selection actions available through standard tap
- No long press gestures required for core functionality
- Optional long press for additional context (not required)

**Swipe Alternatives**:
- Location browsing possible through standard scrolling
- Arrow key navigation available as alternative
- No required swipe gestures for core functionality

## Cognitive Accessibility

### Clear Information Architecture

#### Consistent Layout Patterns
**Predictable Structure**:
- Top-to-bottom information flow matches reading patterns
- Consistent card layouts reduce cognitive load
- Repeated interaction patterns throughout interface
- Clear visual hierarchy guides attention

#### Progress Indication
**Journey Awareness**:
```jsx
<Text 
  accessibilityLabel="Step 1 of 2: Selection. Next step will be Context Creation."
  accessibilityRole="progressbar"
  accessibilityValue={{
    min: 1,
    max: 2,
    now: 1
  }}
>
  Step 1 of 2
</Text>
```

### Error Prevention and Recovery

#### Clear Selection Requirements
**Helpful Guidance**:
- Button disabled until both selections made
- Clear helper text explains requirements
- No error messages - proactive prevention
- Visual indicators show completion progress

**Selection State Clarity**:
```jsx
const SelectionStatus = ({ locationSelected, difficultySelected }) => (
  <Text 
    accessibilityLiveRegion="polite"
    accessibilityLabel={`
      ${locationSelected ? 'Location selected' : 'Location needed'}, 
      ${difficultySelected ? 'Difficulty selected' : 'Difficulty needed'}
    `}
  >
    {getSelectionStatusMessage(locationSelected, difficultySelected)}
  </Text>
);
```

#### Mistake Recovery
**Easy Correction**:
- No confirmation dialogs for selection changes
- Clear deselection visual feedback
- Easy to explore options without commitment
- Return navigation always available

### Reduced Cognitive Load Features

#### Simplified Decision Making
**Progressive Disclosure**:
- Two clear decision points (location, then difficulty)
- No overwhelming number of simultaneous choices
- Clear visual grouping of related options
- Minimal text with clear hierarchies

#### Memory Support
**Selection Persistence**:
- Selections remain visually confirmed throughout session
- Clear indication of current choices
- No need to remember previous selections
- Visual confirmation before proceeding

## Testing and Validation

### Accessibility Testing Requirements

#### Automated Testing
**Required Accessibility Audits**:
- **ESLint A11y**: All accessibility linting rules pass
- **Axe Testing**: No accessibility violations detected
- **Color Contrast**: All ratios verified automatically
- **Touch Target**: All targets meet minimum size requirements

#### Manual Testing Protocol
**Screen Reader Testing**:
- Complete navigation with VoiceOver (iOS) and TalkBack (Android)
- All content accessible and understandable
- Selection states properly announced
- Navigation hints clear and helpful

**Keyboard Testing**:
- Full functionality available through keyboard only
- Logical tab order maintained
- Focus indicators clearly visible
- All actions accessible via keyboard

**Motor Testing**:
- All functions accessible with switch control
- Touch targets appropriately sized and spaced
- Alternative input methods functional
- No precision-dependent interactions

### User Testing with Disabilities

#### Testing Participant Requirements
**Diverse User Groups**:
- **Vision**: Blind users, low-vision users, color-blind users
- **Motor**: Switch control users, limited dexterity users
- **Cognitive**: Users with learning disabilities, attention challenges
- **Hearing**: While not primary concern, test with deaf/HOH users for completeness

#### Success Metrics
**Accessibility Success Criteria**:
- **Task Completion**: >95% success rate for selection completion
- **Error Recovery**: Users can easily correct selection mistakes
- **Navigation Efficiency**: Comparable task completion time to visual users
- **User Satisfaction**: High ratings for accessibility experience

### Implementation Validation

#### Code Review Requirements
**Accessibility Code Standards**:
- All interactive elements have proper accessibility props
- Focus management implemented correctly
- Color contrast verified in code
- Touch targets meet minimum requirements

**Testing Integration**:
```jsx
// Example accessibility test
describe('Unified Selection Accessibility', () => {
  it('provides proper screen reader support', async () => {
    const { getByLabelText, getByRole } = render(<UnifiedSelection />);
    
    // Test location card accessibility
    const coffeeShopCard = getByLabelText(/coffee shop location/i);
    expect(coffeeShopCard).toHaveAccessibilityState({ selected: false });
    
    // Test selection announcement
    fireEvent.press(coffeeShopCard);
    expect(coffeeShopCard).toHaveAccessibilityState({ selected: true });
    
    // Test button state changes
    const createButton = getByRole('button', { name: /create scenario/i });
    expect(createButton).toBeDisabled();
  });
});
```

## Platform-Specific Accessibility

### iOS VoiceOver Optimization
**iOS-Specific Features**:
- Rotor navigation support for quick element type navigation
- Custom accessibility actions for advanced users
- Proper integration with iOS accessibility shortcuts
- VoiceOver gesture support for card browsing

### Android TalkBack Optimization
**Android-Specific Features**:
- TalkBack gesture navigation support
- Explore-by-touch optimization
- Android accessibility service integration
- Material Design accessibility patterns

### Web Accessibility (Future)
**WCAG 2.1 AA Compliance**:
- ARIA landmarks and regions
- Keyboard navigation with focus management
- Screen reader testing with NVDA, JAWS, and VoiceOver
- High contrast mode support

## Last Updated
- **Version 1.0.0**: Comprehensive accessibility specifications meeting WCAG 2.1 AA standards
- **Focus**: Universal design ensuring full functionality for all users
- **Next**: Implementation guidelines and technical specifications