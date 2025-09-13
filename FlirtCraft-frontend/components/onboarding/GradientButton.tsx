import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ViewStyle, TextStyle, ActivityIndicator, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface GradientButtonProps {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
  variant?: 'primary' | 'secondary';
  cooldown?: boolean;
}

export const GradientButton: React.FC<GradientButtonProps> = ({
  title,
  onPress,
  disabled = false,
  loading = false,
  style,
  textStyle,
  variant = 'primary',
  cooldown = false,
}) => {
  const getGradientColors = (): [string, string] => {
    if (cooldown) {
      return ['#FFF6F0', '#FFFAF6']; // Light warm background for cooldown
    }
    return variant === 'primary'
      ? ['#FC993C', '#E75200']
      : ['#f3f4f6', '#e5e7eb'];
  };

  const gradientColors = getGradientColors();
  const isDisabled = disabled || loading;

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={isDisabled}
      style={[styles.container, style]}
      activeOpacity={0.8}
    >
      <LinearGradient
        colors={gradientColors}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={[
          styles.gradient,
          isDisabled && !cooldown && styles.gradientDisabled,
          cooldown && styles.gradientCooldown,
        ]}
      >
        {cooldown && (
          <View style={styles.cooldownBorder} />
        )}
        {loading ? (
          <ActivityIndicator 
            color={variant === 'primary' ? '#ffffff' : '#374151'} 
            size="small" 
          />
        ) : (
          <Text
            style={[
              styles.text,
              variant === 'secondary' && styles.textSecondary,
              textStyle,
              isDisabled && !cooldown && styles.textDisabled,
              cooldown && styles.textCooldown,
            ]}
          >
            {title}
          </Text>
        )}
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  gradient: {
    paddingHorizontal: 32,
    paddingVertical: 16,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 52,
  },
  gradientDisabled: {
    opacity: 0.5,
  },
  gradientCooldown: {
    opacity: 0.85, // Less blurred than disabled
  },
  text: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
    textAlign: 'center',
  },
  textSecondary: {
    color: '#374151',
  },
  textDisabled: {
    opacity: 0.7,
  },
  textCooldown: {
    color: '#EF4444', // Red text for cooldown
    opacity: 1,
    fontWeight: '600',
  },
  cooldownBorder: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#EF4444', // Red border
  },
});

export default GradientButton;