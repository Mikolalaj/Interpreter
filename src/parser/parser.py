from typing import List, Optional
from src.lexer import Lexer
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    BlockWithoutFunciton,
    Break,
    ComparisonExpression,
    ConditionWithBlock,
    Continue,
    ForEachLoop,
    FunctionCall,
    IfStatement,
    LemonList,
    LemonListValue,
    Literal,
    LiteralBool,
    LiteralFloat,
    LiteralIndentifier,
    LiteralInt,
    LiteralString,
    LogicalAndExpression,
    LogicalOrExpression,
    MultiplicativeExpression,
    Parameter,
    FunctionDefinition,
    PrimaryExpression,
    Expression,
    ReturnStatement,
    Statement,
    StatementWithoutFunction,
    VariableDeclaration,
    WhileBlock,
    WhileLoop,
    WhileOperation,
)
from src.token_type import TokenType
from src.tokens import Position, Token


class Parser:
    def __init__(self, lexer: Lexer, tokens: Optional[List[Token]] = None) -> None:
        self.lexer = lexer
        self.token = tokens[0] if tokens else lexer.getNextToken()
        self.tokens = tokens
        self.assignableTokens = [
            TokenType.VT_ID,
            TokenType.VT_INT,
            TokenType.VT_FLOAT,
            TokenType.VT_STRING,
            TokenType.VT_BOOLEAN,
        ]

        self.nextLexerToken()

    def nextLexerToken(self) -> None:
        if self.tokens:
            if len(self.tokens) > 0:
                self.token = self.tokens.pop(0)
            else:
                self.token = Token(TokenType.VT_EOF, self.token.startPosition)
        else:
            self.token = self.lexer.getNextToken()

    def parse(self) -> List:
        objects = []
        while self.token.type != TokenType.VT_EOF:
            node = self.parseStatement()
            if node is not None:
                objects.append(node)
            else:
                print(f"Unexpected token {self.token}")
                self.nextLexerToken()
        return objects

    def parseStatement(self) -> Optional[Statement]:
        return self.parseStatementWithoutFunction() or self.parseFunctionDefinition()

    def parseStatementWithoutFunction(self) -> Optional[StatementWithoutFunction]:
        return (
            self.parseStartingWithIdentifier()
            or self.parseExpression()
            or self.parseIfStatement()
            or self.parseVariableDeclaration()
            or self.parseReturnStatement()
            or self.parseWhileLoop()
            or self.parseForEachLoop()
        )

    def parseParameters(self) -> Optional[List[Parameter]]:
        parameters = []
        if self.token.type != TokenType.T_LPARENT:
            return None
        self.nextLexerToken()
        if self.token.type == TokenType.VT_ID:
            parameters.append(Parameter(self.token.getValue()))
            self.nextLexerToken()
            while self.token.type == TokenType.T_COMMA:
                self.nextLexerToken()
                if self.token.type == TokenType.VT_ID:
                    parameters.append(Parameter(self.token.getValue()))
                    self.nextLexerToken()
                else:
                    raise Exception(f"Expected variable type, got {self.token}")
        if self.token.type == TokenType.T_RPARENT:
            self.nextLexerToken()
            return parameters
        else:
            raise Exception(f"Expected ')', got {self.token}")

    def parseFunctionDefinition(self) -> Optional[FunctionDefinition]:
        if self.token.type != TokenType.T_FUNCTION:
            return None
        self.nextLexerToken()
        if self.token.type != TokenType.VT_ID:
            raise Exception(f"Expected function name, got {self.token}")
        name = self.token.getValue()
        self.nextLexerToken()
        parameters = self.parseParameters()
        if parameters is None:
            raise Exception(f"Expected parameters, got {self.token}")
        body = self.parseBlockWithoutFunction()
        if body is None:
            raise Exception(f"Expected block, got {self.token}")
        self.nextLexerToken()
        return FunctionDefinition(name, parameters, body)

    # Assignment = Identifier = ( Expression | String | List | FunctionCall | ObjectMethodCall | ObjectProperty | ListGetValue ) ;
    def parseAssignment(self, name: Optional[str] = None) -> Optional[Assignment]:
        if not name:
            if self.token.type != TokenType.VT_ID:
                return None
            name = self.token.getValue()
            self.nextLexerToken()

        if self.token.type != TokenType.T_ASSIGN:
            return None
        self.nextLexerToken()
        expression = self.parseExpression()
        if expression is not None:
            # self.nextLexerToken()
            return Assignment(name, expression)
        list = self.parseList()
        if list is not None:
            self.nextLexerToken()
            return Assignment(name, list)
        if self.token.type == TokenType.VT_STRING:
            value = self.token.getValue()
            self.nextLexerToken()
            return Assignment(name, value)
        value = self.token.getValue()
        self.nextLexerToken()
        return Assignment(name, value)

    def parseArguments(self) -> Optional[List[Assignment]]:
        arguments = []
        if self.token.type != TokenType.T_LPARENT:
            return None
        self.nextLexerToken()
        argument = self.parseAssignment()
        if argument:
            arguments.append(argument)
            while self.token.type == TokenType.T_COMMA:
                self.nextLexerToken()
                argument = self.parseAssignment()
                if argument:
                    arguments.append(argument)
                else:
                    raise Exception(f"Expected variable type, got {self.token}")
        if self.token.type == TokenType.T_RPARENT:
            self.nextLexerToken()
            return arguments
        else:
            raise Exception(f"Expected ')', got {self.token}")

    def parseStartingWithIdentifier(self) -> Optional[FunctionCall | Assignment | LiteralIndentifier]:
        if self.token.type != TokenType.VT_ID:
            return None
        name = self.token.getValue()
        startPosition = self.token.startPosition
        self.nextLexerToken()
        arguments = self.parseArguments()
        if arguments is not None:
            return FunctionCall(name, arguments)
        assignment = self.parseAssignment(name)
        if assignment is not None:
            return assignment
        else:
            return LiteralIndentifier(startPosition, name)

    # List = LeftBracket ListValue (Comma ListValue)* RightBracket ;
    def parseList(self) -> Optional[LemonList]:
        if self.token.type != TokenType.T_LSQBRACKET:
            return None
        self.nextLexerToken()
        values = self.parseListValues()
        if self.token.type != TokenType.T_RSQBRACKET:
            raise Exception(f"Expected ']', got {self.token}")
        self.nextLexerToken()
        return LemonList(values)

    # ListValue = Number | String | Boolean | Identifier ;
    def parseListValues(self) -> Optional[List[LemonListValue]]:
        values = []
        while self.isType(
            TokenType.VT_INT, TokenType.VT_FLOAT, TokenType.VT_STRING, TokenType.VT_BOOLEAN, TokenType.VT_ID
        ):
            if self.token.type == TokenType.VT_INT:
                values.append(LemonListValue(LiteralInt(self.token.startPosition, self.token.getValue())))
            elif self.token.type == TokenType.VT_FLOAT:
                values.append(LemonListValue(LiteralFloat(self.token.startPosition, self.token.getValue())))
            elif self.token.type == TokenType.VT_STRING:
                values.append(LemonListValue(LiteralString(self.token.startPosition, self.token.getValue())))
            elif self.token.type == TokenType.VT_BOOLEAN:
                values.append(LemonListValue(LiteralBool(self.token.startPosition, self.token.getValue())))
            elif self.token.type == TokenType.VT_ID:
                values.append(LemonListValue(LiteralIndentifier(self.token.startPosition, self.token.getValue())))
            else:
                if len(values) == 0:
                    return None
                raise Exception(f"Expected int, float, string, bool or identifier, got {self.token}")
            self.nextLexerToken()
            if self.token.type == TokenType.T_COMMA:
                self.nextLexerToken()
            elif self.token.type == TokenType.T_RSQBRACKET:
                break
            else:
                raise Exception(f"Expected ',', got {self.token}")
        return values

    # Literal = Identifier | Boolean | Number ;
    def parseLiteral(self) -> Optional[Literal]:
        token = self.token
        if self.token.type == TokenType.VT_BOOLEAN:
            self.nextLexerToken()
            return LiteralBool(token.startPosition, token.getValue())
        if self.token.type == TokenType.VT_INT:
            self.nextLexerToken()
            return LiteralInt(token.startPosition, token.getValue())
        if self.token.type == TokenType.VT_FLOAT:
            self.nextLexerToken()
            return LiteralFloat(token.startPosition, token.getValue())
        if self.token.type == TokenType.VT_ID:
            self.nextLexerToken()
            return LiteralIndentifier(token.startPosition, token.getValue())
        return None

    # PrimaryExpression = NotOperator? Literal | ( LeftParenthesis Expression RightParenthesis ) ;
    def parsePrimaryExpression(self) -> Optional[Expression]:
        isNegated = False
        startPosition = None
        if self.isType(TokenType.T_NOT, TokenType.T_MINUS):
            startPosition = self.token.startPosition
            self.nextLexerToken()
            isNegated = True
        if self.isType(TokenType.T_LPARENT):
            if not isNegated:
                startPosition = self.token.startPosition
            self.nextLexerToken()
            expression = self.parseExpression()
            if expression is None:
                raise Exception(f"Expected expression, got {self.token}")
            if self.isType(TokenType.T_RPARENT):
                self.nextLexerToken()
                if startPosition:
                    return PrimaryExpression(startPosition, isNegated, expression)
                else:
                    raise Exception("Start Position is not set")
            else:
                raise Exception(f"Expected ')', got {self.token}")
        else:
            literal = self.parseLiteral()
            if literal is None:
                return None
            if isNegated:
                if startPosition:
                    return PrimaryExpression(startPosition, True, literal)
                else:
                    raise Exception("Start Position is not set")
            return literal

    # MultiplicativeExpression = PrimaryExpression ( ( "*" | "/" ) PrimaryExpression )* ;
    def parseMultiplicativeExpression(self) -> Optional[Expression]:
        left = self.parsePrimaryExpression()
        if left is None:
            return None
        if self.isType(TokenType.T_MUL, TokenType.T_DIV) and self.isNextSameLine(left.startPosition):
            operator = "*" if self.token.type == TokenType.T_MUL else "/"
            self.nextLexerToken()
            right = self.parseMultiplicativeExpression()
            if right is None:
                raise Exception(f"Expected expression, got {self.token}")
            return MultiplicativeExpression(left, right, operator)
        return left

    # AdditiveExpression = MultiplicativeExpression ( ( "+" | "-" ) MultiplicativeExpression )* ;
    def parseAdditiveExpression(self) -> Optional[Expression]:
        left = self.parseMultiplicativeExpression()
        if left is None:
            return None
        if self.isType(TokenType.T_PLUS, TokenType.T_MINUS) and self.isNextSameLine(left.startPosition):
            operator = "+" if self.token.type == TokenType.T_PLUS else "-"
            self.nextLexerToken()
            right = self.parseAdditiveExpression()
            if right is None:
                raise Exception(f"Expected expression, got {self.token}")
            return AdditiveExpression(left, right, operator)
        return left

    # ComparisonExpression = AdditiveExpression ( ( "<" | ">" | "<=" | ">=" | "==" | "!=" ) AdditiveExpression )? ;
    def parseComparisonExpression(self) -> Optional[Expression]:
        left = self.parseAdditiveExpression()
        if left is None:
            return None
        if self.isType(
            TokenType.T_LESS,
            TokenType.T_GREATER,
            TokenType.T_LESS_OR_EQ,
            TokenType.T_GREATER_OR_EQ,
            TokenType.T_EQ,
            TokenType.T_NOT_EQ,
        ) and self.isNextSameLine(left.startPosition):
            operator = self.token.type.value
            self.nextLexerToken()
            right = self.parseComparisonExpression()
            if right is None:
                raise Exception(f"Expected expression, got {self.token}")
            return ComparisonExpression(left, right, operator)
        return left

    # LogicalAndExpression = ComparisonExpression ( AndOperator ComparisonExpression )* ;
    def parseLogicalAndExpression(self) -> Optional[Expression]:
        left = self.parseComparisonExpression()
        if left is None:
            return None
        if self.isType(TokenType.T_AND) and self.isNextSameLine(left.startPosition):
            self.nextLexerToken()
            right = self.parseLogicalAndExpression()
            if right is None:
                raise Exception(f"Expected expression, got {self.token}")
            return LogicalAndExpression(left, right)
        return left

    # LogicalOrExpression = LogicalAndExpression ( OrOperator LogicalAndExpression )* ;
    def parseLogicalOrExpression(self) -> Optional[Expression]:
        left = self.parseLogicalAndExpression()
        if left is None:
            return None
        if self.isType(TokenType.T_OR) and self.isNextSameLine(left.startPosition):
            self.nextLexerToken()
            right = self.parseLogicalOrExpression()
            if right is None:
                raise Exception(f"Expected expression, got {self.token}")
            return LogicalOrExpression(left, right)
        return left

    # Expression = LogicalOrExpression ;
    def parseExpression(self) -> Optional[Expression]:
        return self.parseLogicalOrExpression()

    # IfStatement = "if" ConditionWithBlock ( "elif" ConditionWithBlock )* ( "else" Block )? ;
    def parseIfStatement(self) -> Optional[IfStatement]:
        if not self.isType(TokenType.T_IF):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        conditionWithBlock = self.parseConditionWithBlock()
        elifCBs = []
        while self.isType(TokenType.T_ELSEIF):
            self.nextLexerToken()
            elifCBs.append(self.parseConditionWithBlock())
        elseBlock = None
        if self.isType(TokenType.T_ELSE):
            self.nextLexerToken()
            elseBlock = self.parseBlockWithoutFunction()
        return IfStatement(startPosition, conditionWithBlock, elifCBs if len(elifCBs) else None, elseBlock)

    # ConditionWithBlock = Condition Block
    def parseConditionWithBlock(self) -> ConditionWithBlock:
        condition = self.parseCondition()
        if condition is None:
            raise Exception(f"Expected condition, got {self.token}")
        block = self.parseBlockWithoutFunction()
        if block is None:
            raise Exception(f"Expected block, got {self.token}")
        return ConditionWithBlock(condition, block)

    def parseCondition(self) -> Optional[Expression]:
        if not self.isType(TokenType.T_LPARENT):
            return None
        self.nextLexerToken()
        expression = self.parseExpression()
        if expression is None:
            raise Exception(f"Expected expression, got {self.token}")
        if self.isType(TokenType.T_RPARENT):
            self.nextLexerToken()
            return expression
        else:
            raise Exception(f"Expected ')', got {self.token}")

    def parseBlockWithoutFunction(self) -> Optional[BlockWithoutFunciton]:
        if not self.isType(TokenType.T_LBRACKET):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        statements: List[StatementWithoutFunction] = []
        while not self.isType(TokenType.T_RBRACKET):
            statement = self.parseStatementWithoutFunction()
            if statement is None:
                raise Exception(f"Expected statement, got {self.token}")
            statements.append(statement)
        self.nextLexerToken()
        return BlockWithoutFunciton(startPosition, statements)

    # VariableDeclaration = "let" VariableAssignment ;
    def parseVariableDeclaration(self) -> Optional[VariableDeclaration]:
        if not self.isType(TokenType.T_VARIABLE):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        variableAssignment = self.parseAssignment()
        if variableAssignment is None:
            raise Exception(f"Expected variable assignment, got {self.token}")
        return VariableDeclaration(startPosition, variableAssignment)

    def parseReturnStatement(self) -> Optional[ReturnStatement]:
        if not self.isType(TokenType.T_RETURN):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        expression = self.parseExpression()
        if expression is None:
            raise Exception(f"Expected expression, got {self.token}")
        return ReturnStatement(startPosition, expression)

    def parseWhileOperation(self) -> Optional[WhileOperation]:
        if self.isType(TokenType.T_BREAK):
            self.nextLexerToken()
            return Break()
        if self.isType(TokenType.T_CONTINUE):
            self.nextLexerToken()
            return Continue()
        return None

    def parseStatementForWhileLoop(self) -> Optional[StatementWithoutFunction | WhileOperation]:
        return self.parseStatementWithoutFunction() or self.parseWhileOperation()

    def parseWhileBlock(self) -> Optional[WhileBlock]:
        if not self.isType(TokenType.T_LBRACKET):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        statements: List[StatementWithoutFunction | WhileOperation] = []
        while not self.isType(TokenType.T_RBRACKET):
            statement = self.parseStatementForWhileLoop()
            if statement is None:
                raise Exception(f"Expected statement, got {self.token}")
            statements.append(statement)
        self.nextLexerToken()
        return WhileBlock(startPosition, statements)

    def parseWhileLoop(self) -> Optional[WhileLoop]:
        if not self.isType(TokenType.T_WHILE):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        condition = self.parseCondition()
        if condition is None:
            raise Exception(f"Expected condition, got {self.token}")
        block = self.parseWhileBlock()
        if block is None:
            raise Exception(f"Expected block, got {self.token}")
        return WhileLoop(startPosition, condition, block)

    # ForEachLoop = "foreach" Identifier "in" Identifier WhileBlock ;
    def parseForEachLoop(self) -> Optional[ForEachLoop]:
        if not self.isType(TokenType.T_FOREACH):
            return None
        startPosition = self.token.startPosition
        self.nextLexerToken()
        if not self.isType(TokenType.T_LPARENT):
            raise Exception(f"Expected '(', got {self.token}")
        self.nextLexerToken()
        if not self.isType(TokenType.VT_ID):
            raise Exception(f"Expected identifier, got {self.token}")
        identifier = self.token.getValue()
        self.nextLexerToken()
        if not self.isType(TokenType.T_IN):
            raise Exception(f"Expected 'in', got {self.token}")
        self.nextLexerToken()
        if not self.isType(TokenType.VT_ID):
            raise Exception(f"Expected identifier, got {self.token}")
        iterable = self.token.getValue()
        self.nextLexerToken()
        if not self.isType(TokenType.T_RPARENT):
            raise Exception(f"Expected ')', got {self.token}")
        self.nextLexerToken()
        block = self.parseWhileBlock()
        if block is None:
            raise Exception(f"Expected block, got {self.token}")
        return ForEachLoop(startPosition, identifier, iterable, block)

    def isType(self, *type: TokenType) -> bool:
        return self.token.type in type

    def isNextSameLine(self, position: Position) -> bool:
        return self.token.startPosition.line == position.line
