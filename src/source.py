# STDIN_EOT_TEXT = "DONE"


from .tokens import Position


class Source:
    def __init__(self) -> None:
        self.position: Position = Position(line=0, column=0)

    def readNextCharacter(self) -> str:
        return ""

    def isEndOfSource(self) -> bool:
        return False

    def getPosition(self) -> Position:
        return self.position.copy()


class FileSource(Source):
    def __init__(self, path):
        self.fileStream = open(path, "r")
        self.eof = False

    def readNextCharacter(self) -> str:
        char = self.fileStream.read(1)
        if not char:
            self.eof = True
        return char

    def isEndOfSource(self) -> bool:
        return self.eof

    def __del__(self):
        self.fileStream.close()


class StringSource(Source):
    def __init__(self, text):
        self.text = text + "\0"
        self.index = 0
        self.position = Position(line=1, column=0)

    def readNextCharacter(self) -> str:
        if self.index < len(self.text):
            char = self.text[self.index]
            self.position = self.position.getNextLine() if char == "\n" else self.position.getNextCharacter()
            self.index += 1
            return char
        return ""

    def isEndOfSource(self) -> bool:
        return self.index >= len(self.text)


# class StdInSource(Source):
#     def __init__(self):
#         self.text = None

#     def readNextCharacter(self):
#         self.text = input("stdin code > ")
#         return self.text

#     def isEndOfSource(self):
#         return self.text == STDIN_EOT_TEXT
