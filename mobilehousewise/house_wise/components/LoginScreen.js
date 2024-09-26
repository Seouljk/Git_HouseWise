import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useNavigation } from '@react-navigation/native'; // Import useNavigation hook
import * as Google from 'expo-auth-session/providers/google';
import * as WebBrowser from 'expo-web-browser';
import { FontAwesome } from '@expo/vector-icons';
import axios from 'axios';

const handleLogin = async () => {
  try {
    const response = await axios.post('http://<your_django_backend_url>/auth/login/', {
      username: email,
      password: password,
    });
    if (response.status === 200) {
      useNavigation.navigate('Build'); // navigate to profile page upon success
    }
  } catch (error) {
    console.error('Login failed', error);
  }
};

const handleSignUp = async () => {
  try {
    const response = await axios.post('http://<your_django_backend_url>/auth/signup/', {
      username: email,
      password: password,
    });
    if (response.status === 201) {
      useNavigation.navigate('Login'); // navigate to login page after signup
    }
  } catch (error) {
    console.error('Signup failed', error);
  }
};

WebBrowser.maybeCompleteAuthSession();

const LoginScreen = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigation = useNavigation(); // Access navigation

  const [request, response, promptAsync] = Google.useAuthRequest({
    expoClientId: 'YOUR_EXPO_CLIENT_ID',
    iosClientId: 'YOUR_IOS_CLIENT_ID',
    androidClientId: 'YOUR_ANDROID_CLIENT_ID',
    webClientId: 'YOUR_WEB_CLIENT_ID',
  });

  const handleLogin = () => {
    console.log('Login pressed');
  };

  // Handle Google Authentication response
  useEffect(() => {
    if (response?.type === 'success') {
      const { authentication } = response;

      if (authentication) {
        // Here, authentication will have access_token
        console.log('Access Token:', authentication.accessToken);

        // You can now use this token to authenticate with your backend
        // or navigate to a new screen, etc.
        // Example: navigation.navigate('Home');

        // Optionally, you can store the token locally
        // AsyncStorage.setItem('token', authentication.accessToken);
      }
    }
  }, [response]);

  return (
    <View style={styles.container}>
      {/* Illustration */}
      <Image source={require('../assets/HWLogo.png')}  style={styles.illustration}/>
      
      {/* Form Section */}
      <View style={styles.formContainer}>
        <TextInput style={styles.input} placeholder="youremail@gmail.com" placeholderTextColor="#000"
          value={email} onChangeText={setEmail} keyboardType="email-address"/>

        <TextInput style={styles.input} placeholder="••••••••" placeholderTextColor="#000"
          value={password} onChangeText={setPassword} secureTextEntry />

        <TouchableOpacity onPress={() => console.log('Forgot Password? pressed')}>
          <Text style={styles.forgotPasswordText}>Forgot Password?</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.loginButton} onPress = {() => navigation.navigate ('Profile')}>
          <Text style={styles.loginButtonText}>Log In</Text>
        </TouchableOpacity>

        {/* or Login with Google */}
        <View style={styles.googleButtonWrapper}>
            <View style={styles.line} />
              <Text style={styles.googleButtonText}>Login with Google</Text>
            <View style={styles.line} />
        </View>

        {/* Google button */}
        <View style={styles.socialContainer}>
          <TouchableOpacity style={styles.googleButton} disabled={!request} onPress={() => promptAsync()}>
            <View style={styles.googleButtonContent}>
              <FontAwesome name="google" size={32} color="#DB4437" style={styles.googleIcon} />
            </View>
          </TouchableOpacity>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>Don't have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Sign up')}>
            <Text style={styles.registerText}>Register</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },

  illustration: {
    width: 200,
    height: 200,
    marginBottom: 20,
    marginTop: 100,
    resizeMode: 'contain',
  },

  formContainer: {
    width: '99.7%',
    height: '80%',
    backgroundColor: '#FCC205',
    padding: 30,
    borderRadius: 40

  },

  input: {
    height: 50,
    backgroundColor: '#FCC205',
    borderRadius: 10,
    paddingHorizontal: 15,
    marginBottom: 15,
    borderBottomColor: '#000',
    borderBottomEndRadius: 0,
    borderBottomLeftRadius: 10,
    borderLeftColor: '#FCC205',
    borderBottomWidth: 2,
    color: '#000',
    marginTop: 30
  },

  forgotPasswordText: {
    alignSelf: 'flex-end',
    color: '#000',
    marginBottom: 30,
  },

  loginButton: {
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
    elevation: 10
  },

  loginButtonText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#FCC205',
  },

  googleButtonWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%', // Adjust this as necessary
    justifyContent: 'center'
  
  },

  googleButtonText: {
    color: '#353336',
    fontSize: 11,
    fontWeight: 'bold',
    marginHorizontal: 10, // Space between text and lines
    marginTop: 20,
  },

  line: {
    flex: 1,
    height: 1,
    backgroundColor: '#000', // Color of the line
    marginHorizontal: 1, // Add some space between line and text
    marginTop: 20,
  },

  socialContainer: {
    marginLeft: 10,
    marginTop: 25,
    color: '#DB4437',
    fontWeight: 'bold',
    fontSize: 11,
    alignItems: 'center',
  },

  googleButton: {
    borderColor: '#FCC205',
    borderWidth: 1,
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 30,
    width: 200,
    alignItems:'center',
    backgroundColor: '#353336',
    elevation: 10
  },

  googleButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  googleIcon: {
    marginRight: 10,
  },

  footer: {
    flexDirection: 'row',
    marginTop: 20,
  },

  footerText: {
    color: '#000',
    alignItems: 'center',
    marginTop: 10,
    marginLeft: 65,
  },

  registerText: {
    marginLeft: 10,
    marginTop: 10,
    color: '#000',
    fontWeight: 'bold',
    fontSize: 15,
  },
});

export default LoginScreen;
