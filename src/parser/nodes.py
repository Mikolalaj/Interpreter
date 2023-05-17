from typing import Any, List, Optional
from typing import Literal as LiteralType

from src.tokens import Position


class Assignment:
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"(Assignment: {self.name} Value:{self.value})"

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


class Expression:
    def __init__(self, startPosition: Position):
        self.startPosition = startPosition


class Literal(Expression):
    pass


class LiteralFloat(Literal):
    def __init__(self, startPosition: Position, value: float):
        super().__init__(startPosition)
        self.value = value

    def __repr__(self):
        return f"(LiteralNumber:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LiteralFloat):
            return self.value == __value.value
        else:
            return False


class LiteralInt(Literal):
    def __init__(self, startPosition: Position, value: int):
        super().__init__(startPosition)
        self.value = value

    def __repr__(self):
        return f"(LiteralNumber:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LiteralInt):
            return self.value == __value.value and self.startPosition == __value.startPosition
        else:
            return False


class LiteralBool(Literal):
    def __init__(self, startPosition: Position, value: bool):
        super().__init__(startPosition)
        self.value = value

    def __repr__(self):
        return f"(LiteralBool:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LiteralBool):
            return self.value == __value.value
        else:
            return False


class LiteralIndentifier(Literal):
    def __init__(self, startPosition: Position, value: str):
        super().__init__(startPosition)
        self.value = value

    def __repr__(self):
        return f"(LiteralIdentifier:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LiteralIndentifier):
            return self.value == __value.value
        else:
            return False


class LiteralString(Literal):
    def __init__(self, startPosition: Position, value: str):
        super().__init__(startPosition)
        self.value = value

    def __repr__(self):
        return f"(LiteralString:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LiteralString):
            return self.value == __value.value
        else:
            return False


class PrimaryExpression(Expression):
    def __init__(self, startPosition: Position, isNegated: bool, literal: Expression):
        super().__init__(startPosition)
        self.isNegated = isNegated
        self.literal = literal

    def __repr__(self):
        return f"(PrimaryExpression:{self.literal} Negated:{self.isNegated})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PrimaryExpression):
            return (
                self.isNegated == __value.isNegated
                and self.literal == __value.literal
                and self.startPosition == __value.startPosition
            )
        else:
            return False


class MultiplicativeExpression(Expression):
    def __init__(self, left: Expression, right: Expression, operator: LiteralType["*", "/"]):  # noqa: F722
        super().__init__(left.startPosition)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"(MultiplicativeExpression:{self.left} {self.operator} {self.right})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, MultiplicativeExpression):
            return (
                self.left == __value.left
                and self.operator == __value.operator
                and self.right == __value.right
                and self.startPosition == __value.startPosition
            )
        else:
            return False


class AdditiveExpression(Expression):
    def __init__(
        self,
        left: Expression,
        right: Expression,
        operator: LiteralType["+", "-"],  # noqa: F722
    ):
        super().__init__(left.startPosition)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"(AdditiveExpression:{self.left} {self.operator} {self.right})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, AdditiveExpression):
            return (
                self.left == __value.left
                and self.operator == __value.operator
                and self.right == __value.right
                and self.startPosition == __value.startPosition
            )
        else:
            return False


class ComparisonExpression(Expression):
    def __init__(
        self,
        left: Expression,
        right: Expression,
        operator: LiteralType["<", ">", "<=", ">=", "==", "!="],  # noqa: F722
    ):
        super().__init__(left.startPosition)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"(ComparisonExpression:{self.left} {self.operator} {self.right})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ComparisonExpression):
            return (
                self.left == __value.left
                and self.operator == __value.operator
                and self.right == __value.right
                and self.startPosition == __value.startPosition
            )
        else:
            return False


class LogicalAndExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left.startPosition)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(LogicalAndExpression:{self.left} && {self.right})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LogicalAndExpression):
            return (
                self.left == __value.left
                and self.right == __value.right
                and self.startPosition == __value.startPosition
            )
        else:
            return False


class LogicalOrExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left.startPosition)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(LogicalOrExpression:{self.left} || {self.right})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LogicalOrExpression):
            return (
                self.left == __value.left
                and self.right == __value.right
                and self.startPosition == __value.startPosition
            )
        else:
            return False


class LemonListValue:
    def __init__(self, value: Literal) -> None:
        self.value = value

    def __repr__(self):
        return f"(LemonListValue:{self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LemonListValue):
            return self.value == __value.value
        else:
            return False


