from .utils import getInterpreter
from src.parser.nodes import (
    AdditiveExpression,
    Argument,
    Assignment,
    BlockWithoutFunciton,
    ComparisonExpression,
    ConditionWithBlock,
    FunctionCall,
    FunctionDefinition,
    IfStatement,
    LiteralBool,
    LiteralIdentifier,
    LiteralInt,
    ReturnStatement,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestFunction:
    def testFunctionDefinition(self) -> None:
        """
        function add(a, b) {
            return a + b
        }
        """
        functionDefinition = FunctionDefinition(
            POSITION,
            "add",
            ["a", "b"],
            BlockWithoutFunciton(
                POSITION,
                [
                    ReturnStatement(
                        POSITION,
                        AdditiveExpression(LiteralIdentifier(POSITION, "a"), LiteralIdentifier(POSITION, "b"), "+"),
                    )
                ],
            ),
        )
        interpreter = getInterpreter([functionDefinition])

        assert interpreter.context == {"add": (functionDefinition, POSITION)}

    def testFunctionCall(self):
        """
        function add(a, b) {
            return a + b
        }
        let a = add(a=1, b=2)
        """
        functionDefinition = FunctionDefinition(
            Position(0, 0),
            "add",
            ["a", "b"],
            BlockWithoutFunciton(
                Position(0, 19),
                [
                    ReturnStatement(
                        Position(1, 4),
                        AdditiveExpression(
                            LiteralIdentifier(Position(1, 11), "a"), LiteralIdentifier(Position(1, 15), "b"), "+"
                        ),
                    )
                ],
            ),
        )
        interpreter = getInterpreter(
            [
                functionDefinition,
                VariableDeclaration(
                    Position(3, 0),
                    Assignment(
                        Position(3, 4),
                        "a",
                        FunctionCall(
                            Position(3, 8),
                            "add",
                            [
                                Argument(Position(3, 12), "a", LiteralInt(Position(3, 14), 1)),
                                Argument(Position(3, 16), "b", LiteralInt(Position(3, 18), 2)),
                            ],
                        ),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"add": (functionDefinition, Position(0, 0)), "a": (3, Position(3, 0))}

    def testFunctionCallScopes(self):
        """
        let a = 1
        function test() {
            return a + 1
        }
        let b = test()
        """
        functionDefinition = FunctionDefinition(
            Position(1, 0),
            "test",
            [],
            BlockWithoutFunciton(
                Position(1, 16),
                [
                    ReturnStatement(
                        Position(2, 4),
                        AdditiveExpression(
                            LiteralIdentifier(Position(1, 11), "a"), LiteralInt(Position(1, 15), 1), "+"
                        ),
                    )
                ],
            ),
        )
        interpreter = getInterpreter(
            [
                VariableDeclaration(Position(0, 0), Assignment(Position(0, 4), "a", LiteralInt(Position(0, 6), 1))),
                functionDefinition,
                VariableDeclaration(
                    Position(3, 0),
                    Assignment(Position(3, 4), "b", FunctionCall(Position(3, 8), "test", [])),
                ),
            ]
        )

        assert interpreter.context == {
            "a": (1, Position(0, 0)),
            "test": (functionDefinition, Position(1, 0)),
            "b": (2, Position(3, 0)),
        }

    def testFunctionCallScopes2(self):
        """
        let a = 1
        function test() {
            let a = 2
            return a + 1
        }
        let b = test()
        """
        functionDefinition = FunctionDefinition(
            Position(1, 0),
            "test",
            [],
            BlockWithoutFunciton(
                Position(1, 16),
                [
                    VariableDeclaration(
                        Position(2, 4), Assignment(Position(2, 8), "a", LiteralInt(Position(2, 10), 2))
                    ),
                    ReturnStatement(
                        Position(3, 4),
                        AdditiveExpression(
                            LiteralIdentifier(Position(3, 11), "a"), LiteralInt(Position(3, 15), 1), "+"
                        ),
                    ),
                ],
            ),
        )
        interpreter = getInterpreter(
            [
                VariableDeclaration(Position(0, 0), Assignment(Position(0, 4), "a", LiteralInt(Position(0, 6), 1))),
                functionDefinition,
                VariableDeclaration(
                    Position(4, 0),
                    Assignment(Position(4, 4), "b", FunctionCall(Position(4, 8), "test", [])),
                ),
            ]
        )

        assert interpreter.context == {
            "a": (1, Position(0, 0)),
            "test": (functionDefinition, Position(1, 0)),
            "b": (3, Position(4, 0)),
        }

    def testFunctionCallWithIf(self):
        """
        function test(a) {
            if (a > 0) {
                return true
            }
            return false
        }
        let a = test(a=2)
        let b = test(a=-3)
        """
        functionDefinition = FunctionDefinition(
            Position(0, 0),
            "test",
            ["a"],
            BlockWithoutFunciton(
                Position(1, 16),
                [
                    IfStatement(
                        Position(1, 20),
                        ConditionWithBlock(
                            ComparisonExpression(
                                LiteralIdentifier(Position(1, 24), "a"), LiteralInt(Position(1, 28), 0), ">"
                            ),
                            BlockWithoutFunciton(
                                Position(1, 31),
                                [
                                    ReturnStatement(
                                        Position(2, 8),
                                        LiteralBool(Position(2, 15), True),
                                    )
                                ],
                            ),
                        ),
                        None,
                        None,
                    ),
                    ReturnStatement(
                        Position(4, 8),
                        LiteralBool(Position(4, 15), False),
                    ),
                ],
            ),
        )
        interpreter = getInterpreter(
            [
                functionDefinition,
                VariableDeclaration(
                    Position(6, 0),
                    Assignment(
                        Position(6, 4),
                        "a",
                        FunctionCall(
                            Position(6, 8), "test", [Argument(Position(6, 12), "a", LiteralInt(Position(6, 14), 2))]
                        ),
                    ),
                ),
                VariableDeclaration(
                    Position(7, 0),
                    Assignment(
                        Position(7, 4),
                        "b",
                        FunctionCall(
                            Position(7, 8), "test", [Argument(Position(7, 12), "a", LiteralInt(Position(7, 14), -3))]
                        ),
                    ),
                ),
            ]
        )

        assert interpreter.context == {
            "test": (functionDefinition, Position(0, 0)),
            "a": (True, Position(6, 0)),
            "b": (False, Position(7, 0)),
        }
