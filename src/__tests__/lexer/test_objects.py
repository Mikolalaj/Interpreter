from src.lexer import Lexer
from src.source import StringSource


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
