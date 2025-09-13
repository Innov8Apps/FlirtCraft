import { useEffect, useRef } from 'react';
import {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  withDelay,
  Easing,
  runOnJS
} from 'react-native-reanimated';

export type AnimationType = 'fadeIn' | 'slideUp' | 'slideDown' | 'slideLeft' | 'slideRight' | 'scale' | 'fadeSlideUp';

export interface EntranceAnimationOptions {
  type: AnimationType;
  delay?: number;
  duration?: number;
  useSpring?: boolean;
  springConfig?: {
    damping?: number;
    stiffness?: number;
    mass?: number;
  };
}

export const useEntranceAnimation = (options: EntranceAnimationOptions) => {
  const { type, delay = 0, duration = 500, useSpring = true, springConfig } = options;

  // Initialize values to their STARTING states to prevent flicker
  // This ensures elements start invisible/displaced and animate to final position
  const getInitialValues = () => {
    switch (type) {
      case 'fadeIn':
        return { opacity: 0, translateX: 0, translateY: 0, scale: 1 };
      case 'slideUp':
      case 'fadeSlideUp':
        return {
          opacity: type === 'fadeSlideUp' ? 0 : 1,
          translateX: 0,
          translateY: 24,
          scale: 1
        };
      case 'slideDown':
        return { opacity: 1, translateX: 0, translateY: -24, scale: 1 };
      case 'slideLeft':
        return { opacity: 1, translateX: 24, translateY: 0, scale: 1 };
      case 'slideRight':
        return { opacity: 1, translateX: -24, translateY: 0, scale: 1 };
      case 'scale':
        return { opacity: 0, translateX: 0, translateY: 0, scale: 0.92 };
      default:
        return { opacity: 0, translateX: 0, translateY: 24, scale: 1 };
    }
  };

  const initialValues = getInitialValues();
  const opacity = useSharedValue(initialValues.opacity);
  const translateX = useSharedValue(initialValues.translateX);
  const translateY = useSharedValue(initialValues.translateY);
  const scale = useSharedValue(initialValues.scale);
  const hasAnimated = useRef(false);

  useEffect(() => {
    // Only animate once on mount
    if (hasAnimated.current) return;
    hasAnimated.current = true;

    // Use a timeout to defer animation start outside of render cycle
    const timeoutId = setTimeout(() => {
      // Premium animation configurations
      const createOpacityAnimation = () => {
        return useSpring
          ? withSpring(1, {
              damping: springConfig?.damping || 16,
              stiffness: springConfig?.stiffness || 120,
              mass: springConfig?.mass || 1.2,
            })
          : withTiming(1, {
              duration,
              easing: Easing.bezier(0.25, 0.46, 0.45, 0.94), // Premium easeOutQuart
            });
      };

      const createTransformAnimation = () => {
        return useSpring
          ? withSpring(0, {
              damping: springConfig?.damping || 18,
              stiffness: springConfig?.stiffness || 110,
              mass: springConfig?.mass || 1.1,
            })
          : withTiming(0, {
              duration,
              easing: Easing.bezier(0.25, 0.46, 0.45, 0.94), // Premium easeOutQuart
            });
      };

      const createScaleAnimation = () => {
        return useSpring
          ? withSpring(1, {
              damping: springConfig?.damping || 14,
              stiffness: springConfig?.stiffness || 140,
              mass: springConfig?.mass || 0.9,
            })
          : withTiming(1, {
              duration: duration * 0.8, // Slightly faster scale for premium feel
              easing: Easing.bezier(0.34, 1.56, 0.64, 1), // Subtle bounce for scale
            });
      };

      // Create animations
      const opacityAnimation = createOpacityAnimation();
      const transformAnimation = createTransformAnimation();
      const scaleAnimation = createScaleAnimation();

      // Apply delays
      const delayedOpacity = delay > 0 ? withDelay(delay, opacityAnimation) : opacityAnimation;
      const delayedTransform = delay > 0 ? withDelay(delay, transformAnimation) : transformAnimation;
      const delayedScale = delay > 0 ? withDelay(delay, scaleAnimation) : scaleAnimation;

      // Execute animations based on type
      switch (type) {
        case 'fadeIn':
          opacity.value = delayedOpacity;
          break;
        case 'slideUp':
        case 'fadeSlideUp':
          if (type === 'fadeSlideUp') {
            opacity.value = delayedOpacity;
          }
          translateY.value = delayedTransform;
          break;
        case 'slideDown':
          translateY.value = delayedTransform;
          break;
        case 'slideLeft':
          translateX.value = delayedTransform;
          break;
        case 'slideRight':
          translateX.value = delayedTransform;
          break;
        case 'scale':
          opacity.value = delayedOpacity;
          scale.value = delayedScale;
          break;
      }
    }, 0); // Use timeout to defer to next tick

    return () => {
      clearTimeout(timeoutId);
    };
  }, []); // Empty dependency array for single execution

  const animatedStyle = useAnimatedStyle(() => {
    return {
      opacity: opacity.value,
      transform: [
        { translateX: translateX.value },
        { translateY: translateY.value },
        { scale: scale.value },
      ],
    };
  });

  // Return both the style and the opacity shared value for color interpolation
  return {
    style: animatedStyle,
    opacity: opacity, // Return the shared value, not the .value
  };
};

export const useStaggeredAnimation = (
  itemCount: number,
  baseDelay: number = 60, // Reduced for faster, more premium feel
  animationType: AnimationType = 'fadeSlideUp'
) => {
  const animations = Array.from({ length: itemCount }, (_, index) =>
    useEntranceAnimation({
      type: animationType,
      delay: baseDelay + (index * 40), // Tighter stagger timing
      duration: 450, // Slightly faster for premium feel
      useSpring: true,
      springConfig: {
        damping: 16, // Premium damping for smooth motion
        stiffness: 120, // Balanced stiffness
        mass: 1.2, // Slightly heavier for more natural feel
      }
    })
  );

  return animations;
};