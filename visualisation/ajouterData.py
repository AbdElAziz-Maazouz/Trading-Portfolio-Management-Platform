import datetime
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from visualisation.controllerOfVisu import buttonAfficherClicked, buttonAppliquerClick, buttonRetourClick,updatePaires, buttonSupprimerClick, fillInComboBoxes, getDdataToShow
from visualisation.myFigure import MainWindow
from visualisation.controllerOfVisu import *


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"ajouterData.ui"))

class ajouterData(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(ajouterData,self).__init__(parent)
        self.setupUi(self)
        dfInitial=getDdataToShow("binance","BTC/USDT","1m",datetime(2020,1,1,1,0,0),datetime(2020,1,1,3,0,0),self)
        self.figure =  MainWindow(dfInitial,self)
        fillInComboBoxes(self)
        self.designerButton.clicked.connect(lambda:buttonAfficherClicked(self))
        self.supprimerButton.clicked.connect(lambda:buttonSupprimerClick(self))
        self.appliquerButton.clicked.connect(lambda:buttonAppliquerClick(self))
        self.retourButton.clicked.connect(lambda:buttonRetourClick(self))
        self.platform.currentIndexChanged.connect(lambda:updatePaires(self))
    