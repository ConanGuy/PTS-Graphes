from PyQt5.QtWidgets import *

from view.Graph.GraphWidget import GraphWidget
from view.PlusTabWidget import PlusTabWidget

class MainWidget(QWidget):
    
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab_handler)

        self.plusTabWidget = PlusTabWidget(self)

        self.tabs.addTab(GraphWidget(self), "Graph 1")
        self.tabs.addTab(self.plusTabWidget, "+")

        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def add_tab(self, widget, title):
        self.tabs.insertTab(len(self.tabs)-1, widget, title)

    def close_tab_handler(self, index):
        self.tabs.removeTab(index)