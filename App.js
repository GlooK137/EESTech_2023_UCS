import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import ScreenOne from './screens/ScreenOne';
import ScreenTwo from './screens/ScreenTwo';
import ScreenThree from './screens/ScreenThree';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ color, size }) => {
            let iconName;

            if (route.name === 'ScreenOne') {
              iconName = 'home-outline';
            } else if (route.name === 'ScreenTwo') {
              iconName = 'chatbubbles-outline';
            } else if (route.name === 'ScreenThree') {
              iconName = 'person-outline';
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
        })}
        tabBarOptions={{
          activeTintColor: 'blue',
          inactiveTintColor: 'gray',
        }}
      >
        <Tab.Screen name="ScreenOne" component={ScreenOne} />
        <Tab.Screen name="ScreenTwo" component={ScreenTwo} />
        <Tab.Screen name="ScreenThree" component={ScreenThree} />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

export default App;
