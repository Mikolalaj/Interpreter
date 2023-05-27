from typing import List
from src.interpreter.interpreter import Interpreter
from src.lexer import Lexer
from src.parser.nodes import Node
from src.parser.parser import Parser
from src.source import StringSource


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
