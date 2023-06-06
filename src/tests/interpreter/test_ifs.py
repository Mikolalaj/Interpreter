from .interpreter_utils import getInterpreter
from parser.nodes import (
    Assignment,
    BlockWithoutFunciton,
    ComparisonExpression,
    ConditionWithBlock,
    IfStatement,
    LiteralBool,
    LiteralInt,
    VariableDeclaration,
)
from lexer.tokens import Position

POSITION = Position(0, 0)


class TestIf:
    def testIf(self):
        """
        let a = 1
        if (2 > 3) {
            a = 2
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 1))),
                IfStatement(
                    POSITION,
                    ConditionWithBlock(
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), ">"),
                        BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 2))]),
                    ),
                    None,
                    None,
                ),
            ]
        )

        assert interpreter.context == {"a": (1, POSITION)}

    def testIfElse(self):
        """
        let a = 1
        if (2 > 3) {
            a = 2
        }
        else {
            a = 3
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 1))),
                IfStatement(
                    POSITION,
                    ConditionWithBlock(
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), ">"),
                        BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 2))]),
                    ),
                    None,
                    BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 3))]),
                ),
            ]
        )

        assert interpreter.context == {"a": (3, POSITION)}

    def testIfElseIfElse(self):
        """
        let a = 1
        if (2 > 3) {
            a = 2
        }
        elif (3 == 2) {
            a = 3
        }
        elif (3 > 2) {
            a = 4
        }
        else {
            a = 5
        }
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 1))),
                IfStatement(
                    POSITION,
                    ConditionWithBlock(
                        ComparisonExpression(LiteralInt(POSITION, 2), LiteralInt(POSITION, 3), ">"),
                        BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 2))]),
                    ),
                    [
                        ConditionWithBlock(
                            ComparisonExpression(LiteralInt(POSITION, 3), LiteralInt(POSITION, 2), "=="),
                            BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 3))]),
                        ),
                        ConditionWithBlock(
                            ComparisonExpression(LiteralInt(POSITION, 3), LiteralInt(POSITION, 2), ">"),
                            BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 4))]),
                        ),
                    ],
                    BlockWithoutFunciton(POSITION, [Assignment(POSITION, "a", LiteralInt(POSITION, 5))]),
                ),
            ]
        )

        assert interpreter.context == {"a": (4, POSITION)}

    def testIfContext(self, capfd):
        """
        if (true) {
            let a = 2
        }
        a = 1
        """
        interpreter = getInterpreter(
            [
                IfStatement(
                    POSITION,
                    ConditionWithBlock(
                        LiteralBool(POSITION, True),
                        BlockWithoutFunciton(
                            POSITION,
                            [VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 2)))],
                        ),
                    ),
                    None,
                    None,
                ),
                Assignment(POSITION, "a", LiteralInt(POSITION, 1)),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: Variable a at [Line 0, Column 0] is not defined\n"

        assert interpreter.context == {}
