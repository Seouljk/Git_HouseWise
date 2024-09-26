// ProfileScreen.js
import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { MaterialIcons, FontAwesome5, Ionicons } from '@expo/vector-icons'; // Icons used


export default function ProfileScreen({ navigation }) {
  return (
    <View style={styles.container}>
      {/* Header with Hamburger Icon */}
      <View style={styles.header}>
        {/* Hamburger Menu Icon */}
        <TouchableOpacity onPress={() => navigation.navigate('Dashboard')} style={styles.hamburger}>
          <Ionicons name="menu" size={28} color="#fff" />
        </TouchableOpacity>

        <Image
          source={{ uri: 'https://www.example.com/profile-image.png' }} // Placeholder image
          style={styles.profileImage}
        />
        <Text style={styles.profileName}>Marvin Margin Dala</Text>
      </View>

      {/* Options */}
      <View style={styles.optionContainer}>
        {/* History Icon */}
        <TouchableOpacity style={styles.option} onPress={() => navigation.navigate('Create')}>
          <FontAwesome5 name="history" size={24} color="black" />
          <Text style={styles.optionText}>History</Text>
        </TouchableOpacity>

        {/* Feedback Icon */}
        <TouchableOpacity style={styles.option} onPress={() => navigation.navigate('History')}>
          <MaterialIcons name="feedback" size={24} color="black" />
          <Text style={styles.optionText}>Feedback</Text>
        </TouchableOpacity>

        {/* Logout Option */}
        <TouchableOpacity style={[styles.option, styles.logout]}>
          <Ionicons name="log-out-outline" size={24} color="red" />
          <Text style={[styles.optionText, { color: 'red' }]}>Logout</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    backgroundColor: '#FCC205',
    alignItems: 'center',
    paddingVertical: 40,
    borderBottomLeftRadius: 40,
    borderBottomRightRadius: 40,
  },
  hamburger: {
    position: 'absolute',
    top: 40,
    left: 20,
    zIndex: 1,
  },
  profileImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#fff',
  },
  profileName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 10,
  },
  optionContainer: {
    marginTop: 30,
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f1f1f1',
  },
  optionText: {
    marginLeft: 20,
    fontSize: 16,
  },
  logout: {
    borderTopWidth: 1,
    borderTopColor: '#f1f1f1',
    marginTop: 20,
  },
});
