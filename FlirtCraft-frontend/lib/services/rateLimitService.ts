import AsyncStorage from '@react-native-async-storage/async-storage';

export interface RateLimitState {
  attemptCount: number;
  cooldownEndTime: number | null;
  lastAttemptTime: number;
}

export interface RateLimitStatus {
  isInCooldown: boolean;
  countdownSeconds: number;
  attemptCount: number;
  cooldownDuration: number;
}

class RateLimitService {
  private static readonly STORAGE_KEY = 'email_validation_rate_limit';
  private static readonly COOLDOWN_THRESHOLDS = [
    { attempts: 3, cooldown: 60 },   // 60 seconds after 3 attempts
    { attempts: 6, cooldown: 120 },  // 120 seconds after 6 attempts
    { attempts: 9, cooldown: 180 },  // 180 seconds after 9 attempts
    { attempts: 12, cooldown: 180 }, // 180 seconds after 12+ attempts (repeating)
  ];
  private static readonly RESET_AFTER_HOURS = 24; // Reset attempts after 24 hours of inactivity

  /**
   * Get current rate limit state from storage
   */
  private async getRateLimitState(): Promise<RateLimitState> {
    try {
      const stored = await AsyncStorage.getItem(RateLimitService.STORAGE_KEY);
      if (!stored) {
        return { attemptCount: 0, cooldownEndTime: null, lastAttemptTime: 0 };
      }

      const state: RateLimitState = JSON.parse(stored);

      // Check if we should reset due to long inactivity
      const now = Date.now();
      const hoursSinceLastAttempt = (now - state.lastAttemptTime) / (1000 * 60 * 60);

      if (hoursSinceLastAttempt >= RateLimitService.RESET_AFTER_HOURS) {
        return { attemptCount: 0, cooldownEndTime: null, lastAttemptTime: now };
      }

      return state;
    } catch (error) {
      console.error('Error reading rate limit state:', error);
      return { attemptCount: 0, cooldownEndTime: null, lastAttemptTime: 0 };
    }
  }

  /**
   * Save rate limit state to storage
   */
  private async saveRateLimitState(state: RateLimitState): Promise<void> {
    try {
      await AsyncStorage.setItem(RateLimitService.STORAGE_KEY, JSON.stringify(state));
    } catch (error) {
      console.error('Error saving rate limit state:', error);
    }
  }

  /**
   * Calculate cooldown duration based on attempt count
   */
  private calculateCooldownDuration(attemptCount: number): number {
    for (const threshold of RateLimitService.COOLDOWN_THRESHOLDS) {
      if (attemptCount <= threshold.attempts) {
        return threshold.cooldown;
      }
    }
    // For attempts beyond 12, use the last threshold (180 seconds)
    return RateLimitService.COOLDOWN_THRESHOLDS[RateLimitService.COOLDOWN_THRESHOLDS.length - 1].cooldown;
  }

  /**
   * Get user-friendly message for rate limit
   */
  private getFormattedRateLimitMessage(attemptCount: number, cooldownSeconds: number): string {
    const minutes = Math.floor(cooldownSeconds / 60);
    const seconds = cooldownSeconds % 60;
    const timeString = minutes > 0 ? `${minutes}:${seconds.toString().padStart(2, '0')}` : `${seconds} seconds`;

    if (attemptCount <= 3) {
      return `Too many attempts with existing emails. Please wait ${timeString} before trying again.`;
    } else if (attemptCount <= 6) {
      return `Multiple failed attempts detected. Please wait ${timeString} before continuing.`;
    } else {
      return `Too many failed attempts. Please wait ${timeString} before trying again.`;
    }
  }

  /**
   * Track a failed email validation attempt
   */
  async trackFailedAttempt(): Promise<void> {
    const state = await this.getRateLimitState();
    const now = Date.now();

    const newState: RateLimitState = {
      attemptCount: state.attemptCount + 1,
      cooldownEndTime: null,
      lastAttemptTime: now,
    };

    // Only set cooldown if we've reached a threshold
    const shouldSetCooldown = RateLimitService.COOLDOWN_THRESHOLDS.some(
      threshold => newState.attemptCount >= threshold.attempts
    );

    if (shouldSetCooldown) {
      // Calculate cooldown duration
      const cooldownDuration = this.calculateCooldownDuration(newState.attemptCount);
      // Set cooldown end time
      newState.cooldownEndTime = now + (cooldownDuration * 1000);
    }

    await this.saveRateLimitState(newState);
  }

  /**
   * Get current rate limit status
   */
  async getRateLimitStatus(): Promise<RateLimitStatus> {
    const state = await this.getRateLimitState();
    const now = Date.now();

    let isInCooldown = false;
    let countdownSeconds = 0;
    let cooldownDuration = 0;

    if (state.cooldownEndTime && state.cooldownEndTime > now) {
      isInCooldown = true;
      countdownSeconds = Math.ceil((state.cooldownEndTime - now) / 1000);
      cooldownDuration = this.calculateCooldownDuration(state.attemptCount);
    }

    return {
      isInCooldown,
      countdownSeconds,
      attemptCount: state.attemptCount,
      cooldownDuration,
    };
  }

  /**
   * Get rate limit error message
   */
  async getRateLimitMessage(): Promise<string> {
    const status = await this.getRateLimitStatus();
    return this.getFormattedRateLimitMessage(status.attemptCount, status.countdownSeconds);
  }

  /**
   * Reset rate limit (for successful validation or manual reset)
   */
  async resetRateLimit(): Promise<void> {
    const state: RateLimitState = {
      attemptCount: 0,
      cooldownEndTime: null,
      lastAttemptTime: Date.now(),
    };

    await this.saveRateLimitState(state);
  }

  /**
   * Clear all rate limit data from storage (for testing/debugging)
   */
  async clearRateLimitStorage(): Promise<void> {
    try {
      await AsyncStorage.removeItem(RateLimitService.STORAGE_KEY);
      console.log('Rate limit storage cleared');
    } catch (error) {
      console.error('Error clearing rate limit storage:', error);
    }
  }

  /**
   * Check if action is allowed (not in cooldown)
   */
  async isActionAllowed(): Promise<boolean> {
    const status = await this.getRateLimitStatus();
    return !status.isInCooldown;
  }

  /**
   * Start countdown timer and return cleanup function
   */
  startCountdownTimer(
    onTick: (secondsRemaining: number) => void,
    onComplete: () => void
  ): () => void {
    let intervalId: ReturnType<typeof setInterval> | null = null;

    const checkStatus = async () => {
      const status = await this.getRateLimitStatus();

      if (!status.isInCooldown) {
        if (intervalId) {
          clearInterval(intervalId);
        }
        onComplete();
        return;
      }

      onTick(status.countdownSeconds);
    };

    // Check immediately
    checkStatus();

    // Set up interval to check every second
    intervalId = setInterval(checkStatus, 1000);

    // Return cleanup function
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }
}

export const rateLimitService = new RateLimitService();