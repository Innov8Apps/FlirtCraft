import React, { useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated, Easing } from 'react-native';
import { Ionicons, MaterialIcons, Feather, FontAwesome5 } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface OnboardingHeaderProps {
  currentStep: number;
  totalSteps: number;
  completedSteps: number;
  showBackButton?: boolean;
  onBackPress?: () => void;
  title?: string;
  lastNavigationDirection?: 'forward' | 'backward';
  rightIcon?: {
    name: string;
    type?: 'ionicons' | 'material' | 'feather' | 'fontawesome';
    color?: string;
    size?: number;
  };
}

export const OnboardingHeader: React.FC<OnboardingHeaderProps> = ({
  currentStep,
  totalSteps,
  completedSteps,
  showBackButton = true,
  onBackPress,
  title,
  lastNavigationDirection,
  rightIcon,
}) => {
  const insets = useSafeAreaInsets();
  // Initialize animated width - will be set correctly based on navigation direction
  const animatedWidth = useRef(new Animated.Value(0)).current;
  const animatedScale = useRef(new Animated.Value(1)).current;
  const animatedGlow = useRef(new Animated.Value(0)).current;
  const previousCompletedSteps = useRef(completedSteps);
  const isFirstRender = useRef(true);
  
  useEffect(() => {
    const targetPercentage = (completedSteps / totalSteps) * 100;

    if (isFirstRender.current) {
      isFirstRender.current = false;

      // Determine starting value based on navigation direction
      let startingPercentage;

      if (lastNavigationDirection === 'backward') {
        // Going backwards: start from the next step position and animate down
        startingPercentage = Math.min(100, ((completedSteps + 1) / totalSteps) * 100);
      } else {
        // Going forwards or initial: start from the previous step position and animate up
        startingPercentage = Math.max(0, ((completedSteps - 1) / totalSteps) * 100);
      }

      // Set the starting value
      animatedWidth.setValue(startingPercentage);

      // Start the animation immediately
      // Create a sequence of animations for smooth progress filling/defilling
      Animated.sequence([
        // Slight scale up and glow for emphasis
        Animated.parallel([
          Animated.timing(animatedScale, {
            toValue: 1.02,
            duration: 200,
            easing: Easing.out(Easing.quad),
            useNativeDriver: true,
          }),
          Animated.timing(animatedGlow, {
            toValue: 1,
            duration: 200,
            easing: Easing.out(Easing.quad),
            useNativeDriver: true,
          }),
        ]),
        // Progress bar animation (fill or defill) with extremely gentle spring physics
        Animated.parallel([
          Animated.spring(animatedWidth, {
            toValue: targetPercentage,
            tension: 4, // Very low tension for extremely slow animation
            friction: 35, // High friction for very controlled movement
            useNativeDriver: false, // Cannot use native driver for width animations
          }),
          // Scale back to normal (much slower)
          Animated.timing(animatedScale, {
            toValue: 1,
            duration: 2000,
            easing: Easing.out(Easing.quad),
            useNativeDriver: true,
          }),
          // Fade out the glow (much slower)
          Animated.timing(animatedGlow, {
            toValue: 0,
            duration: 2500,
            easing: Easing.out(Easing.quad),
            useNativeDriver: true,
          }),
        ]),
      ]).start();
    }
  }, [completedSteps, totalSteps, currentStep, lastNavigationDirection, animatedWidth, animatedScale, animatedGlow]);
  
  const handleBackPress = () => {
    if (onBackPress) {
      onBackPress();
    } else {
      router.back();
    }
  };

  const progressPercentage = (completedSteps / totalSteps) * 100;

  const renderRightIcon = () => {
    if (!rightIcon) return null;
    
    const iconProps = {
      name: rightIcon.name as any,
      size: rightIcon.size || 24,
      color: rightIcon.color || '#FF6B35',
    };

    switch (rightIcon.type) {
      case 'material':
        return <MaterialIcons {...iconProps} />;
      case 'feather':
        return <Feather {...iconProps} />;
      case 'fontawesome':
        return <FontAwesome5 {...iconProps} />;
      default:
        return <Ionicons {...iconProps} />;
    }
  };

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      {/* Header with back button and centered step text */}
      <View style={styles.headerContent}>
        <View style={styles.leftSection}>
          {showBackButton && (
            <TouchableOpacity
              onPress={handleBackPress}
              style={styles.backButton}
              activeOpacity={0.7}
            >
              <Ionicons 
                name="chevron-back" 
                size={18} 
                color="#FF6B35" 
              />
            </TouchableOpacity>
          )}
        </View>
        
        {/* Step text centered above progress bar */}
        <View style={styles.stepContainer}>
          <Text style={styles.stepText}>
            Step {currentStep} of {totalSteps}
          </Text>
        </View>
      </View>

      {/* Progress bar */}
      <Animated.View
        style={[
          styles.progressContainer,
          {
            transform: [{ scaleY: animatedScale }],
            shadowOpacity: animatedGlow.interpolate({
              inputRange: [0, 1],
              outputRange: [0.1, 0.4],
            }),
          }
        ]}
      >
        <View style={styles.progressTrack}>
          <Animated.View 
            style={[
              styles.progressBarContainer,
              {
                width: animatedWidth.interpolate({
                  inputRange: [0, 100],
                  outputRange: ['0%', '100%'],
                }),
              }
            ]}
          >
            <LinearGradient
              colors={['#FC993C', '#E75200']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.progressBar}
            />
          </Animated.View>
        </View>
      </Animated.View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'transparent',
    paddingHorizontal: 24,
    paddingBottom: 12,
  },
  progressContainer: {
    marginBottom: 8,
    shadowColor: '#FC993C',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowRadius: 4,
    elevation: 3,
  },
  progressTrack: {
    height: 10, // Slightly taller for better visibility
    backgroundColor: '#e5e7eb',
    borderRadius: 5,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  progressBarContainer: {
    height: '100%',
    overflow: 'hidden',
    borderRadius: 5,
  },
  progressBar: {
    height: '100%',
    borderRadius: 5,
    shadowColor: '#FC993C',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.3,
    shadowRadius: 2,
    elevation: 2,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  leftSection: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-start',
    flex: 1,
  },
  stepContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    position: 'absolute',
    left: 0,
    right: 0,
  },
  backButton: {
    padding: 4,
    marginRight: 4,
    marginLeft: -4,
  },
  stepText: {
    fontSize: 16,
    color: '#FA7215',
    fontWeight: '500',
    textAlign: 'center',
  },
  titleText: {
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '600',
    marginTop: 2,
    textAlign: 'center',
  },
  rightIcon: {
    padding: 8,
    marginRight: -8,
    width: 60,
    alignItems: 'flex-end',
  },
});

export default OnboardingHeader;