import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { ErrorProvider } from '../../lib/contexts/ErrorContext';
import { ErrorNotificationWrapper } from '../../components/onboarding/ErrorNotificationWrapper';

export default function AuthLayout() {
  return (
    <ErrorProvider>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerShown: false,
          gestureEnabled: true,
          animation: 'slide_from_right',
          animationDuration: 180,
        }}
      >
        <Stack.Screen name="login" />
      </Stack>
      <ErrorNotificationWrapper />
    </ErrorProvider>
  );
}