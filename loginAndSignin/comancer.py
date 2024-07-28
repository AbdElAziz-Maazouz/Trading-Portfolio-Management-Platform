import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem
from loginAndSignin.listWidgetItem import Ui_listWidgetItem 

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"comancer.ui"))

class comancer(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(comancer,self).__init__(parent)
        self.setupUi(self)
        for i in range(100):
            # item = QListWidgetItem()
            widget = Ui_listWidgetItem()
            # widget.setupUi(item)
            self.listview.addItem(widget)