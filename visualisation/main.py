from PyQt5 import *
from PyQt5.QtWidgets import QApplication , QWidget,QLabel
import sys


from visualisation.ajouterData import *
from visualisation.controllerOfVisu import *


app = QApplication(sys.argv)
if __name__=='__main__':    
    pan = ajouterData()
    pan.figure.show()
    pan.show()
    sys.exit(app.exec_())
