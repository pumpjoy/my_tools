# Note: I'm lazy so some user convenience is not implemented like finding if multiple pdf are chosen.
import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QComboBox, QLabel, QPushButton, QStackedLayout, QFileDialog, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt
from PIL import Image
from PyPDF2 import PdfWriter

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,800)
        self.setWindowTitle("Tools 0.5")

        # Create the tabs and set up the layout
        self.tabs = QTabWidget()
        self.tab_jpg = QWidget()
        self.tab_pdf = QWidget()
        self.tab_folder = QWidget()
        
        self.list_of_file_paths = []
        
        ####################################################
        # First tab: JPG
        self.tabs.addTab(self.tab_jpg, "JPG")
        
        # Create the drop-down menus
        self.jpg_dropdown = QComboBox()
        self.jpg_dropdown.addItem("JPG/PNG Resize (Percentage)")
        self.jpg_dropdown.addItem("JPG/PNG Crop")
        self.jpg_dropdown.addItem("JPG Colour Picker")
        self.jpg_dropdown.addItem("JPG-to-PNG Converter")
        self.jpg_dropdown.addItem("JPG-to-PDF Converter")
        self.jpg_dropdown.currentIndexChanged.connect(self.jpg_on_dropdown_changed)
        
        # Create first stacked layouts
        self.jpg_stack = QStackedLayout()
        
        ##########################
        # Stack: JPG-PNG-Resizer (Percentage)
        # Create the jpg/png resize page
        self.jpg_png_resize_page = QWidget()
        jpg_png_resize_label1 = QLabel("Enter a number between 0 and 300: (Resize based on percentage)")
        jpg_png_resize_label2 = QLabel("")
        jpg_png_resize_label3 = QLabel("This is a JPG/PNG Resizer by Percentage. File selected:")
        jpg_png_resize_button1 = QPushButton("Select Image File")
        jpg_png_resize_button1.clicked.connect(lambda: self.select_file(jpg_png_resize_label3, 'file', 'Image File (*.jpg *.jpeg *.png)'))
        jpg_png_resize_button2 = QPushButton("Submit", self)
        jpg_png_resize_button2.clicked.connect(lambda: self.jpg_png_resizer(jpg_png_resize_label2, 1))
        self.jpg_resize_line_edit1 = QLineEdit()
        
        self.jpg_resize_layout = QVBoxLayout()
        self.jpg_resize_layout.addWidget(jpg_png_resize_button1)
        self.jpg_resize_layout.addWidget(jpg_png_resize_label1)
        self.jpg_resize_layout.addWidget(self.jpg_resize_line_edit1)
        self.jpg_resize_layout.addWidget(jpg_png_resize_button2)
        self.jpg_resize_layout.addWidget(jpg_png_resize_label2)
        self.jpg_resize_layout.addWidget(jpg_png_resize_label3)
        self.jpg_resize_layout.addStretch()
        self.jpg_png_resize_page.setLayout(self.jpg_resize_layout)

        ##########################
        # Stack: JPG-Resizer 2 (Freedom) 
        # Create the JPG Resize page
        """
        # Create the jpg resize2 (freedom) page
        # TODO INCOMPLETE FUNCTION
        # self.jpg_resize2_page = QWidget()
        # jpg_resize2_label1 = QLabel("Width")
        # jpg_resize2_label2 = QLabel("Height")
        # jpg_resize2_label3 = QLabel("Maintain Aspect Ratio")
        # jpg_resize2_button1 = QPushButton("Select Image File")
        # self.jpg_resize2_line_edit1 = QLineEdit()
        # self.jpg_resize2_line_edit2 = QLineEdit()
        # self.jpg_resize2_checkbox1 = QCheckBox(self)
        # self.jpg_resize2_checkbox1.stateChanged.connect(self.jpg_png_resizer)
        # self.jpg_resize2_checkbox2 = QCheckBox(self)
        # self.jpg_resize2_checkbox2.stateChanged.connect(self.jpg_png_resizer)
        # jpg_resize2_label4 = QLabel("Do Not Enlarge")
        # jpg_resize2_button2 = QPushButton("Submit")
        # jpg_resize2_label5 = QLabel("")
        # jpg_resize2_button2.clicked.connect(lambda: self.resize(jpg_resize2_label5, 2, 'Image Files (*.jpg *.jpeg *.png')))
        # jpg_resize2_layout = QGridLayout()
        # jpg_resize2_layout.addWidget(jpg_resize2_button1, 0, 0)
        # jpg_resize2_layout.addWidget(jpg_resize2_label1, 1, 0)
        # jpg_resize2_layout.addWidget(self.jpg_resize2_line_edit1, 1, 1)
        # jpg_resize2_layout.addWidget(jpg_resize2_label2, 2, 0)
        # jpg_resize2_layout.addWidget(self.jpg_resize2_line_edit2, 2, 1)
        # jpg_resize2_layout.addWidget(jpg_resize2_label3, 3, 0)
        # jpg_resize2_layout.addWidget(self.jpg_resize2_checkbox1, 3, 1)
        # jpg_resize2_layout.addWidget(jpg_resize2_label4, 4, 0)
        # jpg_resize2_layout.addWidget(self.jpg_resize2_checkbox1, 4, 1)
        # jpg_resize2_layout.setRowStretch(jpg_resize2_layout.rowCount(), 1)
        # self.jpg_resize2_page.setLayout(jpg_resize2_layout)
        """
        
        ##########################
        # Stack: JPG/PNG-Crop 
        # Create the JPG crop page
        self.jpg_png_crop_page = QWidget()
        self.jpg_png_crop_label1 = QLabel("This is JPG/PNG Crop")
        self.jpg_png_crop_button1 = QPushButton("Button 2")
        
        self.jpg_png_crop_layout = QVBoxLayout()
        self.jpg_png_crop_layout.addWidget(self.jpg_png_crop_button1)
        self.jpg_png_crop_layout.addWidget(self.jpg_png_crop_label1)
        self.jpg_png_crop_layout.addStretch()
        self.jpg_png_crop_page.setLayout(self.jpg_png_crop_layout)
        
        ##########################
        # Stack: JPG Colour Picker
        # Colour picker that displays HEX, RGB, HSV values
        # TODO Colour Picker: Add pixel enhancer circle (like that one in website)
        # TODO Colour Picker: Add image size changer
        self.jpg_colour_picker_page = QWidget()
        jpg_colour_picker_label1 = QLabel("This is a colour picker. Select Image file, will display HEX, RGB and HSV values")
    
        
        jpg_colour_picker_label2 = QLabel("")
        self.jpg_colour_picker_label_hex = QLabel("HEX: ")
        self.jpg_colour_picker_label_hex.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.jpg_colour_picker_label_rgb = QLabel("RGB: ")
        self.jpg_colour_picker_label_rgb.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.jpg_colour_picker_label_hsv = QLabel("HSV: ")
        self.jpg_colour_picker_label_hsv.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        jpg_colour_picker_button1 = QPushButton("Select Image File", self)
        jpg_colour_picker_button1.clicked.connect(lambda: self.jpg_colour_picker_select_file(jpg_colour_picker_label2))
    
        self.jpg_colour_picker_image_label = QLabel() 
    
        self.jpg_colour_picker_misc_layout = QVBoxLayout() 
        self.jpg_colour_picker_misc_layout.addWidget(jpg_colour_picker_button1)
        self.jpg_colour_picker_misc_layout.addWidget(jpg_colour_picker_label1)
        self.jpg_colour_picker_misc_layout.addWidget(jpg_colour_picker_label2)
        self.jpg_colour_picker_misc_layout.addWidget(self.jpg_colour_picker_label_hex)
        self.jpg_colour_picker_misc_layout.addWidget(self.jpg_colour_picker_label_rgb)
        self.jpg_colour_picker_misc_layout.addWidget(self.jpg_colour_picker_label_hsv) 
        
        self.jpg_colour_picker_image_layout = QHBoxLayout()
        self.jpg_colour_picker_image_layout.addWidget(self.jpg_colour_picker_image_label)
        
        jpg_colour_picker_main_layout = QVBoxLayout()
        jpg_colour_picker_main_layout.addLayout(self.jpg_colour_picker_misc_layout)
        jpg_colour_picker_main_layout.addLayout(self.jpg_colour_picker_image_layout)
        jpg_colour_picker_main_layout.addStretch()
        
        self.jpg_colour_picker_page.setLayout(jpg_colour_picker_main_layout)
        
        
        
        ##########################
        # Stack: JPG-to-PNG 
        # Create the JPG to PNG page
        self.jpg_png_page = QWidget()
        jpg_png_label1 = QLabel("This is JPG to PNG converter", self) 
        
        # Initialize conversion mode and set the initial index
        self.conversion_mode = "jpg-png" 
        self.jpg_png_combo_box = QComboBox()
        self.jpg_png_combo_box.addItems(["JPG-PNG", "PNG-JPG"]) 
        self.jpg_png_combo_box.currentIndexChanged.connect(self.jpg_png_update_conversion_mode)
        
        jpg_png_button1 = QPushButton("Select Multiple Image Files", self)
        jpg_png_button1.clicked.connect(lambda: self.jpg_png_select_file(jpg_png_label1))
        jpg_png_button2 = QPushButton("Convert all")
        jpg_png_button2.clicked.connect(lambda: self.jpg_png_convert(jpg_png_label1))
        
        self.jpg_png_layout = QVBoxLayout()
        self.jpg_png_layout.addWidget(self.jpg_png_combo_box)
        self.jpg_png_layout.addWidget(jpg_png_button1)
        self.jpg_png_layout.addWidget(jpg_png_button2) 
        self.jpg_png_layout.addWidget(jpg_png_label1)
        self.jpg_png_layout.addStretch()
        self.jpg_png_page.setLayout(self.jpg_png_layout)
        
        
        ##########################
        # Stack: JPG-to-PDF Converter
        # Create the JPG to PDF Converter page
        self.jpg_to_pdf_page = QWidget()
        jpg_to_pdf_label1 = QLabel("This is Image to PDF Converter", self)
        self.jpg_to_pdf_label2 = QLabel("", self)
        jpg_to_pdf_button1 = QPushButton("Select Multiple Image Files", self)
        jpg_to_pdf_button1.clicked.connect(lambda: self.select_file(jpg_to_pdf_label1, 'files', 'Image Files (*.jpg *.jpeg *.png)'))
        jpg_to_pdf_button2 = QPushButton("Convert and Merge")
        jpg_to_pdf_button2.clicked.connect(lambda: self.jpg_to_pdf_convert(jpg_to_pdf_label1))
        
        self.jpg_to_pdf_layout = QVBoxLayout()
        self.jpg_to_pdf_layout.addWidget(jpg_to_pdf_button1)
        self.jpg_to_pdf_layout.addWidget(jpg_to_pdf_button2)
        self.jpg_to_pdf_layout.addWidget(self.jpg_to_pdf_label2)
        self.jpg_to_pdf_layout.addWidget(jpg_to_pdf_label1)
        self.jpg_to_pdf_layout.addStretch()
        self.jpg_to_pdf_page.setLayout(self.jpg_to_pdf_layout)
        
        
        
        ####################################################
        # Summarize JPG Tab
        # Add the pages to the stack layouts
        self.jpg_stack.addWidget(self.jpg_png_resize_page)
        # self.jpg_stack.addWidget(self.jpg_resize2_page)
        self.jpg_stack.addWidget(self.jpg_png_crop_page)
        self.jpg_stack.addWidget(self.jpg_colour_picker_page)
        self.jpg_stack.addWidget(self.jpg_png_page)
        self.jpg_stack.addWidget(self.jpg_to_pdf_page)

