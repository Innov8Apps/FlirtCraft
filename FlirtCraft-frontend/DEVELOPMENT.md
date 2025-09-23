# FlirtCraft Frontend - Local Development Setup

This document provides comprehensive information for setting up and working with the FlirtCraft frontend in local development.

## ✅ Setup Status

The FlirtCraft frontend is now **fully configured** for local development with all necessary dependencies, providers, and services in place.

## 🎯 Architecture Overview

The frontend is built using:

- **React Native 0.81.4** via **Expo 54+** for cross-platform development
- **NativeBase** for UI components with custom FlirtCraft theme
- **React Query (@tanstack/react-query)** for server state management
- **Zustand** for global client state management
- **React Hook Form** for form state and validation
- **Supabase** for authentication and database
- **TypeScript** for type safety

## 📁 Project Structure

```
FlirtCraft-frontend/
├── app/                          # Expo Router pages
│   ├── _layout.tsx              # Root layout with providers
│   ├── onboarding/              # Onboarding flow screens
│   └── (tabs)/                  # Main app navigation
├── components/                   # Shared UI components
├── features/                     # Feature-specific components
│   └── onboarding/              # Onboarding components
├── lib/                         # Core libraries and utilities
│   ├── api/                     # API client and services
│   │   ├── client.ts            # HTTP client with auth
│   │   ├── types.ts             # TypeScript definitions
│   │   └── services/            # API service classes
│   ├── providers/               # React context providers
│   │   ├── ReactQueryProvider.tsx
│   │   └── NativeBaseProvider.tsx
│   ├── hooks/                   # React Query hooks
│   ├── storage/                 # Secure storage utilities
│   ├── utils/                   # Helper functions and constants
│   └── supabase.ts             # Supabase client configuration
├── stores/                      # Zustand state stores
└── .env                         # Environment configuration
```

## 🔧 Environment Configuration

The project uses environment variables for configuration:

```bash
# Supabase Configuration
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Backend API Configuration
EXPO_PUBLIC_API_URL=http://localhost:8000
```

**Current Status**: ✅ Environment variables are properly configured with working Supabase credentials.

## 🛠 Development Commands

```bash
# Start development server
npm start
# or with cache cleared
npm run dev

# Platform-specific development
npm run android    # Start Android emulator
npm run ios        # Start iOS simulator
npm run web        # Start web development

# Code Quality
npm run lint       # Run ESLint
npm run lint:fix   # Fix ESLint issues
npm run type-check # TypeScript type checking

# Testing
npm test           # Run tests
npm test:watch     # Run tests in watch mode

# Building
npm run prebuild         # Generate native code
npm run prebuild:clean   # Clean and regenerate
npm run build:android    # Build Android
npm run build:ios        # Build iOS
```

## 🎨 UI & Theming

### NativeBase Theme
- **Primary Color**: `#f59e0b` (Amber)
- **Typography**: Inter font family
- **Components**: Custom button, input, and card styles
- **Dark Mode**: Currently disabled (light mode only)

### Component Usage
```tsx
import { Box, Button, Input, VStack } from 'native-base';

function MyComponent() {
  return (
    <VStack space={4} p={4}>
      <Input placeholder="Enter text" />
      <Button>Primary Button</Button>
    </VStack>
  );
}
```

## 📡 API Integration

### Backend Connection
- **Base URL**: `http://localhost:8000/api/v1`
- **Authentication**: JWT tokens via Supabase
- **Error Handling**: Centralized error management
- **Type Safety**: Full TypeScript definitions

### Usage Examples
```tsx
import { useConversations, useCreateConversation } from '@/lib/api';

function ConversationList() {
  const { data: conversations, isLoading } = useConversations();
  const createConversation = useCreateConversation();

  const handleCreate = () => {
    createConversation.mutate({
      scenario_type: 'coffee_shop',
      difficulty_level: 'green'
    });
  };

  return (
    // Your component JSX
  );
}
```

