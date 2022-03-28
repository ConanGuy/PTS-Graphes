from PyQt5.QtWidgets import *

from view.Graph.GraphWidget import GraphWidget
from view.PlusTabWidget import PlusTabWidget
from view.WorldMap.WorldMapWidget import WorldMapWidget

class MainWidget(QWidget):
    
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab_handler)

        self.plusTabWidget = PlusTabWidget(self)

        self.tabs.addTab(GraphWidget(self), "Graph")
        self.tabs.addTab(self.plusTabWidget, "+")

        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def add_tab(self, widget, title):
        self.tabs.insertTab(self.tabs.currentIndex(), widget, title)
        self.tabs.setCurrentIndex(self.tabs.currentIndex()-1)

    def close_tab_handler(self, index):
        self.tabs.removeTab(index)