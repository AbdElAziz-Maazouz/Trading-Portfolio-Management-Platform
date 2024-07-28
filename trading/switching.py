


import time
from comparaison.ajouterData import ajouterDataCompare
from loginAndSignin.ajouterApi import ajouterApiPan
from loginAndSignin.controllerOfApp import ajouterApiAction, loginethod, logout, siginMethod
from loginAndSignin.index import indexPan
from loginAndSignin.login import loginPan
from loginAndSignin.signin import signinPan
from loginAndSignin.welcome import wellcomePan
from trading.apiPanel import apiPanel
from trading.database import getNomPlatformesApi
from trading.tradingPan import tradingPanel
from visualisation.ajouterData import ajouterData
from PyQt5.QtWidgets import QPushButton,QVBoxLayout,QWidget

def switchTovisualisationPage(tohide,pan):
        tohide.hide()
        pan.visualisationPage  = ajouterData(pan)
        pan.visualisationPage.show()
        pan.visualisationPage.cancle.clicked.connect(lambda:switchTowellcomePage(pan.visualisationPage,pan))

def switchTotradingpanel(tohide,pan):
        tohide.hide()
        # pan.tradingpanel  = tradingPanel(pan)
        # pan.tradingpanel.cin=pan.wellcomePage.cin
        # pan.tradingpanel.apiPanel.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel.apiPanel,pan))
        # pan.tradingpanel.parametresPanel.cancle.clicked.connect(lambda:switchToapiPanel(pan.tradingpanel.parametresPanel,pan))
        # pan.tradingpanel.testOrReal.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel,pan))
        # pan.tradingpanel.parametresPanel.cancle.clicked.connect(lambda:switchToapiPanel(pan.tradingpanel.parametresPanel,pan))
        # pan.tradingpanel.testOrReal.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel.testOrReal,pan))
        pan.tradingpanel.show()

def switchTosigninPage(tohide,pan):
        tohide.hide()
        pan.signinPage  = signinPan(pan)
        pan.signinPage.show()
        pan.signinPage.cancle.clicked.connect(lambda:switchToindexPage(pan.signinPage,pan))
        pan.signinPage.signinButton.clicked.connect(lambda:siginMethod(pan))

def switchTologinPagePage(tohide,pan):
        tohide.hide()
        pan.loginPage = loginPan(pan)
        pan.loginPage.show()
        pan.loginPage.cancle.clicked.connect(lambda:switchToindexPage(pan.loginPage,pan))
        pan.loginPage.loginButton.clicked.connect(lambda:loginethod(pan))

def switchTocompairePage(tohide,pan):
        tohide.hide()
        pan.compairePage = ajouterDataCompare(pan)
        pan.compairePage.show()
        pan.compairePage.cancle.clicked.connect(lambda:switchTowellcomePage(pan.compairePage,pan))

def switchToindexPage(tohide,pan):
        tohide.hide()
        pan.indexPage = indexPan(pan)
        pan.indexPage.show()
        pan.indexPage.signinButton.clicked.connect(lambda:switchTosigninPage(pan.indexPage,pan))
        pan.indexPage.loginButton.clicked.connect(lambda:switchTologinPagePage(pan.indexPage,pan))

def switchToajouterApiPage(tohide,pan):
        tohide.hide()
        pan.ajouterApiPage = ajouterApiPan(pan)
        pan.ajouterApiPage.show()
        pan.ajouterApiPage.cancle.clicked.connect(lambda:switchTowellcomePage(pan.ajouterApiPage,pan))
        pan.ajouterApiPage.ajouter.clicked.connect(lambda:ajouterApiAction(pan))

def switchTowellcomePage(tohide,pan):

        tohide.hide()
        cin=pan.wellcomePage.cin
        pan.wellcomePage  = wellcomePan(pan)
        pan.wellcomePage.cin=cin
        pan.wellcomePage.show()
        pan.wellcomePage.logout.clicked.connect(lambda:logout(pan))
        pan.wellcomePage.visualisation.clicked.connect(lambda:switchTovisualisationPage(pan.wellcomePage,pan))
        pan.wellcomePage.comancer.clicked.connect(lambda:goTrade(pan))
        pan.wellcomePage.compaire.clicked.connect(lambda:switchTocompairePage(pan.wellcomePage,pan))
        pan.wellcomePage.ajouter.clicked.connect(lambda:switchToajouterApiPage(pan.wellcomePage,pan))

def switchToapiPanel(tohide,pan):
    tohide.hide()
    #    pan.tradingpanel.apiPanel=apiPanel(pan.tradingpanel)
