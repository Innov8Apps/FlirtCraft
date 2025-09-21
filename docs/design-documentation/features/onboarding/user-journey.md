# Onboarding User Journey Analysis

---
title: Complete Onboarding User Journey Mapping
description: Step-by-step user experience flow with persona variations
feature: onboarding
last-updated: 2025-09-07
version: 2.0.0
related-files:
  - ./README.md
  - ./screen-states.md
  - ../../accessibility/guidelines.md
status: approved
---

## Core Experience Flow

### Screen 1: Welcome & Value Proposition

#### Entry Point
**How Users Arrive:**
- App store download and first launch
- Referral link from friend or social media
- Marketing campaign link with tracking parameters
- Organic discovery through app store search

#### State Description
**Visual Layout:**
- **Hero section**: Large, welcoming illustration of diverse people in conversation
- **Headline**: "Build Confidence in Real Conversations" (H1, center-aligned)
- **Subheading**: "Practice with AI partners in realistic scenarios before the real thing" (Body Large, center-aligned)
- **Value props**: Three key benefits with icons and brief descriptions
- **Primary CTA**: "Start Building Confidence" (PremiumButton with particle effects on press, full-width)
- **Secondary info**: "Free to try • No awkward real people • Private practice" (Caption, warm orange muted)

**Available Actions:**
- **Primary**: "Start Building Confidence" button proceeds to age verification
- **Secondary**: "Learn More" link to marketing page (opens in-app browser)
- **Tertiary**: Legal footer links (Privacy Policy, Terms of Service)

**Visual Hierarchy:**
1. Welcoming illustration draws attention first
2. Headline establishes core value proposition  
3. Subheading provides clarity and reduces anxiety
4. Value props reinforce benefits with easy scanning
5. CTA button stands out with primary styling
6. Supporting text provides reassurance without distraction

**System Feedback (Premium):**
- **Loading State**: React Native Reanimated 3 smooth app launch animation with confidence-building messaging
- **Interaction Feedback**: PremiumButton press with particle celebration, haptic feedback, and gentle bounce
- **Progress**: Orange gradient progress indicator (1 of 5) with smooth animation transitions

**Persona Adaptations:**

**Anxious Alex**: 
- Headline emphasizes "safe practice" and "no pressure"
- Value props include "Practice privately" and "Build confidence gradually"
- Additional reassurance text: "Your conversations stay completely private"

**Comeback Catherine**:
- Headline mentions "Get back in the game with confidence"  
- Value props highlight "Modern dating scenarios" and "Refresh your skills"
- Supporting text includes "Perfect for getting back out there"

**Confident Carlos**:
- Headline focuses on "Optimize your conversation skills"
- Value props emphasize "Advanced scenarios" and "Track your progress"
- CTA button text: "Level Up My Game"

**Shy Sarah**:
- Headline uses gentle language: "Build conversation confidence step by step"
- Value props stress "No judgment" and "Start at your comfort level"
- Extra reassurance: "Completely private practice environment"

---

### Screen 2: Age Verification

#### Trigger
User taps primary CTA from welcome screen

#### State Description
**Visual Layout:**
- **Progress indicator**: 2 of 5 with subtle animation
- **Headline**: "Let's make sure you're 18+" (H2, friendly tone)
- **Explanation**: Brief, non-intimidating explanation of age requirement
- **Date picker**: Large, easy-to-use date selection interface
- **Primary CTA**: "Confirm Age" (disabled until valid date selected)
- **Legal text**: Required compliance text in smaller, non-threatening font

**Available Actions:**
- **Primary**: Date selection with native platform picker
- **Secondary**: "Confirm Age" button (enabled when date validates 18+)
- **Tertiary**: Back button to return to welcome screen

**Visual Hierarchy:**
1. Progress indicator shows forward momentum
2. Friendly headline reduces legal anxiety
3. Explanation builds understanding without intimidation
4. Large date picker is easy to interact with
5. CTA button provides clear next step

**System Feedback:**
- **Validation**: Real-time validation shows when eligible age entered
- **Error State**: Clear, non-judgmental message for under-18 users
- **Success State**: Button enables with subtle color change
- **Loading**: Brief validation check with spinner

**Error Handling:**
- **Under 18**: "FlirtCraft is designed for adults 18 and over. Thanks for your interest!"
- **Invalid Date**: "Please select your birth date to continue"
- **Future Date**: "Please check your birth date entry"

---

### Screen 3: Registration/Sign In

#### Trigger
Successful age verification

#### State Description
**Visual Layout:**
- **Progress indicator**: 3 of 5 with continued progression animation
- **Headline**: "Create your FlirtCraft account" (H2, welcoming tone)
- **Toggle option**: "Already have an account? Sign In" (link button)
- **Email input**: Large, clear input field with validation
- **Password input**: Secure field with strength indicator
- **Confirm password**: Matching validation field
- **Terms agreement**: Checkboxes for Terms of Service and Privacy Policy
- **Primary CTA**: "Create Account" (disabled until valid and agreed)
- **Alternative**: "Sign In Instead" (secondary text link)

