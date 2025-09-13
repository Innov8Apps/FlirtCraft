import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions, ScrollView, NativeSyntheticEvent, NativeScrollEvent } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Fun and sassy age-specific messages
const AGE_MESSAGES: Record<number, string> = {
  // Under 18 messages (sassy but clear about age requirement)
  13: "13 and full of teenage energy! But FlirtCraft adventures start at 18 - patience, young padawan! 🌟",
  14: "14 and fabulous! Keep growing that confidence - FlirtCraft will be here when you're ready! ✨",
  15: "15 and fierce! Just a few more years until you can master the art of conversation with us! 💫",
  16: "Sweet 16 and full of dreams! But you'll need to wait a bit more for FlirtCraft adventures! 💫",
  17: "17 and almost there! One more year until you can join the conversation mastery club! 🌟",

  // 18-30 specific messages
  18: "Just turned 18? Welcome to adulthood! Time to practice those conversation skills! 🎉",
  19: "19 and feeling fine! Ready to charm your way through conversations? 💫",
  20: "Twenty and plenty ready for some flirty fun! Let's get those skills polished! ✨",
  21: "21 - now you're legally fabulous everywhere! Time to level up your charm game! 🥂",
  22: "22 and still got it! Ready to turn heads with your conversation skills? 😏",
  23: "23 - the perfect age for perfecting your flirt game! Let's make it happen! 💃",
  24: "24 and absolutely radiant! Time to practice those smooth moves! 🌟",
  25: "Quarter-century of awesomeness! Ready to add some serious charm to that resume? 💼✨",
  26: "26 and thriving! Let's make every conversation count, gorgeous! 💫",
  27: "27 - prime time for prime conversations! You've got this, superstar! ⭐",
  28: "28 and feeling great! Ready to master the art of enchanting conversations? 🎭",
  29: "29 and fine as wine! Time to polish those conversation skills to perfection! 🍷",
  30: "Dirty thirty and absolutely flirty! Welcome to your confidence era! 🔥"
};

// Age range messages for 31+ (randomized within each 5-year range)
const AGE_RANGE_MESSAGES: Record<string, string[]> = {
  "31-35": [
    "Early thirties and absolutely thriving! Time to show them how experience meets charm! 🔥",
    "31-35 and in your prime! Ready to turn conversations into pure magic? ✨",
    "Thirty-something sophistication with a playful twist! Let's master those skills! 💫",
    "Early thirties confidence is unmatched! Time to practice that irresistible charm! 👑",
    "Peak millennial energy! Ready to blend wisdom with flirtation? 🌟"
  ],
  "36-40": [
    "Late thirties and absolutely glowing! Time to show them what real charm looks like! ✨",
    "36-40 and fabulous! Ready to turn every conversation into an art form? 🎨",
    "Late thirties wisdom meets undeniable charm! Let's perfect those skills! 💎",
    "Almost forty and absolutely magnetic! Time to practice that sophisticated flirt game! 🔥",
    "Peak confidence years! Ready to blend experience with enchantment? 👑"
  ],
  "41-45": [
    "Early forties and absolutely radiant! Time to show them how it's really done! 🌟",
    "41-45 and in your power era! Ready to master the art of sophisticated conversation? 💫",
    "Forty-something fabulous! Let's combine wisdom with irresistible charm! ✨",
    "Early forties confidence is everything! Time to practice those expert-level skills! 👑",
    "Peak life experience meets peak charm! Ready to enchant with every word? 🔥"
  ],
  "46-50": [
    "Mid-forties and absolutely stunning! Time to demonstrate true conversational mastery! 💎",
    "46-50 and in your prime! Ready to turn charm into a fine art? 🎨",
    "Forty-something sophistication at its finest! Let's perfect those legendary skills! ✨",
    "Mid-forties magnetic energy! Time to show them what real experience brings! 🌟",
    "Peak wisdom meets peak allure! Ready to enchant with seasoned charm? 👑"
  ],
  "51+": [
    "Fifty-plus and absolutely legendary! Time to show them what true mastery looks like! 👑",
    "50+ and in your golden era! Ready to turn every conversation into pure gold? ✨",
    "Mature magnificence at its peak! Let's demonstrate what real charm achieves! 💎",
    "Fifty-something fabulous! Time to practice those expert-level enchantment skills! 🌟",
    "Ultimate life experience meets ultimate charm! Ready to be absolutely irresistible? 🔥"
  ]
};

interface WheelDatePickerProps {
  value?: Date;
  onChange: (date: Date) => void;
  onYearAdjusted?: () => void;
  placeholder?: string;
  minimumDate?: Date;
  maximumDate?: Date;
  error?: string;
}

