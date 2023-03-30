from src.__tests__.lexer.utils import getTokens
from src.lexer import Lexer
from src.source import StringSource
from src.token_type import TokenType
from src.tokens import IdentifierValueToken, Position, Token


class TestObjects:
    def testCreating(self):
        code = "let a = Cuboid ( width = 4 , length = 2 , height = 5 )"
        lexer = Lexer(source=StringSource(code))
        print(lexer.allTokens)
        assert len(lexer.allTokens) == 17

    def testCreatingNoSpaces(self):
        code = "let a=Cuboid(width=4,length=2,height=5)"
        lexer = Lexer(source=StringSource(code))
        print(lexer.allTokens)
        assert len(lexer.allTokens) == 17

    def testAllObjectTypes(self):
        code = """
            Cuboid cuboid
            Pyramid pyramid
            Cone cone
            Cylinder cylinder
            Sphere sphere
            Tetrahedron tetrahedron
        """

        tokens = getTokens(code)
        assert len(tokens) == 12

        assert tokens[0] == Token(startPosition=Position(line=1, column=1), type=TokenType.T_CUBOID)
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=8), length=6, value="cuboid")
        assert tokens[2] == Token(startPosition=Position(line=2, column=1), type=TokenType.T_PYRAMID)
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=2, column=9), length=7, value="pyramid")
        assert tokens[4] == Token(startPosition=Position(line=3, column=1), type=TokenType.T_CONE)
        assert tokens[5] == IdentifierValueToken(startPosition=Position(line=3, column=6), length=4, value="cone")
        assert tokens[6] == Token(startPosition=Position(line=4, column=1), type=TokenType.T_CYLINDER)
        assert tokens[7] == IdentifierValueToken(startPosition=Position(line=4, column=10), length=8, value="cylinder")
        assert tokens[8] == Token(startPosition=Position(line=5, column=1), type=TokenType.T_SPHERE)
        assert tokens[9] == IdentifierValueToken(startPosition=Position(line=5, column=8), length=6, value="sphere")
        assert tokens[10] == Token(startPosition=Position(line=6, column=1), type=TokenType.T_TETRAHEDRON)
        assert tokens[11] == IdentifierValueToken(startPosition=Position(line=6, column=13), length=11, value="tetrahedron")

    def testObjectMethodCall(self):
        code = """
            let a = cuboid.getProperty()
        """

        tokens = getTokens(code)
        assert len(tokens) == 8

        assert tokens[0] == Token(startPosition=Position(line=1, column=1), type=TokenType.T_VARIABLE)
        assert tokens[1] == IdentifierValueToken(startPosition=Position(line=1, column=5), length=1, value="a")
        assert tokens[2] == Token(startPosition=Position(line=1, column=7), type=TokenType.T_ASSIGN)
        assert tokens[3] == IdentifierValueToken(startPosition=Position(line=1, column=9), length=6, value="cuboid")
        assert tokens[4] == Token(startPosition=Position(line=1, column=15), type=TokenType.T_DOT)
        assert tokens[5] == IdentifierValueToken(startPosition=Position(line=1, column=16), length=11, value="getProperty")
        assert tokens[6] == Token(startPosition=Position(line=1, column=27), type=TokenType.T_LPARENT)
        assert tokens[7] == Token(startPosition=Position(line=1, column=28), type=TokenType.T_RPARENT)
