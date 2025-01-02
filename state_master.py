from time import time

class StateMaster:
    def __init__(self, settings):
        self.duration = 0.5
        self.last_key_event = None
        self.timer = time()
        self.settings = settings
        self.fps_counter = 0

    def set_last_event(self, event):
        self.last_key_event = event
    
    def check_is_key_accessible(self, event):
        # La touche actuelle n'a aucun rapport avec la touche précédente
        if event != self.last_key_event:
            self.timer = time() # Remettre à 0 le timer pour la touche
            return True
        if time() - self.timer < self.duration:
            return False
        return True
    
    def update_last_event(self, event):
        self.last_key_event = event


    def update(self):
        self.key_timer = time()
    
    def update_fps_counter(self):
        self.fps_counter += 1
        self.fps_counter %= self.settings.FPS
        
    def check_cursor_visible(self):
        if self.fps_counter < self.settings.FPS / 2:
            return True
        return False
