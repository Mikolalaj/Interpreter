from src.interpreter.objects import Cuboid
from .utils import assertNoOutput, getInterpreter
from src.parser.nodes import (
    Argument,
    Assignment,
    FunctionCall,
    LiteralInt,
    ObjectConstructor,
    ObjectMethodCall,
    ObjectType,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestObjects:
    def testObjectConstructor(self, capfd):
        """
        let a = new Cuboid(width=2, height=3, length=4)
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

    def testObjectObjectMethodCall(self, capfd):
        """
        let cube = new Cuboid(width=2, height=3, length=4)
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
