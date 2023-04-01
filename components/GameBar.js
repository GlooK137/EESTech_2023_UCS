import React from 'react';
import { View, Text, StyleSheet, Image, StatusBar } from 'react-native';
import { Avatar, ProgressBar, Colors } from 'react-native-paper';
import { Svg, Circle, Text as SvgText, Rect, LinearGradient, Stop } from 'react-native-svg';

const GameBar = () => {
  return (
    
    <View style={styles.container}>
        <View style={styles.content}>
            <View style={styles.avatar}>
            <Svg height="70" width="70">
                <Circle cx="35" cy="25" r="25" fill="blue" />
                <SvgText x="15" y="65" fill="#fff" fontSize="15">Юрий</SvgText>
            </Svg>
        </View>
        <View style={styles.progress}>
            <Svg height="70" width="200">
            <LinearGradient id="gradient" x1="0" y1="0" x2="100%" y2="0">
                <Stop offset="0" stopColor="#E31E24" />
                <Stop offset="1" stopColor="#28619B" />
            </LinearGradient>
                <Rect x = {0} y={15} height="20" width={200} rx="10" ry="10" fill="#D9D9D9" />
                <Rect x = {0} y={15} height="20" width={200 * 0.7} rx="8" ry="8" fill="url(#gradient)" />
                <SvgText x="70" y="65" fill="#fff" fontSize="15">Прогресс</SvgText>
            </Svg>
        </View>
        <View style={styles.lvl}>
            <Svg height="70" width="70">
                <SvgText x="25" y="45" fill="#fff" fontSize="30">6</SvgText>
                <SvgText x="5" y="65" fill="#fff" fontSize="15">уровень</SvgText>
            </Svg>
        </View>
        </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    height: 100,
    width: "100%"
  },
  content: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: '#1D1D27',
    alignItems: "center",
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  text:{
    paddingRight:10
  },
  avatar:{
    paddingLeft:20
  },
  progress:{
    paddingLeft:20
  }
});

export default GameBar;
