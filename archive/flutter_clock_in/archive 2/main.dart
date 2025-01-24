//TODO: SAVE INTO CSV, AND LOAD IT EVERYTIME LAUNCH

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:csv/csv.dart';

void main() {
  runApp(NotesApp());
}

class NotesApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Notes App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: NotesPage(),
    );
  }
}

class NotesPage extends StatefulWidget {
  @override
  _NotesPageState createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  List<Map<String, String>> notes = [];

  // Function to clean up text by removing specific symbols
  String cleanText(String text) {
    // Replace unwanted symbols
    return text.replaceAll(RegExp(r'[*_~^`]+'), ''); // Remove *, _, ~, ^, and `
  }


  Future<void> saveNotesToCSV() async {
    // Prepare the CSV content
    List<List<dynamic>> rows = [];
    rows.add(['Title', 'Description']); // Header row
    for (var note in notes) {
      rows.add([note['title'], note['description']]);
    }

    // Convert List<List<dynamic>> to CSV string
    String csv = const ListToCsvConverter().convert(rows);

    // Get the path to save the file
    Directory directory = await getApplicationDocumentsDirectory();
    File file = File('${directory.path}/notes.csv');

    // Write the CSV string to the file
    await file.writeAsString(csv);
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notes'),
      ),
      body: ListView.builder(
        itemCount: notes.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(cleanText(notes[index]['title']!)), // Clean the title
            subtitle: Text(
              cleanText(notes[index]['description']!.split('\n').first), // Clean and show the first line of the description
            ),
            onTap: () async {
              // Navigate to Note Details page
              final updatedNote = await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => NoteDetailsPage(
                    note: notes[index],
                    index: index,
                  ),
                ),
              );

              // Update the note if edited
              if (updatedNote != null) {
                setState(() {
                  notes[index] = updatedNote;
                });
              }
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final newNote = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => AddNotePage()),
          );

          if (newNote != null) {
            setState(() {
              notes.add(newNote);
            });
          }
        },
        child: const Icon(Icons.add),
        tooltip: 'Add Note',
      ),
    );
  }
}


class AddNotePage extends StatefulWidget {
  @override
  _AddNotePageState createState() => _AddNotePageState();
}

class _AddNotePageState extends State<AddNotePage> {
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Note'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: 'Title'),
            ),
            const SizedBox(height: 16.0),
            TextField(
              controller: _descriptionController,
              decoration: const InputDecoration(labelText: 'Description'),
              maxLines: 5,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                if (_titleController.text.isNotEmpty && _descriptionController.text.isNotEmpty) {
                  Navigator.pop(context, {
                    'title': _titleController.text,
                    'description': _descriptionController.text,
                  });
                }
              },
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}

class NoteDetailsPage extends StatelessWidget {
  final Map<String, String> note;
  final int index;

  NoteDetailsPage({required this.note, required this.index});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            icon: Icon(Icons.edit),
            onPressed: () async {
              final editedNote = await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => EditNotePage(note: note),
                ),
              );

              if (editedNote != null) {
                Navigator.pop(context, editedNote); // Return the edited note
              }
            },
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // RichText for the Title with custom parsing (just above description)
            RichText(
              text: TextSpan(
                children: _parseText(note['title']!),
              ),
              textAlign: TextAlign.left,
            ),
            SizedBox(height: 16.0),

            // RichText for the Description with custom parsing
            RichText(
              text: TextSpan(
                children: _parseText(note['description']!),
              ),
              textAlign: TextAlign.left,
            ),
          ],
        ),
      ),
    );
  }

  List<TextSpan> _parseText(String text) {
    List<TextSpan> spans = [];
    // Regular expressions to capture bold (*word*), italic (_word_), strikethrough (~word~), and underline (^word^)
    final RegExp exp = RegExp(r'(```.*?```)|(\*[^*]+\*)|(_[^_]+_)|(~[^~]+~)|(\^[^\^]+\^)');
    int currentIndex = 0;

    // Find all matches for bold (*word*), italic (_word_), strikethrough (~word~), and underline (^word^)
    for (final match in exp.allMatches(text)) {
      // Add the part of the text before the match
      if (match.start > currentIndex) {
        spans.add(TextSpan(
          text: text.substring(currentIndex, match.start),
          style: TextStyle(color: Colors.black),
        ));
      }

      String matchText = match.group(0)!;

      // Check if it's a bold (*word*), italic (_word_), strikethrough (~word~), or underline (^word^) match
      if (matchText.startsWith('```') && matchText.endsWith('```')) {
      spans.add(TextSpan(
        text: matchText.substring(3, matchText.length - 3), // Remove ``` on both sides
        style: TextStyle(color: Colors.black), // Plain text style
      ));
      } else if (matchText.startsWith('*') && matchText.endsWith('*')) {
        // Bold text
        spans.add(TextSpan(
          text: matchText.substring(1, matchText.length - 1), // Remove * on both sides
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black),
        ));
      } else if (matchText.startsWith('_') && matchText.endsWith('_')) {
        // Italic text
        spans.add(TextSpan(
          text: matchText.substring(1, matchText.length - 1), // Remove _ on both sides
          style: TextStyle(fontStyle: FontStyle.italic, color: Colors.black),
        ));
      } else if (matchText.startsWith('~') && matchText.endsWith('~')) {
        // Strikethrough text
        spans.add(TextSpan(
          text: matchText.substring(1, matchText.length - 1), // Remove ~ on both sides
          style: TextStyle(
            decoration: TextDecoration.lineThrough,
            color: Colors.black,
          ),
        ));
      } else if (matchText.startsWith('^') && matchText.endsWith('^')) {
        // Underlined text
        spans.add(TextSpan(
          text: matchText.substring(1, matchText.length - 1), // Remove ^ on both sides
          style: TextStyle(
            decoration: TextDecoration.underline,
            color: Colors.black,
          ),
        ));
      }

      // Update the current index to after the match
      currentIndex = match.end;
    }

    // Add any remaining text after the last match
    if (currentIndex < text.length) {
      spans.add(TextSpan(
        text: text.substring(currentIndex),
        style: TextStyle(color: Colors.black),
      ));
    }

    return spans;
  }
}


class EditNotePage extends StatefulWidget {
  final Map<String, String> note;

  EditNotePage({required this.note});

  @override
  _EditNotePageState createState() => _EditNotePageState();
}

class _EditNotePageState extends State<EditNotePage> {
  late TextEditingController _titleController;
  late TextEditingController _descriptionController;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.note['title']);
    _descriptionController = TextEditingController(text: widget.note['description']);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Note'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: 'Title'),
            ),
            const SizedBox(height: 16.0),
            TextField(
              controller: _descriptionController,
              decoration: const InputDecoration(labelText: 'Description'),
              maxLines: 5,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                if (_titleController.text.isNotEmpty && _descriptionController.text.isNotEmpty) {
                  Navigator.pop(context, {
                    'title': _titleController.text,
                    'description': _descriptionController.text,
                  });
                }
              },
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}
