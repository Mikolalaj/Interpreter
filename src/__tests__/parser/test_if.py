from .utils import getObjects
from src.parser.nodes import (
    Assignment,
    BlockWithoutFunciton,
    ComparisonExpression,
    ConditionWithBlock,
    IfStatement,
    LiteralIndentifier,
    LiteralInt,
)
from src.token_type import TokenType
from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestIf:
    def testIf(self):
        """
        if (a > b) {
            a = 1
        }
        """
        tokens = [
            Token(type=TokenType.T_IF, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 3)),
            IdentifierValueToken(value="a", startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 6)),
            IdentifierValueToken(value="b", startPosition=Position(0, 8), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 12)),
            IdentifierValueToken(value="a", startPosition=Position(1, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(1, 7)),
            IntValueToken(value=1, startPosition=Position(1, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(2, 0)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == IfStatement(
            startPosition=Position(0, 0),
            ifCB=ConditionWithBlock(
                condition=ComparisonExpression(
                    left=LiteralIndentifier(value="a", startPosition=Position(0, 4)),
                    right=LiteralIndentifier(value="b", startPosition=Position(0, 8)),
                    operator=">",
                ),
                block=BlockWithoutFunciton(
                    statements=[Assignment(name="a", value=LiteralInt(Position(1, 9), 1))],
                    startPosition=Position(0, 12),
                ),
            ),
            elifCBs=None,
            elseBlock=None,
        )

    def testIfElif(self):
        """
        if (a > b) {
            a = 1
        }
        elif (a < b) {
            a = 2
        }
        """
        tokens = [
            Token(type=TokenType.T_IF, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 3)),
            IdentifierValueToken(value="a", startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 6)),
            IdentifierValueToken(value="b", startPosition=Position(0, 8), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 12)),
            IdentifierValueToken(value="a", startPosition=Position(1, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(1, 7)),
            IntValueToken(value=1, startPosition=Position(1, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(2, 0)),
            Token(type=TokenType.T_ELSEIF, startPosition=Position(3, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(3, 4)),
            IdentifierValueToken(value="a", startPosition=Position(3, 5), length=1),
            Token(type=TokenType.T_LESS, startPosition=Position(3, 7)),
            IdentifierValueToken(value="b", startPosition=Position(3, 9), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(3, 11)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(3, 13)),
            IdentifierValueToken(value="a", startPosition=Position(4, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(4, 7)),
            IntValueToken(value=2, startPosition=Position(4, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(5, 0)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == IfStatement(
            startPosition=Position(0, 0),
            ifCB=ConditionWithBlock(
                condition=ComparisonExpression(
                    left=LiteralIndentifier(value="a", startPosition=Position(0, 4)),
                    right=LiteralIndentifier(value="b", startPosition=Position(0, 8)),
                    operator=">",
                ),
                block=BlockWithoutFunciton(
                    statements=[Assignment(name="a", value=LiteralInt(Position(1, 9), 1))],
                    startPosition=Position(0, 12),
                ),
            ),
            elifCBs=[
                ConditionWithBlock(
                    condition=ComparisonExpression(
                        left=LiteralIndentifier(value="a", startPosition=Position(3, 5)),
                        right=LiteralIndentifier(value="b", startPosition=Position(3, 9)),
                        operator="<",
                    ),
                    block=BlockWithoutFunciton(
                        statements=[Assignment(name="a", value=LiteralInt(Position(4, 9), 2))],
                        startPosition=Position(3, 13),
                    ),
                )
            ],
            elseBlock=None,
        )

    def testIfElifs(self):
        """
        if (a > b) {
            a = 1
        }
        elif (a < b) {
            a = 2
        }
        elif (a == b) {
            a = 3
        }
        """
        tokens = [
            Token(type=TokenType.T_IF, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 3)),
            IdentifierValueToken(value="a", startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 6)),
            IdentifierValueToken(value="b", startPosition=Position(0, 8), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 12)),
            IdentifierValueToken(value="a", startPosition=Position(1, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(1, 7)),
            IntValueToken(value=1, startPosition=Position(1, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(2, 0)),
            Token(type=TokenType.T_ELSEIF, startPosition=Position(3, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(3, 4)),
            IdentifierValueToken(value="a", startPosition=Position(3, 5), length=1),
            Token(type=TokenType.T_LESS, startPosition=Position(3, 7)),
            IdentifierValueToken(value="b", startPosition=Position(3, 9), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(3, 11)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(3, 13)),
            IdentifierValueToken(value="a", startPosition=Position(4, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(4, 7)),
            IntValueToken(value=2, startPosition=Position(4, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(5, 0)),
            Token(type=TokenType.T_ELSEIF, startPosition=Position(6, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(6, 4)),
            IdentifierValueToken(value="a", startPosition=Position(6, 5), length=1),
            Token(type=TokenType.T_EQ, startPosition=Position(6, 7)),
            IdentifierValueToken(value="b", startPosition=Position(6, 10), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(6, 11)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(6, 13)),
            IdentifierValueToken(value="a", startPosition=Position(7, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(7, 7)),
            IntValueToken(value=3, startPosition=Position(7, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(8, 0)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == IfStatement(
            startPosition=Position(0, 0),
            ifCB=ConditionWithBlock(
                condition=ComparisonExpression(
                    left=LiteralIndentifier(value="a", startPosition=Position(0, 4)),
                    right=LiteralIndentifier(value="b", startPosition=Position(0, 8)),
                    operator=">",
                ),
                block=BlockWithoutFunciton(
                    statements=[Assignment(name="a", value=LiteralInt(Position(1, 9), 1))],
                    startPosition=Position(0, 12),
                ),
            ),
            elifCBs=[
                ConditionWithBlock(
                    condition=ComparisonExpression(
                        left=LiteralIndentifier(value="a", startPosition=Position(3, 5)),
                        right=LiteralIndentifier(value="b", startPosition=Position(3, 9)),
                        operator="<",
                    ),
                    block=BlockWithoutFunciton(
                        statements=[Assignment(name="a", value=LiteralInt(Position(4, 9), 2))],
                        startPosition=Position(3, 13),
                    ),
                ),
                ConditionWithBlock(
                    condition=ComparisonExpression(
                        left=LiteralIndentifier(value="a", startPosition=Position(6, 5)),
                        right=LiteralIndentifier(value="b", startPosition=Position(6, 10)),
                        operator="==",
                    ),
                    block=BlockWithoutFunciton(
                        statements=[Assignment(name="a", value=LiteralInt(Position(7, 9), 3))],
                        startPosition=Position(6, 13),
                    ),
                ),
            ],
            elseBlock=None,
        )

    def testIfElse(self):
        """
        if (a > b) {
            a = 1
        }
        else {
            a = 2
        }
        """
        tokens = [
            Token(type=TokenType.T_IF, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 3)),
            IdentifierValueToken(value="a", startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 6)),
            IdentifierValueToken(value="b", startPosition=Position(0, 8), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 12)),
            IdentifierValueToken(value="a", startPosition=Position(1, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(1, 7)),
            IntValueToken(value=1, startPosition=Position(1, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(2, 0)),
            Token(type=TokenType.T_ELSE, startPosition=Position(3, 0)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(3, 5)),
            IdentifierValueToken(value="a", startPosition=Position(4, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(4, 7)),
            IntValueToken(value=2, startPosition=Position(4, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(5, 0)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == IfStatement(
            startPosition=Position(0, 0),
            ifCB=ConditionWithBlock(
                condition=ComparisonExpression(
                    left=LiteralIndentifier(value="a", startPosition=Position(0, 4)),
                    right=LiteralIndentifier(value="b", startPosition=Position(0, 8)),
                    operator=">",
                ),
                block=BlockWithoutFunciton(
                    statements=[Assignment(name="a", value=LiteralInt(Position(1, 9), 1))],
                    startPosition=Position(0, 12),
                ),
            ),
            elifCBs=None,
            elseBlock=BlockWithoutFunciton(
                statements=[Assignment(name="a", value=LiteralInt(Position(4, 9), 2))],
                startPosition=Position(3, 5),
            ),
        )

    def testIfElifElse(self):
        """
        if (a > b) {
            a = 1
        }
        elif (a < b) {
            a = 2
        }
        else {
            a = 3
        }
        """
        tokens = [
            Token(type=TokenType.T_IF, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 3)),
            IdentifierValueToken(value="a", startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 6)),
            IdentifierValueToken(value="b", startPosition=Position(0, 8), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(0, 12)),
            IdentifierValueToken(value="a", startPosition=Position(1, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(1, 7)),
            IntValueToken(value=1, startPosition=Position(1, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(2, 0)),
            Token(type=TokenType.T_ELSEIF, startPosition=Position(3, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(3, 4)),
            IdentifierValueToken(value="a", startPosition=Position(3, 5), length=1),
            Token(type=TokenType.T_LESS, startPosition=Position(3, 7)),
            IdentifierValueToken(value="b", startPosition=Position(3, 9), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(3, 11)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(3, 13)),
            IdentifierValueToken(value="a", startPosition=Position(4, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(4, 7)),
            IntValueToken(value=2, startPosition=Position(4, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(5, 0)),
            Token(type=TokenType.T_ELSE, startPosition=Position(6, 0)),
            Token(type=TokenType.T_LBRACKET, startPosition=Position(6, 5)),
            IdentifierValueToken(value="a", startPosition=Position(7, 5), length=1),
            Token(type=TokenType.T_ASSIGN, startPosition=Position(7, 7)),
            IntValueToken(value=3, startPosition=Position(7, 9), length=1),
            Token(type=TokenType.T_RBRACKET, startPosition=Position(8, 0)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == IfStatement(
            startPosition=Position(0, 0),
            ifCB=ConditionWithBlock(
                condition=ComparisonExpression(
                    left=LiteralIndentifier(value="a", startPosition=Position(0, 4)),
                    right=LiteralIndentifier(value="b", startPosition=Position(0, 8)),
                    operator=">",
                ),
                block=BlockWithoutFunciton(
                    statements=[Assignment(name="a", value=LiteralInt(Position(1, 9), 1))],
                    startPosition=Position(0, 12),
                ),
            ),
            elifCBs=[
                ConditionWithBlock(
                    condition=ComparisonExpression(
                        left=LiteralIndentifier(value="a", startPosition=Position(3, 5)),
                        right=LiteralIndentifier(value="b", startPosition=Position(3, 9)),
                        operator="<",
                    ),
                    block=BlockWithoutFunciton(
                        statements=[Assignment(name="a", value=LiteralInt(Position(4, 9), 2))],
                        startPosition=Position(3, 13),
                    ),
                )
            ],
            elseBlock=BlockWithoutFunciton(
                statements=[Assignment(name="a", value=LiteralInt(Position(7, 9), 3))],
                startPosition=Position(6, 5),
            ),
        )
