import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QLabel






FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"testOrRealPan.ui"))

class testOrRealPan(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(testOrRealPan,self).__init__(parent)
        self.setupUi(self)
        self.test.clicked.connect(parent.testClicked)
        self.real.clicked.connect(parent.realClicked)
        