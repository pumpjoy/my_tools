import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMainWindow, QFileDialog, QDesktopWidget, QPushButton, QLabel, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # Creates UI for fixed border window 
    def init_ui(self):
        width = 800
        height = 800
        self.setWindowTitle("JPG to PDF changer")
        self.center()
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.list_of_file_paths = []

        # Button that prompts file selection 
        button = QPushButton("Select Files", self)
        button.move (700, 20)
        button.clicked.connect(self.show_file_dialog)

        # Text to show the file paths
        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 10))
        self.label.setGeometry(20,20,600,600)
        self.label.setAlignment(Qt.AlignTop)
        self.label.setText("JPG files")

        # Second button that prompts to merge
        button2 = QPushButton("Convert", self)
        button2.move(700, 60)
        button2.clicked.connect(self.jpg_to_png)

        self.show()
    
    """
    center 
    """
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    """
    for File open prompt with button press
    """
    def show_file_dialog(self):
        self.list_of_file_paths = []
        really_long_string = ''
        options = QFileDialog.Option()
        #options |= QFileDialog.DontUseNativeDialog
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Image Files (*.jpg )", options=options)
        if file_paths:
            for file_path in file_paths:
                file_path = str(file_path)
                if not file_path.endswith('.jpg'):
                    self.label.setText("Only jpg files allowed.")
                else:
                    self.list_of_file_paths.append(file_path)
                    really_long_string += file_path + '\n'
            self.label.setText(really_long_string)

    """
    Change jpg to png 
    """
    def jpg_to_png(self):
        # check if theres convertible files in list
        if len(self.list_of_file_paths) == 0:
            self.label.setText("Need to have files to convert first")
        else:
            # creates a dialog to ask for new file name to be saved as pdf
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*.pdf)", options=options)

            # actual conversion
            image_list = []
            image1 = Image.open(self.list_of_file_paths[0])
            image1.convert('RGB')

            for file_path in self.list_of_file_paths[1:]:
                image = Image.open(file_path)
                image_list.append(image.convert('RGB'))
            image1.save(file_name, save_all=True, append_images=image_list)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