const { width: screenWidth } = Dimensions.get('window');
const ITEM_HEIGHT = 40;
const CONTAINER_HEIGHT = 120;

// Function to get age-specific messages
const getAgeMessage = (age: number): string => {
  // For specific ages with individual messages (13, 14, 15, 16, 17, 18-30)
  if (AGE_MESSAGES[age]) {
    return AGE_MESSAGES[age];
  }

  // For age ranges 31+, use randomized messages within the range
  if (age >= 31) {
    let rangeKey: string;

    if (age >= 31 && age <= 35) {
      rangeKey = "31-35";
    } else if (age >= 36 && age <= 40) {
      rangeKey = "36-40";
    } else if (age >= 41 && age <= 45) {
      rangeKey = "41-45";
    } else if (age >= 46 && age <= 50) {
      rangeKey = "46-50";
    } else {
      rangeKey = "51+";
    }

    const messages = AGE_RANGE_MESSAGES[rangeKey];
    const randomIndex = Math.floor(Math.random() * messages.length);
    return messages[randomIndex];
  }

  // Fallback for ages not covered (under 13, etc.)
  return "Please verify you are 18 or older to continue.";
};

export const WheelDatePicker: React.FC<WheelDatePickerProps> = ({
  value,
  onChange,
  onYearAdjusted,
  placeholder = "Select your birth date",
  minimumDate,
  maximumDate,
  error,
}) => {
  // Initialize with proper values or defaults
  const initialDay = value?.getDate() || 15;
  const initialMonth = value ? value.getMonth() + 1 : 6; // June (middle month)
  const initialYear = value?.getFullYear() || 2008;

  const [selectedDay, setSelectedDay] = useState<number>(initialDay);
  const [selectedMonth, setSelectedMonth] = useState<number>(initialMonth);
  const [selectedYear, setSelectedYear] = useState<number>(initialYear);
  

  const dayScrollRef = useRef<ScrollView>(null);
  const monthScrollRef = useRef<ScrollView>(null);
  const yearScrollRef = useRef<ScrollView>(null);

  // Generate years array (100 years ago to 2025)
  const currentYear = new Date().getFullYear();
  const minYear = currentYear - 100;
  const maxYear = 2025;
  
  const years = Array.from({ length: maxYear - minYear + 1 }, (_, i) => maxYear - i);
  
  // Month names
  const months = [
    { label: 'Jan', value: 1 },
    { label: 'Feb', value: 2 },
    { label: 'Mar', value: 3 },
    { label: 'Apr', value: 4 },
    { label: 'May', value: 5 },
    { label: 'Jun', value: 6 },
    { label: 'Jul', value: 7 },
    { label: 'Aug', value: 8 },
    { label: 'Sep', value: 9 },
    { label: 'Oct', value: 10 },
    { label: 'Nov', value: 11 },
    { label: 'Dec', value: 12 },
  ];

  // Get days in month
  const getDaysInMonth = (month: number, year: number) => {
    return new Date(year, month, 0).getDate();
  };

  const daysInMonth = getDaysInMonth(selectedMonth, selectedYear);
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  // Calculate which item is at the center of the selection box
  const getCenterIndex = (scrollOffset: number) => {
    // With the new padding structure, the first item center is at (CONTAINER_HEIGHT / 2)
    // Each subsequent item is ITEM_HEIGHT apart
    // So the index is simply scrollOffset / ITEM_HEIGHT (rounded to nearest)
    return Math.round(scrollOffset / ITEM_HEIGHT);
  };

  // Simple scroll handlers - only update selection, no auto-snapping
  const handleDayScroll = (event: NativeSyntheticEvent<NativeScrollEvent>) => {
    const offsetY = event.nativeEvent.contentOffset.y;
    const centerIndex = getCenterIndex(offsetY);
    const newDay = Math.min(Math.max(1, centerIndex + 1), daysInMonth);
    
    if (newDay !== selectedDay && newDay >= 1 && newDay <= daysInMonth) {
      setSelectedDay(newDay);
    }
  };

  const handleMonthScroll = (event: NativeSyntheticEvent<NativeScrollEvent>) => {
    const offsetY = event.nativeEvent.contentOffset.y;
    const centerIndex = getCenterIndex(offsetY);
    const newMonth = Math.min(Math.max(1, centerIndex + 1), 12);
    
    if (newMonth !== selectedMonth && newMonth >= 1 && newMonth <= 12) {
      setSelectedMonth(newMonth);
    }
  };

  const handleYearScroll = (event: NativeSyntheticEvent<NativeScrollEvent>) => {
    const offsetY = event.nativeEvent.contentOffset.y;
    const centerIndex = getCenterIndex(offsetY);
    const newYear = years[Math.min(Math.max(0, centerIndex), years.length - 1)];

    if (newYear && newYear !== selectedYear) {
      setSelectedYear(newYear);
      // Notify parent component that year has been adjusted
      if (onYearAdjusted) {
        onYearAdjusted();
      }
    }
  };

  // Scroll to selected values - position so the selected item is perfectly centered
  const scrollToSelected = () => {
    // With the new padding structure, items snap perfectly at multiples of ITEM_HEIGHT
    // To center item N, scroll to position (N * ITEM_HEIGHT)
    
    // Scroll day
    const dayIndex = selectedDay - 1;
    dayScrollRef.current?.scrollTo({ 
      y: dayIndex * ITEM_HEIGHT, 
      animated: false 
    });

    // Scroll month
    const monthIndex = selectedMonth - 1;
    monthScrollRef.current?.scrollTo({ 
      y: monthIndex * ITEM_HEIGHT, 
      animated: false 
    });

    // Scroll year
    const yearIndex = years.indexOf(selectedYear);
    if (yearIndex !== -1) {
      yearScrollRef.current?.scrollTo({ 
        y: yearIndex * ITEM_HEIGHT, 
        animated: false 
      });
    }
  };

  // Update date when any wheel changes
  useEffect(() => {
    // Adjust day if it exceeds the days in the selected month
    const maxDay = getDaysInMonth(selectedMonth, selectedYear);
    const adjustedDay = Math.min(selectedDay, maxDay);
    
    if (adjustedDay !== selectedDay) {
      setSelectedDay(adjustedDay);
      // Re-scroll day picker if day was adjusted
      setTimeout(() => {
        const dayIndex = adjustedDay - 1;
        dayScrollRef.current?.scrollTo({ 
          y: dayIndex * ITEM_HEIGHT, 
          animated: true 
        });
      }, 100);
    }

    const newDate = new Date(selectedYear, selectedMonth - 1, adjustedDay);
    onChange(newDate);
  }, [selectedDay, selectedMonth, selectedYear]);

  // Initialize scroll positions - wait for component to fully mount
  useEffect(() => {
    // Multiple attempts to ensure proper positioning
    const timers = [
      setTimeout(scrollToSelected, 100),
      setTimeout(scrollToSelected, 300),
      setTimeout(scrollToSelected, 500),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  // Update state when value prop changes from outside
  useEffect(() => {
    if (value) {
      const newDay = value.getDate();
      const newMonth = value.getMonth() + 1;
      const newYear = value.getFullYear();
      
      setSelectedDay(newDay);
      setSelectedMonth(newMonth);
      setSelectedYear(newYear);
      
      const timer = setTimeout(scrollToSelected, 100);
      return () => clearTimeout(timer);
    }
  }, [value]);

  // Format display date
  const formatDisplayDate = () => {
    if (!value) return placeholder;
    
    const day = value.getDate();
    const monthName = months[value.getMonth()].label;
    const year = value.getFullYear();
    
    return `${day} ${monthName} ${year}`;
  };

  // Calculate age for display
  const calculateAge = (date: Date): number => {
    const today = new Date();
    const birth = new Date(date);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    
    return age;
  };

  const age = value ? calculateAge(value) : null;
  const isEligible = age !== null && age >= 18;

  return (
    <View style={styles.container}>
      {/* Display selected date */}
      <View style={[styles.dateDisplay, error && styles.dateDisplayError]}>
        <Ionicons 
          name="calendar" 
          size={20} 
          color="#FA7215" 
          style={styles.calendarIcon}
        />
        <Text style={styles.dateText}>
          {formatDisplayDate()}
        </Text>
      </View>

      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}

      {/* Wheel selectors */}
      <View style={styles.wheelContainer}>
        {/* Column headers */}
        <View style={styles.headerRow}>
          <Text style={styles.columnHeader}>DAY</Text>
          <Text style={styles.columnHeader}>MONTH</Text>
          <Text style={styles.columnHeader}>YEAR</Text>
        </View>

        {/* Scrollable wheels */}
        <View style={styles.pickersRow}>
          {/* Day Wheel */}
          <View style={styles.pickerContainer}>
            <ScrollView
              ref={dayScrollRef}
              style={styles.scrollWheel}
              contentContainerStyle={styles.scrollContent}
              showsVerticalScrollIndicator={false}
              snapToInterval={ITEM_HEIGHT}
              decelerationRate="fast"
              onMomentumScrollEnd={handleDayScroll}
              onScrollEndDrag={handleDayScroll}
              nestedScrollEnabled={true}
              bounces={false}
            >
              {days.map((day, index) => (
                <View key={day} style={styles.wheelItem}>
                  <Text
                    style={[
                      styles.wheelItemText,
                      selectedDay === day && styles.wheelItemTextSelected,
                    ]}
                  >
                    {day}
                  </Text>
                </View>
              ))}
            </ScrollView>
            <View style={styles.selectionOverlay} />
          </View>

          {/* Month Wheel */}
          <View style={styles.pickerContainer}>
            <ScrollView
              ref={monthScrollRef}
              style={styles.scrollWheel}
              contentContainerStyle={styles.scrollContent}
              showsVerticalScrollIndicator={false}
              snapToInterval={ITEM_HEIGHT}
              decelerationRate="fast"
              onMomentumScrollEnd={handleMonthScroll}
              onScrollEndDrag={handleMonthScroll}
              nestedScrollEnabled={true}
              bounces={false}
            >
              {months.map((month, index) => (
                <View key={month.value} style={styles.wheelItem}>
                  <Text
                    style={[
                      styles.wheelItemText,
                      selectedMonth === month.value && styles.wheelItemTextSelected,
                    ]}
                  >
                    {month.label}
                  </Text>
                </View>
              ))}
            </ScrollView>
            <View style={styles.selectionOverlay} />
          </View>

          {/* Year Wheel */}
          <View style={styles.pickerContainer}>
            <ScrollView
              ref={yearScrollRef}
              style={styles.scrollWheel}
              contentContainerStyle={styles.scrollContent}
              showsVerticalScrollIndicator={false}
              snapToInterval={ITEM_HEIGHT}
              decelerationRate="fast"
              onMomentumScrollEnd={handleYearScroll}
              onScrollEndDrag={handleYearScroll}
              nestedScrollEnabled={true}
              bounces={false}
            >
              {years.map((year, index) => (
                <View key={year} style={styles.wheelItem}>
                  <Text
                    style={[
                      styles.wheelItemText,
                      selectedYear === year && styles.wheelItemTextSelected,
                    ]}
                  >
                    {year}
                  </Text>
                </View>
              ))}
            </ScrollView>
            <View style={styles.selectionOverlay} />
          </View>
        </View>
      </View>


    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  dateDisplay: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#F3F4F6',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    marginBottom: 16,
    shadowColor: '#FF8C42',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  dateDisplayError: {
    borderColor: '#ef4444',
    backgroundColor: '#FFF5F5',
    shadowColor: '#ef4444',
  },
  calendarIcon: {
    marginRight: 12,
  },
  dateText: {
    fontSize: 16,
    color: '#FA7215',
    fontWeight: '500',
  },
  errorText: {
    fontSize: 14,
    color: '#ef4444',
    marginTop: -20,
    marginBottom: 20,
    marginLeft: 4,
  },
  wheelContainer: {
    backgroundColor: 'transparent',
    padding: 16,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 18,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 12,
  },
  columnHeader: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6b7280',
    letterSpacing: 0.5,
    textAlign: 'center',
    flex: 1,
  },
  pickersRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: CONTAINER_HEIGHT,
  },
  pickerContainer: {
    flex: 1,
    backgroundColor: '#FFF5F0',
    borderRadius: 8,
    marginHorizontal: 4,
    overflow: 'hidden',
    position: 'relative',
    height: CONTAINER_HEIGHT,
  },
  scrollWheel: {
    flex: 1,
  },
  scrollContent: {
    paddingTop: CONTAINER_HEIGHT / 2 - ITEM_HEIGHT / 2,
    paddingBottom: CONTAINER_HEIGHT / 2 - ITEM_HEIGHT / 2,
  },
  wheelItem: {
    height: ITEM_HEIGHT,
    justifyContent: 'center',
    alignItems: 'center',
  },
  wheelItemText: {
    fontSize: 16,
    color: 'rgba(156, 163, 175, 0.4)',
    fontWeight: '400',
    textAlign: 'center',
    opacity: 0.6,
  },
  wheelItemTextSelected: {
    fontSize: 18,
    color: '#FA7215',
    fontWeight: '600',
    opacity: 1,
  },
  selectionOverlay: {
    position: 'absolute',
    top: '50%',
    left: 0,
    right: 0,
    height: ITEM_HEIGHT,
    marginTop: -ITEM_HEIGHT / 2,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: '#FA7215',
    backgroundColor: 'rgba(255, 107, 53, 0.1)',
    pointerEvents: 'none',
  },
});

export default WheelDatePicker;