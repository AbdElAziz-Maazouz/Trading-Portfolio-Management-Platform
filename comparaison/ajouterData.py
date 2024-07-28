import datetime
from datetime import datetime
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from comparaison.controller import buttonAfficherClicked, buttonAjouterClick, fillInComboBoxes, getDdataToShow
from comparaison.installing import MainWindow2
from comparaison.myFigure import MainWindow
from comparaison.controller import *


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"ajouterData.ui"))

class ajouterDataCompare(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(ajouterDataCompare,self).__init__(parent)
        self.setupUi(self)
        dfInitial=getDdataToShow("kucoin","BTC/USDT","1d",datetime(2020,1,1,0,0,0),datetime(2020,2,1,0,0,0),self)
        self.figure =  MainWindow(dfInitial,self)
        self.pan1 = MainWindow2(self)
        self.pan1.setGeometry(0,0,1122,641)
        self.pan1.setStyleSheet("background-color:white;")
        self.pan1.hide()
        fillInComboBoxes(self)
        self.designerButton.clicked.connect(lambda:buttonAfficherClicked(self))
        self.AjouterButton.clicked.connect(lambda:buttonAjouterClick(self))
        self.platform.currentIndexChanged.connect(lambda:updatePaires(self))

    