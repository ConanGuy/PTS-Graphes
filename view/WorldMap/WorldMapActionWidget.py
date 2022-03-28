from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from consts import *
from view.Graph.GraphGUI import VertexGUI
from options import Options

class WorldMapActionWidget(QtWidgets.QWidget):   

    def __init__(self, options, parent=None):
        super(WorldMapActionWidget,self).__init__(parent)
        self.options = options

        def centerUS():
            self.parent().browserWidget.fig.update_layout(mapbox={"zoom":3.3, "center":{"lat": 38.5517, "lon": -95.7073}})
            self.parent().browserWidget.save_fig()
            self.parent().browserWidget.show_graph()

        buttonCenterUS = QPushButton("Center US")
        buttonCenterUS.clicked.connect(centerUS)

            ########

        def centerFR():
            self.parent().browserWidget.fig.update_layout(mapbox={"zoom":4.7, "center":{"lat": 46.8517, "lon": 1.7073}})
            self.parent().browserWidget.save_fig()
            self.parent().browserWidget.show_graph()

        buttonCenterFR = QPushButton("Center FR")
        buttonCenterFR.clicked.connect(centerFR)

            ########
            
        self.setMaximumHeight(50)

        gLayout = QGridLayout()
        gLayout.addWidget(buttonCenterFR, 0, 0)
        gLayout.addWidget(buttonCenterUS, 0, 1)
        self.setLayout(gLayout)
