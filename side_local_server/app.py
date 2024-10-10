import os
import sys
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Determine the base path for the application
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # Running in a development environment
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Define the shared folder path
SHARED_FOLDER = os.path.join(BASE_PATH, 'shared_folder')

# Create the shared folder if it doesn't exist
if not os.path.exists(SHARED_FOLDER):
    os.makedirs(SHARED_FOLDER)

# Set the upload folder (this will be the same as the shared folder)
UPLOAD_FOLDER = SHARED_FOLDER

# Home route - display all files and folders in the shared folder
@app.route('/')
def home():
    folder = request.args.get('folder', '')  # Get the folder name from the query parameter
    folder_path = os.path.join(SHARED_FOLDER, folder) if folder else SHARED_FOLDER
    
    # List files and folders
    shared_files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        shared_files.append({
            'name': item,
            'is_directory': os.path.isdir(item_path),
            'path': os.path.relpath(item_path, SHARED_FOLDER).replace('\\', '/')  # Use relative path and forward slashes
        })

    return render_template('index.html', shared_files=shared_files, current_folder=folder)

# Route to download files from the 'shared_folder' or subfolders
@app.route('/download/<path:filename>')
def download_file(filename):
    full_path = os.path.join(SHARED_FOLDER, filename)
    logging.debug(f"Attempting to download file at: {full_path}")
    print(f"Attempting to download: {filename}")  # Log the attempted filename
    try:
        return send_from_directory(SHARED_FOLDER, filename)
    except FileNotFoundError:
        logging.error(f"File not found: {full_path}")
        return "File not found", 404

# Route to upload files to the selected folder in 'shared_folder'
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(url_for('home'))
    
    folder_path = request.form.get('folder_path', '')  # Get the folder path from the form
    files = request.files.getlist('files')  # Get multiple files from the form
    
    for file in files:
        if file.filename == '':
            continue
        save_path = os.path.join(SHARED_FOLDER, folder_path, file.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Create folder if it doesn't exist
        file.save(save_path)  # Save each file
    
    return redirect(url_for('home'))

# Route to create a new folder in 'shared_folder'
@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form.get('folder_name')
    if folder_name:
        folder_path = os.path.join(SHARED_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
