import React, { useMemo } from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import Animated, { useSharedValue, useDerivedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';

const TAB_BAR_HEIGHT = 50;

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    height: TAB_BAR_HEIGHT,
    backgroundColor: 'rgba(0,0,0,0)',
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: '#ddd',
    paddingHorizontal: 10,
    paddingBottom: 5,
  },
  tab: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  icon: {
    marginBottom: 2,
  },
  label: {
    fontSize: 10,
    fontWeight: 'bold',
    textTransform: 'uppercase',
  },
});

const BottomTabBar = ({ state, descriptors, navigation }) => {
  const insets = useSafeAreaInsets();
  const { width: screenWidth } = useWindowDimensions();
  const tabWidth = useMemo(() => screenWidth / state.routes.length, [screenWidth, state.routes.length]);

  const selectedTab = useDerivedValue(() => {
    return state.routes.findIndex(route => route.name === state.routeNames[state.index]);
  });

  const left = useSharedValue(0);
  const handlePress = index => {
    left.value = withTiming(index * tabWidth);
    navigation.navigate(state.routeNames[index]);
  };

  const tabStyles = useAnimatedStyle(() => {
    return {
      left: left.value,
      width: tabWidth,
    };
  });

  return (
    <View style={[styles.container, { paddingBottom: insets.bottom }]}>
      {state.routes.map((route, index) => {
        const { options } = descriptors[route.key];
        const label = options.tabBarLabel || options.title || route.name;
        const isFocused = selectedTab.value === index;

        const icon = options.tabBarIcon && (
          <Ionicons name={options.tabBarIcon} size={20} color={isFocused ? '#00bcd4' : '#9e9e9e'} style={styles.icon} />
        );

        return (
          <TouchableOpacity key={route.key} style={styles.tab} onPress={() => handlePress(index)}>
            <View>
              {icon}
              <Animated.Text style={[styles.label, isFocused && { color: '#00bcd4' }]}>{label}</Animated.Text>
            </View>
          </TouchableOpacity>
        );
      })}
      <Animated.View style={[tabStyles, { height: 2, position: 'absolute', bottom: 0 }]} />
    </View>
  );
};

export default BottomTabBar;
