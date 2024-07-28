import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QLabel
import ccxt
from trading.apiPanel import apiPanel
from trading.choisirParametresPan import choisirParametresPan
from trading.database import getApiOfPlatformeAndUser, getNomPlatformesApi
from trading.testOrRealPan import testOrRealPan


from trading.tradePanel import tradePanel,MyWidget

def is_number(string):
    if string.isnumeric()==True:
        return True
    elif string.isnumeric()==False:
        if "." in string:
            parts = string.split('.')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return True
        if "-" in string :
            tring = string[1:]
            return is_number(tring)
    return False

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"tradingPanel.ui"))

class tradingPanel(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(tradingPanel,self).__init__(parent)
        self.setupUi(self)
        self.cin=None
        self.strings=None
        self.platform=None
        self.testOrReal = testOrRealPan(self)
        self.tradePanel = tradePanel(self)
        self.tradePanel.hide()
        self.apiPanel = apiPanel(self)
        self.apiPanel.hide()
        self.parametresPanel = choisirParametresPan(self)
        self.parametresPanel.hide()
        self.api=None
        self.symbols=[]
        self.capitales=[]
        self.indicatorOfSell=0.02
        self.limitOfUsdt=-10
        self.test=True

    def testClicked(self):
        self.test = True
        self.testOrReal.hide()
        self.apiPanel.show()

    def realClicked(self):
        self.test = False
        self.testOrReal.hide()
        self.apiPanel.show()
  
    def getRealExchange(self,key,secret,platforme):
        # if platforme=="binance":
            exchange = ccxt.binance({
                'apiKey':'your key',
                'secret':'your secret',
                'options': {
                'defaultType':'spot',
                'adjustForTimeDifference': True,
                'test':True
                }
            })
            exchange.set_sandbox_mode(True)
            return exchange


    def getExchange(self,key,secret,platforme):
        exch = getattr(ccxt,platforme)
        exchange = exch()
        print(platforme)
        print(str(exchange))
        return exchange

    def continueMethod(self):
        for i in range(1,int(self.parametresPanel.nbPaires.currentText())+2):
            panel = "panel"+str(i)
            if self.parametresPanel.pan.panels[panel].paire.currentText() in self.symbols:
                self.parametresPanel.errorLabel.setText("vous avez choisis un choix multiple d'un paire")
                self.symbols=[]
                self.capitales=[]
                return 0
            self.symbols.append(self.parametresPanel.pan.panels[panel].paire.currentText())
            if is_number(self.parametresPanel.pan.panels[panel].balance.text())==False: 
                self.parametresPanel.errorLabel.setText("tout les balances doivent etre > 0")
                self.symbols=[]
                self.capitales=[]
                return 0
            self.capitales.append(float(self.parametresPanel.pan.panels[panel].balance.text()))
            if (float(self.parametresPanel.pan.panels[panel].balance.text())<=0) :
                self.parametresPanel.errorLabel.setText("tout les balances doivent etre > 0")
                self.symbols=[]
                self.capitales=[]
                return 0
        if "USDT" not in self.symbols:
            self.parametresPanel.errorLabel.setText("vos paires manquent USDT")
            self.symbols=[]
            self.capitales=[]
            return 0
        if is_number(self.parametresPanel.paireLimit.text())==False:
            self.parametresPanel.errorLabel.setText("le pourcentage des paires doit etre un numero")
            self.symbols=[]
            self.capitales=[]
            return 0
        if is_number(self.parametresPanel.usdtLimit.text())==False:
            self.parametresPanel.errorLabel.setText("le pourcentagede usdt  doit etre un numero")
            self.symbols=[]
            self.capitales=[]
            return 0
        self.indicatorOfSell=float(self.parametresPanel.paireLimit.text())
        self.limitOfUsdt=float(self.parametresPanel.usdtLimit.text())

        self.tradePanel.symbols=self.symbols
        if self.tradePanel.dataPanel:
            self.tradePanel.dataPanel.clear()
        self.tradePanel.dataPanel=MyWidget(parent=self.tradePanel,symbols=self.symbols,exchange=self.tradePanel.exchange,capitales=self.capitales,indicatorOfSell=self.indicatorOfSell,limitOfUsdt=self.limitOfUsdt,test=self.test)
        self.tradePanel.dataPanel.setGeometry(50,50,10,10)
        self.tradePanel.show()
        self.parametresPanel.hide()
        return 1
    
    def getSymbolsAvailables(self,exchange):
        markets = exchange.load_markets()
        m=list(markets)
        currencies=[]
        for i in m:
            if ("/USDT" in i) and ":" not in i:
              paire= i[:i.index("/USDT")] 
              if paire!="TRX":
                 currencies.append(paire)
        currencies.append("USDT")
        return currencies

    def on_button_clicked(self):
        self.api = getApiOfPlatformeAndUser(self.sender().text(),self.cin)
        if self.test==True:
          self.tradePanel.exchange = self.getExchange(self.api[0],self.api[1],self.sender().text())
          self.parametresPanel.show()
          self.apiPanel.hide()
        else:
            self.tradePanel.exchange = self.getRealExchange(self.api[0],self.api[1],self.sender().text())
            self.tradePanel.symbols = []
            self.tradePanel.symbols = self.getSymbolsAvailables(self.tradePanel.exchange)
            print(self.tradePanel.symbols)
            self.capitales = [100 for i in self.tradePanel.symbols]
            if self.tradePanel.dataPanel:
                self.tradePanel.dataPanel.clear()
            self.tradePanel.dataPanel=MyWidget(parent=self.tradePanel,symbols=self.tradePanel.symbols,exchange=self.tradePanel.exchange,capitales=self.capitales,indicatorOfSell=self.indicatorOfSell,limitOfUsdt=self.limitOfUsdt,test=self.test)
            self.tradePanel.dataPanel.setGeometry(50,50,10,10)
            self.tradePanel.show()            
            self.apiPanel.hide()


    def closingtradePanel(self):
        # self.tradePanel.hide()
        self.tradePanel.hide()
        self.tradePanel.dataPanel.worker.stopp = True
        self.symbols=[]
        self.capitales=[]
        self.indicatorOfSell=0
        self.limitOfUsdt=0
        # self.self.tradePanel.symbols=[]
        # self.symbols=[]
        self.apiPanel.show()
        # super().parent.wellcomePage.show()