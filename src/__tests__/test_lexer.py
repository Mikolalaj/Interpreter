from src.source import StringSource
from src.lexer import Lexer
from src.tokens import FloatValueToken, IdentifierValueToken, IntValueToken, Token, Position
from src.token_type import TokenType


class TestNumbers:
    def testValidNumbers(self):
        numbers = """
23
5  13.111
1.1
0 -1
        """

        lexer = Lexer(source=StringSource(numbers[1:-1]))

        assert len(lexer.allTokens) == 7
        assert lexer.allTokens[0] == IntValueToken(value=23, startPosition=Position(line=1, column=1), length=2)
        assert lexer.allTokens[1] == IntValueToken(value=5, startPosition=Position(line=2, column=1), length=1)
        assert lexer.allTokens[2] == FloatValueToken(value=13.111, startPosition=Position(line=2, column=4), length=6)
        assert lexer.allTokens[3] == FloatValueToken(value=1.1, startPosition=Position(line=3, column=1), length=3)
        assert lexer.allTokens[4] == IntValueToken(value=0, startPosition=Position(line=4, column=1), length=1)
        assert lexer.allTokens[5] == Token(type=TokenType.T_MINUS, startPosition=Position(line=4, column=3), length=1)
        assert lexer.allTokens[6] == IntValueToken(value=1, startPosition=Position(line=4, column=4), length=1)

    def testNotValidNumbers(self):
        numbers = """
1 .3
 05
-.2
    """

        lexer = Lexer(source=StringSource(numbers[1:-1]))

        assert len(lexer.allTokens) == 2
        assert lexer.allTokens[0] == IntValueToken(value=1, startPosition=Position(line=1, column=1), length=1)


def testIdentifier():
    code = """
jp2 gmd
 2asd
3qq
d3
"""

    lexer = Lexer(source=StringSource(code[1:-1]))

    assert len(lexer.allTokens) == 3
    assert lexer.allTokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=3, value="jp2")
    assert lexer.allTokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=3, value="gmd")
    assert lexer.allTokens[2] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=2, value="d3")


def testIf():
    code = """
if ( a > 3 ) {
    a = 0
}
    """

    lexer = Lexer(source=StringSource(code[1:-1]))

    assert len(lexer.allTokens) == 11
    assert lexer.allTokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1), length=2)
    assert lexer.allTokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4), length=1)
    assert lexer.allTokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=6), length=1, value="a")
    assert lexer.allTokens[3] == Token(type=TokenType.T_GREATER, startPosition=Position(line=1, column=8), length=1)
    assert lexer.allTokens[4] == IntValueToken(value=3, startPosition=Position(line=1, column=10), length=1)
    assert lexer.allTokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=12), length=1)
    assert lexer.allTokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=14), length=1)
    assert lexer.allTokens[7] == IdentifierValueToken(startPosition=Position(line=2, column=5), length=1, value="a")
    assert lexer.allTokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=7), length=1)
    assert lexer.allTokens[9] == IntValueToken(value=0, startPosition=Position(line=2, column=9), length=1)
    assert lexer.allTokens[10] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1), length=1)