**Available Actions:**
- **Primary**: Email and password entry with real-time validation
- **Secondary**: Toggle between Sign Up and Sign In modes
- **Tertiary**: "Create Account" or "Sign In" button when validation passes
- **Navigation**: Back button returns to age verification

**Visual Hierarchy:**
1. Progress indicator maintains momentum feeling
2. Registration form most prominent with clear visual structure
3. Password strength indicator guides secure password creation
4. Terms agreement clearly visible but not overwhelming
5. CTA button provides obvious next step when requirements met

**System Feedback:**
- **Email validation**: Real-time check for valid format and availability
- **Password strength**: Visual indicator (weak/fair/strong/excellent)
- **Matching passwords**: Confirmation field validation
- **Terms agreement**: Required checkboxes with inline policy links
- **Button enablement**: CTA enables only when all requirements met
- **Accessibility**: Screen reader announcements for all validation states

**Registration Flow Features:**
- **Email availability check**: Immediate feedback if email already exists
- **Password requirements**: Clear visual indicators for all criteria
- **Show/hide password**: Toggle for password visibility
- **Auto-focus progression**: Smart focus movement between fields
- **Error recovery**: Helpful error messages with suggested actions

**Sign In Mode (Alternative):**
- **Simplified layout**: Email and password fields only
- **Remember me**: Optional checkbox for session persistence  
- **Forgot password**: Link to password recovery flow
- **Switch to registration**: "Don't have an account? Sign Up" option

**Persona Adaptations:**

**Anxious Alex**:
- Additional explanation: "Your information is encrypted and secure"
- Reassurance text: "You can update your email anytime in settings"
- Strong password help: Detailed explanation of why security matters

**Comeback Catherine**:
- Context text: "Create your account to save your progress and preferences"
- Email suggestion: "Use an email you check regularly for tips and updates"
- Quick sign-in option prominently displayed for returning users

**Confident Carlos**:
- Efficient presentation with minimal explanation text
- Auto-focus and keyboard shortcuts for rapid completion
- Option to import account from other services (if available)

**Shy Sarah**:
- Gentle explanation of why account creation helps
- Reassuring note about privacy and data protection
- Option to use nickname instead of real name (where appropriate)

**Security Features:**
- **Temporary storage**: Registration data held locally until onboarding complete
- **Password validation**: Real-time strength checking with visual feedback
- **Email verification**: Verification email sent but not required until onboarding complete
- **Error handling**: Clear, helpful messages for all validation scenarios
- **Rate limiting**: Protection against multiple registration attempts

---

### Screen 4: Preference Setup

#### Trigger
Successful account registration/sign in

#### State Description
**Visual Layout:**
- **Progress indicator**: 4 of 5 with continued progression animation
- **Headline**: "Who would you like to practice with?" (H2, inclusive language)
- **Gender selection**: Three options with inclusive icons and descriptions
  - "Men" (male icon, clean typography)
  - "Women" (female icon, matching style)  
  - "Everyone" (inclusive icon, encouraging option)
- **Age range section**: Headline "What age range interests you?"
- **Age range slider**: Visual slider with current range display (default ±5 years from user age)
- **Primary CTA**: "Continue Setup" (enabled when selections made)

**Available Actions:**
- **Primary**: Gender preference selection (single choice, required)
- **Secondary**: Age range adjustment via slider or input fields
- **Tertiary**: "Continue Setup" button proceeds when valid selections made
- **Navigation**: Back button returns to age verification

**Visual Hierarchy:**
1. Progress indicator maintains momentum feeling
2. Gender selection section most prominent with clear visual choices
3. Age range section secondary but clearly labeled
4. CTA button provides obvious next step when ready

**System Feedback:**
- **Selection feedback**: Selected option highlights with primary color
- **Range feedback**: Live update of selected range as user adjusts
- **Validation**: Button enables when minimum required selections made
- **Accessibility**: Screen reader announcements for all changes

**Persona Adaptations:**

**Anxious Alex**:
- Additional explanation: "This helps create realistic practice scenarios"
- Reassurance text: "You can change these preferences anytime"
- Default to "Everyone" to reduce decision anxiety

**Comeback Catherine**:
- Context text: "Practice with your preferred dating demographic"
- Age range defaults to slightly wider range (±7 years)
- Emphasizes "realistic scenarios" matching modern dating

**Confident Carlos**:
- Efficient presentation with minimal explanation text
- Quick selection interface with keyboard shortcuts
- Option to "Choose randomly for variety" as advanced feature

**Shy Sarah**:
- Gentle explanation of why preferences help
- Reassuring note about privacy and practice-only nature
- Option to select "Not sure yet" for gender preference

---

### Screen 5: Skill Goal Selection

#### Trigger
Completion of preference setup

