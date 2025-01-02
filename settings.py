from pygame import SYSTEM_CURSOR_IBEAM

class Settings:
    SCREEN_DIMS = (800, 600)
    FPS = 30

    MAX_LINES = 30
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    CURSOR_NATURE = SYSTEM_CURSOR_IBEAM

    SELECTION_COLOR = (0, 100, 255, 180)

    TEXT_FONT_NAME = "Courier"
    SPACE_BEETWEEN_LINES = 2
    TEXT_FONT_WIDTH = 11
    SMALL_FONT_NAME = "Consolas"
    SMALL_FONT_HEIGHT = 16
    text_left_margin = 5

    cmd_light_error = (255, 255, 0)
    cmd_error = (255, 0, 0)
