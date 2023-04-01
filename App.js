import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import MainScreen from './screens/mainScreen';
import EventsListScreen from './screens/EventsListScreen';
import ScreenThree from './screens/ScreenThree';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          headerShown: false,
          tabBarIcon: ({ color, size }) => {
            let iconName;

            if (route.name === 'mainScreen') {
              iconName = 'ios-home';
            } else if (route.name === 'eventsList') {
              iconName = 'ios-calendar';
            } else if (route.name === 'leaderBoard') {
              iconName = 'ios-people';
            } else if (route.name === 'personalCabinet') {
              iconName = 'ios-person';
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
        })}
        tabBarOptions={{
          activeTintColor: '#28619B',
          inactiveTintColor: 'gray',
          showLabel: false,
          activeBackgroundColor: '#1D1D27',
          inactiveBackgroundColor: '#1D1D27',
        }}
      >
        <Tab.Screen name="mainScreen" component={MainScreen} />
        <Tab.Screen name="eventsList" component={EventsListScreen} />
        <Tab.Screen name="leaderBoard" component={ScreenThree} />
        <Tab.Screen name="personalCabinet" component={ScreenThree} />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

export default App;
