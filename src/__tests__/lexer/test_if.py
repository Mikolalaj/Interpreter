from src.tokens import IdentifierValueToken, IntValueToken, Token, Position
from src.token_type import TokenType
from .utils import getTokens


class TestIf:
    def testSingleIf(self):
        code = """
            if ( a > 3 ) {
                a = 0
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 11
        assert tokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4))
        assert tokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=6), length=1, value="a")
        assert tokens[3] == Token(type=TokenType.T_GREATER, startPosition=Position(line=1, column=8))
        assert tokens[4] == IntValueToken(value=3, startPosition=Position(line=1, column=10), length=1)
        assert tokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=12))
        assert tokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=14))
        assert tokens[7] == IdentifierValueToken(startPosition=Position(line=2, column=5), length=1, value="a")
        assert tokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=7))
        assert tokens[9] == IntValueToken(value=0, startPosition=Position(line=2, column=9), length=1)
        assert tokens[10] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1))

    def testSingleIfNoSpaces(self):
        code = "if(a>3){a=0}"

        tokens = getTokens(code, ifRemoveSpaces=False)
        assert len(tokens) == 11
        assert tokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=3))
        assert tokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=4), length=1, value="a")
        assert tokens[3] == Token(type=TokenType.T_GREATER, startPosition=Position(line=1, column=5))
        assert tokens[4] == IntValueToken(value=3, startPosition=Position(line=1, column=6), length=1)
        assert tokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=7))
        assert tokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=8))
        assert tokens[7] == IdentifierValueToken(startPosition=Position(line=1, column=9), length=1, value="a")
        assert tokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=10))
        assert tokens[9] == IntValueToken(value=0, startPosition=Position(line=1, column=11), length=1)
        assert tokens[10] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=1, column=12))

    def testIfElif(self):
        code = """
            if ( a < b ) {
                a = a - 1
            } elif ( a < 3 ) {
                a = 1
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 24
        assert tokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4))
        assert tokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=6), length=1, value="a")
        assert tokens[3] == Token(type=TokenType.T_LESS, startPosition=Position(line=1, column=8))
        assert tokens[4] == IdentifierValueToken(startPosition=Position(line=1, column=10), length=1, value="b")
        assert tokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=12))
        assert tokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=14))
        assert tokens[7] == IdentifierValueToken(startPosition=Position(line=2, column=5), length=1, value="a")
        assert tokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=7))
        assert tokens[9] == IdentifierValueToken(startPosition=Position(line=2, column=9), length=1, value="a")
        assert tokens[10] == Token(type=TokenType.T_MINUS, startPosition=Position(line=2, column=11))
        assert tokens[11] == IntValueToken(value=1, startPosition=Position(line=2, column=13), length=1)
        assert tokens[12] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1))
        assert tokens[13] == Token(type=TokenType.T_ELSEIF, startPosition=Position(line=3, column=3))
        assert tokens[14] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=3, column=8))
        assert tokens[15] == IdentifierValueToken(startPosition=Position(line=3, column=10), length=1, value="a")
        assert tokens[16] == Token(type=TokenType.T_LESS, startPosition=Position(line=3, column=12))
        assert tokens[17] == IntValueToken(startPosition=Position(line=3, column=14), length=1, value=3)
        assert tokens[18] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=3, column=16))
        assert tokens[19] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=3, column=18))
        assert tokens[20] == IdentifierValueToken(startPosition=Position(line=4, column=5), length=1, value="a")
        assert tokens[21] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=4, column=7))
        assert tokens[22] == IntValueToken(value=1, startPosition=Position(line=4, column=9), length=1)
        assert tokens[23] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=5, column=1))

    def testIfElse(self):
        code = """
            if () {
            } else () {
            }
        """

        tokens = getTokens(code)

        assert len(tokens) == 10
        assert tokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4))
        assert tokens[2] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=5))
        assert tokens[3] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=7))
        assert tokens[4] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=2, column=1))
        assert tokens[5] == Token(type=TokenType.T_ELSE, startPosition=Position(line=2, column=3))
        assert tokens[6] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=2, column=8))
        assert tokens[7] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=2, column=9))
        assert tokens[8] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=2, column=11))
        assert tokens[9] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1))
