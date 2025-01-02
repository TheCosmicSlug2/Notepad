from pygame import Rect


class ScrollBar:
    def __init__(self, x: int, y: int, width: int, height: int, mode: str, settings):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_vertical = True if mode == "vertical" else False
        self.is_horizontal = True if mode == "horizontal" else False
        self.passive_color = (200, 200, 200)
        self.active_color = (100, 100, 100)
        self.clicked = False
        self.last_mouse_pos = None
        self.line_master = None
        self.settings = settings
    
    def in_bounds_x(self, posx: float) -> bool:
        return self.x <= posx <= self.x + self.width
    
    def in_bounds_y(self, posy: float) -> bool:
        return self.y <= posy <= self.y + self.height
    
    def in_bounds(self, posx: float, posy: float) -> bool:
        return self.in_bounds_x(posx) and self.in_bounds_y(posy)
    
    def check_mouse_collided(self, mouse_pos: tuple[int, int]) -> bool:
        mousex, mousey = mouse_pos
        return self.in_bounds(mousex, mousey)

    def set_scroll_pos(self, scroll: int, nb_lines: int) -> None:
        nb_lines_out_of_frame = max(0, nb_lines - self.settings.MAX_LINES)
        if nb_lines_out_of_frame == 0:
            self.y = 0
            return
        ratio = scroll / nb_lines_out_of_frame
        self.y = self.get_pos_with_ratio(ratio)

    
    def get_scroll(self, scroll: int, nb_lines: int, max_chars: int) -> tuple[int, int]:
        # La totalité de la longueur visible est de 0 à total-width ou total-height
        ratio = self.get_ratio()
        scrollx, scrolly = scroll
        # Get lines out of frame
        if self.is_vertical:
            nb_lines_out_of_frame = max(0, nb_lines - self.settings.MAX_LINES)
            scrolly = round(ratio * nb_lines_out_of_frame)
        if self.is_horizontal:
            max_chars_per_line = self.settings.SCREEN_DIMS[1] // self.settings.TEXT_FONT_WIDTH
            nb_chars_out_of_frame = max(0, max_chars - max_chars_per_line)
            scrollx = round(ratio * nb_chars_out_of_frame)
        return scrollx, scrolly
    
    def get_pos_with_ratio(self, ratio: float) -> float:
        screen_width, screen_height = self.settings.SCREEN_DIMS
        if self.is_vertical:
            return ratio * (screen_height - self.height)
        

    def get_ratio(self) -> float:
        screen_width, screen_height = self.settings.SCREEN_DIMS
        if self.is_vertical:
            ratio = self.y / (screen_height - self.height)
        if self.is_horizontal:
            ratio = self.x / (screen_width - self.width)
        return ratio

    def pos_update(self, dx: int, dy: int):
        if self.is_horizontal:
            self.x = min(max(0, self.x + dx), self.settings.SCREEN_DIMS[0] - self.width)
        if self.is_vertical:
            self.y = min(max(0, self.y + dy), self.settings.SCREEN_DIMS[1] - self.height)

    def get_rect(self) -> Rect:
        return Rect(self.x, self.y, self.width, self.height)

    def get_color(self) -> tuple[int, int, int]:
        if self.clicked:
            return self.active_color
        return self.passive_color
    

class WidgetMaster:
    def __init__(self, widgets_list: list):
        self.widgets = widgets_list
        self.focused_widget = None
        self.mouse_on_widget = False
    
    def update_y_bar(self, scroll: int, nb_lines: int) -> None:
        for widget in self.widgets:
            if not isinstance(widget, ScrollBar):
                continue
            if widget.is_vertical:
                widget.set_scroll_pos(scroll, nb_lines)

    
    def scrollbars_updates(self, mouse_pos: tuple[int, int], leftclick: bool) -> None: # TODO Rewrite with has_grabbed
        self.focused_widget = None
        self.mouse_on_widget = False
        for widget in self.widgets:
            if not isinstance(widget, ScrollBar):
                return
            widget_collided = widget.check_mouse_collided(mouse_pos)

            if not widget_collided:
                if not widget.clicked:
                    continue
                if widget.clicked or leftclick:
                    self.mouse_on_widget = True
                    self.focused_widget = widget
                else:
                    widget.clicked = False
                    self.focused_widget = None
                    continue
            
            self.mouse_on_widget = True
            if widget.clicked:
                dx = mouse_pos[0] - widget.last_mouse_pos[0]
                dy = mouse_pos[1] - widget.last_mouse_pos[1]
                widget.pos_update(dx, dy)
                self.focused_widget = widget
            elif leftclick:
                widget.clicked = True
                self.focused_widget = widget
            widget.last_mouse_pos = mouse_pos

    def update_button_status(self, mouse_pos: tuple[int, int], cell_dims: tuple[int, int]) -> None:
        mousex, mousey = mouse_pos
        gridx = mousex // cell_dims[0]
        gridy = mousey // cell_dims[1]
        hover_value = None
        for button in self.widgets:
            if button.gridx == gridx and button.gridy == gridy:
                button.state = 1
                hover_value = button.value
            else:
                button.state = 0
        return hover_value
            
    
    def reset_clicked(self) -> None:
        for widget in self.widgets:
            widget.clicked = False


class Button:
    def __init__(self, gridpos: tuple[int, int], dims: tuple[int, int], text: str, value):
        self.gridx, self.gridy = gridpos
        self.sizex, self.sizey = dims
        self.text = text
        self.value = value
        self.state = 0
    

    