#### State Description
**Visual Layout:**
- **Progress indicator**: 5 of 5, nearing completion
- **Headline**: "What conversation skills do you want to improve?" (H2)
- **Goal cards**: Three primary skill areas displayed as selectable cards
  - **Conversation Starters**: "Learn to break the ice naturally"
  - **Keeping Flow**: "Maintain engaging conversations"
  - **Storytelling**: "Share experiences compellingly"
- **Multiple selection**: Users can choose 1-3 goals
- **Secondary goals**: Expandable section for additional specific areas
- **Primary CTA**: "Start Practicing" (exciting, forward-looking)

**Available Actions:**
- **Primary**: Goal selection (1-3 goals, visual card selection)
- **Secondary**: "Show More Goals" expansion for additional options
- **Advanced**: Individual skill sliders for users who want granular control
- **Navigation**: "Start Practicing" when at least one goal selected

**Visual Hierarchy:**
1. Progress indicator shows near-completion excitement
2. Headline focuses on improvement and growth
3. Goal cards are visually prominent with clear descriptions
4. Additional options available but not overwhelming
5. CTA button emphasizes immediate action and practice

**System Feedback:**
- **Card selection**: Selected cards show checkmark and primary color border
- **Counter**: Shows "X of 3 goals selected" to guide selection
- **Expansion**: Smooth animation reveals additional goal options
- **Button state**: CTA enables and shows excitement when goals selected

**Advanced Options (Expandable):**
- Handling rejection gracefully
- Reading body language signals  
- Escalating from chat to asking out
- Dealing with nervousness
- Being authentic while flirting
- Conversation recovery after awkward moments

**Persona Adaptations:**

**Anxious Alex**:
- Pre-selects "Conversation Starters" as suggested starting point
- Emphasizes "gradual improvement" and "at your own pace"
- Additional goal: "Building confidence" prominently featured

**Comeback Catherine**:
- Highlights "Keeping Flow" and "Storytelling" as relevant skills
- Context text: "Refresh skills you may have used before"
- Advanced option: "Modern dating conversation styles"

**Confident Carlos**:
- All goals available immediately without pre-selection
- Advanced options expanded by default
- Focus on "optimization" and "skill refinement" language

**Shy Sarah**:
- Pre-selects "Conversation Starters" with encouraging explanation
- Emphasizes "baby steps" and "comfortable progression"
- Additional reassurance about practice environment safety

---


### Completion and Transition

#### Onboarding Complete Experience
**Success State:**
- **Celebration animation**: Positive messaging about readiness
- **Achievement unlock**: "Getting Started" badge
- **Confidence message**: "You're ready to start practicing!"
- **Clear next steps**: Direct path to Home Dashboard

**Data Capture:**
- User preferences and goals for personalization
- Initial comfort level for difficulty recommendations
- Selected skill goals for practice recommendations
- Complete user profile with registration data

**Seamless Transition:**
- **Account finalization**: Create Supabase Auth account and database record
- **Data migration**: Move all temporary data to permanent user profile
- **Email verification**: Send verification email for account security
- **Main app access**: 
  - **Development**: Navigate to placeholder 4-tab interface for testing
  - **Production**: Direct entry to Home Dashboard with "Start Your First Practice" CTA
- **Progress preservation**: All onboarding data carried forward to user account
- **First-time experience**: Prominent guidance for first practice session

### Development/Testing Transition
**After onboarding completion in development:**
- User lands on **placeholder main app** with 4 tabs
- **Home tab**: Welcome message and development notice
- **Chat tab**: "Feature in development" placeholder
- **Scenarios tab**: "Feature in development" placeholder
- **Profile tab**: Includes "Reset App & Clear Data" button for testing

**Testing workflow:**
1. Complete onboarding with registration
2. Land on placeholder interface
3. Navigate to Profile tab
4. Tap "Reset App & Clear Data"
5. Confirm reset in alert dialog
6. Return to onboarding start
7. Test registration flow again

**Important**: This placeholder interface is temporary and only appears in development builds for testing purposes

---

## Edge Cases and Error Handling

### Technical Error States
**Network Issues:**
- Onboarding preference collection works completely offline
- Clear messaging about connectivity requirements
- Graceful fallback to cached content where possible
- Resume capability when connection restored

**App Performance Issues:**
- Loading states for each screen transition
- Timeout handling with user-friendly error messages
- Alternative interaction methods if animations fail
- Progressive enhancement for slower devices

### User Experience Edge Cases
**Abandonment and Return:**
- Progress saved automatically at each screen
- Return users can resume where they left off
- Option to restart onboarding if desired
- Clear indication of completed vs remaining steps

**Accessibility Considerations:**
- Screen reader optimization for every screen
- Alternative input methods for date selection
- High contrast mode support throughout
- Voice control compatibility where available

**Privacy and Data Concerns:**
- Clear data usage explanations at each collection point
- Option to complete onboarding with minimal data collection
- Anonymous mode available for privacy-conscious users
- Transparent about what data is required vs optional

---

*This comprehensive user journey ensures every user type can successfully complete onboarding while building genuine confidence in FlirtCraft's value proposition through hands-on experience.*