import sys
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget,QComboBox,QLineEdit,QStackedLayout, QVBoxLayout,QHBoxLayout, QScrollArea, QPushButton, QListWidget, QLabel
# from trading.apiPanel import apiPanel
# from trading.controller import getExchange, startTrading
# from trading.database import getApiOfPlatformeAndUser, getNomPlatformesApi


class smallWidget(QWidget):
    def __init__(self, parent=None):
        super(smallWidget, self).__init__(parent)
        self.setWindowTitle('smallOne')
        layout = QHBoxLayout()
        self.paire = QComboBox()
        self.paire.addItem("BTC")
        self.paire.addItem("ETH")
        self.paire.addItem("LTC")
        self.paire.addItem("ADA")
        self.paire.addItem("XRP")
        self.paire.addItem("BNB")
        self.paire.addItem("FLUX")
        self.paire.addItem("ETC")
        self.paire.addItem("USDT")
        self.paire.setCurrentIndex(0)
        self.balance = QLineEdit()
        font = QFont()
        font.setPointSize(16)
        layout.addWidget(self.paire)
        layout.addWidget(self.balance)
        self.setLayout(layout)
        self.setMaximumSize(200, 50)
        self.setMinimumSize(200, 50)

class MyWidget(QWidget):
    def __init__(self, parent=None, n=1):
        super(MyWidget, self).__init__(parent)
        self.setWindowTitle('My Widget')
        self.panels = {}
        layout = QVBoxLayout()
        for i in range(1,n+1):
            panel = "panel"+str(i)
            self.panels[panel]=smallWidget()
        panel = "panel"+str(n+1)
        self.panels[panel]=smallWidget()
        for panel in self.panels.values():
            layout.addWidget(panel)
        self.setLayout(layout)
        self.setMaximumSize(200, 400)
        self.setMinimumSize(200, 400)
        



FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"choisirParametresPan.ui"))

class choisirParametresPan(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(choisirParametresPan, self).__init__(parent)
        self.setupUi(self)
        self.pan = MyWidget(self,2)
        self.pan.setGeometry(400,200,10,10)
        self.nbPaires.currentTextChanged.connect(lambda:self.switch_subpanels(int(self.nbPaires.currentText())))
        self.continueButton.clicked.connect(parent.continueMethod)
        
    def switch_subpanels(self,n):
        self.pan.hide()
        self.pan = MyWidget(self,n)
        self.pan.setGeometry(400,200,10,10)
        self.pan.show()


# if __name__=="__main__":
#    app = QApplication(sys.argv)
#    pan = choisirParametresPan()
#    pan.show()
#    sys.exit(app.exec_())