from .utils import getObjects
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    Break,
    ComparisonExpression,
    LiteralIndentifier,
    LiteralInt,
    WhileBlock,
    WhileLoop,
)
from src.token_type import TokenType
from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestWhile:
    def testWhile(self):
        # while (a < 10) { a = a + 1 }
        tokens = [
            Token(type=TokenType.T_WHILE, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 6)),
            IdentifierValueToken(value="a", startPosition=Position(0, 7), length=1),
            Token(type=TokenType.T_LESS, startPosition=Position(0, 9)),
            IntValueToken(value=10, startPosition=Position(0, 11), length=2),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 13)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 15)),
            IdentifierValueToken(value="a", startPosition=Position(0, 17), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(0, 19)),
            IdentifierValueToken(value="a", startPosition=Position(0, 21), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 23)),
            IntValueToken(value=1, startPosition=Position(0, 25), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(0, 27)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == WhileLoop(
            startPosition=Position(0, 0),
            condition=ComparisonExpression(
                left=LiteralIndentifier(value="a", startPosition=Position(0, 7)),
                right=LiteralInt(value=10, startPosition=Position(0, 11)),
                operator="<",
            ),
            block=WhileBlock(
                startPosition=Position(0, 15),
                statements=[
                    Assignment(
                        name="a",
                        value=AdditiveExpression(
                            left=LiteralIndentifier(value="a", startPosition=Position(0, 21)),
                            right=LiteralInt(value=1, startPosition=Position(0, 25)),
                            operator="+",
                        ),
                    )
                ],
            ),
        )

    def testWhileBreak(self):
        # while (a < 10) { break }
        tokens = [
            Token(type=TokenType.T_WHILE, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 6)),
            IdentifierValueToken(value="a", startPosition=Position(0, 7), length=1),
            Token(type=TokenType.T_LESS, startPosition=Position(0, 9)),
            IntValueToken(value=10, startPosition=Position(0, 11), length=2),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 13)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 15)),
            Token(type=TokenType.T_BREAK, startPosition=Position(0, 17)),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(0, 23)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == WhileLoop(
            startPosition=Position(0, 0),
            condition=ComparisonExpression(
                left=LiteralIndentifier(value="a", startPosition=Position(0, 7)),
                right=LiteralInt(value=10, startPosition=Position(0, 11)),
                operator="<",
            ),
            block=WhileBlock(
                startPosition=Position(0, 15),
                statements=[
                    Break(),
                ]
            ),
        )