#        pan.tradingpanel = tradingPanel(pan)
    pan.tradingpanel.strings=None 
    pan.tradingpanel.hide()
    if pan.tradingpanel.apiPanel:
        pan.tradingpanel.apiPanel.clear()
#     pan.tradingpanel.apiPanel = apiPanel(pan.tradingpanel)
#     pan.tradingpanel.apiPanel.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel,pan))
    pan.tradingpanel.strings=getNomPlatformesApi(pan.tradingpanel.cin)
#     if pan.tradingpanel.strings!=None:
#         for string in pan.tradingpanel.strings:
#             button = QPushButton(string)
#             button.clicked.connect(pan.tradingpanel.on_button_clicked)
#             pan.tradingpanel.apiPanel.layout1=QVBoxLayout()
#             pan.tradingpanel.apiPanel.layout1.addWidget(button)
#         pan.tradingpanel.apiPanel.panel.setLayout(pan.tradingpanel.apiPanel.layout1)
#         pan.tradingpanel.show()
#         tohide.hide()
    if pan.tradingpanel.strings!=None:
        for string in pan.tradingpanel.strings:
            button = QPushButton(string)
            button.clicked.connect(pan.tradingpanel.on_button_clicked)
            pan.tradingpanel.apiPanel.layout1=QVBoxLayout()
            pan.tradingpanel.apiPanel.layout1.addWidget(button)
        pan.tradingpanel.apiPanel.panel.setLayout(pan.tradingpanel.apiPanel.layout1)
    
    pan.tradingpanel.apiPanel.show()


def switchTotestOrReal(tohide,pan):
       tohide.hide()
       pan.tradingpanel.testOrReal.show()

def switchPage(tohide,toshow):
      tohide.hide()
      toshow.show()

def goTrade(pan):
    
    
    
    # pan.tradingpanel.strings=None

    # pan.tradingpanel.apiPanel=apiPanel(pan.tradingpanel)
    if pan.tradingpanel.apiPanel:
      pan.tradingpanel.apiPanel.clear()
    pan.wellcomePage.hide()
#     cin=pan.wellcome.cin
    pan.tradingpanel=tradingPanel(pan)
    pan.tradingpanel.hide()
    pan.tradingpanel.cin=pan.wellcomePage.cin
    pan.tradingpanel.strings=None
    pan.tradingpanel.strings=getNomPlatformesApi(pan.tradingpanel.cin)
#     pan.tradingpanel.apiPanel = apiPanel(pan.tradingpanel)
    pan.tradingpanel.apiPanel.cancle.clicked.connect(lambda:switchPage(pan.tradingpanel,pan.wellcomePage))
    pan.tradingpanel.apiPanel.cancle.clicked.connect(lambda:switchPage(pan.tradingpanel,pan.wellcomePage))
    pan.tradingpanel.parametresPanel.cancle.clicked.connect(lambda:switchPage(pan.tradingpanel,pan.wellcomePage))
    pan.tradingpanel.testOrReal.cancle.clicked.connect(lambda:switchPage(pan.tradingpanel,pan.wellcomePage))

    if pan.tradingpanel.strings!=None:
        for string in pan.tradingpanel.strings:
            button = QPushButton(string)
            button.clicked.connect(pan.tradingpanel.on_button_clicked)
            pan.tradingpanel.apiPanel.layout1=QVBoxLayout()
            pan.tradingpanel.apiPanel.layout1.addWidget(button)
        pan.tradingpanel.apiPanel.panel.setLayout(pan.tradingpanel.apiPanel.layout1)
    elif pan.tradingpanel.strings==[]:
          pan.wellcomePage.errorLab.setText("vous n'avez aucun api ,veillez ajouter un api")
          return
    # pan.tradingpanel=tradingPanel(pan)
    # pan.tradingpanel.apiPanel.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel.apiPanel,pan))
    # pan.tradingpanel.parametresPanel.cancle.clicked.connect(lambda:switchToapiPanel(pan.tradingpanel.parametresPanel,pan))
    # pan.tradingpanel.testOrReal.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel,pan))
    # pan.tradingpanel.parametresPanel.cancle.clicked.connect(lambda:switchToapiPanel(pan.tradingpanel.parametresPanel,pan))
    # pan.tradingpanel.testOrReal.cancle.clicked.connect(lambda:switchTowellcomePage(pan.tradingpanel.testOrReal,pan))
    # pan.tradingpanel.cin=pan.wellcomePage.cin
#     pan.tradingpanel.apiPanel.hide()
    pan.tradingpanel.show()
    
    