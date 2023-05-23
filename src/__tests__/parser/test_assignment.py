from typing import List

from src.token_type import TokenType
from .utils import getObjects
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    LiteralBool,
    LiteralFloat,
    LiteralIndentifier,
    LiteralInt,
    LiteralSubscriptable,
    LiteralString,
    ObjectConstructor,
    ObjectType,
)

from src.tokens import (
    BooleanValueToken,
    FloatValueToken,
    IdentifierValueToken,
    IntValueToken,
    Position,
    StringValueToken,
    Token,
)


# Assignment = Identifier = ( Expression | String | List | FunctionCall | ObjectMethodCall | ObjectProperty | ListGetValue ) ;
class TestAssignment:
    def testIntAssignment(self):
        # a = 1
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            IntValueToken(Position(0, 4), 1, 1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment("a", LiteralInt(Position(0, 4), 1))

    def testFloatAssignment(self):
        # a = 1.0
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            FloatValueToken(Position(0, 4), 1, 1.0),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment("a", LiteralFloat(Position(0, 4), 1.0))

    def testBoolAssignment(self):
        # a = true
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            BooleanValueToken(Position(0, 4), True),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment("a", LiteralBool(Position(0, 4), True))

    def testStringAssignment(self):
        # a = "hello"
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            StringValueToken(Position(0, 4), 4, "hello"),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment("a", LiteralString(Position(0, 4), "hello"))

    def testIdentifierAssignment(self):
        # a = b
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            IdentifierValueToken(Position(0, 4), 1, "b"),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment("a", LiteralIndentifier(Position(0, 4), "b"))

    def testExpressionAssignment(self):
        # a = 1 + 2
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            IntValueToken(Position(0, 4), 1, 1),
            Token(TokenType.T_PLUS, Position(0, 6)),
            IntValueToken(Position(0, 8), 1, 2),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a", AdditiveExpression(LiteralInt(Position(0, 4), 1), LiteralInt(Position(0, 8), 2), "+")
        )

    def testListIndexAssignment(self):
        # a = b[0]
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            IdentifierValueToken(Position(0, 4), 1, "b"),
            Token(TokenType.T_LSQBRACKET, Position(0, 5)),
            IntValueToken(Position(0, 6), 1, 0),
            Token(TokenType.T_RSQBRACKET, Position(0, 7)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment("a", LiteralSubscriptable(Position(0, 4), "b", LiteralInt(Position(0, 6), 0)))

    def testObjectAssignment(self):
        # a = Cuboid(width=4, length=2, height=5)
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            Token(TokenType.T_CUBOID, Position(0, 4)),
            Token(TokenType.T_LPARENT, Position(0, 10)),
            IdentifierValueToken(Position(0, 11), 1, "width"),
            Token(TokenType.T_ASSIGN, Position(0, 16)),
            IntValueToken(Position(0, 17), 1, 4),
            Token(TokenType.T_COMMA, Position(0, 18)),
            IdentifierValueToken(Position(0, 20), 1, "length"),
            Token(TokenType.T_ASSIGN, Position(0, 26)),
            IntValueToken(Position(0, 27), 1, 2),
            Token(TokenType.T_COMMA, Position(0, 28)),
            IdentifierValueToken(Position(0, 30), 1, "height"),
            Token(TokenType.T_ASSIGN, Position(0, 37)),
            IntValueToken(Position(0, 38), 1, 5),
            Token(TokenType.T_RPARENT, Position(0, 39)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a",
            ObjectConstructor(
                Position(0, 4),
                ObjectType.CUBOID,
                [
                    Assignment("width", LiteralInt(Position(0, 17), 4)),
                    Assignment("length", LiteralInt(Position(0, 27), 2)),
                    Assignment("height", LiteralInt(Position(0, 38), 5)),
                ],
            ),
        )
