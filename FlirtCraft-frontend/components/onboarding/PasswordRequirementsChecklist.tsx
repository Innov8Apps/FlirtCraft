import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface PasswordRequirement {
  id: string;
  text: string;
  regex: RegExp;
  validator?: (password: string) => boolean;
}

interface PasswordRequirementsChecklistProps {
  password: string;
  style?: any;
}

export const PasswordRequirementsChecklist: React.FC<PasswordRequirementsChecklistProps> = ({
  password,
  style
}) => {
  const requirements: PasswordRequirement[] = [
    {
      id: 'length',
      text: 'At least 8 characters',
      regex: /.{8,}/,
    },
    {
      id: 'uppercase',
      text: 'One uppercase letter (A-Z)',
      regex: /[A-Z]/,
    },
    {
      id: 'lowercase',
      text: 'One lowercase letter (a-z)',
      regex: /[a-z]/,
    },
    {
      id: 'number',
      text: 'One number (0-9)',
      regex: /\d/,
    },
  ];

  const checkRequirement = (requirement: PasswordRequirement): boolean => {
    if (requirement.validator) {
      return requirement.validator(password);
    }
    return requirement.regex.test(password);
  };

  const getRequirementIcon = (isMet: boolean) => {
    return isMet ? (
      <Ionicons name="checkmark-circle" size={18} color="#059669" />
    ) : (
      <Ionicons name="close-circle" size={18} color="#EF4444" />
    );
  };

  const getRequirementTextStyle = (isMet: boolean) => {
    return [
      styles.requirementText,
      isMet ? styles.requirementTextMet : styles.requirementTextUnmet
    ];
  };

  // Only render if there's a password to check AND there are unmet requirements
  if (!password) {
    return null;
  }

  // Check if all requirements are met
  const allRequirementsMet = requirements.every(requirement => checkRequirement(requirement));

  // Don't render if all requirements are satisfied
  if (allRequirementsMet) {
    return null;
  }

  return (
    <View style={[styles.container, style]}>
      {requirements.map((requirement) => {
        const isMet = checkRequirement(requirement);

        // Only show unmet requirements
        if (isMet) {
          return null;
        }

        return (
          <View key={requirement.id} style={styles.requirementRow}>
            <View style={styles.iconContainer}>
              {getRequirementIcon(isMet)}
            </View>
            <Text style={getRequirementTextStyle(isMet)}>
              {requirement.text}
            </Text>
          </View>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    // Remove all box styling - no background, borders, padding
  },
  requirementRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  iconContainer: {
    marginRight: 10,
    width: 18,
    alignItems: 'center',
  },
  requirementText: {
    fontSize: 14,
    flex: 1,
    lineHeight: 20,
  },
  requirementTextMet: {
    color: '#059669',
    fontWeight: '500',
  },
  requirementTextUnmet: {
    color: '#6B7280',
    fontWeight: '400',
  },
});