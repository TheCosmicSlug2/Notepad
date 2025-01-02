from settings import Settings
import pygame as pg


class Renderer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.SCREEN = pg.display.set_mode(self.settings.SCREEN_DIMS)
        pg.display.set_caption("Python notepad")
        self.clock = pg.time.Clock()

        self.passive_button_color = (200, 200, 200)
        self.active_button_color = (220, 220, 220)
        self.scrolly = 0
        self.scrollx = 0

        self.cursor_sprite = pg.cursors.Cursor(self.settings.CURSOR_NATURE)
        pg.mouse.set_cursor(self.cursor_sprite)

        pg.font.init()
        self.small_font = pg.font.SysFont(self.settings.SMALL_FONT_NAME, self.settings.SMALL_FONT_HEIGHT)

        self.space_beetween_lines = self.settings.SPACE_BEETWEEN_LINES
        self.font_width = self.settings.TEXT_FONT_WIDTH
        self.text_font_height = self.settings.SCREEN_DIMS[1] // self.settings.MAX_LINES - self.space_beetween_lines # -1 pour pouvoir après laisser plus d'espace entre les lignes
        self.line_height = self.text_font_height + self.space_beetween_lines
        self.text_font = pg.font.SysFont(self.settings.TEXT_FONT_NAME, self.text_font_height)
        self.line_manager = None

        self.cmd_font = pg.font.SysFont("Consolas", self.text_font_height)

        self.doc_style = {
            "bg": self.settings.WHITE,
            "line": self.settings.WHITE,
            "text": self.settings.BLACK,
            "cursor": self.settings.BLACK,
        }
        self.cmd_style = {
            "bg": (0, 0, 0),
            "line": (0, 0, 0),
            "text": (0, 255, 0)
        }

        self.cursor_dims = (3, self.line_height)
    
    @property
    def scroll(self) -> None:
        return self.scrollx, self.scrolly
    
    @scroll.setter
    def scroll(self, scroll_values: tuple[int, int]) -> None:
        if not scroll_values:
            raise ValueError(f"Wrong scroll values : {scroll_values}")
        self.scrollx, self.scrolly = scroll_values

    def getfont(self, font: str) -> pg.font:
        try:
            font = pg.font.Font(font, self.line_height) # Police personnalisée
        except FileNotFoundError:
            font = pg.font.SysFont(font, self.line_height) # Police système
        except Exception as e:
            print(f"Erreur lors du chargement de la police : {e}")
        return font
    
    def render_cursor_info(self, cursor_pos: tuple[int, int]) -> None:
        text = f"Ln {cursor_pos[1] + 1}, Col {cursor_pos[0] + 1}"
        surface = self.small_font.render(text, False, (0, 0, 0))
        self.SCREEN.blit(surface, (self.settings.SCREEN_DIMS[0] - surface.get_width(), self.settings.SCREEN_DIMS[1] - surface.get_height()))

    def get_line_surface(self, text: str, line_color=None, text_color=None) -> None:
        if not line_color:
            line_color = self.doc_style["line"]
        if not text_color:
            text_color = self.doc_style["text"]
        return self.text_font.render(text, False, text_color, line_color)

    def render_lines(self, lines: list[list], colored_lines: list[dict]) -> None:
        # Get lines we're interested in rendering
        visible_lines = lines[self.scrolly:self.scrolly + self.settings.MAX_LINES]
        visible_colored = colored_lines[self.scrolly:self.scrolly + self.settings.MAX_LINES]
        self.SCREEN.fill(self.doc_style["bg"])
        y = 0
        for line, color_data in zip(visible_lines, visible_colored):
            bg_color = color_data["line"]
            fg_color = color_data["text"]
            line_string = "".join(line[self.scrollx:])
            self.SCREEN.blit(self.get_line_surface(line_string, bg_color, fg_color), (self.settings.text_left_margin, y))
            y += self.line_height


    def render_selection(self, xy_start: tuple[int, int], xy_end: tuple[int, int]) -> None:
        if xy_start == xy_end:
            return  # Pas de sélection à rendre si les coordonnées de départ et de fin sont identiques
        
        x_start, y_start = xy_start
        x_end, y_end = xy_end
        if y_end == x_end == 0:
            return

        # Cas où la sélection est sur une seule ligne
        if y_start == y_end:
            x = (x_start - self.scrollx) * self.font_width + self.settings.text_left_margin
            y = (y_start - self.scrolly) * self.line_height
            width = (x_end - x_start) * self.font_width
            height = self.line_height
            surface = pg.Surface((width, height), flags=pg.SRCALPHA)
            surface.fill(self.settings.SELECTION_COLOR)
            self.SCREEN.blit(surface, (x, y))
            return

        # Cas où la sélection est sur plusieurs lignes
        for y in range(y_start, y_end+1):
            if y == y_start:  # Première ligne de la sélection
                x = (x_start - self.scrollx) * self.font_width + self.settings.text_left_margin
                width = (len(self.line_manager.lines[y]) - x_start) * self.font_width
            elif y == y_end:  # Dernière ligne de la sélection
                x = self.settings.text_left_margin
                width = max(0, x_end - self.scrollx) * self.font_width
            else:  # Lignes intermédiaires
                x = self.settings.text_left_margin
                width = max(0, len(self.line_manager.lines[y]) - self.scrollx) * self.font_width

            visible_y = (y - self.scrolly) * self.line_height
            height = self.line_height

            surface = pg.Surface((width, height), flags=pg.SRCALPHA)
            surface.fill(self.settings.SELECTION_COLOR)
            self.SCREEN.blit(surface, (x, visible_y))

    
    def render_cursor(self, gridpos: tuple[int, int], visible: bool) -> None:
        if not visible:
            return
        posx = (gridpos[0] - self.scrollx) * self.font_width + self.settings.text_left_margin
        posy = (gridpos[1] - self.scrolly) * self.line_height
        cursor_rect = pg.Rect(posx, posy, self.cursor_dims[0], self.cursor_dims[1])
        pg.draw.rect(self.SCREEN, self.doc_style["cursor"], cursor_rect)
            
    def render_scrollbars(self, scrollbar_list: list):
        if not scrollbar_list:
            return
        for scrollbar in scrollbar_list:
            pg.draw.rect(self.SCREEN, scrollbar.get_color(), scrollbar.get_rect())
    
    def set_mouse_nature(self, nature: pg.cursors.Cursor):
        self.cursor_sprite = nature
        pg.mouse.set_cursor(self.cursor_sprite)
    
    def hide_mouse(self) -> None:
        pg.mouse.set_visible(False)

    def show_mouse(self) -> None:
        pg.mouse.set_visible(True)

    def show_buttons(self, button_list: list, celldims: tuple[int, int]) -> None:
        margin_left = 1
        margin_top = 1
        for button in button_list:
            buttonx = button.gridx * celldims[0]
            buttony = button.gridy * celldims[1]
            button_insidex = buttonx + margin_left
            button_insidey = buttony + margin_top
            inside_color = self.passive_button_color if button.state == 0 else self.active_button_color
            button_rect = pg.Rect(buttonx, buttony, button.sizex, button.sizey)
            inside_rect = pg.Rect(button_insidex, button_insidey, button.sizex - 2*margin_left, button.sizey - 2*margin_top)
            button_text = self.get_line_surface(button.text, line_color=inside_color)
            text_rect = button_text.get_rect(center=button_rect.center)

            # dessine le bouton
            pg.draw.rect(self.SCREEN, (0, 0, 0), button_rect)
            pg.draw.rect(self.SCREEN, inside_color, inside_rect)
            self.SCREEN.blit(button_text, text_rect)

    def fill_screen(self, color=None) -> None:
        if not color:
            self.SCREEN.fill((255, 255, 255))
        self.SCREEN.fill(color)

    def draw_terminal(self, lines: list[str], colored_lines: list[dict], input: str, cursor_pos: tuple[int, int], scroll_up: int) -> None:
        self.fill_screen(self.cmd_style["bg"])
        y = 0
        start_idx = -(self.settings.MAX_LINES+scroll_up)
        visible_lines = lines[start_idx:]
        visible_data = colored_lines[start_idx:]
        for line, line_data in zip(visible_lines, visible_data):
            line_color = line_data["line"]
            text_color = line_data["text"]
            line_surface = self.cmd_font.render(line, True, text_color, line_color)
            self.SCREEN.blit(line_surface, (10, y))
            y += self.line_height
        if (pg.time.get_ticks() // 500) % 2 == 0:
            cursor = "|"
        else:
            cursor = ""
        input_surface = self.cmd_font.render(f" > {input[0:cursor_pos]}{cursor}{input[cursor_pos:]}", True, self.cmd_style["text"], self.cmd_style["line"])
        self.SCREEN.blit(input_surface, (10, y))

    def update(self) -> None:
        pg.display.flip()
        self.clock.tick(self.settings.FPS)