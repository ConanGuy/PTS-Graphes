import time
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from consts import *
from view.Graph.GraphGUI import VertexGUI
from options import Options
from ColoringAlgos import ALGO_FCTS, ColoringAlgos, VerifAlgos
import threading

class ComparisonActionWidget(QtWidgets.QWidget):   
    def __init__(self, options, parent=None):
        super(ComparisonActionWidget,self).__init__(parent)
        self.options = options

        def colorGraphs():
            def colorWidget(widget):
                    algo = widget.algo        
                    ColoringAlgos.coloredLimit = len(self.parent().graph.vertices)

                    widget.graph.reset_colors()
                    eval("ColoringAlgos."+ALGO_FCTS[algo])(widget.graph)

                    widget.repaint()
            
            for widget in self.parent().pygameWidgets:
                t0 = time.time()
                colorWidget(widget)
                t1 = time.time()
                tms = round((t1-t0)*1000, 3)
                widget.label.setText(widget.algo+": "+str(tms)+"ms")

        buttonColor = QPushButton("Color")
        buttonColor.clicked.connect(colorGraphs)

            ########
            
        gLayout = QGridLayout()
        gLayout.addWidget(buttonColor, 0, 0)
        self.setLayout(gLayout)
