
class Local:

    @staticmethod
    def save_txtfile(name: str, lines: list[list[str]]) -> None:
        with open(name, "w", encoding="utf-8") as txt_file:
            for lst_line in lines:
                str_line = "".join(lst_line) + "\r\n"
                txt_file.write(str_line)
        print(f"File saved as {name}")
    
    @staticmethod
    def load_txtfile(path: str) -> None:
        with open(path, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()  # Lire tout le contenu du fichier
        lst = contenu.split("\n")
        converted_content = []
        for strline in lst:
            line = list(strline)
            converted_content.append(line)
        print(f"File {path} loaded")
        return converted_content
