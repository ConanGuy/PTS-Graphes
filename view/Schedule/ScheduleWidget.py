import math
import random

from consts import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from options import Options
from view.Schedule.ScheduleSurfaceWidget import ScheduleSurfaceWidget

class ScheduleWidget(QWidget):

    def __init__(self, parent=None):
        super(ScheduleWidget,self).__init__(parent)

        self.options = Options()
        
        self.pygameWidget = ScheduleSurfaceWidget(self.options, self)

        #######################################

        layout = QGridLayout()        
        layout.addWidget(self.pygameWidget, 0, 0, 1, 1)       

        self.setLayout(layout)