import React from 'react';
import { View, Text, StyleSheet, Image, StatusBar } from 'react-native'
import Logo from '../assets/svg/logo';

const Header = () => {
  return (
    
    <View style={styles.container}>
        <StatusBar backgroundColor="#1D1D27" />
        <View style={styles.topRow}>
        <Logo />
        </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    height: 60,
    width: "100%"
  },
  topRow: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    backgroundColor: '#1D1D27',
    alignItems: "center",
  },
});

export default Header;
