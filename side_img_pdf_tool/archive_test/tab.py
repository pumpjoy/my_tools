import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QStackedLayout

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,800)
        self.setWindowTitle("Tools 0.2")

        # Create the tabs and set up the layout
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Create the drop-down menus
        self.dropdown1 = QComboBox()
        self.dropdown1.addItem("Option 1")
        self.dropdown1.addItem("Option 2")
        self.dropdown1.currentIndexChanged.connect(self.on_dropdown1_changed)

        self.dropdown2 = QComboBox()
        self.dropdown2.addItem("Option 3")
        self.dropdown2.addItem("Option 4")
        self.dropdown2.currentIndexChanged.connect(self.on_dropdown2_changed)

        # Create the stacked layouts
        self.stack1 = QStackedLayout()
        self.stack2 = QStackedLayout()

        # Create the pages for each stack layout
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.page4 = QWidget()

        # Add labels and buttons to each page
        self.label1 = QLabel("This is Page 1")
        self.label2 = QLabel("This is Page 2")
        self.label3 = QLabel("This is Page 3")
        self.label4 = QLabel("This is Page 4")

        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton("Button 4")

        # Set up the layout for each page
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.button1)
        self.page1.setLayout(self.layout1)

        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.label2)
        self.layout2.addWidget(self.button2)
        self.page2.setLayout(self.layout2)

        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(self.label3)
        self.layout3.addWidget(self.button3)
        self.page3.setLayout(self.layout3)

        self.layout4 = QVBoxLayout()
        self.layout4.addWidget(self.label4)
        self.layout4.addWidget(self.button4)
        self.page4.setLayout(self.layout4)

        # Add the pages to the stack layouts
        self.stack1.addWidget(self.page1)
        self.stack1.addWidget(self.page2)

        self.stack2.addWidget(self.page3)
        self.stack2.addWidget(self.page4)

        # Set up the layout for each tab
        self.layout_tab1 = QVBoxLayout()
        self.layout_tab1.addWidget(self.dropdown1)
        self.layout_tab1.addLayout(self.stack1)
        self.tab1.setLayout(self.layout_tab1)

        self.layout_tab2 = QVBoxLayout()
        self.layout_tab2.addWidget(self.dropdown2)
        self.layout_tab2.addLayout(self.stack2)
        self.tab2.setLayout(self.layout_tab2)

        # Set the central widget and show the window
        self.setCentralWidget(self.tabs)
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def on_dropdown1_changed(self, index):
        self.stack1.setCurrentIndex(index)

    def on_dropdown2_changed(self, index):
        self.stack2.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())