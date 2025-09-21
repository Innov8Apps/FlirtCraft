# iOS Platform Adaptations

---
title: FlirtCraft iOS Design Guidelines
description: iOS Human Interface Guidelines compliance and native iOS user experience patterns
platform: iOS
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../../accessibility/guidelines.md
dependencies:
  - iOS Human Interface Guidelines
  - SF Symbols (where appropriate)
status: approved
---

## Overview

FlirtCraft on iOS provides a native, familiar experience that feels at home on Apple devices while maintaining the app's core identity and functionality. These guidelines ensure compliance with iOS Human Interface Guidelines while preserving FlirtCraft's unique design language.

## iOS Design Principles

### Core iOS Alignment

**Clarity:**
- Clear visual hierarchy using iOS-standard typography scaling
- High contrast ratios that exceed iOS requirements
- Clean, uncluttered interface design
- Purpose-driven interface elements

**Deference:**
- Content takes precedence over UI chrome
- Meaningful imagery and branding support content
- Subtle interface elements don't compete with content
- Edge-to-edge design where appropriate

**Depth:**
- Strategic use of layers and motion
- iOS-standard shadows and blur effects
- Meaningful transitions that aid navigation
- Respectful use of system gestures and affordances

## Navigation and Structure

### iOS Navigation Patterns

**Stack Navigation Implementation:**
```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

const IOSStackNavigator = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: '#FFFFFF',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 0.5 },
        shadowOpacity: 0.1,
        shadowRadius: 0,
      },
      headerTitleStyle: {
        fontSize: 17,
        fontWeight: '600',
      },
      headerBackTitleVisible: false,
      gestureEnabled: true,
      gestureDirection: 'horizontal',
    }}
  >
    {/* Screen definitions */}
  </Stack.Navigator>
);
```

**Tab Bar Implementation:**
```jsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

const IOSTabNavigator = () => (
  <Tab.Navigator
    screenOptions={{
      tabBarStyle: {
        backgroundColor: '#FFFFFF',
        borderTopWidth: 0.5,
        borderTopColor: '#E5E7EB',
        height: 84, // Including safe area
        paddingTop: 8,
      },
      tabBarActiveTintColor: '#F97316',
      tabBarInactiveTintColor: '#9CA3AF',
      tabBarLabelStyle: {
        fontSize: 10,
        fontWeight: '500',
        marginTop: -2,
      },
    }}
  >
    {/* Tab screens */}
  </Tab.Navigator>
);
```

### iOS Header Patterns

**Standard Header:**
- Navigation title in center using iOS system font weight (600)
- Back button with iOS chevron (no text for cleaner appearance)
- Right-aligned action buttons using SF Symbols where appropriate
- Blur effect on scroll for immersive content

**Large Title Header (where appropriate):**
```jsx
<Stack.Screen
  name="Home"
  component={HomeScreen}
  options={{
    headerLargeTitle: true,
    headerLargeTitleStyle: {
      fontSize: 34,
      fontWeight: '700',
    },
    headerSearchBarOptions: {
      placeholder: 'Search scenarios...',
    },
  }}
/>
```

### Modal Presentations

**iOS Modal Behavior:**
- Sheet presentation style for contextual actions
- Pull-to-dismiss gesture support
- Appropriate modal sizes (medium, large, full-screen)
- Navigation cancel/done button patterns

```jsx
const IOSModal = ({ visible, onClose, children }) => (
  <Modal
    animationType="slide"
    presentationStyle="pageSheet"
    visible={visible}
    onRequestClose={onClose}
  >
    <SafeAreaView style={styles.modalContainer}>
      <View style={styles.modalHeader}>
        <TouchableOpacity onPress={onClose}>
          <Text style={styles.cancelButton}>Cancel</Text>
        </TouchableOpacity>
        <Text style={styles.modalTitle}>Modal Title</Text>
        <TouchableOpacity onPress={onSave}>
          <Text style={styles.doneButton}>Done</Text>
        </TouchableOpacity>
      </View>
      {children}
    </SafeAreaView>
  </Modal>
);
```

