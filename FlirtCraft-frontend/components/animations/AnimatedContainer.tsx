import React from 'react';
import { View, ViewStyle } from 'react-native';
import Animated, { useAnimatedStyle } from 'react-native-reanimated';
import { useEntranceAnimation, AnimationType, EntranceAnimationOptions } from '../../lib/hooks/useEntranceAnimation';

interface AnimatedContainerProps {
  children: React.ReactNode;
  animation?: AnimationType;
  delay?: number;
  duration?: number;
  useSpring?: boolean;
  springConfig?: EntranceAnimationOptions['springConfig'];
  style?: ViewStyle;
}

export const AnimatedContainer: React.FC<AnimatedContainerProps> = ({
  children,
  animation = 'fadeSlideUp',
  delay = 0,
  duration = 500,
  useSpring = true,
  springConfig,
  style,
}) => {
  const animationResult = useEntranceAnimation({
    type: animation,
    delay,
    duration,
    useSpring,
    springConfig,
  });

  // Handle backward compatibility - if it's just a style object, use it directly
  const animatedStyle = animationResult && typeof animationResult === 'object' && 'style' in animationResult
    ? animationResult.style
    : animationResult;

  return (
    <Animated.View
      style={[
        // Ensure the container doesn't interfere with layout
        { flex: style?.flex, width: style?.width, height: style?.height },
        // Apply the animated style which includes opacity for fade effects
        animatedStyle,
        // Apply custom styles last, but don't override the opacity from animation
        style && { ...style, opacity: undefined }
      ]}
      collapsable={false}
      renderToHardwareTextureAndroid={true}
      shouldRasterizeIOS={true}
    >
      {children}
    </Animated.View>
  );
};

interface StaggeredContainerProps {
  children: React.ReactNode[];
  baseDelay?: number;
  staggerDelay?: number;
  animation?: AnimationType;
  containerStyle?: ViewStyle;
  itemStyle?: ViewStyle;
}

export const StaggeredContainer: React.FC<StaggeredContainerProps> = ({
  children,
  baseDelay = 120, // Faster start for premium feel
  staggerDelay = 50, // Tighter stagger for cohesive motion
  animation = 'fadeSlideUp',
  containerStyle,
  itemStyle,
}) => {
  return (
    <View style={containerStyle}>
      {children.map((child, index) => (
        <AnimatedContainer
          key={index}
          animation={animation}
          delay={baseDelay + index * staggerDelay}
          duration={450} // Slightly faster for premium feel
          style={itemStyle}
          useSpring={true}
          springConfig={{
            damping: 16, // Premium damping for smooth motion
            stiffness: 120, // Balanced stiffness
            mass: 1.2, // Natural mass for realistic motion
          }}
        >
          {child}
        </AnimatedContainer>
      ))}
    </View>
  );
};