## 🗃 State Management

### React Query (Server State)
- **Caching**: 5-minute stale time, 10-minute garbage collection
- **Retry Logic**: Smart retry for network errors
- **Background Updates**: Automatic refetching
- **Optimistic Updates**: Immediate UI feedback

### Zustand (Client State)
- **Onboarding Progress**: Form step tracking
- **App Preferences**: Theme, notifications, etc.
- **Persistent Storage**: Automatic persistence

### React Hook Form (Form State)
- **Validation**: Zod schema validation
- **Type Safety**: Full TypeScript integration
- **Performance**: Minimal re-renders

## 🔐 Security & Storage

### Secure Storage
```tsx
import { secureStorage } from '@/lib/storage/secureStorage';

// Store encrypted data
await secureStorage.setAuthToken(token);
await secureStorage.setUserPreferences(preferences);

// Retrieve encrypted data
const token = await secureStorage.getAuthToken();
const prefs = await secureStorage.getUserPreferences();
```

### Authentication
- **Provider**: Supabase Auth
- **Token Storage**: Encrypted in Expo SecureStore
- **Auto-refresh**: Automatic token renewal
- **Session Management**: Persistent sessions

## 🧪 Testing Strategy

### Unit Testing
- **Framework**: Jest + React Native Testing Library
- **Components**: Component behavior testing
- **Hooks**: Custom hook testing
- **Services**: API service testing

### Type Safety
- **TypeScript**: Strict mode enabled
- **API Types**: Generated from backend schema
- **Runtime Validation**: Zod schemas

## 📱 Platform Adaptations

### React Native
- **Navigation**: Expo Router file-based routing
- **Gestures**: React Native Gesture Handler
- **Animations**: React Native Reanimated 3
- **Platform APIs**: Expo modules for device features

### Cross-Platform Considerations
- **Styling**: NativeBase handles platform differences
- **Navigation**: Consistent behavior across platforms
- **Storage**: Secure storage on all platforms

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Development**:
   ```bash
   npm start
   ```

4. **Choose Platform**:
   - Press `a` for Android
   - Press `i` for iOS
   - Press `w` for Web

## 🐛 Troubleshooting

### Common Issues

1. **Metro bundler issues**:
   ```bash
   npm run dev  # Starts with cache cleared
   ```

2. **Type errors**:
   ```bash
   npm run type-check
   ```

3. **Dependency issues**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Expo cache issues**:
   ```bash
   npx expo start -c
   ```

### Performance Optimization
- **Bundle Analysis**: Use Expo's built-in analyzer
- **Image Optimization**: Expo Image with caching
- **Memory Management**: React Query automatic cleanup
- **Network Optimization**: Request deduplication

## 🔗 Backend Integration

### API Endpoints
The frontend is configured to work with these backend endpoints:

- **Authentication**: `/api/v1/auth/*`
- **Onboarding**: `/api/v1/onboarding/*`
- **Scenarios**: `/api/v1/scenarios/*`
- **Conversations**: `/api/v1/conversations/*`
- **Analytics**: `/api/v1/analytics/*`

### Real-time Features
- **WebSocket**: Planned for live conversation features
- **Push Notifications**: Expo Notifications configured
- **Background Sync**: React Query background updates

## 📚 Documentation

- **API Documentation**: Available at `/api/v1/docs` when backend is running
- **Component Storybook**: Planned for component documentation
- **Architecture Guide**: See `/docs/architecture-output.md`

## 🤝 Contributing

1. **Code Style**: Follow ESLint configuration
2. **Testing**: Add tests for new features
3. **Type Safety**: Maintain strict TypeScript
4. **Documentation**: Update relevant docs

---

**Status**: ✅ **Ready for Local Development**

The FlirtCraft frontend is fully configured and ready for active development. All core systems are in place, and the development environment is optimized for productivity.