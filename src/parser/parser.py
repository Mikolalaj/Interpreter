from typing import List, Optional
from src.lexer import Lexer
from src.parser.nodes import Parameter, FunctionDefinition
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
            node = self.parseFunctionDefinition()
            if node:
                objects.append(node)
            else:
                print(f"Unexpected token {self.token}")
                self.nextLexerToken()
        return objects

    def parseParameters(self) -> Optional[List[Parameter]]:
        parameters = []
        if self.token.type == TokenType.T_LPARENT:
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
        else:
            return None

    def parseFunctionDefinition(self) -> Optional[FunctionDefinition]:
        if self.token.type == TokenType.T_FUNCTION:
            self.nextLexerToken()
            if self.token.type == TokenType.VT_ID:
                name = self.token.getValue()
                self.nextLexerToken()
                parameters = self.parseParameters()
                if parameters is None:
                    raise Exception(f"Expected parameters, got {self.token}")
                if self.token.type == TokenType.T_LBRACKET:
                    self.nextLexerToken()
                    body = "body"
                    if self.token.type == TokenType.T_RBRACKET:
                        self.nextLexerToken()
                        return FunctionDefinition(name, parameters, body)
                    else:
                        raise Exception(f"Expected '}}', got {self.token}")
                else:
                    raise Exception(f"Expected '{{', got {self.token}")
            else:
                raise Exception(f"Expected function name, got {self.token}")
        return None
