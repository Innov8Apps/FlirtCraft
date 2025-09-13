import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { ErrorProvider } from '../../lib/contexts/ErrorContext';
import { ErrorNotificationWrapper } from '../../components/onboarding/ErrorNotificationWrapper';

export default function OnboardingLayout() {
  return (
    <ErrorProvider>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerShown: false,
          gestureEnabled: true,
          animation: 'slide_from_right',
          animationDuration: 180, // Back to original good speed
        }}
      >
        <Stack.Screen 
          name="welcome" 
          options={{
            gestureEnabled: false, // Disable swipe back on welcome screen
          }}
        />
        <Stack.Screen name="age-verification" />
        <Stack.Screen name="register" />
        <Stack.Screen name="preferences" />
        <Stack.Screen name="skills" />
      </Stack>
      <ErrorNotificationWrapper />
    </ErrorProvider>
  );
}