## iOS-Specific Components

### iOS Button Styles

**Primary Button (iOS Style):**
```jsx
const IOSPrimaryButton = ({ title, onPress }) => (
  <TouchableOpacity
    style={[
      styles.iosPrimaryButton,
      {
        backgroundColor: '#F97316',
        borderRadius: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.2,
        shadowRadius: 2,
      }
    ]}
    onPress={onPress}
  >
    <Text style={styles.iosPrimaryButtonText}>
      {title}
    </Text>
  </TouchableOpacity>
);
```

**iOS System Button (Secondary):**
- Uses iOS system blue (`#007AFF`) for secondary actions
- System font weights and sizing
- Appropriate touch targets (minimum 44pt)

### iOS Form Elements

**Text Input (iOS Style):**
```jsx
const IOSTextInput = ({ placeholder, value, onChangeText }) => (
  <TextInput
    style={[
      styles.iosTextInput,
      {
        borderWidth: 1,
        borderColor: '#E5E7EB',
        borderRadius: 8,
        fontSize: 16, // Prevents zoom on iOS
        paddingHorizontal: 12,
        paddingVertical: 12,
        backgroundColor: '#FFFFFF',
      }
    ]}
    placeholder={placeholder}
    value={value}
    onChangeText={onChangeText}
    placeholderTextColor="#9CA3AF"
    autoCapitalize="none"
    autoCorrect={false}
  />
);
```

**iOS Picker/Selector:**
- Uses iOS-native picker wheels where appropriate
- Action sheet presentation for simple choices
- Inline editing for complex selections

### iOS List Patterns

**iOS List Implementation:**
```jsx
const IOSList = ({ data, renderItem }) => (
  <FlatList
    data={data}
    renderItem={renderItem}
    style={styles.iosList}
    contentInsetAdjustmentBehavior="automatic"
    showsVerticalScrollIndicator={true}
    bounces={true}
    ItemSeparatorComponent={() => (
      <View style={styles.iosListSeparator} />
    )}
  />
);
```

**iOS Section List:**
- Grouped table view style for settings and categories
- Section headers with iOS-standard typography
- Proper section separators and insets

## iOS Gestures and Interactions

### Native iOS Gestures

**Swipe Back Navigation:**
```jsx
// Enabled by default in React Navigation native stack
const stackOptions = {
  gestureEnabled: true,
  gestureDirection: 'horizontal',
  gestureResponseDistance: {
    horizontal: 50,
    vertical: 135,
  },
};
```

**Pull-to-Refresh:**
```jsx
import { RefreshControl } from 'react-native';

const IOSRefreshableContent = ({ onRefresh, refreshing, children }) => (
  <ScrollView
    refreshControl={
      <RefreshControl
        refreshing={refreshing}
        onRefresh={onRefresh}
        tintColor="#F97316"
        title="Pull to refresh..."
        titleColor="#6B7280"
      />
    }
  >
    {children}
  </ScrollView>
);
```

**Long Press Context Menus (iOS 13+):**
```jsx
import { MenuView } from '@react-native-menu/menu';

const IOSContextMenu = ({ children, actions }) => (
  <MenuView
    title="Options"
    actions={actions}
    shouldOpenOnLongPress={true}
  >
    {children}
  </MenuView>
);
```

### Haptic Feedback

**iOS Haptic Implementation:**
```jsx
import { HapticFeedback } from 'react-native';

// Success feedback
const playSuccessHaptic = () => {
  HapticFeedback.notificationAsync(
    HapticFeedback.NotificationFeedbackType.Success
  );
};

// Selection feedback
const playSelectionHaptic = () => {
  HapticFeedback.selectionAsync();
};

// Impact feedback
const playImpactHaptic = (style = 'light') => {
  HapticFeedback.impactAsync(
    HapticFeedback.ImpactFeedbackStyle[style]
  );
};
```

