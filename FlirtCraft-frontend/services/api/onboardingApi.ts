/**
 * Onboarding API Integration
 * Connects to FlirtCraft backend endpoints for onboarding flow
 */

import { OnboardingFormData } from '@/features/onboarding/types';

// API Base URL - In production, this would come from environment variables
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

// Request/Response Types
export interface OnboardingStartRequest {
  userId: string;
}

export interface OnboardingUpdateRequest {
  userId: string;
  step: number;
  data: Partial<OnboardingFormData>;
}

export interface OnboardingCompleteRequest {
  userId: string;
  formData: OnboardingFormData;
}

export interface OnboardingStatusResponse {
  success: boolean;
  data: {
    isCompleted: boolean;
    currentStep: number;
    formData?: Partial<OnboardingFormData>;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    timestamp: string;
  };
}

// API Client helper
class OnboardingApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error?.message || 'API request failed');
      }

      return data;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  // Start onboarding session
  async startOnboarding(request: OnboardingStartRequest): Promise<ApiResponse<{ sessionId: string }>> {
    return this.makeRequest('/api/v1/onboarding/start', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Update onboarding step
  async updateOnboarding(request: OnboardingUpdateRequest): Promise<ApiResponse<{ updated: boolean }>> {
    return this.makeRequest('/api/v1/onboarding/update', {
      method: 'PUT',
      body: JSON.stringify(request),
    });
  }

  // Get onboarding status
  async getOnboardingStatus(userId: string): Promise<OnboardingStatusResponse> {
    return this.makeRequest(`/api/v1/onboarding/status?userId=${userId}`, {
      method: 'GET',
    });
  }

  // Complete onboarding
  async completeOnboarding(request: OnboardingCompleteRequest): Promise<ApiResponse<{ completed: boolean }>> {
    return this.makeRequest('/api/v1/onboarding/complete', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }
}

// Create API client instance
export const onboardingApi = new OnboardingApiClient(API_BASE_URL);

// Mock API functions for development/testing
export const mockOnboardingApi = {
  async startOnboarding(request: OnboardingStartRequest): Promise<ApiResponse<{ sessionId: string }>> {
    await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
    return {
      success: true,
      data: { sessionId: `session_${Date.now()}` },
      meta: { timestamp: new Date().toISOString() },
    };
  },

  async updateOnboarding(request: OnboardingUpdateRequest): Promise<ApiResponse<{ updated: boolean }>> {
    await new Promise(resolve => setTimeout(resolve, 300));
    console.log('Mock API - Update onboarding:', request);
    return {
      success: true,
      data: { updated: true },
      meta: { timestamp: new Date().toISOString() },
    };
  },

  async getOnboardingStatus(userId: string): Promise<OnboardingStatusResponse> {
    await new Promise(resolve => setTimeout(resolve, 200));
    return {
      success: true,
      data: {
        isCompleted: false,
        currentStep: 0,
      },
    };
  },

  async completeOnboarding(request: OnboardingCompleteRequest): Promise<ApiResponse<{ completed: boolean }>> {
    await new Promise(resolve => setTimeout(resolve, 800));
    console.log('Mock API - Complete onboarding:', request);
    return {
      success: true,
      data: { completed: true },
      meta: { timestamp: new Date().toISOString() },
    };
  },
};

// Export the appropriate API client based on environment
export const api = process.env.NODE_ENV === 'production' ? onboardingApi : mockOnboardingApi;