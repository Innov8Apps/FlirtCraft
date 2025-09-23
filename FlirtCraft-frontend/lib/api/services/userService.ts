import apiClient from '../client';
import { User, UserProfile, UserStats, UserAchievement } from '../types';

export class UserService {
  // Get current user profile
  async getProfile(): Promise<User> {
    return apiClient.get<User>('/users/profile');
  }

  // Update user profile
  async updateProfile(data: Partial<UserProfile>): Promise<User> {
    return apiClient.put<User>('/users/profile', data);
  }

  // Get user stats (XP, level, streak, etc.)
  async getStats(): Promise<UserStats> {
    return apiClient.get<UserStats>('/users/stats');
  }

  // Update user streak
  async updateStreak(): Promise<{ streak_count: number; xp_earned: number }> {
    return apiClient.post<{ streak_count: number; xp_earned: number }>('/users/streak');
  }

  // Get user achievements
  async getAchievements(): Promise<UserAchievement[]> {
    return apiClient.get<UserAchievement[]>('/users/achievements');
  }

  // Award XP points
  async awardXP(points: number, source: string): Promise<{ total_xp: number; level: number; level_up: boolean }> {
    return apiClient.post<{ total_xp: number; level: number; level_up: boolean }>('/users/xp', {
      points,
      source,
    });
  }

  // Check premium status and limits
  async checkLimits(): Promise<{
    daily_conversations_used: number;
    daily_limit: number;
    premium_tier: string;
    premium_expires_at?: string;
    can_start_conversation: boolean;
  }> {
    return apiClient.get('/users/limits');
  }
}

export const userService = new UserService();