# Android Platform Adaptations

---
title: FlirtCraft Android Design Guidelines
description: Material Design 3 integration and native Android user experience patterns
platform: Android
last-updated: 2025-08-23
version: 1.0.0
related-files: 
  - ../style-guide.md
  - ../../accessibility/guidelines.md
dependencies:
  - Material Design 3 specifications
  - Android Design Guidelines
status: approved
---

## Overview

FlirtCraft on Android provides a native Material Design experience while maintaining the app's core brand identity. These guidelines ensure compliance with Material Design 3 principles and Android platform conventions while preserving FlirtCraft's unique user experience.

## Material Design 3 Integration

### Core Material Principles

**Material as Metaphor:**
- Surfaces and shadows that feel familiar and intuitive
- Realistic lighting and depth cues
- Meaningful motion that guides user understanding
- Consistent material properties throughout the app

**Bold, Graphic, Intentional:**
- Typography that creates clear hierarchy
- Strategic use of color for emphasis and branding
- Iconography that communicates clearly
- Generous whitespace for content focus

**Motion Provides Meaning:**
- Choreographed motion that guides attention
- Meaningful transitions between states
- Performance-optimized animations
- Respectful use of system gestures

### Material You Integration

**Dynamic Color Support:**
```jsx
import { useColorScheme } from 'react-native';
import { MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

const MaterialTheme = () => {
  const colorScheme = useColorScheme();
  const theme = colorScheme === 'dark' ? MD3DarkTheme : MD3LightTheme;
  
  return {
    ...theme,
    colors: {
      ...theme.colors,
      primary: '#F97316', // FlirtCraft primary
      secondary: '#E65100', // FlirtCraft secondary
      tertiary: '#10B981', // FlirtCraft success
    }
  };
};
```

**Adaptive Layouts:**
- Responsive design for different screen sizes
- Foldable device support considerations
- Tablet and large screen optimizations
- Multi-window mode compatibility

## Android Navigation Patterns

### Material Navigation Implementation

**Bottom Navigation Bar:**
```jsx
import { BottomNavigation } from 'react-native-paper';

const AndroidBottomNav = ({ navigationState, onIndexChange, renderScene }) => (
  <BottomNavigation
    navigationState={navigationState}
    onIndexChange={onIndexChange}
    renderScene={renderScene}
    barStyle={{
      backgroundColor: '#FFFFFF',
      elevation: 8,
    }}
    activeColor="#F97316"
    inactiveColor="#9CA3AF"
    labeled={true}
    shifting={false}
  />
);
```

**Navigation Drawer (Secondary Navigation):**
```jsx
import { Drawer } from 'react-native-paper';

const AndroidDrawer = ({ navigation, route }) => (
  <Drawer.Section title="Main">
    <Drawer.Item
      label="Home"
      icon="home"
      active={route.name === 'Home'}
      onPress={() => navigation.navigate('Home')}
    />
    <Drawer.Item
      label="Progress"
      icon="chart-line"
      active={route.name === 'Progress'}
      onPress={() => navigation.navigate('Progress')}
    />
  </Drawer.Section>
);
```

### Android System Navigation

**Hardware Back Button Handling:**
```jsx
import { BackHandler } from 'react-native';

const AndroidBackHandler = ({ onBackPress }) => {
  useEffect(() => {
    const backAction = () => {
      if (onBackPress) {
        onBackPress();
        return true; // Prevent default behavior
      }
      return false; // Use default behavior
    };

    const backHandler = BackHandler.addEventListener(
      'hardwareBackPress',
      backAction
    );

    return () => backHandler.remove();
  }, [onBackPress]);
};
```

**Gesture Navigation Support:**
```jsx
// Edge-to-edge support for gesture navigation
const AndroidEdgeToEdge = ({ children }) => (
  <View style={{
    flex: 1,
    paddingTop: StatusBar.currentHeight || 0,
  }}>
    <StatusBar
      barStyle="dark-content"
      backgroundColor="transparent"
      translucent={true}
    />
    {children}
  </View>
);
```

## Material Design Components

### Material Buttons

**Material Primary Button:**
```jsx
import { Button } from 'react-native-paper';

const MaterialPrimaryButton = ({ title, onPress, disabled }) => (
  <Button
    mode="contained"
    onPress={onPress}
    disabled={disabled}
    buttonColor="#F97316"
    textColor="#FFFFFF"
    rippleColor="rgba(255, 255, 255, 0.2)"
    style={{
      borderRadius: 20,
      elevation: 2,
    }}
    contentStyle={{
      paddingVertical: 4,
    }}
    labelStyle={{
      fontSize: 16,
      fontWeight: '500',
      letterSpacing: 0.1,
    }}
  >
    {title}
  </Button>
);
```

