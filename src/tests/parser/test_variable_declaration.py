from typing import List

from lexer.token_type import TokenType
from .parser_utils import getObjects
from parser.nodes import Argument, Assignment, LiteralInt, ObjectConstructor, ObjectType, VariableDeclaration

from lexer.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestAssignment:
    def testIntAssignment(self) -> None:
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
            startPosition=Position(0, 0), assignment=Assignment(Position(0, 0), "a", LiteralInt(Position(0, 8), 1))
        )

    def testObjectDeclaration(self) -> None:
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
                Position(0, 0),
                "a",
                ObjectConstructor(
                    startPosition=Position(0, 8),
                    objectType=ObjectType.TETRAHEDRON,
                    arguments=[Argument(Position(0, 20), "edge", LiteralInt(Position(0, 25), 3))],
                ),
            ),
        )
