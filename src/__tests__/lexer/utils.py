from src.tokens import Token
from src.source import StringSource
from src.lexer import Lexer


def removeSpaces(string: str) -> str:
    # Removes 12 spaces from the beginning of each line
    return "\n".join([line[12:] for line in string.splitlines()[1:-1]])


def getTokens(code: str, ifRemoveSpaces=True) -> list[Token]:
    if ifRemoveSpaces:
        code = removeSpaces(code)
    lexer = Lexer(source=StringSource(code))
    return lexer.allTokens
