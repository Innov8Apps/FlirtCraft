import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userService } from '../api/services/userService';
import { User, UserProfile, UserStats, UserAchievement } from '../api/types';

// Query keys
export const userKeys = {
  all: ['user'] as const,
  profile: () => [...userKeys.all, 'profile'] as const,
  stats: () => [...userKeys.all, 'stats'] as const,
  achievements: () => [...userKeys.all, 'achievements'] as const,
  limits: () => [...userKeys.all, 'limits'] as const,
};

// Get user profile
export const useUserProfile = () => {
  return useQuery({
    queryKey: userKeys.profile(),
    queryFn: userService.getProfile,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: (failureCount, error: any) => {
      // Don't retry on auth errors
      if (error?.status === 401 || error?.status === 403) {
        return false;
      }
      return failureCount < 3;
    },
  });
};

// Get user stats
export const useUserStats = () => {
  return useQuery({
    queryKey: userKeys.stats(),
    queryFn: userService.getStats,
    staleTime: 30 * 1000, // 30 seconds - stats change frequently
    refetchInterval: 60 * 1000, // Refetch every minute when component is focused
  });
};

// Get user achievements
export const useUserAchievements = () => {
  return useQuery({
    queryKey: userKeys.achievements(),
    queryFn: userService.getAchievements,
    staleTime: 10 * 60 * 1000, // 10 minutes - achievements don't change often
  });
};

// Check user limits
export const useUserLimits = () => {
  return useQuery({
    queryKey: userKeys.limits(),
    queryFn: userService.checkLimits,
    staleTime: 60 * 1000, // 1 minute - limits can change with usage
    refetchOnWindowFocus: true,
  });
};

// Update user profile
export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<UserProfile>) => userService.updateProfile(data),
    onSuccess: (updatedUser) => {
      // Update the profile cache
      queryClient.setQueryData(userKeys.profile(), updatedUser);
    },
    onError: (error) => {
      console.error('Failed to update profile:', error);
    },
  });
};

// Update user streak
export const useUpdateStreak = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userService.updateStreak,
    onSuccess: (result) => {
      // Update stats cache
      queryClient.setQueryData(userKeys.stats(), (old: UserStats | undefined) => {
        if (!old) return old;
        return {
          ...old,
          streak_count: result.streak_count,
          xp_points: old.xp_points + result.xp_earned,
        };
      });

      // Invalidate profile to get updated streak date
      queryClient.invalidateQueries({ queryKey: userKeys.profile() });
    },
    onError: (error) => {
      console.error('Failed to update streak:', error);
    },
  });
};

// Award XP points
export const useAwardXP = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ points, source }: { points: number; source: string }) =>
      userService.awardXP(points, source),
    onSuccess: (result) => {
      // Update stats cache
      queryClient.setQueryData(userKeys.stats(), (old: UserStats | undefined) => {
        if (!old) return old;
        return {
          ...old,
          xp_points: result.total_xp,
          level: result.level,
        };
      });

      // Update profile cache if level changed
      if (result.level_up) {
        queryClient.setQueryData(userKeys.profile(), (old: User | undefined) => {
          if (!old) return old;
          return {
            ...old,
            level: result.level,
            xp_points: result.total_xp,
          };
        });
      }

      // Invalidate achievements in case new ones were unlocked
      if (result.level_up) {
        queryClient.invalidateQueries({ queryKey: userKeys.achievements() });
      }
    },
    onError: (error) => {
      console.error('Failed to award XP:', error);
    },
  });
};