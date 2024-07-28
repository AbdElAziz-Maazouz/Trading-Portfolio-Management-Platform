import time
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import ccxt
from trading.binanceController import trade
from trading.realTrading import tradeReal
from trading.timeSynchro import timeSyncronisationAvecBinance

class WorkerThread(QThread):
    def __init__(self, sym, exchange,capitales,indicatorOfSell,limitOfUsdt,stop,test):
        super().__init__()
        self.sym = sym
        self.exchange = exchange
        self.capitales=capitales
        self.indicatorOfSell=indicatorOfSell
        self.limitOfUsdt=limitOfUsdt
        self.markets= self.exchange.load_markets()
        self.values = []
        self.usdt = 0
        self.total = 0
        self.banque=0
        self.benifit=0
        self.stopp=stop
        self.test = test
    update_signal = pyqtSignal(list, float, float,float,float)

    def run(self):
        timeSyncronisationAvecBinance()
        while self.stopp==False:
            try:
               self.update_signal.emit(self.values, self.total, self.usdt,self.banque,self.benifit)
            except Exception as e:
                print(f"Error in trade(): {e}")
            finally:
                timeSyncronisationAvecBinance()
                if self.test==True:
                    results = trade(self.exchange,self.sym,self.markets,self.capitales,self.indicatorOfSell,self.limitOfUsdt)
                    self.values = results[2]
                    self.total = results[0]
                    self.usdt = results[1]
                    self.banque=results[3]
                    self.benifit=results[4]
                else:
                    results = tradeReal(self.exchange,self.sym,self.markets,self.capitales,self.indicatorOfSell,self.limitOfUsdt)    
                    self.values = results[2]
                    self.total = results[0]
                    self.usdt = results[1]
                    self.banque=results[3]
                    self.benifit=results[4]
            time.sleep(2)

                


class smallWidget(QWidget):
    def __init__(self, parent=None):
        super(smallWidget, self).__init__(parent)
        self.setWindowTitle('smallOne')
        self.setGeometry(50, 50, 300, 100)
        self.k=None
        layout = QHBoxLayout()
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()
        font = QFont()
        font.setPointSize(16)
        # set the font for the label
        self.label1.setFont(font)
        self.label2.setFont(font)
        self.label3.setFont(font)
        self.label4.setFont(font)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label4.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(self.label4)
        self.setLayout(layout)
        self.setMaximumSize(1000, 50)
        self.setMinimumSize(1000, 50)
        


class MyWidget(QWidget):
    def __init__(self,parent=None,symbols=None,exchange=None,capitales=None,indicatorOfSell=None,limitOfUsdt=None,stop=False,test=None):
        super(MyWidget,self).__init__(parent)
        self.setWindowTitle('My Widget')
        self.stop=stop
        self.symbols=symbols
        self.test=test
        self.exchange=exchange
        self.capitales=capitales
        self.indicatorOfSell=indicatorOfSell
        self.limitOfUsdt=limitOfUsdt
        self.panels = {}
        self.benifits = smallWidget(self)
        self.benifits.label1.setText("bank")
        self.benifits.label1.setStyleSheet("background-color:#5aff68;")
        self.benifits.label2.setText("")
        self.benifits.label3.setText("benifit")
        self.benifits.label3.setStyleSheet("background-color:#5aff68;")
        self.benifits.label4.setText("")
      
        self.totalAndUsdt = smallWidget(self)
        self.totalAndUsdt.label1.setText("totale")
        self.totalAndUsdt.label1.setStyleSheet("background-color:#5aff68;")
        self.totalAndUsdt.label2.setText("")
        self.totalAndUsdt.label3.setText("USDT")
        self.totalAndUsdt.label3.setStyleSheet("background-color:#5aff68;")
        self.totalAndUsdt.label4.setText("")
        

        self.headers={"symbols":"symbols","balance":"balance","price":"price","percentage":"percentage"}
        self.head = smallWidget(self)
        self.head.label1.setText(str(self.headers["symbols"]))
        self.head.label1.setStyleSheet("background-color:#5aff68;")
        self.head.label2.setText(str(self.headers["balance"]))
        self.head.label2.setStyleSheet("background-color:#5aff68;")
        self.head.label3.setText(str(self.headers["price"]))
        self.head.label3.setStyleSheet("background-color:#5aff68;")
        self.head.label4.setText(str(self.headers["percentage"]))
        self.head.label4.setStyleSheet("background-color:#5aff68;")
        if self.symbols[-1]!="USDT":
            for i in range(0,len(self.symbols)):
               if self.symbols[i]=="USDT":
                  break
            self.symbols.pop(i)
            capOfUsdt=self.capitales[i]
            self.capitales.pop(i)
            self.symbols.append("USDT")
            self.capitales.append(capOfUsdt)
            
        for i in self.symbols[:-1]:
            panel_name = i
            panel = smallWidget(self)
            self.panels[panel_name] = panel
            self.panels[panel_name].k=i
            self.panels[panel_name].label1.setText(str(self.panels[panel_name].k))
            self.panels[panel_name].label1.setStyleSheet("background-color:#5aff68;")
            self.panels[panel_name].label2.setText("")
            self.panels[panel_name].label3.setText("")
            self.panels[panel_name].label4.setText("")
            
            
        # Create layout and add labels
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.benifits)
        self.layout.addWidget(self.totalAndUsdt)
        self.layout.addWidget(self.head)
        for panel_name in self.panels:
            self.layout.addWidget(self.panels[panel_name])
        self.setLayout(self.layout)
        self.setMaximumSize(1000, 400)
        self.setMinimumSize(1000, 400)
        # Create worker thread and connect signal to update function
        self.worker = WorkerThread(self.symbols,self.exchange,self.capitales,self.indicatorOfSell,self.limitOfUsdt,self.stop,self.test)
        self.worker.update_signal.connect(self.update_labels)
        self.worker.start()

    def clear(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_labels(self, values,total,usdt,banque,benifit):
        if benifit==100:
            color="blue"
        elif benifit<100:
            color="red"
        else:
            color="green"
        for i,v in zip(self.symbols,values):
            self.panels[i].label2.setText(str(v[0])+"$")
            self.panels[i].label3.setText(str(v[1])+"$")
            self.panels[i].label4.setText(str(v[2])+"%")
        self.totalAndUsdt.label2.setText(str(total)+"$")
        self.totalAndUsdt.label4.setText(str(usdt)+"$")
        self.benifits.label2.setText(str(banque)+"$")
        self.benifits.label4.setStyleSheet(f"color:{color};")
        self.benifits.label4.setText(str(benifit)+"%")



FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"tradePanel.ui"))

class tradePanel(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(tradePanel,self).__init__(parent)
        self.setupUi(self)
        self.cancle.clicked.connect(parent.closingtradePanel)
        self.exchange = None
        self.symbols=None
        self.dataPanel = None