**Haptic Usage Guidelines:**
- Light impact for button presses
- Medium impact for significant actions
- Heavy impact for major state changes
- Notification feedback for success/error states
- Selection feedback for picker changes

## iOS Accessibility Integration

### VoiceOver Optimization

**Accessibility Labels:**
```jsx
const IOSAccessibleButton = ({ title, onPress, accessibilityHint }) => (
  <TouchableOpacity
    onPress={onPress}
    accessibilityRole="button"
    accessibilityLabel={title}
    accessibilityHint={accessibilityHint}
    accessibilityTraits={['button']}
  >
    <Text>{title}</Text>
  </TouchableOpacity>
);
```

**Screen Reader Navigation:**
- Proper heading hierarchy using `accessibilityRole="header"`
- Landmark regions for major sections
- Live regions for dynamic content updates
- Focus management for modal presentations

### Dynamic Type Support

**Typography Scaling:**
```jsx
import { useAccessibilityInfo } from 'react-native';

const IOSScalableText = ({ children, style }) => {
  const { fontScale } = useAccessibilityInfo();
  
  return (
    <Text 
      style={[
        style,
        {
          fontSize: style.fontSize * Math.min(fontScale, 2.0), // Cap at 200%
        }
      ]}
      maxFontSizeMultiplier={2.0}
    >
      {children}
    </Text>
  );
};
```

**Layout Adaptation:**
- Flexible layouts that adapt to larger text sizes
- Minimum touch target enforcement at all scales
- Content prioritization for space-constrained scenarios

### iOS Accessibility Features

**Reduce Motion Support:**
```jsx
import { AccessibilityInfo } from 'react-native';

const useReducedMotion = () => {
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
    
    const subscription = AccessibilityInfo.addEventListener(
      'reduceMotionChanged',
      setReduceMotion
    );

    return () => subscription?.remove();
  }, []);

  return reduceMotion;
};
```

**High Contrast Mode:**
- Automatic adaptation to iOS high contrast settings
- Enhanced border definition in high contrast
- Simplified visual elements when needed

## iOS System Integration

### Siri Shortcuts Integration

**Shortcut Donation:**
```jsx
import { donate } from 'react-native-siri-shortcut';

const donateConversationShortcut = async () => {
  const shortcut = {
    activityType: 'com.flirtcraft.startConversation',
    title: 'Start Practice Conversation',
    userInfo: {},
    isEligibleForSearch: true,
    isEligibleForPrediction: true,
  };

  try {
    await donate(shortcut);
  } catch (error) {
    console.error('Failed to donate shortcut:', error);
  }
};
```

**Voice Shortcuts:**
- "Start FlirtCraft practice session"
- "Check my FlirtCraft progress"
- "View my conversation streak"

### iOS Share Sheet Integration

**Share Sheet Implementation:**
```jsx
import { Share } from 'react-native';

const shareProgress = async (progressData) => {
  try {
    await Share.share({
      message: `I just completed my ${progressData.totalConversations}th practice conversation on FlirtCraft!`,
      url: 'https://flirtcraft.app/share', // Deep link
    });
  } catch (error) {
    console.error('Share failed:', error);
  }
};
```

### Spotlight Search Integration

**Searchable Content:**
```jsx
import { SpotlightSearch } from 'react-native-spotlight-search';

const indexConversationHistory = async (conversations) => {
  const searchableItems = conversations.map(conversation => ({
    title: `${conversation.location} Conversation`,
    contentDescription: `Practice conversation at ${conversation.location} with ${conversation.difficulty} difficulty`,
    uniqueIdentifier: conversation.id,
    thumbnailData: conversation.imageData,
  }));

  try {
    await SpotlightSearch.indexItems(searchableItems);
  } catch (error) {
    console.error('Spotlight indexing failed:', error);
  }
};
```

## iOS Performance Optimization

### Memory Management

**iOS-Specific Optimizations:**
- Proper image memory management
- Background task completion
- Memory warnings handling
- Efficient view controller lifecycle

