import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';

const FirstScreen = ({ navigation }) => {
  const goToSecondScreen = () => {
    navigation.navigate('SecondScreen');
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.squareButton} onPress={goToSecondScreen}>
        <Text style={styles.buttonText}>Go to Second Screen</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  squareButton: {
    backgroundColor: 'blue',
    width: 150,
    height: 150,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default FirstScreen;
