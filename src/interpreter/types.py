from typing import Callable
from src.interpreter.objects import Object

Literals = int | float | bool | str | list
Objects = Object
Functions = Callable
Values = Literals | Objects | Functions
Variables = dict[str, Values]
