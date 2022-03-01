from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from view.MainWidget import MainWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.mainWidget = MainWidget(self)
        self.pos

        self.setCentralWidget(self.mainWidget)