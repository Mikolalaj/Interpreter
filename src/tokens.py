from typing import Self
from .token_type import TokenType


class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __str__(self):
        return f"[Line {self.line}, Column {self.column}]"

    def __eq__(self, other):
        return True if self.line == other.line and self.column == other.column else False

    def copy(self) -> Self:
        return Position(self.line, self.column)

    def getNextCharacter(self) -> Self:
        return Position(self.line, self.column + 1)

    def getNextLine(self) -> Self:
        return Position(self.line + 1, 0)


class Token:
    def __init__(self, type: TokenType, startPosition: Position):
        self.type = type
        self.startPosition = startPosition

    def __str__(self):
        return f"<type '{self.type.toString()}' - Start {self.startPosition}>"

    def __repr__(self):
        return f"<`{self.type.toString()}` {self.startPosition}>"

    def __eq__(self, other):
        if self.type == other.type and self.startPosition == other.startPosition:
            return True
        else:
            return False


class ValueToken(Token):
    def __init__(self, type: TokenType, startPosition: Position, value: str | int | float | bool):
        super().__init__(type, startPosition)
        self.value = value

    def __str__(self):
        return f"<type '{self.type.toString()}' - Start {self.startPosition} - value: {self.value}>"

    def __repr__(self):
        return f"<`{self.type.toString()}` {self.startPosition} - `{self.value}`>"

    def __eq__(self, valueToken: Self):
        if self.type == valueToken.type and self.value == valueToken.value and self.startPosition == valueToken.startPosition:
            return True
        else:
            return False


class StringValueToken(ValueToken):
    def __init__(self, startPosition: Position, length: int, value: str):
        super().__init__(TokenType.VT_STRING, startPosition, value)
        self.length = length


class FloatValueToken(ValueToken):
    def __init__(self, startPosition: Position, length: int, value: float):
        super().__init__(TokenType.VT_FLOAT, startPosition, value)
        self.length = length


class IntValueToken(ValueToken):
    def __init__(self, startPosition: Position, length: int, value: int):
        super().__init__(TokenType.VT_INT, startPosition, value)
        self.length = length


class BooleanValueToken(ValueToken):
    def __init__(self, startPosition: Position, value: bool):
        super().__init__(TokenType.VT_BOOLEAN, startPosition, value)
        self.length = 4 if value else 5


class IdentifierValueToken(ValueToken):
    def __init__(self, startPosition: Position, length: int, value: str):
        super().__init__(TokenType.VT_ID, startPosition, value)
        self.length = length
