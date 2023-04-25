from src.tokens import Position, IntValueToken
from .utils import getTokens


class TestComments:
    def testComment(self):
        code = """
            # This is a comment
        """

        tokens = getTokens(code)
        assert len(tokens) == 0

    def testCommentAfterCode(self):
        code = """
            5 # This is a comment
        """

        tokens = getTokens(code)
        assert len(tokens) == 1

        assert tokens[0] == IntValueToken(value=5, length=1, startPosition=Position(line=1, column=1))