**Material Outlined Button:**
```jsx
const MaterialOutlinedButton = ({ title, onPress }) => (
  <Button
    mode="outlined"
    onPress={onPress}
    textColor="#F97316"
    rippleColor="rgba(99, 102, 241, 0.1)"
    style={{
      borderRadius: 20,
      borderColor: '#F97316',
      borderWidth: 1,
    }}
  >
    {title}
  </Button>
);
```

**Floating Action Button:**
```jsx
import { FAB } from 'react-native-paper';

const MaterialFAB = ({ onPress, icon = "plus" }) => (
  <FAB
    icon={icon}
    onPress={onPress}
    style={{
      position: 'absolute',
      margin: 16,
      right: 0,
      bottom: 0,
      backgroundColor: '#F97316',
    }}
    color="#FFFFFF"
  />
);
```

### Material Form Elements

**Material Text Input:**
```jsx
import { TextInput } from 'react-native-paper';

const MaterialTextInput = ({ label, value, onChangeText, ...props }) => (
  <TextInput
    label={label}
    value={value}
    onChangeText={onChangeText}
    mode="outlined"
    outlineColor="#E5E7EB"
    activeOutlineColor="#F97316"
    textColor="#1F2937"
    style={{
      backgroundColor: '#FFFFFF',
      marginVertical: 4,
    }}
    contentStyle={{
      fontSize: 16,
    }}
    {...props}
  />
);
```

**Material Chip Selection:**
```jsx
import { Chip } from 'react-native-paper';

const MaterialChipGroup = ({ options, selected, onSelect }) => (
  <View style={styles.chipContainer}>
    {options.map((option) => (
      <Chip
        key={option.value}
        selected={selected.includes(option.value)}
        onPress={() => onSelect(option.value)}
        style={{
          margin: 4,
          backgroundColor: selected.includes(option.value) 
            ? '#F97316' 
            : '#F3F4F6'
        }}
        textStyle={{
          color: selected.includes(option.value) 
            ? '#FFFFFF' 
            : '#374151'
        }}
      >
        {option.label}
      </Chip>
    ))}
  </View>
);
```

### Material Cards

**Material Card Implementation:**
```jsx
import { Card, Title, Paragraph } from 'react-native-paper';

const MaterialCard = ({ title, description, onPress, children }) => (
  <Card
    style={{
      margin: 8,
      elevation: 2,
      borderRadius: 12,
    }}
    onPress={onPress}
  >
    <Card.Content>
      {title && <Title>{title}</Title>}
      {description && <Paragraph>{description}</Paragraph>}
      {children}
    </Card.Content>
  </Card>
);
```

**Elevated Card (Material 3):**
```jsx
const MaterialElevatedCard = ({ elevation = 1, children, ...props }) => (
  <Card
    style={{
      elevation: elevation,
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: elevation,
      },
      shadowOpacity: 0.1,
      shadowRadius: elevation * 2,
      borderRadius: 12,
      backgroundColor: '#FFFFFF',
    }}
    {...props}
  >
    {children}
  </Card>
);
```

## Android-Specific Interactions

### Material Touch Feedback

**Ripple Effects:**
```jsx
import { TouchableRipple } from 'react-native-paper';

const MaterialTouchable = ({ onPress, children, rippleColor }) => (
  <TouchableRipple
    onPress={onPress}
    rippleColor={rippleColor || 'rgba(99, 102, 241, 0.2)'}
    borderless={false}
    style={{
      borderRadius: 8,
      overflow: 'hidden',
    }}
  >
    {children}
  </TouchableRipple>
);
```

**Long Press Context Actions:**
```jsx
const MaterialLongPress = ({ onLongPress, children }) => (
  <TouchableRipple
    onLongPress={onLongPress}
    delayLongPress={500}
    rippleColor="rgba(0, 0, 0, 0.1)"
  >
    {children}
  </TouchableRipple>
);
```

### Android Haptic Feedback

**Material Haptics Implementation:**
```jsx
import { Vibration } from 'react-native';

const MaterialHaptics = {
  light: () => Vibration.vibrate(10),
  medium: () => Vibration.vibrate(20),
  heavy: () => Vibration.vibrate([0, 30]),
  success: () => Vibration.vibrate([0, 10, 100, 10]),
  error: () => Vibration.vibrate([0, 20, 100, 20, 100, 20]),
};

// Usage example
const handleButtonPress = () => {
  MaterialHaptics.light();
  onPress();
};
```

