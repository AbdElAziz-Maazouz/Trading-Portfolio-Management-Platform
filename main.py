
import sys
from PyQt5.QtWidgets import QApplication
from MyApplication import MyApplicationPan
import ctypes
import sys
import requests
import win32api
from datetime import datetime


def run_as_admin(argv=None, debug=False):
    if argv is None:
        argv = sys.argv
    # Prompt the user to run as administrator
    params = '/k ' + ' '.join(argv)
    if debug:
        print(params)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)


if __name__=='__main__':
   run_as_admin()
   app = QApplication(sys.argv)
   pan = MyApplicationPan()
   pan.show()
   sys.exit(app.exec_())