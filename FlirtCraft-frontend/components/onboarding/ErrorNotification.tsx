import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Easing,
} from 'react-native';
import {
  PanGestureHandler,
  PanGestureHandlerGestureEvent,
} from 'react-native-gesture-handler';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface ErrorNotificationProps {
  message: string;
  isVisible: boolean;
  onDismiss: () => void;
  type?: 'error' | 'warning' | 'info';
}

export const ErrorNotification: React.FC<ErrorNotificationProps> = ({
  message,
  isVisible,
  onDismiss,
  type = 'error',
}) => {
  const insets = useSafeAreaInsets();
  const slideAnim = useRef(new Animated.Value(-200)).current;
  const opacityAnim = useRef(new Animated.Value(0)).current;
  const translateXAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const panRef = useRef<PanGestureHandler>(null);

  useEffect(() => {
    if (isVisible) {
      // Reset all transform values to ensure proper positioning
      translateXAnim.setValue(0);
      scaleAnim.setValue(1);
      slideAnim.setValue(-200);
      opacityAnim.setValue(0);

      // Pop down animation
      Animated.parallel([
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 500,
          easing: Easing.out(Easing.back(1.2)),
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 1,
          duration: 400,
          easing: Easing.out(Easing.cubic),
          useNativeDriver: true,
        }),
      ]).start();
    } else {
      // Pop up animation
      Animated.parallel([
        Animated.timing(slideAnim, {
          toValue: -200,
          duration: 300,
          easing: Easing.in(Easing.cubic),
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 300,
          easing: Easing.in(Easing.cubic),
          useNativeDriver: true,
        }),
      ]).start(() => {
        // Reset transform values after hiding to prepare for next appearance
        if (!isVisible) {
          translateXAnim.setValue(0);
          scaleAnim.setValue(1);
        }
      });
    }
  }, [isVisible, slideAnim, opacityAnim, translateXAnim, scaleAnim]);

  const onGestureEvent = (event: PanGestureHandlerGestureEvent) => {
    const { translationY, translationX } = event.nativeEvent;

    // Follow finger movement smoothly in all directions
    slideAnim.setValue(translationY);
    translateXAnim.setValue(translationX);

    // Add subtle scale effect based on distance
    const totalDistance = Math.sqrt(translationX * translationX + translationY * translationY);
    const scaleValue = Math.max(0.85, 1 - totalDistance / 300);
    scaleAnim.setValue(scaleValue);

    // Fade out based on distance for visual feedback
    const fadeValue = Math.max(0.3, 1 - totalDistance / 200);
    opacityAnim.setValue(fadeValue);
  };

  const onHandlerStateChange = (event: any) => {
    if (event.nativeEvent.state === 5) { // GESTURE_STATE_END
      const { translationY, translationX, velocityY, velocityX } = event.nativeEvent;

      // Calculate total distance and velocity
      const totalDistance = Math.sqrt(translationX * translationX + translationY * translationY);
      const totalVelocity = Math.sqrt(velocityX * velocityX + velocityY * velocityY);

      // Dismiss if swiped far enough or with enough velocity
      if (totalDistance > 80 || totalVelocity > 800) {
        // Animate out in the direction of the swipe
        const finalX = translationX + velocityX * 0.1;
        const finalY = translationY + velocityY * 0.1;

        Animated.parallel([
          Animated.timing(translateXAnim, {
            toValue: finalX,
            duration: 200,
            easing: Easing.out(Easing.cubic),
            useNativeDriver: true,
          }),
          Animated.timing(slideAnim, {
            toValue: finalY,
            duration: 200,
            easing: Easing.out(Easing.cubic),
            useNativeDriver: true,
          }),
          Animated.timing(opacityAnim, {
            toValue: 0,
            duration: 200,
            useNativeDriver: true,
          }),
          Animated.timing(scaleAnim, {
            toValue: 0.7,
            duration: 200,
            easing: Easing.out(Easing.cubic),
            useNativeDriver: true,
          }),
        ]).start(() => {
          onDismiss();
        });
      } else {
        // Bounce back to original position with nice spring animation
        Animated.parallel([
          Animated.spring(slideAnim, {
            toValue: 0,
            tension: 150,
            friction: 8,
            useNativeDriver: true,
          }),
          Animated.spring(translateXAnim, {
            toValue: 0,
            tension: 150,
            friction: 8,
            useNativeDriver: true,
          }),
          Animated.spring(opacityAnim, {
            toValue: 1,
            tension: 150,
            friction: 8,
            useNativeDriver: true,
          }),
          Animated.spring(scaleAnim, {
            toValue: 1,
            tension: 150,
            friction: 8,
            useNativeDriver: true,
          }),
        ]).start();
      }
    }
  };

  const getIconName = () => {
    switch (type) {
      case 'warning':
        return 'warning';
      case 'info':
        return 'information-circle';
      default:
        return 'alert-circle';
    }
  };

  const getIconColor = () => {
    switch (type) {
      case 'warning':
        return '#FF6B35';
      case 'info':
        return '#FF6B35';
      default:
        return '#EF4444';
    }
  };

  const getCardStyle = () => {
    switch (type) {
      case 'warning':
        return {
          backgroundColor: '#FFF6F0',
          borderColor: '#FF6B35',
        };
      case 'info':
        return {
          backgroundColor: '#FFF6F0',
          borderColor: '#FF6B35',
        };
      default:
        return {
          backgroundColor: '#FEF2F2',
          borderColor: '#EF4444',
        };
    }
  };


  if (!isVisible) {
    return null;
  }

  return (
    <Animated.View
      style={[
        styles.container,
        {
          paddingTop: insets.top + 16,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <PanGestureHandler
        ref={panRef}
        onGestureEvent={onGestureEvent}
        onHandlerStateChange={onHandlerStateChange}
      >
        <Animated.View
          style={[
            styles.notificationCard,
            getCardStyle(),
            {
              transform: [
                { translateX: translateXAnim },
                { scale: scaleAnim }
              ],
              opacity: opacityAnim
            }
          ]}
        >
          <View style={styles.iconContainer}>
            <Ionicons
              name={getIconName() as any}
              size={20}
              color={getIconColor()}
            />
          </View>
          
          <Text style={styles.messageText} numberOfLines={3}>
            {message}
          </Text>
        </Animated.View>
      </PanGestureHandler>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
    paddingHorizontal: 24,
  },
  notificationCard: {
    borderWidth: 2,
    borderRadius: 16,
    padding: 18,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#FF6B35',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    elevation: 6,
    minHeight: 64,
  },
  iconContainer: {
    marginRight: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  messageText: {
    flex: 1,
    fontSize: 15,
    color: '#1F2937',
    lineHeight: 22,
    fontWeight: '500',
    letterSpacing: 0.2,
    paddingRight: 8,
  },
});

export default ErrorNotification;