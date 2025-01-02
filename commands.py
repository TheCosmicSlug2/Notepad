parameters = {
    "newdoc": ["rand", "-color"], 
    "newline": [],
    "delline": [], 
    "setcursorpos": ["posx", "posy", "-endline", "-startline", "-endoc", "-startdoc"],
    "select": ["start", "end", "-all"],
    "copy": ["start", "end", "-all"],
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

    "clear": [], 
    "show": [], 
    "exit": ["-all"], 
    "help": ["name"],

    "loop": ["rep"],
    "sleep": ["time"],
}

commands = {
    "==== Text and Lines ====": None,
    "newdoc": {
        "description": "Creates an empty document",
        "param": [
            "[No parameters] : Creates an empty document",
            "[rand] (int,int) : Generates a random document with X maximum lines and Y maximum line length",
            "[color] (switch) : If present, will add random colors to text and lines"
        ],
        "exemples": [
            "'newdoc rand=10,20' # Creates a new document with a maximum of 10 lines and 20 characters per line",
            "'newdoc rand=15,30 -color' # Creates a document with random colors and 15 lines max, 30 characters per line"
        ]
    },
    "newline": {
        "description": "Adds an empty line",
        "param": [
            "[No parameters] : Adds a line at the current cursor position"
        ],
        "exemples": [
            "'newline' # Adds an empty line at the current cursor position",
        ]
    },
    "delline": {
        "description": "Deletes a line",
        "param": [
            "[No parameters] : Deletes the line at the current cursor position"
        ],
        "exemples": [
            "'delline' # Deletes the current line at the cursor position",
        ]
    },
    "setcursorpos": {
        "description": "Sets the cursor position",
        "param": [
            "[pos] (int,int) : Sets the position at the designated X,Y coordinates",
            "[startline] (switch) : Sets the position at the start of the current line",
            "[startdoc] (switch) : Sets the position at the start of the document",
            "[endline] (switch) : Sets the position at the end of the current line",
            "[enddoc] (switch) : Sets the position at the end of the document"
        ],
        "exemples": [
            "'setcursorpos pos=3,4' # Moves the cursor to position (3,4)",
            "'setcursorpos -startdoc' # Places the cursor at the start of the document"
        ]
    },
    "select": {
        "description": "Selects text",
        "param": [
            "[start] (int,int) : (x,y) coordinates for the selection start",
            "[end] (int,int) : (x,y) coordinates for the selection end",
            "[-all] (switch) : Selects all text"
        ],
        "exemples": [
            "'select start=1,1 end=3,5' # Selects all text between positions (1,1) and (3,5)",
            "'select -all' # Selects all text in the document"
        ]
    },
    "copy": {
        "description": "Copies text from the current notepad content",
        "param": [
            "[No parameters] : Copies from the current cursor selection",
            "[start] (int,int) : (x,y) coordinates for the copy start",
            "[end] (int,int) : (x,y) coordinates for the copy end",
            "[-all] (switch) : Copies all text"
        ],
        "exemples": [
            "'copy' # Copies text from the current cursor selection",
            "'copy start=1,2 end=3,4' # Copies text between positions (1,2) and (3,4)"
        ]
    },
    "upper": {
        "description": "Converts text to uppercase",
        "param": [
            "[No parameters] : Converts the line at the current cursor position to uppercase",
            "[line] (int) : The y-coordinate of the selected line",
            "[-all] (switch) : Converts all lines to uppercase"
        ],
        "exemples": [
            "'upper line=5' # Converts line 5 to uppercase",
            "'upper -all' # Converts the entire document to uppercase"
        ]
    },
    "lower": {
        "description": "Converts text to lowercase",
        "param": [
            "[No parameters] : Converts the line at the current cursor position to lowercase",
            "[line] (int) : The y-coordinate of the selected line",
            "[-all] (switch) : Converts all lines to lowercase"
        ],
        "exemples": [
            "'lower line=3' # Converts line 3 to lowercase",
            "'lower -all' # Converts the entire document to lowercase"
        ]
    },
    "insert": {
        "description": "Inserts text at a specified position",
        "param": [
            "[text] (str) : Text content to insert",
            "[line] (int) : Line index for insertion",
            "[x] (int) : X position within the line",
            "[-start] (switch) : Inserts text at the start of the line",
            "[-end] (switch) : Inserts text at the end of the line"
        ],
        "exemples": [
            "'insert text=\"Hello\" line=3 x=5' # Inserts the text \"Hello\" at line 3, position 5",
            "'insert text=\"End of document\" end' # Appends the text \"End of document\" to the document"
        ]
    },
    "inserthour": {
        "description": "Inserts the current hour",
        "param": [
            "[No parameters] : Inserts the current hour at the cursor position",
            "[pos] (int,int) : Inserts the current hour at the specified (x,y) coordinates"
        ],
        "exemples": [
            "'inserthour pos=2,3' # Inserts the current hour at position (2,3)",
            "'inserthour' # Inserts the current hour at the current cursor position"
        ]
    },
    "insertdate": {
        "description": "Insert current date",
        "param": [
            "[No parameters] : Insert current date at current cursor position",
            "[pos] (int,int) : Insert current date at (x,y) coordinates"
        ],
        "exemples": ""
    },
    "==== Local ====": None,
    "save": {
        "description": "Saves the current file to a specified location",
        "param": [
            "[No parameters] : Saves the file to the current directory as 'txt_file.txt'",
            "[directory] (str) : Specifies the path to save the file",
            "[name] (str) : Specifies the name of the saved file",
            "[fullpath] (str) : Specifies the full file path"
        ],
        "exemples": [
            "'save directory=\"C:/Documents\" name=\"myfile.txt\"' # Saves the file to 'C:/Documents' with the name 'myfile.txt'",
            "'save fullpath=\"C:/Documents/myfile.txt\"' # Saves the file to the specified full path"
        ]
    },
    "load": {
        "description": "Loads a .txt file or a macro file",
        "param": [
            "[fullpath] (str) : Specifies the full file path to load",
            "[-macro] (switch) : If present, loads the file as a macro"
        ],
        "exemples": [
            "'load fullpath=\"C:/Documents/myfile.txt\"' # Loads the file located at 'C:/Documents/myfile.txt'",
            "'load fullpath=\"C:/Scripts/macro.mcr\" -macro' # Loads the file as a macro"
        ]
    },
    "==== Style and Customisation ====": None,
    "setdocstyle": {
        "description": "Sets the style for the notepad window",
        "param": [
            "[bg] (int,int,int) : Sets the background color of the window",
            "[line] (int,int,int) : Sets the background color of every line",
            "[text] (int,int,int) : Sets the text color of every line",
            "[cursor] (int,int,int) : Sets the cursor color",
            "[cursorwidth] (int) : Sets the cursor width",
            "[cursorheight] (int) : Sets the cursor height"
        ],
        "exemples": [
            "'setdocstyle bg=255,255,255 text=0,0,0' # Sets a white background and black text color",
            "'setdocstyle cursor=255,0,0 cursorwidth=2' # Sets a red cursor with width 2"
        ]
    },
    "setcmdstyle": {
        "description": "Sets the style for the command window",
        "param": [
            "[bg] (int,int,int) : Sets the background color of the command window",
            "[line] (int,int,int) : Sets the background color of every line in the command window",
            "[text] (int,int,int) : Sets the text color in the command window",
            "[font] (str) : Sets the font used in the command window"
        ],
        "exemples": [
            "'setcmdstyle bg=0,0,0 text=255,255,255 font=\"Courier New\"' # Sets a black background, white text, and 'Courier New' font",
            "'setcmdstyle line=100,100,100' # Sets the line background color to gray"
        ]
    },
    "setlinestyle": {
        "description": "Sets the style for a specific line",
        "param": [
            "[No parameters] : Applies style to the current cursor line",
            "[idx] (int) : Specifies the line index",
            "[line] (int,int,int) : Sets the background color for the line",
            "[text] (int,int,int) : Sets the text color for the line"
        ],
        "exemples": [
            "'setlinestyle idx=3 line=0,255,0' # Sets the background of line 3 to green",
            "'setlinestyle idx=4 text=255,0,0' # Sets the text color of line 4 to red"
        ]
    },
    "==== CMD exclusive ====": None,
    "clear": {
        "description": "Clears the command window",
        "param": [
            "[No parameters] : Clears the command window"
        ],
        "exemples": [
            "'clear' # Clears all content from the command window"
        ]
    },
    "show": {
        "description": "Displays the list of all available commands",
        "param": [
            "[No parameters] : Shows the list of commands"
        ],
        "exemples": [
            "'show' # Displays the list of all commands"
        ]
    },
    "exit": {
        "description": "Exits the command window or the entire app",
        "param": [
            "[No parameters] : Exits the command window",
            "[-all] (switch) : Exits the entire app"
        ],
        "exemples": [
            "'exit' # Exits the command window",
            "'exit -all' # Closes the entire application"
        ]
    },
    "help": {
        "description": "Shows help information for a specified command",
        "param": [
            "[No parameters] : Displays the full help for all commands",
            "[name] (str) : Displays help for the specified command"
        ],
        "exemples": [
            "'help' # Displays the full help menu",
            "'help name=\"newdoc\"' # Displays help for the 'newdoc' command"
        ]
    },
    "==== Macro exclusive ====": None,
    "loop": {
        "description": "Repeats a command list multiple times \n CANNOT BE USED WITHOUT 'ENDLOOP'",
        "param": [
            "[rep] (int) : Specifies the number of repetitions",
        ],
        "exemples": [
            "'loop rep=5 # Will tell the macro that every command beetween this and 'endloop' will be executed 5 time"
        ]
    },
    "sleep": {
        "description": "Stop the program for a period of time",
        "param": [
            "[time] (int | float) : Sleep duration"
        ],
        "exemples": [
            "sleep time=10 # Stop the program for 10 seconds"
        ]
    }
}
