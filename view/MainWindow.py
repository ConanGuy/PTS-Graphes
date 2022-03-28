from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from view.MainWidget import MainWidget
from view.WorldMap.WorldMapBrowserWidget import WorldMapBrowserWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.mainWidget = MainWidget(self)

        self.setCentralWidget(self.mainWidget)