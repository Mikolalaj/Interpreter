from .utils import assertNoOutput, getInterpreter
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    ComparisonExpression,
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
