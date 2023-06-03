from src.interpreter.objects import Cuboid
from .utils import assertNoOutput, getInterpreter
from src.parser.nodes import (
    Argument,
    Assignment,
    FunctionCall,
    LiteralInt,
    ObjectConstructor,
    ObjectMethodCall,
    ObjectProperty,
    ObjectType,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestObjects:
    def testConstructor(self, capfd):
        """
        let a = Cuboid(width=2, height=3, length=4)
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        POSITION,
                        "a",
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
            ]
        )

        assert interpreter.context == {"a": (Cuboid(width=2, height=3, length=4), POSITION)}
        assertNoOutput(capfd)

    def testMethodCall(self, capfd):
        """
        let cube = Cuboid(width=2, height=3, length=4)
        let volume = cube.getVolume()
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
                        "volume",
                        ObjectMethodCall(
                            POSITION,
                            "cube",
                            FunctionCall(
                                POSITION,
                                "getVolume",
                                [],
                            ),
                        ),
                    ),
                ),
            ]
        )

        cube = Cuboid(width=2, height=3, length=4)

        assert interpreter.context == {
            "cube": (cube, POSITION),
            "volume": (cube.getVolume(), POSITION),
        }
        assertNoOutput(capfd)

    def testProperty(self, capfd):
        """
        let cube = Cuboid(width=2, height=3, length=4)
        cube.width = 5
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
                Assignment(
                    POSITION,
                    ObjectProperty(
                        POSITION,
                        "cube",
                        "width",
                    ),
                    LiteralInt(POSITION, 5),
                ),
            ]
        )

        cube = Cuboid(width=5, height=3, length=4)

        assert interpreter.context == {"cube": (cube, POSITION)}
        assertNoOutput(capfd)
