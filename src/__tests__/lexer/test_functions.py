from src.tokens import IdentifierValueToken, Token, Position, IntValueToken
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
        assert len(tokens) == 8

        assert tokens[0] == Token(startPosition=Position(line=1, column=1), type=TokenType.T_FUNCTION)
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=10), length=4, value="test")
        assert tokens[2] == Token(startPosition=Position(line=1, column=14), type=TokenType.T_LPARENT)
        assert tokens[3] == Token(startPosition=Position(line=1, column=15), type=TokenType.T_RPARENT)
        assert tokens[4] == Token(startPosition=Position(line=1, column=17), type=TokenType.T_LBRACKET)
        assert tokens[5] == Token(startPosition=Position(line=2, column=5), type=TokenType.T_RETURN)
        assert tokens[6] == IntValueToken(startPosition=Position(line=2, column=12), length=1, value=1)
        assert tokens[7] == Token(startPosition=Position(line=3, column=1), type=TokenType.T_RBRACKET)

    def testSimpleWithArguments(self):
        code = """
            function test(a, b) {
                return a + b
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 13

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
