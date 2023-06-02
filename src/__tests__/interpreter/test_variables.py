from .utils import getInterpreter
from src.parser.nodes import (
    Assignment,
    LiteralBool,
    LiteralFloat,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
    LiteralSubscriptable,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestVariables:
    def testVariableDeclarations(self):
        """
        let a = 1
        let b = 2.5
        let c = "Hello"
        let d = true
        let e = a
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 1))),
                VariableDeclaration(POSITION, Assignment(POSITION, "b", LiteralFloat(POSITION, 2.5))),
                VariableDeclaration(POSITION, Assignment(POSITION, "c", LiteralString(POSITION, "Hello"))),
                VariableDeclaration(POSITION, Assignment(POSITION, "d", LiteralBool(POSITION, True))),
                VariableDeclaration(POSITION, Assignment(POSITION, "e", LiteralIdentifier(POSITION, "a"))),
            ]
        )

        assert interpreter.context == {
            "a": (1, POSITION),
            "b": (2.5, POSITION),
            "c": ("Hello", POSITION),
            "d": (True, POSITION),
            "e": (1, POSITION),
        }

    def testVariableDeclarationsFail(self, capfd):
        """
        let a = 1
        let a = 2
        let c = "Hello"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(Position(0, 0), Assignment(Position(0, 4), "a", LiteralInt(Position(0, 8), 1))),
                VariableDeclaration(Position(1, 0), Assignment(Position(1, 4), "a", LiteralInt(Position(1, 8), 2))),
                VariableDeclaration(Position(2, 0), Assignment(Position(2, 4), "c", LiteralString(Position(2, 8), "Hello"))),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: Variable a at [Line 1, Column 0] is already defined at [Line 0, Column 0]\n"

        assert interpreter.context == {"a": (1, POSITION)}

    def testVariableDeclarationsFail2(self, capfd):
        """
        let a = 1
        a = "2"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(Position(0, 0), Assignment(Position(0, 4), "a", LiteralInt(Position(0, 8), 1))),
                Assignment(Position(1, 0), "a", LiteralString(Position(1, 5), "2")),
            ]
        )
        out, _ = capfd.readouterr()
        assert (
            out
            == "InterpreterError: Variable a at [Line 1, Column 0] is already defined as <class 'int'> at [Line 0, Column 0]\n"
        )

        assert interpreter.context == {"a": (1, POSITION)}

    def testVariableDeclarationAndAssignment(self):
        """
        let a = 1
        a = 2
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 1))),
                Assignment(POSITION, "a", LiteralInt(POSITION, 2)),
            ]
        )

        assert interpreter.context == {"a": (2, POSITION)}

    def testStringSubscript(self):
        """
        let a = "Hello"
        let b = a[0]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralString(POSITION, "Hello"))),
                VariableDeclaration(
                    POSITION, Assignment(POSITION, "b", LiteralSubscriptable(POSITION, "a", LiteralInt(POSITION, 0)))
                ),
            ]
        )

        assert interpreter.context == {"a": ("Hello", POSITION), "b": ("H", POSITION)}

    def testStringSubscriptError(self, capfd):
        """
        let a = "Hello"
        let b = a[5]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralString(POSITION, "Hello"))),
                VariableDeclaration(
                    POSITION, Assignment(POSITION, "b", LiteralSubscriptable(POSITION, "a", LiteralInt(POSITION, 5)))
                ),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: Index 5 is out of range\n"

        assert interpreter.context == {"a": ("Hello", POSITION)}
