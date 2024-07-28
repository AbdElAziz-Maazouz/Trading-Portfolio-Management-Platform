import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QLabel




FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"apiPanel.ui"))

class apiPanel(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(apiPanel,self).__init__(parent)
        self.setupUi(self)
        self.layout1 = QVBoxLayout()
        self.panel = QWidget(self)
        self.panel.setGeometry(400,200,350,300)
        self.sendere=None
        if parent.strings!=None:
            for string in parent.strings:
                button = QPushButton(string)
                button.clicked.connect(parent.on_button_clicked)
                self.layout1.addWidget(button)
            self.panel.setLayout(self.layout1)

    def clear(self):
        while self.layout1.count():
            child = self.layout1.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
     

# if __name__ == '__main__':
#     app = QApplication([])
#     widget = apiPanel()
#     widget.show()
#     app.exec_()