from src.interpreter.objects import Cuboid
from .utils import getInterpreter
from src.parser.nodes import (
    Assignment,
    LiteralInt,
    ObjectConstructor,
    ObjectType,
    VariableDeclaration,
)
from src.tokens import Position

POSITION = Position(0, 0)


class TestObjects:
    def testObjectConstructor(self):
        """
        let a = new Cuboid(width=2, height=3, length=4)
        """
        interpreter = getInterpreter(
            [
                VariableDeclaration(
                    POSITION,
                    Assignment(
                        "a",
                        ObjectConstructor(
                            POSITION,
                            ObjectType.CUBOID,
                            [
                                Assignment("width", LiteralInt(POSITION, 2)),
                                Assignment("height", LiteralInt(POSITION, 3)),
                                Assignment("length", LiteralInt(POSITION, 4)),
                            ],
                        ),
                    ),
                ),
            ]
        )

        assert interpreter.context == {"a": Cuboid(width=2, height=3, length=4)}
