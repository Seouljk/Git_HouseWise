import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native'; 

export default function App() {
  const navigation = useNavigation();
  const handlePressConcrete = () => {
    alert('wapa nahuman');
  };

  const handlePressWooden = () => {
    alert('Wooden icon clicked!');
  };

  return (
    <View style={styles.container}>
      {/* Wrap the two icons in a row */}
      <View style={styles.row}>
        <TouchableOpacity style={styles.iconContainer} onPress={() => navigation.navigate('ConcreteScreen')}>
          <Image source={require('../assets/concreteicon.png')} style={styles.icon} />
          <Text style={styles.iconText}>Concrete</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.iconContainer} onPress={() => navigation.navigate('WoodenScreen')}>
          <Image source={require('../assets/woodenicon.png')} style={styles.icon} />
          <Text style={styles.iconText}>Wooden</Text>
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
  },
  row: {
    flexDirection: 'row', // Puts the two icons in a row
    justifyContent: 'space-between', // Space between the two icons
    alignItems: 'center',
  },
  iconContainer: {
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 20, // Adds space between the two icons
    elevation: 5, // Shadow for Android
    borderRadius: 15,
    borderColor:'#FCC205',
    borderWidth: 3
  },
  icon: {
    width: 100, // Adjust the width and height as per your icon's aspect ratio
    height: 100,
    resizeMode: 'contain',
  },
  iconText: {
    marginTop: 1,
    fontSize: 18,
    fontWeight: 'bold',
  },
});
