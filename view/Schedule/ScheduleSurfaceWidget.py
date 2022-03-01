import pygame as pg
from consts import *

class ScheduleSurfaceWidget(pg.Surface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
