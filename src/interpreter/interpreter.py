from typing import List, Optional, cast
from typing import Literal as LiteralType
from src.errors import CriticalInterpreterError, InterpreterError
from src.interpreter.context import Context
from src.interpreter.objects import Cuboid, Object, Pyramid, Cone, Cylinder, Tetrahedron, Sphere
from src.interpreter.types import Values
from src.parser.nodes import (
    AdditiveExpression,
    Argument,
    Assignment,
    BlockWithoutFunciton,
    ComparisonExpression,
    FunctionCall,
    FunctionDefinition,
    IfStatement,
    LemonList,
    LiteralBool,
    LiteralFloat,
    LiteralIdentifier,
    LiteralInt,
    LiteralString,
    LiteralSubscriptable,
    LogicalAndExpression,
    LogicalOrExpression,
    MultiplicativeExpression,
    Node,
    ObjectConstructor,
    ObjectType,
    PrimaryExpression,
    ReturnStatement,
    VariableDeclaration,
)
from src.parser.parser import Parser


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
        self.context = Context()

    def interpret(self):
        nodes = self.parser.parse()
        for node in nodes:
            try:
                self.visit(node)
            except TypeError as e:
                print(f"TypeError: {e}")
                return
            except CriticalInterpreterError as e:
                print(e)
                return
            except InterpreterError as e:
                print(e)

    def visitVariableDeclaration(self, node: VariableDeclaration) -> None:
        variableName = node.assignment.name
        value = node.assignment.value
        if type(variableName) == str:
            self.context.declare(variableName, self.visit(value), node.startPosition)
        else:
            raise InterpreterError("Variable declaration's name has to be an identifier, not object property", node)

    def visitAssignment(self, node: Assignment):
        variableName = node.name
        value = node.value
        if type(variableName) == str:
            self.context.set(variableName, self.visit(value), node.position)
        else:
            raise InterpreterError("Assignment's name has to be an identifier, not object property", node)

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

    # Literals

    def visitLiteralFloat(self, node: LiteralFloat) -> float:
        return node.value

    def visitLiteralInt(self, node: LiteralInt) -> int:
        return node.value

    def visitLiteralBool(self, node: LiteralBool) -> bool:
        return node.value

    def visitLiteralString(self, node: LiteralString) -> str:
        return node.value

    def visitLiteralIdentifier(self, node: LiteralIdentifier) -> Values:
        return self.context.get(node.value, node.startPosition)

    def visitLiteralSubscriptable(self, node: LiteralSubscriptable) -> int | float | bool | str:
        subscriptable = self.context.get(node.value, node.startPosition)
        index = self.visit(node.subscript)
        if type(index) != int:
            raise TypeError(f"String indices must be integers, not {type(index)}")
        if type(subscriptable) == str or type(subscriptable) == list:
            subscriptable = cast(str | list, subscriptable)
            if index >= len(subscriptable):
                raise InterpreterError(f"Index {index} is out of range")
            return subscriptable[index]
        else:
            raise TypeError(f"Type {type(subscriptable)} is not subscriptable")

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

    # If

    def visitIfStatement(self, node: IfStatement) -> Optional[Values]:
        conditionsWithBlocks = [node.ifCB] + (node.elifCBs or [])
        for conditionWithBlock in conditionsWithBlocks:
            if self.visit(conditionWithBlock.condition):
                self.nextContext()
                returnValue = self.visit(conditionWithBlock.block)
                self.previousContext()
                return returnValue
        if node.elseBlock:
            return self.visit(node.elseBlock)
        return None

    def visitBlockWithoutFunciton(self, node: BlockWithoutFunciton):
        returnValue = None
        for statement in node.statements:
            returnValue = self.visit(statement)
            if returnValue is not None:
                break
        return returnValue

    # Functions

    def visitArgument(self, node: Argument):
        variableName = node.name
        value = node.value
        self.context.declare(variableName, self.visit(value), node.position)

    def visitFunctionDefinition(self, node: FunctionDefinition):
        functionName = node.name
        if not self.context.isNameAvailable(functionName):
            raise InterpreterError(f"Function '{functionName}' is already defined", node)
        self.context.declare(functionName, node, node.position)

    def visitFunctionCall(self, node: FunctionCall) -> Optional[Values]:
        function = self.context.get(node.name, node.startPosition)
        if type(function) != FunctionDefinition:
            raise TypeError(f"Type {type(function)} is not callable")
        function = cast(FunctionDefinition, function)
        self.nextContext()
        self.expectNumberOfArguments(node.arguments, len(function.parameters), node)
        for parameter in function.parameters:
            argument = self.getArgumentValue(node, parameter)
            self.context.declare(parameter, argument, node.startPosition)
        result = self.visit(function.body)
        result = cast(Values | None, result)
        self.previousContext()
        return result

    def visitReturnStatement(self, node: ReturnStatement) -> Optional[Values]:
        return self.visit(node.expression)

    def getArgumentValue(self, node: FunctionCall, name: str) -> Values:
        value = next((argument.value for argument in node.arguments if argument.name == name), None)
        if value is None:
            raise InterpreterError(f"Funciton {node.name} requires {name} argument", node)
        return self.visit(value)

    # Objects

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

    def expectNumberOfArguments(
        self, arguments: list[Argument], expected: int, node: ObjectConstructor | FunctionCall
    ) -> None:
        if len(arguments) != expected:
            if type(node) == FunctionCall:
                raise InterpreterError(f"{node.name} constructor takes 3 arguments, {len(arguments)} were given", node)
            elif type(node) == ObjectConstructor:
                raise InterpreterError(
                    f"{node.objectType} constructor takes 3 arguments, {len(arguments)} were given", node
                )

    def getObjectArgumentValue(
        self, node: ObjectConstructor, name: LiteralType["width", "length", "height", "radius", "edge"]  # noqa: F821
    ) -> int | float:
        value = next((argument.value for argument in node.arguments if argument.name == name), None)
        if value is None:
            raise InterpreterError(f"{node.objectType} constructor requires {name} argument", node)
        expressionValue = self.visit(value)
        if type(expressionValue) != int and type(expressionValue) != float:
            raise InterpreterError(f"{node.objectType} constructor requires {name} argument to be a number", node)
        return expressionValue

    # Context

    def nextContext(self) -> None:
        self.context = Context(self.context)

    def previousContext(self) -> None:
        if self.context.parent is None:
            raise InterpreterError("Cannot exit global context")
        self.context = self.context.parent


class Function:
    def __init__(self, arguments: list[str], block: BlockWithoutFunciton):
        self.arguments = arguments
        self.block = block
