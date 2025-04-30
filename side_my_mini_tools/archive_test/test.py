import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel

class CheckBoxWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.label = QLabel("No boxes checked")
        vbox.addWidget(self.label)

        self.cb1 = QCheckBox('Checkbox 1', self)
        self.cb1.stateChanged.connect(self.checkBoxChanged)
        vbox.addWidget(self.cb1)

        self.cb2 = QCheckBox('Checkbox 2', self)
        self.cb2.stateChanged.connect(self.checkBoxChanged)
        vbox.addWidget(self.cb2)

        self.cb3 = QCheckBox('Checkbox 3', self)
        self.cb3.stateChanged.connect(self.checkBoxChanged)
        vbox.addWidget(self.cb3)

        self.setLayout(vbox)
        self.setWindowTitle('Checkbox Example')
        self.setGeometry(300, 300, 250, 150)

    def checkBoxChanged(self, state):
        sender = self.sender()

        if sender == self.cb1 and state:
            self.label.setText("Checkbox 1 checked")
        elif sender == self.cb2 and state:
            self.label.setText("Checkbox 2 checked")
        elif sender == self.cb3 and state:
            self.label.setText("Checkbox 3 checked")
        else:
            self.label.setText("No boxes checked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckBoxWindow()
    ex.show()
    sys.exit(app.exec_())
