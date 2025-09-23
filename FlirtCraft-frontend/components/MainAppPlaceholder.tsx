import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeIn, SlideInUp } from 'react-native-reanimated';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { supabase } from '@/lib/supabase';
import { useOnboardingStore } from '@/stores/onboardingStore';
import OnboardingButton from './onboarding/OnboardingButton';

type TabType = 'home' | 'chat' | 'scenarios' | 'profile';

interface TabBarItemProps {
  tab: TabType;
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  active: boolean;
  onPress: () => void;
}

const TabBarItem: React.FC<TabBarItemProps> = ({ tab, icon, label, active, onPress }) => {
  return (
    <TouchableOpacity
      style={styles.tabBarItem}
      onPress={onPress}
      accessibilityRole="tab"
      accessibilityState={{ selected: active }}
      accessibilityLabel={`${label} tab`}
    >
      <Ionicons
        name={icon}
        size={24}
        color={active ? '#FF6B35' : '#9CA3AF'}
      />
      <Text style={[styles.tabBarLabel, active && styles.tabBarLabelActive]}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

export default function MainAppPlaceholder() {
  const [activeTab, setActiveTab] = useState<TabType>('home');
  const [isResetting, setIsResetting] = useState(false);
  const { resetOnboarding } = useOnboardingStore();

  const handleResetApp = async () => {
    Alert.alert(
      'Reset App',
      'This will sign you out and clear all data. You can test registration again.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            setIsResetting(true);
            try {
              // Sign out from Supabase
              await supabase.auth.signOut();

              // Clear all local storage
              await AsyncStorage.clear();

              // Reset onboarding state
              resetOnboarding();

              // Show success message
              Alert.alert(
                'App Reset',
                'App has been reset successfully. You can now test the registration flow again.',
                [{ text: 'OK' }]
              );
            } catch (error) {
              console.error('Failed to reset app:', error);
              Alert.alert('Error', 'Failed to reset app. Please try again.');
            } finally {
              setIsResetting(false);
            }
          },
        },
      ]
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'home':
        return (
          <ScrollView contentContainerStyle={styles.tabContent}>
            <Animated.View entering={FadeIn} style={styles.welcomeContainer}>
              <View style={styles.logoContainer}>
                <Ionicons name="heart" size={64} color="#FF6B35" />
              </View>
              <Text style={styles.welcomeTitle}>
                Welcome to FlirtCraft! 🎉
              </Text>
              <Text style={styles.welcomeSubtitle}>
                You've successfully completed the onboarding process
              </Text>
            </Animated.View>

            <Animated.View entering={SlideInUp.delay(200)} style={styles.infoCard}>
              <View style={styles.infoIconContainer}>
                <Ionicons name="information-circle" size={24} color="#3B82F6" />
              </View>
              <View style={styles.infoContent}>
                <Text style={styles.infoTitle}>Development Build</Text>
                <Text style={styles.infoDescription}>
                  This is a placeholder interface for testing the registration flow. Main features are in development.
                </Text>
              </View>
            </Animated.View>

            <Animated.View entering={SlideInUp.delay(400)} style={styles.featuresContainer}>
              <Text style={styles.featuresTitle}>Coming Soon:</Text>
              <View style={styles.featuresList}>
                <View style={styles.featureItem}>
                  <Ionicons name="checkmark-circle" size={16} color="#4CAF50" />
                  <Text style={styles.featureText}>AI conversation practice</Text>
                </View>
                <View style={styles.featureItem}>
                  <Ionicons name="checkmark-circle" size={16} color="#4CAF50" />
                  <Text style={styles.featureText}>Realistic scenario selection</Text>
                </View>
                <View style={styles.featureItem}>
                  <Ionicons name="checkmark-circle" size={16} color="#4CAF50" />
                  <Text style={styles.featureText}>Detailed feedback system</Text>
                </View>
                <View style={styles.featureItem}>
                  <Ionicons name="checkmark-circle" size={16} color="#4CAF50" />
                  <Text style={styles.featureText}>Progress tracking</Text>
                </View>
              </View>
            </Animated.View>
          </ScrollView>
        );

      case 'chat':
        return (
          <View style={styles.placeholderContainer}>
            <View style={styles.placeholderIconContainer}>
              <Ionicons name="chatbubble-ellipses" size={64} color="#FF6B35" />
            </View>
            <Text style={styles.placeholderTitle}>Chat Feature</Text>
            <Text style={styles.placeholderDescription}>
              Custom conversation practice will be available here. Practice with AI partners in realistic scenarios.
            </Text>
            <View style={styles.statusBadge}>
              <Text style={styles.statusText}>Feature in development</Text>
            </View>
          </View>
        );

      case 'scenarios':
        return (
          <View style={styles.placeholderContainer}>
            <View style={styles.placeholderIconContainer}>
              <Ionicons name="grid" size={64} color="#FF6B35" />
            </View>
            <Text style={styles.placeholderTitle}>Scenarios Feature</Text>
            <Text style={styles.placeholderDescription}>
              Choose from various practice scenarios like coffee shops, bookstores, and social events.
            </Text>
            <View style={[styles.statusBadge, styles.statusBadgeInfo]}>
              <Text style={[styles.statusText, styles.statusTextInfo]}>Feature in development</Text>
            </View>
          </View>
        );

      case 'profile':
        return (
          <ScrollView contentContainerStyle={styles.tabContent}>
            <Animated.View entering={FadeIn} style={styles.profileHeader}>
              <Text style={styles.profileTitle}>Profile</Text>
              <Text style={styles.profileSubtitle}>
                Manage your account and preferences
              </Text>
            </Animated.View>

            <Animated.View entering={SlideInUp.delay(200)} style={styles.profileSection}>
              <Text style={styles.sectionTitle}>User Information</Text>
              <View style={styles.profileInfo}>
                <Text style={styles.profileInfoText}>
                  Profile features will be available here in the full app.
                </Text>
              </View>
            </Animated.View>

            <Animated.View entering={SlideInUp.delay(400)} style={styles.developmentSection}>
              <Text style={styles.sectionTitle}>Development Tools</Text>
              <Text style={styles.developmentDescription}>
                Use this to test the registration flow multiple times during development.
              </Text>

              <View style={styles.resetContainer}>
                <OnboardingButton
                  title={isResetting ? "Resetting..." : "Reset App & Clear Data"}
                  onPress={handleResetApp}
                  variant="secondary"
                  loading={isResetting}
                  disabled={isResetting}
                  accessibilityLabel="Reset application data for testing"
                  accessibilityHint="This will clear all data and return to onboarding"
                />
              </View>

              <View style={styles.warningNote}>
                <Ionicons name="warning" size={16} color="#F59E0B" />
                <Text style={styles.warningText}>
                  This reset function is only available in development builds
                </Text>
              </View>
            </Animated.View>
          </ScrollView>
        );

      default:
        return null;
    }
  };

  const tabs = [
    { id: 'home' as TabType, icon: 'home' as keyof typeof Ionicons.glyphMap, label: 'Home' },
    { id: 'chat' as TabType, icon: 'chatbubble-ellipses' as keyof typeof Ionicons.glyphMap, label: 'Chat' },
    { id: 'scenarios' as TabType, icon: 'grid' as keyof typeof Ionicons.glyphMap, label: 'Scenarios' },
    { id: 'profile' as TabType, icon: 'person' as keyof typeof Ionicons.glyphMap, label: 'Profile' },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#FFFFFF', '#FAFAFA']}
        style={styles.backgroundGradient}
      >
        {/* Main Content */}
        <View style={styles.content}>
          {renderTabContent()}
        </View>

        {/* Bottom Tab Bar */}
        <View style={styles.tabBar}>
          {tabs.map((tab) => (
            <TabBarItem
              key={tab.id}
              tab={tab.id}
              icon={tab.icon}
              label={tab.label}
              active={activeTab === tab.id}
              onPress={() => setActiveTab(tab.id)}
            />
          ))}
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  backgroundGradient: {
    flex: 1,
  },
  content: {
    flex: 1,
  },
  tabContent: {
    padding: 24,
    paddingBottom: 100, // Account for tab bar
  },
  welcomeContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  logoContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#FFF7F4',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 2,
    borderColor: '#FDBA8C',
  },
  welcomeTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1A1A1A',
    textAlign: 'center',
    marginBottom: 8,
  },
  welcomeSubtitle: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
  },
  infoCard: {
    flexDirection: 'row',
    backgroundColor: '#EBF8FF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#BFDBFE',
  },
  infoIconContainer: {
    marginRight: 12,
  },
  infoContent: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1E40AF',
    marginBottom: 4,
  },
  infoDescription: {
    fontSize: 14,
    color: '#3730A3',
    lineHeight: 20,
  },
  featuresContainer: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#E5E5E5',
  },
  featuresTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 16,
  },
  featuresList: {
    gap: 12,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureText: {
    fontSize: 14,
    color: '#4B5563',
    marginLeft: 8,
  },
  placeholderContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  placeholderIconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#FFF7F4',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  placeholderTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 12,
  },
  placeholderDescription: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 24,
  },
  statusBadge: {
    backgroundColor: '#FEF3C7',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#F59E0B',
  },
  statusBadgeInfo: {
    backgroundColor: '#DBEAFE',
    borderColor: '#3B82F6',
  },
  statusText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#92400E',
  },
  statusTextInfo: {
    color: '#1D4ED8',
  },
  profileHeader: {
    alignItems: 'center',
    marginBottom: 32,
  },
  profileTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  profileSubtitle: {
    fontSize: 16,
    color: '#6B7280',
  },
  profileSection: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 16,
  },
  profileInfo: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E5E5',
  },
  profileInfoText: {
    fontSize: 14,
    color: '#6B7280',
  },
  developmentSection: {
    backgroundColor: '#FEF2F2',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#FECACA',
  },
  developmentDescription: {
    fontSize: 14,
    color: '#7F1D1D',
    marginBottom: 20,
    lineHeight: 20,
  },
  resetContainer: {
    marginBottom: 16,
  },
  warningNote: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFBEB',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#FDE68A',
  },
  warningText: {
    fontSize: 12,
    color: '#92400E',
    marginLeft: 8,
    flex: 1,
  },
  tabBar: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E5E5E5',
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  tabBarItem: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 8,
  },
  tabBarLabel: {
    fontSize: 12,
    color: '#9CA3AF',
    marginTop: 4,
    fontWeight: '500',
  },
  tabBarLabelActive: {
    color: '#FF6B35',
  },
});