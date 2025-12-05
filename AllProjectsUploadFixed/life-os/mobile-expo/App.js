import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button, Alert, ScrollView } from 'react-native';

export default function App() {
  const [content, setContent] = useState("hello from mobile");
  const [q, setQ] = useState("hello");

  async function sendIngest(){
    try {
      const res = await fetch('http://0.0.0.0:8000/ingest', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
          source: 'mobile',
          type: 'message',
          timestamp: Math.floor(Date.now()/1000),
          content,
          metadata:{from:'mobile'}
        })
      });
      const j = await res.json();
      Alert.alert('Ingest Success', JSON.stringify(j));
    } catch (e) {
      Alert.alert('Error', String(e));
    }
  }

  async function doSearch(){
    try {
      const res = await fetch('http://0.0.0.0:8000/search/', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({query:q, top_k:5})
      });
      const j = await res.json();
      Alert.alert('Search Results', JSON.stringify(j));
    } catch (e) {
      Alert.alert('Error', String(e));
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Life OS — Mobile Demo</Text>

      <Text style={styles.label}>Ingest Content</Text>
      <TextInput style={styles.input} value={content} onChangeText={setContent} multiline />

      <Button title="Send Ingest" onPress={sendIngest} />

      <Text style={styles.label}>Search Query</Text>
      <TextInput style={styles.input} value={q} onChangeText={setQ} />

      <Button title="Search" onPress={doSearch} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight:'600', marginBottom: 20 },
  label: { marginTop: 20, marginBottom: 6, fontSize: 16 },
  input: { borderWidth:1, borderColor:'#ddd', padding:12, borderRadius:6, fontSize:16 }
});
