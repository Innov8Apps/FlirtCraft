# Form Components

---
title: FlirtCraft Form Components
description: Input fields, selectors, and form elements for user preferences and onboarding
feature: onboarding, profile
last-updated: 2025-08-30
version: 2.0.0
related-files: 
  - ../style-guide.md
  - ../tokens/colors.md
  - ../tokens/typography.md
  - ../tokens/nativebase-theme.md
dependencies:
  - NativeBase Input, Select, Checkbox, FormControl components
  - NativeWind 4.1 utility classes
  - React Hook Form integration
status: approved
---

## Overview

Form components in FlirtCraft prioritize user comfort and accessibility during sensitive onboarding processes. All inputs emphasize clarity, error prevention, and psychological safety to reduce anxiety during preference setting.

## Component Specifications

### Text Input

#### Purpose
Primary text input for names, age verification, and open-ended responses.

#### Visual Specifications

**Default State:**
- **Height**: `48px` – Touch-friendly sizing prevents iOS zoom
- **Padding**: `12px 16px` – Comfortable text spacing
- **Border**: `2px solid #E5E7EB` (Neutral-200)
- **Border Radius**: `8px` – Subtle, clean corners
- **Background**: `#FFFFFF` (White)
- **Typography**: Body (16px/22px, 400 weight) – Prevents iOS zoom behavior
- **Placeholder**: Neutral-400 (`#9CA3AF`)

**States:**

*Focus State:*
- **Border**: `2px solid #F97316` (Primary)
- **Shadow**: `0 0 0 4px rgba(99, 102, 241, 0.1)` – Subtle focus ring
- **Background**: `#FFFFFF` maintained
- **Transition**: `200ms ease-out` border color change

*Error State:*
- **Border**: `2px solid #EF4444` (Error)
- **Background**: `#FEF2F2` (Red-50) – Very subtle error background
- **Error Text**: Displayed below input in Error color
- **Icon**: Small warning icon (16px) positioned right with 12px margin

*Success State:*
- **Border**: `2px solid #10B981` (Success)
- **Icon**: Checkmark icon (16px) positioned right
- **Background**: Remains white

*Disabled State:*
- **Background**: `#F9FAFB` (Neutral-50)
- **Border**: `1px solid #E5E7EB` (Neutral-200)
- **Text Color**: `#9CA3AF` (Neutral-400)
- **Opacity**: No additional opacity reduction

#### NativeBase Implementation
```jsx
import { Input, FormControl, Text } from 'native-base';

<FormControl isInvalid={hasError}>
  <FormControl.Label>
    <Text color="gray.700" fontWeight="medium" mb="2">Name</Text>
  </FormControl.Label>
  
  <Input
    variant="outline"
    size="lg"
    borderRadius="8"
    borderWidth="2"
    _focus={{
      borderColor: 'primary.500',
      bg: 'white'
    }}
    _invalid={{
      borderColor: 'error.300',
      bg: 'error.50'
    }}
    placeholder="Enter your name"
    fontSize="md"
    color="gray.900"
    placeholderTextColor="gray.400"
  />
  
  {hasError && (
    <FormControl.ErrorMessage>
      <Text color="error.500" fontSize="sm" mt="1">{errorMessage}</Text>
    </FormControl.ErrorMessage>
  )}
</FormControl>
```

#### NativeWind 4.1 Classes
```jsx
// Input container with dark mode support
className="h-12 px-4 border-2 border-gray-200 rounded-lg bg-white text-base 
           focus:border-primary focus:shadow-lg focus:shadow-primary/10
           invalid:border-error invalid:bg-error/5
           dark:bg-gray-800 dark:border-gray-600 dark:text-gray-50
           dark:focus:border-primary-light dark:invalid:border-error"

// Label classes
className="text-gray-700 font-medium mb-2 dark:text-gray-200"

// Error message classes
className="text-error text-sm mt-1 dark:text-error-light"
```

#### Accessibility Requirements
- **Label**: Always paired with descriptive label
- **ARIA**: `aria-required` for mandatory fields
- **Error Association**: `aria-describedby` links to error message
- **Placeholder**: Never as sole label, always supplementary
- **Keyboard**: Standard text input behavior

### Age Selector (Date Picker)

#### Purpose
Age verification input for legal compliance and preference matching.

#### Visual Specifications

**Layout:**
- **Three Separate Inputs**: Month, Day, Year in horizontal layout
- **Mobile**: Stacked layout with clear labels
- **Tablet+**: Side-by-side with equal spacing

*Month Selector:*
- **Type**: Dropdown/Select with month names
- **Options**: "January", "February", etc. (full names for clarity)
- **Default**: No selection, placeholder "Month"

*Day Selector:*
- **Type**: Dropdown/Select with numbers 1-31
- **Validation**: Dynamic based on selected month/year
- **Default**: No selection, placeholder "Day"

