from lexer.tokens import BooleanValueToken, IdentifierValueToken, Token, Position, IntValueToken
from lexer.token_type import TokenType
from .lexer_utils import getTokens


class TestLoops:
    def testWhileTrue(self):
        code = """
            while(true) { }
        """

        tokens = getTokens(code)
        assert len(tokens) == 7

        assert tokens[0] == Token(type=TokenType.T_WHILE, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=6))
        assert tokens[2] == BooleanValueToken(startPosition=Position(line=1, column=7), value=True)
        assert tokens[3] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=11))
        assert tokens[4] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=13))
        assert tokens[5] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=1, column=15))
        assert tokens[6] == Token(TokenType.VT_EOF, startPosition=Position(line=1, column=16))

    def testWhileWithContinueBreak(self):
        code = """
            while(i<5) {
                continue
                break
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 11

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
        assert tokens[10] == Token(TokenType.VT_EOF, startPosition=Position(line=4, column=2))

    def testForeach(self):
        code = """
            let arr = [1, 2, 3]
            foreach(i in arr) {
                print(i)
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 23

        assert tokens[0] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=1, column=1))
        assert tokens[1] == IdentifierValueToken(value="arr", length=3, startPosition=Position(line=1, column=5))
        assert tokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=9))
        assert tokens[3] == Token(type=TokenType.T_LSQBRACKET, startPosition=Position(line=1, column=11))
        assert tokens[4] == IntValueToken(value=1, length=1, startPosition=Position(line=1, column=12))
        assert tokens[5] == Token(type=TokenType.T_COMMA, startPosition=Position(line=1, column=13))
        assert tokens[6] == IntValueToken(value=2, length=1, startPosition=Position(line=1, column=15))
        assert tokens[7] == Token(type=TokenType.T_COMMA, startPosition=Position(line=1, column=16))
        assert tokens[8] == IntValueToken(value=3, length=1, startPosition=Position(line=1, column=18))
        assert tokens[9] == Token(type=TokenType.T_RSQBRACKET, startPosition=Position(line=1, column=19))
        assert tokens[10] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=2, column=1))
        assert tokens[11] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=2, column=8))
        assert tokens[12] == IdentifierValueToken(value="i", length=1, startPosition=Position(line=2, column=9))
        assert tokens[13] == Token(type=TokenType.T_IN, startPosition=Position(line=2, column=11))
        assert tokens[14] == IdentifierValueToken(value="arr", length=3, startPosition=Position(line=2, column=14))
        assert tokens[15] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=2, column=17))
        assert tokens[16] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=2, column=19))
        assert tokens[17] == IdentifierValueToken(value="print", length=5, startPosition=Position(line=3, column=5))
        assert tokens[18] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=3, column=10))
        assert tokens[19] == IdentifierValueToken(value="i", length=1, startPosition=Position(line=3, column=11))
        assert tokens[20] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=3, column=12))
        assert tokens[21] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=4, column=1))
        assert tokens[22] == Token(TokenType.VT_EOF, startPosition=Position(line=4, column=2))
