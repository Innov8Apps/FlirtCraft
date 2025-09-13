import AsyncStorage from '@react-native-async-storage/async-storage';

export interface LoginRateLimitState {
  attemptCount: number;
  cooldownEndTime: number | null;
  lastAttemptTime: number;
}

export interface LoginRateLimitStatus {
  isInCooldown: boolean;
  countdownSeconds: number;
  attemptCount: number;
  cooldownDuration: number;
}

class LoginRateLimitService {
  private static readonly STORAGE_KEY = 'login_attempts_rate_limit';
  private static readonly MAX_ATTEMPTS = 5; // 5 attempts before cooldown
  private static readonly COOLDOWN_DURATION = 300; // 5 minutes (300 seconds)
  private static readonly RESET_AFTER_HOURS = 24; // Reset attempts after 24 hours of inactivity

  /**
   * Get current rate limit state from storage
   */
  private async getRateLimitState(): Promise<LoginRateLimitState> {
    try {
      const stored = await AsyncStorage.getItem(LoginRateLimitService.STORAGE_KEY);
      if (!stored) {
        return { attemptCount: 0, cooldownEndTime: null, lastAttemptTime: 0 };
      }

      const state: LoginRateLimitState = JSON.parse(stored);

      // Check if we should reset due to long inactivity
      const now = Date.now();
      const hoursSinceLastAttempt = (now - state.lastAttemptTime) / (1000 * 60 * 60);

      if (hoursSinceLastAttempt >= LoginRateLimitService.RESET_AFTER_HOURS) {
        return { attemptCount: 0, cooldownEndTime: null, lastAttemptTime: now };
      }

      return state;
    } catch (error) {
      console.error('Error reading login rate limit state:', error);
      return { attemptCount: 0, cooldownEndTime: null, lastAttemptTime: 0 };
    }
  }

  /**
   * Save rate limit state to storage
   */
  private async saveRateLimitState(state: LoginRateLimitState): Promise<void> {
    try {
      await AsyncStorage.setItem(LoginRateLimitService.STORAGE_KEY, JSON.stringify(state));
    } catch (error) {
      console.error('Error saving login rate limit state:', error);
    }
  }

  /**
   * Get user-friendly message for rate limit
   */
  private getFormattedRateLimitMessage(attemptCount: number, cooldownSeconds: number): string {
    const minutes = Math.floor(cooldownSeconds / 60);
    const seconds = cooldownSeconds % 60;
    const timeString = minutes > 0 ? `${minutes}:${seconds.toString().padStart(2, '0')}` : `${seconds} seconds`;

    return `Too many failed login attempts. Please wait ${timeString} before trying again.`;
  }

  /**
   * Track a failed login attempt
   */
  async trackFailedAttempt(): Promise<void> {
    const state = await this.getRateLimitState();
    const now = Date.now();

    const newState: LoginRateLimitState = {
      attemptCount: state.attemptCount + 1,
      cooldownEndTime: null,
      lastAttemptTime: now,
    };

    // Set cooldown if we've reached the maximum attempts
    if (newState.attemptCount >= LoginRateLimitService.MAX_ATTEMPTS) {
      newState.cooldownEndTime = now + (LoginRateLimitService.COOLDOWN_DURATION * 1000);
    }

    await this.saveRateLimitState(newState);
  }

  /**
   * Get current rate limit status
   */
  async getRateLimitStatus(): Promise<LoginRateLimitStatus> {
    const state = await this.getRateLimitState();
    const now = Date.now();

    let isInCooldown = false;
    let countdownSeconds = 0;
    const cooldownDuration = LoginRateLimitService.COOLDOWN_DURATION;

    if (state.cooldownEndTime && state.cooldownEndTime > now) {
      isInCooldown = true;
      countdownSeconds = Math.ceil((state.cooldownEndTime - now) / 1000);
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
   * Reset rate limit (for successful login or manual reset)
   */
  async resetRateLimit(): Promise<void> {
    const state: LoginRateLimitState = {
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
      await AsyncStorage.removeItem(LoginRateLimitService.STORAGE_KEY);
      console.log('Login rate limit storage cleared');
    } catch (error) {
      console.error('Error clearing login rate limit storage:', error);
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

export const loginRateLimitService = new LoginRateLimitService();