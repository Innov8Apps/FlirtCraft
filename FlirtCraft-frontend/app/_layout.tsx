import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/use-color-scheme';
import { useOnboardingStore } from '@/stores/onboardingStore';
import OnboardingFlow from '@/features/onboarding/components/OnboardingFlow';
import MainAppPlaceholder from '@/components/MainAppPlaceholder';
import { ReactQueryProvider, NativeBaseAppProvider } from '@/lib/providers';

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const { isComplete } = useOnboardingStore();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Allow state to hydrate from persistence
    const timer = setTimeout(() => {
      setIsReady(true);
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  if (!isReady) {
    // Show loading while state hydrates
    return null;
  }

  // Use standard navigation in both dev and production
  return (
    <ReactQueryProvider>
      <NativeBaseAppProvider>
        <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
          <Stack>
            <Stack.Screen name="index" options={{ headerShown: false }} />
            <Stack.Screen name="onboarding/index" options={{ headerShown: false }} />
            <Stack.Screen name="signin/index" options={{ headerShown: false }} />
            <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
            <Stack.Screen name="modal" options={{ presentation: 'modal', title: 'Modal' }} />
          </Stack>
          <StatusBar style="auto" />
        </ThemeProvider>
      </NativeBaseAppProvider>
    </ReactQueryProvider>
  );
}