## Android System Integration

### Adaptive Icons

**Adaptive Icon Support:**
```xml
<!-- android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml -->
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
  <background android:drawable="@color/ic_launcher_background"/>
  <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
```

**Dynamic Icon Colors:**
- Themed app icons for Android 13+
- Monochrome icon variants
- Adaptive icon background colors that work with system themes

### Android Shortcuts

**App Shortcuts Configuration:**
```jsx
import { ShortcutManager } from 'react-native-shortcuts';

const setupAndroidShortcuts = async () => {
  const shortcuts = [
    {
      type: 'Dynamic',
      name: 'Start Practice',
      title: 'Start Practice Conversation',
      subtitle: 'Begin a new conversation session',
      iconName: 'ic_shortcut_conversation',
      data: {
        action: 'start_conversation'
      }
    },
    {
      type: 'Dynamic', 
      name: 'View Progress',
      title: 'Check Progress',
      subtitle: 'View your learning progress',
      iconName: 'ic_shortcut_progress',
      data: {
        action: 'view_progress'
      }
    }
  ];

  try {
    await ShortcutManager.setDynamicShortcuts(shortcuts);
  } catch (error) {
    console.error('Failed to set shortcuts:', error);
  }
};
```

### Android Sharing

**Share Intent Integration:**
```jsx
import { Share } from 'react-native';

const androidShare = async (content) => {
  try {
    await Share.share({
      message: content.message,
      title: content.title,
    }, {
      dialogTitle: 'Share your FlirtCraft progress',
      excludedActivityTypes: [
        'com.apple.UIKit.activity.AirDrop', // iOS-specific
      ],
    });
  } catch (error) {
    console.error('Android share failed:', error);
  }
};
```

## Android Accessibility

### TalkBack Optimization

**TalkBack-Friendly Components:**
```jsx
const AndroidAccessibleButton = ({ title, onPress, accessibilityHint }) => (
  <TouchableRipple
    onPress={onPress}
    accessible={true}
    accessibilityRole="button"
    accessibilityLabel={title}
    accessibilityHint={accessibilityHint}
    accessibilityState={{ disabled: false }}
  >
    <View style={styles.buttonContainer}>
      <Text style={styles.buttonText}>{title}</Text>
    </View>
  </TouchableRipple>
);
```

**Content Descriptions:**
```jsx
const AndroidAccessibleContent = ({ children, contentDescription }) => (
  <View
    accessible={true}
    accessibilityLabel={contentDescription}
    accessibilityRole="text"
    importantForAccessibility="yes"
  >
    {children}
  </View>
);
```

### Android-Specific Accessibility Features

**High Contrast Support:**
```jsx
import { AccessibilityInfo } from 'react-native';

const useAndroidHighContrast = () => {
  const [isHighContrast, setIsHighContrast] = useState(false);

  useEffect(() => {
    // Check if high contrast is enabled
    AccessibilityInfo.isHighTextContrastEnabled()
      .then(setIsHighContrast);

    const subscription = AccessibilityInfo.addEventListener(
      'highTextContrastChanged',
      setIsHighContrast
    );

    return () => subscription?.remove();
  }, []);

  return isHighContrast;
};
```

**Font Scale Support:**
```jsx
import { PixelRatio, Dimensions } from 'react-native';

const getAndroidFontScale = () => {
  return PixelRatio.getFontScale();
};

const AndroidScalableText = ({ children, style }) => {
  const fontScale = getAndroidFontScale();
  
  return (
    <Text 
      style={[
        style,
        {
          fontSize: style.fontSize * Math.min(fontScale, 2.0),
        }
      ]}
      allowFontScaling={true}
      maxFontSizeMultiplier={2.0}
    >
      {children}
    </Text>
  );
};
```

## Android Performance Optimization

### Memory Management

**Android Memory Optimization:**
```jsx
import { AppState, DeviceEventEmitter } from 'react-native';

const AndroidMemoryManager = () => {
  useEffect(() => {
    const handleLowMemory = () => {
      // Clear image caches
      // Remove non-essential data
      // Optimize memory usage
    };

    const memoryListener = DeviceEventEmitter.addListener(
      'memoryWarning',
      handleLowMemory
    );

    return () => memoryListener.remove();
  }, []);
};
```

**Background Processing:**
```jsx
import BackgroundJob from '@react-native-async-storage/async-storage';

const AndroidBackgroundSync = async () => {
  try {
    // Perform lightweight background operations
    await syncEssentialData();
  } catch (error) {
    console.error('Background sync failed:', error);
  }
};
```

### Android-Specific Optimizations

