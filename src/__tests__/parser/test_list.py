from typing import List

from src.token_type import TokenType
from .utils import getObjects
from src.parser.nodes import Assignment, LemonList, LemonListValue, LiteralInt

from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestList:
    def testListOfIntegers(self):
        # a = [1, 2, 3]
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            Token(TokenType.T_LSQBRACKET, Position(0, 4)),
            IntValueToken(Position(0, 5), 1, 1),
            Token(TokenType.T_COMMA, Position(0, 6)),
            IntValueToken(Position(0, 8), 1, 2),
            Token(TokenType.T_COMMA, Position(0, 9)),
            IntValueToken(Position(0, 11), 1, 3),
            Token(TokenType.T_RSQBRACKET, Position(0, 12)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a",
            LemonList(
                values=[
                    LemonListValue(LiteralInt(Position(0, 5), 1)),
                    LemonListValue(LiteralInt(Position(0, 8), 2)),
                    LemonListValue(LiteralInt(Position(0, 11), 3)),
                ]
            ),
        )
