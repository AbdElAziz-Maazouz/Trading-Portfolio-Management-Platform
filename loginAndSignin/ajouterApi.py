import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"ajouterApi.ui"))

class ajouterApiPan(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(ajouterApiPan,self).__init__(parent)
        self.setupUi(self)
        self.key.setText("your key")
        self.secret.setText("your secret")