**APK Size Optimization:**
- Android App Bundle (AAB) generation
- Dynamic feature modules for premium content
- Image format optimization (WebP support)
- ProGuard/R8 code shrinking

**Startup Performance:**
```jsx
import { InteractionManager } from 'react-native';

const AndroidOptimizedScreen = ({ children }) => {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    InteractionManager.runAfterInteractions(() => {
      setIsReady(true);
    });
  }, []);

  if (!isReady) {
    return <AndroidLoadingScreen />;
  }

  return children;
};
```

## Material Design Theming

### Dynamic Theming Support

**Material You Color Extraction:**
```jsx
import { extractColors } from 'react-native-image-colors';

const extractMaterialColors = async (imageUri) => {
  try {
    const colors = await extractColors(imageUri, {
      fallback: '#F97316',
      cache: true,
      key: imageUri,
    });

    if (colors.platform === 'android') {
      return {
        primary: colors.dominant,
        secondary: colors.vibrant,
        background: colors.lightMuted,
      };
    }
  } catch (error) {
    console.error('Color extraction failed:', error);
    return defaultColors;
  }
};
```

**Theme Application:**
```jsx
const MaterialDynamicTheme = ({ colors, children }) => {
  const theme = {
    ...MD3LightTheme,
    colors: {
      ...MD3LightTheme.colors,
      primary: colors.primary,
      secondary: colors.secondary,
      primaryContainer: colors.primaryContainer,
      onPrimary: colors.onPrimary,
    },
  };

  return (
    <PaperProvider theme={theme}>
      {children}
    </PaperProvider>
  );
};
```

## Google Play Integration

### Play Store Requirements

**Google Play Policy Compliance:**
- Target SDK version requirements
- Privacy policy and data handling disclosure
- Content rating accuracy
- In-app purchase integration (for premium features)

**Play Console Optimization:**
- App bundle optimization
- Staged rollouts for updates
- Play Console analytics integration
- Crash reporting and ANR monitoring

### Android Testing Requirements

**Device Testing Matrix:**
- Pixel devices (latest 3 generations)
- Samsung Galaxy devices (popular models)
- OnePlus, Xiaomi, and other OEM devices
- Foldable devices (Samsung Galaxy Fold, Google Pixel Fold)
- Android TV/tablets (if supporting)

**Android Version Support:**
- Android 7.0 (API 24) minimum (covers 95%+ devices)
- Android 14+ (API 34) optimizations
- Graceful degradation for older Android versions
- Regular testing on Android beta versions

### Performance Testing

**Android-Specific Testing:**
- Memory usage across different OEM customizations
- Battery optimization compliance
- Background processing limits
- ANR (Application Not Responding) prevention

## Foldable and Large Screen Support

### Foldable Device Adaptations

**Screen Configuration Changes:**
```jsx
import { useDeviceOrientation } from '@react-native-community/hooks';

const AndroidFoldableSupport = ({ children }) => {
  const { isLandscape, isPortrait } = useDeviceOrientation();
  const [screenSize, setScreenSize] = useState('normal');

  useEffect(() => {
    const updateScreenSize = () => {
      const { width, height } = Dimensions.get('window');
      const aspectRatio = Math.max(width, height) / Math.min(width, height);
      
      if (aspectRatio > 1.8) {
        setScreenSize('foldable');
      } else if (width > 600) {
        setScreenSize('tablet');
      } else {
        setScreenSize('phone');
      }
    };

    const subscription = Dimensions.addEventListener('change', updateScreenSize);
    updateScreenSize();

    return () => subscription?.remove();
  }, []);

  return (
    <View style={getLayoutStyles(screenSize)}>
      {children}
    </View>
  );
};
```

**Multi-Window Mode Support:**
- Responsive layouts for split-screen mode
- Activity lifecycle management
- State preservation across window changes

---

## Related Documentation

- [iOS Adaptations](./ios.md) - iOS-specific design patterns
- [Component Library](../components/) - Material component implementations  
- [Accessibility Guidelines](../../accessibility/guidelines.md) - Android accessibility requirements
- [Style Guide](../style-guide.md) - Core design system foundations

## External References

- [Material Design 3](https://m3.material.io/)
- [Android Design Guidelines](https://developer.android.com/design)
- [Material You](https://material.io/blog/announcing-material-you)
- [Android Accessibility](https://developer.android.com/guide/topics/ui/accessibility)
- [Google Play Console](https://developer.android.com/distribute/console)

## Last Updated
*Version 1.0.0 - 2025-08-23*
*Status: Complete Android adaptation guidelines ready for implementation*