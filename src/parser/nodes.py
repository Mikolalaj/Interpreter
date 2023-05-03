from typing import Any, List


class Parameter:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Parameter):
            return self.name == __value.name
        else:
            return False


class FunctionDefinition:
    def __init__(self, name: str, parameters: List[Parameter], body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"(Function:{self.name} Args:{self.parameters} Body:{self.body})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, FunctionDefinition):
            return self.name == __value.name and self.parameters == __value.parameters and self.body == __value.body
        else:
            return False


class Assignment:
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"(Argument:{self.name} Value:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Assignment):
            return self.name == __value.name and self.value == __value.value
        else:
            return False


class FunctionCall:
    def __init__(self, name: str, arguments: List[Assignment]):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"(FunctionCall:{self.name} Args:{self.arguments})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, FunctionCall):
            return self.name == __value.name and self.arguments == __value.arguments
        else:
            return False


class IfStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"(If:{self.condition} Body:{self.body})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, IfStatement):
            return self.condition == __value.condition and self.body == __value.body
        else:
            return False