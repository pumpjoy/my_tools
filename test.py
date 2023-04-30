import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyPDF2 import PdfFileMerger, PdfFileReader

# Create a PyQt5 application
app = QApplication([])

# Show a file dialog to select the PDF files to merge
file_dialog = QFileDialog()
file_dialog.setFileMode(QFileDialog.ExistingFiles)
file_dialog.setNameFilter('PDF files (*.pdf)')
if file_dialog.exec_() == QFileDialog.Accepted:
    # Get a list of the selected PDF files
    pdf_files = file_dialog.selectedFiles()
else:
    # The user cancelled the file dialog
    pdf_files = []

if not pdf_files:
    # No PDF files were selected
    print('No PDF files selected.')
else:
    # Create a PdfFileMerger object
    merger = PdfFileMerger()

    # Sort the list of PDF files by filename
    pdf_files.sort()

    # Loop through each selected PDF file
    for pdf in pdf_files:
        # Open the PDF file
        pdf_file = open(pdf, 'rb')
        # Create a PdfFileReader object
        pdf_reader = PdfFileReader(pdf_file)
        # Add the PDF pages to the PdfFileMerger object
        merger.append(pdf_reader)
        # Close the PDF file
        pdf_file.close()

    # Show a file dialog to save the merged PDF file
    save_dialog = QFileDialog()
    save_dialog.setAcceptMode(QFileDialog.AcceptSave)
    save_dialog.setDefaultSuffix('pdf')
    save_dialog.setNameFilter('PDF files (*.pdf)')
    if save_dialog.exec_() == QFileDialog.Accepted:
        # Get the filename and location to save the merged PDF file as
        output_file = save_dialog.selectedFiles()[0]
    else:
        # The user cancelled the file dialog
        output_file = None

    if output_file:
        # Create a new PDF file and write the merged pages to it
        output_file = open(output_file, 'wb')
        merger.write(output_file)
        # Close the output PDF file
        output_file.close()

        # Show a message box to confirm the PDF files were merged and saved
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText("PDF files merged and saved successfully!")
        message_box.setWindowTitle("Success")
        message_box.exec_()
    else:
        # Show a message box to inform the user that the PDF files were not merged
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText("PDF files were not merged.")
        message_box.setWindowTitle("Warning")
        message_box.exec_()
