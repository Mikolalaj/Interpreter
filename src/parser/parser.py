from typing import List, Optional
from src.lexer import Lexer
from src.parser.nodes import Assignment, FunctionCall, Parameter, FunctionDefinition
from src.token_type import TokenType
from src.tokens import Token


class Parser:
    def __init__(self, lexer: Lexer, tokens: Optional[List[Token]] = None) -> None:
        self.lexer = lexer
        self.token = tokens[0] if tokens else lexer.getNextToken()
        self.tokens = tokens

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
            node = (
                self.parseFunctionDefinition()
                or self.parseStartingWithIdentifier()
                # or self.parseAssignment()
                or self.parseArguments()
            )
            if node is not None:
                objects.append(node)
            else:
                print(f"Unexpected token {self.token}")
                self.nextLexerToken()
        return objects

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
        if self.token.type != TokenType.T_LBRACKET:
            raise Exception(f"Expected '{{', got {self.token}")
        self.nextLexerToken()
        body = "body"
        if self.token.type != TokenType.T_RBRACKET:
            raise Exception(f"Expected '}}', got {self.token}")
        self.nextLexerToken()
        return FunctionDefinition(name, parameters, body)

    def parseAssignment(self, name: Optional[str] = None) -> Optional[Assignment]:
        if not name:
            if self.token.type != TokenType.VT_ID:
                return None
            name = self.token.getValue()
            self.nextLexerToken()

        if self.token.type != TokenType.T_ASSIGN:
            raise Exception(f"Expected '=', got {self.token}")
        self.nextLexerToken()
        if (
            self.token.type != TokenType.VT_ID
            and self.token.type != TokenType.VT_INT
            and self.token.type != TokenType.VT_FLOAT
            and self.token.type != TokenType.VT_STRING
            and self.token.type != TokenType.VT_BOOLEAN
        ):  # TODO: Tutaj powinien być też Array i Object
            raise Exception(f"Expected variable name, got {self.token}")
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

    def parseStartingWithIdentifier(self) -> Optional[FunctionCall | Assignment]:
        if self.token.type != TokenType.VT_ID:
            return None
        name = self.token.getValue()
        self.nextLexerToken()
        arguments = self.parseArguments()
        if arguments is not None:
            return FunctionCall(name, arguments)
        assignment = self.parseAssignment(name)
        if assignment is not None:
            return assignment