*Year Selector:*
- **Type**: Dropdown/Select with years
- **Range**: Current year - 80 to Current year - 18
- **Default**: No selection, placeholder "Year"

**Error Handling:**
- **Under 18**: "FlirtCraft is designed for adults 18 and older"
- **Invalid Date**: "Please enter a valid birth date"
- **Incomplete**: "Please complete your birth date"

#### NativeBase Implementation
```jsx
import { HStack, VStack, Text, Select } from 'native-base';

<HStack space={2} alignItems="flex-end">
  <VStack flex={1}>
    <Text fontSize="sm" color="gray.600">Month</Text>
    <Select placeholder="Month" size="lg" borderRadius="8">
      <Select.Item label="January" value="01" />
      <Select.Item label="February" value="02" />
      <Select.Item label="March" value="03" />
      {/* ... other months */}
    </Select>
  </VStack>
  
  <VStack flex={1}>
    <Text fontSize="sm" color="gray.600">Day</Text>
    <Select placeholder="Day" size="lg" borderRadius="8">
      <Select.Item label="1" value="01" />
      {/* ... other days */}
    </Select>
  </VStack>
  
  <VStack flex={1}>
    <Text fontSize="sm" color="gray.600">Year</Text>
    <Select placeholder="Year" size="lg" borderRadius="8">
      <Select.Item label="2006" value="2006" />
      {/* ... other years */}
    </Select>
  </VStack>
</HStack>
```

### Gender Selection (Radio Group)

#### Purpose
Gender identity selection for AI partner preferences and personalization.

#### Visual Specifications

**Layout Options:**
- **Card-based Selection**: Each option as a card with icon and label
- **List-based**: Vertical list with radio indicators

*Card Design (Recommended):*
- **Size**: Full-width mobile, 2-column tablet+
- **Height**: `64px` minimum
- **Border**: `2px solid #E5E7EB` (Neutral-200) default
- **Border Radius**: `12px`
- **Background**: `#FFFFFF` (White)
- **Padding**: `16px`
- **Icon**: 24px inclusive gender icons
- **Typography**: Body Medium (16px/22px, 500 weight)

**Selection States:**
- **Default**: Light border, white background
- **Hover**: `#F3F4F6` (Neutral-100) background
- **Selected**: `#F97316` (Primary) border, `#FFF7ED` (Indigo-50) background
- **Focus**: Primary color focus ring

**Options Provided:**
- "Male" with inclusive icon
- "Female" with inclusive icon  
- "Non-binary" with inclusive icon
- "Prefer not to say" with question mark icon

#### Accessibility Requirements
- **Radio Group**: Proper `role="radiogroup"` 
- **Labels**: Clear, descriptive labels
- **Keyboard**: Arrow key navigation between options
- **Screen Reader**: Announces selection state changes

### Preference Sliders (Age Range)

#### Purpose
Age range selection for AI practice partner preferences.

#### Visual Specifications

**Dual-Range Slider:**
- **Track Height**: `8px`
- **Track Color**: `#E5E7EB` (Neutral-200)
- **Active Track**: `#F97316` (Primary) between thumbs
- **Thumb Size**: `24px` diameter
- **Thumb Color**: `#F97316` (Primary) with white border
- **Thumb Shadow**: `0 2px 4px rgba(0, 0, 0, 0.1)`

**Value Display:**
- **Position**: Centered above slider
- **Typography**: Body Medium (16px/22px, 500 weight)
- **Format**: "Ages 23 - 28"
- **Real-time Update**: Values update as user drags

**Range Constraints:**
- **Minimum Range**: 3-year spread (e.g., 25-28)
- **Maximum Range**: 20-year spread
- **Default**: User's age ±5 years
- **Boundaries**: 18 minimum, 65 maximum

#### NativeBase Implementation
```jsx
import { Box, Text, Slider } from 'native-base';

<Box>
  <Text textAlign="center" fontSize="md" fontWeight="medium" mb="4">
    Ages {minAge} - {maxAge}
  </Text>
  <Slider
    defaultValue={userAge}
    minValue={18}
    maxValue={65}
    step={1}
    colorScheme="primary"
    size="lg"
  >
    <Slider.Track>
      <Slider.FilledTrack />
    </Slider.Track>
    <Slider.Thumb />
  </Slider>
  
  {/* For dual range, you would use two sliders or a custom component */}
  <Text fontSize="sm" color="gray.500" textAlign="center" mt="2">
    Drag to adjust preferred age range
  </Text>
</Box>
```

### Multi-Select Checkboxes (Skill Goals)

#### Purpose
Multiple skill goal selection during onboarding for personalized training.

#### Visual Specifications

**Checkbox Cards:**
- **Layout**: Grid - 1 column mobile, 2 columns tablet+
- **Size**: Full-width with 16px spacing between
- **Height**: Minimum `72px` for touch accessibility
- **Border**: `2px solid #E5E7EB` (Neutral-200)
- **Border Radius**: `12px`
- **Padding**: `16px`

