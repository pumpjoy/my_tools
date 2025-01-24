// util.dart
// TODO: IMPORT, EXPORT WITH TIME AND DATE. Need time and date???

import 'dart:convert';
import 'dart:io';
import 'package:googleapis/drive/v3.dart' as drive;
import 'package:googleapis_auth/auth_io.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:csv/csv.dart'; // For CSV handling


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

// Import from Google Drives
Future<void> importFromGoogleDrive(String fileId) async {
  var client = await authenticateGoogle();
  var driveApi = drive.DriveApi(client);

  try {
    var file = await driveApi.files.get(fileId, downloadOptions: drive.DownloadOptions.fullMedia);

    // The file object is of type drive.Media
    if (file is drive.Media) {
      // Write the file content to local storage
      var directory = await getApplicationDocumentsDirectory();
      var localFile = File('${directory.path}/clock_in_diary.csv');

      var fileSink = localFile.openWrite();
      await file.stream.pipe(fileSink); // Pipe the media content to local storage
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

// Export to Google Drive
Future<void> exportToGoogleDrive(String filePath) async {
  var client = await authenticateGoogle();
  var driveApi = drive.DriveApi(client);

  // File to be uploaded
  var fileToUpload = File(filePath);
  var fileStream = fileToUpload.openRead();
  var media = drive.Media(fileStream, fileToUpload.lengthSync());

  var driveFile = drive.File();
  driveFile.name = "clock_in_diary.csv"; // Name of the file to be uploaded

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

