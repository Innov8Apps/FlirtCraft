// Test utility to demonstrate and verify rate limiting functionality
// This is for development/testing purposes only

import { rateLimitService } from './rateLimitService';

export class RateLimitTester {
  /**
   * Simulate multiple failed email validation attempts
   */
  static async simulateFailedAttempts(count: number): Promise<void> {
    console.log(`🧪 Simulating ${count} failed email validation attempts...`);

    for (let i = 1; i <= count; i++) {
      await rateLimitService.trackFailedAttempt();
      const status = await rateLimitService.getRateLimitStatus();

      console.log(`❌ Attempt ${i}:`);
      console.log(`   - Total attempts: ${status.attemptCount}`);
      console.log(`   - In cooldown: ${status.isInCooldown}`);
      if (status.isInCooldown) {
        console.log(`   - Cooldown seconds: ${status.countdownSeconds}`);
        console.log(`   - Cooldown duration: ${status.cooldownDuration}s`);
      }
      console.log('');
    }
  }

  /**
   * Check current rate limit status
   */
  static async checkStatus(): Promise<void> {
    const status = await rateLimitService.getRateLimitStatus();
    const message = await rateLimitService.getRateLimitMessage();

    console.log('📊 Current Rate Limit Status:');
    console.log(`   - Attempt count: ${status.attemptCount}`);
    console.log(`   - In cooldown: ${status.isInCooldown}`);
    console.log(`   - Countdown seconds: ${status.countdownSeconds}`);
    console.log(`   - Message: ${message}`);
  }

  /**
   * Reset rate limiting
   */
  static async reset(): Promise<void> {
    await rateLimitService.resetRateLimit();
    console.log('🔄 Rate limit has been reset');
  }

  /**
   * Test progressive timeout system
   */
  static async testProgressiveTimeouts(): Promise<void> {
    console.log('🚀 Testing Progressive Timeout System\n');

    // Reset first
    await this.reset();

    // Test thresholds
    const testCases = [
      { attempts: 3, expectedCooldown: 60 },
      { attempts: 6, expectedCooldown: 120 },
      { attempts: 9, expectedCooldown: 180 },
      { attempts: 12, expectedCooldown: 180 },
      { attempts: 15, expectedCooldown: 180 }, // Should still be 180
    ];

    for (const testCase of testCases) {
      await this.reset();
      await this.simulateFailedAttempts(testCase.attempts);

      const status = await rateLimitService.getRateLimitStatus();
      const actualCooldown = status.cooldownDuration;

      console.log(`🎯 Test: ${testCase.attempts} attempts`);
      console.log(`   Expected cooldown: ${testCase.expectedCooldown}s`);
      console.log(`   Actual cooldown: ${actualCooldown}s`);
      console.log(`   ✅ ${actualCooldown === testCase.expectedCooldown ? 'PASS' : 'FAIL'}\n`);
    }
  }

  /**
   * Simulate countdown timer behavior
   */
  static async simulateCountdown(): Promise<void> {
    console.log('⏱️ Simulating countdown timer...\n');

    // Trigger rate limit
    await this.reset();
    await this.simulateFailedAttempts(3);

    // Start countdown simulation
    const cleanup = rateLimitService.startCountdownTimer(
      (secondsRemaining) => {
        console.log(`⏳ Countdown: ${Math.floor(secondsRemaining / 60)}:${(secondsRemaining % 60).toString().padStart(2, '0')}`);
      },
      () => {
        console.log('✅ Countdown complete! Rate limit cleared.');
      }
    );

    // Clean up after 10 seconds for testing
    setTimeout(() => {
      cleanup();
      console.log('🧹 Test cleanup completed');
    }, 10000);
  }
}

// Export for testing in development
export default RateLimitTester;