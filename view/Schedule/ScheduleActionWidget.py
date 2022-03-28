from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from consts import *
from view.Graph.GraphGUI import VertexGUI
import view.Schedule.Schedule as sch
from view.Graph.GraphWidget import GraphWidget

class ScheduleActionWidget(QtWidgets.QWidget):   
    def __init__(self, options, parent=None):
        super(ScheduleActionWidget,self).__init__(parent)
        self.options = options

            ########

        def nextGroup():
            self.parent().currentClass += 1
            self.parent().currentClass %= len(self.parent().schedule.all_diaries)
            self.parent().pygameWidget.repaint()

        buttonNextGroup = QPushButton(">")
        buttonNextGroup.clicked.connect(nextGroup)

            ########

        def prevGroup():
            self.parent().currentClass -= 1
            if self.parent().currentClass < 0: self.parent().currentClass = len(self.parent().schedule.all_diaries)
            self.parent().pygameWidget.repaint()

        buttonPrevGroup = QPushButton("<")
        buttonPrevGroup.clicked.connect(prevGroup)

            ########

        def reloladSchedule():
            self.parent().currentClass = 0
            self.parent().schedule = sch.main_schedule() 
            self.parent().pygameWidget.repaint()

        buttonReload = QPushButton("Reload Schedule")
        buttonReload.clicked.connect(reloladSchedule)

            ########
            
        self.setMaximumHeight(50)

        gLayout = QGridLayout()
        gLayout.addWidget(buttonPrevGroup, 0, 0)
        gLayout.addWidget(buttonReload, 0, 1)
        gLayout.addWidget(buttonNextGroup, 0, 2)
        self.setLayout(gLayout)