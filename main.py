from tracemalloc import start
from PyQt5 import QtWidgets
import sys
import pygame
from pygame import color
from ColoringAlgos import ColoringAlgos
from graph import *
from view.MainWindow import MainWindow

from consts import *

import matplotlib.pyplot as plt
import plotly.subplots as ps
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.io as pio

def start_gui():
    pygame.font.init()
    
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    
    my_window=MainWindow()
    my_window.show()
    app.exec_()

def run_map():
    import usages.world_map.world_map as wm

    wm.load_us()
    wm.load_fr()
    
def run_schedule():
    import usages.schedule.schedule as sch

    sch.main_schedule()

if __name__ == "__main__":
    import usages.schedule.interface as ui
    # ui.main_inter()

    # Webhook test 4

    start_gui()