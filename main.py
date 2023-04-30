import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QCheckBox, QGridLayout, QComboBox, QLabel, QPushButton, QStackedLayout, QFileDialog, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PIL import Image

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,800)
        self.setWindowTitle("Tools 0.2")

        # Create the tabs and set up the layout
        self.tabs = QTabWidget()
        self.tab_jpg = QWidget()
        self.tab_pdf = QWidget()


        # First tab
        self.tabs.addTab(self.tab_jpg, "JPG")
        
        # Create the drop-down menus
        self.jpg_dropdown = QComboBox()
        self.jpg_dropdown.addItem("Image Resize(Percentage)")
        self.jpg_dropdown.addItem("Image Resize(Aspect Ratio)")
        self.jpg_dropdown.addItem("Image Crop")
        self.jpg_dropdown.addItem("JPG-to-PDF Converter")
        self.jpg_dropdown.currentIndexChanged.connect(self.jpg_on_dropdown_changed)
        
        # Create first stacked layouts
        self.jpg_stack = QStackedLayout()

        # Create the jpg resize page
        self.jpg_resize_page = QWidget()
        jpg_resize_button1 = QPushButton("Select Image File")
        jpg_resize_button1.clicked.connect(lambda: self.select_file(self.jpg_resize_label3, 1))
        jpg_resize_label1 = QLabel("Enter a number between 0 and 300: (Resize based on percentage)")
        self.jpg_resize_line_edit1 = QLineEdit()
        jpg_resize_button2 = QPushButton("Submit", self)
        jpg_resize_button2.clicked.connect(lambda: self.jpg_resizer(self.jpg_resize_label2, 1))
        self.jpg_resize_label2 = QLabel("Only first file will be taken if multiple are selected")
        self.jpg_resize_label3 = QLabel("File selected")
        self.jpg_resize_layout = QVBoxLayout()
        self.jpg_resize_layout.addWidget(jpg_resize_button1)
        self.jpg_resize_layout.addWidget(jpg_resize_label1)
        self.jpg_resize_layout.addWidget(self.jpg_resize_line_edit1)
        self.jpg_resize_layout.addWidget(jpg_resize_button2)
        self.jpg_resize_layout.addWidget(self.jpg_resize_label2)
        self.jpg_resize_layout.addWidget(self.jpg_resize_label3)
        self.jpg_resize_layout.addStretch()
        self.jpg_resize_page.setLayout(self.jpg_resize_layout)

        # Create the jpg resize2 (freedom) page
        # TODO INCOMPLETE FUNCTION
        self.jpg_resize2_page = QWidget()
        jpg_resize2_button1 = QPushButton("Select Image File")
        jpg_resize2_label1 = QLabel("Width")
        self.jpg_resize2_line_edit1 = QLineEdit()
        jpg_resize2_label2 = QLabel("Height")
        self.jpg_resize2_line_edit2 = QLineEdit()
        self.jpg_resize2_checkbox1 = QCheckBox(self)
        self.jpg_resize2_checkbox1.stateChanged.connect(self.jpg_resizer)
        jpg_resize2_label3 = QLabel("Maintain Aspect Ratio")
        self.jpg_resize2_checkbox2 = QCheckBox(self)
        self.jpg_resize2_checkbox2.stateChanged.connect(self.jpg_resizer)
        jpg_resize2_label4 = QLabel("Do Not Enlarge")
        jpg_resize2_button2 = QPushButton("Submit")
        jpg_resize2_label5 = QLabel("")
        jpg_resize2_button2.clicked.connect(lambda: self.resize(jpg_resize2_label5, 2))
        jpg_resize2_layout = QGridLayout()
        jpg_resize2_layout.addWidget(jpg_resize2_button1, 0, 0)
        jpg_resize2_layout.addWidget(jpg_resize2_label1, 1, 0)
        jpg_resize2_layout.addWidget(self.jpg_resize2_line_edit1, 1, 1)
        jpg_resize2_layout.addWidget(jpg_resize2_label2, 2, 0)
        jpg_resize2_layout.addWidget(self.jpg_resize2_line_edit2, 2, 1)
        jpg_resize2_layout.addWidget(jpg_resize2_label3, 3, 0)
        jpg_resize2_layout.addWidget(self.jpg_resize2_checkbox1, 3, 1)
        jpg_resize2_layout.addWidget(jpg_resize2_label4, 4, 0)
        jpg_resize2_layout.addWidget(self.jpg_resize2_checkbox1, 4, 1)
        jpg_resize2_layout.setRowStretch(jpg_resize2_layout.rowCount(), 1)
        self.jpg_resize2_page.setLayout(jpg_resize2_layout)


        # Create the jpg crop page
        self.jpg_crop_page = QWidget()
        self.jpg_crop_label1 = QLabel("This is JPG Crop")
        self.jpg_crop_button1 = QPushButton("Button 2")
        self.jpg_crop_layout = QVBoxLayout()
        self.jpg_crop_layout.addWidget(self.jpg_crop_label1)
        self.jpg_crop_layout.addWidget(self.jpg_crop_button1)
        self.jpg_crop_page.setLayout(self.jpg_crop_layout)


        # Create the jpg to pdf converter page
        self.jpg_list_of_file_paths = []
        self.jpg_to_pdf_page = QWidget()
        jpg_to_pdf_button1 = QPushButton("Select Multiple Image Files", self)
        jpg_to_pdf_button1.clicked.connect(lambda: self.select_file(jpg_to_pdf_label1, 2))
        jpg_to_pdf_button2 = QPushButton("Convert and Merge")
        jpg_to_pdf_button2.clicked.connect(lambda: self.jpg_to_pdf_convert(jpg_to_pdf_label1))
        jpg_to_pdf_label1 = QLabel("This is Image to PDF Converter", self)
        self.jpg_to_pdf_label2 = QLabel("", self)
        self.jpg_to_pdf_layout = QVBoxLayout()
        self.jpg_to_pdf_layout.addWidget(jpg_to_pdf_button1)
        self.jpg_to_pdf_layout.addWidget(jpg_to_pdf_button2)
        self.jpg_to_pdf_layout.addWidget(self.jpg_to_pdf_label2)
        self.jpg_to_pdf_layout.addWidget(jpg_to_pdf_label1)
        self.jpg_to_pdf_layout.addStretch()
        self.jpg_to_pdf_page.setLayout(self.jpg_to_pdf_layout)


        # Add the pages to the stack layouts
        self.jpg_stack.addWidget(self.jpg_resize_page)
        self.jpg_stack.addWidget(self.jpg_resize2_page)
        self.jpg_stack.addWidget(self.jpg_crop_page)
        self.jpg_stack.addWidget(self.jpg_to_pdf_page)

