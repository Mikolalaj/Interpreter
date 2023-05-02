from typing import List


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
