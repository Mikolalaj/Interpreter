from typing import List
from src.lexer import Lexer
from src.source import StringSource
from src.tokens import Token
from src.parser.parser import Parser


def getObjects(tokens: List[Token]):
    parser = Parser(Lexer(StringSource("")), tokens=tokens)
    return parser.parse()
