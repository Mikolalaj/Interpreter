from .tokens import Position, Token


class LexerError(Exception):
    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position

    def __str__(self):
        return f"LexerError: {self.message} at {self.position}"


class ParserError(Exception):
    def __init__(self, expected: Token | str, actualToken: Token):
        self.expected = expected
        self.actualToken = actualToken

    def __str__(self):
        return f"ParserError: Expected {self.expected} but got {self.actualToken} instead"
