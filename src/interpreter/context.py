from dataclasses import dataclass, field
from src.errors import CriticalInterpreterError
from src.interpreter.types import Variables, Values


@dataclass
class Context:
    parent: "Context | None" = None
    local_values: Variables = field(default_factory=dict)

    def __getitem__(self, key: str) -> Values:
        if key in self.local_values:
            return self.local_values[key]
        elif self.parent is not None:
            return self.parent[key]
        else:
            raise CriticalInterpreterError(f"Variable {key} is not defined")

    def __setitem__(self, key: str, value: Values) -> None:
        if key in self.local_values:
            if type(self.local_values[key]) != type(value):
                raise CriticalInterpreterError(f"Variable {key} is already defined as {type(self.local_values[key])}")
            self.local_values[key] = value
        elif self.parent is not None:
            self.parent[key] = value
        else:
            raise CriticalInterpreterError(f"Variable {key} is not defined")

    def __eq__(self, __value: object) -> bool:
        return self.local_values == __value

    def declare(self, key: str, value: Values) -> None:
        if key in self.local_values:
            raise CriticalInterpreterError(f"Variable {key} is already defined")
        self.local_values[key] = value

    def __repr__(self) -> str:
        return f"Context(parent={self.parent}, local_values={self.local_values})"

    def __str__(self) -> str:
        return f"Context(parent={self.parent}, local_values={self.local_values})"
