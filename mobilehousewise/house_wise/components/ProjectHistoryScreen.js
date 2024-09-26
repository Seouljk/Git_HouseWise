import React from 'react';
import { View, Text, FlatList } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import { useNavigation } from '@react-navigation/native'; // Import useNavigation hook

const ProjectHistoryScreen = () => {
const navigation = useNavigation(); // Access navigation
  const projects = [
    { id: '1', name: 'Project A' },
    { id: '2', name: 'Project B' },
    { id: '3', name: 'Project C' },
  ];

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Project History</Text>
      <FlatList
        data={projects}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 10 }}>
            <Icon name="folder" size={20} color="#000" />
            <Text style={{ marginLeft: 10 }}>{item.name}</Text>
          </View>
        )}
      />
    </View>
  );
};

export default ProjectHistoryScreen;
