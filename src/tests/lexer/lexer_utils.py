from lexer.tokens import Token
from lexer.source import StringSource
from lexer.lexer import Lexer


def removeSpaces(string: str) -> str:
    # Removes 12 spaces from the beginning of each line
    return "\n".join([line[12:] for line in string.splitlines()[1:-1]])


def getTokens(code: str, ifRemoveSpaces=True) -> list[Token]:
    if ifRemoveSpaces:
        code = removeSpaces(code)
    lexer = Lexer(source=StringSource(code))
    return lexer._getAllTokens()
