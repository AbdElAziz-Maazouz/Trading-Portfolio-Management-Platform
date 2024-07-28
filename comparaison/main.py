from PyQt5 import *
from PyQt5.QtWidgets import QApplication , QWidget,QLabel
import sys
from comparaison.ajouterData import *
from comparaison.controller import *

app = QApplication(sys.argv)
if __name__=='__main__':    
    pan = ajouterDataCompare()
    pan.figure.show()
    pan.show()
    sys.exit(app.exec_())
