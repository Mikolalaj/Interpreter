from .utils import getInterpreter
from src.parser.nodes import (
    Assignment,
    LemonList,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
    LiteralSubscriptable,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestList:
    def testListInts(self):
        """
        let a = [1, 2, 3]
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
            ]
        )

        assert interpreter.context == {"a": ([1, 2, 3], POSITION)}

    def testListTypeError(self, capfd):
        """
        let a = [1, 2, "3"]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LemonList([LiteralInt(POSITION, 1), LiteralInt(POSITION, 2), LiteralString(POSITION, "3")]),
                    ),
                ),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: List cannot contain multiple types\n"

        assert interpreter.context == {}

    def testListType(self):
        """
        let i = 1
        let a = [i, 2, 3]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "i", LiteralInt(POSITION, 1))),
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LemonList([LiteralIdentifier(POSITION, "i"), LiteralInt(POSITION, 2), LiteralInt(POSITION, 3)]),
                    ),
                ),
            ]
        )
        assert interpreter.context == {"a": ([1, 2, 3], POSITION), "i": (1, POSITION)}

    def testListSubscript(self):
        """
        let a = [1, 2, 3]
        let b = a[1]
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
                VariableDeclaration(
                    POSITION, Assignment(POSITION, "b", LiteralSubscriptable(POSITION, "a", LiteralInt(POSITION, 1)))
                ),
            ]
        )
        assert interpreter.context == {"a": ([1, 2, 3], POSITION), "b": (2, POSITION)}
