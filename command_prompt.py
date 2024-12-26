from text_manager import LineManager
import pygame as pg
from input_manager import *
import pygame as pg
from local import Local
import pyperclip
from utils import *
from commands import *
from time import sleep
import re


"""
Le command prompt est une version plus exhaustive des commandes de main.py
ça peut se répéter, mais ça va surtout plus en profondeur
"""


class CommandPrompt:
    def __init__(self, line_master: LineManager, cursor, renderer, state_master):
        self.renderer = renderer
        self.line_master = line_master
        self.CMD_line_master = LineManager()
        self.cursor = cursor
        self.command_idx = -1
        self.input_master = InputManager()
        self.prefix = "  > "
        self.state_master = state_master
        self.notepad_running = True
        self.last_commands = [""]
        self.macro_loaded = False
        self.macro_commands = []
        self.macro_command_idx = 0
        self.start_loop = 0
        self.end_loop = 0
        self.rep = 0
        self.looping = False
        self.loop_ctr = 0
        self.filling_idx = 0
        self.possible_commands = {}
        self.output_lines = []
        self.colored_lines = []
        self.pretext()
        self.reset()
        self.set_possible_commands()


    def set_possible_commands(self) -> None:
        self.possible_commands = {
            "clear": self.clear_cmd,
            "copy": self.copy_selection,
            "exit": self.exit,
            "paste": self.paste,
            "select": self.select,
            "upper": self.upper,
            "lower": self.lower,
            "inserthour": self.hour,
            "insertdate": self.date,
            "save": self.save,
            "load": self.load,
            "setdocstyle": self.set_doc_style,
            "setcmdstyle": self.setcmdstyle,
            "setlinestyle": self.setlinestyle,
            "newdoc": self.newdoc,
            "newline": self.newline,
            "delline": self.delline,
            "insert": self.insert,
            "show": self.show_instructions,
            "help": self.displayhelp,
            "loop": self.set_loop,
            "setcursorpos": self.setcursorpos,
            "sleep": self.sleep,
            "setlinetext": self.setlinetext
        }
    
    def reset(self) -> None:
        self.current_line = ""
        self.running = True
        self.command = None
        

    def pretext(self) -> None:
        self.add_line()
        self.add_line("Notepad Terminal")
        self.add_line()
        self.add_line(" Mouse to navigate")
        self.add_line(" Type 'Show' to see the available commands")
        self.add_line()

    
    def mainloop(self) -> None:
        self.reset()
        scroll = -1
        cmd_cursor_x = 0
        while self.running:
            event = self.input_master.get_pg_events()
            if event in self.input_master.REQUIRE_WAIT:
                if self.state_master.check_is_key_accessible(event):
                    can_update = True
                else:
                    can_update = False
            if event == QUIT:
                self.running = False
                self.notepad_running = False
            if event == CTRL_C and can_update:
                self.add_line(self.prefix + self.current_line)
                self.current_line = ""
                cmd_cursor_x = 0
            if event == CTRL_V and can_update:
                self.current_line = self.current_line[:cmd_cursor_x] + pyperclip.paste() + self.current_line[cmd_cursor_x:]
            if event == RETURN and can_update:
                if self.current_line != "" and self.current_line != self.last_commands[0]:
                    self.last_commands.insert(0, self.current_line)
                self.command_idx = -1
                self.add_line(self.prefix + self.current_line)
                self.command = Command(self.current_line)
                self.execute_command()
                self.current_line = ""
                cmd_cursor_x = 0
                self.debug_lines_too_long()
            if event == TAB and can_update:
                self.propose_filling()
                cmd_cursor_x = len(self.current_line)
            if event == BACKSPACE and can_update:
                if len(self.current_line) != 0 and cmd_cursor_x != 0:
                    self.current_line = self.current_line[0:cmd_cursor_x-1] + self.current_line[cmd_cursor_x:]
                    cmd_cursor_x = max(0, cmd_cursor_x-1)
            if event == MW_UP:
                scroll = min(scroll + self.input_master.mw_value, abs((len(self.output_lines) - self.renderer.settings.MAX_LINES)))
            if event == MW_DOWN:
                scroll = max(scroll - self.input_master.mw_value, -1)
            if event == UP and can_update:
                self.command_idx = min(self.command_idx+1, len(self.last_commands)-1)
                self.current_line = self.last_commands[self.command_idx]
            if event == DOWN and can_update:
                self.command_idx = max(0, self.command_idx-1)
                self.current_line = self.last_commands[self.command_idx]
            if event == LEFT and can_update:
                cmd_cursor_x = max(0, cmd_cursor_x-1)
            if event == RIGHT and can_update:
                cmd_cursor_x = min(cmd_cursor_x+1, len(self.current_line))
            if self.input_master.unicode_event and self.input_master.is_only_unicode:
                self.current_line = self.current_line[0:cmd_cursor_x] + self.input_master.unicode_event + self.current_line[cmd_cursor_x:]
                cmd_cursor_x += 1
                scroll = -1

            self.state_master.set_last_event(event)
            self.renderer.draw_terminal(self.output_lines, self.colored_lines, self.current_line, cmd_cursor_x, scroll)
            self.renderer.update()
    
    def debug_lines_too_long(self):
        max_chars = 79
        for line_idx, line in enumerate(self.output_lines):
            if len(line) <= max_chars:
                continue
            changed_line = line[:max_chars]
            added_line = line[max_chars:]
            self.output_lines[line_idx] = changed_line
            self.add_line(string=added_line, idx=line_idx + 1)

    
    def propose_filling(self) -> None:
        # Obtenir le premier mot
        cut_line = self.current_line.strip().split(" ")
        for idx, element in enumerate(cut_line):
            if "=" in element:
                element = element[:element.index("=")+1]
                cut_line[idx] = element
        if len(cut_line) == 0:
            return
        if cut_line[0] in commands:
            command_name = cut_line[0]
            # Get parameters
            for param in parameters[command_name]:
                string = "" if param.startswith("-") else "="
                visible_param = param + string
                if visible_param in cut_line:
                    continue
                self.current_line += f" {visible_param}"
                return
            return
        # Trouver tous les noms qui commencent par le 1er élément
        incomplete_name = cut_line[0]
        possible_fillings = []
        for name in commands:
            if name.startswith(incomplete_name):
                possible_fillings.append(name)
        if not possible_fillings:
            return
        cut_line[0] = possible_fillings[self.filling_idx]
        self.current_line = "".join(cut_line[0])
    
    def sleep(self):
        if not self.command.parameters:
            self.add_line("No sleep value")
            return
        if "time" in self.command.parameters:
            time_sleep = self.command.parameters["time"]
        sleep(time_sleep)


    def add_line(self, string="", lighterror=False, error=False, idx=-1) -> None:
        line_color = self.renderer.cmd_style["line"]
        text_color = self.renderer.cmd_style["text"]
        if not string:
            string = ""
        if lighterror:
            text_color = (255, 255, 0)
        if error:
            text_color = (255, 0, 0)
        
        if idx == -1:        
            self.output_lines.append(string)
            self.colored_lines.append({"line": line_color, "text": text_color})
        else:
            self.output_lines.insert(idx, string)
            self.colored_lines.insert(idx, {"line": line_color, "text": text_color})
    
    def clear_cmd(self) -> None:
        self.output_lines = []
        self.colored_lines = []
        self.pretext()
    
    def copy_selection(self) -> None:
        if not self.command.parameters:
            self.cursor.copy_selection()
            self.add_line("Sélection curseur copiée")
            return
        # Set current selection to everything
        start = (0, 0)
        end = (self.line_master.len_last_line, self.line_master.last_line_idx)
        if "start" in self.command.parameters and "end" in self.command.parameters:
            start = self.command.parameters["start"]
            end = self.command.parameters["end"]
        elif "start" in self.command.parameters:
            start = self.command.parameters["start"]
        elif "end" in self.command.parameters:
            end = self.command.parameters["end"]
        elif "all" in self.command.parameters:
            pass
        else:
            self.add_line("Arguments 'start', 'end' or 'all' necessary", lighterror=True)
        
        self.cursor.gridpos = start
        self.cursor.set_anchor_pos(end)
        self.cursor.copy_selection()
        self.add_line(f"Copied from {start} to {end}")

    
    def paste(self) -> None:
        if not self.command.parameters:
            clipboard_content = pyperclip.paste()
            addx, addy = self.line_master.add_to_line(clipboard_content, self.cursor.gridpos, get_cursor_repos_info=True)
            self.cursor.set_pos_and_anchor((self.cursor.gridposx + addx, self.cursor.gridposy + addy)) # Pas idéal, si ?
            self.add_line("Pasted clipboard content to current cursor position")
            return
        
        if "pos" in self.command.parameters:
            gridpos = self.command.parameters["pos"]
            clipboard_content = pyperclip.paste()
            addx, addy = self.line_master.add_to_line(clipboard_content, gridpos, get_cursor_repos_info=True)
            self.cursor.set_pos_and_anchor((gridpos[0] + addx, gridpos[1] + addy), self.renderer.scrolly)
        
        
    def select(self) -> None:
        if not self.command.parameters:
            self.add_line("Need at least 1 argument", lighterror=True)
            return
        start = (0, 0)
        end = (self.line_master.len_last_line, self.line_master.last_line_idx)
        if "start"in self.command.parameters and "end"in self.command.parameters:
            start = self.command.parameters["start"]
            end = self.command.parameters["end"]
        if "start" in self.command.parameters:
            start = self.command.parameters["start"]
        if "end" in self.command.parameters:
            end = self.command.parameters["end"]
        if "all" in self.command.parameters:
            pass
        self.cursor.select_from_pos(start, end)
        
    
    def upper(self) -> None:
        if not self.command.parameters:
            line_y = self.cursor.gridposy
            self.line_master.upper_line(line_y)
            self.add_line(f"Line {line_y} changed to uppercase")
            return
        if "lines" in self.command.parameters:
            startline, endline = self.command.parameters["lines"]
            dy = endline - startline
            for y in range(dy):
                self.line_master.upper_line(startline + y)
            self.add_line(f"Lines {startline} to {endline} changed to uppercase")
        if "all" in self.command.parameters:
            for line_idx in range(self.line_master.nb_lines):
                self.line_master.upper_line(line_idx)
        
            
    def lower(self) -> None:
        if not self.command.parameters:
            line_y = self.cursor.gridposy
            self.line_master.lower_line(line_y)
            self.add_line(f"Line {line_y} changed to lowercase")
            return

        if "lines" in self.command.parameters:
            startline, endline = self.command.parameters["lines"]
            dy = endline - startline
            for y in range(dy):
                self.line_master.lower_line(startline + y)
            self.add_line(f"Lines {startline} to {endline} changed to lowercase")
    
    def hour(self) -> None:
        gridpos = None
        if not self.command.parameters:
            gridpos = self.cursor.gridpos
        if "pos" in self.command.parameters:
            gridpos = self.command.parameters["pos"]
        if not gridpos:
            self.add_line("Wrong arguments", lighterror=True)
            return
        self.line_master.insert_hour(gridpos)
        self.add_line(f"Hour inserted at {gridpos}")
        
    
    def date(self) -> None:
        gridpos = None
        if not self.command.parameters:
            gridpos = self.cursor.gridpos
        if "pos" in self.command.parameters:
            gridpos = self.command.parameters["pos"]
        if not gridpos:
            self.add_line("Wrong arguments", lighterror=True)
            return
        self.line_master.insert_date(gridpos)
        self.add_line(f"Date inserted at {gridpos}")
    
    def save(self) -> None:
        if not self.command.parameters:
            filename = "txt_file.txt"
            Local.save_txtfile(filename, self.line_master.lines)
            self.add_line(f"File has been saved in local directory as {filename}")
        if "directory" in self.command.parameters and "name" in self.command.parameters:
            path = self.command.parameters["directory"]
            name = self.command.parameters["name"]
            fullpath = path+"/"+name
        if "fullpath" in self.command.parameters:
            fullpath = self.command.parameters["fullpath"]
        Local.save_txtfile(fullpath, self.line_master.lines)
        self.add_line(f"File has been saved in {fullpath}")
    
    def load(self) -> None:
        if not self.command.parameters:
            self.add_line("'Fullpath' argument required", lighterror=True)
            return
        if "fullpath" in self.command.parameters:
            fullpath = self.command.parameters["fullpath"]
            lines = Local.load_txtfile(fullpath)
            
        if "macro" in self.command.parameters:
            self.macro_commands = []
            for line in lines:
                self.macro_commands.append(Command("".join(line)))
            self.macro_loaded = True
            self.add_line("File loaded as macro | Press [Ctrl+m] in the notepad to start")
        else:
            self.line_master.lines = Local.load_txtfile(fullpath)
            for _ in range(len(self.line_master.lines)):
                self.line_master.colored_lines.append(self.line_master.default_colored_args())
            self.add_line("File loaded as text")
    
    def set_doc_style(self) -> None:
        if not self.command.parameters:
            self.add_line("At least 1 parameter required", lighterror=True)
        if "bg" in self.command.parameters:
            self.renderer.doc_style["bg"] = self.command.parameters["bg"]
        if "line" in self.command.parameters:
            self.renderer.doc_style["line"] = self.command.parameters["line"]
        if "text" in self.command.parameters:
            self.renderer.doc_style["text"] = self.command.parameters["text"]
        if "cursor" in self.command.parameters:
            self.renderer.doc_style["cursor"] = self.command.parameters["cursor"]
        if "cursorwidth" in self.command.parameters:
            self.renderer.cursor_dims = (self.command.parameters["cursorwidth"], self.renderer.cursor_dims[1])
        if "cursorheight" in self.command.parameters:
            self.renderer.cursor_dims = (self.renderer.cursor_dims[0], self.command.parameters["cursorheight"])
    
    def setcmdstyle(self) -> None:
        if not self.command.parameters:
            self.add_line("At least 1 parameter required", lighterror=True)
        if "bg" in self.command.parameters:
            self.renderer.cmd_style["bg"] = self.command.parameters["bg"]
        if "line" in self.command.parameters:
            self.renderer.cmd_style["line"] = self.command.parameters["line"]
        if "text" in self.command.parameters:
            self.renderer.cmd_style["text"] = self.command.parameters["text"]
        if "font" in self.command.parameters:
            self.renderer.cmd_font = self.renderer.getfont(self.command.parameters["font"])
    
    def setlinestyle(self) -> None:
        if not self.command.parameters:
            self.add_line("At least 1 parameter required", lighterror=True)
        start = end = self.cursor.gridposy
        line_color = None
        text_color = None
        if "line" in self.command.parameters:
            line_color = self.command.parameters["line"]
        if "text" in self.command.parameters:
            text_color = self.command.parameters["text"]
        if "idx" in self.command.parameters:
            start = end = self.command.parameters["idx"]
        if "array" in self.command.parameters:
            start, end = self.command.parameters["array"]
        for line_idx in range(start, end+1):
            if text_color:
                self.line_master.colored_lines[line_idx]["text"] = text_color
            if line_color:
                self.line_master.colored_lines[line_idx]["line"] = line_color
    
    def setlinetext(self):
        if not self.command.parameters:
            self.add_line("Parameter 'text' required")
            return
        line_y = self.cursor.gridposy
        if "idx" in self.command.parameters:
            line_y = self.command.parameters["idx"]
        if "text" in self.command.parameters:
            text = self.command.parameters["text"]
        self.line_master.lines[line_y] = list(text)

    
    def newdoc(self) -> None:
        self.cursor.set_pos_and_anchor((0, 0))
        if not self.command.parameters:
            self.line_master.reset_all_lines()
            self.add_line("Empty document created")
            return
        
        if "rand" in self.command.parameters:
            maxlines, maxlenght = self.command.parameters["rand"]
        colored = False
        if "color" in self.command.parameters:
            colored = True

        self.line_master.random_doc(maxlines, maxlenght, colored)
        color_string = "color filled" if colored else "black and white"
        self.add_line(f"New {color_string} document of {self.line_master.nb_lines} lines created (longuest : {self.line_master.len_longuest_line} characters)")

    def newline(self) -> None:
        if not self.command.parameters:
            line_y = self.cursor.gridposy
            self.line_master.new_line(self.cursor.gridposy)
            self.cursor.set_pos_and_anchor((0, line_y + 1))
            self.renderer.scrollx, self.renderer.scrolly = self.cursor.get_updated_scroll(self.renderer.scroll)
    
    def delline(self) -> None:
        if not self.command.parameters:
            line_idx = self.cursor.gridposy
            self.cursor.move_up()
            self.cursor.set_anchor()
            del self.line_master.lines[line_idx]
            if not self.line_master.lines:
                self.line_master.lines = [[]]
            self.add_line(f"Line {line_idx} deleted")


    def insert(self) -> None:
        if not self.command.parameters:
            self.add_line("At least 1 parameter required", lighterror=True)
            return
        if "text" in self.command.parameters:
            x, y = self.cursor.gridpos
            if "line" in self.command.parameters:
                y = self.command.parameters["line"]
            if "x" in self.command.parameters:
                x = self.command.parameters["x"]
            if "start" in self.command.parameters:
                x = 0
            if "end" in self.command.parameters:
                x = len(self.line_master.lines[y])
            gridpos = (x, y)
            text = self.command.parameters["text"]
            addx, addy = self.line_master.add_to_line(text, gridpos, True)
            self.cursor.set_pos_and_anchor((self.cursor.gridposx + addx, self.cursor.gridposy + addy))
            self.add_line(f"Text inserted at line {y}, character {x}")
    
    def setcursorpos(self) -> None:
        x, y = self.cursor.gridpos
        if not self.command.parameters:
            self.add_line("Cursor position unchanged")
            return
        if "startline" in self.command.parameters:
            x = 0
        if "startdoc" in self.command.parameters:
            x = 0
            y = 0
        if "endline" in self.command.parameters:
            x = len(self.line_master.lines[y])
        if "enddoc" in self.command.parameters:
            x, y = self.line_master.last_gridpos
        if "pos" in self.command.parameters:
            x, y = self.command.parameters["pos"]
        self.cursor.set_pos_and_anchor((x, y))
        self.add_line(f"New cursor position : ({x},{y})")
    
    def exit(self) -> None:
        if not self.command.parameters:
            self.running = False
        if "all" in self.command.parameters:
            self.running = False
            self.notepad_running = False

    @staticmethod
    def get_instructions() -> str:
        text = f"{titlelize('Available Commands')} \n"
        for ligne in commands.keys():
            if ligne.startswith("="):
                text += f"\n{ligne}\n\n"
                continue
            text += f" - \"{ligne}\"\n"
        text += "\nType 'help name=[command name]' to show the help for a command"
        return text
    
    def show_instructions(self) -> None:
        self.add_line()
        for line in self.get_instructions().split("\n"):
            self.add_line(line)
        self.add_line()

    def displayhelp(self) -> None:
        asked_command = self.command.parameters["name"]
        # Get the command data
        if asked_command not in commands:
            self.add_line(f"Command \"{asked_command}\" not recognised", error=True)
            self.execution_sucess = False
            return
        command_data = commands[asked_command]
        description = command_data["description"]
        params = command_data["param"]
        exemples = command_data["exemples"]
        
        self.add_line()
        for line in titlelize('Help').split("\n"):
            self.add_line(line)
        self.add_line()
        self.add_line(f"Command name : '{asked_command}'")
        self.add_line()
        self.add_line(f"Description : {description}")
        self.add_line()
        self.add_line(f"Parameters :")
        for param in params:
            self.add_line(f" - {param}")
        self.add_line()
        self.add_line("Exemples :")
        for exemple in exemples:
            self.add_line(f" - {exemple}")
        self.add_line()
    
    def reset_macro_mode(self) -> None:
        self.macro_command_idx = 0
        self.start_loop = 0
        self.end_loop = 0
        self.loop_ctr = 0
        self.rep = 0

    
    def execute_current_macro_command(self) -> None:
        self.command = self.macro_commands[self.macro_command_idx]
        self.execute_command()
        if self.looping and self.macro_command_idx >= self.end_loop - 1:
            self.macro_command_idx = self.start_loop
            self.loop_ctr += 1
            if self.loop_ctr >= self.rep:
                self.looping = False
        self.macro_command_idx += 1
        #print(f"Start loop : {self.start_loop}, current_idx = {self.macro_command_idx}, endloop = {self.end_loop}")


    def set_loop(self) -> None:
        if not self.macro_commands:
            self.add_line("No macro initialised", error=True)
            return

        self.start_loop = self.macro_command_idx
        self.rep = self.command.parameters["rep"]

        # Recherche directe de "endloop" après start_loop
        for idx in range(self.start_loop, len(self.macro_commands)):
            if self.macro_commands[idx].name == "endloop":
                self.end_loop = idx
                self.looping = True
                return

        print("No endloop found!")
        self.looping = False


    def execute_command(self) -> None:
        if not self.command.name:
            return
        if self.command.name not in self.possible_commands:
            self.add_line(f"Command '{self.command.name}' not recognised", error=True)
            return
        if self.command.error_flag:
            for line in self.command.error_log:
                self.add_line(line, lighterror=True)
            return
        
        executable_command = self.possible_commands[self.command.name]
        executable_command()


