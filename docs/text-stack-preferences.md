# User Requested Tech Stack Documentation

The user's preferred tech stack is below.

You are permitted to expand upon it with new tools, but you can't replace any of these without first getting explicit permission. And please suggest where and when relevant

For anything not explicitly outlined, always prefer built-in Expo solutions

## Frontend

### Core

- React Native via Expo (already configured)
- Typescript
- EAS Build

### Data Flow & State

- Zustand for state management
- React Query for Server state
- React Hook Form for Form state

### Navigation

- React Navigation
- Expo Linking for deep linking (if needed based on features)

### UI, Styling, & Interactivity

- React Native Reanimated for animations
- React Native Gesture Handler
- Expo Haptics for any haptic feedback
- NativeBase for core component library
- NativeWind for styling approach
- Custom design token system
- Expo Vector Icons

### Networking

- Fetch API for http requests
- GraphQL

### Data Storage
- Expo SecureStore
- External Supabase instance for primary app database

### Authentication & Authorization
- Supabase Auth
- Expo LocalAuthentication for Biometrics

### Other
- Expo Notifications for app notifications
- Expo Localization
- Jest for unit testing

## Backend

### Core API
- FastAPI backend
- Supabase database
- SQLAlchemy for ORM

### LLM Integrations

OpenAI API for core LLM work

### Authentication & Security

- Supabase Auth

### Background Jobs
- Redis + RQ

### CI/CD
- Github Actions
- Sentry for error monitoring

### Deployment
- Railway
- Docker Containers