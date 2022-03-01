import pygame as pg
from consts import *

class ScheduleSurface(pg.Surface):

    def __init__(self, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
