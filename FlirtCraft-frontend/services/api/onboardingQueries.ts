/**
 * React Query hooks for onboarding API integration
 * Provides caching, synchronization, and error handling
 */

import { useMutation, useQuery } from '@tanstack/react-query';
import { api, OnboardingStartRequest, OnboardingUpdateRequest, OnboardingCompleteRequest } from './onboardingApi';
import { OnboardingFormData } from '@/features/onboarding/types';

// Query keys for consistent caching
export const onboardingKeys = {
  all: ['onboarding'] as const,
  status: (userId: string) => [...onboardingKeys.all, 'status', userId] as const,
};

// Get onboarding status
export const useOnboardingStatusQuery = (userId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: onboardingKeys.status(userId),
    queryFn: () => api.getOnboardingStatus(userId),
    enabled,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
};

// Start onboarding mutation
export const useStartOnboardingMutation = () => {
  return useMutation({
    mutationFn: (request: OnboardingStartRequest) => api.startOnboarding(request),
    onSuccess: (data) => {
      console.log('Onboarding started successfully:', data);
    },
    onError: (error) => {
      console.error('Failed to start onboarding:', error);
    },
  });
};

// Update onboarding step mutation
export const useUpdateOnboardingMutation = () => {
  return useMutation({
    mutationFn: (request: OnboardingUpdateRequest) => api.updateOnboarding(request),
    onSuccess: (data, variables) => {
      console.log(`Step ${variables.step} updated successfully:`, data);
    },
    onError: (error) => {
      console.error('Failed to update onboarding step:', error);
    },
  });
};

// Complete onboarding mutation
export const useCompleteOnboardingMutation = () => {
  return useMutation({
    mutationFn: (request: OnboardingCompleteRequest) => api.completeOnboarding(request),
    onSuccess: (data) => {
      console.log('Onboarding completed successfully:', data);
    },
    onError: (error) => {
      console.error('Failed to complete onboarding:', error);
    },
  });
};

// Combined hook for onboarding operations
export const useOnboardingOperations = (userId: string) => {
  const statusQuery = useOnboardingStatusQuery(userId);
  const startMutation = useStartOnboardingMutation();
  const updateMutation = useUpdateOnboardingMutation();
  const completeMutation = useCompleteOnboardingMutation();

  const startOnboarding = () => {
    return startMutation.mutateAsync({ userId });
  };

  const updateStep = (step: number, data: Partial<OnboardingFormData>) => {
    return updateMutation.mutateAsync({ userId, step, data });
  };

  const completeOnboarding = (formData: OnboardingFormData) => {
    return completeMutation.mutateAsync({ userId, formData });
  };

  return {
    // Status
    status: statusQuery.data?.data,
    isLoading: statusQuery.isLoading,
    isError: statusQuery.isError,
    error: statusQuery.error,
    refetchStatus: statusQuery.refetch,

    // Mutations
    startOnboarding,
    updateStep,
    completeOnboarding,

    // Mutation states
    isStarting: startMutation.isPending,
    isUpdating: updateMutation.isPending,
    isCompleting: completeMutation.isPending,

    // Combined loading state
    isBusy: startMutation.isPending || updateMutation.isPending || completeMutation.isPending,
  };
};