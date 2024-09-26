import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native'; 

export default function HomeScreen() {
  const navigation = useNavigation(); // Access navigation
  const handlePress = () => {
    alert('Icon clicked!');
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Welcome!</Text>
        <Text style={styles.subtitleText}>Build Your Dream House, Where Every Brick Tells Your Story</Text>
      </View>

      <TouchableOpacity onPress={handlePress}>
        <Image  source={require('../assets/HWLogo.png')} style={styles.icon} />
      </TouchableOpacity>

      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.loginButton} onPress={() => navigation.navigate('Login')}>
          <Text style={styles.loginButtonText}>Log In</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.signUpButton} onPress={() => navigation.navigate('Sign up')}>
          <Text style={styles.loginButtonText}>Sign Up</Text>
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

  header: {
    marginBottom: 20,
    alignItems: 'center',
  },

  welcomeText: {
    fontSize: 35,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
  },

  subtitleText: {
    fontSize: 15,
    color: '#777',
  },

  icon: {
    width: 200, // Adjust the width and height as per your icon's aspect ratio
    height: 200,
    resizeMode: 'contain',
  },
  buttonRow: {
    flexDirection: 'row', // Puts the Log In and Sign Up buttons in a row
    justifyContent: 'space-between', // Adds space between the buttons
    alignItems: 'center',
    marginTop: 20,
    width: '80%',
  },
  loginButton: {
    backgroundColor: '#353336',
    borderRadius: 10,
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
    height: 45,
    width: '45%', // Adjust the button width to fit both in the row
    marginHorizontal: 5, // Adds a little space between the buttons
  },
  signUpButton: {
    backgroundColor: '#353336',
    borderRadius: 10,
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
    height: 45,
    width: '45%',
    marginHorizontal: 5,
  },
  loginButtonText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#FCC205',
  },
});
