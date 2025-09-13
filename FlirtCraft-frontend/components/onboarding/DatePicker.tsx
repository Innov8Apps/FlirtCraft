import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Platform } from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import { Ionicons } from '@expo/vector-icons';

interface DatePickerProps {
  value?: Date;
  onChange: (date: Date) => void;
  placeholder?: string;
  minimumDate?: Date;
  maximumDate?: Date;
  error?: string;
}

export const DatePicker: React.FC<DatePickerProps> = ({
  value,
  onChange,
  placeholder = "Select your birth date",
  minimumDate,
  maximumDate,
  error,
}) => {
  const [showPicker, setShowPicker] = useState(false);

  const handleDateChange = (event: any, selectedDate?: Date) => {
    if (Platform.OS === 'android') {
      setShowPicker(false);
    }
    
    if (selectedDate) {
      onChange(selectedDate);
    }
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const showDatePicker = () => {
    setShowPicker(true);
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={showDatePicker}
        style={[
          styles.dateButton,
          error && styles.dateButtonError,
        ]}
        activeOpacity={0.7}
      >
        <Text
          style={[
            styles.dateText,
            !value && styles.placeholderText,
          ]}
        >
          {value ? formatDate(value) : placeholder}
        </Text>
        <Ionicons 
          name="calendar-outline" 
          size={20} 
          color={error ? "#ef4444" : "#6b7280"} 
        />
      </TouchableOpacity>

      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}

      {showPicker && (
        <DateTimePicker
          value={value || new Date()}
          mode="date"
          display={Platform.OS === 'ios' ? 'spinner' : 'default'}
          onChange={handleDateChange}
          minimumDate={minimumDate}
          maximumDate={maximumDate}
          style={Platform.OS === 'ios' ? styles.iosPickerStyle : undefined}
        />
      )}
      
      {Platform.OS === 'ios' && showPicker && (
        <View style={styles.iosPickerContainer}>
          <View style={styles.iosPickerHeader}>
            <TouchableOpacity
              onPress={() => setShowPicker(false)}
              style={styles.iosPickerButton}
            >
              <Text style={styles.iosPickerButtonText}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => setShowPicker(false)}
              style={styles.iosPickerButton}
            >
              <Text style={[styles.iosPickerButtonText, styles.iosPickerConfirm]}>Done</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  dateButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    minHeight: 52,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  dateButtonError: {
    borderColor: '#ef4444',
    backgroundColor: '#FFF5F5',
    shadowColor: '#ef4444',
  },
  dateText: {
    fontSize: 16,
    color: '#1f2937',
  },
  placeholderText: {
    color: '#6b7280',
  },
  errorText: {
    fontSize: 14,
    color: '#ef4444',
    marginTop: 8,
    marginLeft: 4,
  },
  iosPickerStyle: {
    backgroundColor: 'white',
  },
  iosPickerContainer: {
    backgroundColor: 'white',
    borderRadius: 12,
    marginTop: 8,
  },
  iosPickerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  iosPickerButton: {
    padding: 8,
  },
  iosPickerButtonText: {
    fontSize: 16,
    color: '#6b7280',
  },
  iosPickerConfirm: {
    color: '#FF6B35',
    fontWeight: '600',
  },
});

export default DatePicker;