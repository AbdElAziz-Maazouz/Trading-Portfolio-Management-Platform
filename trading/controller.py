

import ccxt
from comparaison.ajouterData import ajouterDataCompare
from loginAndSignin.ajouterApi import ajouterApiPan
# from MyApplication import switchPages
 
# from loginAndSignin.controllerOfApp import  *
from loginAndSignin.controllerOfApp import  ajouterApiAction, loginethod, logout, siginMethod, switchPages
from loginAndSignin.index import indexPan
from loginAndSignin.login import loginPan
from loginAndSignin.signin import signinPan
from loginAndSignin.welcome import wellcomePan
from trading.binanceController import startbinance

from trading.database import getNomPlatformesApi
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QLabel

from trading.tradingPan import tradingPanel
from visualisation.ajouterData import ajouterData





      



def startTrading(exchange,platforme,currencies):
    # if platforme=="bybit":
    #     startbybit(exchange,currencies)
    if platforme=="binance":
        startbinance(exchange,currencies)
    else :
        print("not developped yet")