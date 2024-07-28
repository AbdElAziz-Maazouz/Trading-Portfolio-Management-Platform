from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from os import path

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"welcome.ui"))

class wellcomePan(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(wellcomePan,self).__init__(parent)
        self.setupUi(self)
        self.cin=None
        