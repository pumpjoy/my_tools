import 'package:flutter/material.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';


import 'package:http/http.dart' as http;
import 'package:csv/csv.dart'; // Ensure you have this dependency


const fileName = "clock_in_diary.csv";



class CommonApp extends StatelessWidget {
  final List<Map<String, String>> notes;

  CommonApp({required this.notes});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Common App'),
        actions: <Widget>[
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'Settings') {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => SettingsPage(notes: notes)),
                );
              }
            },
            itemBuilder: (BuildContext context) {
              return {'Settings'}.map((String choice) {
                return PopupMenuItem<String>(
                  value: choice,
                  child: Text(choice),
                );
              }).toList();
            },
          ),
        ],
      ),
      body: Center(child: Text('Home Page Content')),
    );
  }
}

class SettingsPage extends StatelessWidget {
  final List<Map<String, String>> notes;

  SettingsPage({required this.notes});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Settings')),
      body: ListView(
        children: [
          ListTile(
            title: Text('Export Notes to Local'),
            onTap: () async {
              await saveNotesToCSV(notes);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Notes exported to local storage')),
              );
            },
          ),
          ListTile(
            title: Text('Import Notes from Local'),
            onTap: () async {
              // Implement import logic
              await importNotesFromCSV();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Notes imported from local storage')),
              );
            },
          ),
          /* GOOGLE DRIVE UI
          ListTile(
            title: Text('Export Notes to Google Drive'),
            onTap: () async {
              // Implement export to Google Drive
              await exportToGoogleDrive();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Notes exported to Google Drive')),
              );
            },
          ),
          ListTile(
            title: Text('Import Notes from Google Drive'),
            onTap: () async {
              // Implement import from Google Drive
              await importFromGoogleDrive();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Notes imported from Google Drive')),
              );
            },
          ), */
        ],
      ),
    );
  }
}



// Saving notes to local CSV
Future<void> saveNotesToCSV(List<Map<String, String>> notes) async {
  final directory = await getApplicationDocumentsDirectory();
  final path = '${directory.path}/$fileName';
  final file = File(path);

  String csvData = const ListToCsvConverter().convert(
    notes.map((note) => [note['title'], note['description']]).toList(),
  );

  await file.writeAsString(csvData);
  print('Notes saved to $path');
}

// Importing notes from local CSV
Future<void> importNotesFromCSV() async {
  final directory = await getApplicationDocumentsDirectory();
  final path = '${directory.path}/$fileName';
  final file = File(path);

  if (!file.existsSync()) {
    print('File does not exist');
    return;
  }

  String csvData = await file.readAsString();
  List<List<dynamic>> rows = const CsvToListConverter().convert(csvData);

  // Example of updating notes based on imported data (adjust as needed)
  List<Map<String, dynamic>> importedNotes = rows.map((row) {
    return {'title': row[0], 'description': row[1]};
  }).toList();

  // Do something with the imported notes
  print(importedNotes);
}


/* GOOGLE DRIVE BACKEND:

import 'package:googleapis/drive/v3.dart' as drive;
import 'package:googleapis_auth/auth_io.dart';

// OAuth credentials
const _clientId = 'YOUR_GOOGLE_OAUTH_CLIENT_ID';
const _clientSecret = 'YOUR_GOOGLE_OAUTH_CLIENT_SECRET';
// Scopes for Google Drive
const _scopes = [drive.DriveApi.driveFileScope];


// Function to authenticate with Google
Future<http.Client> authenticateGoogle() async {
  var clientId = ClientId(_clientId, _clientSecret);
  var authClient = await clientViaUserConsent(clientId, _scopes, (url) {
    // You can use any way to present this URL to the user (e.g., a webview)
    print("Please go to the following URL and grant access: $url");
  });
  return authClient;
}

// Exporting notes to Google Drive
Future<void> exportToGoogleDrive(String filePath) async {
  var client = await authenticateGoogle();
  var driveApi = drive.DriveApi(client);

  // File to be uploaded
  var fileToUpload = File(filePath);
  var fileStream = fileToUpload.openRead();
  var media = drive.Media(fileStream, fileToUpload.lengthSync());

  var driveFile = drive.File();
  driveFile.name = fileName; // Name of the file to be uploaded

  try {
    var response = await driveApi.files.create(
      driveFile,
      uploadMedia: media,
    );
    print("Uploaded file ID: ${response.id}");
  } catch (e) {
    print("Failed to upload to Google Drive: $e");
  }
}

// Import from Google Drives
Future<void> importFromGoogleDrive(String fileId) async {
  var client = await authenticateGoogle();
  var driveApi = drive.DriveApi(client);

  try {
    var file = await driveApi.files
        .get(fileId, downloadOptions: drive.DownloadOptions.fullMedia);

    // The file object is of type drive.Media
    if (file is drive.Media) {
      // Write the file content to local storage
      var directory = await getApplicationDocumentsDirectory();
      var localFile = File('${directory.path}/$fileName');

      var fileSink = localFile.openWrite();
      await file.stream
          .pipe(fileSink); // Pipe the media content to local storage
      await fileSink.flush();
      await fileSink.close();

      print("Downloaded file saved to: ${localFile.path}");
    } else {
      print("No media content available for the file.");
    }
  } catch (e) {
    print("Failed to download file from Google Drive: $e");
  }
}
*/