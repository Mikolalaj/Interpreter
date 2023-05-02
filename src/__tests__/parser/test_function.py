from .utils import getObjects
from src.parser.nodes import FunctionDefinition, Parameter
from src.token_type import TokenType
from src.tokens import IdentifierValueToken, Position, Token


class TestFunctionDefinition:
    def testWithArguments(self):
        tokens = [
            Token(type=TokenType.T_FUNCTION, startPosition=Position(0, 0)),
            IdentifierValueToken(value="test", startPosition=Position(0, 9), length=4),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 13)),
            IdentifierValueToken(value="a", startPosition=Position(0, 14), length=1),
            Token(type=TokenType.T_COMMA, startPosition=Position(0, 15)),
            IdentifierValueToken(value="b", startPosition=Position(0, 17), length=1),
            Token(type=TokenType.T_COMMA, startPosition=Position(0, 18)),
            IdentifierValueToken(value="c", startPosition=Position(0, 20), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 21)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 23)),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(0, 25)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == FunctionDefinition(
            name="test",
            parameters=[Parameter("a"), Parameter("b"), Parameter("c")],
            body="body",
        )

    def testWithoutArguments(self):
        tokens = [
            Token(type=TokenType.T_FUNCTION, startPosition=Position(0, 0)),
            IdentifierValueToken(value="test", startPosition=Position(0, 9), length=4),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 13)),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 14)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 16)),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(0, 18)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == FunctionDefinition(
            name="test",
            parameters=[],
            body="body",
        )
