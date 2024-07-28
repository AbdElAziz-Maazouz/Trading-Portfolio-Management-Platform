import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton,QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from controller import getDdataToShow

class MainWindow2(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.setParent(parent)
        self.initUI()

    def initUI(self):
        self.label = QLabel()
        self.resize(590, 300)
        self.label = QLabel(self)
        self.label.setGeometry(QRect(40, 90, 491, 91))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("INSTALLING DATA ... THAT MAY TAKE SEVERAL MINUTES")        
