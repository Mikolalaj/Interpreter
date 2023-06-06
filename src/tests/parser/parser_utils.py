from typing import List
from lexer.lexer import Lexer
from lexer.source import StringSource
from lexer.tokens import Token
from parser.parser import Parser


def getObjects(tokens: List[Token]):
    parser = Parser(Lexer(StringSource("")), tokens=tokens)
    return parser.parse()
