from src.interpreter.objects import Object
from src.parser.nodes import FunctionDefinition
from src.tokens import Position

Literals = int | float | bool | str | list
Objects = Object
Values = Literals | Objects | FunctionDefinition
Variables = dict[str, Values]
VariableWithPosition = dict[str, tuple[Values, Position]]
