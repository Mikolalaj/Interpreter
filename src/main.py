from lexer.lexer import Lexer
from lexer.source import StringSource
from parser.parser import Parser
from interpreter.interpreter import Interpreter

code = """
let a = [1, 2, 3]
foreach (i in a) {
    print(out=i)
}
"""

lexer = Lexer(StringSource(code))
parser = Parser(lexer)
interpreter = Interpreter(parser)

interpreter.interpret()
