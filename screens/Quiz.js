import React, {useState} from 'react';
import { View, Text, StyleSheet, StatusBar } from 'react-native';
import Button from '../components/PrequizButton';
import Header from '../components/Header';

const Quiz = () => {
    const [showNewScreen, setShowNewScreen] = useState(false);
    return(
    <View style={styles.content}>
        <View>
            <Button color={"#F00"} onPress={() => console.log(13)}/>
        </View>
      <Button color={"#F00"} />
      <Button color={"#0F0"} />
      <Button color={"#00F"} />
    </View>
    )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    //justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 18,
    color: '#555',
  },
});

export default Quiz;
