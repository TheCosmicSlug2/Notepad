from random import randint, choice
from pyperclip import copy
from datetime import datetime
from utils import random_rgb


class LineManager:
    def __init__(self):
        self.lines = [[]]
        self.colored_lines = [self.default_colored_args()]

    
    def reset_all_lines(self) -> None:
        self.lines = [[]]
        self.colored_lines = [self.default_colored_args()]
    
    def no_lines(self) -> None:
        self.lines = []
        self.colored_lines = []
    
    def random_doc(self, maxlines: int, maxlinelenght: int, colored=False) -> None:
        self.no_lines()
        possible = "abcdefghijklmnopqrstuvwxyz1234567890&é\"'(-è_çà=~#{[|`\^@])^¨ù%!:;,§/.?*µ²"
        lst = list(possible)
        for _ in range(randint(1, maxlines)): # La taille totale doit être au moins d'une ligne
            line = []
            for _ in range(randint(0, maxlinelenght)):
                line.append(choice(lst))
            self.lines.append(line)
            color_dic = {"line": None, "text": None}
            if colored:
                color_dic = {"line": random_rgb(), "text": random_rgb()}
            self.colored_lines.append(color_dic)

    @staticmethod
    def convert_clipboard_to_list(string: str) -> None:
        split_lines = string.split("\r\n")
        new_line_lists = [list(line) for line in split_lines]
        return new_line_lists
    
    @property
    def nb_lines(self) -> int:
        return len(self.lines)

    @property
    def idx_longuest_line(self) -> int:
        if not self.lines:
            return 
        return self.lines.index(max(self.lines, key=len))
    
    @property
    def len_longuest_line(self) -> int:
        return len(self.lines[self.idx_longuest_line])
    
    @property 
    def longuest_line(self) -> int:
        return self.lines[self.idx_longuest_line]

    @property
    def last_gridpos(self) -> tuple[int, int]:
        return self.nb_lines, len(self.lines[-1]) -1

    @property
    def last_line_idx(self) -> int:
        return len(self.lines) - 1
    
    @property
    def len_last_line(self) -> int:
        return len(self.lines[self.last_line_idx])
    
    def new_line(self, last_line_idx: int) -> None:
        self.lines.insert(last_line_idx+1, [])
        self.colored_lines.insert(last_line_idx+1, self.default_colored_args())
    
    def add_line_at_cursor(self, cursor_gridpos: tuple[int, int]) -> None:
        char_idx, line_idx = cursor_gridpos
        # Choper tous les éléments qui viennent après le curseur
        next_ligne = self.lines[line_idx][char_idx:]
        # Supprimer les caractères de la ligne actuelle
        del self.lines[line_idx][char_idx:]
        self.lines.insert(line_idx + 1, next_ligne)
        self.colored_lines.insert(line_idx + 1, self.default_colored_args())
    

    @staticmethod
    def default_colored_args() -> dict[int, bool]:
        return {"line": None, "text": None}
    
    def add_line(self, content: list[str]=None) -> None:

        # 3 cas : 
        # le curseur est au début : on ajoute une ligne avant
        # le curseur est au mileu : on ajoute une ligne au milieu
        # Le curseur est à la fin : on ajoute une ligne après

        # Couper la ligne
        if not content:
            # Nécessaire de créer une instance à part, sinon toutes les lignes partagent la même instance et tous les changements sur une ligne se répercutent aux autres
            content = []         
        self.lines.append(content)
        self.colored_lines.append(self.default_colored_args())
    
    def upper_line(self, line_idx: int) -> None:
        self.lines[line_idx] = [char.upper() for char in self.lines[line_idx]]

    def lower_line(self, line_idx: int) -> None:
        self.lines[line_idx] = [char.lower() for char in self.lines[line_idx]]
    
    def insert_hour(self, gridpos: tuple[int, int]) -> None:
        char_idx, line_idx = gridpos
        self.lines[line_idx][char_idx:char_idx] = list(datetime.now().strftime("%Hh%M"))
    
    def insert_date(self, gridpos: tuple[int, int]) -> None:
        char_idx, line_idx = gridpos
        self.lines[line_idx][char_idx:char_idx] = list(datetime.now().strftime("%d-%m-%Y"))
    
    def change_line_bg(self, line_idx: int) -> None:
        self.colored_lines[line_idx]["line"] = random_rgb()
    
    def change_line_fg(self, line_idx: int) -> None:
        self.colored_lines[line_idx]["text"] = random_rgb()

    def remove_selection(self, selection_indices: tuple[tuple[int, int], tuple[int, int]]) -> None:
        start_pos, end_pos = selection_indices
        if start_pos == end_pos:
            self.remove_char_at_cursor(start_pos) # Ou end_pos, peu importe
            return
        
        # Change first line
        self.lines[start_pos[1]] = self.lines[start_pos[1]][:start_pos[0]] + self.lines[end_pos[1]][end_pos[0]:]
        # Remove inner lines
        self.lines = self.lines[:start_pos[1]+1] + self.lines[end_pos[1] + 1:]

    
    def remove_char_at_cursor(self, cursor_gridpos: tuple[int, int]) -> None:
        char_idx, line_idx = cursor_gridpos
        if char_idx != 0:
            self.lines[line_idx].pop(char_idx - 1)
            return
        if line_idx == 0: # Si le curseur est déjà sur la première ligne
            return
        cursor_newgridx = len(self.lines[line_idx - 1])
        self.lines[line_idx - 1].extend(self.lines[line_idx])
        self.lines.pop(line_idx)
        self.colored_lines.pop(line_idx)
        return cursor_newgridx
        
    
    def add_char_at_cursor(self, cursor_gridpos: tuple[int, int], char: int) -> None:
        char_idx, line_idx = cursor_gridpos
        self.lines[line_idx].insert(char_idx, char)
    
    def remove_character(self, line_idx: int, char_idx: int) -> None:
        # Supprimer une ligne vide
        if self.lines[line_idx] == [] and len(self.lines) > 1:
            self.lines.pop(line_idx)
            self.colored_lines.pop(line_idx)
            return
        # Supprimer un caractère d'une ligne
        if char_idx == -1 and self.lines[line_idx] != []: # dernier caractère de la ligne
            self.lines[line_idx].pop(-1)
            self.colored_lines.pop(-1)
            return


    
    def add_to_line(self, string: str, cursor_pos: tuple[int, int], get_cursor_repos_info: bool) -> None:
        char_idx, line_idx = cursor_pos
        current_line = self.lines[line_idx]

        # Convertir la ligne actuelle en une chaîne pour faciliter l'insertion
        flat_line = ''.join(current_line)
        
        # Insérer le texte au bon endroit
        new_text = flat_line[:char_idx] + string + flat_line[char_idx:]

        # Scinder le nouveau texte par les retours chariot et les retours à la ligne
        split_lines = new_text.split("\r\n")

        # Convertir chaque ligne en une liste de strings (si nécessaire)
        new_line_lists = [list(line) for line in split_lines]

        # Remplacer la ligne actuelle et insérer les nouvelles lignes
        self.lines[line_idx:line_idx + 1] = new_line_lists
        self.colored_lines[line_idx:line_idx + 1] = [self.default_colored_args() for _ in range(len(split_lines))]

        if get_cursor_repos_info:
            return len(new_line_lists[-1]), len(new_line_lists)-1