############################################################

        # Second tab
        self.tabs.addTab(self.tab_pdf, "PDF")

        # Create the drop-down menus
        self.pdf_dropdown = QComboBox()
        self.pdf_dropdown.addItem("PDF Merge")
        self.pdf_dropdown.addItem("PDF Split")
        self.pdf_dropdown.currentIndexChanged.connect(self.pdf_on_dropdown_changed)

        # Create second stacked layouts
        self.pdf_stack = QStackedLayout()

        # Create the pdf merge page
        self.pdf_merge_page = QWidget()
        self.pdf_merge_label = QLabel("This is PDF Merge")
        self.pdf_merge_button = QPushButton("Button 3")
        self.pdf_merge_layout = QVBoxLayout()
        self.pdf_merge_layout.addWidget(self.pdf_merge_label)
        self.pdf_merge_layout.addWidget(self.pdf_merge_button)
        self.pdf_merge_page.setLayout(self.pdf_merge_layout)

        # Create the pdf split page
        self.pdf_split_page = QWidget()
        self.pdf_split_label = QLabel("This is PDF Split")
        self.pdf_split_button = QPushButton("Button 4")
        self.pdf_split_layout = QVBoxLayout()
        self.pdf_split_layout.addWidget(self.pdf_split_label)
        self.pdf_split_layout.addWidget(self.pdf_split_button)
        self.pdf_split_page.setLayout(self.pdf_split_layout)


        # Add the pages to the stack layouts
        self.pdf_stack.addWidget(self.pdf_merge_page)
        self.pdf_stack.addWidget(self.pdf_split_page)

