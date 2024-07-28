
from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from os import path


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"signin.ui"))

class signinPan(QtWidgets.QWidget,FORM_CLASS):
    def __init__(self,parent=None):
        super(signinPan,self).__init__(parent)
        self.setupUi(self)
        self.nom.setText("username")
        self.prenom.setText("userlastname")
        self.telephone.setText("0610934468")
        self.mail.setText("usermail@gmail.com")
        self.cin.setText("CD617699")
        self.password.setText("password1")
        self.confirm.setText("password1")


