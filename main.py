from PyQt5 import QtWidgets
import sys
import pygame
from graph import *
from view.MainWindow import MainWindow

from consts import *

def start_gui():
    pygame.font.init()
    
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    
    my_window=MainWindow()
    my_window.show()
    app.exec_()

if __name__ == "__main__":
    start_gui()