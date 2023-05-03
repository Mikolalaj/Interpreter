from .utils import getObjects
from src.parser.nodes import Assignment, FunctionCall, FunctionDefinition, Parameter
from src.token_type import TokenType
from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestFunction:
    def testDefinitionWithParameters(self):
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

    def testDefinitionWithoutParameters(self):
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

    def testCallWithoutArguments(self):
        # test()
        tokens = [
            IdentifierValueToken(value="test", startPosition=Position(0, 1), length=4),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 5)),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 6)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == FunctionCall(
            name="test",
            arguments=[],
        )


class TestAruments:
    def testArgument(self):
        # a = 1
        tokens = [
            IdentifierValueToken(value="a", startPosition=Position(0, 1), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(0, 3)),
            IntValueToken(value=1, startPosition=Position(0, 5), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(name="a", value=1)

    def testArgumentsSingle(self):
        # (a = 1)
        tokens = [
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 0)),
            IdentifierValueToken(value="a", startPosition=Position(0, 1), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(0, 3)),
            IntValueToken(value=1, startPosition=Position(0, 5), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 6)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert type(objects[0]) == list
        assert len(objects[0]) == 1
        assert objects[0][0] == Assignment(name="a", value=1)

    def testArgumentsMultiple(self):
        # (a = 1, b = 2)
        tokens = [
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 0)),
            IdentifierValueToken(value="a", startPosition=Position(0, 1), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(0, 3)),
            IntValueToken(value=1, startPosition=Position(0, 5), length=1),
            Token(type=TokenType.T_COMMA, startPosition=Position(0, 6)),
            IdentifierValueToken(value="b", startPosition=Position(0, 8), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(0, 10)),
            IntValueToken(value=2, startPosition=Position(0, 12), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 13)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert type(objects[0]) == list
        assert len(objects[0]) == 2
        assert objects[0][0] == Assignment(name="a", value=1)
        assert objects[0][1] == Assignment(name="b", value=2)

    def testArgumentsEmpty(self):
        # ()
        tokens = [
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 0)),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 1)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert type(objects[0]) == list
        assert len(objects[0]) == 0