class LemonList:
    def __init__(self, values: Optional[List[LemonListValue]]) -> None:
        self.values = values

    def __repr__(self):
        return f"(LemonList:{self.values})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LemonList):
            return self.values == __value.values
        else:
            return False


# Block = LeftBrace StatementWithoutFunciton* RightBrace
class BlockWithoutFunciton:
    def __init__(self, startPosition: Position, statements: List["StatementWithoutFunction"]) -> None:
        self.startPosition = startPosition
        self.statements = statements

    def __repr__(self):
        return f"(BlockWithoutFunciton:{self.statements} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, BlockWithoutFunciton):
            return self.statements == __value.statements and self.startPosition == __value.startPosition
        else:
            return False


# ConditionWithBlock = Condition Block
class ConditionWithBlock:
    def __init__(self, condition: Expression, block: BlockWithoutFunciton) -> None:
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f"(ConditionWithBlock:{self.condition} {self.block})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ConditionWithBlock):
            return self.condition == __value.condition and self.block == __value.block
        else:
            return False


# IfStatement = "if" ConditionWithBlock ( "elif" ConditionWithBlock )* ( "else" Block )? ;
class IfStatement:
    def __init__(
        self,
        startPosition: Position,
        ifCB: ConditionWithBlock,
        elifCBs: Optional[List[ConditionWithBlock]],
        elseBlock: Optional[BlockWithoutFunciton],
    ):
        self.startPosition = startPosition
        self.ifCB = ifCB
        self.elifCBs = elifCBs
        self.elseBlock = elseBlock

    def __repr__(self):
        return f"(IfStatement: {self.ifCB} {self.elifCBs} {self.elseBlock} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, IfStatement):
            return (
                self.ifCB == __value.ifCB
                and self.elifCBs == __value.elifCBs
                and self.elseBlock == __value.elseBlock
                and self.startPosition == __value.startPosition
            )
        else:
            return False


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
    def __init__(
        self,
        name: str,
        parameters: List[Parameter],
        body: Optional[BlockWithoutFunciton],
    ):
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


class VariableDeclaration:
    def __init__(self, startPosition: Position, assignment: Assignment):
        self.startPosition = startPosition
        self.assignment = assignment

    def __repr__(self):
        return f"(VariableDeclaration: {self.assignment} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, VariableDeclaration):
            return self.assignment == __value.assignment and self.startPosition == __value.startPosition
        else:
            return False


class ReturnStatement:
    def __init__(self, startPosition: Position, expression: Expression):
        self.startPosition = startPosition
        self.expression = expression

    def __repr__(self):
        return f"(ReturnStatement: {self.expression} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ReturnStatement):
            return self.expression == __value.expression and self.startPosition == __value.startPosition
        else:
            return False


class WhileOperation:
    pass


class Break(WhileOperation):
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Break)


class Continue(WhileOperation):
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Continue)


class WhileBlock:
    def __init__(self, startPosition: Position, statements: List["StatementWithoutFunction | WhileOperation"]) -> None:
        self.startPosition = startPosition
        self.statements = statements

    def __repr__(self):
        return f"(WhileBlock:{self.statements} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, WhileBlock):
            return self.statements == __value.statements and self.startPosition == __value.startPosition
        else:
            return False


# WhileLoop = "while" Condition WhileBlock ;
class WhileLoop:
    def __init__(self, startPosition: Position, condition: Expression, block: WhileBlock) -> None:
        self.startPosition = startPosition
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f"(WhileLoop:{self.condition} {self.block} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, WhileLoop):
            return (
                self.condition == __value.condition
                and self.block == __value.block
                and self.startPosition == __value.startPosition
            )
        else:
            return False


# ForEachLoop = "foreach" Identifier "in" Identifier WhileBlock ;
class ForEachLoop:
    def __init__(self, startPosition: Position, identifier: str, iterable: str, block: WhileBlock) -> None:
        self.startPosition = startPosition
        self.identifier = identifier
        self.iterable = iterable
        self.block = block

    def __repr__(self):
        return f"(ForEachLoop:{self.identifier} {self.iterable} {self.block} {self.startPosition})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ForEachLoop):
            return (
                self.identifier == __value.identifier
                and self.iterable == __value.iterable
                and self.block == __value.block
                and self.startPosition == __value.startPosition
            )
        else:
            return False


StatementWithoutFunction = (
    Expression
    | IfStatement
    | Assignment
    | FunctionCall
    | VariableDeclaration
    | ReturnStatement
    | WhileLoop
    | ForEachLoop
    # | ObjectDeclaration
    # | ObjectMethodCall
    # | Comment
)

Statement = FunctionDefinition | StatementWithoutFunction
