from lexer.lexer import Lexer
from lexer.source import StringSource
from parser.parser import Parser
from interpreter.interpreter import Interpreter


def interpretCode(code: str):
    lexer = Lexer(StringSource(code))
    parser = Parser(lexer)
    interpreter = Interpreter(parser)

    interpreter.interpret()


code = """
function add(a, b) {
    return a + b
}

let cube = Cuboid(width=2, height=3, length=4)

if (2 > 3) {
    cube.width = add(a=2, b=3)
}
else {
    cube.width = add(a=3, b=4)
}

let cylinder = Cylinder(radius=2, height=3)

let volume = cube.getVolume() + cylinder.getVolume()
let volumeString = string(value=volume)
print(out="Volume: " + volumeString)

let objects = [cube, cylinder]

foreach (object in objects) {
    object.display()
}

let string = "2"
let number = int(value=string) + 3
print(out=number)
"""

interpretCode(code)
