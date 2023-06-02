from .utils import getInterpreter
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    ComparisonExpression,
    LiteralBool,
    LiteralFloat,
    LiteralInt,
    LiteralString,
    LogicalAndExpression,
    LogicalOrExpression,
    MultiplicativeExpression,
    PrimaryExpression,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestExpressions:
    def testPrimaryExpressions(self):
        """
        let a = -1
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION, Assignment(POSITION, "a", PrimaryExpression(POSITION, True, LiteralInt(POSITION, 1)))
                ),
            ]
        )

        assert interpreter.context == {"a": (-1, POSITION)}

    def testMultiplicativeExpressions(self):
        """
        let a = 4 * 5 / 2.0
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        MultiplicativeExpression(
                            LiteralInt(POSITION, 4),
                            MultiplicativeExpression(LiteralInt(POSITION, 5), LiteralFloat(POSITION, 2), "/"),
                            "*",
                        ),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (10, POSITION)}

    def testMultiplicativeExpressionsFail(self, capfd):
        """
        let a = 4 * "2"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        MultiplicativeExpression(LiteralInt(POSITION, 4), LiteralString(POSITION, "2"), "*"),
                    ),
                ),
            ]
        )

        out, _ = capfd.readouterr()
        assert out == "TypeError: Unsupported operand type(s) for *: '<class 'int'>' and '<class 'str'>'\n"
        assert interpreter.context == {}

    def testAdditiveExpressionsNumbers(self):
        """
        let a = 2 + 3.2
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        AdditiveExpression(LiteralInt(POSITION, 2), LiteralFloat(POSITION, 3.2), "+"),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (5.2, POSITION)}

    def testAdditiveExpressionsStrings(self):
        """
        let a = "Ala ma " + "kota"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        AdditiveExpression(LiteralString(POSITION, "Ala ma "), LiteralString(POSITION, "kota"), "+"),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": ("Ala ma kota", POSITION)}

    def testAdditiveExpressionsFail(self, capfd):
        """
        let a = "Ala ma " + 5
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        AdditiveExpression(LiteralString(POSITION, "Ala ma "), LiteralInt(POSITION, 5), "+"),
                    ),
                ),
            ]
        )

        out, _ = capfd.readouterr()
        assert out == "TypeError: Unsupported operand type(s) for +: '<class 'str'>' and '<class 'int'>'\n"
        assert interpreter.context == {}

    def testComparisonExpressionsEq(self):
        """
        let a = 2 > 3
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), ">"),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (False, POSITION)}

    def testComparisonExpressionsNe(self):
        """
        let a = 2 != 3
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), "!="),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (True, POSITION)}

    def testComparisonExpressionsLe(self):
        """
        let a = 2 <= 3
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), "<="),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (True, POSITION)}

    def testComparisonExpressionsGe(self):
        """
        let a = 2 >= 3
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), ">="),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (False, POSITION)}

    def testComparisonExpressionsLt(self):
        """
        let a = 2 < 3
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), "<"),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (True, POSITION)}

    def testComparisonExpressionsGt(self):
        """
        let a = 2 > 3
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), ">"),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (False, POSITION)}

    def testComparisonExpressionsFail(self, capfd):
        """
        let a = 2 > "3"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralString(POSITION, "3"), ">"),
                    ),
                ),
            ]
        )

        out, _ = capfd.readouterr()
        assert out == "TypeError: Unsupported operand type(s) for >: '<class 'int'>' and '<class 'str'>'\n"
        assert interpreter.context == {}

    def testLogicalExpressionsAnd(self) -> None:
        """
        let a = true and false
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LogicalAndExpression(LiteralBool(POSITION, True), LiteralBool(POSITION, False)),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (False, POSITION)}

    def testLogicalExpressionsOr(self):
        """
        let a = true or false
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LogicalOrExpression(LiteralBool(POSITION, True), LiteralBool(POSITION, False)),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (True, POSITION)}
