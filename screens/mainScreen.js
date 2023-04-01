import React, {useState} from 'react';
import { View, Text, StyleSheet, ImageBackground, Image, TouchableOpacity } from 'react-native';
import Button from '../components/Button';
import Header from '../components/Header';
import ScreenThree from "./ScreenThree"
import Quiz from './Quiz';
import GameBar from '../components/GameBar';
import { useFonts } from 'expo-font';
import { Svg, Rect } from 'react-native-svg';
import Button_Icon from "../components/Button_Icon"

const images = [
  require('../assets/image/stars/1.png'),
  require('../assets/image/stars/2.png'),
  require('../assets/image/stars/3.png'),
];

const names = [
  "Техника Безопасности",
  "Правила работы в компании",
  "Работа с внутренней системой"
]

const MainScreen = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showNewScreen, setShowNewScreen] = useState(false);
  const [fontsLoaded] = useFonts({
    'Montserrat_M': require("../assets/font/Montserrat-Medium.ttf"),
  });

  const handleLeftPress = () => {
    setCurrentImageIndex((prevIndex) => {
      const newIndex = prevIndex - 1;
      if (newIndex < 0) {
        return images.length - 1;
      }
      return newIndex;
    });
  };

  const handleRightPress = () => {
    setCurrentImageIndex((prevIndex) => {
      const newIndex = prevIndex + 1;
      if (newIndex >= images.length) {
        return 0;
      }
      return newIndex;
    });
  };

  return (
    <ImageBackground
    source={require('../assets/image/bg.png')} 
      style={styles.backgroundImage}>
    <View style={styles.container}>
      {showNewScreen ? (
        <Quiz />
      ) : (
      <View style={styles.content}>
        <Header />
        <GameBar />
        <Text style={styles.title}>Деревья навыков</Text>
        <View style={styles.stars}>
          <Button_Icon icon="arrow-back-ios" onPress={handleLeftPress} />
          <View style={styles.star}>
            <Image source={images[currentImageIndex]} style={{width: '80%', height: '80%'}}/>
            <Text style={styles.name_star}>{names[currentImageIndex]}</Text>
          </View>  
          <Button_Icon icon="arrow-forward-ios" onPress={handleRightPress}/>
        </View>
        <Text style={styles.title}>Изучай и получай баллы</Text>
        <TouchableOpacity style={styles.quiz} onPress={() => setShowNewScreen(true)}>
          <Text>123</Text>
        </TouchableOpacity>
      </View>
      )}
      </View>
      </ImageBackground>
  );
};

const styles = StyleSheet.create({
  backgroundImage: {
  flex: 1,
  resizeMode: "cover"
},
  container: {
    flex: 1,
    
  },
  content: {
    flex: 1,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontFamily:"Montserrat_M",
    marginBottom: 20,
    color:"white"
  },
  subtitle: {
    fontSize: 18,
    color: '#555',
  },
  stars:{
    flexDirection: "row",
    backgroundColor:"rgba(29, 29, 39, 0.5)",
    height:300,
    width:"90%",
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center'
  },
  star:{
    width:"70%",
    alignItems: 'center'
  },
  name_star:{
    fontFamily: "Montserrat_M",
    color: "white"
  },
  quiz:{
    color: "red",
    padding: 10,
    borderRadius: 5,
    marginVertical: 10,
    minWidth: 150,
  }
});

export default MainScreen;
