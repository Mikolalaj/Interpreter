from typing import List

from lexer.token_type import TokenType
from .parser_utils import getObjects
from parser.nodes import (
    AdditiveExpression,
    ComparisonExpression,
    LiteralBool,
    LiteralFloat,
    LiteralIdentifier,
    LiteralInt,
    LogicalAndExpression,
    LogicalOrExpression,
    MultiplicativeExpression,
    PrimaryExpression,
)

from lexer.tokens import BooleanValueToken, FloatValueToken, IdentifierValueToken, IntValueToken, Position, Token


class TestLiterals:
    def testLiteralInt(self):
        tokens: List[Token] = [IntValueToken(value=2137, startPosition=Position(0, 0), length=4)]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LiteralInt(Position(0, 0), 2137)

    def testLiteralFloat(self):
        tokens: List[Token] = [FloatValueToken(value=21.37, startPosition=Position(0, 0), length=5)]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LiteralFloat(Position(0, 0), 21.37)

    def testLiteralBool(self):
        tokens: List[Token] = [BooleanValueToken(value=False, startPosition=Position(0, 0))]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LiteralBool(Position(0, 0), False)

    def testLiteralIdentifier(self):
        tokens: List[Token] = [IdentifierValueToken(value="test", startPosition=Position(0, 0), length=4)]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LiteralIdentifier(Position(0, 0), "test")


class TestPrimaryExpression:
    def testNegatedNumbers(self):
        # -2137
        # -21.37
        tokens: List[Token] = [
            Token(type=TokenType.T_MINUS, startPosition=Position(0, 0)),
            IntValueToken(value=2137, startPosition=Position(0, 0), length=4),
            Token(type=TokenType.T_MINUS, startPosition=Position(1, 0)),
            FloatValueToken(value=21.37, startPosition=Position(1, 0), length=5),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 2
        assert objects[0] == PrimaryExpression(
            isNegated=True, literal=LiteralInt(Position(0, 0), 2137), startPosition=Position(0, 0)
        )
        assert objects[1] == PrimaryExpression(
            isNegated=True, literal=LiteralFloat(Position(1, 0), 21.37), startPosition=Position(1, 0)
        )

    def testNegatedBool(self):
        # not false
        tokens: List[Token] = [
            Token(type=TokenType.T_NOT, startPosition=Position(0, 0)),
            BooleanValueToken(value=False, startPosition=Position(0, 0)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == PrimaryExpression(
            isNegated=True, literal=LiteralBool(Position(0, 0), False), startPosition=Position(0, 0)
        )

    def testNegatedIdentifier(self):
        # -test
        tokens: List[Token] = [
            Token(type=TokenType.T_MINUS, startPosition=Position(0, 0)),
            IdentifierValueToken(value="test", startPosition=Position(0, 0), length=4),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == PrimaryExpression(
            isNegated=True, literal=LiteralIdentifier(Position(0, 0), "test"), startPosition=Position(0, 0)
        )

    def testParenthesis(self):
        # (2137)
        tokens: List[Token] = [
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 0)),
            IntValueToken(value=2137, startPosition=Position(0, 1), length=4),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 5)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == PrimaryExpression(
            isNegated=False, literal=LiteralInt(Position(0, 1), 2137), startPosition=Position(0, 0)
        )

        # (-2137)
        tokens: List[Token] = [
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 0)),
            Token(type=TokenType.T_MINUS, startPosition=Position(0, 1)),
            IntValueToken(value=2137, startPosition=Position(0, 2), length=4),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 6)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == PrimaryExpression(
            isNegated=False,
            literal=PrimaryExpression(
                startPosition=Position(0, 1), isNegated=True, literal=LiteralInt(Position(0, 2), 2137)
            ),
            startPosition=Position(0, 0),
        )

        # -(-2137)
        tokens: List[Token] = [
            Token(type=TokenType.T_MINUS, startPosition=Position(0, 0)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 1)),
            Token(type=TokenType.T_MINUS, startPosition=Position(0, 2)),
            IntValueToken(value=2137, startPosition=Position(0, 3), length=4),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 7)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == PrimaryExpression(
            isNegated=True,
            literal=PrimaryExpression(
                startPosition=Position(0, 2), isNegated=True, literal=LiteralInt(Position(0, 3), 2137)
            ),
            startPosition=Position(0, 0),
        )


