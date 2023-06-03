from src.interpreter.objects import Cuboid, Cylinder
from .utils import assertNoOutput, getInterpreter
from src.parser.nodes import (
    Argument,
    Assignment,
    LemonList,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
    LiteralSubscriptable,
    ObjectConstructor,
    ObjectType,
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

    def testListOfObjects(self, capfd):
        """
        let cube = Cuboid(width=2, height=3, length=4)
        let cylinder = Cylinder(radius=2, height=3)
        let a = [cube, cylinder]
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "cube",
                        ObjectConstructor(
                            POSITION,
                            ObjectType.CUBOID,
                            [
                                Argument(POSITION, "width", LiteralInt(POSITION, 2)),
                                Argument(POSITION, "height", LiteralInt(POSITION, 3)),
                                Argument(POSITION, "length", LiteralInt(POSITION, 4)),
                            ],
                        ),
                    ),
                ),
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "cylinder",
                        ObjectConstructor(
                            POSITION,
                            ObjectType.CYLINDER,
                            [
                                Argument(POSITION, "radius", LiteralInt(POSITION, 2)),
                                Argument(POSITION, "height", LiteralInt(POSITION, 3)),
                            ],
                        ),
                    ),
                ),
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
                        LemonList([LiteralIdentifier(POSITION, "cube"), LiteralIdentifier(POSITION, "cylinder")]),
                    ),
                ),
            ]
        )

        cube = Cuboid(width=2, height=3, length=4)
        cylinder = Cylinder(radius=2, height=3)
        a = [cube, cylinder]

        assert interpreter.context == {
            "a": (a, POSITION),
            "cube": (cube, POSITION),
            "cylinder": (cylinder, POSITION),
        }
        assertNoOutput(capfd)
