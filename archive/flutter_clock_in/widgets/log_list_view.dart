// ignore_for_file: unused_import

import 'package:flutter/material.dart';

import '../models/data.dart' as data;
import '../models/models.dart';
import 'log_widget.dart';
import 'search_bar.dart' as search_bar;

class LogListView extends StatelessWidget {
  const LogListView({
    super.key,
    this.selectedIndex,
    this.onSelected,
  });

  final int? selectedIndex;
  final ValueChanged<int>? onSelected;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Note List')
      ),
      body: ListView.builder(
        itemCount: data.notes.length,
        itemBuilder: (context, index) {
          final note = data.notes[index];
          return ListTile(
            title: Text(note.title),
            subtitle: Text(note.date),

            onTap: () {
              // Navigate to detailed view of the note
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => NoteDetailView(note: note) 
                )
              );
            }
          );
        },
      )
    );
  }
}