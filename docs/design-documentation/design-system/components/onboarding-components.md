# Onboarding Components

## Overview
This document defines the design specifications for onboarding components in the FlirtCraft application.

## Color Palette
- **Primary Orange**: `#FF6B35` / `#FF7F50` (Coral)
- **Secondary Gray**: `#E5E5E5`
- **Background**: `#FFFFFF` / `#FAFAFA`
- **Text Primary**: `#1A1A1A`
- **Text Secondary**: `#6B7280`
- **Success Green**: `#4CAF50` / `#2E7D32` / `#E8F5E8`
- **Error Red**: `#EF4444`

## Components

### 1. OnboardingHeader
A unified header component used across all onboarding screens.

#### Structure
```typescript
interface OnboardingHeaderProps {
  currentStep: number;
  totalSteps: number;
  onBack: () => void;
  showBackButton?: boolean;
}
```

#### Visual Specifications
- **Container**: 
  - Background: White (#FFFFFF)
  - Padding: 20px horizontal, 10px top, 20px bottom
  - SafeArea: Yes

- **Back Button**:
  - Position: Absolute, left 20px, top 10px
  - Text Color: #FF6B35
  - Font Size: 16px
  - Font Weight: 500
  - Icon: Chevron-back (Ionicons), size 20px
  - Interaction: TouchableOpacity with opacity 0.8 on press

- **Step Indicator**:
  - Position: Center, below back button (35px padding top)
  - Text: "Step X of Y"
  - Font Size: 18px
  - Font Weight: 600
  - Color: #FF6B35

### 2. StepIndicator
Progress bar showing the current step in the onboarding flow.

#### Visual Specifications
- **Text**:
  - Format: "Step {current} of {total}"
  - Font Size: 18px
  - Font Weight: 600
  - Color: #FF6B35
  - Margin Bottom: 12px

- **Progress Bar**:
  - Width: 100% of container
  - Height: 8px
  - Background Color: #E5E5E5
  - Border Radius: 4px
  - Fill Color: #FF6B35
  - Animation: Smooth width transition

### 3. BackButton
Standalone back navigation button.

#### Visual Specifications
- **Container**:
  - Flex Direction: Row
  - Align Items: Center
  - Padding: 8px vertical

- **Icon**:
  - Type: Ionicons "chevron-back"
  - Size: 20px
  - Color: #FF6B35

- **Text**:
  - Default: "Back"
  - Font Size: 16px
  - Color: #FF6B35
  - Margin Left: 4px
  - Font Weight: 500

### 4. WheelPicker (Date Selection)
Custom wheel picker for date selection in age verification.

#### Visual Specifications
- **Container**:
  - Height: 180px
  - Width: 100%

- **Selection Highlight**:
  - Background: #FF7F50
  - Border Radius: 12px
  - Height: 60px
  - Position: Center of picker

- **Items**:
  - Height: 60px per item
  - Selected: Bold font weight, white color
  - Unselected: Medium font weight, gray.600 color
  - Font Size: Large (lg)

- **Label**:
  - Font Size: Small (sm)
  - Color: gray.500
  - Font Weight: Medium
  - Position: Above picker

## Usage Guidelines

### Navigation Flow
1. All onboarding screens should use the `OnboardingHeader` component
2. The back button should check `router.canGoBack()` before navigation
3. Fallback to welcome screen if no previous route exists

### Accessibility
- All interactive elements must have a minimum touch target of 44x44px
- Color contrast must meet WCAG AA standards
- Progress indicators should have appropriate ARIA labels

### Animation
- Use `react-native-reanimated` for smooth transitions
- Fade in delays: 200ms for primary content, 400ms for secondary, 600ms for tertiary
- Slide animations should use `SlideInUp` with appropriate delays

## Implementation Example

```tsx
import OnboardingHeader from '../../components/onboarding/OnboardingHeader';

export default function OnboardingScreen() {
  const { progress } = useOnboardingStore();
  
  const handleBack = () => {
    if (router.canGoBack()) {
      previousStep();
      router.back();
    } else {
      router.replace('/onboarding/welcome');
    }
  };

  return (
    <View style={styles.container}>
      <OnboardingHeader 
        currentStep={progress.currentStep + 1}
        totalSteps={progress.totalSteps}
        onBack={handleBack}
      />
      {/* Screen content */}
    </View>
  );
}
```

## File Locations
- Components: `/FlirtCraft-frontend/components/onboarding/`
- Screens: `/FlirtCraft-frontend/app/onboarding/`
- Store: `/FlirtCraft-frontend/stores/onboardingStore.ts`