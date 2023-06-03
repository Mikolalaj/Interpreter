from .interpreter_utils import assertNoOutput, getInterpreter
from parser.nodes import (
    AdditiveExpression,
    Argument,
    Assignment,
    BlockWithoutFunciton,
    Break,
    ComparisonExpression,
    ConditionWithBlock,
    Continue,
    ForEachLoop,
    FunctionCall,
    IfStatement,
    LemonList,
    LiteralIdentifier,
    LiteralInt,
    VariableDeclaration,
    WhileBlock,
    WhileLoop,
)
from lexer.tokens import Position

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

    def testForEach(self, capfd):
        """
        let a = [1, 2, 3]
        foreach (i in a) {
            print(out=i)
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LemonList([LiteralInt(POSITION, 1), LiteralInt(POSITION, 2), LiteralInt(POSITION, 3)]),
                    ),
                ),
                ForEachLoop(
                    POSITION,
                    "i",
                    LiteralIdentifier(POSITION, "a"),
                    WhileBlock(
                        POSITION,
                        [
                            FunctionCall(
                                POSITION,
                                "print",
                                [Argument(POSITION, "out", LiteralIdentifier(POSITION, "i"))],
                            )
                        ],
                    ),
                ),
            ]
        )

        assert capfd.readouterr().out == "1\n2\n3\n"
        assert interpreter.context == {"a": ([1, 2, 3], POSITION)}
