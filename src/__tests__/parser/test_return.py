from .utils import getObjects
from src.parser.nodes import AdditiveExpression, LiteralIndentifier, LiteralInt, ReturnStatement
from src.token_type import TokenType
from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


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
                left=LiteralIndentifier(value="a", startPosition=Position(0, 7)),
                right=LiteralInt(value=1, startPosition=Position(0, 11)),
                operator="+",
            ),
        )
