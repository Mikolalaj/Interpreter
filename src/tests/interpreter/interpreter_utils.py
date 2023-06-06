from typing import List
from interpreter.interpreter import Interpreter
from lexer.lexer import Lexer
from parser.nodes import Node
from parser.parser import Parser
from lexer.source import StringSource


class ParserMock(Parser):
    def __init__(self, nodes: List[Node]) -> None:
        lexer = Lexer(StringSource(""))
        super().__init__(lexer, None)
        self.nodes = nodes

    def parse(self) -> List[Node]:
        return self.nodes


def getInterpreter(nodes: List[Node]) -> Interpreter:
    parser = ParserMock(nodes=nodes)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    return interpreter


def assertNoOutput(capfd):
    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""
