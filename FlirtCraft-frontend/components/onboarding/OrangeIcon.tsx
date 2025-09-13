import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons, MaterialIcons, FontAwesome5, Feather } from '@expo/vector-icons';

interface OrangeIconProps {
  type: string;
  selected?: boolean;
  disabled?: boolean;
  size?: number;
}

export const OrangeIcon: React.FC<OrangeIconProps> = ({ type, selected = false, disabled = false, size = 32 }) => {
  const getIconColor = () => {
    if (disabled) return '#E5E7EB';
    return '#FF8C42';
  };

  const iconProps = {
    size: size,
    color: getIconColor(),
  };

  switch (type) {
    case 'conversation_starters':
      return <Ionicons name="chatbubbles" {...iconProps} />;
    case 'active_listening':
      return <Feather name="headphones" {...iconProps} />;
    case 'flirting_techniques':
      return <Ionicons name="heart" {...iconProps} />;
    case 'confidence_building':
      return <MaterialIcons name="psychology" {...iconProps} />;
    case 'body_language':
      return <Ionicons name="body" {...iconProps} />;
    case 'humor_and_wit':
      return <Ionicons name="happy" {...iconProps} />;
    case 'emotional_intelligence':
      return <FontAwesome5 name="brain" {...iconProps} />;
    case 'authentic_connection':
      return <Ionicons name="link" {...iconProps} />;
    // Gender icons
    case 'male':
      return <Ionicons name="male" {...iconProps} />;
    case 'female':
      return <Ionicons name="female" {...iconProps} />;
    case 'non-binary':
      return <Ionicons name="person" {...iconProps} />;
    case 'prefer-not-to-say':
      return <Ionicons name="help-circle" {...iconProps} />;
    case 'everyone':
      return <Ionicons name="people" {...iconProps} />;
    default:
      return <Ionicons name="star" {...iconProps} />;
  }
};

const styles = StyleSheet.create({
  container: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
});