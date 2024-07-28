from doctest import COMPARISON_FLAGS
from symbol import comparison
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from os import path
from loginAndSignin.ajouterApi import ajouterApiPan
from loginAndSignin.comancer import comancer
from loginAndSignin.controllerOfApp import ajouterApiAction, loginethod, logout, siginMethod, switchPages
# from loginAndSignin.controllerOfApp import ajouterApiAction, loginethod, logout, siginMethod, switchPages, switchToajouterApiPage, switchTocompairePage, switchToindexPage, switchTologinPagePage, switchTosigninPage, switchTovisualisationPage, switchTowellcomePage
from loginAndSignin.index import indexPan
from loginAndSignin.login import loginPan
from loginAndSignin.signin import signinPan
from trading.apiPanel import apiPanel
from trading.switching import goTrade, switchPage
from trading.switching import switchToajouterApiPage, switchToapiPanel, switchTocompairePage, switchToindexPage, switchTologinPagePage, switchTosigninPage, switchTotestOrReal, switchTovisualisationPage, switchTowellcomePage
from trading.tradePanel import tradePanel
from trading.tradingPan import tradingPanel
from visualisation.ajouterData import ajouterData
from loginAndSignin.welcome import wellcomePan
from  comparaison.ajouterData import ajouterDataCompare

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"MyApplication.ui"))

   


class MyApplicationPan(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(MyApplicationPan,self).__init__(parent)
        self.setupUi(self)
        self.signinPage = signinPan(self)
        self.signinPage.hide()
        self.loginPage = loginPan(self)
        self.loginPage.hide()
        self.wellcomePage=wellcomePan(self)
        self.wellcomePage.hide()
        self.indexPage=indexPan(self)
        self.ajouterApiPage=ajouterApiPan(self)
        self.ajouterApiPage.hide()
        self.visualisationPage  = ajouterData(self)
        self.visualisationPage.hide()
        self.compairePage=ajouterDataCompare(self)
        self.compairePage.hide()
        self.tradingpanel = tradingPanel(self)
        self.tradingpanel.hide()



        self.visualisationPage.cancle.clicked.connect(lambda:switchPages(self.visualisationPage,self.wellcomePage))
        self.indexPage.signinButton.clicked.connect(lambda:switchTosigninPage(self.indexPage,self))
        self.indexPage.loginButton.clicked.connect(lambda:switchTologinPagePage(self.indexPage,self))
        self.loginPage.cancle.clicked.connect(lambda:switchToindexPage(self.loginPage,self))
        self.signinPage.cancle.clicked.connect(lambda:switchToindexPage(self.signinPage,self))
        self.loginPage.loginButton.clicked.connect(lambda:loginethod(self))
        self.signinPage.signinButton.clicked.connect(lambda:siginMethod(self))
        self.wellcomePage.logout.clicked.connect(lambda:logout(self))
        self.wellcomePage.ajouter.clicked.connect(lambda:switchToajouterApiPage(self.wellcomePage,self))
        # self.wellcomePage.visualisation.clicked.connect(lambda:switchPages(self.wellcomePage,self.visualisationPage))
        self.wellcomePage.visualisation.clicked.connect(lambda:switchTovisualisationPage(self.wellcomePage,self))
        self.ajouterApiPage.cancle.clicked.connect(lambda:switchTowellcomePage(self.ajouterApiPage,self))
        self.ajouterApiPage.ajouter.clicked.connect(lambda:ajouterApiAction(self))
        self.wellcomePage.comancer.clicked.connect(lambda:goTrade(self))
        self.wellcomePage.compaire.clicked.connect(lambda:switchTocompairePage(self.wellcomePage,self))
        self.tradingpanel.apiPanel.cancle.clicked.connect(lambda:switchPage(self.tradingpanel,self.wellcomePage))
        # self.tradingpanel.tradePanel.cancle.clicked.connect(lambda:switchPages(self.tradingpanel.tradePanel,self.tradingPanel.apiPanel))
        self.compairePage.cancle.clicked.connect(lambda:switchTowellcomePage(self.compairePage,self))
        self.tradingpanel.parametresPanel.cancle.clicked.connect(lambda:switchPage(self.tradingpanel,self.wellcomePage))
        self.tradingpanel.testOrReal.cancle.clicked.connect(lambda:switchPage(self.tradingpanel,self.wellcomePage))
        
       
        # self.wellcomePage.comencer.clicked.connect(lambda:switchPages(self.wellcomePage,self.trade))
        # self.wellcomePage.statistics.clicked.connect(lambda:switchPages(self.wellcomePage,self.statistics))
