from src.tokens import IdentifierValueToken, Token, Position, IntValueToken
from src.token_type import TokenType
from .utils import getTokens


class TestLoops:
    def testWhileTrue(self):
        code = """
            while(true) { }
        """

        tokens = getTokens(code)
        assert len(tokens) == 6

        assert tokens[0] == Token(type=TokenType.T_WHILE, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=6))
        assert tokens[2] == Token(type=TokenType.T_TRUE, startPosition=Position(line=1, column=7))
        assert tokens[3] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=11))
        assert tokens[4] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=13))
        assert tokens[5] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=1, column=15))

    def testWhileWithContinueBreak(self):
        code = """
            while(i<5) {
                continue
                break
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 10

        assert tokens[0] == Token(type=TokenType.T_WHILE, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=6))
        assert tokens[2] == IdentifierValueToken(value="i", length=1, startPosition=Position(line=1, column=7))
        assert tokens[3] == Token(type=TokenType.T_LESS, startPosition=Position(line=1, column=8))
        assert tokens[4] == IntValueToken(value=5, length=1, startPosition=Position(line=1, column=9))
        assert tokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=10))
        assert tokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=12))
        assert tokens[7] == Token(type=TokenType.T_CONTINUE, startPosition=Position(line=2, column=5))
        assert tokens[8] == Token(type=TokenType.T_BREAK, startPosition=Position(line=3, column=5))
        assert tokens[9] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=4, column=1))

    def testForeach(self):
        code = """
            let arr = [1, 2, 3]
            foreach(i in arr) {
                print(i)
            }
        """