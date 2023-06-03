from lexer.token_type import TokenType
from lexer.tokens import Position, IntValueToken, Token
from .lexer_utils import getTokens


class TestComments:
    def testComment(self):
        code = """
            # This is a comment
        """

        tokens = getTokens(code)
        assert len(tokens) == 1

        assert tokens[0] == Token(TokenType.VT_EOF, startPosition=Position(line=1, column=20))

    def testCommentAfterCode(self):
        code = """
            5 # This is a comment
        """

        tokens = getTokens(code)
        assert len(tokens) == 2

        assert tokens[0] == IntValueToken(value=5, length=1, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(TokenType.VT_EOF, startPosition=Position(line=1, column=22))
