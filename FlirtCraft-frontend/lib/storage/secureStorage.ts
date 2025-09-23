import * as SecureStore from 'expo-secure-store';
import * as Crypto from 'crypto-js';

class SecureStorageService {
  private encryptionKey: string;

  constructor() {
    // In a real app, this should be generated or derived from device-specific data
    this.encryptionKey = 'flirtcraft-secure-key-2024';
  }

  private encrypt(data: string): string {
    return Crypto.AES.encrypt(data, this.encryptionKey).toString();
  }

  private decrypt(encryptedData: string): string {
    const bytes = Crypto.AES.decrypt(encryptedData, this.encryptionKey);
    return bytes.toString(Crypto.enc.Utf8);
  }

  async setItem(key: string, value: string): Promise<void> {
    try {
      const encryptedValue = this.encrypt(value);
      await SecureStore.setItemAsync(key, encryptedValue);
    } catch (error) {
      console.error('SecureStorage setItem error:', error);
      throw error;
    }
  }

  async getItem(key: string): Promise<string | null> {
    try {
      const encryptedValue = await SecureStore.getItemAsync(key);
      if (!encryptedValue) return null;
      return this.decrypt(encryptedValue);
    } catch (error) {
      console.error('SecureStorage getItem error:', error);
      return null;
    }
  }

  async removeItem(key: string): Promise<void> {
    try {
      await SecureStore.deleteItemAsync(key);
    } catch (error) {
      console.error('SecureStorage removeItem error:', error);
      throw error;
    }
  }

  async setObject(key: string, value: any): Promise<void> {
    const jsonString = JSON.stringify(value);
    await this.setItem(key, jsonString);
  }

  async getObject<T>(key: string): Promise<T | null> {
    const jsonString = await this.getItem(key);
    if (!jsonString) return null;
    try {
      return JSON.parse(jsonString) as T;
    } catch (error) {
      console.error('SecureStorage getObject parse error:', error);
      return null;
    }
  }

  // Convenience methods for common data types
  async setAuthToken(token: string): Promise<void> {
    await this.setItem('auth_token', token);
  }

  async getAuthToken(): Promise<string | null> {
    return this.getItem('auth_token');
  }

  async removeAuthToken(): Promise<void> {
    await this.removeItem('auth_token');
  }

  async setUserPreferences(preferences: any): Promise<void> {
    await this.setObject('user_preferences', preferences);
  }

  async getUserPreferences<T>(): Promise<T | null> {
    return this.getObject<T>('user_preferences');
  }
}

export const secureStorage = new SecureStorageService();