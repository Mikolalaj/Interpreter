from .tokens import Position


class LexerError(Exception):
    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position

    def __str__(self):
        return f"LexerError: {self.message} at {self.position}"

    def print_error_and_exit(self):
        print(f"Error: unexpected character: {self.message} at: {self.position}")
        exit()
