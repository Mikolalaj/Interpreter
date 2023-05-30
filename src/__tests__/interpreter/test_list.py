from .utils import getInterpreter
from src.parser.nodes import (
    Assignment,
    LemonList,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
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
                        "a",
                        LemonList([LiteralInt(POSITION, 1), LiteralInt(POSITION, 2), LiteralInt(POSITION, 3)]),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": [1, 2, 3]}

    def testListTypeError(self, capfd):
        """
        let a = [1, 2, "3"]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
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
                VariableDeclaration(POSITION, Assignment("i", LiteralInt(POSITION, 1))),
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        "a",
                        LemonList([LiteralIdentifier(POSITION, "i"), LiteralInt(POSITION, 2), LiteralInt(POSITION, 3)]),
                    ),
                ),
            ]
        )
        assert interpreter.context == {"a": [1, 2, 3], "i": 1}
