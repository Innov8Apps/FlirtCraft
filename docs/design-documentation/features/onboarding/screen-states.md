# Onboarding Feature - Screen States

---
title: Onboarding Feature Screen States and Visual Specifications
description: Complete screen-by-screen visual design specifications for app onboarding flow
feature: onboarding
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - interactions.md
  - accessibility.md
  - implementation.md
  - ../../design-system/components/buttons.md
  - ../../design-system/components/forms.md
  - ../../design-system/components/navigation.md
  - ../../design-system/tokens/colors.md
  - ../../design-system/tokens/typography.md
  - ../../design-system/tokens/spacing.md
dependencies:
  - design-system/components
  - profile feature integration
status: approved
---

## Screen States Overview

The premium onboarding feature includes 5 primary screens designed to introduce users to FlirtCraft through confidence-building animations, build trust with celebration effects, secure account creation with enhanced micro-interactions, and seamlessly transition into the main app experience. Each screen prioritizes emotional engagement through React Native Reanimated 3, security with premium feedback, and clear value communication using NativeBase UI v2 with NativeWind 4.1 styling and pure orange design system.

## NativeBase UI v2 Component Mapping

### Core Components Used
- **Box**: Container component with NativeWind classes `className="flex-1 bg-white safe-area"`
- **VStack/HStack**: Layout components with spacing tokens `space="$4"` (16px)
- **Text**: Typography component with design system tokens `size="xl" weight="$bold" color="$primary900"`
- **Button/ButtonText**: Action components with variants `action="primary" size="lg"`
- **Input/InputField**: Form components with validation states `isInvalid={hasError}`
- **Card**: Content containers with elevation `variant="elevated" size="md"`
- **Modal**: Overlay components with backdrop and accessibility
- **Progress**: Visual progress indicators with color tokens
- **FormControl**: Comprehensive form handling with labels and errors
- **Toast**: Feedback notifications with semantic colors
- **Pressable**: Touch-optimized interaction areas with haptic feedback

### Design Token Integration
All components use systematic design tokens from the FlirtCraft design system:

