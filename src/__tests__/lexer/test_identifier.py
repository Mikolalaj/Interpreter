from src.tokens import IdentifierValueToken, Token, Position
from src.token_type import TokenType
from .utils import getTokens


class TestIdentifier:
    def testIdentifier(self, capfd):
        code = """
            jp2 gmd
             2asd
            3qq=
            d3
        """

        tokens = getTokens(code)

        out, _ = capfd.readouterr()
        assert (
            out
            == """LexerError: Invalid character `a` in number at [Line 2, Column 2]
LexerError: Invalid character `q` in number at [Line 3, Column 1]
"""
        )
        assert len(tokens) == 4

        assert tokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=3, value="jp2")
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=3, value="gmd")
        assert tokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=4))
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=2, value="d3")