############################################################
        # Set up the layout for each tab
        self.layout_tab_jpg = QVBoxLayout()
        self.layout_tab_jpg.addWidget(self.jpg_dropdown)
        self.layout_tab_jpg.addLayout(self.jpg_stack)
        self.tab_jpg.setLayout(self.layout_tab_jpg)

        self.layout_tab_pdf = QVBoxLayout()
        self.layout_tab_pdf.addWidget(self.pdf_dropdown)
        self.layout_tab_pdf.addLayout(self.pdf_stack)
        self.tab_pdf.setLayout(self.layout_tab_pdf)

        # Set the central widget and show the window
        self.setCentralWidget(self.tabs)
        self.setGeometry(100, 100, 800, 800)
        self.show()


    def jpg_on_dropdown_changed(self, index):
        self.jpg_stack.setCurrentIndex(index)


    def pdf_on_dropdown_changed(self, index):
        self.pdf_stack.setCurrentIndex(index)


    """
    select file
    * label to determine which label to change text
    * i to keep track of which button is calling
    """
    def select_file(self, label, i):
        self.jpg_list_of_file_paths = []
        match(i):
            case 1:
                # Select single image file
                options = QFileDialog.Option()
                file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Image Files (*.jpg *.jpeg *.png)", options=options)
                if file_paths:
                    file_path = str(file_paths[0])
                    self.jpg_list_of_file_paths.append(file_path)
                    label.setText(file_path)
            case 2:
                # To select image files
                really_long_string = ''
                options = QFileDialog.Option()
                file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Image Files (*.jpg *.jpeg *.png)", options=options)
                if file_paths:
                    for file_path in file_paths:
                        file_path = str(file_path)
                        self.jpg_list_of_file_paths.append(file_path)
                        really_long_string += file_path + '\n'
                    label.setText(really_long_string)


    """
    jpg resizer (ONLY SUPPORT 1 FILE FOR NOW)
    """
    def jpg_resizer(self, label, i):
        user_input = self.jpg_resize_line_edit1.text()
        match(i):
            case 1:
                # Check if within range of 0 to 300
                if user_input.isnumeric():
                    if int(user_input)>=0 and int(user_input)<= 300:
                        if len(self.jpg_list_of_file_paths) == 0:
                            label.setText("Please select an image file first.")
                        input_image = Image.open(self.jpg_list_of_file_paths[0])
                        width, height = input_image.size
                        new_width = int(width*int(user_input)/100)
                        new_height = int(height*int(user_input)/100)
                        resized_image = input_image.resize((new_width, new_height))

                        # Select where to save
                        options = QFileDialog.Options()
                        file_type = self.jpg_list_of_file_paths[0][-4:]
                        match(file_type):
                            case ".jpg":
                                file_type = "JPG (*.jpg)"
                            case ".jpeg":
                                file_type = "JPEG(*.jpeg)"
                            case ".png":
                                file_type = "PNG (*.png)"
                        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_type, options=options)
                        try:
                            resized_image.save(file_name)
                            label.setText("Resize done.")
                        except ValueError as e:
                            pass
                        return
                label.setText("Please enter a number between 0 and 300")

            case 2:
                user_width = self.jpg_resize2_line_edit1.text()
                user_height = self.jpg_resize2_line_edit2.text()

                if user_input.isnumeric(): pass

                with Image.open(self.jpg_list_of_file_paths[0]) as image:
                    # keep aspect ratio
                    if self.jpg_resize2_checkbox1.isChecked(): 
                        width_ratio = user_width / input_image.width if user_width is not None else user_height / image.height
                        height_ratio= user_height / image.height if user_height is not None else user_width / image.width
                        ratio = min(width_ratio, height_ratio)
                        new_width = int(image.width * ratio)
                        new_height = int(image.height * ratio)

                    else:
                        new_width = user_width
                        new_height= user_width


                    # Check if image is allowed to enlarge 
                    # TODO:
                    # if self.jpg_resize2_checkbox1.isChecked(): 
                    #     user_width > image.width 


                    # Return and save
                    resized_image = input_image.resize((new_width, new_height))

                    # Select where to save
                    options = QFileDialog.Options()
                    file_type = self.jpg_list_of_file_paths[0][-4:]
                    match(file_type):
                        case ".jpg":
                            file_type = "JPG (*.jpg)"
                        case ".jpeg":
                            file_type = "JPEG(*.jpeg)"
                        case ".png":
                            file_type = "PNG (*.png)"
                    file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_type, options=options)
                    try:
                        resized_image.save(file_name)
                        label.setText("Resize done.")
                    except ValueError as e:
                        pass
                    return
                

    """
    Change jpg to pdf convert 
    """
    def jpg_to_pdf_convert(self, label):
        # check if theres convertible files in list
        if len(self.jpg_list_of_file_paths) == 0:
            label.setText("Please select an image file first.")
        else:
            # creates a dialog to ask for new file name to be saved as pdf
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF (*.pdf)", options=options)

            # actual conversion
            image_list = []
            # if png, direct just change the file type
            image1 = Image.open(self.jpg_list_of_file_paths[0])
            if image1.mode == 'RGBA':
                bg = Image.new("RGB", image1.size, (255,255,255)) #if transparent background, turn black
                bg.paste(image1, mask=image1.split()[3])
                image1 = bg
            else:
                image1.convert('RGB')
                
                
            for file_path in self.jpg_list_of_file_paths[1:]:
                image = Image.open(file_path)
                if image.mode == 'RGBA':
                    bg = Image.new('RGB', image.size, (255, 255, 255)) # create a new white background image
                    bg.paste(image, mask=image.split()[3]) # paste the image onto the background
                    image_list.append(bg)
                else:
                    image_list.append(image.convert('RGB'))
                
            try:
                image1.save(file_name, save_all=True, append_images=image_list)
                self.jpg_to_pdf_label2.setText("Convert complete")
            except ValueError as e:
                pass
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())