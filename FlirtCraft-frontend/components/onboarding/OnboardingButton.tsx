import React from 'react';
import { Text, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
  withSequence,
  runOnJS
} from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';

interface OnboardingButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  loading?: boolean;
  accessibilityLabel?: string;
  accessibilityHint?: string;
}

const AnimatedTouchableOpacity = Animated.createAnimatedComponent(TouchableOpacity);

export default function OnboardingButton({
  title,
  onPress,
  variant = 'primary',
  disabled = false,
  loading = false,
  accessibilityLabel,
  accessibilityHint,
}: OnboardingButtonProps) {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const scaleAnimatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const opacityAnimatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  const handlePress = () => {
    if (disabled || loading) return;

    // Call onPress immediately for instant navigation
    onPress();

    // Play smooth visual feedback animation without blocking navigation
    scale.value = withSequence(
      withSpring(0.95, { duration: 150 }),
      withSpring(1, { duration: 300 })
    );

    opacity.value = withSequence(
      withSpring(0.8, { duration: 150 }),
      withSpring(1, { duration: 300 })
    );
  };

  const buttonStyle = [
    styles.button,
    variant === 'secondary' && styles.secondaryButton,
    disabled && styles.disabledButton,
  ];

  const textStyle = [
    styles.buttonText,
    variant === 'secondary' && styles.secondaryButtonText,
    disabled && styles.disabledButtonText,
  ];

  if (variant === 'primary' && !disabled) {
    return (
      <Animated.View style={[scaleAnimatedStyle, { borderRadius: 12 }]}>
        <AnimatedTouchableOpacity
          style={[opacityAnimatedStyle, { borderRadius: 12 }]}
          onPress={handlePress}
          accessibilityRole="button"
          accessibilityLabel={accessibilityLabel || title}
          accessibilityHint={accessibilityHint}
          disabled={disabled || loading}
        >
          <LinearGradient
            colors={['#FF6B35', '#FF7F50']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={[styles.button, styles.primaryGradient]}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" size="small" />
            ) : (
              <Text style={textStyle}>{title}</Text>
            )}
          </LinearGradient>
        </AnimatedTouchableOpacity>
      </Animated.View>
    );
  }

  return (
    <Animated.View style={[scaleAnimatedStyle]}>
      <AnimatedTouchableOpacity
        style={[opacityAnimatedStyle, buttonStyle]}
        onPress={handlePress}
        accessibilityRole="button"
        accessibilityLabel={accessibilityLabel || title}
        accessibilityHint={accessibilityHint}
        disabled={disabled || loading}
      >
        {loading ? (
          <ActivityIndicator
            color={variant === 'primary' ? '#FFFFFF' : '#FF6B35'}
            size="small"
          />
        ) : (
          <Text style={textStyle}>{title}</Text>
        )}
      </AnimatedTouchableOpacity>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 56,
    backgroundColor: '#FF6B35',
  },
  primaryGradient: {
    backgroundColor: 'transparent',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#FF6B35',
  },
  disabledButton: {
    backgroundColor: '#E5E5E5',
    borderColor: '#E5E5E5',
  },
  buttonText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
    textAlign: 'center',
  },
  secondaryButtonText: {
    color: '#FF6B35',
  },
  disabledButtonText: {
    color: '#9CA3AF',
  },
});