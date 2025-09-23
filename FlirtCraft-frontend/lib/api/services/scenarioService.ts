import apiClient from '../client';
import { Scenario } from '../types';

export class ScenarioService {
  // Get all scenarios
  async getScenarios(): Promise<Scenario[]> {
    return apiClient.get<Scenario[]>('/scenarios');
  }

  // Get a specific scenario by type
  async getScenario(type: string): Promise<Scenario> {
    return apiClient.get<Scenario>(`/scenarios/${type}`);
  }

  // Get scenarios available to user (based on premium status)
  async getAvailableScenarios(): Promise<Scenario[]> {
    return apiClient.get<Scenario[]>('/scenarios', { available_only: true });
  }
}

export const scenarioService = new ScenarioService();