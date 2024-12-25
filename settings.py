import pygame as pg


class Settings:
    def __init__(self):
        self.SCREEN_DIMS = (800, 600)
        self.FPS = 30

        self.MAX_LINES = 30
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)

        self.CURSOR_NATURE = pg.SYSTEM_CURSOR_IBEAM

        self.SELECTION_COLOR = (0, 100, 255, 180)

        self.TEXT_FONT_NAME = "Courier"
        self.SPACE_BEETWEEN_LINES = 2
        self.TEXT_FONT_WIDTH = 11
        self.SMALL_FONT_NAME = "Consolas"
        self.SMALL_FONT_HEIGHT = 16
        self.text_left_margin = 5