import 'package:flutter/material.dart';
import 'common_app.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Sample list of notes to be passed to CommonApp
    List<Map<String, String>> notes = [
      {'title': 'Note 1', 'description': 'Description 1'},
      {'title': 'Note 2', 'description': 'Description 2'},
    ];

    return MaterialApp(
      title: 'Notes App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: CommonApp(notes: notes),
    );
  }
}
