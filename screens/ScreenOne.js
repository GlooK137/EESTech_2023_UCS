import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';

const SecondScreen = ({ navigation }) => {
  const goToFirstScreen = () => {
    navigation.navigate('FirstScreen');
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.triangleButton} onPress={goToFirstScreen}>
        <Text style={styles.buttonText}>Go to First Screen</Text>
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
  triangleButton: {
    width: 0,
    height: 0,
    borderLeftWidth: 50,
    borderRightWidth: 50,
    borderBottomWidth: 100,
    borderLeftColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: 'red',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default SecondScreen;
