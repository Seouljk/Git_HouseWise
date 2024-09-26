import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native'; 
import { ScrollView } from 'react-native-gesture-handler';

export default function ConcreteScreen() {
  const navigation = useNavigation(); // Access navigation
  const handlePress = () => {
    alert('Wapa nahuman!');
  };

  return (
    <View style={styles.container}>

        <View style ={styles.concreteiconContainer}>
            <Image  source={require('../assets/concreteicon.png')} style ={styles.concreteicon}/>
            <Text style={styles.concreteiconText}>Concrete</Text>
        </View>


    
      <ScrollView style = {styles.formContainer}>
        <View style = {styles.row} >
        <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/Dimensionicon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText}>Dimension</Text>
            </TouchableOpacity>

            <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/footingicon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText}>Footing</Text>
            </TouchableOpacity>
        </View>  

        <View  style = {styles.row}>
        <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/Wallicon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText} >Wall</Text>
            </TouchableOpacity>

            <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/beamicon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText} >Beam</Text>
            </TouchableOpacity>
        </View>

        <View  style = {styles.row}>
        <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/Columnicon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText} >Column</Text>
            </TouchableOpacity>

            <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/Flooring.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText} >Flooring</Text>
            </TouchableOpacity>
        </View>


        <View  style = {styles.row}>
        <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/rooficon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText} >Roofing</Text>
            </TouchableOpacity>

            <TouchableOpacity style = {styles.concreteiconContainer2} onPress={handlePress}>
                <Image  source={require('../assets/roomicon.png')} style={styles.concreteicon} />
                <Text style={styles.concreteiconText} >Room</Text>
            </TouchableOpacity>
        </View>

      </ScrollView>
    
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

  formContainer: {
    width: '99.5%',
    height: '70%',
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 40,
    marginTop: 10,
  },

  row: {
    flexDirection: 'row', // Puts the two icons in a row
    justifyContent: 'space-evenly',// Space between the two icons
    alignItems: 'center',
  },
  concreteiconContainer: {
    backgroundColor: '#FCC205',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop:80 ,
    marginBottom: 20,
    elevation: 10,
    borderColor:'#FCC205',
    borderWidth: 3,
    borderRadius:10

  },
  concreteiconContainer2: {
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 10,
    marginTop:40 ,
    marginBottom: 20,
    borderColor: '#FCC205',
    borderWidth: 2,
    borderRadius: 15
  },
  concreteicon: {
    width: 120, // Adjust the width and height as per your icon's aspect ratio
    height: 90,
    resizeMode: 'contain',
  },
  concreteiconText: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: 'bold',
  },

});