class TestMultiplicativeExpression:
    def testMultiplyNumbers(self):
        # 6 * 9
        tokens: List[Token] = [
            IntValueToken(value=6, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            IntValueToken(value=9, startPosition=Position(0, 4), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == MultiplicativeExpression(
            operator="*",
            left=LiteralInt(Position(0, 0), 6),
            right=LiteralInt(Position(0, 4), 9),
        )

    def testDivideFloats(self):
        # 6.9 / 9.6
        tokens: List[Token] = [
            FloatValueToken(value=6.9, startPosition=Position(0, 0), length=3),
            Token(type=TokenType.T_DIV, startPosition=Position(0, 4)),
            FloatValueToken(value=9.6, startPosition=Position(0, 6), length=3),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == MultiplicativeExpression(
            operator="/",
            left=LiteralFloat(Position(0, 0), 6.9),
            right=LiteralFloat(Position(0, 6), 9.6),
        )

    def testMultiplyMultipleNumbers(self):
        # 4 * 2 * 0
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 6)),
            IntValueToken(value=0, startPosition=Position(0, 8), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == MultiplicativeExpression(
            operator="*",
            left=LiteralInt(Position(0, 0), 4),
            right=MultiplicativeExpression(
                operator="*", left=LiteralInt(Position(0, 4), 2), right=LiteralInt(Position(0, 8), 0)
            ),
        )

    def testMultiplyAndDivideMultipleNumbers(self):
        # 4 * 2 / 3
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_DIV, startPosition=Position(0, 7)),
            IntValueToken(value=3, startPosition=Position(0, 8), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == MultiplicativeExpression(
            operator="*",
            left=LiteralInt(Position(0, 0), 4),
            right=MultiplicativeExpression(
                operator="/", left=LiteralInt(Position(0, 4), 2), right=LiteralInt(Position(0, 8), 3)
            ),
        )


class TestAdditiveExpression:
    def testAddNumbers(self):
        # 6 + 9
        tokens: List[Token] = [
            IntValueToken(value=6, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 2)),
            IntValueToken(value=9, startPosition=Position(0, 4), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == AdditiveExpression(
            operator="+",
            left=LiteralInt(Position(0, 0), 6),
            right=LiteralInt(Position(0, 4), 9),
        )

    def testSubtractFloats(self):
        # 6.9 - 9.6
        tokens: List[Token] = [
            FloatValueToken(value=6.9, startPosition=Position(0, 0), length=3),
            Token(type=TokenType.T_MINUS, startPosition=Position(0, 4)),
            FloatValueToken(value=9.6, startPosition=Position(0, 6), length=3),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == AdditiveExpression(
            operator="-",
            left=LiteralFloat(Position(0, 0), 6.9),
            right=LiteralFloat(Position(0, 6), 9.6),
        )

    def testAddMultipleNumbers(self):
        # 4 + 2 + 0
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 6)),
            IntValueToken(value=0, startPosition=Position(0, 8), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == AdditiveExpression(
            operator="+",
            left=LiteralInt(Position(0, 0), 4),
            right=AdditiveExpression(
                operator="+", left=LiteralInt(Position(0, 4), 2), right=LiteralInt(Position(0, 8), 0)
            ),
        )


class TestComparisonExpression:
    def testLessThan(self):
        # 4 < 2
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_LESS, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ComparisonExpression(
            operator="<",
            left=LiteralInt(Position(0, 0), 4),
            right=LiteralInt(Position(0, 4), 2),
        )

    def testLessThanEqual(self):
        # 4 <= 2
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_LESS_OR_EQ, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ComparisonExpression(
            operator="<=",
            left=LiteralInt(Position(0, 0), 4),
            right=LiteralInt(Position(0, 5), 2),
        )

    def testGreaterThan(self):
        # 4 > 2
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ComparisonExpression(
            operator=">",
            left=LiteralInt(Position(0, 0), 4),
            right=LiteralInt(Position(0, 4), 2),
        )

    def testGreaterThanEqual(self):
        # 4 >= 2
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_GREATER_OR_EQ, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ComparisonExpression(
            operator=">=",
            left=LiteralInt(Position(0, 0), 4),
            right=LiteralInt(Position(0, 5), 2),
        )


class TestLogicalAndExpression:
    def testLogicalAnd(self):
        # True and False
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_AND, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LogicalAndExpression(
            left=LiteralInt(Position(0, 0), 4),
            right=LiteralInt(Position(0, 5), 2),
        )


class TestLogicalOrExpression:
    def testLogicalOr(self):
        # True or False
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_OR, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LogicalOrExpression(
            left=LiteralInt(Position(0, 0), 4),
            right=LiteralInt(Position(0, 5), 2),
        )


class TestExpressions:
    def testAdditiveAndMultiplicative(self):
        # 4 + 2 * 0
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 6)),
            IntValueToken(value=0, startPosition=Position(0, 8), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == AdditiveExpression(
            operator="+",
            left=LiteralInt(Position(0, 0), 4),
            right=MultiplicativeExpression(
                operator="*", left=LiteralInt(Position(0, 4), 2), right=LiteralInt(Position(0, 8), 0)
            ),
        )

    def testMultiplicativeAndAdditive(self):
        # 4 * 2 + 0
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            IntValueToken(value=2, startPosition=Position(0, 4), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 6)),
            IntValueToken(value=0, startPosition=Position(0, 8), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == AdditiveExpression(
            operator="+",
            right=LiteralInt(Position(0, 8), 0),
            left=MultiplicativeExpression(
                operator="*", left=LiteralInt(Position(0, 0), 4), right=LiteralInt(Position(0, 4), 2)
            ),
        )

    def testMultiplicativeAdditiveAndParentheses(self):
        # 4 * (2 + 0)
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 4)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 7)),
            IntValueToken(value=0, startPosition=Position(0, 9), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == MultiplicativeExpression(
            operator="*",
            left=LiteralInt(Position(0, 0), 4),
            right=PrimaryExpression(
                Position(0, 4),
                False,
                AdditiveExpression(
                    operator="+", left=LiteralInt(Position(0, 5), 2), right=LiteralInt(Position(0, 9), 0)
                ),
            ),
        )

    def testMultiplicativeAdditiveComparison(self):
        # 4 * (2 + 1) < 1
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 4)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 7)),
            IntValueToken(value=1, startPosition=Position(0, 9), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LESS, startPosition=Position(0, 12)),
            IntValueToken(value=1, startPosition=Position(0, 14), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ComparisonExpression(
            operator="<",
            left=MultiplicativeExpression(
                operator="*",
                left=LiteralInt(Position(0, 0), 4),
                right=PrimaryExpression(
                    Position(0, 4),
                    False,
                    AdditiveExpression(
                        operator="+", left=LiteralInt(Position(0, 5), 2), right=LiteralInt(Position(0, 9), 1)
                    ),
                ),
            ),
            right=LiteralInt(Position(0, 14), 1),
        )

    def testAll(self):
        # 4 * (2 + 1) < 1 and 2 > 1 or 3 == 4
        tokens: List[Token] = [
            IntValueToken(value=4, startPosition=Position(0, 0), length=1),
            Token(type=TokenType.T_MUL, startPosition=Position(0, 2)),
            Token(type=TokenType.T_LPARENT, startPosition=Position(0, 4)),
            IntValueToken(value=2, startPosition=Position(0, 5), length=1),
            Token(type=TokenType.T_PLUS, startPosition=Position(0, 7)),
            IntValueToken(value=1, startPosition=Position(0, 9), length=1),
            Token(type=TokenType.T_RPARENT, startPosition=Position(0, 10)),
            Token(type=TokenType.T_LESS, startPosition=Position(0, 12)),
            IntValueToken(value=1, startPosition=Position(0, 14), length=1),
            Token(type=TokenType.T_AND, startPosition=Position(0, 16)),
            IntValueToken(value=2, startPosition=Position(0, 19), length=1),
            Token(type=TokenType.T_GREATER, startPosition=Position(0, 21)),
            IntValueToken(value=1, startPosition=Position(0, 24), length=1),
            Token(type=TokenType.T_OR, startPosition=Position(0, 26)),
            IntValueToken(value=3, startPosition=Position(0, 29), length=1),
            Token(type=TokenType.T_EQ, startPosition=Position(0, 31)),
            IntValueToken(value=4, startPosition=Position(0, 34), length=1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == LogicalOrExpression(
            left=LogicalAndExpression(
                left=ComparisonExpression(
                    operator="<",
                    left=MultiplicativeExpression(
                        operator="*",
                        left=LiteralInt(Position(0, 0), 4),
                        right=PrimaryExpression(
                            Position(0, 4),
                            False,
                            AdditiveExpression(
                                operator="+", left=LiteralInt(Position(0, 5), 2), right=LiteralInt(Position(0, 9), 1)
                            ),
                        ),
                    ),
                    right=LiteralInt(Position(0, 14), 1),
                ),
                right=ComparisonExpression(
                    operator=">",
                    left=LiteralInt(Position(0, 19), 2),
                    right=LiteralInt(Position(0, 24), 1),
                ),
            ),
            right=ComparisonExpression(
                operator="==",
                left=LiteralInt(Position(0, 29), 3),
                right=LiteralInt(Position(0, 34), 4),
            ),
        )
