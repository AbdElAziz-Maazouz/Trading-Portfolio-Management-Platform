import re
import time

import ccxt
from comparaison.ajouterData import ajouterDataCompare
from loginAndSignin.ajouterApi import ajouterApiPan

from loginAndSignin.database import ajouterApiMethod, ajouterPlatforme, apiExist, clientExist, insertClient, modifierApiMethod, platformExist, trueInfos
from loginAndSignin.index import indexPan
from loginAndSignin.login import loginPan
from loginAndSignin.signin import signinPan
from loginAndSignin.welcome import wellcomePan
# from trading.controller import goTrade
from visualisation.ajouterData import ajouterData

def trueMail(mail):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, mail)==None:
        return False
    else:
        return True
    

def truePhone(phone):
    pattern = r'^[0-9]*$'
    if re.match(pattern, phone)==None:
        return False
    else:
        return True
    

def trueCni(cni):
    pattern = r'^[A-Z][A-Z][0-9]*$'
    if re.match(pattern, cni)==None:
        return False
    else:
        return True


def switchPages(toHide,toShow):
    toHide.hide()
    toShow.show()
    # toHide.deleteLater()
 
     






def siginMethod(pan):
    nom=pan.signinPage.nom.text()
    prenom=pan.signinPage.prenom.text()
    cin=pan.signinPage.cin.text()
    password=pan.signinPage.password.text()
    confirm=pan.signinPage.confirm.text()
    mail=pan.signinPage.mail.text()
    telephone=pan.signinPage.telephone.text()
    messageLabel=pan.signinPage.message
    lista = [nom,prenom,cin,password,confirm,mail,telephone]
    for i in lista:
        if i=="":
            messageLabel.setText("remplissez tout les champs")
            return 
    if password!=confirm:
         messageLabel.setText("utiliser le meme password dans las confirmation")
         return
    if trueCni(cin)==False:
         messageLabel.setText("mal cin")
         return
    if trueMail(mail)==False:
         messageLabel.setText("mal email")
         return
    if truePhone(telephone)==False:
         messageLabel.setText("mal telephone")
         return
    if clientExist(cin)==True:
         messageLabel.setText("utilisateur deja exist")
         return
    insertClient(cin,nom,prenom,telephone,mail,password)
    pan.signinPage.hide()
    pan.loginPage.show()

def loginethod(pan):
    cin=pan.loginPage.cin.text()
    password=pan.loginPage.password.text()
    messageLabel=pan.loginPage.message
    if clientExist(cin)==False:
            messageLabel.setText("utilisateur n'existe pas")
            return
    if trueInfos(cin,password)==False:
            messageLabel.setText("mot de passe incorrecte ou utilisateur n'existe pas")
            return 
    pan.wellcomePage.cin=cin
    print(pan.wellcomePage.cin)
    pan.loginPage.hide()
    pan.wellcomePage.show()
    
    
def logout(pan):
     pan.wellcomePage.cin=None
     pan.wellcomePage.hide()
     pan.loginPage.show()
     

def ajouterApiAction(pan):
     key    = pan.ajouterApiPage.key.text()
     secret = pan.ajouterApiPage.secret.text()
     platforme = pan.ajouterApiPage.platformes.currentText()
     cin=pan.wellcomePage.cin
     
    #  if apiExist(cin,key,platforme)==True:
    #       pan.ajouterApiPage.message.setText("api est deja existe")
    #       return
     
    # Create an instance of the ccxt.kucoin class
    #  exchange = ccxt.kucoin({
    #     'password': "kucoinApiPassword",
    #     'apiKey': key,
    #     'secret': secret
    #  })
     exch = getattr(ccxt,platforme)

     
     exchange=exch({
        'apiKey':key,
        'secret':secret,
        'enableRateLimit': True,
        'options': {
        'defaultType':'spot',
        'adjustForTimeDifference': True,
        'createMarketBuyOrderRequiresPrice':False,
        'test':True
        }
    })
     exchange.set_sandbox_mode(True)

    # Test if the API key and secret are correct
     try:
        balance = exchange.fetch_balance()
     except ccxt.AuthenticationError:
        pan.ajouterApiPage.message.setText("Incorrect API key or secret.")
        return
     except Exception as e:
        pan.ajouterApiPage.message.setText("An error occurred: "+str(e))
        print('An error occurred:'+ str(e))
        return

     if platformExist(platforme)==False:
          ajouterPlatforme(platforme)
     if apiExist(cin,key,platforme)==False:
         ajouterApiMethod(cin,key,secret,platforme)
     elif apiExist(cin,key,platforme)==True :
          modifierApiMethod(cin,key,secret,platforme)
     pan.ajouterApiPage.hide()
     pan.wellcomePage.show()