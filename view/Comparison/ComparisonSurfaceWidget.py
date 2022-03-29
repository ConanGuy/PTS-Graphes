from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from consts import *
from view.Comparison.ComparisonSurface import ComparisonSurface
from options import Options
from ColoringAlgos import ALGO_FCTS, ColoringAlgos, VerifAlgos
import threading

class ComparisonSurfaceWidget(QtWidgets.QWidget): 
    
    def __init__(self, graph, algo, options, parent=None):
        super(ComparisonSurfaceWidget,self).__init__(parent)
        self.options = options
        self.graph = graph
        self.algo = algo
        
        self.surfaceWidget = ComparisonSurface(self.graph, self.algo, self.options, self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.algo)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.surfaceWidget)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        
    def set_graph(self, graph):
        self.graph = graph
        self.surfaceWidget.graph = self.graph