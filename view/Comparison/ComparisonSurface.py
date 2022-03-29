from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pygame

from consts import *
from view.Graph.GraphGUI import VertexGUI
from options import Options

class ComparisonSurface(QtWidgets.QWidget):   
    def __init__(self, graph, algo, options, parent=None):
        super(ComparisonSurface,self).__init__(parent)
        self.surface = pygame.Surface((WIDTH/3, HEIGHT/3))
        self.options = options
        self.graph = graph
        self.algo = algo

        self.image=QtGui.QImage("usages/world_map/fr_departements/colored_fr.png") 

        self.setFixedSize(self.surface.get_width(), self.surface.get_height())

        self.selected = None
        self.action = None
        self.actionParams = []
        self.actionStep = 0

    def draw(self):
        self.surface.fill(NONE_COLOR)
        
        for edge in self.graph.edges:
            pygame.draw.line(self.surface, (255,255,255), edge[0].pos, edge[1].pos, 1)

        for vertex in self.graph.vertices:
            bordercol = (0,255,0) if vertex == self.selected else vertex.border
            if self.action == "addEdge" and vertex in self.actionParams:
                bordercol = (0,0,255)
            elif self.action == "delEdge" and vertex in self.actionParams:
                bordercol = (255,0,0)

            pygame.draw.circle(self.surface, bordercol, vertex.pos, self.options.POINTS_RADIUS, 0)
            pygame.draw.circle(self.surface, vertex.color, vertex.pos, self.options.POINTS_RADIUS-1, 0)

            font = pygame.font.Font(None, int(self.options.POINTS_RADIUS*1.5))
            text = font.render(vertex.name, True, (255,255,255))
            text_rect = text.get_rect(center=vertex.pos)
            self.surface.blit(text, text_rect)
    
        if self.action:
            font = pygame.font.Font(None, 34)
            text = font.render(self.action+" (step "+str(self.actionStep)+")", True, (255,0,0,155))
            text_rect = text.get_rect()
            self.surface.blit(text, (10,10))

    def paintEvent(self, event):
        self.draw()
        
        w=self.surface.get_width()
        h=self.surface.get_height()
        data=self.surface.get_buffer().raw
        self.image=QtGui.QImage(data,w,h,QtGui.QImage.Format_RGB32)
        #self.image=QtGui.QImage("usages/world_map/fr_departements/colored_fr.png") 

        self.setFixedSize(self.image.width(), self.image.height())

        my_paint=QtGui.QPainter()  
        my_paint.begin(self)
        my_paint.drawImage(0,0,self.image)
        my_paint.end()

    def mousePressEvent(self, QMouseEvent):

        modifiers = QApplication.keyboardModifiers()
        if self.action == None:
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            for vertex in self.graph.vertices:
                center_x, center_y = vertex.x, vertex.y
                if (x - center_x)**2 + (y - center_y)**2 < self.options.POINTS_RADIUS**2:
                    self.selected = vertex

            self.repaint()

    def mouseMoveEvent(self, QMouseEvent) -> None:
        if self.selected:
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            for widget in self.parent().parent().pygameWidgets:
                v = widget.graph.vertices[self.selected.id]
                v.pos = (x,y)
                widget.repaint()

    def mouseReleaseEvent(self, QMouseEvent):
        self.selected = None
        self.repaint()
