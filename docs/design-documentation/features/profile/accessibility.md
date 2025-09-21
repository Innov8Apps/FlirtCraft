# Profile Feature - Accessibility

---
title: Profile Feature Accessibility Implementation
description: Complete accessibility specifications for inclusive profile management and data control
feature: profile
last-updated: 2025-09-07
version: 2.0.0
related-files: 
  - README.md
  - user-journey.md
  - screen-states.md
  - interactions.md
  - implementation.md
  - ../../accessibility/guidelines.md
dependencies:
  - React Native accessibility APIs
  - platform-specific form accessibility
status: approved
---

## Accessibility Overview

The profile feature handles sensitive personal information and preferences, making accessibility critical for ensuring all users can safely and independently manage their data. This includes comprehensive support for screen readers, keyboard navigation, form accessibility, and cognitive accessibility features.

## Table of Contents

1. [Form Accessibility](#form-accessibility)
2. [Screen Reader Experience](#screen-reader-experience)
3. [Keyboard Navigation](#keyboard-navigation)
4. [Cognitive Accessibility](#cognitive-accessibility)
5. [Visual Accessibility](#visual-accessibility)
6. [Motor Accessibility](#motor-accessibility)

---

## Form Accessibility

### Profile Creation Form Flow

#### Multi-Step Form Navigation

```javascript
// React Native Accessibility Implementation
const ProfileCreationForm = ({ currentStep, totalSteps }) => {
  const [stepAnnouncement, setStepAnnouncement] = useState('');
  
  useEffect(() => {
    const announcement = `Step ${currentStep} of ${totalSteps}. ${getStepTitle(currentStep)}`;
    setStepAnnouncement(announcement);
    
    // Announce step changes
    AccessibilityInfo.announceForAccessibility(announcement);
  }, [currentStep, totalSteps]);

  return (
    <View
      accessible={true}
      accessibilityRole="form"
      accessibilityLabel={`Profile setup, ${stepAnnouncement}`}
      accessibilityLiveRegion="polite"
    >
      <ProgressIndicator 
        current={currentStep} 
        total={totalSteps}
        accessibilityLabel={`Progress: step ${currentStep} of ${totalSteps}`}
      />
      
      <StepContent 
        step={currentStep}
        accessibilityLiveRegion="polite"
      />
    </View>
  );
};

const getStepTitle = (step) => {
  const titles = {
    1: 'Basic information',
    2: 'Dating preferences', 
    3: 'Learning goals',
    4: 'Progression settings',
    5: 'Review and confirm',
  };
  return titles[step] || 'Profile setup';
};
```

#### Form Field Accessibility

```javascript
const AccessibleFormField = ({ 
  label, 
  value, 
  error, 
  required, 
  helpText,
  onChangeText,
  ...props 
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const fieldId = useId();
  const errorId = error ? `${fieldId}-error` : undefined;
  const helpId = helpText ? `${fieldId}-help` : undefined;
  
  const accessibilityLabelText = [
    label,
    required ? 'required' : 'optional',
    error ? `error: ${error}` : '',
    helpText || '',
  ].filter(Boolean).join(', ');

  return (
    <View style={styles.fieldContainer}>
      <Text
        style={[styles.label, required && styles.requiredLabel]}
        accessibilityRole="text"
        nativeID={`${fieldId}-label`}
      >
        {label}
        {required && <Text style={styles.requiredIndicator}> *</Text>}
      </Text>
      
      <TextInput
        {...props}
        value={value}
        onChangeText={onChangeText}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        accessible={true}
        accessibilityRole="text"
        accessibilityLabel={accessibilityLabelText}
        accessibilityLabelledBy={`${fieldId}-label`}
        accessibilityDescribedBy={[errorId, helpId].filter(Boolean).join(' ')}
        accessibilityRequired={required}
        accessibilityInvalid={!!error}
        style={[
          styles.input,
          isFocused && styles.inputFocused,
          error && styles.inputError,
        ]}
      />
      
      {helpText && (
        <Text
          nativeID={helpId}
          style={styles.helpText}
          accessibilityRole="text"
        >
          {helpText}
        </Text>
      )}
      
      {error && (
        <Text
          nativeID={errorId}
          style={styles.errorText}
          accessibilityRole="alert"
          accessibilityLiveRegion="assertive"
        >
          {error}
        </Text>
      )}
    </View>
  );
};
```

### Age Selection Accessibility

#### Custom Age Picker with Screen Reader Support

```javascript
const AccessibleAgePicker = ({ selectedAge, onAgeChange, minAge = 18, maxAge = 100 }) => {
  const [isPickerVisible, setIsPickerVisible] = useState(false);
  const ageRange = Array.from({ length: maxAge - minAge + 1 }, (_, i) => minAge + i);
  
  return (
    <>
      <TouchableOpacity
        onPress={() => setIsPickerVisible(true)}
        accessible={true}
        accessibilityRole="button"
        accessibilityLabel={`Age: ${selectedAge || 'not selected'}. Double tap to select age.`}
        accessibilityHint="Opens age selection picker"
        style={styles.ageSelector}
      >
        <Text style={styles.ageSelectorText}>
          {selectedAge ? `Age: ${selectedAge}` : 'Select your age'}
        </Text>
        <Icon name="chevron-down" size={20} color="#666" />
      </TouchableOpacity>

      <Modal
        visible={isPickerVisible}
        transparent={true}
        accessibilityViewIsModal={true}
      >
        <View
          style={styles.pickerOverlay}
          accessible={false}
          accessibilityElementsHidden={false}
        >
          <View
            style={styles.pickerContainer}
            accessible={true}
            accessibilityRole="dialog"
            accessibilityLabel="Age selection"
          >
            <Text
              style={styles.pickerTitle}
              accessibilityRole="header"
            >
              Select your age
            </Text>
            
            <ScrollView
              style={styles.ageList}
              accessible={false}
              accessibilityLabel="Age options"
            >
              {ageRange.map((age) => (
                <TouchableOpacity
                  key={age}
                  onPress={() => {
                    onAgeChange(age);
                    setIsPickerVisible(false);
                    AccessibilityInfo.announceForAccessibility(`Age ${age} selected`);
                  }}
                  accessible={true}
                  accessibilityRole="button"
                  accessibilityLabel={`Age ${age}`}
                  accessibilityState={{ selected: selectedAge === age }}
                  style={[
                    styles.ageOption,
                    selectedAge === age && styles.ageOptionSelected,
                  ]}
                >
                  <Text style={[
                    styles.ageOptionText,
                    selectedAge === age && styles.ageOptionTextSelected,
                  ]}>
                    {age}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
            
            <TouchableOpacity
              onPress={() => setIsPickerVisible(false)}
              accessible={true}
              accessibilityRole="button"
              accessibilityLabel="Close age picker"
              style={styles.pickerCloseButton}
            >
              <Text style={styles.pickerCloseText}>Done</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </>
  );
};
```

### Multi-Selection Accessibility

#### Skill Goals Selection with Screen Reader Support

```javascript
const AccessibleSkillSelection = ({ skills, selectedSkills, onSkillToggle, maxSelections = 3 }) => {
  const [selectionAnnouncement, setSelectionAnnouncement] = useState('');
  
  const handleSkillToggle = (skillId) => {
    const skill = skills.find(s => s.id === skillId);
    const isCurrentlySelected = selectedSkills.includes(skillId);
    const newCount = isCurrentlySelected ? selectedSkills.length - 1 : selectedSkills.length + 1;
    
    if (!isCurrentlySelected && selectedSkills.length >= maxSelections) {
      const announcement = `Cannot select more than ${maxSelections} skills. Please deselect another skill first.`;
      setSelectionAnnouncement(announcement);
      AccessibilityInfo.announceForAccessibility(announcement);
      return;
    }
    
    onSkillToggle(skillId);
    
    const action = isCurrentlySelected ? 'deselected' : 'selected';
    const countText = `${newCount} of ${maxSelections} skills selected`;
    const announcement = `${skill.name} ${action}. ${countText}`;
    
    setSelectionAnnouncement(announcement);
    AccessibilityInfo.announceForAccessibility(announcement);
  };

  return (
    <View
      accessible={true}
      accessibilityRole="group"
      accessibilityLabel={`Skill selection. ${selectedSkills.length} of ${maxSelections} selected.`}
    >
      <Text
        style={styles.sectionTitle}
        accessibilityRole="header"
        accessibilityLevel={2}
      >
        Select your learning goals (up to {maxSelections})
      </Text>
      
      <Text
        style={styles.selectionCounter}
        accessibilityLiveRegion="polite"
        accessibilityLabel={`${selectedSkills.length} of ${maxSelections} skills selected`}
      >
        {selectedSkills.length}/{maxSelections} selected
      </Text>

      {skills.map((skill) => {
        const isSelected = selectedSkills.includes(skill.id);
        const isDisabled = !isSelected && selectedSkills.length >= maxSelections;
        
        return (
          <TouchableOpacity
            key={skill.id}
            onPress={() => handleSkillToggle(skill.id)}
            disabled={isDisabled}
            accessible={true}
            accessibilityRole="checkbox"
            accessibilityState={{ 
              checked: isSelected,
              disabled: isDisabled,
            }}
            accessibilityLabel={skill.name}
            accessibilityHint={skill.description}
            style={[
              styles.skillCard,
              isSelected && styles.skillCardSelected,
              isDisabled && styles.skillCardDisabled,
            ]}
          >
            <View style={styles.skillCardContent}>
              <View style={styles.skillIconContainer}>
                <Icon name={skill.icon} size={24} color={isSelected ? '#F97316' : '#6B7280'} />
                {isSelected && (
                  <View style={styles.selectedIndicator} accessibilityElementsHidden={true}>
                    <Icon name="check" size={12} color="white" />
                  </View>
                )}
              </View>
              
              <View style={styles.skillTextContent}>
                <Text style={[styles.skillTitle, isSelected && styles.skillTitleSelected]}>
                  {skill.name}
                </Text>
                <Text style={[styles.skillDescription, isSelected && styles.skillDescriptionSelected]}>
                  {skill.description}
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        );
      })}
    </View>
  );
};
```

---

## Screen Reader Experience

### VoiceOver (iOS) Implementation

#### Profile Navigation Structure

```javascript
const ProfileScreen = () => {
  return (
    <ScrollView
      accessible={true}
      accessibilityRole="main"
      accessibilityLabel="Profile settings"
    >
      <View
        accessible={true}
        accessibilityRole="header"
        accessibilityLevel={1}
      >
        <Text>Your Profile</Text>
      </View>
      
      <View
        accessible={true}
        accessibilityRole="region"
        accessibilityLabel="Personal information"
      >
        <ProfileBasicInfo />
      </View>
      
      <View
        accessible={true}
        accessibilityRole="region"
        accessibilityLabel="Dating preferences"
      >
        <DatingPreferences />
      </View>
      
      <View
        accessible={true}
        accessibilityRole="region"
        accessibilityLabel="Learning goals and progress"
      >
        <LearningGoals />
        <ProgressSummary />
      </View>
      
      <View
        accessible={true}
        accessibilityRole="region"
        accessibilityLabel="Privacy and data controls"
      >
        <PrivacySettings />
      </View>
    </ScrollView>
  );
};
```

#### Progress Visualization for Screen Readers

```javascript
const AccessibleProgressChart = ({ progressData, skillName }) => {
  const [chartDescription, setChartDescription] = useState('');
  
  useEffect(() => {
    const description = generateChartDescription(progressData, skillName);
    setChartDescription(description);
  }, [progressData, skillName]);

  const generateChartDescription = (data, skill) => {
    if (!data || data.length === 0) return `No progress data available for ${skill}`;
    
    const latest = data[data.length - 1];
    const earliest = data[0];
    const trend = latest.score > earliest.score ? 'improving' : 
                  latest.score < earliest.score ? 'declining' : 'stable';
    
    const changeAmount = Math.abs(latest.score - earliest.score);
    
    return `${skill} progress: Currently ${latest.score} out of 100. ` +
           `${trend} by ${changeAmount} points over ${data.length} conversations. ` +
           `Highest score: ${Math.max(...data.map(d => d.score))}, ` +
           `lowest score: ${Math.min(...data.map(d => d.score))}.`;
  };

  return (
    <View
      accessible={true}
      accessibilityRole="img"
      accessibilityLabel={chartDescription}
    >
      {/* Visual chart for sighted users */}
      <ProgressChart data={progressData} />
      
      {/* Hidden text alternative for screen readers */}
      <Text
        style={{ position: 'absolute', left: -10000 }}
        accessibilityElementsHidden={false}
        accessible={true}
      >
        {chartDescription}
      </Text>
      
      {/* Data table alternative */}
      <TouchableOpacity
        onPress={() => setShowDataTable(true)}
        accessible={true}
        accessibilityRole="button"
        accessibilityLabel="View progress data as table"
        style={styles.dataTableButton}
      >
        <Text>View as data table</Text>
      </TouchableOpacity>
    </View>
  );
};

const ProgressDataTable = ({ data, skillName }) => {
  return (
    <View
      accessible={true}
      accessibilityRole="table"
      accessibilityLabel={`Progress data table for ${skillName}`}
    >
      <View
        accessible={true}
        accessibilityRole="columnheader"
        style={styles.tableHeader}
      >
        <Text>Date</Text>
        <Text>Score</Text>
        <Text>Change</Text>
      </View>
      
      {data.map((entry, index) => {
        const previousScore = index > 0 ? data[index - 1].score : entry.score;
        const change = entry.score - previousScore;
        const changeText = change > 0 ? `+${change}` : change < 0 ? `${change}` : 'No change';
        
        return (
          <View
            key={entry.date}
            accessible={true}
            accessibilityRole="row"
            accessibilityLabel={`${entry.date}, score ${entry.score}, ${changeText} points`}
            style={styles.tableRow}
          >
            <Text>{entry.date}</Text>
            <Text>{entry.score}</Text>
            <Text>{changeText}</Text>
          </View>
        );
      })}
    </View>
  );
};
```

### TalkBack (Android) Implementation

#### Profile Settings Navigation

```javascript
const useProfileAccessibility = () => {
  const announcePreferenceChange = (settingName, newValue) => {
    const announcement = `${settingName} changed to ${newValue}`;
    AccessibilityInfo.announceForAccessibility(announcement);
  };

  const announcePrivacyChange = (settingName, isEnabled) => {
    const status = isEnabled ? 'enabled' : 'disabled';
    const announcement = `${settingName} ${status}`;
    AccessibilityInfo.announceForAccessibility(announcement);
  };

  const announceSaveSuccess = () => {
    AccessibilityInfo.announceForAccessibility('Profile settings saved successfully');
  };

  const announceSaveError = (error) => {
    AccessibilityInfo.announceForAccessibility(`Error saving settings: ${error}`);
  };

  return {
    announcePreferenceChange,
    announcePrivacyChange,
    announceSaveSuccess,
    announceSaveError,
  };
};
```

---

## Keyboard Navigation

### Form Navigation System

#### Tab Order Management

```javascript
const useProfileKeyboardNavigation = () => {
  const fieldRefs = useRef({});
  const [currentFieldIndex, setCurrentFieldIndex] = useState(0);
  const [fieldOrder, setFieldOrder] = useState([]);

  useEffect(() => {
    // Define logical tab order for profile forms
    const order = [
      'age',
      'location',
      'genderPreference',
      'ageRange',
      'relationshipGoals',
      'skill1',
      'skill2', 
      'skill3',
      'progressionStyle',
      'feedbackLevel',
      'saveButton',
      'cancelButton',
    ];
    setFieldOrder(order);
  }, []);

  const focusNextField = () => {
    const nextIndex = Math.min(currentFieldIndex + 1, fieldOrder.length - 1);
    const nextFieldId = fieldOrder[nextIndex];
    
    if (fieldRefs.current[nextFieldId]) {
      fieldRefs.current[nextFieldId].focus();
      setCurrentFieldIndex(nextIndex);
    }
  };

  const focusPreviousField = () => {
    const prevIndex = Math.max(currentFieldIndex - 1, 0);
    const prevFieldId = fieldOrder[prevIndex];
    
    if (fieldRefs.current[prevFieldId]) {
      fieldRefs.current[prevFieldId].focus();
      setCurrentFieldIndex(prevIndex);
    }
  };

  const handleKeyPress = (event) => {
    switch (event.key) {
      case 'Tab':
        event.preventDefault();
        if (event.shiftKey) {
          focusPreviousField();
        } else {
          focusNextField();
        }
        break;
        
      case 'Enter':
        if (currentFieldIndex === fieldOrder.length - 2) { // Save button
          handleSave();
        }
        break;
        
      case 'Escape':
        handleCancel();
        break;
    }
  };

  return { fieldRefs, handleKeyPress, focusNextField, focusPreviousField };
};
```

#### Keyboard Shortcuts for Profile Actions

```javascript
const ProfileKeyboardShortcuts = () => {
  useEffect(() => {
    const handleKeyDown = (event) => {
      // Only handle shortcuts when not in form fields
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
      }

      if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
          case 's':
            event.preventDefault();
            handleSaveProfile();
            break;
            
          case 'e':
            event.preventDefault();
            handleEditProfile();
            break;
            
          case 'p':
            event.preventDefault();
            handleViewProgress();
            break;
            
          case ',':
            event.preventDefault();
            handleOpenSettings();
            break;
        }
      }
      
      // Navigation shortcuts
      switch (event.key) {
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
          if (event.altKey) {
            event.preventDefault();
            const stepIndex = parseInt(event.key) - 1;
            navigateToStep(stepIndex);
          }
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return null; // This component only handles keyboard events
};
```

### Range Slider Keyboard Accessibility

#### Accessible Age Range Slider

```javascript
const KeyboardAccessibleRangeSlider = ({ 
  minValue, 
  maxValue, 
  currentMin, 
  currentMax, 
  onRangeChange,
  step = 1 
}) => {
  const [focusedThumb, setFocusedThumb] = useState(null); // 'min' | 'max' | null
  
  const handleKeyPress = (event, thumbType) => {
    const isMinThumb = thumbType === 'min';
    const currentValue = isMinThumb ? currentMin : currentMax;
    let newValue = currentValue;
    
    switch (event.key) {
      case 'ArrowRight':
      case 'ArrowUp':
        newValue = Math.min(currentValue + step, maxValue);
        break;
        
      case 'ArrowLeft':
      case 'ArrowDown':
        newValue = Math.max(currentValue - step, minValue);
        break;
        
      case 'PageUp':
        newValue = Math.min(currentValue + step * 10, maxValue);
        break;
        
      case 'PageDown':
        newValue = Math.max(currentValue - step * 10, minValue);
        break;
        
      case 'Home':
        newValue = minValue;
        break;
        
      case 'End':
        newValue = maxValue;
        break;
        
      default:
        return;
    }
    
    event.preventDefault();
    
    if (isMinThumb && newValue <= currentMax) {
      onRangeChange(newValue, currentMax);
    } else if (!isMinThumb && newValue >= currentMin) {
      onRangeChange(currentMin, newValue);
    }
    
    // Announce value change
    AccessibilityInfo.announceForAccessibility(
      `${isMinThumb ? 'Minimum' : 'Maximum'} age: ${newValue}`
    );
  };

  return (
    <View style={styles.rangeSliderContainer}>
      <Text style={styles.rangeLabel}>Age Range: {currentMin} - {currentMax}</Text>
      
      <View style={styles.sliderTrack}>
        <View
          ref={(ref) => (minThumbRef.current = ref)}
          style={[styles.thumb, { left: `${(currentMin - minValue) / (maxValue - minValue) * 100}%` }]}
          accessible={true}
          accessibilityRole="slider"
          accessibilityLabel="Minimum age"
          accessibilityValue={{
            min: minValue,
            max: maxValue,
            now: currentMin,
          }}
          onFocus={() => setFocusedThumb('min')}
          onBlur={() => setFocusedThumb(null)}
          onKeyDown={(event) => handleKeyPress(event, 'min')}
          tabIndex={0}
        />
        
        <View
          ref={(ref) => (maxThumbRef.current = ref)}
          style={[styles.thumb, { left: `${(currentMax - minValue) / (maxValue - minValue) * 100}%` }]}
          accessible={true}
          accessibilityRole="slider"
          accessibilityLabel="Maximum age"
          accessibilityValue={{
            min: minValue,
            max: maxValue,
            now: currentMax,
          }}
          onFocus={() => setFocusedThumb('max')}
          onBlur={() => setFocusedThumb(null)}
          onKeyDown={(event) => handleKeyPress(event, 'max')}
          tabIndex={0}
        />
      </View>
      
      <Text style={styles.sliderInstructions}>
        Use arrow keys to adjust, Page Up/Down for larger steps, Home/End for min/max values
      </Text>
    </View>
  );
};
```

---

## Cognitive Accessibility

### Simplified Profile Creation

#### Progressive Disclosure for Complex Preferences

```javascript
const CognitiveAccessibleProfileForm = () => {
  const [complexityLevel, setComplexityLevel] = useState('simple'); // 'simple' | 'standard' | 'advanced'
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);

  const getFormFields = () => {
    const baseFields = ['age', 'basicPreferences'];
    
    switch (complexityLevel) {
      case 'simple':
        return baseFields;
      case 'standard':
        return [...baseFields, 'learningGoals', 'basicSettings'];
      case 'advanced':
        return [...baseFields, 'learningGoals', 'advancedSettings', 'privacyControls'];
      default:
        return baseFields;
    }
  };

  const simplifyLanguage = (text) => {
    const simplifications = {
      'personalization': 'customization',
      'optimization': 'improvement',
      'algorithm': 'system',
      'demographics': 'basic info',
      'parameters': 'settings',
    };
    
    return Object.entries(simplifications).reduce(
      (simplified, [complex, simple]) => 
        simplified.replace(new RegExp(complex, 'gi'), simple),
      text
    );
  };

  return (
    <View
      accessible={true}
      accessibilityRole="form"
      accessibilityLabel="Profile setup form"
    >
      <View style={styles.complexitySelector}>
        <Text style={styles.sectionTitle}>How detailed would you like to be?</Text>
        
        {['simple', 'standard', 'advanced'].map((level) => (
          <TouchableOpacity
            key={level}
            onPress={() => setComplexityLevel(level)}
            accessible={true}
            accessibilityRole="radio"
            accessibilityState={{ checked: complexityLevel === level }}
            style={[
              styles.complexityOption,
              complexityLevel === level && styles.complexityOptionSelected,
            ]}
          >
            <Text style={styles.complexityOptionText}>
              {level === 'simple' && 'Simple - Just the basics'}
              {level === 'standard' && 'Standard - Balanced setup'}
              {level === 'advanced' && 'Advanced - Full customization'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <FormFields 
        fields={getFormFields()}
        simplifyLanguage={complexityLevel === 'simple'}
        showHelpText={complexityLevel !== 'advanced'}
      />
    </View>
  );
};
```

#### Clear Error Messages and Help Text

```javascript
const CognitiveAccessibleField = ({ 
  label, 
  error, 
  helpText, 
  simplifyLanguage = false,
  ...props 
}) => {
  const getSimplifiedError = (error) => {
    const errorSimplifications = {
      'This field is required': 'Please fill this out',
      'Invalid format': 'Please check your answer',
      'Age must be 18 or older': 'You must be at least 18 years old',
      'Maximum selections exceeded': 'You can only choose 3 options',
    };
    
    return simplifyLanguage ? 
      errorSimplifications[error] || error : 
      error;
  };

  const getHelpTextWithContext = (helpText) => {
    if (!helpText) return '';
    
    return simplifyLanguage ? 
      `Help: ${helpText}` : 
      helpText;
  };

  return (
    <View style={styles.fieldWrapper}>
      <Text style={styles.fieldLabel}>
        {label}
        {props.required && <Text style={styles.required}> (required)</Text>}
      </Text>
      
      {helpText && (
        <Text 
          style={styles.helpText}
          accessible={true}
          accessibilityRole="text"
        >
          {getHelpTextWithContext(helpText)}
        </Text>
      )}
      
      <FormInput {...props} />
      
      {error && (
        <View 
          style={styles.errorContainer}
          accessible={true}
          accessibilityRole="alert"
          accessibilityLiveRegion="assertive"
        >
          <Icon name="alert-circle" size={16} color="#EF4444" />
          <Text style={styles.errorText}>
            {getSimplifiedError(error)}
          </Text>
        </View>
      )}
    </View>
  );
};
```

### Time-Based Considerations

#### Auto-Save and Session Management

```javascript
const useProfileSessionManagement = () => {
  const [sessionTimeout, setSessionTimeout] = useState(30 * 60 * 1000); // 30 minutes
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(true);
  const lastActivityRef = useRef(Date.now());
  const autoSaveIntervalRef = useRef(null);

  useEffect(() => {
    if (autoSaveEnabled) {
      autoSaveIntervalRef.current = setInterval(() => {
        const now = Date.now();
        const timeSinceActivity = now - lastActivityRef.current;
        
        if (timeSinceActivity < 5 * 60 * 1000) { // 5 minutes
          autoSaveProfile();
        }
      }, 60 * 1000); // Check every minute
    }

    return () => {
      if (autoSaveIntervalRef.current) {
        clearInterval(autoSaveIntervalRef.current);
      }
    };
  }, [autoSaveEnabled]);

  const updateActivity = () => {
    lastActivityRef.current = Date.now();
  };

  const showSessionWarning = () => {
    const timeLeft = Math.ceil((sessionTimeout - (Date.now() - lastActivityRef.current)) / 60000);
    
    return (
      <View 
        style={styles.sessionWarning}
        accessible={true}
        accessibilityRole="alert"
        accessibilityLiveRegion="assertive"
      >
        <Icon name="clock" size={20} color="#F97316" />
        <Text style={styles.sessionWarningText}>
          Your session will expire in {timeLeft} minutes. 
          Any unsaved changes will be lost.
        </Text>
        <TouchableOpacity
          onPress={extendSession}
          accessible={true}
          accessibilityRole="button"
          accessibilityLabel="Extend session"
          style={styles.extendButton}
        >
          <Text>Continue Working</Text>
        </TouchableOpacity>
      </View>
    );
  };

  return { updateActivity, showSessionWarning, autoSaveEnabled, setAutoSaveEnabled };
};
```

---

## Visual Accessibility

### High Contrast and Color Blindness Support

#### Accessible Color Scheme Implementation

```javascript
const useProfileVisualAccessibility = () => {
  const [highContrast, setHighContrast] = useState(false);
  const [colorBlindMode, setColorBlindMode] = useState(null); // null | 'deuteranopia' | 'protanopia' | 'tritanopia'

  useEffect(() => {
    AccessibilityInfo.isHighContrastEnabled().then(setHighContrast);
    
    const subscription = AccessibilityInfo.addEventListener(
      'highContrastChanged',
      setHighContrast
    );
    
    return () => subscription?.remove();
  }, []);

  const getAccessibleColors = () => {
    if (highContrast) {
      return {
        background: '#FFFFFF',
        text: '#000000',
        primary: '#FF4500',  // High contrast orange
        secondary: '#CC3300',  // High contrast red-orange
        error: '#FF0000',
        success: '#008000',
        border: '#000000',
      };
    }
    
    if (colorBlindMode) {
      return getColorBlindFriendlyColors(colorBlindMode);
    }
    
    return {
      background: '#F9FAFB',
      text: '#1F2937',
      primary: '#F97316',
      secondary: '#6B7280',
      error: '#EF4444',
      success: '#10B981',
      border: '#E5E7EB',
    };
  };

  const getColorBlindFriendlyColors = (type) => {
    // Colors tested for different types of color blindness
    const colorSets = {
      deuteranopia: {
        primary: '#0077BB',   // Blue instead of orange
        secondary: '#CC6677', // Pink instead of gray
        error: '#882255',     // Dark magenta instead of red
        success: '#44AA99',   // Teal instead of green
      },
      protanopia: {
        primary: '#0077BB',
        secondary: '#999933',
        error: '#AA4499',
        success: '#117733',
      },
      tritanopia: {
        primary: '#CC6677',
        secondary: '#DDCC77',
        error: '#AA4499',
        success: '#44AA99',
      },
    };
    
    return {
      ...getAccessibleColors(),
      ...colorSets[type],
    };
  };

  return { 
    highContrast, 
    colorBlindMode, 
    setColorBlindMode,
    getAccessibleColors,
  };
};
```

### Dynamic Type Support

#### Scalable Text for Profile Forms

```javascript
const useAccessibleTypography = () => {
  const [fontScale, setFontScale] = useState(1);
  const [preferredFontSize, setPreferredFontSize] = useState('medium');

  useEffect(() => {
    PixelRatio.getFontScale().then(setFontScale);
    
    const subscription = Appearance.addChangeListener(() => {
      PixelRatio.getFontScale().then(setFontScale);
    });
    
    return () => subscription?.remove();
  }, []);

  const getScaledFontSize = (baseSize) => {
    const scaledSize = baseSize * fontScale;
    const maxSize = baseSize * 2; // Cap at 200% for layout stability
    return Math.min(scaledSize, maxSize);
  };

  const getAccessibleTextStyles = () => {
    const baseSizes = {
      small: 12,
      medium: 16,
      large: 20,
      xlarge: 24,
    };

    return {
      caption: {
        fontSize: getScaledFontSize(baseSizes.small),
        lineHeight: getScaledFontSize(baseSizes.small * 1.4),
      },
      body: {
        fontSize: getScaledFontSize(baseSizes.medium),
        lineHeight: getScaledFontSize(baseSizes.medium * 1.5),
      },
      heading: {
        fontSize: getScaledFontSize(baseSizes.large),
        lineHeight: getScaledFontSize(baseSizes.large * 1.3),
        fontWeight: 'bold',
      },
      title: {
        fontSize: getScaledFontSize(baseSizes.xlarge),
        lineHeight: getScaledFontSize(baseSizes.xlarge * 1.2),
        fontWeight: 'bold',
      },
    };
  };

  return { fontScale, getScaledFontSize, getAccessibleTextStyles };
};
```

---

## Motor Accessibility

### Touch Target Optimization

#### Accessible Form Controls

```javascript
const AccessibleFormControls = () => {
  const [touchTargetSize, setTouchTargetSize] = useState('standard'); // 'small' | 'standard' | 'large'
  
  const getTouchTargetDimensions = () => {
    const sizes = {
      small: { minWidth: 44, minHeight: 44 },
      standard: { minWidth: 56, minHeight: 56 },
      large: { minWidth: 64, minHeight: 64 },
    };
    return sizes[touchTargetSize];
  };

  return {
    TouchableButton: ({ children, onPress, accessibilityLabel, ...props }) => {
      const dimensions = getTouchTargetDimensions();
      
      return (
        <TouchableOpacity
          onPress={onPress}
          accessible={true}
          accessibilityRole="button"
          accessibilityLabel={accessibilityLabel}
          style={[
            dimensions,
            styles.touchableButton,
            { 
              justifyContent: 'center',
              alignItems: 'center',
              padding: 12,
            }
          ]}
          hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
          {...props}
        >
          {children}
        </TouchableOpacity>
      );
    },
    
    AccessibleCheckbox: ({ checked, onPress, label, disabled = false }) => {
      const dimensions = getTouchTargetDimensions();
      
      return (
        <TouchableOpacity
          onPress={onPress}
          disabled={disabled}
          accessible={true}
          accessibilityRole="checkbox"
          accessibilityState={{ checked, disabled }}
          accessibilityLabel={label}
          style={[
            dimensions,
            styles.checkboxContainer,
            disabled && styles.disabled,
          ]}
          hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
        >
          <View style={[
            styles.checkbox,
            checked && styles.checkboxChecked,
            disabled && styles.checkboxDisabled,
          ]}>
            {checked && (
              <Icon name="check" size={16} color={disabled ? '#9CA3AF' : '#FFFFFF'} />
            )}
          </View>
          <Text style={[
            styles.checkboxLabel,
            disabled && styles.checkboxLabelDisabled,
          ]}>
            {label}
          </Text>
        </TouchableOpacity>
      );
    },
  };
};
```

### Alternative Input Methods

#### Voice Input Support for Profile Fields

```javascript
const VoiceInputField = ({ 
  label, 
  value, 
  onChangeText, 
  voiceInputEnabled = true,
  ...props 
}) => {
  const [isListening, setIsListening] = useState(false);
  const [voiceError, setVoiceError] = useState(null);

  const startVoiceInput = async () => {
    if (!voiceInputEnabled) return;
    
    try {
      setIsListening(true);
      setVoiceError(null);
      
      const result = await Voice.start('en-US');
      
      Voice.onSpeechResults = (event) => {
        if (event.value && event.value[0]) {
          onChangeText(event.value[0]);
          setIsListening(false);
          Voice.stop();
        }
      };
      
      Voice.onSpeechError = (error) => {
        setVoiceError(error.error.message);
        setIsListening(false);
        Voice.stop();
      };
      
    } catch (error) {
      setVoiceError('Voice input not available');
      setIsListening(false);
    }
  };

  const stopVoiceInput = () => {
    Voice.stop();
    setIsListening(false);
  };

  return (
    <View style={styles.voiceInputContainer}>
      <View style={styles.inputRow}>
        <TextInput
          value={value}
          onChangeText={onChangeText}
          placeholder={`Enter ${label.toLowerCase()}`}
          accessible={true}
          accessibilityLabel={label}
          style={[styles.textInput, { flex: 1 }]}
          {...props}
        />
        
        {voiceInputEnabled && (
          <TouchableOpacity
            onPress={isListening ? stopVoiceInput : startVoiceInput}
            accessible={true}
            accessibilityRole="button"
            accessibilityLabel={isListening ? 'Stop voice input' : 'Start voice input'}
            accessibilityHint={`Use voice to input ${label.toLowerCase()}`}
            style={[
              styles.voiceButton,
              isListening && styles.voiceButtonActive,
            ]}
          >
            <Icon 
              name={isListening ? 'mic-off' : 'mic'} 
              size={20} 
              color={isListening ? '#EF4444' : '#6B7280'} 
            />
          </TouchableOpacity>
        )}
      </View>
      
      {isListening && (
        <Text 
          style={styles.listeningIndicator}
          accessibilityLiveRegion="polite"
        >
          Listening... Speak now
        </Text>
      )}
      
      {voiceError && (
        <Text 
          style={styles.voiceError}
          accessibilityRole="alert"
          accessibilityLiveRegion="assertive"
        >
          Voice input error: {voiceError}
        </Text>
      )}
    </View>
  );
};
```

## Testing and Validation

### Accessibility Testing Procedures

#### Automated Accessibility Testing

```javascript
const runProfileAccessibilityTests = async () => {
  const testResults = {
    formAccessibility: await testFormAccessibility(),
    keyboardNavigation: await testKeyboardNavigation(),
    screenReaderCompatibility: await testScreenReaderFlow(),
    colorContrast: await testColorContrast(),
    touchTargets: await testTouchTargetSizes(),
  };
  
  return testResults;
};

const testFormAccessibility = async () => {
  const issues = [];
  
  // Test all form fields have labels
  const unlabeledFields = await findUnlabeledFormFields();
  if (unlabeledFields.length > 0) {
    issues.push(`Unlabeled form fields found: ${unlabeledFields.join(', ')}`);
  }
  
  // Test error states have proper ARIA
  const errorFields = await findFieldsWithErrors();
  const errorFieldsWithoutAria = errorFields.filter(field => !field.hasAriaInvalid);
  if (errorFieldsWithoutAria.length > 0) {
    issues.push(`Error fields without ARIA: ${errorFieldsWithoutAria.map(f => f.id).join(', ')}`);
  }
  
  return { passed: issues.length === 0, issues };
};
```

## Related Documentation

- **[Accessibility Guidelines](../../accessibility/guidelines.md)** - Overall accessibility strategy
- **[Screen States](./screen-states.md)** - Visual accessibility specifications
- **[Interactions](./interactions.md)** - Accessible interaction patterns
- **[Implementation](./implementation.md)** - Technical accessibility implementation

## Implementation Checklist

### Form Accessibility
- [ ] All form fields have proper labels and descriptions
- [ ] Error states include ARIA invalid and live region announcements
- [ ] Multi-step forms announce progress and step changes
- [ ] Required fields are clearly marked and announced

### Navigation Accessibility  
- [ ] Logical tab order throughout all profile screens
- [ ] Keyboard shortcuts for common profile actions
- [ ] Skip links for long forms and complex layouts
- [ ] Focus management during screen transitions

### Content Accessibility
- [ ] Progress charts have text alternatives and data tables
- [ ] Achievement unlocks have proper announcements
- [ ] All interactive elements meet minimum touch target sizes
- [ ] High contrast and color blind support implemented

### Cognitive Support
- [ ] Progressive disclosure for complex preferences
- [ ] Simplified language options for form text
- [ ] Clear error messages with recovery guidance
- [ ] Auto-save and session management for long forms

## Last Updated
- **Version 1.0.0**: Complete accessibility implementation for profile management
- **Focus**: Inclusive design for sensitive personal data management
- **Next**: Integration testing and user validation with assistive technologies