############################################################
        # Second tab: PDF
        self.tabs.addTab(self.tab_pdf, "PDF")

        # Create the drop-down menus
        self.pdf_dropdown = QComboBox()
        self.pdf_dropdown.addItem("PDF Merge")
        self.pdf_dropdown.addItem("PDF Split")
        self.pdf_dropdown.currentIndexChanged.connect(self.pdf_on_dropdown_changed)

        # Create second stacked layouts
        self.pdf_stack = QStackedLayout()
        
        ##########################
        # Stack 1: PDF Merge 
        # Create PDF Merge page
        self.pdf_merge_page = QWidget()
        pdf_merge_label1 = QLabel("This is PDF Merger", self)
        self.pdf_merge_label2 = QLabel("", self)
        pdf_merge_button1 = QPushButton("Select Multiple PDF Files", self)
        pdf_merge_button1.clicked.connect(lambda: self.select_file(pdf_merge_label1, 'files', "PDF Files (*.pdf)"))
        pdf_merge_button2 = QPushButton("Merge PDF Files")
        pdf_merge_button2.clicked.connect(lambda: self.pdf_merge_convert(pdf_merge_label1))
        self.pdf_merge_layout = QVBoxLayout()
        self.pdf_merge_layout.addWidget(pdf_merge_button1)
        self.pdf_merge_layout.addWidget(pdf_merge_button2)
        self.pdf_merge_layout.addWidget(self.pdf_merge_label2)
        self.pdf_merge_layout.addWidget(pdf_merge_label1)
        self.pdf_merge_layout.addStretch()
        self.pdf_merge_page.setLayout(self.pdf_merge_layout)

        ##########################
        # Stack 2: PDF Split
        # Create the PDF Split page
        self.pdf_split_page = QWidget()
        self.pdf_split_label = QLabel("This is PDF Split")
        self.pdf_split_button = QPushButton("Button 4")
        self.pdf_split_layout = QVBoxLayout()
        self.pdf_split_layout.addWidget(self.pdf_split_label)
        self.pdf_split_layout.addWidget(self.pdf_split_button)
        self.pdf_split_layout.addStretch()
        self.pdf_split_page.setLayout(self.pdf_split_layout)

        ####################################################
        # Summarize PDF tab
        # Add the pages to the stack layouts
        self.pdf_stack.addWidget(self.pdf_merge_page)
        self.pdf_stack.addWidget(self.pdf_split_page)