```jsx
import { AppState } from 'react-native';

const IOSMemoryManager = () => {
  useEffect(() => {
    const handleMemoryWarning = () => {
      // Clear non-essential caches
      // Reduce memory usage
      // Notify user if needed
    };

    const memoryWarningListener = DeviceEventEmitter.addListener(
      'memoryWarning',
      handleMemoryWarning
    );

    return () => memoryWarningListener.remove();
  }, []);
};
```

### Background Processing

**iOS Background Modes:**
- Background App Refresh for conversation sync
- Silent push notifications for system updates
- Background processing for analytics

```jsx
import { BackgroundTask } from 'react-native-background-task';

const syncDataInBackground = async () => {
  BackgroundTask.start();
  
  try {
    // Perform background sync
    await syncConversationData();
  } finally {
    BackgroundTask.stop();
  }
};
```

## iOS-Specific UI Patterns

### Safe Area Handling

**Safe Area Implementation:**
```jsx
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

const IOSSafeLayout = ({ children }) => (
  <SafeAreaProvider>
    <SafeAreaView style={styles.safeContainer}>
      {children}
    </SafeAreaView>
  </SafeAreaProvider>
);
```

**Dynamic Island Considerations:**
- Content padding around dynamic island
- Interactive elements positioning
- Status bar content coordination

### iOS Keyboard Behavior

**Keyboard Avoidance:**
```jsx
import { KeyboardAvoidingView } from 'react-native';

const IOSKeyboardLayout = ({ children }) => (
  <KeyboardAvoidingView 
    behavior="padding"
    style={styles.keyboardContainer}
    keyboardVerticalOffset={88} // Header + tab bar height
  >
    {children}
  </KeyboardAvoidingView>
);
```

**Input Accessory View:**
```jsx
const IOSInputAccessory = () => (
  <InputAccessoryView>
    <View style={styles.accessoryToolbar}>
      <TouchableOpacity onPress={dismissKeyboard}>
        <Text style={styles.doneButton}>Done</Text>
      </TouchableOpacity>
    </View>
  </InputAccessoryView>
);
```

## App Store Optimization

### iOS App Store Requirements

**App Store Guidelines Compliance:**
- Human Interface Guidelines adherence
- Content and functionality requirements
- Privacy policy and data handling disclosure
- Age rating accuracy and appropriateness

**iOS Assets Required:**
- App icon sets (all required sizes)
- Launch screen storyboard
- Screenshots for all supported devices
- App preview videos (recommended)

### iOS Metadata Optimization

**App Store Connect Optimization:**
- Keyword-optimized app title and subtitle
- Compelling app description with key features
- Regular app updates with meaningful release notes
- Appropriate category and subcategory selection

## Testing and Quality Assurance

### iOS Device Testing

**Device Coverage:**
- iPhone SE (3rd generation) - minimum screen size
- iPhone 14/15 series - current standard devices
- iPhone 14/15 Plus - larger standard screens
- iPhone 14/15 Pro Max - largest screens
- iPad (9th generation) - minimum iPad support
- iPad Pro - maximum iPad capabilities

**iOS Version Support:**
- iOS 14.0 minimum (covers 95%+ of active devices)
- iOS 17+ optimizations and features
- Graceful degradation for older iOS versions
- Regular testing on latest iOS beta versions

### iOS-Specific Testing

**Functionality Testing:**
- VoiceOver navigation and usability
- Dynamic Type scaling across all text sizes
- Haptic feedback appropriateness and timing
- Gesture navigation and system gesture conflicts

**Performance Testing:**
- Memory usage across different devices
- Battery impact measurement
- Launch time optimization
- Background processing efficiency

---

## Related Documentation

- [Android Adaptations](./android.md) - Android-specific design patterns
- [Component Library](../components/) - iOS component implementations
- [Accessibility Guidelines](../../accessibility/guidelines.md) - iOS accessibility requirements
- [Style Guide](../style-guide.md) - Core design system foundations

## External References

- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
- [iOS Accessibility](https://developer.apple.com/accessibility/)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete iOS adaptation guidelines ready for implementation*