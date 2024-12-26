import pygame as pg

# Event Souris de 0-99
LEFTCLICK = 0
RIGHTCLICK = 1
MW_UP = 2
MW_DOWN = 3
# Event Clavier de 100-199
LEFT = 100
UP = 101
RIGHT = 102
DOWN = 103
RETURN = 104
BACKSPACE = 105 # Effets sur text
DELETE = 106
ESCAPE = 107
TAB = 108
CTRL_C = 109
CTRL_X = 110
CTRL_V = 111
CTRL_S = 112
CTRL_L = 113
CTRL_A = 114
CTRL_M = 115
CTRL_RIGHT = 116
CTRL_LEFT = 117
CTRL_UP = 118
CTRL_DOWN = 119
# Event Pygame Window de 200-299
QUIT = 200
# Event Text de 300-399
UPPER = 300
LOWER = 301
INSERT_HOUR = 302
INSERT_DATE = 303
BG = 304
FG = 305
CONSOLE = 306




class InputManager:
    def __init__(self):
        self.last_event = None
        self.REQUIRE_WAIT = [
            DOWN,
            UP,
            LEFT,
            RIGHT,
            RETURN,
            BACKSPACE,
            CTRL_C,
            CTRL_V,
            CTRL_X,
            CTRL_S,
            CTRL_L,
            CTRL_A,
            CTRL_M,
            CTRL_RIGHT,
            CTRL_LEFT,
            CTRL_UP,
            CTRL_DOWN,
            TAB
        ]
        self.mw_value = 0

    def get_pg_events(self):
        self.unicode_event = None
        self.is_only_unicode = False
        for event in pg.event.get():
            # Hiérarchie de event check

            # Fenêtre quittée
            # Molette haut/ bas
            # Clic droit pressé
            # Clic gauche pressé
            # Touche contrôle pressée (voire si d'autres touches sont pressées alors) : Important : Ctr+c, Ctr+v, Ctr+s / Optionnel : Ctr+A, Ctr+x, Ctr+z, Ctr+y
            # Touches directionnelles du curseur
            # Enter
            # Backspace
            # Touches à valeur unicode
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.MOUSEWHEEL:
                self.mw_value = abs(event.y)
                if event.y > 0:
                    return MW_UP
                if event.y < 0:
                    return MW_DOWN
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                return RIGHTCLICK
            if event.type == pg.KEYDOWN and event.unicode:
                self.unicode_event = event.unicode

        pressed_mouse = pg.mouse.get_pressed()
        if pressed_mouse[0]: # Le clic gauche peut drag, etc. Il est nécessaire de connaitre son état en continu
            return LEFTCLICK


        # On range les touches dans des ditionnaires/boucles pour ne pas avoir à répéter qu'on met l'event unicode à None si une touche plus important est pressée
        # Rappel : si l'event unicode n'est pas None, l'appli va écrire le nom de la touche (ex: "ctrl+s", "backspace", etc)
        keys = pg.key.get_pressed()
        crtl_keys = {
            pg.K_c: CTRL_C,
            pg.K_x: CTRL_X,
            pg.K_v: CTRL_V,
            pg.K_s: CTRL_S,
            pg.K_l: CTRL_L,
            pg.K_a: CTRL_A,
            pg.K_m: CTRL_M,
            pg.K_RIGHT: CTRL_RIGHT,
            pg.K_LEFT: CTRL_LEFT,
            pg.K_DOWN: CTRL_DOWN,
            pg.K_UP: CTRL_UP
        }
        if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:
            for crtl_key in crtl_keys:
                if not keys[crtl_key]:
                    continue
                self.unicode_event = None
                return crtl_keys[crtl_key]
            
        auxiliary_keys = {
            pg.K_ESCAPE: ESCAPE,
            pg.K_DOWN: DOWN,
            pg.K_UP: UP,
            pg.K_LEFT: LEFT,
            pg.K_RIGHT: RIGHT,
            pg.K_RETURN: RETURN,
            pg.K_BACKSPACE: BACKSPACE,
            pg.K_DELETE: DELETE,
            pg.K_TAB: TAB
        }
        for key in auxiliary_keys:
            if not keys[key]:
                continue
            self.unicode_event = None
            return auxiliary_keys[key]
        
        self.is_only_unicode = True
        return self.unicode_event
    
    def update_last_event(self, event_name):
        self.last_event = event_name

    def get_key_pressed():
        return pg.key.get_pressed()

    @staticmethod
    def get_mouse_pos():
        return pg.mouse.get_pos()
    
    @staticmethod
    def get_mouse_grid_pos(cell_dims):
        mousex, mousey = pg.mouse.get_pos()
        gridx = mousex // cell_dims[0]
        gridy = mousey // cell_dims[1]
        return gridx, gridy
    
    def set_last_event(self, event):
        self.last_event = event
