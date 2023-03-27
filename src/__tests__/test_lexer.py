from src.source import StringSource
from src.lexer import Lexer
from src.tokens import FloatValueToken, IdentifierValueToken, IntValueToken, Token, Position
from src.token_type import TokenType


def removeSpaces(string: str) -> str:
    # Removes 12 spaces from the beginning of each line
    return "\n".join([line[12:] for line in string.splitlines()[1:-1]])


class TestNumbers:
    def testValidNumbers(self):
        code = """
            23
            5  13.111
            1.1
            0 -1
        """

        lexer = Lexer(source=StringSource(removeSpaces(code)))

        assert len(lexer.allTokens) == 7
        assert lexer.allTokens[0] == IntValueToken(value=23, startPosition=Position(line=1, column=1), length=2)
        assert lexer.allTokens[1] == IntValueToken(value=5, startPosition=Position(line=2, column=1), length=1)
        assert lexer.allTokens[2] == FloatValueToken(value=13.111, startPosition=Position(line=2, column=4), length=6)
        assert lexer.allTokens[3] == FloatValueToken(value=1.1, startPosition=Position(line=3, column=1), length=3)
        assert lexer.allTokens[4] == IntValueToken(value=0, startPosition=Position(line=4, column=1), length=1)
        assert lexer.allTokens[5] == Token(type=TokenType.T_MINUS, startPosition=Position(line=4, column=3))
        assert lexer.allTokens[6] == IntValueToken(value=1, startPosition=Position(line=4, column=4), length=1)


#     def testNotValidNumbers(self):
#         numbers = """
# 1 .3
#  05
# -.2
# """

#         lexer = Lexer(source=StringSource(numbers[1:-1]))
#         print(lexer.allTokens)
#         assert len(lexer.allTokens) == 2
#         assert lexer.allTokens[0] == IntValueToken(value=1, startPosition=Position(line=1, column=1), length=1)
#         assert lexer.allTokens[1] == Token(type=TokenType.T_MINUS, startPosition=Position(line=3, column=1), length=1)


class TestIdentifier:
    def testIdentifier(self, capfd):
        code = """
            jp2 gmd
             2asd
            3qq=
            d3
        """

        lexer = Lexer(source=StringSource(removeSpaces(code)))

        out, _ = capfd.readouterr()
        assert (
            out
            == """LexerError: Invalid character in number at [Line 2, Column 2]
LexerError: Invalid character in number at [Line 3, Column 1]
"""
        )
        print(lexer.allTokens)
        assert len(lexer.allTokens) == 4

        assert lexer.allTokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=3, value="jp2")
        assert lexer.allTokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=3, value="gmd")
        assert lexer.allTokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=4))
        assert lexer.allTokens[3] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=2, value="d3")


