import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native'; 

export default function App() {
  const navigation = useNavigation(); // Access navigation
  const handlePress = () => {
    alert('Icon clicked!');
  };

  return (
    <View style={styles.container}>

      <View  style = {styles.container2}>

      <TouchableOpacity style={styles.iconContainer} onPress={() => navigation.navigate('Options')} >
        <Image  source={require('../assets/houseiconn.png')} style={styles.icon} />
        <Text style={styles.iconText}>Build</Text>
      </TouchableOpacity>

      </View>

    </View>
    
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FCC205', // Yellow background
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 30,
  },

  startText:{
    fontSize : 20,
    fontWeight: 'bold'
  },
  container2: {
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    height: '80%',
    borderRadius: 40,
    alignContent: 'center',
    marginTop:-450
  },

  iconContainer: {
    backgroundColor: '#FCC205',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 400,
    borderColor:'#FCC205',
    borderWidth: 3,
    borderRadius: 15,
    elevation: 20
  },

  icon: {
    width: 100, // Adjust the width and height as per your icon's aspect ratio
    height: 100,
    resizeMode: 'contain',

  },

  iconText: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: 'bold',
  },
});
;