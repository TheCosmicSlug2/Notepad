parameters = {
    "select": ["start", "end", "-all"],
    "copy": ["start", "end" "-all"],
    "upper": ["line", "-all"],
    "lower": ["line", "-all"],
    "insert": ["text", "line", "x", "start", "end"],
    "inserthour": ["pos"],
    "insertdate": ["pos"],
    "save": ["directory", "name", "fullpath"], 
    "load": ["fullpath", "-macro"],
    "setdocstyle": ["bg", "line", "text", "cursor", "cursorwidth", "cursorheight"],
    "setcmdstyle": ["bg", "line", "text", "font"],
    "setlinestyle": ["idx", "line", "text"],
    "newdoc": ["rand", "-color"], 
    "newline": [],
    "delline": [], 
    "clear": [], 
    "show": [], 
    "exit": ["-all"], 
    "help": ["name"],
    "loop": ["rep"],
    "setcursorpos": ["posx", "posy", "-endline", "-startline", "-endoc", "-startdoc"]
}


commands = {
    "select": {
        "description": "Select text",
        "param": [
            "[start] (int,int) : (x,y) coordinates for the selection start",
            "[end] (int,int) : (x,y) coordinates for the selection end",
            "[-all] (switch) : select all text"
        ],
        "exemples": ["select end=2,2     # Will select all text before line 2, column 2"]
    },
    "copy": {
        "description": "Copy text from the current notepad content",
        "param": [
            "[No parameter] : copy from current cursor selection", 
            "[start] (int,int) : (x,y) coordinates for the copy start",
            "[end] (int,int) : (x,y) coordinates for the copy end" ,
            "[-all] (switch) : copy all text"
        ],
        "exemples": [
            "copy    # Copy from current cursor selection",
            "copy start=1,2    # Copy all text after line 1, column 2"
        ],
    },
    "upper": {
        "description": "Upper a line",
        "param": [
            "[No parameters] : Upper line at current cursor position",
            "[line] (int) : y coordinate of the selected line",
            "[all] (switch) : Upper every line"
        ],
        "exemples": [""]
    },
    "lower": {
        "description": "Lower a line",
        "param": [
            "[No parametes] : Lower line at current cursor position",
            "[line] (int) : y coordinate of the selected line",
            "[all] (switch) : Lower every line"
        ],
        "exemples": ""
    },
    "insert": { 
        "description": "Insert text at specified line",
        "param": [
            "[text] (str) : Text content",
            "[line] (int) : Line idx",
            "[x] (int) : X position inside line",
            "[start] (switch) : Will insert at line start",
            "[end] (switch) : Will insert at line end"
        ],
        "exemples": ""
    },
    "inserthour": { 
        "description": "Insert current hour",
        "param": [
            "[No parameters] : Insert current hour at current cursor position",
            "[pos] : (int,int) : Insert current hour at (x,y) coordinates"
        ],
        "exemples": ""
    },
    "insertdate": {
        "description": "Insert current date",
        "param": [
            "[No parameters] : Insert current date at current cursor position",
            "[pos] : (int,int) : Insert current date at (x,y) coordinates"
        ],
        "exemples": ""
    },
    "save": { 
        "description": "Save current file at designated location",
        "param": [
            "[No parameters] : Save file to current directory as 'txt_file.txt'",
            "[directory] (str) : Path to the saved file",
            "[name] (str) : Name of the saved file",
            "[fullpath] (str) : Full file path",
        ],
        "exemples": ""
    },
    "load": {
        "description": "Load a .txt file or a macro file",
        "param": [
            "[fullpath] (str) : Full file path",
            "[macro] (switch) : If present, will treat as macro file"
        ],
        "exemples": ""
    },
    "setdocstyle": { 
        "description": "Set style for the notepad window ",
        "param": [
            "[bg] (int,int,int) : Set background for the window",
            "[line] (int,int,int) : Set every line background color",
            "[text] (int,int,int) : Set every line text color",
            "[cursor] (int,int,int) : Set cursor color",
            "[cursorwidth] (int) : Set cursor width",
            "[cursorheight] (int) : Set cursor height",
        ],
        "exemples": ""
    },
    "setcmdstyle": {
        "description": "Set style for the command window ",
        "param": [
            "[bg] (int,int,int) : Set background for the window",
            "[line] (int,int,int) : Set every line background color",
            "[text] (int,int,int) : Set every line text color",
            "[font] (str) : Set the font"
        ],
        "exemples": ""
    },
    "setlinestyle": {
        "description": "Set style for a line",
        "param": [
            "[No parameter] : Current cursor pos",
            "[idx] (int) : Line idx",
            "[line] (int,int,int) : Set background color for the line",
            "[text] (int,int,int) : Set text color for the line",
        ],
        "exemples": ""
    },
    "newdoc": { 
        "description": "Creates an empty doc",
        "param": [
            "[No parameters] : Creates empty doc",
            "[rand] (int,int) : Random doc with X Maximum lines and Y maximum line lenght",
            "[color] (switch) : If present, will add random color to text and lines"
        ],
        "exemples": ""
    },
    "newline": { 
        "description": "Add an empty line",
        "param" : [
            "[No parameters] : Add line at current cursor position"
        ],
        "exemples" : ""
    },
    "delline": { 
        "description": "Deletes a line",
        "param": [
            "[No parameters] : deletes line at current cursor position"
        ],
        "exemples": ""
    },
    "clear": {
        "description": "Clear the cmd window",
        "param": [
            "[No parameters]",
        ],
        "exemples": ""
    },
    "show": { 
        "description": "Show the list of all the commands",
        "param": [
            "[No parameters] : Show the list of all the commands",
        ],
        "exemples": ""
    },
    "exit": { 
        "description": "Exit cmd",
        "param": [
            "[No parameters] : Exit cmd",
            "[all] (switch): Exit the entire app",
        ],
        "exemples": ""
    },
    "help": { 
        "description": "Show the help for the specified command",
        "param": [
            "[No parameters] : Show the full help for the cmd",
            "[?] (str) : Show help for the command",
        ],
        "exemples": ""
    },
    "loop": {
        "description": "Show the help for the specified command",
        "param": [
            "[No parameters] : Show the full help for the cmd",
            "[command] (str) : Show help for the command",
        ],
        "exemples": ""
    },
    "setcursorpos": {

    }
}
