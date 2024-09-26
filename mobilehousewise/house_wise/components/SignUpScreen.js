import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image } from 'react-native';
import * as Google from 'expo-auth-session/providers/google';
import * as WebBrowser from 'expo-web-browser';
import { FontAwesome } from '@expo/vector-icons';

WebBrowser.maybeCompleteAuthSession();

export default function SignUpScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [request, response, promptAsync] = Google.useAuthRequest({
    expoClientId: 'YOUR_EXPO_CLIENT_ID',
    iosClientId: 'YOUR_IOS_CLIENT_ID',
    androidClientId: 'YOUR_ANDROID_CLIENT_ID',
    webClientId: 'YOUR_WEB_CLIENT_ID',
  });

  useEffect(() => {
    if (response?.type === 'success') {
      const { authentication } = response;
      // Handle the authentication and get the user info
    }
  }, [response]);

  return (
    <View style={styles.container}>
      {/* Logo */}
      <View style={styles.logoContainer}>
        <Image source={require('../assets/HWLogo.png')} style={styles.logo} />
      </View>

      {/* Sign Up Form */}
      <View style ={styles.formContainer}>
        <TextInput style={styles.input} placeholder="Username" value={name} onChangeText={setName}/>

        <TextInput style={styles.input} placeholder="Email" keyboardType="email-address" value={email} 
            onChangeText={setEmail}/>

        <TextInput style={styles.input} placeholder="Create Password" secureTextEntry value={password}
            onChangeText={setPassword}/>

        {/* Sign Up Button */}
        <TouchableOpacity style={styles.button}>
          <Text style= {styles.buttonText}>Sign Up</Text>
        </TouchableOpacity>

        {/* Terms & Privacy Policy */}
        <Text style={styles.termsText}>
          By Signing Up, you agree to our{' '}
          <Text style={styles.linkText}>Terms & Privacy Policy</Text>
        </Text>

      {/* Social Login Buttons */}
      <View style={styles.socialContainer}>
        <TouchableOpacity disabled={!request} onPress={() => promptAsync()}>
          <FontAwesome name="google" size={32} color="#DB4437" />
        </TouchableOpacity>
        <TouchableOpacity>
          <FontAwesome name="facebook" size={32} color="#3b5998" />
        </TouchableOpacity>
        <TouchableOpacity>
          <FontAwesome name="twitter" size={32} color="#1DA1F2" />
        </TouchableOpacity>
      </View>

      {/* Already have an account */}
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.loginText}>
          Already have an account? <Text style={styles.linkText}>Login</Text>
        </Text>
      </TouchableOpacity>
      </View>
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
  },

  formContainer: {
    width: '100%',
    height: '70%',
    backgroundColor: '#FCC205',
    padding: 30,
    borderRadius: 40,
    marginTop:20

  },

  logoContainer: {
    alignItems: 'center',
    marginBottom: 10,
    alignItems:'center',
    marginTop: 40

  },
  logo: {
    width: 200, // Adjust the width and height as per your icon's aspect ratio
    height: 200,
    resizeMode: 'contain',
  },

  input: {
    height: 50,
    backgroundColor: '#FCC205',
    borderRadius: 10,
    paddingHorizontal: 15,
    marginBottom: 10,
    borderBottomColor: '#000',
    borderBottomEndRadius: 10,
    borderBottomLeftRadius: 10,
    borderLeftColor: '#FCC205',
    borderBottomWidth: 2,
    color: '#000',
  },
  button: {
    backgroundColor: '#353336',
    borderRadius: 10,
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
    height: 50,
    width: 200,
    marginLeft: 50,
    borderColor: '#FCC205',
    borderWidth: 1,
    elevation: 10,
    marginTop: 20
  },
  buttonText: {
    color: '#FCC205',
    fontSize: 16,
    fontWeight: 'bold',
  },
  termsText: {
    textAlign: 'center',
    marginBottom: 20,
    marginTop: 20,
    color: '#000',
  },
  linkText: {
    fontWeight: 'bold',
  },
  socialContainer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    marginBottom: 30,
  },
  loginText: {
    textAlign: 'center',
    color: '#000',
  },
});
