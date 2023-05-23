from src.parser.parser import Parser


class Interpreter:
    def __init__(self, parser: Parser) -> None:
        self.parser = parser
