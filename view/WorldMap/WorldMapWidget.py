from PyQt5.QtWidgets import *
from consts import *
from PyQt5 import QtWebEngineWidgets
from graph import *
from view.WorldMap.WorldMapActionWidget import WorldMapActionWidget
from view.WorldMap.WorldMapBrowserWidget import WorldMapBrowserWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from consts import *
import pandas as pd
import json
import plotly.express as px
from ColoringAlgos import ColoringAlgos
from graph import *
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
import os
import plotly.offline as po

class WorldMapWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.browserWidget = WorldMapBrowserWidget(self)
        self.actionWidget = WorldMapActionWidget(self)
        
        self.layout.addWidget(self.browserWidget)
        self.layout.addWidget(self.actionWidget)
        
        self.setLayout(self.layout)