class TestIf:
    def testSingleIf(self):
        code = """
            if ( a > 3 ) {
                a = 0
            }
        """

        lexer = Lexer(source=StringSource(removeSpaces(code)))

        assert len(lexer.allTokens) == 11
        assert lexer.allTokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert lexer.allTokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4))
        assert lexer.allTokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=6), length=1, value="a")
        assert lexer.allTokens[3] == Token(type=TokenType.T_GREATER, startPosition=Position(line=1, column=8))
        assert lexer.allTokens[4] == IntValueToken(value=3, startPosition=Position(line=1, column=10), length=1)
        assert lexer.allTokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=12))
        assert lexer.allTokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=14))
        assert lexer.allTokens[7] == IdentifierValueToken(startPosition=Position(line=2, column=5), length=1, value="a")
        assert lexer.allTokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=7))
        assert lexer.allTokens[9] == IntValueToken(value=0, startPosition=Position(line=2, column=9), length=1)
        assert lexer.allTokens[10] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1))

    def testSingleIfNoSpaces(self):
        code = "if(a>3){a=0}"

        lexer = Lexer(source=StringSource(code))
        print((lexer.allTokens))
        assert len(lexer.allTokens) == 11
        assert lexer.allTokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert lexer.allTokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=3))
        assert lexer.allTokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=4), length=1, value="a")
        assert lexer.allTokens[3] == Token(type=TokenType.T_GREATER, startPosition=Position(line=1, column=5))
        assert lexer.allTokens[4] == IntValueToken(value=3, startPosition=Position(line=1, column=6), length=1)
        assert lexer.allTokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=7))
        assert lexer.allTokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=8))
        assert lexer.allTokens[7] == IdentifierValueToken(startPosition=Position(line=1, column=9), length=1, value="a")
        assert lexer.allTokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=10))
        assert lexer.allTokens[9] == IntValueToken(value=0, startPosition=Position(line=1, column=11), length=1)
        assert lexer.allTokens[10] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=1, column=12))

    def testIfElif(self):
        code = """
            if ( a < b ) {
                a = a - 1
            } elif ( a < 3 ) {
                a = 1
            }
        """

        lexer = Lexer(source=StringSource(removeSpaces(code)))

        assert len(lexer.allTokens) == 24
        assert lexer.allTokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert lexer.allTokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4))
        assert lexer.allTokens[2] == IdentifierValueToken(startPosition=Position(line=1, column=6), length=1, value="a")
        assert lexer.allTokens[3] == Token(type=TokenType.T_LESS, startPosition=Position(line=1, column=8))
        assert lexer.allTokens[4] == IdentifierValueToken(startPosition=Position(line=1, column=10), length=1, value="b")
        assert lexer.allTokens[5] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=12))
        assert lexer.allTokens[6] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=14))
        assert lexer.allTokens[7] == IdentifierValueToken(startPosition=Position(line=2, column=5), length=1, value="a")
        assert lexer.allTokens[8] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=2, column=7))
        assert lexer.allTokens[9] == IdentifierValueToken(startPosition=Position(line=2, column=9), length=1, value="a")
        assert lexer.allTokens[10] == Token(type=TokenType.T_MINUS, startPosition=Position(line=2, column=11))
        assert lexer.allTokens[11] == IntValueToken(value=1, startPosition=Position(line=2, column=13), length=1)
        assert lexer.allTokens[12] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1))
        assert lexer.allTokens[13] == Token(type=TokenType.T_ELSEIF, startPosition=Position(line=3, column=3))
        assert lexer.allTokens[14] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=3, column=8))
        assert lexer.allTokens[15] == IdentifierValueToken(startPosition=Position(line=3, column=10), length=1, value="a")
        assert lexer.allTokens[16] == Token(type=TokenType.T_LESS, startPosition=Position(line=3, column=12))
        assert lexer.allTokens[17] == IntValueToken(startPosition=Position(line=3, column=14), length=1, value=3)
        assert lexer.allTokens[18] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=3, column=16))
        assert lexer.allTokens[19] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=3, column=18))
        assert lexer.allTokens[20] == IdentifierValueToken(startPosition=Position(line=4, column=5), length=1, value="a")
        assert lexer.allTokens[21] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=4, column=7))
        assert lexer.allTokens[22] == IntValueToken(value=1, startPosition=Position(line=4, column=9), length=1)
        assert lexer.allTokens[23] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=5, column=1))

    def testIfElse(self):
        code = """
            if () {
            } else () {
            }
        """

        lexer = Lexer(source=StringSource(removeSpaces(code)))

        assert len(lexer.allTokens) == 10
        assert lexer.allTokens[0] == Token(type=TokenType.T_IF, startPosition=Position(line=1, column=1))
        assert lexer.allTokens[1] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=1, column=4))
        assert lexer.allTokens[2] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=1, column=5))
        assert lexer.allTokens[3] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=1, column=7))
        assert lexer.allTokens[4] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=2, column=1))
        assert lexer.allTokens[5] == Token(type=TokenType.T_ELSE, startPosition=Position(line=2, column=3))
        assert lexer.allTokens[6] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=2, column=8))
        assert lexer.allTokens[7] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=2, column=9))
        assert lexer.allTokens[8] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=2, column=11))
        assert lexer.allTokens[9] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=3, column=1))


class TestObjects:
    def testCreating(self):
        codeWithSpaces = "let a = Cuboid ( width = 4 , length = 2 , height = 5 )"
        lexer1 = Lexer(source=StringSource(codeWithSpaces))
        print(lexer1.allTokens)
        assert len(lexer1.allTokens) == 17

        codeWithoutSpaces = "let a=Cuboid(width=4,length=2,height=5)"
        lexer2 = Lexer(source=StringSource(codeWithoutSpaces))
        print(lexer2.allTokens)
        assert len(lexer2.allTokens) == 17
