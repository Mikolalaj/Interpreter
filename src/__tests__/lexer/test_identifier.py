from src.tokens import IdentifierValueToken, Token, Position, IntValueToken
from src.token_type import TokenType
from .utils import getTokens


class TestIdentifier:
    def testIdentifier(self, capfd):
        code = """
            jp2 gmd
             2asd
            3qq=
            a@d3
            d3
        """

        tokens = getTokens(code)

        out, _ = capfd.readouterr()
        assert (
            out
            == """LexerError: Invalid character `a` in number at [Line 2, Column 2]
LexerError: Invalid character `q` in number at [Line 3, Column 1]
LexerError: Invalid character `@` at [Line 4, Column 2]
"""
        )
        assert len(tokens) == 6

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=3, value="jp2")
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=3, value="gmd")
        assert tokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=4))
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=1, value="a")
        assert tokens[4] == IdentifierValueToken(startPosition=Position(line=4, column=3), length=2, value="d3")
        assert tokens[5] == IdentifierValueToken(startPosition=Position(line=5, column=1), length=2, value="d3")

    def testIdentifierWithUnderscore(self):
        code = """
            let _a = 1
            let _a_ = 2
            let _a_1 = 3
            let _a_1_ = 4
            let a_1_ = 5
        """

        tokens = getTokens(code)
        assert len(tokens) == 20

        assert tokens[0] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=1, column=1))
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=2, value="_a")
        assert tokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=8))
        assert tokens[3] == IntValueToken(startPosition=Position(line=1, column=10), length=1, value=1)
        assert tokens[4] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=2, column=1))
        assert tokens[5] == IdentifierValueToken(startPosition=Position(line=2, column=5), length=3, value="_a_")
        assert tokens[6] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=9))
        assert tokens[7] == IntValueToken(startPosition=Position(line=2, column=11), length=1, value=2)
        assert tokens[8] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=3, column=1))
        assert tokens[9] == IdentifierValueToken(startPosition=Position(line=3, column=5), length=4, value="_a_1")
        assert tokens[10] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=10))
        assert tokens[11] == IntValueToken(startPosition=Position(line=3, column=12), length=1, value=3)
        assert tokens[12] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=4, column=1))
        assert tokens[13] == IdentifierValueToken(startPosition=Position(line=4, column=5), length=5, value="_a_1_")
        assert tokens[14] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=4, column=11))
        assert tokens[15] == IntValueToken(startPosition=Position(line=4, column=13), length=1, value=4)
        assert tokens[16] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=5, column=1))
        assert tokens[17] == IdentifierValueToken(startPosition=Position(line=5, column=5), length=4, value="a_1_")
        assert tokens[18] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=5, column=10))
        assert tokens[19] == IntValueToken(startPosition=Position(line=5, column=12), length=1, value=5)
