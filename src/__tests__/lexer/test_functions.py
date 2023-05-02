from src.tokens import IdentifierValueToken, StringValueToken, Token, Position, IntValueToken
from src.token_type import TokenType
from .utils import getTokens


class TestFunctions:
    def testSimpleNoArguments(self):
        code = """
            function test() {
                return 1
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 9

        assert tokens[0] == Token(startPosition=Position(line=1, column=1), type=TokenType.T_FUNCTION)
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=10), length=4, value="test")
        assert tokens[2] == Token(startPosition=Position(line=1, column=14), type=TokenType.T_LPARENT)
        assert tokens[3] == Token(startPosition=Position(line=1, column=15), type=TokenType.T_RPARENT)
        assert tokens[4] == Token(startPosition=Position(line=1, column=17), type=TokenType.T_LBRACKET)
        assert tokens[5] == Token(startPosition=Position(line=2, column=5), type=TokenType.T_RETURN)
        assert tokens[6] == IntValueToken(startPosition=Position(line=2, column=12), length=1, value=1)
        assert tokens[7] == Token(startPosition=Position(line=3, column=1), type=TokenType.T_RBRACKET)
        assert tokens[8] == Token(TokenType.VT_EOF, startPosition=Position(line=3, column=2))

    def testSimpleWithArguments(self):
        code = """
            function test(a, b) {
                return a + b
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 14

        assert tokens[0] == Token(startPosition=Position(line=1, column=1), type=TokenType.T_FUNCTION)
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=10), length=4, value="test")
        assert tokens[2] == Token(startPosition=Position(line=1, column=14), type=TokenType.T_LPARENT)
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=1, column=15), length=1, value="a")
        assert tokens[4] == Token(startPosition=Position(line=1, column=16), type=TokenType.T_COMMA)
        assert tokens[5] == IdentifierValueToken(startPosition=Position(line=1, column=18), length=1, value="b")
        assert tokens[6] == Token(startPosition=Position(line=1, column=19), type=TokenType.T_RPARENT)
        assert tokens[7] == Token(startPosition=Position(line=1, column=21), type=TokenType.T_LBRACKET)
        assert tokens[8] == Token(startPosition=Position(line=2, column=5), type=TokenType.T_RETURN)
        assert tokens[9] == IdentifierValueToken(startPosition=Position(line=2, column=12), length=1, value="a")
        assert tokens[10] == Token(startPosition=Position(line=2, column=14), type=TokenType.T_PLUS)
        assert tokens[11] == IdentifierValueToken(startPosition=Position(line=2, column=16), length=1, value="b")
        assert tokens[12] == Token(startPosition=Position(line=3, column=1), type=TokenType.T_RBRACKET)
        assert tokens[13] == Token(TokenType.VT_EOF, startPosition=Position(line=3, column=2))

    def testFunctionCall(self):
        code = """
            add(2, 3)
            print("test")
        """

        tokens = getTokens(code)
        assert len(tokens) == 11

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=3, value="add")
        assert tokens[1] == Token(startPosition=Position(line=1, column=4), type=TokenType.T_LPARENT)
        assert tokens[2] == IntValueToken(startPosition=Position(line=1, column=5), value=2, length=1)
        assert tokens[3] == Token(startPosition=Position(line=1, column=6), type=TokenType.T_COMMA)
        assert tokens[4] == IntValueToken(startPosition=Position(line=1, column=8), value=3, length=1)
        assert tokens[5] == Token(startPosition=Position(line=1, column=9), type=TokenType.T_RPARENT)
        assert tokens[6] == IdentifierValueToken(startPosition=Position(line=2, column=1), length=5, value="print")
        assert tokens[7] == Token(startPosition=Position(line=2, column=6), type=TokenType.T_LPARENT)
        assert tokens[8] == StringValueToken(startPosition=Position(line=2, column=7), length=6, value="test")
        assert tokens[9] == Token(startPosition=Position(line=2, column=13), type=TokenType.T_RPARENT)
        assert tokens[10] == Token(TokenType.VT_EOF, startPosition=Position(line=2, column=14))
