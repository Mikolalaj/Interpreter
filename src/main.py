from lexer.lexer import Lexer
from lexer.source import StringSource
from parser.parser import Parser
from interpreter.interpreter import Interpreter

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

let objects = [cube, cylinder]

foreach (object in objects) {
    object.display()
}
"""

lexer = Lexer(StringSource(code))
parser = Parser(lexer)
interpreter = Interpreter(parser)

interpreter.interpret()
