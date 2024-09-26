import { createDrawerNavigator } from '@react-navigation/drawer';  // Correct import for the drawer
import { NavigationContainer } from '@react-navigation/native';
import React from 'react';

import HomeScreen from '../components/HomeScreen';
import LoginScreen from '../components/LoginScreen';
import SignUpScreen from '../components/SignUpScreen';
import BuildScreen from '../components/BuildScreen';
import OptionsBuild from '../components/OptionsBuild';
import ConcreteScreen from '../components/ConcreteScreen';
import WoodenScreen from '../components/WoodenScreen';
import ProfileScreen from '../components/ProfileScreen';
import Dashboard from '../components/Dashboard';
import CreateProjectScreen from '../components/CreateProjectScreen';
import ProjectHistoryScreen from '../components/ProjectHistoryScreen';  // Fixed typo here too

const Drawer = createDrawerNavigator();  // Create the drawer navigator

// Drawer Navigator
const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Drawer.Navigator initialRouteName="HomeDrawer">
        {/* Drawer items */}
        <Drawer.Screen name="HomeDrawer" component={HomeScreen} options={{ title: 'Home' }} />
        <Drawer.Screen name="ProfileDrawer" component={ProfileScreen} options={{ title: 'Profile' }} />
        <Drawer.Screen name="DashboardDrawer" component={Dashboard} options={{ title: 'Dashboard' }} />
        <Drawer.Screen name="ProjectHistoryDrawer" component={ProjectHistoryScreen} options={{ title: 'Project History' }} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
