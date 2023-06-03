from .utils import assertNoOutput, getInterpreter
from src.parser.nodes import (
    AdditiveExpression,
    Argument,
    Assignment,
    BlockWithoutFunciton,
    Break,
    ComparisonExpression,
    ConditionWithBlock,
    Continue,
    FunctionCall,
    IfStatement,
    LiteralIdentifier,
    LiteralInt,
    VariableDeclaration,
    WhileBlock,
    WhileLoop,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestLoops:
    def testWhile(self, capfd):
        """
        let a = 1
        while (a < 5) {
            a = a + 1
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LiteralInt(POSITION, 1),
                    ),
                ),
                WhileLoop(
                    POSITION,
                    ComparisonExpression(
                        LiteralIdentifier(POSITION, "a"),
                        LiteralInt(POSITION, 5),
                        "<",
                    ),
                    WhileBlock(
                        POSITION,
                        [
                            Assignment(
                                POSITION,
                                "a",
                                AdditiveExpression(
                                    LiteralIdentifier(POSITION, "a"),
                                    LiteralInt(POSITION, 1),
                                    "+",
                                ),
                            )
                        ],
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (5, POSITION)}
        assertNoOutput(capfd)

    def testWhileBreak(self, capfd):
        """
        let a = 1
        while (a < 5) {
            a = a + 1
            if (a == 3) {
                break
            }
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LiteralInt(POSITION, 1),
                    ),
                ),
                WhileLoop(
                    POSITION,
                    ComparisonExpression(
                        LiteralIdentifier(POSITION, "a"),
                        LiteralInt(POSITION, 5),
                        "<",
                    ),
                    WhileBlock(
                        POSITION,
                        [
                            Assignment(
                                POSITION,
                                "a",
                                AdditiveExpression(
                                    LiteralIdentifier(POSITION, "a"),
                                    LiteralInt(POSITION, 1),
                                    "+",
                                ),
                            ),
                            IfStatement(
                                POSITION,
                                ConditionWithBlock(
                                    ComparisonExpression(
                                        LiteralIdentifier(POSITION, "a"),
                                        LiteralInt(POSITION, 3),
                                        "==",
                                    ),
                                    BlockWithoutFunciton(POSITION, [Break()]),
                                ),
                                None,
                                None,
                            ),
                        ],
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": (3, POSITION)}
        assertNoOutput(capfd)

    def testWhileContinue(self, capfd):
        """
        let a = 1
        while (a < 5) {
            a = a + 1
            if (a == 3) {
                continue
            }
            print(out=a)
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LiteralInt(POSITION, 1),
                    ),
                ),
                WhileLoop(
                    POSITION,
                    ComparisonExpression(
                        LiteralIdentifier(POSITION, "a"),
                        LiteralInt(POSITION, 5),
                        "<",
                    ),
                    WhileBlock(
                        POSITION,
                        [
                            Assignment(
                                POSITION,
                                "a",
                                AdditiveExpression(
                                    LiteralIdentifier(POSITION, "a"),
                                    LiteralInt(POSITION, 1),
                                    "+",
                                ),
                            ),
                            IfStatement(
                                POSITION,
                                ConditionWithBlock(
                                    ComparisonExpression(
                                        LiteralIdentifier(POSITION, "a"),
                                        LiteralInt(POSITION, 3),
                                        "==",
                                    ),
                                    BlockWithoutFunciton(POSITION, [Continue()]),
                                ),
                                None,
                                None,
                            ),
                            FunctionCall(
                                POSITION,
                                "print",
                                [Argument(POSITION, "out", LiteralIdentifier(POSITION, "a"))],
                            ),
                        ],
                    ),
                ),
            ]
        )

        assert capfd.readouterr().out == "2\n4\n5\n"
        assert interpreter.context == {"a": (5, POSITION)}
