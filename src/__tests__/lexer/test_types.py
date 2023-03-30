import math
from src.tokens import BooleanValueToken, IdentifierValueToken, Token, Position, IntValueToken, FloatValueToken, StringValueToken
from src.token_type import TokenType
from .utils import getTokens


class TestTypes:
    def testIntegerTypes(self):
        code = """
            a = 1
            b = 0
            c = -1
            d=-1
        """

        tokens = getTokens(code)

        assert len(tokens) == 14

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == IntValueToken(startPosition=Position(line=1, column=5), length=1, value=1)
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=1, value="b")
        assert tokens[4] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=3))
        assert tokens[5] == IntValueToken(startPosition=Position(line=2, column=5), length=1, value=0)
        assert tokens[6] == IdentifierValueToken(startPosition=Position(line=3, column=1), length=1, value="c")
        assert tokens[7] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=3))
        assert tokens[8] == Token(type=TokenType.T_MINUS, startPosition=Position(line=3, column=5))
        assert tokens[9] == IntValueToken(startPosition=Position(line=3, column=6), length=1, value=1)
        assert tokens[10] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=1, value="d")
        assert tokens[11] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=4, column=2))
        assert tokens[12] == Token(type=TokenType.T_MINUS, startPosition=Position(line=4, column=3))
        assert tokens[13] == IntValueToken(startPosition=Position(line=4, column=4), length=1, value=1)

    def testFloatTypes(self):
        code = """
            a = 1.0
            b = 0.0
            c = -1.0
            d=-1.0
        """

        tokens = getTokens(code)

        assert len(tokens) == 14

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == FloatValueToken(startPosition=Position(line=1, column=5), length=3, value=1.0)
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=1, value="b")
        assert tokens[4] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=3))
        assert tokens[5] == FloatValueToken(startPosition=Position(line=2, column=5), length=3, value=0.0)
        assert tokens[6] == IdentifierValueToken(startPosition=Position(line=3, column=1), length=1, value="c")
        assert tokens[7] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=3))
        assert tokens[8] == Token(type=TokenType.T_MINUS, startPosition=Position(line=3, column=5))
        assert tokens[9] == FloatValueToken(startPosition=Position(line=3, column=6), length=3, value=1.0)
        assert tokens[10] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=1, value="d")
        assert tokens[11] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=4, column=2))
        assert tokens[12] == Token(type=TokenType.T_MINUS, startPosition=Position(line=4, column=3))
        assert tokens[13] == FloatValueToken(startPosition=Position(line=4, column=4), length=3, value=1.0)

    def testBoolTypes(self):
        code = """
            a = true
            b = false
        """

        tokens = getTokens(code)

        assert len(tokens) == 6

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == BooleanValueToken(startPosition=Position(line=1, column=5), value=True)
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=1, value="b")
        assert tokens[4] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=3))
        assert tokens[5] == BooleanValueToken(startPosition=Position(line=2, column=5), value=False)

    def testStringTypes(self):
        code = """
            a = "hello"
            b = "hello world"
        """

        tokens = getTokens(code)

        assert len(tokens) == 6

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == StringValueToken(startPosition=Position(line=1, column=5), length=7, value="hello")
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=1, value="b")
        assert tokens[4] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=3))
        assert tokens[5] == StringValueToken(startPosition=Position(line=2, column=5), length=13, value="hello world")

    def testConstants(self):
        code = """
            a = PI
        """

        tokens = getTokens(code)

        assert len(tokens) == 3

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == FloatValueToken(startPosition=Position(line=1, column=5), length=2, value=math.pi)
