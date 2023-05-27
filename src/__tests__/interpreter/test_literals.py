from .utils import getInterpreter
from src.parser.nodes import (
    Assignment,
    LiteralBool,
    LiteralFloat,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


def testLiterals():
    interpreter = getInterpreter(
        [
            VariableDeclaration(POSITION, Assignment("a", LiteralInt(POSITION, 1))),
            VariableDeclaration(POSITION, Assignment("b", LiteralFloat(POSITION, 2.5))),
            VariableDeclaration(POSITION, Assignment("c", LiteralString(POSITION, "Hello"))),
            VariableDeclaration(POSITION, Assignment("d", LiteralBool(POSITION, True))),
            VariableDeclaration(POSITION, Assignment("e", LiteralIdentifier(POSITION, "a"))),
        ]
    )

    assert interpreter.literals == {
        "a": 1,
        "b": 2.5,
        "c": "Hello",
        "d": True,
        "e": 1,
    }