class Command:
    def __init__(self, command_string):
        self.error_log = []
        self.error_flag = False
        self.command_string = command_string
        if self.command_string.startswith("#"):
            self.name = None
            self.parameters = {}
            return
        self.split_command = self.command_string.split()
        if not self.split_command:
            self.name = None
            self.parameters = {}
            return
        self.name, self.parameters = self.parse_string(self.command_string)

    @staticmethod
    def parse_string(input_str):
        # Extraction de la première partie (le mot isolé comme "load")
        name_match = re.match(r'^(\w+)', input_str)
        name = name_match.group(1) if name_match else None
        
        # Extraction des paires clé-valeur
        attributes = re.findall(r'(\w+)=("[^"]*"|\'[^\']*\'|[^\s]+)|(-\w+)', input_str)
        parsed_dict = {}
        
        for attr in attributes:
            if attr[2]:  # Si un mot-clé comme "-macro" est trouvé
                key = attr[2].lstrip('-')  # Retirer le tiret pour utiliser comme clé
                parsed_dict[key] = True
                continue
            key, value = attr[0], attr[1]
            # Traitement des valeurs
            if ',' in value and not value.startswith(("'", '"')):  
                # Si la valeur contient une virgule et n'est pas entourée de guillemets
                value = tuple(map(lambda x: float(x) if '.' in x else int(x), value.split(',')))
            elif (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):  
                # Si la valeur est une chaîne entourée de guillemets
                value = value[1:-1]  # Supprimer les guillemets simples ou doubles
            elif value.isdigit():  # Si la valeur est un entier
                value = int(value)
            elif re.match(r'^\d+\.\d+$', value):  # Si la valeur est un float
                value = float(value)
            
            parsed_dict[key] = value  # Ajouter au dictionnaire
        
        return name, parsed_dict
                
    
    def add_error(self, string) -> None:
        self.error_log.append(string)

c = Command("help name=command")