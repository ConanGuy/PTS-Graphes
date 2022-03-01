from PyQt5.QtWidgets import *

from view.Graph.GraphWidget import GraphWidget

class PlusTabWidget(QWidget):

    def __init__(self, parent=None) -> None:
        super(PlusTabWidget,self).__init__(parent)

        self.layout = QGridLayout(self)

        self.btnGraph = QPushButton("New Graph Tab")
        self.btnMap = QPushButton("New Map Tab")
        self.btnSchedule = QPushButton("New Schedule Tab")
        self.btnSudoku = QPushButton("New Sudoku Tab")

        self.btnGraph.clicked.connect(lambda: self.add_tab(GraphWidget(self.parent()), "Graph"))

        self.layout.addWidget(self.btnGraph, 0, 0)
        self.layout.addWidget(self.btnMap, 0, 1)
        self.layout.addWidget(self.btnSchedule, 1, 0)
        self.layout.addWidget(self.btnSudoku, 1, 1)

        self.setLayout(self.layout)

    def add_tab(self, widget, title):
        self.parent().parent().parent().add_tab(widget, title)