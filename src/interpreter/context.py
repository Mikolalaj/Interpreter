from dataclasses import dataclass, field
from typing import Optional
from src.errors import CriticalInterpreterError
from src.interpreter.objects import Object
from src.interpreter.types import VariableWithPosition, Values
from src.tokens import Position


@dataclass
class Context:
    parent: "Context | None" = None
    local_values: VariableWithPosition = field(default_factory=dict)

    def get(self, key: str, position: Position) -> Values:
        if self.__isNameInLocalValues(key):
            return self.local_values[key][0]
        elif self.parent is not None:
            return self.parent.get(key, position)
        else:
            raise CriticalInterpreterError(f"Variable {key} at {position} is not defined")

    def __getLocal(self, key: str) -> Optional[tuple[Values, Position]]:
        if self.__isNameInLocalValues(key):
            return self.local_values[key]
        return None

    def set(self, key: str, value: Values, position: Position) -> None:
        local = self.__getLocal(key)
        if local is not None:
            if type(local[0]) != type(value):
                raise CriticalInterpreterError(
                    f"Variable {key} at {position} is already defined as {type(local[0])} at {local[1]}"  # noqa: E501
                )
            self.local_values[key] = (value, position)
        elif self.parent is not None:
            self.parent.set(key, value, position)
        else:
            raise CriticalInterpreterError(f"Variable {key} is not defined")

    def setObjectProperty(self, key: str, property: str, value: Values, position: Position) -> None:
        local = self.__getLocal(key)
        if local is not None:
            if not isinstance(local[0], Object):
                raise CriticalInterpreterError(
                    f"Variable {key} at {position} is not an object. It's defined as {type(local[0])} at {local[1]}"  # noqa: E501
                )
            setattr(local[0], property, value)
        elif self.parent is not None:
            self.parent.setObjectProperty(key, property, value, position)
        else:
            raise CriticalInterpreterError(f"Variable {key} is not defined")

    def declare(self, key: str, value: Values, position: Position) -> None:
        local = self.__getLocal(key)
        if local is not None:
            raise CriticalInterpreterError(f"Variable {key} at {position} is already defined at {local[1]}")
        self.local_values[key] = (value, position)

    def __isNameInLocalValues(self, name: str) -> bool:
        return any([name == key for key in self.local_values])

    def __eq__(self, __value: object) -> bool:
        return self.local_values == __value

    def __repr__(self) -> str:
        return f"Context(parent={self.parent}, local_values={self.local_values})"

    def __str__(self) -> str:
        return f"Context(parent={self.parent}, local_values={self.local_values})"

    def isNameAvailable(self, name: str) -> bool:
        if name in self.local_values:
            return False
        elif self.parent is not None:
            return self.parent.isNameAvailable(name)
        else:
            return True
