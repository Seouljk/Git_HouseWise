import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import HomeScreen from '../components/HomeScreen';
import LoginScreen from '../components/LoginScreen';
import SignUpScreen from '../components/SignUpScreen';
import BuildScreen from '../components/BuildScreen';
import OptionsBuild from '../components/OptionsBuild';
import ConcreteScreen from '../components/ConcreteScreen';
import WoodenScreen from '../components/WoodenScreen';
import ProfileScreen from '../components/ProfileScreen';
import Dashboard from '../components/Dashboard';
import CreateProjectScreen from '../components/CreateProjectScreen'
import ProjectHistoryScreen from '../components/ProjectHistoryScreen'


const Stack = createStackNavigator();


const AppNavigator = () => {
  return (
    <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }} initialRouteName='About'>
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Sign up" component={SignUpScreen} />
          <Stack.Screen name="Build" component={BuildScreen} />
          <Stack.Screen name="Options" component={OptionsBuild} />
          <Stack.Screen name="ConcreteScreen" component={ConcreteScreen} />
          <Stack.Screen name="WoodenScreen" component={WoodenScreen} />
          <Stack.Screen name="Profile" component={ProfileScreen} />
          <Stack.Screen name="Dashboard" component={Dashboard} />
          <Stack.Screen name="Create" component={CreateProjectScreen} />
          <Stack.Screen name="History" component={ProjectHistoryScreen} />
        </Stack.Navigator>

    </NavigationContainer>
  );
};

export default AppNavigator;
