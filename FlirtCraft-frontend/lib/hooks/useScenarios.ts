import { useQuery } from '@tanstack/react-query';
import { scenarioService } from '../api/services/scenarioService';
import { Scenario } from '../api/types';

// Query keys
export const scenarioKeys = {
  all: ['scenarios'] as const,
  lists: () => [...scenarioKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...scenarioKeys.lists(), { filters }] as const,
  details: () => [...scenarioKeys.all, 'detail'] as const,
  detail: (type: string) => [...scenarioKeys.details(), type] as const,
};

// Get all scenarios
export const useScenarios = () => {
  return useQuery({
    queryKey: scenarioKeys.lists(),
    queryFn: scenarioService.getScenarios,
    staleTime: 30 * 60 * 1000, // 30 minutes - scenarios rarely change
  });
};

// Get scenarios available to current user
export const useAvailableScenarios = () => {
  return useQuery({
    queryKey: scenarioKeys.list({ available_only: true }),
    queryFn: scenarioService.getAvailableScenarios,
    staleTime: 5 * 60 * 1000, // 5 minutes - depends on user premium status
  });
};

// Get specific scenario
export const useScenario = (type: string) => {
  return useQuery({
    queryKey: scenarioKeys.detail(type),
    queryFn: () => scenarioService.getScenario(type),
    enabled: !!type,
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};