class Cursor:
    def __init__(self, line_manager: LineManager, settings):
        self.gridposx = 0
        self.gridposy = 0
        self.line_manager = line_manager
        self.visible = True
        self.anchor = (self.gridposx, self.gridposy)
        self.highlighted_text = [[]]
        self.list_selection = None
        self.settings = settings
    
    def set_fullpos_to_word_end(self):
        # Quand le curseur est en fin de ligne
        current_line_lenght = len(self.line_manager.lines[self.gridposy])
        if self.gridposx == current_line_lenght:
            if self.gridposy + 1 >= self.line_manager.nb_lines:
                return
            self.gridposy += 1
            self.gridposx = 0
            self.set_anchor()
            return
            
        for character_idx, character in enumerate(self.line_manager.lines[self.gridposy][self.gridposx + 1:]):
            if character == " " :
                self.gridposx += character_idx + 1
                self.set_anchor()
                return
            if self.gridposx + character_idx + 2 == current_line_lenght:
                self.gridposx += character_idx + 2
                self.set_anchor()
                return
    
    def set_fullpos_to_word_start(self):
        if self.gridposx == 0:
            if self.gridposy == 0:
                return
            self.gridposy -= 1
            self.gridposx = len(self.line_manager.lines[self.gridposy])
        
        for character_idx in range(self.gridposx-2, -1, -1):
            character = self.line_manager.lines[self.gridposy][character_idx]
            if character == " ":
                self.gridposx = character_idx + 1
                self.set_anchor()
                return
            if character_idx == 0:
                self.gridposx = 0
                self.set_anchor()
                return
            
    def get_updated_scroll_y(self, scrolly: int) -> int:
        max_visible_lines = self.settings.MAX_LINES
        # Indice de la première ligne visible
        first_visible_line = scrolly
        # Indice de la dernière ligne visible
        last_visible_line = scrolly + max_visible_lines
        # Vérifier si le curseur est sur la dernière ligne visible
        if self.gridposy == last_visible_line:
            # Déplacer le défilement vers le haut si possible
            return max(0, scrolly + 1)  # Remplacez par `scroll - 1` si le sens est inversé
        if self.gridposy == first_visible_line:
            return max(0, scrolly - 1)
        if self.line_manager.nb_lines - self.settings.MAX_LINES < 0:
            return 0
        # Aucun changement
        return scrolly
        
    
    def get_updated_scroll(self, scroll: tuple[int, int]) -> tuple[int, int]:
        scrollx, scrolly = scroll
        new_scrollx, new_scrolly = scrollx, scrolly

        # Update le scroll x
        max_characters_per_line = self.settings.SCREEN_DIMS[1] // self.settings.TEXT_FONT_WIDTH
        if self.gridposx > max_characters_per_line + scrollx:
            new_scrollx = max_characters_per_line + scrollx
        
        # Update le scroll y
        max_visible_lines = self.settings.MAX_LINES
        first_visible_line = scrolly
        last_visible_line = scrolly + max_visible_lines
        if self.gridposy == last_visible_line:
            new_scrolly = max(0, scrolly + 1)  # Remplacez par `scroll - 1` si le sens est inversé
        if self.gridposy == first_visible_line:
            new_scrolly = max(0, scrolly - 1)
        if self.line_manager.nb_lines - self.settings.MAX_LINES < 0:
            new_scrolly = 0

        return new_scrollx, new_scrolly            
    
    
    def copy_selection(self) -> None:
        self.set_highlighted()
        copy(self.get_selected_string())


    def move_to_end(self) -> None:
        self.gridposy = len(self.line_manager.lines - 1)
        self.gridposx = len(self.line_manager[self.gridposy])
    
    def set_anchor_pos(self, gridpos: tuple[int, int]) -> None:
        self.anchor = gridpos

    def set_highlighted(self) -> None:
        # Juste obtenir le texte highlité
        start_y, end_y = sorted([self.anchor[1], self.gridposy])
        start_x, end_x = sorted([self.anchor[0], self.gridposx])
        
        # Obtenir toutes les lignes en y
        self.list_selection = self.line_manager.lines[start_y:end_y+1]
        # Enlever la première position x
        if start_y == end_y:
            # Si une seule ligne est sélectionnée, découper la ligne dans les deux dimensions
            self.list_selection = [self.list_selection[0][start_x:end_x]]
        else:
            # Découper la première et la dernière ligne si plusieurs lignes sont sélectionnées
            self.list_selection[0] = self.list_selection[0][start_x:]
            self.list_selection[-1] = self.list_selection[-1][:end_x]


    @property
    def select_indices(self) -> tuple[tuple[int, int], tuple[int, int]]:
        # Trier les coordonnées pour obtenir toujours (start_x, start_y) et (end_x, end_y)
        (start_x, start_y), (end_x, end_y) = sorted(
            [self.anchor, (self.gridposx, self.gridposy)], key=lambda p: (p[1], p[0]) # TODO Comprendre pourquoi ça marche
        )
        return (start_x, start_y), (end_x, end_y)
        
    def get_selected_string(self) -> str:
        global_string = ""
        for line in self.list_selection:
            inner_string = "".join(line)
            if line != self.list_selection[-1]:
                inner_string += "\r\n"
            global_string += inner_string
        return global_string
    
    def debug_cursor_out_of_frame(self, scrolly: int, max_y_lines: int) -> int:
        if self.gridposy + scrolly > max_y_lines:
            scrolly = max_y_lines - self.gridposy
        return scrolly

    @property
    def gridpos(self) -> tuple[int, int]:
        return (self.gridposx, self.gridposy)
    
    @gridpos.setter
    def gridpos(self, new_pos: tuple[int, int]) -> None:
        self.gridposx, self.gridposy = new_pos
    
    def select_from_pos(self, pos1: int, pos2: int) -> None:
        self.anchor = pos1
        self.gridposx = pos2[0]
        self.gridposy = pos2[1]
    
    def select_all(self) -> None:
        self.anchor = (0, 0)
        self.gridposx = len(self.line_manager.lines[-1])
        self.gridposy = len(self.line_manager.lines) - 1
    
    def set_pos_and_anchor(self, gridpos: tuple[int, int]):
        self.gridpos = gridpos
        self.set_anchor()
    
    def set_anchor(self) -> None:
        self.anchor = self.gridpos
    
    def move_up(self) -> None:
        last_gridposy = self.gridposy # Ligne Actuelle (visuellement, pas dans le temps)
        self.gridposy = max(self.gridposy - 1, 0) # Ligne précédent

        # Si la longueur de la ligne précédente est plus petite que la ligne actuelle
        # Si la position x est plus grande que la longueur de la ligne précédente
        if len(self.line_manager.lines[self.gridposy]) < len(self.line_manager.lines[last_gridposy]) and self.gridposx > len(self.line_manager.lines[self.gridposy]):
            self.gridposx = len(self.line_manager.lines[self.gridposy])
        self.set_anchor()

    
    def move_down(self) -> None:
        last_gridposy = self.gridposy
        self.gridposy = min(self.gridposy + 1, len(self.line_manager.lines) - 1)
        # Si la longueur de la ligne suivant est plus petite que la ligne actuelle
        # la position x est plus grande que la longueur de la ligne suivantes
        if len(self.line_manager.lines[self.gridposy]) < len(self.line_manager.lines[last_gridposy]) and self.gridposx > len(self.line_manager.lines[self.gridposy]):
            self.gridposx = len(self.line_manager.lines[self.gridposy])
        self.set_anchor()
    
    def move_left(self) -> None:
        self.gridposx -= 1
        if self.gridposx < 0:
            if self.gridposy > 0:
                # Go on last line
                self.gridposy -= 1
                self.gridposx = len(self.line_manager.lines[self.gridposy])
            else:
                self.gridposx = 0
        self.set_anchor()
        
    def move_right(self) -> None:
        self.gridposx += 1
        if self.gridposx > len(self.line_manager.lines[self.gridposy]):
            if self.gridposy < len(self.line_manager.lines) - 1:
                self.gridposy += 1
                self.gridposx = 0
            else:
                self.gridposx = len(self.line_manager.lines[self.gridposy])
        self.set_anchor()
    
    def set_pos(self, gridpos: tuple[int, int], scroll: int) -> None:
        gridx, gridy = gridpos
        scrollx, scrolly = scroll
        # Obtenir la ligne la plus proche
        line_idx = min(gridy + scrolly, len(self.line_manager.lines) - 1)
        char_idx = min(gridx + scrollx, len(self.line_manager.lines[line_idx]))

        self.gridposx, self.gridposy = char_idx, line_idx
