import math
import random

from consts import *
from graph import VerticesList, generate_random_graph

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from view.Graph.GraphGUI import GraphGUI, VertexGUI
from options import Options
from view.Schedule.ScheduleSurfaceWidget import ScheduleSurfaceWidget
from view.Schedule.ScheduleActionWidget import ScheduleActionWidget
import view.Schedule.Schedule as sch

class ScheduleWidget(QWidget):

    def __init__(self, parent=None, graph=None):
        super(ScheduleWidget,self).__init__(parent)

        self.schedule = sch.main_schedule()
        self.currentClass = 0
        
        self.options = Options()
        
        self.pygameWidget = ScheduleSurfaceWidget(self.options, self)
        self.actionWidget = ScheduleActionWidget(self.options, self)

        #######################################

        layout = QGridLayout()        
        layout.addWidget(self.pygameWidget, 0, 0, 1, 1)
        layout.addWidget(self.actionWidget, 1, 0)       

        self.setLayout(layout)