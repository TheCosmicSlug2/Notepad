from settings import *
from widget import WidgetMaster, Button
from input_manager import *
import pygame as pg
from input_manager import *


DEF_button_dims = (220, 50)
rightclick_buttons = [
    Button((0, 0), DEF_button_dims, "Copier", CTRL_C),
    Button((0, 1), DEF_button_dims, "Couper", CTRL_X),
    Button((0, 2), DEF_button_dims, "Coller", CTRL_V),
    Button((0, 3), DEF_button_dims, "Selectionner Tout", CTRL_A),
    Button((0, 5), DEF_button_dims, "Majusculer", UPPER),
    Button((0, 6), DEF_button_dims, "Minusculer", LOWER),
    Button((0, 7), DEF_button_dims, "Arrière-Plan", BG),
    Button((0, 8), DEF_button_dims, "Texte", FG),
    Button((2, 0), DEF_button_dims, "Insérer Heure", INSERT_HOUR),
    Button((2, 1), DEF_button_dims, "Insérer Date", INSERT_DATE),
    Button((2, 3), DEF_button_dims, "Sauvegarder", CTRL_S),
    Button((2, 4), DEF_button_dims, "Ouvrir", CTRL_L),
    Button((2, 5), DEF_button_dims, "Console", CONSOLE),
]
color_buttons = [
]

class RightClickAction:
    def __init__(self, renderer, cursor):
        self.renderer = renderer
        self.input_master = InputManager()
        self.cursor = cursor
        self.widget_manager = WidgetMaster(rightclick_buttons)
        self.button_dims = DEF_button_dims
        self.action = None
        
    def mainloop(self) -> None:
        self.renderer.fill_screen((255,255,255))
        self.renderer.set_mouse_nature(pg.SYSTEM_CURSOR_ARROW)
        rightclick_running = True
        last_event = None
        while rightclick_running:
            current_hover_value = self.widget_manager.update_button_status(self.input_master.get_mouse_pos(), self.button_dims)
            event = self.input_master.get_pg_events()
            if event == LEFTCLICK:
                self.action = current_hover_value
                rightclick_running = False
            elif event == RIGHTCLICK and last_event != RIGHTCLICK:
                rightclick_running = False

            last_event = event
            self.renderer.show_buttons(self.widget_manager.widgets, self.button_dims)
            self.renderer.update()
        self.renderer.set_mouse_nature(pg.SYSTEM_CURSOR_IBEAM)