############################################################
        # Third tab: Folder 
        self.tabs.addTab(self.tab_folder, "Folder")

        # Create the drop-down menus
        self.folder_dropdown = QComboBox()
        self.folder_dropdown.addItem("Subfolder Remover")
        self.folder_dropdown.currentIndexChanged.connect(self.pdf_on_dropdown_changed)

        # Create third stacked layouts
        self.folder_stack = QStackedLayout()
        
        # Create SubFolder Remover Page
        self.subf_remove_page = QWidget()
        subf_remove_label1 = QLabel("This will extract 1 level of subfolder depth within the folder; The contents of subfolders in this folder will be extracted and deleted into this folder.")
        subf_remove_label2 = QLabel("")
        self.subf_remove_label3 = QLabel("", self)
        subf_remove_button1= QPushButton("Select Folder")
        subf_remove_button1.clicked.connect(lambda: self.select_file(subf_remove_label2, 'folder'))
        subf_remove_button2= QPushButton("Subfolder remove")
        subf_remove_button2.clicked.connect(lambda: self.subfolder_remove())
        self.subf_remove_layout = QVBoxLayout()
        self.subf_remove_layout.addWidget(subf_remove_button1)
        self.subf_remove_layout.addWidget(subf_remove_button2)
        self.subf_remove_layout.addWidget(subf_remove_label1)
        self.subf_remove_layout.addWidget(subf_remove_label2)
        self.subf_remove_layout.addWidget(self.subf_remove_label3)
        self.subf_remove_layout.addStretch()
        self.subf_remove_page.setLayout(self.subf_remove_layout)
        
        ####################################################
        # Summarize Folder tab
        self.folder_stack.addWidget(self.subf_remove_page)


