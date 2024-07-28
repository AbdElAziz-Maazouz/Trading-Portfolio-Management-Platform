import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path



# class Ui_listWidgetItem(QtWidgets.QWidget):
#     def __init__(self,item, parent=None):
#         super(Ui_listWidgetItem, self).__init__(parent)
#         self.setupUp(Ui_listWidgetItem)
#         self.name = "button"
#         self.button = QtWidgets.QPushButton("hello")
#         self.button.setStyleSheet("background-color: white;")
#         self.button.resize(200, 40)
#         layout = QtWidgets.QHBoxLayout()
#         layout.addWidget(self.button)
#         self.setLayout(layout)

class Ui_listWidgetItem(PyQt5.QtWidgets.QListWidgetItem):
    def __init__(self,parent=None):
        super(Ui_listWidgetItem,self).__init__(parent)
        # self.setupUi(item)
        self.name="button"
        self.button = QtWidgets.QPushButton("hello")
        self.button.setStyleSheet("background-color: white;")
        # self.button.text=self.name
        self.button.resize(200,40)
 
