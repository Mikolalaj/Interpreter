from typing import List

from src.token_type import TokenType
from .utils import getObjects
from src.parser.nodes import Assignment, LiteralInt, VariableDeclaration

from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestAssignment:
    def testIntAssignment(self):
        # let a = 1
        tokens: List[Token] = [
            Token(TokenType.T_VARIABLE, Position(0, 0)),
            IdentifierValueToken(Position(0, 4), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 6)),
            IntValueToken(Position(0, 8), 1, 1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == VariableDeclaration(
            startPosition=Position(0, 0), assignment=Assignment("a", LiteralInt(Position(0, 8), 1))
        )