*Card Content:*
- **Checkbox**: 20px custom checkbox (left side)
- **Title**: Body Medium (16px/22px, 500 weight)
- **Description**: Body Small (14px/20px, 400 weight) in Neutral-500
- **Icon**: 24px skill-related icon (right side)

**Checkbox States:**
- **Unchecked**: Empty square with border
- **Checked**: Primary background with white checkmark
- **Indeterminate**: Not used in this context
- **Focus**: Primary focus ring around entire card

**Selection Feedback:**
- **Unchecked → Checked**: Checkmark animation (200ms ease-out)
- **Card Background**: Subtle Primary color tint when selected
- **Counter**: "3 of 7 selected" progress indicator

#### Skill Goal Options
1. **Starting conversations naturally**
   - Icon: Chat bubble
   - Description: "Learn natural, confident conversation openers"

2. **Maintaining conversation flow** 
   - Icon: Arrows in cycle
   - Description: "Keep discussions engaging and reciprocal"

3. **Building confidence and charm**
   - Icon: Star/sparkle
   - Description: "Develop your natural charisma and self-assurance"

4. **Flirting appropriately**
   - Icon: Heart
   - Description: "Express romantic interest with respect and skill"

5. **Reading social cues and body language**
   - Icon: Eye
   - Description: "Understand non-verbal communication signals"

6. **Handling rejection gracefully** (Phase 2)
   - Icon: Shield
   - Description: "Maintain confidence when interactions don't go as planned"

7. **Telling engaging stories** (Phase 2)
   - Icon: Book
   - Description: "Share experiences that captivate and connect"

### Validation & Error Handling

#### Error Message Design
**Visual Specifications:**
- **Position**: Below input with 8px margin
- **Typography**: Body Small (14px/20px, 400 weight)
- **Color**: `#EF4444` (Error)
- **Icon**: Small warning icon (16px) with 4px margin to text
- **Animation**: Fade in over 200ms when error appears

#### Success Message Design
**Visual Specifications:**
- **Position**: Below input with 8px margin
- **Typography**: Body Small (14px/20px, 400 weight)  
- **Color**: `#10B981` (Success)
- **Icon**: Small checkmark icon (16px) with 4px margin to text
- **Animation**: Fade in with subtle bounce effect

#### Validation Rules

*Text Input:*
- **Name**: 1-50 characters, no special characters except spaces, hyphens, apostrophes
- **Required**: Cannot be empty after focus/blur
- **Real-time**: Validate on blur, not keystroke

*Age Verification:*
- **Required**: All three fields must be completed
- **18+ Validation**: Must be 18 or older on current date
- **Realistic Range**: Maximum age 80 for practical AI conversation context

*Preferences:*
- **Age Range**: Minimum 3-year range, maximum 20-year range
- **Skill Goals**: Minimum 1 selection, maximum all 7
- **Gender**: Optional but recommended for better AI personalization

## Usage Guidelines

### When to Use Each Component

**Text Input:**
- User names, display names
- Open-ended responses
- Simple data entry

**Age Selector:**
- Legal age verification only
- Preference settings where age matters

**Gender Selection:**
- Identity questions requiring inclusive options
- Preference settings for AI partners

**Sliders:**
- Range selections (age, distance, etc.)
- When visual representation helps understanding

**Multi-Select Checkboxes:**
- When multiple simultaneous selections are beneficial
- Goal-setting and preference configuration

### What NOT to Do

- Never use dropdowns for binary choices
- Don't make every field required - respect privacy
- Avoid placeholder text as the only label
- Never validate on every keystroke for text inputs
- Don't use color alone to indicate validation state

## Implementation Notes

### Performance Considerations
- **Lazy Loading**: Complex selectors load options on demand
- **Debounced Validation**: 300ms delay on real-time validation
- **Efficient Re-renders**: Optimize React state updates for smooth interactions

### Platform-Specific Notes

**iOS:**
- Date picker uses native iOS wheel interface when possible
- Haptic feedback on successful form completion
- Respects iOS Dynamic Type for text scaling

**Android:**
- Material Design date/time pickers as fallback
- Follows Android accessibility guidelines for touch targets
- Supports TalkBack screen reader

### Testing Requirements

**Accessibility Testing:**
- Screen reader compatibility for all form elements
- Keyboard navigation through all components
- High contrast mode support
- Text scaling up to 200%

**Usability Testing:**
- Error state clarity and helpfulness
- Form completion success rates
- Time-to-completion for onboarding forms
- User comprehension of preference options

---

## Related Documentation
- [Button Components](./buttons.md) - Form submission buttons
- [Color Tokens](../tokens/colors.md) - Form color specifications
- [Typography Tokens](../tokens/typography.md) - Form text styling
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Form accessibility requirements

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete and ready for implementation*