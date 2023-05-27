from typing import Callable, List, cast
from typing import Literal as LiteralType
from src.errors import InterpreterError
from src.interpreter.objects import Cuboid, Object, Pyramid, Cone, Cylinder, Tetrahedron, Sphere
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    ComparisonExpression,
    Expression,
    LemonList,
    LiteralBool,
    LiteralFloat,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
    LogicalAndExpression,
    LogicalOrExpression,
    MultiplicativeExpression,
    Node,
    ObjectConstructor,
    ObjectType,
    PrimaryExpression,
    VariableDeclaration,
)
from src.parser.parser import Parser


Literals = int | float | bool | str | list
Objects = Object
Functions = Callable
Variables = dict[str, Literals | Objects | Functions]


class NodeVisitor(object):
    def visit(self, node: Node):
        method_name = "visit" + type(node).__name__
        visitor = getattr(self, method_name, self.genericVisit)
        return visitor(node)

    def genericVisit(self, node):
        raise Exception(f"No visit{type(node).__name__} method")


class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser) -> None:
        self.parser = parser
        self.variables: Variables = {}
        self.literals: dict[str, Literals] = {}
        self.objects: dict[str, Objects] = {}
        self.functions: dict[str, Functions] = {}

    def isNameAvailable(self, name: str) -> bool:
        if name in self.literals or name in self.objects:
            return False
        return True

    def interpret(self):
        nodes = self.parser.parse()
        for node in nodes:
            self.visit(node)

    def visitVariableDeclaration(self, node: VariableDeclaration) -> None:
        variableName = node.assignment.name
        value = node.assignment.value
        if type(variableName) == str:
            if not self.isNameAvailable(variableName):
                raise InterpreterError(f"Variable {variableName} already declared", node)
            if type(value) == ObjectConstructor:
                self.objects[variableName] = self.visit(node.assignment.value)
            else:
                self.literals[variableName] = self.visit(node.assignment.value)
        else:
            raise InterpreterError("Variable declaration's name has to be an identifier, not object property", node)

    def visitLogicalOrExpression(self, node: LogicalOrExpression) -> bool:
        left: int | float | str | bool = self.visit(node.left)
        right: int | float | str | bool = self.visit(node.right)

        if type(left) == bool and type(right) == bool:
            return left or right
        else:
            raise TypeError(f"Logical and operator requires two boolean values, not {type(left)} and {type(right)}")

    def visitLogicalAndExpression(self, node: LogicalAndExpression) -> bool:
        left: int | float | str | bool = self.visit(node.left)
        right: int | float | str | bool = self.visit(node.right)

        if type(left) == bool and type(right) == bool:
            return left and right
        else:
            raise TypeError(f"Logical and operator requires two boolean values, not {type(left)} and {type(right)}")

    def visitComparisonExpression(self, node: ComparisonExpression) -> bool:
        left: int | float | str | bool = self.visit(node.left)
        right: int | float | str | bool = self.visit(node.right)
        if node.operator == "==":
            return left == right
        elif node.operator == "!=":
            return left != right

        if (type(left) == int or type(left) == float) and (type(right) == int or type(right) == float):
            if node.operator == "<":
                return left < right
            elif node.operator == "<=":
                return left <= right
            elif node.operator == ">":
                return left > right
            elif node.operator == ">=":
                return left >= right
            else:
                raise InterpreterError(f"Operator {node.operator} is not supported", node)
        else:
            raise TypeError(f"Unsupported operand type(s) for {node.operator}: '{type(left)}' and '{type(right)}'")

    def visitAdditiveExpression(self, node: AdditiveExpression) -> int | float | str:
        left: int | float | str | bool = self.visit(node.left)
        right: int | float | str | bool = self.visit(node.right)

        if node.operator == "+":
            if type(left) == str and type(right) == str:
                return left + right
            elif (type(left) == int or type(left) == float) and (type(right) == int or type(right) == float):
                return left + right
            else:
                raise TypeError(f"Unsupported operand type(s) for {node.operator}: '{type(left)}' and '{type(right)}'")
        elif node.operator == "-":
            if (type(left) == int or type(left) == float) and (type(right) == int or type(right) == float):
                return left + right
            else:
                raise TypeError(f"Unsupported operand type(s) for {node.operator}: '{type(left)}' and '{type(right)}'")
        else:
            raise InterpreterError(f"Operator {node.operator} is not supported", node)

    def visitMultiplicativeExpression(self, node: MultiplicativeExpression) -> int | float:
        left: int | float | str | bool = self.visit(node.left)
        right: int | float | str | bool = self.visit(node.right)

        if (type(left) == int or type(left) == float) and (type(right) == int or type(right) == float):
            if node.operator == "*":
                return left * right
            elif node.operator == "/":
                return left / right
            else:
                raise InterpreterError(f"Operator {node.operator} is not supported", node)
        else:
            raise TypeError(f"Unsupported operand type(s) for {node.operator}: '{type(left)}' and '{type(right)}'")

    def visitPrimaryExpression(self, node: PrimaryExpression):
        literalValue = self.visit(node.literal)
        if node.isNegated:
            if type(literalValue) == int or type(literalValue) == float:
                return -literalValue
            elif type(literalValue) == bool:
                return not literalValue
            else:
                raise TypeError(f"Unsupported type for negation: '{type(literalValue)}'")
        else:
            return literalValue

    def visitLiteralFloat(self, node: LiteralFloat) -> float:
        return node.value

    def visitLiteralInt(self, node: LiteralInt) -> int:
        return node.value

    def visitLiteralBool(self, node: LiteralBool) -> bool:
        return node.value

    def visitLiteralString(self, node: LiteralString) -> str:
        return node.value

    def visitLiteralIdentifier(self, node: LiteralIdentifier) -> int | float | bool | str | list | Object | Callable:
        identifier = node.value
        if identifier in self.literals:
            return self.literals[identifier]
        elif node.value in self.objects:
            return self.objects[identifier]
        else:
            raise InterpreterError(f"Variable {node.value} is not defined", node)

    def visitLemonList(self, node: LemonList) -> List[int] | List[float] | List[bool] | List[str] | List:
        if len(node.values) == 0:
            return []
        firstValue = self.visit(node.values[0])
        listType = type(firstValue)
        list = [firstValue]
        for expression in node.values[1:]:
            value = self.visit(expression)
            if type(value) != listType:
                raise InterpreterError("List cannot contain multiple types", node)
            else:
                list.append(value)
        return cast(List[int] | List[float] | List[bool] | List[str], list)

    def visitObjectConstructor(self, node: ObjectConstructor) -> Object:
        if node.objectType == ObjectType.CUBOID:
            self.expectNumberOfArguments(node.arguments, 3, node)
            width = self.getObjectArgumentValue(node, "width")
            length = self.getObjectArgumentValue(node, "length")
            height = self.getObjectArgumentValue(node, "height")
            return Cuboid(width=width, length=length, height=height)
        elif node.objectType == ObjectType.PYRAMID:
            self.expectNumberOfArguments(node.arguments, 3, node)
            width = self.getObjectArgumentValue(node, "width")
            length = self.getObjectArgumentValue(node, "length")
            height = self.getObjectArgumentValue(node, "height")
            return Pyramid(width=width, length=length, height=height)
        elif node.objectType == ObjectType.SPHERE:
            self.expectNumberOfArguments(node.arguments, 1, node)
            radius = self.getObjectArgumentValue(node, "radius")
            return Sphere(radius=radius)
        elif node.objectType == ObjectType.CONE:
            self.expectNumberOfArguments(node.arguments, 2, node)
            radius = self.getObjectArgumentValue(node, "radius")
            height = self.getObjectArgumentValue(node, "height")
            return Cone(radius=radius, height=height)
        elif node.objectType == ObjectType.CYLINDER:
            self.expectNumberOfArguments(node.arguments, 2, node)
            radius = self.getObjectArgumentValue(node, "radius")
            height = self.getObjectArgumentValue(node, "height")
            return Cylinder(radius=radius, height=height)
        elif node.objectType == ObjectType.TETRAHEDRON:
            self.expectNumberOfArguments(node.arguments, 1, node)
            edge = self.getObjectArgumentValue(node, "edge")
            return Tetrahedron(edge=edge)
        else:
            raise InterpreterError(f"Object type {node.objectType} is not supported", node)

    def expectNumberOfArguments(self, arguments: list[Assignment], expected: int, node: ObjectConstructor) -> None:
        if len(arguments) != expected:
            raise InterpreterError(
                f"{node.objectType} constructor takes 3 arguments, {len(arguments)} were given", node
            )

    def getObjectArgumentValue(
        self, node: ObjectConstructor, name: LiteralType["width", "length", "height", "radius", "edge"]  # noqa: F821
    ) -> int | float:
        value = next((argument.value for argument in node.arguments if argument.name == name), None)
        if value is None:
            raise InterpreterError(f"Cuboid constructor requires {name} argument", node)
        if type(value) != Expression:
            raise InterpreterError(f"Cuboid constructor requires {name} argument to be an expression", node)
        expressionValue = self.visit(value)
        if type(expressionValue) != int and type(expressionValue) != float:
            raise InterpreterError("Cuboid constructor requires width argument to be a number", node)
        return expressionValue
