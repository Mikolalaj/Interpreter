from typing import List

from src.token_type import TokenType
from .utils import getObjects
from src.parser.nodes import Assignment, LiteralInt, ObjectConstructor, VariableDeclaration

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

    def testObjectDeclaration(self):
        # let a = Tetrahedron(edge=3)
        tokens: List[Token] = [
            Token(TokenType.T_VARIABLE, Position(0, 0)),
            IdentifierValueToken(Position(0, 4), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 6)),
            Token(TokenType.T_TETRAHEDRON, Position(0, 8)),
            Token(TokenType.T_LPARENT, Position(0, 19)),
            IdentifierValueToken(Position(0, 20), 1, "edge"),
            Token(TokenType.T_ASSIGN, Position(0, 24)),
            IntValueToken(Position(0, 25), 1, 3),
            Token(TokenType.T_RPARENT, Position(0, 26)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == VariableDeclaration(
            startPosition=Position(0, 0),
            assignment=Assignment(
                "a",
                ObjectConstructor(
                    startPosition=Position(0, 8),
                    objectType=TokenType.T_TETRAHEDRON,
                    arguments=[Assignment("edge", LiteralInt(Position(0, 25), 3))],
                ),
            ),
        )
