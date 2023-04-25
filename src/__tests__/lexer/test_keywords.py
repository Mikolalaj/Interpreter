import math
from src.tokens import IdentifierValueToken, Token, Position, BooleanValueToken, IntValueToken, FloatValueToken, StringValueToken
from src.token_type import TokenType
from .utils import getTokens


class TestKeywords:
    def testKeywordsAndIdentifiers(self, capfd):
        code = """
            foreachtest
            foreach_test
            foreach test
            foreach.
            foreach-
            foreach? test
            foreach?test test
            foreach!test
        """

        tokens = getTokens(code)
        out, _ = capfd.readouterr()
        assert (
            out
            == """LexerError: Invalid character `?` at [Line 6, Column 8]
LexerError: Invalid character `?` at [Line 7, Column 8]
LexerError: Invalid identifier (!test) at [Line 8, Column 8]
"""
        )
        assert len(tokens) == 14

        assert tokens[0] == IdentifierValueToken(value="foreachtest", length=11, startPosition=Position(line=1, column=1))
        assert tokens[1] == IdentifierValueToken(value="foreach_test", length=12, startPosition=Position(line=2, column=1))
        assert tokens[2] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=3, column=1))
        assert tokens[3] == IdentifierValueToken(value="test", length=4, startPosition=Position(line=3, column=9))
        assert tokens[4] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=4, column=1))
        assert tokens[5] == Token(type=TokenType.T_DOT, startPosition=Position(line=4, column=8))
        assert tokens[6] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=5, column=1))
        assert tokens[7] == Token(type=TokenType.T_MINUS, startPosition=Position(line=5, column=8))
        assert tokens[8] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=6, column=1))
        assert tokens[9] == IdentifierValueToken(value="test", length=4, startPosition=Position(line=6, column=10))
        assert tokens[10] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=7, column=1))
        assert tokens[11] == IdentifierValueToken(value="test", length=4, startPosition=Position(line=7, column=9))
        assert tokens[12] == IdentifierValueToken(value="test", length=4, startPosition=Position(line=7, column=14))
        assert tokens[13] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=8, column=1))

    def testAllTokens(self):
        code = """
            let
            Cuboid
            Pyramid
            Cone
            Cylinder
            Sphere
            Tetrahedron
            ,
            .
            [
            ]
            {
            }
            (
            )
            +
            -
            *
            /
            <
            <=
            >
            >=
            ==
            !=
            or
            and
            not
            if
            else
            elif
            true
            false
            return
            break
            continue
            while
            foreach
            in
            =
            function
            5
            5.5
            "test"
            PI
            identifier
        """

        tokens = getTokens(code)
        assert len(tokens) == 46

        assert tokens[0] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=1, column=1))
        assert tokens[1] == Token(type=TokenType.T_CUBOID, startPosition=Position(line=2, column=1))
        assert tokens[2] == Token(type=TokenType.T_PYRAMID, startPosition=Position(line=3, column=1))
        assert tokens[3] == Token(type=TokenType.T_CONE, startPosition=Position(line=4, column=1))
        assert tokens[4] == Token(type=TokenType.T_CYLINDER, startPosition=Position(line=5, column=1))
        assert tokens[5] == Token(type=TokenType.T_SPHERE, startPosition=Position(line=6, column=1))
        assert tokens[6] == Token(type=TokenType.T_TETRAHEDRON, startPosition=Position(line=7, column=1))
        assert tokens[7] == Token(type=TokenType.T_COMMA, startPosition=Position(line=8, column=1))
        assert tokens[8] == Token(type=TokenType.T_DOT, startPosition=Position(line=9, column=1))
        assert tokens[9] == Token(type=TokenType.T_LSQBRACKET, startPosition=Position(line=10, column=1))
        assert tokens[10] == Token(type=TokenType.T_RSQBRACKET, startPosition=Position(line=11, column=1))
        assert tokens[11] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=12, column=1))
        assert tokens[12] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=13, column=1))
        assert tokens[13] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=14, column=1))
        assert tokens[14] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=15, column=1))
        assert tokens[15] == Token(type=TokenType.T_PLUS, startPosition=Position(line=16, column=1))
        assert tokens[16] == Token(type=TokenType.T_MINUS, startPosition=Position(line=17, column=1))
        assert tokens[17] == Token(type=TokenType.T_MUL, startPosition=Position(line=18, column=1))
        assert tokens[18] == Token(type=TokenType.T_DIV, startPosition=Position(line=19, column=1))
        assert tokens[19] == Token(type=TokenType.T_LESS, startPosition=Position(line=20, column=1))
        assert tokens[20] == Token(type=TokenType.T_LESS_OR_EQ, startPosition=Position(line=21, column=1))
        assert tokens[21] == Token(type=TokenType.T_GREATER, startPosition=Position(line=22, column=1))
        assert tokens[22] == Token(type=TokenType.T_GREATER_OR_EQ, startPosition=Position(line=23, column=1))
        assert tokens[23] == Token(type=TokenType.T_EQ, startPosition=Position(line=24, column=1))
        assert tokens[24] == Token(type=TokenType.T_NOT_EQ, startPosition=Position(line=25, column=1))
        assert tokens[25] == Token(type=TokenType.T_OR, startPosition=Position(line=26, column=1))
        assert tokens[26] == Token(type=TokenType.T_AND, startPosition=Position(line=27, column=1))
        assert tokens[27] == Token(type=TokenType.T_NOT, startPosition=Position(line=28, column=1))
        assert tokens[28] == Token(type=TokenType.T_IF, startPosition=Position(line=29, column=1))
        assert tokens[29] == Token(type=TokenType.T_ELSE, startPosition=Position(line=30, column=1))
        assert tokens[30] == Token(type=TokenType.T_ELSEIF, startPosition=Position(line=31, column=1))
        assert tokens[31] == BooleanValueToken(startPosition=Position(line=32, column=1), value=True)
        assert tokens[32] == BooleanValueToken(startPosition=Position(line=33, column=1), value=False)
        assert tokens[33] == Token(type=TokenType.T_RETURN, startPosition=Position(line=34, column=1))
        assert tokens[34] == Token(type=TokenType.T_BREAK, startPosition=Position(line=35, column=1))
        assert tokens[35] == Token(type=TokenType.T_CONTINUE, startPosition=Position(line=36, column=1))
        assert tokens[36] == Token(type=TokenType.T_WHILE, startPosition=Position(line=37, column=1))
        assert tokens[37] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=38, column=1))
        assert tokens[38] == Token(type=TokenType.T_IN, startPosition=Position(line=39, column=1))
        assert tokens[39] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=40, column=1))
        assert tokens[40] == Token(type=TokenType.T_FUNCTION, startPosition=Position(line=41, column=1))
        assert tokens[41] == IntValueToken(startPosition=Position(line=42, column=1), value=5, length=1)
        assert tokens[42] == FloatValueToken(startPosition=Position(line=43, column=1), value=5.5, length=3)
        assert tokens[43] == StringValueToken(startPosition=Position(line=44, column=1), value="test", length=6)
        assert tokens[44] == FloatValueToken(startPosition=Position(line=45, column=1), value=math.pi, length=2)
        assert tokens[45] == IdentifierValueToken(startPosition=Position(line=46, column=1), value="identifier", length=10)
