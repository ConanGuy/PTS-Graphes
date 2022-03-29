import math
import random

from consts import *
from graph import VerticesList, generate_random_graph

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from view.Graph.GraphGUI import GraphGUI, VertexGUI
from options import Options
from view.Comparison.ComparisonSurfaceWidget import ComparisonSurfaceWidget
from view.Comparison.ComparisonActionWidget import ComparisonActionWidget
from ColoringAlgos import ALGO_FCTS, ColoringAlgos, VerifAlgos
from view.Graph.GraphFormWidget import RandomizerForm
from PyQt5 import QtCore

class ComparisonWidget(QWidget):

    def __init__(self, parent=None, graph=None):
        super(ComparisonWidget,self).__init__(parent)

        self.options = Options()
        self.options.POINTS_RADIUS /= 2
        self.options.N_VERTICES_RANDGRAPH = 10
        
        self.graph = generate_random_graph("NEIGHBORS_AMOUNT", self.options.N_VERTICES_RANDGRAPH, self.options.NEIGHBORS_INTERVAL[0], self.options.NEIGHBORS_INTERVAL[1]) if graph is None else graph
        self.init_graph_points()
        
        layout = QGridLayout()
        self.pygameWidgets = [] 
        for i, algo in enumerate(ALGO_FCTS.keys()):
            self.pygameWidgets.append(ComparisonSurfaceWidget(self.graph.copy(), algo, self.options, self))
            layout.addWidget(self.pygameWidgets[i], i//2, i%2)       
            
        self.actionWidget = ComparisonActionWidget(self.options, self) 
        self.randomWidget = RandomizerForm(self.options, self)
        layout.addWidget(self.randomWidget, 0, 2, 1, 1)
        layout.addWidget(self.actionWidget, 1, 2, 1, 1)

        #######################################   

        self.setLayout(layout)
        
    def init_graph_points(self):
        self.graph = GraphGUI.generate(self.graph, self.set_points())

    def set_points(self):
        graph = self.graph

        n = len(graph.keys())
        shift = 20
        w = WIDTH/3-shift*2
        h = HEIGHT/3-shift*2

        pointSpace = (w*h)/n
        length = math.sqrt(pointSpace)
        
        points = {vertex: None for vertex in graph}

        wn = math.ceil(w/length)
        hn = math.ceil(n/wn)
        
        rand = self.options.POINTS_DISTANCE_RANDOMNESS
        k=0
        for i in range(wn):
            for j in range(hn):
                x = (w-(wn-1)*length)/2+shift+i*length+((random.uniform(0,length)-length/2)*rand)
                y = (h-(hn-1)*length)/2+shift+j*length+((random.uniform(0,length)-length/2)*rand)

                try:
                    vertex = list(graph.keys())[k]
                    p = VertexGUI(x, y, vertex=vertex)
                    points[vertex] = p
                except:
                    pass

                k += 1

        def ccw(A,B,C):
            return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        bestPos = [math.inf, {}]
        lastPos = [math.inf, {}]
        for p in range(self.options.POINTS_POSITIONING_ITERATIONS):
            edges = list(set([tuple(sorted([points[vertex], points[neighbor]])) for vertex in graph for neighbor in graph[vertex]]))
            
            intersections = {vertex: 0 for vertex in graph}
            for i in range(len(edges)):
                for j in range(i+1, len(edges)):
                    A, B = edges[i][0], edges[i][1]
                    C, D = edges[j][0], edges[j][1]
                    if A not in [C, D] and B not in [C, D]:
                        if intersect(A,B,C,D):
                            intersections[A] += 1
                            intersections[B] += 1
                            intersections[C] += 1
                            intersections[D] += 1
            
            curPos = [sum(intersections.values())/4, {vertex: points[vertex].pos for vertex in graph}]
            
            if lastPos[0] < curPos[0]:
                curPos = lastPos
            else:
                lastPos = curPos
            
            if bestPos[0] > curPos[0] or bestPos[0] == -1:
                bestPos = curPos

            ordered = sorted(intersections, key=intersections.get, reverse=True)
            if intersections[ordered[0]] == 0: return points
            
            fi, se= ordered[0], random.choice([v for v in ordered if intersections[v] != 0])
            points[fi].pos, points[se].pos = points[se].pos, points[fi].pos

            if bestPos[0] == 0:
                break

        for vertex, pos in bestPos[1].items():
            points[vertex].pos = pos

        pointsV = VerticesList()
        for p in points.values():
            pointsV.add(p)

        return points
    
class RandomizerForm(QTabWidget):

    def __init__(self, options, parent=None) -> None:
        super(RandomizerForm,self).__init__(parent)
        self.options = options

        self.nverticesNeiEdit = QSpinBox()
        self.nverticesNeiEdit.setAlignment(QtCore.Qt.AlignRight)
        self.nverticesNeiEdit.setValue(self.options.N_VERTICES_RANDGRAPH)
        self.nverticesNeiEdit.setMinimum(4)
        self.nverticesNeiEdit.setMaximum(100)

        self.nverticesDelEdit = QSpinBox()
        self.nverticesDelEdit.setAlignment(QtCore.Qt.AlignRight)
        self.nverticesDelEdit.setValue(self.options.N_VERTICES_RANDGRAPH)
        self.nverticesDelEdit.setMinimum(4)
        self.nverticesDelEdit.setMaximum(100)

        self.minEdgeEdit = QSpinBox()
        self.minEdgeEdit.setAlignment(QtCore.Qt.AlignRight)
        self.minEdgeEdit.setValue(self.options.NEIGHBORS_INTERVAL[0])
        self.minEdgeEdit.setMinimum(self.options.NEIGHBORS_INTERVAL[0])
        self.minEdgeEdit.setMaximum(self.options.NEIGHBORS_INTERVAL[1])

        self.maxEdgeEdit = QSpinBox()
        self.maxEdgeEdit.setAlignment(QtCore.Qt.AlignRight)
        self.maxEdgeEdit.setValue(self.options.NEIGHBORS_INTERVAL[1])
        self.maxEdgeEdit.setMinimum(2)
        self.maxEdgeEdit.setMaximum(self.options.NEIGHBORS_INTERVAL[1])

        self.probaEdit = QSlider(QtCore.Qt.Horizontal)
        self.probaEdit.setValue(self.options.DELETE_PROBABILITY*100)
        self.probaEdit.setMinimum(0)
        self.probaEdit.setMaximum(100)

        self.buttonRandomGraphNei = QPushButton("New graph")
        self.buttonRandomGraphDel = QPushButton("New graph")
            
        #########

        neiLayout = QFormLayout()
        neiLayout.addRow("Vertices amount: ", self.nverticesNeiEdit)
        neiLayout.addRow("Min edge amount: ", self.minEdgeEdit)
        neiLayout.addRow("Max edge amount: ", self.maxEdgeEdit)
        neiLayout.addWidget(self.buttonRandomGraphNei)
        
        delLayout = QFormLayout()
        delLayout.addRow("Vertices amount: ", self.nverticesDelEdit)
        delLayout.addRow(f"Deletion probability ({self.probaEdit.value()}%): ", self.probaEdit)
        delLayout.addWidget(self.buttonRandomGraphDel)

        #########

        def changeVerticesAmountNei():
            self.options.N_VERTICES_RANDGRAPH = self.nverticesNeiEdit.value()
            self.nverticesDelEdit.setValue(self.nverticesNeiEdit.value())
            if self.maxEdgeEdit.value() >= self.nverticesNeiEdit.value():
                self.maxEdgeEdit.setValue(self.nverticesNeiEdit.value()-1) 
            self.maxEdgeEdit.setMaximum(self.nverticesNeiEdit.value()-1)

        def changeVerticesAmountDel():
            self.options.N_VERTICES_RANDGRAPH = self.nverticesDelEdit.value()
            self.nverticesNeiEdit.setValue(self.nverticesDelEdit.value())
            if self.maxEdgeEdit.value() >= self.nverticesDelEdit.value():
                self.maxEdgeEdit.setValue(self.nverticesDelEdit.value()-1) 
            self.maxEdgeEdit.setMaximum(self.nverticesNeiEdit.value()-1)
        
        def changeMinEdge():
            self.options.NEIGHBORS_INTERVAL[0] = self.minEdgeEdit.value()
            self.maxEdgeEdit.setMinimum(self.options.NEIGHBORS_INTERVAL[0])
        
        def changeMaxEdge():
            self.options.NEIGHBORS_INTERVAL[1] = self.maxEdgeEdit.value()
            self.minEdgeEdit.setMaximum(self.options.NEIGHBORS_INTERVAL[1]) 

        def randomGraphNei():
            ColoringAlgos.coloredLimit = 0
            
            self.parent().graph = generate_random_graph("NEIGHBORS_AMOUNT", self.options.N_VERTICES_RANDGRAPH, self.options.NEIGHBORS_INTERVAL[0], self.options.NEIGHBORS_INTERVAL[1])
            self.parent().init_graph_points()
            
            for widget in self.parent().pygameWidgets:
                widget.set_graph(self.parent().graph.copy())
                widget.repaint()

        def randomGraphDel():
            ColoringAlgos.coloredLimit = 0
            
            self.parent().graph = generate_random_graph("DELETE_PROBABILITY", self.options.N_VERTICES_RANDGRAPH, self.options.DELETE_PROBABILITY)
            self.parent().init_graph_points()
            
            for widget in self.parent().pygameWidgets:
                widget.set_graph(self.parent().graph.copy())
                widget.repaint()

        def changeProba():
            delLayout.labelForField(self.probaEdit).setText(f"Deletion probability ({self.probaEdit.value()}%): ")
            self.options.DELETE_PROBABILITY = self.probaEdit.value() / 100 

        #########

        self.nverticesNeiEdit.valueChanged.connect(changeVerticesAmountNei)   
        self.nverticesDelEdit.valueChanged.connect(changeVerticesAmountDel)   
        self.minEdgeEdit.valueChanged.connect(changeMinEdge)   
        self.maxEdgeEdit.valueChanged.connect(changeMaxEdge)
        self.probaEdit.valueChanged.connect(changeProba)
        self.buttonRandomGraphNei.clicked.connect(randomGraphNei)
        self.buttonRandomGraphDel.clicked.connect(randomGraphDel)

        delLayout.labelForField(self.probaEdit).setFixedWidth(delLayout.labelForField(self.probaEdit).sizeHint().width())

        #########

        rNF = QWidget()
        rDF = QWidget()

        rNF.setLayout(neiLayout)
        rDF.setLayout(delLayout)

        self.addTab(rNF,"Neighbors")
        self.addTab(rDF,"Delete")
