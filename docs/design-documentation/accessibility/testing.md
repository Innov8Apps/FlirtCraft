# Accessibility Testing

---
title: FlirtCraft Accessibility Testing Procedures and Tools
description: Comprehensive testing methodology for ensuring inclusive user experiences across all features and platforms
last-updated: 2025-08-23
version: 1.0.0
related-files:
  - ./README.md
  - ./guidelines.md
  - ./compliance.md
dependencies:
  - Screen readers (VoiceOver, TalkBack, NVDA, JAWS)
  - Accessibility testing tools
  - Real user testing program
  - Automated testing frameworks
status: implemented
---

## Overview

This document outlines comprehensive accessibility testing procedures for FlirtCraft, ensuring that all features work effectively for users with diverse abilities and assistive technology needs. Our testing approach combines automated tools, manual validation, and real user feedback to achieve and maintain WCAG AAA compliance while providing exceptional user experiences.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Automated Testing Tools](#automated-testing-tools)
3. [Manual Testing Procedures](#manual-testing-procedures)
4. [Screen Reader Testing](#screen-reader-testing)
5. [Keyboard Navigation Testing](#keyboard-navigation-testing)
6. [Visual Accessibility Testing](#visual-accessibility-testing)
7. [Motor Accessibility Testing](#motor-accessibility-testing)
8. [Real User Testing](#real-user-testing)
9. [Continuous Integration](#continuous-integration)

## Testing Philosophy

### Comprehensive Coverage Approach
FlirtCraft's accessibility testing follows a multi-layered approach that ensures no barriers exist between users and their goal of building romantic conversation confidence:

**Automated Foundation**: Catch common accessibility issues early in development
**Manual Validation**: Verify that automated tests translate to real-world usability
**Assistive Technology Testing**: Ensure compatibility with screen readers, switch controls, and voice recognition
**Real User Validation**: Test with actual users who rely on accessibility features
**Continuous Monitoring**: Ongoing testing throughout development and after releases

### Testing Priorities
1. **Critical User Journeys**: Core conversation practice flows work for all users
2. **Gamification Elements**: Progress tracking and achievements are universally accessible
3. **Navigation Systems**: All users can efficiently move through the app
4. **Content Consumption**: Information is perceivable and understandable by all users
5. **Input Methods**: All interaction methods are available to users with diverse abilities

## Automated Testing Tools

### Web-Based Testing Tools

#### axe-core Integration
```javascript
// Automated accessibility testing with axe-core
import { configureAxe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

// Configure axe for FlirtCraft-specific testing
const axeConfig = {
  rules: {
    // Enhanced color contrast requirements (AAA level)
    'color-contrast-enhanced': { enabled: true },
    
    // Strict focus management
    'focus-order-semantics': { enabled: true },
    
    // Form labeling requirements
    'label': { enabled: true },
    'label-title-only': { enabled: true },
    
    // ARIA usage validation
    'aria-valid-attr': { enabled: true },
    'aria-valid-attr-value': { enabled: true },
    'aria-required-parent': { enabled: true }
  },
  
  // Custom FlirtCraft accessibility checks
  checks: [
    {
      id: 'conversation-accessibility',
      evaluate: function(node, options) {
        // Custom check for conversation interface accessibility
        const chatMessages = node.querySelectorAll('[role="log"] .message');
        return chatMessages.length === 0 || 
               Array.from(chatMessages).every(msg => 
                 msg.hasAttribute('aria-label') || 
                 msg.textContent.trim().length > 0
               );
      },
      metadata: {
        impact: 'serious',
        messages: {
          pass: 'All conversation messages are accessible',
          fail: 'Some conversation messages lack proper accessibility labeling'
        }
      }
    }
  ]
};

// Test suite for conversation interface
describe('Conversation Interface Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<ConversationInterface />);
    const results = await axe(container, axeConfig);
    expect(results).toHaveNoViolations();
  });
  
  it('should maintain accessibility during conversation flow', async () => {
    const { container } = render(<ConversationInterface />);
    
    // Simulate conversation interaction
    fireEvent.click(screen.getByRole('button', { name: /start conversation/i }));
    
    // Wait for conversation to load
    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });
    
    const results = await axe(container, axeConfig);
    expect(results).toHaveNoViolations();
  });
});
```

#### Lighthouse Accessibility Audits
```javascript
// Automated Lighthouse accessibility testing
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runAccessibilityAudit(url) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
  
  const options = {
    logLevel: 'info',
    output: 'json',
    onlyCategories: ['accessibility'],
    port: chrome.port,
  };
  
  const runnerResult = await lighthouse(url, options);
  await chrome.kill();
  
  const { lhr } = runnerResult;
  const accessibilityScore = lhr.categories.accessibility.score * 100;
  
  // Ensure accessibility score meets FlirtCraft standards
  expect(accessibilityScore).toBeGreaterThanOrEqual(95);
  
  return {
    score: accessibilityScore,
    audits: lhr.audits,
    violations: Object.values(lhr.audits)
      .filter(audit => audit.score !== null && audit.score < 1)
  };
}

// Test key app screens
describe('Lighthouse Accessibility Audits', () => {
  test('Conversation practice screen meets accessibility standards', async () => {
    const results = await runAccessibilityAudit('http://localhost:3000/practice');
    expect(results.score).toBeGreaterThanOrEqual(95);
  });
  
  test('Progress dashboard meets accessibility standards', async () => {
    const results = await runAccessibilityAudit('http://localhost:3000/progress');
    expect(results.score).toBeGreaterThanOrEqual(95);
  });
});
```

### Mobile Testing Tools

#### iOS Accessibility Inspector Integration
```swift
// iOS accessibility testing integration
import XCTest
import AccessibilityAudit

class FlirtCraftAccessibilityTests: XCTestCase {
    var app: XCUIApplication!
    
    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
        
        // Enable accessibility testing
        app.accessibilityAudit.enabled = true
    }
    
    func testConversationInterfaceAccessibility() throws {
        // Navigate to conversation interface
        app.buttons["Start Practice"].tap()
        
        // Wait for conversation to load
        let conversationView = app.otherElements["conversation-interface"]
        XCTAssert(conversationView.waitForExistence(timeout: 5))
        
        // Run accessibility audit
        let auditResults = app.performAccessibilityAudit()
        XCTAssertTrue(auditResults.isEmpty, "Accessibility violations found: \(auditResults)")
        
        // Test VoiceOver navigation
        XCTAssert(conversationView.isAccessibilityElement || 
                 conversationView.accessibilityElements?.count ?? 0 > 0)
    }
    
    func testGameificationAccessibility() throws {
        // Navigate to progress section
        app.tabBars.buttons["Progress"].tap()
        
        // Test XP progress bar
        let xpProgressBar = app.progressIndicators["xp-progress"]
        XCTAssert(xpProgressBar.exists)
        XCTAssertNotNil(xpProgressBar.accessibilityLabel)
        XCTAssertNotNil(xpProgressBar.accessibilityValue)
        
        // Test achievement accessibility
        let achievementCard = app.buttons.matching(identifier: "achievement-card").firstMatch
        if achievementCard.exists {
            XCTAssertNotNil(achievementCard.accessibilityLabel)
            XCTAssertNotNil(achievementCard.accessibilityTraits)
        }
    }
}
```

#### Android Accessibility Scanner Integration
```kotlin
// Android accessibility testing with Espresso
@RunWith(AndroidJUnit4::class)
class FlirtCraftAccessibilityTest {
    
    @get:Rule
    val activityRule = ActivityTestRule(MainActivity::class.java)
    
    @Test
    fun testConversationInterfaceAccessibility() {
        // Navigate to conversation screen
        onView(withId(R.id.start_practice_button)).perform(click())
        
        // Wait for conversation to load
        onView(withId(R.id.conversation_recycler_view))
            .check(matches(isDisplayed()))
        
        // Check accessibility properties
        onView(withId(R.id.conversation_recycler_view))
            .check(matches(hasContentDescription()))
        
        // Test TalkBack navigation
        onView(withId(R.id.message_input))
            .check(matches(isFocusable()))
            .check(matches(hasContentDescription()))
        
        // Verify achievement accessibility
        onView(withId(R.id.xp_progress_bar))
            .check(matches(hasContentDescription()))
            .check(matches(isAccessibilityFocusable()))
    }
    
    @Test
    fun testKeyboardNavigation() {
        // Test tab navigation through interface
        onView(withId(R.id.conversation_input))
            .perform(requestFocus())
            .check(matches(isFocused()))
        
        // Test keyboard shortcuts
        onView(withId(R.id.conversation_input))
            .perform(pressKey(KeyEvent.KEYCODE_TAB))
        
        onView(withId(R.id.send_button))
            .check(matches(isFocused()))
    }
}
```

## Manual Testing Procedures

### Comprehensive Manual Testing Checklist

#### Pre-Testing Setup
**Environment Preparation**:
- [ ] Test devices configured with different accessibility settings
- [ ] Screen readers installed and configured (VoiceOver, TalkBack, NVDA, JAWS)
- [ ] Keyboard navigation testing setup complete
- [ ] Color blindness simulation tools available
- [ ] High contrast mode enabled for visual testing

**User Scenarios Prepared**:
- [ ] First-time user onboarding journey
- [ ] Daily conversation practice session
- [ ] Achievement unlock and celebration
- [ ] Progress review and analytics exploration
- [ ] Settings adjustment and customization

#### Core Feature Testing

**Conversation Interface Manual Testing**:
```
Test: Conversation Accessibility Flow
Prerequisites: Screen reader active, keyboard navigation enabled

Steps:
1. Navigate to conversation practice using only keyboard
   ✓ Tab order is logical and predictable
   ✓ All interactive elements receive focus
   ✓ Focus indicators are clearly visible

2. Start conversation using screen reader
   ✓ Conversation start button is properly labeled
   ✓ Loading states are announced to screen reader
   ✓ Conversation context is read aloud clearly

3. Engage in conversation practice
   ✓ Messages are announced as they appear
   ✓ Input field is properly labeled
   ✓ Send button is accessible via keyboard
   ✓ Typing indicators are announced appropriately

4. Complete conversation and review feedback
   ✓ Feedback is accessible to screen reader
   ✓ XP awards are announced clearly
   ✓ Achievement unlocks are communicated effectively

Expected Results:
- All conversation elements accessible via screen reader
- Keyboard navigation covers all functionality
- Clear audio feedback for all important state changes
- No confusion about current conversation state
```

**Gamification Elements Manual Testing**:
```
Test: Gamification Accessibility
Prerequisites: User has some existing progress data

Steps:
1. Navigate to progress section
   ✓ XP progress bar value is announced clearly
   ✓ Level information is understandable via screen reader
   ✓ Progress percentages are communicated accurately

2. Explore achievement gallery
   ✓ Achievement cards are properly labeled
   ✓ Locked vs unlocked status is clear
   ✓ Progress toward achievements is announced
   ✓ Achievement details are accessible

3. Review streak information
   ✓ Current streak count is announced
   ✓ Streak status (active/inactive) is clear
   ✓ Next milestone information is accessible

Expected Results:
- All progress information available to screen readers
- Achievement system is motivating, not overwhelming
- Progress visualization has text alternatives
- Numerical progress is communicated precisely
```

#### Cross-Platform Manual Testing

**iOS Manual Testing Protocol**:
```
VoiceOver Testing Checklist:
□ Navigate entire app using VoiceOver gestures
□ Test rotor navigation for different element types
□ Verify custom actions are available where appropriate
□ Check VoiceOver hints provide helpful guidance
□ Test with VoiceOver speech rate variations
□ Validate Dynamic Type support across all text sizes

Switch Control Testing:
□ Navigate using single switch setup
□ Test dual switch configuration
□ Verify switch timing settings are respected
□ Check that all functionality is available via switches
□ Test switch control with conversation interface

Voice Control Testing:
□ Test voice navigation commands
□ Verify voice control labels are appropriate
□ Check dictation functionality in text inputs
□ Test voice control for gaming elements
```

**Android Manual Testing Protocol**:
```
TalkBack Testing Checklist:
□ Navigate app using TalkBack gestures
□ Test explore by touch functionality
□ Verify reading controls work appropriately
□ Check TalkBack global gestures function correctly
□ Test with different TalkBack verbosity settings
□ Validate with system font scaling

Accessibility Services Testing:
□ Test with Select to Speak functionality
□ Verify Live Caption integration
□ Check Sound Amplifier compatibility
□ Test with accessibility shortcuts
□ Validate system accessibility gesture support
```

## Screen Reader Testing

### Comprehensive Screen Reader Validation

#### Screen Reader Testing Matrix
| Feature | VoiceOver (iOS) | TalkBack (Android) | NVDA (Windows) | JAWS (Windows) |
|---------|----------------|-------------------|----------------|----------------|
| Conversation Interface | ✓ Tested | ✓ Tested | ✓ Tested | ✓ Tested |
| XP Progress | ✓ Tested | ✓ Tested | ✓ Tested | ✓ Tested |
| Achievement Gallery | ✓ Tested | ✓ Tested | ✓ Tested | ✓ Tested |
| Navigation | ✓ Tested | ✓ Tested | ✓ Tested | ✓ Tested |
| Settings | ✓ Tested | ✓ Tested | ✓ Tested | ✓ Tested |

#### VoiceOver Testing Procedures
```
VoiceOver Conversation Testing Script:

1. Conversation Start:
   - Activate VoiceOver
   - Navigate to "Start Practice" button
   - Verify button label: "Start Practice, button"
   - Double-tap to activate
   - Listen for loading announcement: "Loading conversation practice"

2. Conversation Flow:
   - Verify chat log announcement: "Conversation history, list"
   - Check message format: "[Character name] says: [message content]"
   - Navigate to input field
   - Verify input label: "Type your response, text field"
   - Enter text and verify echo
   - Navigate to send button: "Send, button"

3. XP Award:
   - Listen for XP announcement: "Earned 100 experience points"
   - Verify progress update: "Level 2, 45% complete, progress bar"
   - Check detailed announcement: "450 of 1000 points toward Level 3"

4. Achievement Unlock:
   - Listen for achievement announcement: "Achievement unlocked: First Steps"
   - Navigate to achievement details
   - Verify full description is readable
   - Check XP reward announcement: "Earned 5 bonus experience points"

Expected VoiceOver Behavior:
- Clear, descriptive labels for all elements
- Logical reading order through content
- Appropriate use of VoiceOver hints
- Custom actions available for complex controls
- Progress updates announced without overwhelming user
```

#### TalkBack Testing Procedures
```
TalkBack Achievement Gallery Testing Script:

1. Gallery Navigation:
   - Enable TalkBack
   - Navigate to achievement gallery
   - Verify section heading: "Achievement Gallery, heading level 1"
   - Use explore by touch to overview layout
   - Navigate using swipe gestures

2. Achievement Card Testing:
   - Focus on achievement card
   - Verify complete announcement: "[Achievement name], [status], [progress]"
   - Example: "Weekly Warrior, unlocked March 15th, button"
   - Test double-tap to open details
   - Verify modal focus management

3. Progress Information:
   - Focus on progress indicators
   - Verify percentage announcements: "75 percent complete"
   - Check detailed progress: "7 of 10 conversations completed"
   - Test navigation between progress elements

4. Filter Testing:
   - Navigate to category filters
   - Verify filter state: "All achievements, selected, tab 1 of 5"
   - Test filter activation and announcement
   - Verify content updates are announced

Expected TalkBack Behavior:
- Comprehensive element descriptions
- Clear state information (selected, unlocked, etc.)
- Appropriate content grouping
- Consistent navigation patterns
- Helpful context for interactive elements
```

### Screen Reader Content Guidelines

#### Effective Labeling Patterns
```javascript
// Screen reader optimized content patterns
const screenReaderLabels = {
  // XP Progress Bar
  xpProgress: {
    label: "Experience Points Progress",
    value: `${currentXP} of ${nextLevelXP} points`,
    description: `Level ${currentLevel}, ${progressPercent}% complete. ${xpRemaining} points needed for next level.`
  },
  
  // Achievement Card
  achievementCard: {
    unlocked: `${achievementName}, unlocked ${unlockDate}. ${achievementDescription}`,
    locked: `${achievementName}, ${progress} of ${target} completed. ${achievementDescription}`,
    secret: `Secret achievement. Complete more conversations to discover.`
  },
  
  // Conversation Message
  conversationMessage: {
    userMessage: `You said: ${messageText}`,
    characterMessage: `${characterName} says: ${messageText}`,
    contextualInfo: `${messageText}. This message demonstrates ${skillType}.`
  },
  
  // Streak Counter
  streakCounter: {
    active: `${streakDays} day practice streak. ${encouragementMessage}`,
    broken: `Ready to start a new practice streak. Your longest streak was ${longestStreak} days.`,
    milestone: `${streakDays} day streak achieved! You've unlocked ${multiplier}x experience point multiplier.`
  }
};
```

## Keyboard Navigation Testing

### Comprehensive Keyboard Testing

#### Keyboard Navigation Test Scenarios
```
Keyboard Navigation Master Test:

Prerequisites: 
- Physical keyboard connected (mobile) or desktop setup
- All mouse/touch input disabled for testing
- Tab order documentation available

Test Scenario 1: App Navigation
□ Tab through main navigation elements
□ Verify logical tab order (left to right, top to bottom)
□ Test Skip Links functionality
□ Verify focus indicators are visible and distinct
□ Test navigation between major app sections

Test Scenario 2: Conversation Interface
□ Tab to conversation practice button and activate with Enter
□ Navigate through conversation history using arrow keys
□ Tab to message input field and verify typing functionality
□ Use Tab to reach Send button and activate with Enter/Space
□ Test Escape key to exit conversation

Test Scenario 3: Gamification Elements
□ Tab through XP progress information
□ Navigate achievement gallery using arrow keys
□ Test Enter/Space to open achievement details
□ Navigate through achievement detail modal
□ Test Escape to close modal and return focus

Test Scenario 4: Settings and Preferences
□ Tab through all settings options
□ Test keyboard activation of toggle switches
□ Navigate dropdown menus using arrow keys
□ Test form submission using Enter key
□ Verify focus returns appropriately after actions

Expected Results:
- All functionality available via keyboard
- Focus never gets trapped unintentionally
- Focus indicators are clearly visible
- Keyboard shortcuts work consistently
- Tab order is logical and predictable
```

#### Advanced Keyboard Testing
```javascript
// Advanced keyboard navigation testing
class KeyboardNavigationTester {
  constructor() {
    this.focusHistory = [];
    this.trapDetected = false;
  }
  
  testTabOrder(startElement, expectedOrder) {
    let currentElement = startElement;
    const actualOrder = [currentElement];
    
    // Simulate tab navigation through expected elements
    for (let i = 1; i < expectedOrder.length; i++) {
      currentElement = this.simulateTab(currentElement);
      actualOrder.push(currentElement);
      
      // Check for focus traps
      if (this.focusHistory.includes(currentElement) && 
          !this.isExpectedLoop(currentElement)) {
        this.trapDetected = true;
        throw new Error(`Focus trap detected at ${currentElement.id}`);
      }
      
      this.focusHistory.push(currentElement);
    }
    
    // Verify tab order matches expected sequence
    const orderMatches = actualOrder.every((element, index) => 
      element === expectedOrder[index]
    );
    
    return {
      success: orderMatches,
      expectedOrder,
      actualOrder,
      focusTrapDetected: this.trapDetected
    };
  }
  
  testModalFocusTrap(modalElement) {
    const focusableElements = modalElement.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    // Test forward navigation trap
    lastElement.focus();
    this.simulateTab(lastElement);
    const focusTrappedForward = document.activeElement === firstElement;
    
    // Test backward navigation trap
    firstElement.focus();
    this.simulateShiftTab(firstElement);
    const focusTrappedBackward = document.activeElement === lastElement;
    
    return {
      forwardTrapWorks: focusTrappedForward,
      backwardTrapWorks: focusTrappedBackward,
      firstElement,
      lastElement,
      totalFocusableElements: focusableElements.length
    };
  }
  
  testKeyboardShortcuts(shortcuts) {
    const results = {};
    
    for (const [shortcut, expectedAction] of Object.entries(shortcuts)) {
      const initialState = this.captureAppState();
      this.simulateKeyboardShortcut(shortcut);
      const finalState = this.captureAppState();
      
      results[shortcut] = {
        executed: this.verifyStateChange(initialState, finalState, expectedAction),
        initialState,
        finalState
      };
    }
    
    return results;
  }
}

// Usage in test suite
describe('Keyboard Navigation Testing', () => {
  let tester;
  
  beforeEach(() => {
    tester = new KeyboardNavigationTester();
  });
  
  it('should follow logical tab order in conversation interface', () => {
    const expectedOrder = [
      document.getElementById('start-conversation'),
      document.getElementById('conversation-input'),
      document.getElementById('send-button'),
      document.getElementById('exit-button')
    ];
    
    const result = tester.testTabOrder(expectedOrder[0], expectedOrder);
    expect(result.success).toBe(true);
    expect(result.focusTrapDetected).toBe(false);
  });
  
  it('should properly trap focus in achievement detail modal', () => {
    const modal = document.getElementById('achievement-detail-modal');
    const result = tester.testModalFocusTrap(modal);
    
    expect(result.forwardTrapWorks).toBe(true);
    expect(result.backwardTrapWorks).toBe(true);
    expect(result.totalFocusableElements).toBeGreaterThan(0);
  });
});
```

## Visual Accessibility Testing

### Color Contrast and Visual Testing

#### Automated Color Contrast Testing
```javascript
// Automated color contrast validation
const colorContrastChecker = require('color-contrast-checker');
const ccc = new colorContrastChecker();

// FlirtCraft color combinations testing
const colorCombinations = [
  // Primary text combinations
  { foreground: '#111827', background: '#FFFFFF', context: 'Primary text on white' },
  { foreground: '#374151', background: '#F9FAFB', context: 'Secondary text on light background' },
  { foreground: '#FFFFFF', background: '#F97316', context: 'White text on primary orange' },
  
  // Interactive element combinations
  { foreground: '#FFFFFF', background: '#EA580C', context: 'Button text on primary dark' },
  { foreground: '#F97316', background: '#FEF3C7', context: 'Primary text on light yellow background' },
  
  // Status and feedback combinations
  { foreground: '#FFFFFF', background: '#10B981', context: 'Success message text' },
  { foreground: '#FFFFFF', background: '#EF4444', context: 'Error message text' },
  { foreground: '#92400E', background: '#FEF3C7', context: 'Warning text on warning background' }
];

describe('Color Contrast Compliance', () => {
  colorCombinations.forEach(({ foreground, background, context }) => {
    it(`should meet AAA contrast standards for ${context}`, () => {
      const contrastRatio = ccc.getContrast(foreground, background);
      const aaaCompliant = ccc.isLevelAAA(foreground, background);
      const aaCompliant = ccc.isLevelAA(foreground, background);
      
      expect(aaaCompliant).toBe(true);
      expect(contrastRatio).toBeGreaterThanOrEqual(7);
      
      console.log(`${context}: ${contrastRatio.toFixed(2)}:1 ratio`);
    });
  });
});
```

#### Color Blindness Simulation Testing
```javascript
// Color blindness simulation testing
class ColorBlindnessSimulator {
  constructor() {
    this.simulations = [
      'protanopia',    // Red-blind
      'deuteranopia',  // Green-blind  
      'tritanopia',    // Blue-blind
      'protanomaly',   // Red-weak
      'deuteranomaly', // Green-weak
      'tritanomaly',   // Blue-weak
      'monochromacy'   // Complete color blindness
    ];
  }
  
  testInterfaceWithColorBlindness(interfaceElement) {
    const results = {};
    
    this.simulations.forEach(condition => {
      results[condition] = this.testCondition(interfaceElement, condition);
    });
    
    return results;
  }
  
  testCondition(element, condition) {
    // Apply color blindness filter
    element.style.filter = this.getFilterForCondition(condition);
    
    // Test critical information visibility
    const tests = {
      xpProgressVisible: this.testXPProgressVisibility(element),
      achievementStatusClear: this.testAchievementStatusClarity(element),
      conversationFlowClear: this.testConversationFlowClarity(element),
      navigationDistinguishable: this.testNavigationDistinguishability(element),
      errorStatesClear: this.testErrorStateClarity(element)
    };
    
    // Remove filter
    element.style.filter = 'none';
    
    return {
      condition,
      passedTests: Object.values(tests).filter(result => result.passed).length,
      totalTests: Object.keys(tests).length,
      details: tests
    };
  }
  
  testXPProgressVisibility(element) {
    const progressBar = element.querySelector('.xp-progress-bar');
    const progressText = element.querySelector('.xp-progress-text');
    
    return {
      passed: progressBar && progressText && 
              this.hasAlternativeToColor(progressBar) &&
              this.textIsReadable(progressText),
      details: 'XP progress must be understandable without color information'
    };
  }
  
  testAchievementStatusClarity(element) {
    const achievements = element.querySelectorAll('.achievement-card');
    
    const allClear = Array.from(achievements).every(achievement => {
      return this.hasNonColorStatusIndicator(achievement) &&
             this.hasAccessibleText(achievement);
    });
    
    return {
      passed: allClear,
      details: 'Achievement locked/unlocked status must be clear without color'
    };
  }
  
  hasAlternativeToColor(element) {
    // Check for text labels, icons, patterns, or other non-color indicators
    return element.querySelector('.progress-text') ||
           element.querySelector('.icon') ||
           element.hasAttribute('aria-label') ||
           element.hasAttribute('aria-describedby');
  }
  
  hasNonColorStatusIndicator(element) {
    // Check for icons, text labels, or other status indicators
    return element.querySelector('.status-icon') ||
           element.querySelector('.status-text') ||
           element.classList.contains('achievement-unlocked') ||
           element.hasAttribute('aria-label');
  }
}
```

#### High Contrast Mode Testing
```css
/* High contrast mode testing styles */
@media (prefers-contrast: high) {
  /* Test all interface elements in high contrast */
  .conversation-bubble {
    border: 2px solid;
    background: ButtonFace;
    color: ButtonText;
  }
  
  .xp-progress-bar {
    border: 1px solid ButtonText;
    background: ButtonFace;
  }
  
  .xp-progress-fill {
    background: Highlight;
  }
  
  .achievement-card {
    border: 2px solid ButtonText;
    background: ButtonFace;
    color: ButtonText;
  }
  
  .achievement-card.unlocked {
    background: Highlight;
    color: HighlightText;
  }
  
  .primary-button {
    background: Highlight;
    color: HighlightText;
    border: 2px solid ButtonText;
  }
  
  .secondary-button {
    background: ButtonFace;
    color: ButtonText;
    border: 2px solid ButtonText;
  }
}

/* Test high contrast mode programmatically */
function testHighContrastMode() {
  const highContrastModeActive = window.matchMedia('(prefers-contrast: high)').matches;
  
  if (highContrastModeActive) {
    // Test all critical interface elements
    const tests = [
      testButtonVisibility(),
      testProgressBarVisibility(),
      testAchievementCardVisibility(),
      testConversationBubbleVisibility(),
      testNavigationVisibility()
    ];
    
    const passedTests = tests.filter(test => test.passed).length;
    
    return {
      highContrastSupported: passedTests === tests.length,
      passedTests,
      totalTests: tests.length,
      details: tests
    };
  }
  
  return { highContrastSupported: true, message: 'High contrast mode not active' };
}
```

## Motor Accessibility Testing

### Touch Target and Interaction Testing

#### Touch Target Size Validation
```javascript
// Automated touch target testing
class TouchTargetTester {
  constructor() {
    this.minimumSize = 44; // 44px minimum per WCAG AAA
    this.recommendedSpacing = 8; // 8px spacing between targets
  }
  
  validateTouchTargets(container) {
    const interactiveElements = container.querySelectorAll(
      'button, a, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const results = Array.from(interactiveElements).map(element => {
      const rect = element.getBoundingClientRect();
      const computedStyle = window.getComputedStyle(element);
      
      // Include padding in touch target calculation
      const paddingTop = parseFloat(computedStyle.paddingTop);
      const paddingBottom = parseFloat(computedStyle.paddingBottom);
      const paddingLeft = parseFloat(computedStyle.paddingLeft);
      const paddingRight = parseFloat(computedStyle.paddingRight);
      
      const effectiveWidth = rect.width + paddingLeft + paddingRight;
      const effectiveHeight = rect.height + paddingTop + paddingBottom;
      
      const widthCompliant = effectiveWidth >= this.minimumSize;
      const heightCompliant = effectiveHeight >= this.minimumSize;
      
      // Check spacing from adjacent interactive elements
      const spacing = this.calculateMinimumSpacing(element, interactiveElements);
      const spacingCompliant = spacing >= this.recommendedSpacing;
      
      return {
        element: element.tagName + (element.id ? `#${element.id}` : ''),
        width: effectiveWidth,
        height: effectiveHeight,
        spacing: spacing,
        widthCompliant,
        heightCompliant,
        spacingCompliant,
        overallCompliant: widthCompliant && heightCompliant && spacingCompliant
      };
    });
    
    return {
      totalElements: results.length,
      compliantElements: results.filter(r => r.overallCompliant).length,
      violations: results.filter(r => !r.overallCompliant),
      passRate: (results.filter(r => r.overallCompliant).length / results.length) * 100
    };
  }
  
  calculateMinimumSpacing(element, allElements) {
    const elementRect = element.getBoundingClientRect();
    let minimumSpacing = Infinity;
    
    allElements.forEach(otherElement => {
      if (element === otherElement) return;
      
      const otherRect = otherElement.getBoundingClientRect();
      
      // Calculate distance between elements
      const horizontalDistance = Math.max(0, 
        Math.max(elementRect.left - otherRect.right, otherRect.left - elementRect.right)
      );
      
      const verticalDistance = Math.max(0,
        Math.max(elementRect.top - otherRect.bottom, otherRect.top - elementRect.bottom)
      );
      
      // Use minimum distance (elements could be adjacent horizontally or vertically)
      const distance = Math.min(horizontalDistance, verticalDistance);
      
      if (distance < minimumSpacing) {
        minimumSpacing = distance;
      }
    });
    
    return minimumSpacing === Infinity ? this.recommendedSpacing : minimumSpacing;
  }
}

// Touch target testing in conversation interface
describe('Touch Target Accessibility', () => {
  it('should have adequate touch targets in conversation interface', () => {
    const conversationInterface = document.getElementById('conversation-interface');
    const tester = new TouchTargetTester();
    const results = tester.validateTouchTargets(conversationInterface);
    
    expect(results.passRate).toBeGreaterThanOrEqual(95);
    expect(results.violations).toHaveLength(0);
  });
  
  it('should maintain touch target sizes across different screen sizes', () => {
    const screenSizes = [
      { width: 320, height: 568 }, // iPhone SE
      { width: 375, height: 812 }, // iPhone X
      { width: 768, height: 1024 }, // iPad
      { width: 1024, height: 1366 }  // iPad Pro
    ];
    
    screenSizes.forEach(size => {
      // Simulate screen size
      Object.defineProperty(window, 'innerWidth', { value: size.width });
      Object.defineProperty(window, 'innerHeight', { value: size.height });
      
      const tester = new TouchTargetTester();
      const results = tester.validateTouchTargets(document.body);
      
      expect(results.passRate).toBeGreaterThanOrEqual(95);
    });
  });
});
```

#### Alternative Input Method Testing
```javascript
// Switch control and alternative input testing
class AlternativeInputTester {
  constructor() {
    this.switchActions = ['select', 'next', 'previous'];
    this.voiceCommands = ['click', 'press', 'tap', 'select'];
  }
  
  testSwitchControlCompatibility(interface) {
    const results = {
      singleSwitchNavigation: this.testSingleSwitchNavigation(interface),
      dualSwitchNavigation: this.testDualSwitchNavigation(interface),
      timingFlexibility: this.testTimingFlexibility(interface),
      feedbackClarity: this.testFeedbackClarity(interface)
    };
    
    return {
      overallCompatibility: Object.values(results).every(test => test.passed),
      results
    };
  }
  
  testSingleSwitchNavigation(interface) {
    // Test that all functionality can be reached with single switch
    const focusableElements = interface.querySelectorAll(
      '[tabindex]:not([tabindex="-1"]), button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href]'
    );
    
    // Simulate single switch scanning
    let currentIndex = 0;
    const navigationPath = [];
    
    while (currentIndex < focusableElements.length) {
      const element = focusableElements[currentIndex];
      navigationPath.push({
        element: element.tagName + (element.id ? `#${element.id}` : ''),
        accessible: this.isAccessibleViaSingleSwitch(element),
        position: currentIndex
      });
      currentIndex++;
    }
    
    const accessibleElements = navigationPath.filter(item => item.accessible).length;
    
    return {
      passed: accessibleElements === focusableElements.length,
      totalElements: focusableElements.length,
      accessibleElements,
      navigationPath
    };
  }
  
  testVoiceControlCompatibility(interface) {
    const interactiveElements = interface.querySelectorAll(
      'button, a, input, select, textarea, [role="button"], [role="link"]'
    );
    
    const results = Array.from(interactiveElements).map(element => {
      const hasVoiceLabel = this.hasAppropriateVoiceLabel(element);
      const isClickable = this.isVoiceClickable(element);
      const hasNumberLabel = this.hasNumberLabel(element);
      
      return {
        element: element.tagName + (element.id ? `#${element.id}` : ''),
        hasVoiceLabel,
        isClickable,
        hasNumberLabel,
        voiceCompatible: hasVoiceLabel && isClickable
      };
    });
    
    const compatibleElements = results.filter(r => r.voiceCompatible).length;
    
    return {
      passed: compatibleElements === results.length,
      totalElements: results.length,
      compatibleElements,
      compatibility: (compatibleElements / results.length) * 100,
      details: results
    };
  }
  
  hasAppropriateVoiceLabel(element) {
    // Check for accessible name that works well with voice control
    const accessibleName = element.getAttribute('aria-label') ||
                          element.textContent.trim() ||
                          element.getAttribute('alt') ||
                          element.getAttribute('title');
    
    return accessibleName && 
           accessibleName.length > 0 && 
           accessibleName.length < 50 && // Not too verbose for voice control
           !/^[0-9]+$/.test(accessibleName); // Not just numbers
  }
  
  isVoiceClickable(element) {
    // Check that element can be activated by voice commands
    return element.onclick !== null ||
           element.getAttribute('role') === 'button' ||
           element.tagName === 'BUTTON' ||
           element.tagName === 'A' ||
           element.tabIndex >= 0;
  }
}
```

## Real User Testing

### User Testing Program Structure

#### Participant Recruitment
```javascript
// Real user testing coordination system
class AccessibilityUserTestingProgram {
  constructor() {
    this.participantProfiles = [
      {
        disability: 'blindness',
        assistiveTech: ['screen-reader', 'braille-display'],
        experience: 'expert',
        platforms: ['ios', 'android']
      },
      {
        disability: 'low-vision',
        assistiveTech: ['screen-magnifier', 'high-contrast'],
        experience: 'intermediate',
        platforms: ['ios', 'android', 'web']
      },
      {
        disability: 'motor-impairment',
        assistiveTech: ['switch-control', 'voice-control'],
        experience: 'intermediate',
        platforms: ['ios', 'android']
      },
      {
        disability: 'cognitive-differences',
        assistiveTech: ['simplified-interface', 'reading-assistance'],
        experience: 'beginner',
        platforms: ['ios', 'android']
      },
      {
        disability: 'hearing-impairment',
        assistiveTech: ['visual-alerts', 'captions'],
        experience: 'intermediate',
        platforms: ['ios', 'android', 'web']
      }
    ];
    
    this.testingScenarios = [
      'first-time-user-onboarding',
      'daily-conversation-practice',
      'achievement-exploration',
      'progress-review',
      'settings-customization',
      'error-recovery'
    ];
  }
  
  scheduleTestingSession(participantProfile, scenario) {
    return {
      participant: participantProfile,
      scenario: scenario,
      duration: 60, // minutes
      preTestSetup: this.generatePreTestSetup(participantProfile),
      testingTasks: this.generateTestingTasks(scenario),
      successCriteria: this.generateSuccessCriteria(scenario),
      postTestQuestions: this.generatePostTestQuestions()
    };
  }
  
  generateTestingTasks(scenario) {
    const taskSets = {
      'first-time-user-onboarding': [
        'Download and open FlirtCraft for the first time',
        'Navigate through onboarding screens',
        'Set up your profile preferences',
        'Understand the gamification system explanation',
        'Start your first conversation practice'
      ],
      
      'daily-conversation-practice': [
        'Open FlirtCraft and check your current progress',
        'Start a conversation practice session',
        'Navigate through the conversation interface',
        'Complete a conversation and review feedback',
        'Check XP gained and achievement progress'
      ],
      
      'achievement-exploration': [
        'Navigate to the achievement gallery',
        'Browse different achievement categories',
        'Open details for a locked achievement',
        'Understand progress toward achievements',
        'Find and explore recently unlocked achievements'
      ]
    };
    
    return taskSets[scenario] || [];
  }
  
  generateSuccessCriteria(scenario) {
    const criteriaMap = {
      'first-time-user-onboarding': [
        'User completes onboarding without assistance',
        'User understands the app\'s core purpose',
        'User successfully starts first conversation',
        'No accessibility barriers encountered',
        'User reports confidence in using the app'
      ],
      
      'daily-conversation-practice': [
        'User navigates to conversation practice efficiently',
        'User completes conversation without accessibility issues',
        'User understands feedback and progress updates',
        'User can access all conversation features',
        'User reports satisfying practice experience'
      ],
      
      'achievement-exploration': [
        'User navigates achievement gallery effectively',
        'User understands locked vs unlocked achievements',
        'User can access achievement details',
        'User understands progress toward goals',
        'User finds achievement system motivating, not overwhelming'
      ]
    };
    
    return criteriaMap[scenario] || [];
  }
}
```

#### Testing Session Protocol
```
Real User Testing Session Protocol:

Pre-Session (15 minutes):
1. Environment Setup
   - Participant's usual assistive technology configured
   - FlirtCraft app installed and ready
   - Recording equipment set up (with consent)
   - Moderator and note-taker prepared

2. Introduction and Consent
   - Explain testing purpose and process
   - Confirm consent for recording
   - Review participant rights and withdrawal options
   - Answer any questions about the session

Testing Session (45 minutes):
3. Baseline Assessment (5 minutes)
   - Confirm assistive technology is working properly
   - Brief demonstration of participant's usual app usage
   - Establish communication preferences for the session

4. Task-Based Testing (30 minutes)
   - Present scenario and tasks one at a time
   - Encourage think-aloud protocol
   - Observe without intervening unless participant is stuck
   - Note both successful interactions and friction points
   - Document exact quotes about user experience

5. Guided Exploration (10 minutes)
   - Ask participant to explore areas they found interesting
   - Test edge cases and error scenarios
   - Explore any features they found confusing
   - Get feedback on overall app navigation

Post-Session (15 minutes):
6. Structured Interview
   - Overall impression of app accessibility
   - Most challenging aspects encountered
   - Features that worked particularly well
   - Comparison to other apps they use regularly
   - Suggestions for improvement

7. Follow-up Planning
   - Schedule follow-up session if needed
   - Provide contact information for ongoing feedback
   - Explain how feedback will be used to improve the app
   - Compensation and thank you

Success Metrics:
- Task completion rate > 90%
- No critical accessibility barriers
- User satisfaction score > 4/5
- User would recommend app to others with similar disabilities
- User expresses confidence in independent app use
```

## Continuous Integration

### Automated Testing Pipeline

#### CI/CD Accessibility Integration
```yaml
# GitHub Actions workflow for accessibility testing
name: Accessibility Testing Pipeline

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  accessibility-tests:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: npm install
      
    - name: Run axe-core accessibility tests
      run: npm run test:accessibility
      
    - name: Run color contrast validation
      run: npm run test:contrast
      
    - name: Run keyboard navigation tests
      run: npm run test:keyboard
      
    - name: Generate accessibility report
      run: npm run accessibility:report
      
    - name: Upload accessibility artifacts
      uses: actions/upload-artifact@v3
      with:
        name: accessibility-report
        path: reports/accessibility/
        
    - name: Comment PR with accessibility results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('reports/accessibility/summary.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## Accessibility Test Results\n\n${report}`
          });
```

#### Accessibility Quality Gates
```javascript
// Quality gates for accessibility in CI/CD
const accessibilityQualityGates = {
  // Minimum scores required for deployment
  minimumScores: {
    axeScore: 100,        // Zero axe violations allowed
    contrastScore: 95,    // 95% of color combinations must meet AAA standards
    keyboardScore: 100,   // 100% keyboard accessibility required
    screenReaderScore: 95 // 95% of content must be screen reader accessible
  },
  
  // Critical issues that block deployment
  blockingIssues: [
    'keyboard-trap',
    'missing-focus-indicator',
    'insufficient-contrast-critical',
    'missing-alt-text-critical',
    'broken-aria-structure'
  ],
  
  // Warning issues that generate reports but don't block
  warningIssues: [
    'insufficient-contrast-minor',
    'missing-aria-label-minor',
    'suboptimal-heading-structure',
    'missing-skip-link'
  ],
  
  checkQualityGates(testResults) {
    const results = {
      passed: true,
      blockingIssues: [],
      warnings: [],
      scores: {}
    };
    
    // Check minimum scores
    for (const [metric, minimumScore] of Object.entries(this.minimumScores)) {
      const actualScore = testResults[metric] || 0;
      results.scores[metric] = {
        actual: actualScore,
        minimum: minimumScore,
        passed: actualScore >= minimumScore
      };
      
      if (actualScore < minimumScore) {
        results.passed = false;
        results.blockingIssues.push(`${metric} score ${actualScore} is below minimum ${minimumScore}`);
      }
    }
    
    // Check for critical blocking issues
    const foundBlockingIssues = testResults.issues?.filter(issue => 
      this.blockingIssues.includes(issue.type)
    ) || [];
    
    if (foundBlockingIssues.length > 0) {
      results.passed = false;
      results.blockingIssues.push(...foundBlockingIssues.map(issue => issue.description));
    }
    
    // Collect warnings
    const foundWarnings = testResults.issues?.filter(issue => 
      this.warningIssues.includes(issue.type)
    ) || [];
    
    results.warnings = foundWarnings.map(warning => warning.description);
    
    return results;
  }
};

module.exports = accessibilityQualityGates;
```

---

## Related Documentation

- [Accessibility Guidelines](./guidelines.md) - Comprehensive accessibility implementation standards
- [Accessibility Compliance](./compliance.md) - WCAG 2.1 AAA compliance documentation and audit results
- [Design System Accessibility](../design-system/README.md) - Accessibility built into design system components
- [Platform Accessibility](../design-system/platform-adaptations/) - Platform-specific accessibility implementations

## Testing Resources

### Tools and Software
- **Screen Readers**: VoiceOver (iOS), TalkBack (Android), NVDA (Windows), JAWS (Windows)
- **Automated Testing**: axe-core, Lighthouse, Pa11y, aXe DevTools
- **Manual Testing**: Accessibility Inspector (iOS), Accessibility Scanner (Android)
- **Color Tools**: Colour Contrast Analyser, WebAIM Contrast Checker
- **Simulation Tools**: Chrome DevTools, Firefox Accessibility Inspector

### External Resources
- **WCAG 2.1 Guidelines**: Official W3C accessibility guidelines and techniques
- **Platform Documentation**: iOS Accessibility Programming Guide, Android Accessibility Developer Guide
- **Testing Communities**: WebAIM community, A11y Slack community, accessibility testing forums
- **User Testing Services**: Access Works, Fable Tech Labs, UserTesting accessibility panel

---

*This comprehensive testing strategy ensures that FlirtCraft's mission of building romantic conversation confidence is accessible to users of all abilities, creating an inclusive environment where everyone can develop their social skills with dignity and independence.*