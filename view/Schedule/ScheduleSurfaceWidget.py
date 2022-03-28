from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from graph import Vertex
import pygame

from consts import *
from view.Graph.GraphGUI import VertexGUI
from options import Options

class ScheduleSurfaceWidget(QtWidgets.QWidget):   
    def __init__(self, options, parent=None):
        super(ScheduleSurfaceWidget,self).__init__(parent)

        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.options = options

        self.image=QtGui.QImage() 

        self.setFixedSize(self.surface.get_width(), self.surface.get_height())
        
        self.schedule = self.parent().schedule

    def draw(self):
        startHour = 8
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        subColors = {
            "Maths": "royalblue",
            "Français": "indianred",
            "Hist/Géo": "darkturquoise",
            "EPS": "gainsboro",
            "Anglais": "darkorange1",
            "LV2": "deeppink3",
            "Sciences": "forestgreen"}
        dayIdx = self.parent().currentClass
        
        shift = 0.1
        borderLen = 1
        startX = WIDTH*shift
        startY = HEIGHT*shift-10
        
        diary = self.schedule.all_diaries[list(self.schedule.all_diaries.keys())[dayIdx]]
        
        nbDays = len(diary)
        nbHours = len(diary[0])
        widthDay = int(((WIDTH - WIDTH*shift*2) - (nbDays+1)*borderLen)/nbDays)
        heightHour = int(((HEIGHT - HEIGHT*shift*2) - (nbHours+1)*borderLen)/nbHours)
        
        self.surface.fill(NONE_COLOR)

        x = startX
        for idx, day in enumerate(diary):
            y = startY

            font = pygame.font.Font(None, 26)
            text = font.render(days[idx], True, "white")
            text_rect = text.get_rect(center=pygame.Rect(x, y-(borderLen*2+heightHour) , borderLen*2+widthDay, borderLen*2+heightHour).center)
            self.surface.blit(text, text_rect)

            for idy, hour in enumerate(day):

                if idx == 0 and idy%2 == 0 :
                    font = pygame.font.Font(None, 18)
                    text = font.render(str(int(startHour+idy/2))+"H00", True, "white")
                    text_rect = text.get_rect(center=pygame.Rect(x-(widthDay/3)+5, y-heightHour/2, widthDay/3, borderLen*2+heightHour).center)
                    self.surface.blit(text, text_rect)

                sameCourse = False
                if idy > 0:
                    if isinstance(day[idy], Vertex) and isinstance(day[idy-1], Vertex):
                        sameCourse = (day[idy].value.subject == day[idy-1].value.subject)
                    if isinstance(day[idy], str) and isinstance(day[idy-1], str):
                        sameCourse = day[idy] == day[idy-1]
                    if day[idy] is None and day[idy-1] is None:
                        sameCourse = day[idy] == day[idy-1]
                pygame.draw.rect(self.surface, "black", (x, y+(borderLen if sameCourse else 0), borderLen*2+widthDay, borderLen*2+heightHour-(borderLen if sameCourse else 0)))

                
                s = "" if hour is None else "Pause"
                c = "gray32" if hour is None else "gold"
                if isinstance(hour, Vertex):
                    s = hour.value.subject+" - "+hour.value.prof
                    c = subColors[hour.value.subject]

                    font = pygame.font.Font(None, 36)
                    text = font.render(hour.value.group.name, True, "white")
                    text_rect = text.get_rect(center=pygame.Rect(startX, startY+borderLen*(nbHours+1)+heightHour*nbHours+30, borderLen*(nbDays+1)+widthDay*nbDays, heightHour).center)
                    self.surface.blit(text, text_rect)

                pygame.draw.rect(self.surface, c, (x+borderLen, y+(borderLen if not sameCourse else 0), widthDay, heightHour+(0 if not sameCourse else borderLen)))
                
                r = pygame.Rect(x+borderLen, y+borderLen, widthDay, heightHour)

                font = pygame.font.Font(None, 14)
                text = font.render(s, True, "black")
                text_rect = text.get_rect(center=r.center)
                self.surface.blit(text, text_rect)
                
                y += heightHour+borderLen

            x += borderLen+widthDay


    def paintEvent(self, event):
        self.draw()
        
        w=self.surface.get_width()
        h=self.surface.get_height()
        data=self.surface.get_buffer().raw
        self.image=QtGui.QImage(data,w,h,QtGui.QImage.Format_RGB32)

        self.setFixedSize(self.image.width(), self.image.height())

        my_paint=QtGui.QPainter()  
        my_paint.begin(self)
        my_paint.drawImage(0,0,self.image)
        my_paint.end()