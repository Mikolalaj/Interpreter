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
                VariableDeclaration(POSITION, Assignment("a", LiteralInt(POSITION, 1))),
                VariableDeclaration(POSITION, Assignment("b", LiteralFloat(POSITION, 2.5))),
                VariableDeclaration(POSITION, Assignment("c", LiteralString(POSITION, "Hello"))),
                VariableDeclaration(POSITION, Assignment("d", LiteralBool(POSITION, True))),
                VariableDeclaration(POSITION, Assignment("e", LiteralIdentifier(POSITION, "a"))),
            ]
        )

        assert interpreter.context == {
            "a": 1,
            "b": 2.5,
            "c": "Hello",
            "d": True,
            "e": 1,
        }

    def testVariableDeclarationsFail(self, capfd):
        """
        let a = 1
        let a = 2
        let c = "Hello"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment("a", LiteralInt(POSITION, 1))),
                VariableDeclaration(POSITION, Assignment("a", LiteralInt(POSITION, 2))),
                VariableDeclaration(POSITION, Assignment("c", LiteralString(POSITION, "Hello"))),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: Variable a is already defined\n"

        assert interpreter.context == {"a": 1}

    def testVariableDeclarationsFail2(self, capfd):
        """
        let a = 1
        a = "2"
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment("a", LiteralInt(POSITION, 1))),
                Assignment("a", LiteralString(POSITION, "2")),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: Variable a is already defined as <class 'int'>\n"

        assert interpreter.context == {"a": 1}

    def testVariableDeclarationAndAssignment(self):
        """
        let a = 1
        a = 2
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment("a", LiteralInt(POSITION, 1))),
                Assignment("a", LiteralInt(POSITION, 2)),
            ]
        )

        assert interpreter.context == {"a": 2}

    def testStringSubscript(self):
        """
        let a = "Hello"
        let b = a[0]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment("a", LiteralString(POSITION, "Hello"))),
                VariableDeclaration(
                    POSITION, Assignment("b", LiteralSubscriptable(POSITION, "a", LiteralInt(POSITION, 0)))
                ),
            ]
        )

        assert interpreter.context == {"a": "Hello", "b": "H"}

    def testStringSubscriptError(self, capfd):
        """
        let a = "Hello"
        let b = a[5]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(POSITION, Assignment("a", LiteralString(POSITION, "Hello"))),
                VariableDeclaration(
                    POSITION, Assignment("b", LiteralSubscriptable(POSITION, "a", LiteralInt(POSITION, 5)))
                ),
            ]
        )
        out, _ = capfd.readouterr()
        assert out == "InterpreterError: Index 5 is out of range\n"

        assert interpreter.context == {"a": "Hello"}
