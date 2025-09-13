import React, { useState } from 'react';
import { router } from 'expo-router';
import {
  Box,
  VStack,
  Text,
  Button,
  HStack,
  Icon,
  Pressable,
  Center,
  Alert,
} from 'native-base';
import { Ionicons } from '@expo/vector-icons';
import { authService } from '../../services/supabase';
import { useOnboardingStore } from '../../stores/onboardingStore';

export default function MainAppScreen() {
  const { resetOnboarding } = useOnboardingStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleSignOut = async () => {
    setIsLoading(true);
    
    try {
      await authService.signOut();
      resetOnboarding();
      router.replace('/');
    } catch (error) {
      console.error('Sign out error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetOnboarding = () => {
    resetOnboarding();
    router.replace('/');
  };

  return (
    <Box flex={1} bg="white" safeArea px={6} py={8}>
      <VStack flex={1} justifyContent="center" space={6}>
        {/* Success Message */}
        <Center>
          <Box
            w={20}
            h={20}
            borderRadius="full"
            bg="success.100"
            justifyContent="center"
            alignItems="center"
            mb={4}
          >
            <Icon
              as={Ionicons}
              name="checkmark-circle"
              size={12}
              color="success.600"
            />
          </Box>
          
          <Text variant="heading1" textAlign="center" color="gray.900" mb={2}>
            Welcome to FlirtCraft! 🎉
          </Text>
          
          <Text
            fontSize="lg"
            color="gray.600"
            textAlign="center"
            maxW="sm"
            lineHeight="lg"
          >
            Congratulations! You've completed the onboarding process. 
            The main app features are in development.
          </Text>
        </Center>

        {/* Info Alert */}
        <Alert status="info" borderRadius="lg">
          <HStack space={2} alignItems="center">
            <Icon as={Ionicons} name="information-circle" size={5} color="info.500" />
            <Text flex={1} fontSize="sm" color="info.700">
              This is a placeholder screen. The conversation practice features 
              will be available in the next development phase.
            </Text>
          </HStack>
        </Alert>

        {/* Coming Soon Features */}
        <VStack space={4}>
          <Text fontSize="lg" fontWeight="semibold" color="gray.900" textAlign="center">
            Coming Soon:
          </Text>
          
          {[
            { icon: 'chatbubbles', title: 'AI Conversation Practice', color: 'primary' },
            { icon: 'location', title: 'Scenario Selection', color: 'success' },
            { icon: 'analytics', title: 'Performance Feedback', color: 'warning' },
            { icon: 'trophy', title: 'Achievement System', color: 'secondary' },
          ].map((feature, index) => (
            <HStack key={index} space={4} alignItems="center" p={3} bg="gray.50" borderRadius="lg">
              <Box
                w={10}
                h={10}
                borderRadius="full"
                bg={`${feature.color}.100`}
                justifyContent="center"
                alignItems="center"
              >
                <Icon
                  as={Ionicons}
                  name={feature.icon as any}
                  size={5}
                  color={`${feature.color}.600`}
                />
              </Box>
              <Text fontSize="md" fontWeight="medium" color="gray.700" flex={1}>
                {feature.title}
              </Text>
              <Icon as={Ionicons} name="hourglass" size={4} color="gray.400" />
            </HStack>
          ))}
        </VStack>

        {/* Development Actions */}
        <VStack space={3} mt={8}>
          <Text fontSize="md" fontWeight="semibold" color="gray.900" textAlign="center">
            Development Options:
          </Text>
          
          <Button
            variant="outline"
            onPress={handleResetOnboarding}
            leftIcon={<Icon as={Ionicons} name="refresh" size={4} />}
          >
            Reset Onboarding (Test Again)
          </Button>
          
          <Button
            variant="ghost"
            colorScheme="error"
            onPress={handleSignOut}
            isLoading={isLoading}
            leftIcon={<Icon as={Ionicons} name="log-out" size={4} />}
          >
            Sign Out
          </Button>
        </VStack>
      </VStack>
    </Box>
  );
}