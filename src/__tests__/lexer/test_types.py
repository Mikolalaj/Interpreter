# type: ignore
from src.tokens import (
    BooleanValueToken,
    IdentifierValueToken,
    Token,
    Position,
    IntValueToken,
    FloatValueToken,
    StringValueToken,
)
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

        assert len(tokens) == 15

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

        assert len(tokens) == 15

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

        assert len(tokens) == 7

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

        assert len(tokens) == 7

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == StringValueToken(startPosition=Position(line=1, column=5), length=7, value="hello")
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=1, value="b")
        assert tokens[4] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=3))
        assert tokens[5] == StringValueToken(startPosition=Position(line=2, column=5), length=13, value="hello world")

    def testStringEscape(self):
        code = """
            "hello\\"world"
            "hello\\nworld"
            "hello\\tworld"
            "hello\\\world"
        """  # noqa: W605

        tokens = getTokens(code)

        assert len(tokens) == 5

        assert tokens[0] == StringValueToken(startPosition=Position(line=1, column=1), length=13, value='hello"world')
        assert tokens[1] == StringValueToken(startPosition=Position(line=2, column=1), length=13, value="hello\nworld")
        assert tokens[2] == StringValueToken(startPosition=Position(line=3, column=1), length=13, value="hello\tworld")
        assert tokens[3] == StringValueToken(startPosition=Position(line=4, column=1), length=13, value="hello\\world")

    def testConstants(self):
        code = """
            a = PI
        """

        tokens = getTokens(code)

        assert len(tokens) == 4

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=1, value="a")
        assert tokens[1] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=3))
        assert tokens[2] == Token(type=TokenType.T_PI, startPosition=Position(line=1, column=5))

    def testListInt(self):
        code = """
            [1, 2, 3]
        """

        tokens = getTokens(code)

        assert len(tokens) == 8
        assert tokens[0] == Token(startPosition=Position(1, 1), type=TokenType.T_LSQBRACKET)
        assert tokens[1] == IntValueToken(startPosition=Position(1, 2), length=1, value=1)
        assert tokens[2] == Token(startPosition=Position(1, 3), type=TokenType.T_COMMA)
        assert tokens[3] == IntValueToken(startPosition=Position(1, 5), length=1, value=2)
        assert tokens[4] == Token(startPosition=Position(1, 6), type=TokenType.T_COMMA)
        assert tokens[5] == IntValueToken(startPosition=Position(1, 8), length=1, value=3)
        assert tokens[6] == Token(startPosition=Position(1, 9), type=TokenType.T_RSQBRACKET)

    def testListFloat(self):
        code = """
            [2.3, 4.5, 6.7]
        """

        tokens = getTokens(code)

        assert len(tokens) == 8
        assert tokens[0] == Token(startPosition=Position(1, 1), type=TokenType.T_LSQBRACKET)
        assert tokens[1] == FloatValueToken(startPosition=Position(1, 2), length=3, value=2.3)
        assert tokens[2] == Token(startPosition=Position(1, 5), type=TokenType.T_COMMA)
        assert tokens[3] == FloatValueToken(startPosition=Position(1, 7), length=3, value=4.5)
        assert tokens[4] == Token(startPosition=Position(1, 10), type=TokenType.T_COMMA)
        assert tokens[5] == FloatValueToken(startPosition=Position(1, 12), length=3, value=6.7)
        assert tokens[6] == Token(startPosition=Position(1, 15), type=TokenType.T_RSQBRACKET)

    def testListBool(self):
        code = """
            [true, false, true]
        """

        tokens = getTokens(code)

        assert len(tokens) == 8
        assert tokens[0] == Token(startPosition=Position(1, 1), type=TokenType.T_LSQBRACKET)
        assert tokens[1] == BooleanValueToken(startPosition=Position(1, 2), value=True)
        assert tokens[2] == Token(startPosition=Position(1, 6), type=TokenType.T_COMMA)
        assert tokens[3] == BooleanValueToken(startPosition=Position(1, 8), value=False)
        assert tokens[4] == Token(startPosition=Position(1, 13), type=TokenType.T_COMMA)
        assert tokens[5] == BooleanValueToken(startPosition=Position(1, 15), value=True)
        assert tokens[6] == Token(startPosition=Position(1, 19), type=TokenType.T_RSQBRACKET)

    def testListString(self):
        code = """
            ["hello", "world"]
        """

        tokens = getTokens(code)

        assert len(tokens) == 6
        assert tokens[0] == Token(startPosition=Position(1, 1), type=TokenType.T_LSQBRACKET)
        assert tokens[1] == StringValueToken(startPosition=Position(1, 2), length=7, value="hello")
        assert tokens[2] == Token(startPosition=Position(1, 9), type=TokenType.T_COMMA)
        assert tokens[3] == StringValueToken(startPosition=Position(1, 11), length=7, value="world")
        assert tokens[4] == Token(startPosition=Position(1, 18), type=TokenType.T_RSQBRACKET)

    def testListIdentifiers(self):
        code = """
            [a, 2, 3]
        """

        tokens = getTokens(code)

        assert len(tokens) == 8
        assert tokens[0] == Token(startPosition=Position(1, 1), type=TokenType.T_LSQBRACKET)
        assert tokens[1] == IdentifierValueToken(startPosition=Position(1, 2), length=1, value="a")
        assert tokens[2] == Token(startPosition=Position(1, 3), type=TokenType.T_COMMA)
        assert tokens[3] == IntValueToken(startPosition=Position(1, 5), length=1, value=2)
        assert tokens[4] == Token(startPosition=Position(1, 6), type=TokenType.T_COMMA)
        assert tokens[5] == IntValueToken(startPosition=Position(1, 8), length=1, value=3)
        assert tokens[6] == Token(startPosition=Position(1, 9), type=TokenType.T_RSQBRACKET)