############################################################
        # Summarize all tab
        # Set up the layout for each tab
        self.layout_tab_jpg = QVBoxLayout()
        self.layout_tab_jpg.addWidget(self.jpg_dropdown)
        self.layout_tab_jpg.addLayout(self.jpg_stack)
        self.tab_jpg.setLayout(self.layout_tab_jpg)

        self.layout_tab_pdf = QVBoxLayout()
        self.layout_tab_pdf.addWidget(self.pdf_dropdown)
        self.layout_tab_pdf.addLayout(self.pdf_stack)
        self.tab_pdf.setLayout(self.layout_tab_pdf)
        
        self.layout_tab_folder = QVBoxLayout()
        self.layout_tab_folder.addWidget(self.folder_dropdown)
        self.layout_tab_folder.addLayout(self.folder_stack)
        self.tab_folder.setLayout(self.layout_tab_folder)

        # Set the central widget and show the window
        self.setCentralWidget(self.tabs)
        self.setGeometry(100, 100, 800, 800)
        self.show()


    def jpg_on_dropdown_changed(self, index):
        self.jpg_stack.setCurrentIndex(index)

    def pdf_on_dropdown_changed(self, index):
        self.pdf_stack.setCurrentIndex(index)        

    def folder_on_dropdown_changed(self, index):
        self.folder_stack.setCurrentIndex(index)


    """
    select file
    * Label to determine which label to change text
    @param
        ~~i - integer. To keep track of which button is calling. I'm too lazy to make multiple, will change if have issues.~~
        i - file/folder, files/folders.
    """
    def select_file(self, label, i, type=None):
        self.list_of_file_paths = []
        options = QFileDialog.Option()
        
        if i == 'file':
            # Select 1 File  
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", type, options=options)
            if file_path: 
                self.list_of_file_paths.append(str(file_path))
                label.setText(f"Selected: {file_path}")
        
        if i == 'files':
            # Select Multiple Files
            really_long_string = '' 
            file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", type, options=options)
            if file_paths:
                for file_path in file_paths:
                    file_path = str(file_path)
                    self.list_of_file_paths.append(file_path)
                    really_long_string += file_path + '\n'
                label.setText(really_long_string)
                
        if i == 'folder': 
            # Select 1 Folder 
            file_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")
            if file_path: 
                self.list_of_file_paths.append(str(file_path))
                label.setText(f"Selected: {file_path}")
        
        if i == 'folders': 
            # Select 1 Folder 
            file_paths = QFileDialog.getExistingDirectory(self, "Select Folders", "")
            if file_paths:
                for file_path in file_paths:
                    file_path = str(file_path)
                    self.list_of_file_paths.append(file_path)
                    really_long_string += file_path + '\n'
                label.setText(really_long_string) 



    """
    jpg resizer (ONLY SUPPORT 1 FILE FOR NOW)
    """
    def jpg_png_resizer(self, label, i):
        user_input = self.jpg_resize_line_edit1.text()
        match(i):
            case 1:
                # Check if within range of 0 to 300
                if user_input.isnumeric():
                    if int(user_input)>=0 and int(user_input)<= 300:
                        if len(self.list_of_file_paths) == 0:
                            label.setText("Please select an image file first.")
                        input_image = Image.open(self.list_of_file_paths[0])
                        width, height = input_image.size
                        new_width = int(width*int(user_input)/100)
                        new_height = int(height*int(user_input)/100)
                        resized_image = input_image.resize((new_width, new_height))

                        # Select where to save
                        options = QFileDialog.Options()
                        file_type = self.list_of_file_paths[0][-4:]
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

                with Image.open(self.list_of_file_paths[0]) as image:
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
                    file_type = self.list_of_file_paths[0][-4:]
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
    Colour picker
    """
    def jpg_colour_picker_select_file(self, label):
        self.list_of_file_paths = []
        options = QFileDialog.Option()
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", 'Image Files (*.jpg *.jpeg *.png)', options=options)
        if file_path: 
            self.list_of_file_paths.append(str(file_path))
            label.setText(f"Selected: {file_path}")
            self.qimage = QImage(file_path)
            self.pixmap = QPixmap.fromImage(self.qimage)
            # Scale down the picture 
            self.scale_and_display_image()
            self.jpg_colour_picker_image_label.mousePressEvent = self.get_pixel_colour
            
    def scale_and_display_image(self):
        # Scale down the picture to only be
        im_width = 800 
        im_height = 600

        scaled_pixmap = self.pixmap.scaled(
            im_width, im_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        
        # Set the pixmap to the QLabel
        self.jpg_colour_picker_image_label.setPixmap(scaled_pixmap)
    
 
    def get_pixel_colour(self, event):
        displayed_size = self.jpg_colour_picker_image_label.pixmap().size()
        original_size = self.qimage.size()
        
        x = event.pos().x()
        y = event.pos().y()
        
        scale_x = original_size.width() / displayed_size.width()
        scale_y = original_size.height() / displayed_size.height()

        mapped_x = int(x * scale_x)
        mapped_y = int(y * scale_y)

        if 0 <= mapped_x < original_size.width() and 0 <= mapped_y < original_size.height():
            colour = QColor(self.qimage.pixel(mapped_x, mapped_y))
            r, g, b, a = colour.red(), colour.green(), colour.blue(), colour.alpha()
            h, s, v, _ = colour.getHsv()
            hex_code = colour.name(QColor.HexArgb)
            
            self.jpg_colour_picker_label_hex.setText(f"HEX: {hex_code}")
            self.jpg_colour_picker_label_rgb.setText(f"RGB: ({r}, {g}, {b})")
            self.jpg_colour_picker_label_hsv.setText(f"HSV: ({h}, {s}, {v})")


    """
    Change jpg to png convert 
    """
    def jpg_png_update_conversion_mode(self, index):
        conversion_modes = ["jpg-png", "png-jpg"]
        self.conversion_mode = conversion_modes[index]
    
    def jpg_png_select_file(self, label):
        self.list_of_file_paths = []
        options = QFileDialog.Option()
        
        index = self.jpg_png_combo_box.currentIndex()
        conversion_mode = ["jpg-png", "png-jpg"][index]
        
        if self.conversion_mode == "jpg-png":
            filter = 'Image Files (*.jpg *.jpeg)'
        elif self.conversion_mode == "png-jpg":
            filter = 'Image Files (*.png)'
            
        really_long_string = '' 
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", filter, options=options)
        if file_paths:
            for file_path in file_paths:
                file_path = str(file_path)
                self.list_of_file_paths.append(file_path)
                really_long_string += file_path + '\n'
            label.setText(really_long_string)
        
    def jpg_png_convert(self, label):
        # Check if theres convertible files in list
        if len(self.list_of_file_paths) == 0:
            label.setText("Please select an image file first.")
        else:
            index = self.jpg_png_combo_box.currentIndex()
            conversion_mode = ["jpg-png", "png-jpg"][index]
            
            dir = os.path.dirname(self.list_of_file_paths[0])
            
            
            for file in self.list_of_file_paths:
                image = Image.open(file)
                
                if conversion_mode=="jpg-png":
                    path = os.path.join(dir, os.path.basename(file).replace('jpg', 'png'))
                if conversion_mode=="png-jpg":
                    image = image.convert('RGB')
                    path = os.path.join(dir, os.path.basename(file).replace('png', 'jpg'))
                
                image.save(path)
                image.close()
            
            label.setText("Sucessfully converted all JPG to PNG")


    """
    Change jpg to pdf convert 
    """     
    def jpg_to_pdf_convert(self, label):
        # Check if theres convertible files in list
        if len(self.list_of_file_paths) == 0:
            label.setText("Please select an image file first.")
        else:
            # Creates a dialog to ask for new file name to be saved as pdf
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF (*.pdf)", options=options)

            # Actual conversion
            image_list = []
            # If png, direct just change the file type
            image1 = Image.open(self.list_of_file_paths[0])
            if image1.mode == 'RGBA':
                bg = Image.new("RGB", image1.size, (255,255,255)) #if transparent background, turn black
                bg.paste(image1, mask=image1.split()[3])
                image1 = bg
            else:
                image1.convert('RGB')
                
                
            for file_path in self.list_of_file_paths[1:]:
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
                self.jpg_to_pdf_label2.setText(f"Error: {e}")
    
    

    """
    pdf merger
    """
    def pdf_merge_convert(self, label):
        # Check if theres convertible files in list
        if len(self.list_of_file_paths) == 0:
            label.setText("Please select some pdf file first. (Note program does not error check if only 1 pdf is chosen)")
        else:
            # Program so far only uses filename sorting
            # TODO: do drag and drop to sort
            self.list_of_file_paths.sort()
            merger = PdfWriter()
            for pdf in self.list_of_file_paths:
                merger.append(pdf)
            # Creates a dialog to ask for new file name to be saved as pdf
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF (*.pdf)", options=options)
            merger.write(file_name)
            merger.close()



    """
    subfolder remove
    """
    def subfolder_remove(self):
        # Sanity check check if there's convertible folder in list
        # self.list_of_file_paths is the big folder
        if len(self.list_of_file_paths) == 0:
            self.subf_remove_label3.setText("Please select a folder.")
            return
        
        main_folder = None
        for path in self.list_of_file_paths:
            try:
                if os.path.isdir(path):
                    main_folder = path
                    break
            except Exception as e:
                self.subf_remove_label3.setText(f"Error checking directory: {str(e)}")
                return
            
        if not main_folder:
            self.subf_remove_label3.setText("This folder does not have subfolder to be extracted and removed.")
            return

        # List of all directories within the main folder
        subdirectories = [entry for entry in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, entry))]
        
        # Continue extract if subfolders exist
        for subdirectory in subdirectories:
            sub_path = os.path.join(main_folder, subdirectory)
            
            try:
                # Get all contents of subdirectory
                contents = os.listdir(sub_path)
                
                for content in contents:
                    src_path = os.path.join(sub_path, content)
                    des_path = os.path.join(main_folder, content)
                    
                    # Move each item from subfolder to main folder
                    shutil.move(src_path, des_path)
            
                # After moving all items, remove the empty subfolder
                if not os.listdir(sub_path):
                    os.rmdir(sub_path)
            
            except Exception as e:
                self.subf_remove_label3.setText(f"An error occurred while processing {subdirectory}: {str(e)}")
        
        self.subf_remove_label3.setText("Subfolders extracted and removed.")
                    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())