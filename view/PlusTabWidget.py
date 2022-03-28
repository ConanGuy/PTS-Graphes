from PyQt5.QtWidgets import *

from view.Graph.GraphWidget import GraphWidget
from view.WorldMap.WorldMapWidget import WorldMapWidget
from view.Schedule.ScheduleWidget import ScheduleWidget

class PlusTabWidget(QWidget):

    def __init__(self, parent=None) -> None:
        super(PlusTabWidget,self).__init__(parent)

        self.layout = QGridLayout(self)

        self.btnGraph = QPushButton("")
        self.btnMap = QPushButton("")
        self.btnSchedule = QPushButton("")
        self.btnSudoku = QPushButton("New Comparison Tab")

        self.btnGraph.clicked.connect(lambda: self.add_tab(GraphWidget(self.parent()), "Graph"))
        self.btnMap.clicked.connect(lambda: self.add_tab(WorldMapWidget(self.parent()), "World Map"))
        self.btnSchedule.clicked.connect(lambda: self.add_tab(ScheduleWidget(self.parent()), "Schedule"))

        self.btnGraph.setStyleSheet("background-image : url(res/imgs/GraphWidget.png);")
        self.btnGraph.setFixedSize(640, 360)
        self.btnMap.setStyleSheet("background-image : url(res/imgs/WorldMapWidget.png);")
        self.btnMap.setFixedSize(640, 360)
        self.btnSchedule.setStyleSheet("background-image : url(res/imgs/ScheduleWidget.png);")
        self.btnSchedule.setFixedSize(640, 360)

        self.layout.addWidget(self.btnGraph, 0, 0)
        self.layout.addWidget(self.btnMap, 0, 1)
        self.layout.addWidget(self.btnSchedule, 1, 0)
        self.layout.addWidget(self.btnSudoku, 1, 1)

        self.setLayout(self.layout)

    def add_tab(self, widget, title):
        self.parent().parent().parent().add_tab(widget, title)