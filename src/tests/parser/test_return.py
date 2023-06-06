from .parser_utils import getObjects
from parser.nodes import AdditiveExpression, LiteralIdentifier, LiteralInt, ReturnStatement
from lexer.token_type import TokenType
from lexer.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestReturn:
    def testReturn(self):
        # return a + 1
        tokens = [
            Token(type=TokenType.T_RETURN, startPosition=Position(0, 0)),
            IdentifierValueToken(value="a", startPosition=Position(0, 7), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 9)),
            IntValueToken(value=1, startPosition=Position(0, 11), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ReturnStatement(
            startPosition=Position(0, 0),
            expression=AdditiveExpression(
                left=LiteralIdentifier(value="a", startPosition=Position(0, 7)),
                right=LiteralInt(value=1, startPosition=Position(0, 11)),
                operator="+",
            ),
        )
