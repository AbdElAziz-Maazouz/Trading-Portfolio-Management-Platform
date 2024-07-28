import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path



FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"index.ui"))

class indexPan(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(indexPan,self).__init__(parent)
        self.setupUi(self)