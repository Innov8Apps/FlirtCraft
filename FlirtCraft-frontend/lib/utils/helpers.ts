import { COLORS, XP_REWARDS } from './constants';

// Date and Time Helpers
export const formatDate = (date: string | Date): string => {
  const d = new Date(date);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatTime = (date: string | Date): string => {
  const d = new Date(date);
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatDateTime = (date: string | Date): string => {
  return `${formatDate(date)} at ${formatTime(date)}`;
};

export const timeAgo = (date: string | Date): string => {
  const now = new Date();
  const past = new Date(date);
  const diffInSeconds = Math.floor((now.getTime() - past.getTime()) / 1000);

  if (diffInSeconds < 60) return 'just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
  if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`;
  if (diffInSeconds < 31536000) return `${Math.floor(diffInSeconds / 2592000)}mo ago`;
  return `${Math.floor(diffInSeconds / 31536000)}y ago`;
};

// String Helpers
export const capitalize = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

export const truncate = (str: string, length: number = 50): string => {
  if (str.length <= length) return str;
  return str.slice(0, length) + '...';
};

export const pluralize = (count: number, singular: string, plural?: string): string => {
  if (count === 1) return `${count} ${singular}`;
  return `${count} ${plural || singular + 's'}`;
};

// Number Helpers
export const formatNumber = (num: number): string => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
};

export const clamp = (value: number, min: number, max: number): number => {
  return Math.min(Math.max(value, min), max);
};

export const randomBetween = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

// Level and XP Helpers
export const calculateLevel = (xp: number): number => {
  // Level formula: Level = floor(sqrt(XP / 100))
  return Math.floor(Math.sqrt(xp / 100)) + 1;
};

export const calculateXPForLevel = (level: number): number => {
  // XP needed for level: XP = (level - 1)^2 * 100
  return Math.pow(level - 1, 2) * 100;
};

export const calculateXPToNextLevel = (currentXP: number): { current: number; needed: number; progress: number } => {
  const currentLevel = calculateLevel(currentXP);
  const currentLevelXP = calculateXPForLevel(currentLevel);
  const nextLevelXP = calculateXPForLevel(currentLevel + 1);
  const xpInCurrentLevel = currentXP - currentLevelXP;
  const xpNeededForNext = nextLevelXP - currentLevelXP;
  const progress = xpInCurrentLevel / xpNeededForNext;

  return {
    current: xpInCurrentLevel,
    needed: xpNeededForNext,
    progress: Math.min(progress, 1),
  };
};

// Score and Rating Helpers
export const getScoreColor = (score: number): string => {
  if (score >= 90) return COLORS.SUCCESS;
  if (score >= 70) return COLORS.WARNING;
  if (score >= 50) return COLORS.PRIMARY;
  return COLORS.ERROR;
};

export const getScoreLabel = (score: number): string => {
  if (score >= 90) return 'Excellent';
  if (score >= 80) return 'Very Good';
  if (score >= 70) return 'Good';
  if (score >= 60) return 'Fair';
  if (score >= 50) return 'Needs Work';
  return 'Keep Practicing';
};

export const getDifficultyColor = (difficulty: 'green' | 'yellow' | 'red'): string => {
  switch (difficulty) {
    case 'green': return COLORS.SUCCESS;
    case 'yellow': return COLORS.WARNING;
    case 'red': return COLORS.ERROR;
    default: return COLORS.GRAY_500;
  }
};

export const getDifficultyLabel = (difficulty: 'green' | 'yellow' | 'red'): string => {
  switch (difficulty) {
    case 'green': return 'Easy';
    case 'yellow': return 'Medium';
    case 'red': return 'Hard';
    default: return 'Unknown';
  }
};

// Validation Helpers
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const isValidAge = (age: number): boolean => {
  return age >= 18 && age <= 100;
};

export const isValidAgeRange = (min: number, max: number): boolean => {
  return isValidAge(min) && isValidAge(max) && min <= max;
};

// Array Helpers
export const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

export const uniqueBy = <T>(array: T[], key: keyof T): T[] => {
  const seen = new Set();
  return array.filter(item => {
    const value = item[key];
    if (seen.has(value)) return false;
    seen.add(value);
    return true;
  });
};

// Storage Helpers
export const sanitizeStorageKey = (key: string): string => {
  return key.replace(/[^a-zA-Z0-9_-]/g, '_');
};

// Error Helpers
export const getErrorMessage = (error: unknown): string => {
  if (error instanceof Error) return error.message;
  if (typeof error === 'string') return error;
  return 'An unexpected error occurred';
};

// Async Helpers
export const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

export const retry = async <T>(
  fn: () => Promise<T>,
  attempts: number = 3,
  delayMs: number = 1000
): Promise<T> => {
  try {
    return await fn();
  } catch (error) {
    if (attempts <= 1) throw error;
    await delay(delayMs);
    return retry(fn, attempts - 1, delayMs * 2);
  }
};

// Platform Helpers
export const isWeb = (): boolean => {
  return typeof window !== 'undefined';
};

export const isNative = (): boolean => {
  return !isWeb();
};