from src.tokens import IdentifierValueToken, Token, Position
from src.token_type import TokenType
from .utils import getTokens


class TestKeywords:
    def testKeywordsAndIdentifiers(self):
        code = """
            foreachtest
            foreach_test
            foreach test
            foreach.
        """

        tokens = getTokens(code)
        assert len(tokens) == 6

        assert tokens[0] == IdentifierValueToken(value="foreachtest", length=11, startPosition=Position(line=1, column=1))
        assert tokens[1] == IdentifierValueToken(value="foreach_test", length=12, startPosition=Position(line=2, column=1))
        assert tokens[2] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=3, column=1))
        assert tokens[3] == IdentifierValueToken(value="test", length=4, startPosition=Position(line=3, column=9))
        assert tokens[4] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=4, column=1))
        assert tokens[5] == Token(type=TokenType.T_DOT, startPosition=Position(line=4, column=8))