**Color Tokens:**
- Primary: `$primary500` (#F97316), `$primary700` (#C2410C), `$primary300` (#FDBA74)
- Semantic: `$success500` (#10B981), `$error500` (#EF4444), `$warning500` (#F59E0B)
- Neutral: `$neutral50` to `$neutral900` for text and background hierarchy

**Spacing Tokens (4px base unit):**
- `$1`: 4px, `$2`: 8px, `$3`: 12px, `$4`: 16px, `$6`: 24px, `$8`: 32px, `$12`: 48px

**Typography Tokens:**
- `size="3xl"`: 28px H1 headings, `size="xl"`: 24px H2 headings
- `weight="$bold"`: 700 for headings, `weight="$semibold"`: 600 for emphasis
- Line heights automatically calculated (1.4x for headings, 1.5x for body)

**Component Styling Examples:**
```typescript
// Primary Button with design tokens
<Button action="primary" size="lg" className="w-full mt-6">
  <ButtonText>Get Started</ButtonText>
</Button>

// Form Input with validation
<FormControl isInvalid={!!errors.email}>
  <FormControlLabel>
    <FormControlLabelText>Email Address *</FormControlLabelText>
  </FormControlLabel>
  <Input variant="outline" size="lg">
    <InputField
      placeholder="Enter your email"
      keyboardType="email-address"
      autoCapitalize="none"
    />
  </Input>
  <FormControlError>
    <FormControlErrorText>{errors.email}</FormControlErrorText>
  </FormControlError>
</FormControl>

// Progress indicator with primary color
<Progress value={currentStep / totalSteps * 100} size="sm" colorScheme="primary" />

// Card with elevation and padding
<Card variant="elevated" size="md" className="p-4 mb-3">
  <Text size="md" weight="$semibold" color="$neutral800">
    Safe Practice Environment
  </Text>
  <Text size="sm" color="$neutral600" className="mt-1">
    Practice conversations without real-world pressure
  </Text>
</Card>
```

## Table of Contents

1. [Welcome Screens](#welcome-screens)
2. [Trust Building Screens](#trust-building-screens)
3. [Registration Screens](#registration-screens)
4. [Value Proposition Screens](#value-proposition-screens)
5. [Permission Request Screens](#permission-request-screens)
6. [Profile Integration Screens](#profile-integration-screens)

---

## Welcome Screens

### Purpose
Create positive first impressions and clearly communicate the app's purpose and benefits.

### Layout Structure
- **Container**: Full screen with centered content and safe area handling
- **Grid**: Vertical layout with hero content, supporting visuals, and action buttons
- **Spacing**: Generous whitespace (32px sections) for premium, uncluttered feel

---

### State: App Launch / Splash

#### Visual Design Specifications

**Brand Introduction**:
- **Logo**: FlirtCraft wordmark centered, 48px height on mobile, 64px on tablet+
- **Animation**: Gentle fade-in with slight scale animation (0.9x → 1.0x)
- **Background**: Subtle gradient from Primary-50 to Secondary-50
- **Loading Indicator**: Minimal progress indicator if needed

**Version and Legal**:
- **App Version**: Subtle text in bottom corner (Caption style)
- **Loading Text**: "Building confidence..." or similar encouraging message
- **Duration**: 2-3 seconds maximum, skippable after 1 second

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Logo Size**: 180px width maximum for readability
- **Safe Areas**: 16px minimum margins from screen edges
- **Status Bar**: Handle different status bar heights (notches, etc.)

**Tablet (768-1023px)**:
- **Logo Size**: 240px width for enhanced visibility
- **Centered Content**: Maximum 600px content width
- **Enhanced Animation**: More prominent scaling effects

**Desktop (1024px+)**:
- **Logo Size**: 320px width maximum
- **Layout**: Consider side-by-side hero layout
- **Background**: More sophisticated gradient or subtle pattern

---

### State: Welcome Introduction

#### Visual Design Specifications

**Hero Content**:
- **Headline**: "Welcome to FlirtCraft" in H1 style (Primary-900)
- **Subheadline**: "Practice conversations. Build confidence. Find connections." in H3 (Neutral-700)
- **Hero Image**: Friendly illustration showing diverse people having conversations
- **Style**: Warm, inclusive illustrations in app color scheme

**Value Preview**:
- **Benefit Cards**: 3 compact cards showing core benefits
  - "Safe Practice Environment"
  - "Personalized AI Partners" 
  - "Real Confidence Building"
- **Card Design**: Light background (Primary-50), subtle border, 16px padding
- **Icons**: Consistent iconography for each benefit

**Primary Action**:
- **Button Text**: "Get Started"
- **Button Style**: Primary button (Primary-500 background)
- **Button Size**: Large size (56px height minimum)
- **Secondary Action**: "Learn More" text link below

#### Content Strategy

**Headline Variations by Persona**:
- **Anxious Users**: "Your safe space to practice conversations"
- **Returning Daters**: "Get back in the dating game with confidence"
- **Advanced Users**: "Master the art of conversation"
- **Default**: "Practice makes perfect conversations"

**Subheadline Messaging**:
- **Focus**: Confidence building over dating success
- **Tone**: Encouraging and supportive, not pressuring
- **Length**: Maximum 2 lines on mobile for readability

---

### State: How It Works (Step 1)

#### Visual Design Specifications

**Step Indicator**:
- **Progress**: "1 of 3" or dot indicators showing current position
- **Style**: Primary-500 for active, Neutral-300 for inactive
- **Position**: Top center with 24px margin from content

**Content Layout**:
- **Main Illustration**: Large visual showing scenario selection
- **Headline**: "Choose Your Practice Scenario" (H2 style)
- **Description**: "Pick from real-world situations like coffee shops, bookstores, or social events" (Body style)
- **Supporting Details**: 2-3 bullet points with specific examples

**Visual Elements**:
- **Illustration Style**: Consistent with welcome screen, showing UI mockup
- **Color Scheme**: App colors with emphasis on Primary-500 for interactive elements
- **Animation**: Subtle parallax or breathing animation for engagement

#### Interaction Elements

**Navigation Controls**:
- **Next Button**: "Next" with forward arrow (Primary button)
- **Back Button**: "Back" text link (Neutral-600)
- **Skip Option**: "Skip Tour" text link in header (Neutral-500)

---

### State: How It Works (Step 2)

#### Visual Design Specifications

**Content Focus**:
- **Main Illustration**: AI conversation interface mockup
- **Headline**: "Chat with AI Practice Partners" (H2 style)
- **Description**: "Our AI creates realistic conversation partners based on your preferences" (Body style)
- **Key Features**: Highlight personalization and realistic responses

**Feature Highlights**:
- **AI Intelligence**: "Responds naturally to your conversation style"
- **Personalization**: "Adapts to your age, interests, and goals"
- **Variety**: "Different personalities and interaction styles"

**Visual Consistency**:
- **Same Layout**: Maintain consistent spacing and structure from Step 1
- **Progress Update**: Show "2 of 3" progress
- **Color Continuity**: Consistent use of Primary and Secondary colors

---

### State: How It Works (Step 3)

#### Visual Design Specifications

**Content Focus**:
- **Main Illustration**: Feedback screen mockup with progress visualization
- **Headline**: "Get Personalized Feedback" (H2 style)
- **Description**: "Learn what worked well and get specific tips for improvement" (Body style)
- **Outcome Focus**: Emphasize skill building and confidence growth

**Feedback Preview**:
- **Mock Feedback Card**: Example showing score and improvement tip
- **Progress Chart**: Simple visualization of improvement over time
- **Achievement Badge**: Example achievement to show gamification

**Call to Action**:
- **Primary Button**: "Go to Home" (Primary-500, emphasis on action)
- **Secondary Option**: "View My Preferences" (text link)

---

## Trust Building Screens

### Purpose
Address privacy concerns and build user confidence in the app's safety and effectiveness.

---

### State: Privacy & Safety

#### Visual Design Specifications

**Trust Indicators**:
- **Security Icon**: Shield or lock icon in Primary-500 (32px)
- **Headline**: "Your Privacy Matters" (H2 style, Primary-900)
- **Subheadline**: "Practice safely with complete privacy protection" (H3 style, Neutral-700)

**Privacy Assurances**:
- **Privacy Points**: 4 key privacy commitments in card format
  - "Conversations stay on your device"
  - "No real names or photos required"
  - "Data encrypted and secure"
  - "You control what's shared"

**Card Specifications**:
- **Background**: White with subtle border (Neutral-200)
- **Layout**: Icon + heading + description
- **Spacing**: 16px internal padding, 12px between cards
- **Icons**: Privacy-related icons in Success-500 (trust association)

**Compliance Badges**:
- **GDPR Compliant**: Subtle badge showing compliance
- **Data Protection**: Reference to privacy policy
- **Security Standards**: Mention of encryption standards

#### Trust-Building Elements

**Social Proof** (Optional):
- **User Count**: "Join 10,000+ people building confidence"
- **Success Stories**: Brief anonymous testimonials
- **Expert Endorsement**: If available, relationship coach endorsement

**Transparency**:
- **Privacy Policy Link**: Easily accessible, clear labeling
- **Data Usage**: Simple explanation of what data is collected and why
- **User Control**: Emphasis on user control over personal information

---

### State: Age Verification

#### Visual Design Specifications

**Legal Compliance**:
- **Headline**: "Verify Your Age" (H2 style)
- **Explanation**: "FlirtCraft is designed for adults 18+" (Body style)
- **Legal Note**: "Required for dating-focused content" (Caption style, Neutral-600)

**Age Input Interface**:
- **Input Type**: Date picker or age selection dropdown
- **Validation**: Real-time validation with helpful errors
- **Error States**: Clear, non-punitive error messaging
- **Privacy Note**: "Age used only for appropriate content matching"

**Alternative Pathways**:
- **Under 18 Route**: Redirect to general social skills resources
- **Verification Issues**: Contact support option
- **Privacy Concerns**: Additional privacy assurance

#### Error States

**Age Too Young**:
- **Message**: "FlirtCraft is designed for adults 18 and older"
- **Alternative**: "Check out these general conversation resources instead"
- **Support**: Link to appropriate alternative resources
- **Design**: Friendly, non-dismissive tone and visuals

**Verification Problems**:
- **Technical Issues**: "Having trouble? Try these steps..."
- **Support Contact**: Easy way to reach customer support
- **Manual Process**: Alternative verification if needed

---

## Registration Screens

### Purpose
Secure account creation with Supabase Auth while maintaining trust and onboarding momentum.

### Layout Structure
- **Container**: Full screen with form-focused layout and clear visual hierarchy
- **Grid**: Vertical form layout with proper spacing and input grouping
- **Spacing**: Consistent 16px internal spacing, 24px between sections

---

### State: Registration Form (Default)

#### Visual Design Specifications

**Form Header**:
- **Progress indicator**: 3 of 5 steps with NativeBase Progress component
  ```typescript
  <Progress value={60} size="sm" colorScheme="primary" className="mb-6" />
  ```
- **Headline**: "Create your FlirtCraft account" using design tokens
  ```typescript
  <Text size="3xl" weight="$bold" color="$primary900" className="text-center mb-2">
    Create your FlirtCraft account
  </Text>
  ```
- **Subheadline**: "Join thousands building conversation confidence"
  ```typescript
  <Text size="lg" color="$neutral700" className="text-center mb-4">
    Join thousands building conversation confidence
  </Text>
  ```
- **Toggle link**: "Already have an account? Sign In"
  ```typescript
  <Pressable onPress={toggleToSignIn} className="self-center mb-8">
    <Text size="md" color="$primary600" weight="$medium">
      Already have an account? Sign In
    </Text>
  </Pressable>
  ```

**Registration Form with React Hook Form Integration**:
```typescript
const registrationSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain an uppercase letter')
    .regex(/\d/, 'Password must contain a number')
    .regex(/[!@#$%^&*(),.?":{}|<>]/, 'Password must contain a special character'),
  confirmPassword: z.string(),
  agreedToTerms: z.boolean().refine(val => val === true, 'You must agree to the Terms of Service'),
  agreedToPrivacy: z.boolean().refine(val => val === true, 'You must agree to the Privacy Policy'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

const { control, handleSubmit, formState: { errors, isValid } } = useForm<RegistrationFormData>({
  resolver: zodResolver(registrationSchema),
  mode: 'onChange',
});
```

- **Email Input with Real-time Validation**: 
  ```typescript
  <FormControl isInvalid={!!errors.email} className="mb-4">
    <FormControlLabel>
      <FormControlLabelText size="md" color="$neutral800">
        Email address *
      </FormControlLabelText>
    </FormControlLabel>
    <Controller
      control={control}
      name="email"
      render={({ field: { onChange, onBlur, value } }) => (
        <Input variant="outline" size="lg" className="h-14">
          <InputField
            placeholder="Enter your email"
            value={value}
            onChangeText={onChange}
            onBlur={onBlur}
            keyboardType="email-address"
            autoCapitalize="none"
            autoComplete="email"
          />
        </Input>
      )}
    />
    {errors.email && (
      <FormControlError>
        <FormControlErrorText>{errors.email.message}</FormControlErrorText>
      </FormControlError>
    )}
    {/* Email availability indicator */}
    {isEmailValid && (
      <HStack className="items-center mt-2" space="$2">
        <Icon name="check-circle" size={16} color="$success500" />
        <Text size="sm" color="$success600">Email is available</Text>
      </HStack>
    )}
  </FormControl>
  ```

- **Password Input with Strength Indicator**:
  ```typescript
  <FormControl isInvalid={!!errors.password} className="mb-4">
    <FormControlLabel>
      <FormControlLabelText size="md" color="$neutral800">
        Create password *
      </FormControlLabelText>
    </FormControlLabel>
    <Input variant="outline" size="lg" className="h-14">
      <InputField
        placeholder="Minimum 8 characters"
        secureTextEntry={!showPassword}
        value={password}
        onChangeText={setPassword}
        autoComplete="new-password"
      />
      <Pressable
        onPress={() => setShowPassword(!showPassword)}
        className="absolute right-3 top-1/2 transform -translate-y-1/2"
      >
        <Icon name={showPassword ? "eye-off" : "eye"} size={20} color="$neutral500" />
      </Pressable>
    </Input>
    
    {/* Password Strength Indicator */}
    <Box className="mt-3">
      <Progress 
        value={passwordStrength} 
        size="xs" 
        colorScheme={getStrengthColor(passwordStrength)}
        className="mb-2"
      />
      <Text size="sm" color="$neutral600">{getStrengthMessage(passwordStrength)}</Text>
    </Box>
    
    {/* Password Requirements Checklist */}
    <VStack space="$1" className="mt-3">
      {passwordRequirements.map((req) => (
        <HStack key={req.id} space="$2" className="items-center">
          <Icon 
            name={req.met ? "check" : "x"} 
            size={14} 
            color={req.met ? "$success500" : "$neutral400"} 
          />
          <Text size="sm" color={req.met ? "$success600" : "$neutral500"}>
            {req.text}
          </Text>
        </HStack>
      ))}
    </VStack>
    
    {errors.password && (
      <FormControlError>
        <FormControlErrorText>{errors.password.message}</FormControlErrorText>
      </FormControlError>
    )}
  </FormControl>
  ```

- **Confirm Password with Match Validation**:
  ```typescript
  <FormControl isInvalid={!!errors.confirmPassword} className="mb-6">
    <FormControlLabel>
      <FormControlLabelText size="md" color="$neutral800">
        Confirm password *
      </FormControlLabelText>
    </FormControlLabel>
    <Controller
      control={control}
      name="confirmPassword"
      render={({ field: { onChange, onBlur, value } }) => (
        <Input variant="outline" size="lg" className="h-14">
          <InputField
            placeholder="Re-enter password"
            secureTextEntry={!showConfirmPassword}
            value={value}
            onChangeText={onChange}
            onBlur={onBlur}
            autoComplete="new-password"
          />
        </Input>
      )}
    />
    {errors.confirmPassword && (
      <FormControlError>
        <FormControlErrorText>{errors.confirmPassword.message}</FormControlErrorText>
      </FormControlError>
    )}
    {/* Password match indicator */}
    {password && confirmPassword && password === confirmPassword && (
      <HStack className="items-center mt-2" space="$2">
        <Icon name="check-circle" size={16} color="$success500" />
        <Text size="sm" color="$success600">Passwords match</Text>
      </HStack>
    )}
  </FormControl>
  ```

**Password Requirements Display**:
- **Minimum 8 characters**: Checkmark when met
- **At least 1 uppercase letter**: Checkmark when met  
- **At least 1 number**: Checkmark when met
- **At least 1 special character**: Checkmark when met
- **Visual indicators**: Green checkmarks and red X marks for instant feedback

**Terms Agreement**:
- **Terms of Service**: Required checkbox with link to full terms
- **Privacy Policy**: Required checkbox with link to policy
- **Marketing communications**: Optional checkbox for updates/tips
- **Layout**: Checkboxes with clear, readable text labels

**Primary Action**:
- **Button text**: "Create Account"
- **Button style**: Primary button (Primary-500 background)
- **Button size**: Large size (56px height)
- **Disabled state**: Grayed out until all requirements met
- **Loading state**: Spinner and "Creating account..." text

#### Interaction Design Specifications

**Form Validation**:
- **Real-time email validation**: Check format and availability on blur
- **Password strength calculation**: Update strength indicator as user types
- **Password matching**: Check confirmation field on every keystroke
- **Terms validation**: Enable submit button only when required terms agreed

**Email Availability Check**:
- **Debounced checking**: Wait 500ms after typing stops
- **Loading indicator**: Small spinner in email field during check
- **Already exists**: "This email is already registered. Sign in instead?"
- **Available**: Green checkmark in email field
- **Error handling**: Network error recovery with retry option

**Password Strength Indicator**:
- **Weak**: Red progress bar (0-25%), "Add more characters"
- **Fair**: Orange progress bar (26-50%), "Add numbers or symbols" 
- **Strong**: Yellow progress bar (51-75%), "Good password strength"
- **Excellent**: Green progress bar (76-100%), "Excellent password!"

**Auto-focus Progression**:
- **Email → Password**: Focus moves automatically after valid email
- **Password → Confirm**: Focus moves after password meets requirements
- **Smart error focus**: Focus moves to first field with error

#### Responsive Design Specifications

**Mobile (320-767px)**:
- **Form width**: Full width with 16px side margins
- **Input height**: 56px for easy touch interaction
- **Button height**: 56px minimum for accessibility
- **Spacing**: 16px between form elements

**Tablet (768-1023px)**:
- **Form width**: Maximum 480px, centered
- **Two-column layout**: Password requirements alongside password field
- **Enhanced visual hierarchy**: Larger headings and spacing

**Desktop (1024px+)**:
- **Form width**: Maximum 520px, centered
- **Side-by-side validation**: Real-time feedback next to form fields
- **Keyboard shortcuts**: Tab navigation and Enter to submit

---

### State: Sign In Form (Alternative)

#### Visual Design Specifications

**Form Header**:
- **Progress indicator**: Same 3 of 5 steps
- **Headline**: "Welcome back to FlirtCraft" (H2 style, Primary-900)
- **Subheadline**: "Continue building your conversation confidence" (H3 style, Neutral-700)
- **Toggle link**: "Don't have an account? Sign Up" (text link, Primary-600)

**Sign In Form**:
- **Email input**: 
  - Label: "Email address"
  - Placeholder: "Enter your email"
  - Auto-fill support: Compatible with password managers
- **Password input**:
  - Label: "Password"
  - Placeholder: "Enter your password"
  - Show/hide password toggle
- **Remember me**: Optional checkbox for session persistence
- **Forgot password**: Text link below password field

**Primary Action**:
- **Button text**: "Sign In"
- **Button style**: Primary button (Primary-500 background)
- **Button size**: Large size (56px height)
- **Loading state**: Spinner and "Signing in..." text

#### Error States

**Invalid Credentials**:
- **Message**: "Email or password incorrect. Please try again."
- **Suggestion**: "Forgot your password? Reset it here"
- **Visual treatment**: Error border on both email and password fields
- **Accessibility**: Error message announced to screen readers

**Account Locked**:
- **Message**: "Too many sign in attempts. Please try again in 15 minutes."
- **Alternative**: "Reset your password if you've forgotten it"
- **Support**: Link to contact customer support

**Network Issues**:
- **Message**: "Unable to sign in right now. Please check your connection."
- **Retry**: "Try Again" button with loading state
- **Offline**: "Continue without account" option if applicable

---

### State: Email Verification Sent

#### Visual Design Specifications

**Success Confirmation**:
- **Icon**: Large email/checkmark icon in Success-500 (64px)
- **Headline**: "Check your email" (H2 style, Success-600)
- **Message**: "We sent a verification link to [email address]" (Body style)
- **Instructions**: "Click the link to verify your account and continue setup"

**Action Options**:
- **Primary button**: "Continue Setup" (continues onboarding without waiting)
- **Secondary action**: "Resend email" (text link with cooldown timer)
- **Support**: "Having trouble? Contact support" (text link)

**Email Not Received**:
- **Expandable section**: "Didn't receive the email?"
- **Common solutions**: Check spam folder, verify email address
- **Alternative**: Change email address option

---

### State: Form Validation Errors

#### Error Display Specifications

**Email Validation Errors**:
- **Invalid format**: "Please enter a valid email address"
- **Already registered**: "This email is already registered. Sign in instead?"
- **Blocked domain**: "Please use a personal email address"
- **Network error**: "Unable to check email availability. Try again."

**Password Validation Errors**:
- **Too short**: "Password must be at least 8 characters"
- **Missing uppercase**: "Password must include at least 1 uppercase letter"
- **Missing number**: "Password must include at least 1 number"
- **Missing special char**: "Password must include at least 1 special character (@$!%*?&)"
- **Passwords don't match**: "Passwords do not match"

**Terms Agreement Errors**:
- **Terms required**: "Please agree to the Terms of Service to continue"
- **Privacy required**: "Please agree to the Privacy Policy to continue"

**Visual Treatment**:
- **Error borders**: Red border (Error-500) on invalid fields
- **Error messages**: Red text (Error-600) below affected fields
- **Success states**: Green border (Success-500) on valid fields
- **Accessibility**: Proper ARIA labels and error announcements

#### Error Recovery

**Helpful Error Handling**:
- **Specific guidance**: Tell users exactly what to fix
- **Positive framing**: "Almost there! Just fix these items"
- **Progressive disclosure**: Show only relevant errors for current field
- **Smart suggestions**: Offer common fixes for typical errors

---

### State: Registration Success

#### Visual Design Specifications

**Success Celebration**:
- **Animation**: Subtle success animation (checkmark or confetti)
- **Icon**: Large success checkmark in Success-500 (64px)
- **Headline**: "Account created successfully!" (H2 style, Success-600)
- **Message**: "Welcome to FlirtCraft! Let's finish setting up your profile."

**Next Steps**:
- **Primary button**: "Continue Setup" (transitions to preferences)
- **Progress indicator**: Updated to show registration complete
- **Motivational message**: "You're doing great! Just 2 more quick steps."

**Background Process**:
- **Temporary storage**: All registration data stored locally
- **Email verification**: Verification email sent in background
- **Security**: Password securely hashed and ready for account creation
- **Progress tracking**: Registration step marked as complete

---

## Value Proposition Screens

### Purpose
Clearly communicate unique value and differentiate from competitors.

---

### State: Why FlirtCraft Works

#### Visual Design Specifications

**Comparison Layout**:
- **Two Column**: "Other Apps" vs "FlirtCraft" comparison
- **Problem/Solution**: Address common dating app frustrations
- **Visual Contrast**: Use color coding to show improvements

**Key Differentiators**:
1. **Practice vs Performance Pressure**
   - Other: "Jump into real conversations unprepared"
   - FlirtCraft: "Practice in a safe environment first"

2. **Rejection Risk vs Safe Learning**
   - Other: "Risk embarrassment and rejection"
   - FlirtCraft: "Build confidence through practice"

3. **Generic Advice vs Personalized Coaching**
   - Other: "Generic dating tips"
   - FlirtCraft: "Personalized feedback on your conversations"

**Visual Treatment**:
- **Problem Side**: Muted colors (grays), frustrated expressions
- **Solution Side**: Vibrant colors (Primary scheme), confident expressions
- **Connecting Elements**: Arrows or bridges showing improvement

---

### State: Success Stories (Optional)

#### Visual Design Specifications

**Testimonial Cards**:
- **Layout**: Quote-style cards with user demographics (no photos)
- **Content**: Brief success stories focusing on confidence building
- **Attribution**: Age, location (general), timeframe
- **Privacy**: No real names, photos, or identifying details

**Story Examples**:
- "After 2 weeks of practice, I finally asked someone out at my local coffee shop"
- "The feedback helped me realize I was talking too fast - now conversations flow naturally"
- "I went from awkward to confident in group conversations"

**Visual Design**:
- **Card Style**: Clean, modern cards with subtle shadows
- **Typography**: Italic for quotes, regular for attribution
- **Color Scheme**: Neutral backgrounds with Primary accents
- **Spacing**: Generous whitespace between testimonials

---

## Permission Request Screens

### Purpose
Request necessary permissions with clear value explanations and easy alternatives.

---

### State: Notification Permissions

#### Visual Design Specifications

**Permission Request Layout**:
- **Icon**: Notification bell icon in Primary-500 (48px)
- **Headline**: "Stay Motivated with Gentle Reminders" (H2 style)
- **Description**: Clear explanation of notification value and frequency

**Notification Types**:
- **Practice Reminders**: "Gentle nudges to keep building confidence"
- **Progress Celebrations**: "Celebrate your conversation milestones"
- **Helpful Tips**: "Weekly conversation tips and insights"
- **Frequency**: "2-3 per week maximum, easily customizable"

**User Control**:
- **Primary Action**: "Enable Notifications" (Primary button)
- **Alternative**: "Maybe Later" (Secondary button)
- **Settings Preview**: "You can change these anytime in settings"

#### Privacy and Control

**Opt-out Clarity**:
- **Easy Disable**: Clear instructions for disabling later
- **Granular Control**: "Choose which types of notifications you want"
- **No Penalty**: "Full app functionality without notifications"

---

### State: Analytics Consent (Optional)

#### Visual Design Specifications

**Consent Request**:
- **Headline**: "Help Us Improve FlirtCraft" (H2 style)
- **Description**: Clear explanation of analytics data and benefits
- **Value Exchange**: How user data improves the experience

**Data Transparency**:
- **What's Collected**: "Anonymous usage patterns and feature preferences"
- **What's Not**: "Never personal conversations or identifying information"
- **Purpose**: "Helps us build better practice scenarios and features"
- **Control**: "Change your mind anytime in privacy settings"

**Consent Options**:
- **Accept**: "Yes, Help Improve the App" (Primary button)
- **Decline**: "No, Keep My Usage Private" (Secondary button)
- **Learn More**: Link to detailed privacy policy

---

## Profile Integration Screens

### Purpose
Seamlessly transition from onboarding to profile creation with maintained momentum.

---

### State: Ready to Personalize

#### Visual Design Specifications

**Transition Messaging**:
- **Headline**: "Let's Personalize Your Experience" (H1 style)
- **Description**: "A few quick questions help create realistic practice scenarios"
- **Benefit Focus**: "Better practice partners = faster confidence building"

**Preview of Profile Process**:
- **Steps Preview**: "Just 3 steps: basics, preferences, goals"
- **Time Estimate**: "Takes about 2 minutes"
- **Skip Option**: "You can always customize later" (but encourage completion)

**Visual Continuity**:
- **Design Language**: Consistent with onboarding screens
- **Color Scheme**: Maintain Primary/Secondary color usage
- **Spacing**: Same generous whitespace approach

**Action Buttons**:
- **Primary**: "Set Up My Profile" (Primary-500 button)
- **Secondary**: "Start Practicing Now" (less prominent, skips profile)

---

### State: Onboarding Complete

#### Visual Design Specifications

**Completion Celebration**:
- **Visual Element**: Success animation or congratulations graphic
- **Headline**: "You're All Set!" (H1 style, Success-600)
- **Achievement**: "Ready to start building conversation confidence"

**Next Steps Preview**:
- **Quick Guide**: Preview of first conversation experience
- **Recommendation**: Suggested first scenario based on profile
- **Confidence Message**: "Remember, this is practice - have fun with it!"

**Final Actions**:
- **Primary**: "Start My First Conversation" (Primary-500, large button)
- **Secondary**: "Explore Scenarios First" (Secondary button)
- **Settings Access**: "Adjust My Preferences" (text link)

#### Success Metrics Integration

**Progress Indication**:
- **Setup Complete**: Visual indicator that setup is 100% complete
- **Profile Completeness**: If applicable, show profile completion status
- **Achievement Unlock**: First achievement badge for completing onboarding

---

## Error States

### Purpose
Handle various error conditions gracefully while maintaining positive user experience.

---

### State: Network Connection Issues

#### Visual Design Specifications

**Offline Indicator**:
- **Icon**: Wifi-off icon in Warning-500
- **Headline**: "Connection Needed for Setup"
- **Description**: "Some onboarding features require internet connection"
- **Retry Option**: "Try Again" button when connection returns

**Offline Alternatives**:
- **Cached Content**: Show what can be viewed offline
- **Demo Mode**: Limited demo of features without network
- **Save Progress**: Assurance that progress will be saved when connected

---

### State: Age Verification Failure

#### Visual Design Specifications

**Alternative Pathways**:
- **Under 18**: Redirect to appropriate resources
- **Verification Issues**: Contact support with clear instructions
- **Technical Problems**: Alternative verification methods

**Design Treatment**:
- **Non-punitive Tone**: Helpful and understanding language
- **Clear Options**: Obvious next steps for each scenario
- **Support Access**: Easy way to get help if needed

---

## Post-Onboarding Placeholder Screens (Development/Testing)

### Overview
These placeholder screens appear after onboarding completion during development. They provide basic navigation structure for testing while features are being built.

### Home Tab Screen
**Purpose**: Landing screen after onboarding completion
**Layout**:
- **Header**: "Welcome to FlirtCraft! 🎉"
- **Subheading**: "Main features are in development"
- **Content Box**: Development build notice
- **Visual**: Centered layout with orange accent color (#F97316)

**State**: Static placeholder
**Interactions**: Tab switching only

### Chat Tab Screen
**Purpose**: Placeholder for custom conversation feature
**Layout**:
- **Icon**: Message circle icon (48px, orange)
- **Title**: "Chat Feature"
- **Description**: "Custom conversation practice will be available here"
- **Status Badge**: "Feature in development" (warning style)

**State**: Static placeholder
**Interactions**: Tab switching only

### Scenarios Tab Screen
**Purpose**: Placeholder for predefined scenarios feature
**Layout**:
- **Icon**: Grid icon (48px, orange)
- **Title**: "Scenarios Feature"
- **Description**: "Predefined practice scenarios will be available here"
- **Status Badge**: "Feature in development" (info style)

**State**: Static placeholder
**Interactions**: Tab switching only

### Profile Tab Screen (With Reset Function)
**Purpose**: Profile placeholder with development reset tool
**Layout**:
- **Header**: "Profile"
- **User Info Section**: 
  - Gray box with "Profile features coming soon..."
- **Development Tools Section** (Red accent):
  - Title: "Development Tools"
  - Description: "Use this to test the registration flow again"
  - **Reset Button**: "Reset App & Clear Data" (destructive action)
- **Note**: "This reset function is only available in development builds"

**States**:
- **Default**: Shows reset button
- **Confirming**: Alert dialog for reset confirmation
- **Resetting**: Loading state while clearing data

**Reset Flow**:
1. User taps "Reset App & Clear Data"
2. Confirmation alert appears
3. On confirm: Sign out → Clear storage → Reset state → Navigate to onboarding
4. On cancel: Return to profile

### Bottom Tab Bar
**Layout**:
- **4 Tabs**: Home | Chat | Scenarios | Profile
- **Active State**: Orange color (#F97316) for icon and label
- **Inactive State**: Gray color (#9CA3AF)
- **Touch Targets**: Full width divided by 4, 48px height minimum

**Visual Design**:
- White background
- Top border (1px, #E5E7EB)
- Icons: 24px size
- Labels: 12px font size
- Safe area padding at bottom

### Important Development Notes
- **Temporary Implementation**: These screens exist only for testing
- **No Real Features**: All tabs show placeholder content
- **Reset Capability**: Profile tab allows complete app reset for testing
- **Production Replacement**: Will be replaced with actual features

---

## Accessibility Specifications

### Screen Reader Experience

**Navigation Announcements**:
- **Screen Changes**: Clear announcements of new screen content
- **Progress Updates**: "Step 2 of 3" announcements
- **Completion Status**: "Onboarding complete" confirmation

**Content Structure**:
- **Heading Hierarchy**: Proper H1, H2, H3 structure for navigation
- **Landmark Roles**: Main, navigation, complementary roles
- **List Structure**: Benefit lists and step lists properly marked up

### Keyboard Navigation

**Tab Order**:
- **Logical Flow**: Tab order follows visual layout
- **Skip Links**: Quick navigation options for long screens
- **Focus Indicators**: Clear focus indication throughout

### Motor Accessibility

**Touch Targets**:
- **Minimum Size**: 44×44px for all interactive elements
- **Spacing**: Adequate space between touch targets
- **Large Buttons**: Primary actions use large button sizes

### Visual Accessibility

**Color Contrast**:
- **Text Contrast**: All text meets WCAG AA standards (4.5:1 ratio)
- **Interactive Elements**: Clear distinction between states
- **Error States**: Don't rely solely on color for error indication

**Typography**:
- **Scalable Text**: Support for dynamic type sizing
- **Clear Hierarchy**: Strong visual hierarchy without relying on color alone
- **Reading Comfort**: Appropriate line spacing and character width

## Performance Specifications

### Loading Performance
- **Screen Transitions**: <300ms between onboarding screens
- **Image Loading**: Progressive image loading with placeholders
- **Animation Performance**: 60fps maintained for all transitions

### Memory Management
- **Image Optimization**: Appropriate image sizes for different screen densities
- **Animation Cleanup**: Proper cleanup of animation resources
- **State Management**: Efficient state updates without memory leaks

## Implementation Notes

### Component Usage
- **Button Components**: Standard button variants from design system
- **Card Components**: Consistent card styling for benefit and feature displays
- **Typography**: Established type scale with appropriate weights and sizes
- **Spacing**: 4px base unit mathematical spacing throughout

### State Transitions
- **Smooth Animations**: Consistent transition timing and easing
- **Data Persistence**: Onboarding progress saved locally
- **Error Recovery**: Graceful handling of interruptions and errors

### Analytics Integration
- **Screen Tracking**: Track completion rates for each onboarding screen
- **Drop-off Analysis**: Identify where users exit onboarding flow
- **A/B Testing**: Support for testing different onboarding variations

## Related Documentation

- **[User Journey](./user-journey.md)** - Complete onboarding flow and decision points
- **[Interactions](./interactions.md)** - Animation and interaction specifications
- **[Accessibility](./accessibility.md)** - Complete accessibility implementation
- **[Implementation](./implementation.md)** - Technical specifications and handoff

## Last Updated
- **Version 1.0.0**: Complete screen state specifications with accessibility and responsive design
- **Focus**: Trust-building first impressions with seamless profile integration
- **Next**: Technical implementation and animation specifications