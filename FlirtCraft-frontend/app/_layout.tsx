import { Slot } from 'expo-router';
import { NativeBaseProvider } from 'native-base';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StatusBar } from 'expo-status-bar';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import theme from '../lib/theme';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
});

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <QueryClientProvider client={queryClient}>
        <NativeBaseProvider theme={theme}>
          <GestureHandlerRootView style={{ flex: 1 }}>
            <StatusBar style="dark" />
            <Slot />
          </GestureHandlerRootView>
        </NativeBaseProvider>
      </QueryClientProvider>
    </SafeAreaProvider>
  );
}