from src.tokens import FloatValueToken, IdentifierValueToken, IntValueToken, Token, Position
from src.token_type import TokenType
from .utils import getTokens


class TestNumbers:
    def testValidNumbers(self):
        code = """
            23
            5  13.111
            1.1
            0 -1
        """

        tokens = getTokens(code)
        assert len(tokens) == 7
        assert tokens[0] == IntValueToken(value=23, startPosition=Position(line=1, column=1), length=2)
        assert tokens[1] == IntValueToken(value=5, startPosition=Position(line=2, column=1), length=1)
        assert tokens[2] == FloatValueToken(value=13.111, startPosition=Position(line=2, column=4), length=6)
        assert tokens[3] == FloatValueToken(value=1.1, startPosition=Position(line=3, column=1), length=3)
        assert tokens[4] == IntValueToken(value=0, startPosition=Position(line=4, column=1), length=1)
        assert tokens[5] == Token(type=TokenType.T_MINUS, startPosition=Position(line=4, column=3))
        assert tokens[6] == IntValueToken(value=1, startPosition=Position(line=4, column=4), length=1)

    def testNotValidNumbers(self):
        code = """
            1 .3
            05
            -.2
        """

        tokens = getTokens(code)
        assert len(tokens) == 6
        assert tokens[0] == IntValueToken(value=1, startPosition=Position(line=1, column=1), length=1)
        assert tokens[1] == Token(type=TokenType.T_DOT, startPosition=Position(line=1, column=3))
        assert tokens[2] == IntValueToken(value=3, startPosition=Position(line=1, column=4), length=1)
        assert tokens[3] == Token(type=TokenType.T_MINUS, startPosition=Position(line=3, column=1))
        assert tokens[4] == Token(type=TokenType.T_DOT, startPosition=Position(line=3, column=2))
        assert tokens[5] == IntValueToken(value=2, startPosition=Position(line=3, column=3), length=1)

    def testArithmeticOperations(self):
        code = """
            1 + 2
            3-4
            5 * 6
            7/8
        """

        tokens = getTokens(code)
        assert len(tokens) == 12
        assert tokens[0] == IntValueToken(value=1, startPosition=Position(line=1, column=1), length=1)
        assert tokens[1] == Token(type=TokenType.T_PLUS, startPosition=Position(line=1, column=3))
        assert tokens[2] == IntValueToken(value=2, startPosition=Position(line=1, column=5), length=1)
        assert tokens[3] == IntValueToken(value=3, startPosition=Position(line=2, column=1), length=1)
        assert tokens[4] == Token(type=TokenType.T_MINUS, startPosition=Position(line=2, column=2))
        assert tokens[5] == IntValueToken(value=4, startPosition=Position(line=2, column=3), length=1)
        assert tokens[6] == IntValueToken(value=5, startPosition=Position(line=3, column=1), length=1)
        assert tokens[7] == Token(type=TokenType.T_MUL, startPosition=Position(line=3, column=3))
        assert tokens[8] == IntValueToken(value=6, startPosition=Position(line=3, column=5), length=1)
        assert tokens[9] == IntValueToken(value=7, startPosition=Position(line=4, column=1), length=1)
        assert tokens[10] == Token(type=TokenType.T_DIV, startPosition=Position(line=4, column=2))
        assert tokens[11] == IntValueToken(value=8, startPosition=Position(line=4, column=3), length=1)

    def testNumberVariableInitialization(self):
        code = """
            let a = 1
            a=2.3
            c=0
        """

        tokens = getTokens(code)
        assert len(tokens) == 10
        assert tokens[0] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=1, column=1))
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=1, value="a")
        assert tokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=7))
        assert tokens[3] == IntValueToken(value=1, startPosition=Position(line=1, column=9), length=1)
        assert tokens[4] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=1, value="a")
        assert tokens[5] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=2))
        assert tokens[6] == FloatValueToken(value=2.3, startPosition=Position(line=2, column=3), length=3)
        assert tokens[7] == IdentifierValueToken(startPosition=Position(line=3, column=1), length=1, value="c")
        assert tokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=2))
        assert tokens[9] == IntValueToken(value=0, startPosition=Position(line=3, column=3), length=1)
