import math
from typing import Callable, List, Optional

from .errors import LexerError
from .source import Source
from .tokens import BooleanValueToken, StringValueToken, Token, FloatValueToken, IntValueToken, IdentifierValueToken
from .token_type import TokenType


MAX_NUMBER = 2**31 - 1
MAX_STRING_LENGTH = 2**31 - 1


class Lexer:
    def __init__(self, source: Source):
        self.source = source
        self.tokenIterator = 0
        self.currentCharacter: str = self.source.readNextCharacter()
        self.allTokens = self._getAllTokens()

    def _getAllTokens(self) -> List[Token]:
        allTokens = []
        while not self.source.isEndOfSource():
            token = self._getNextToken()
            if token is not None:
                allTokens.append(token)
        return allTokens

    def _getNextToken(self) -> Optional[Token]:
        self._skipWhitespace()
        if self.currentCharacter == '#':
            self._skipLine()
        try:
            token = self._tryBuildString() or self._tryBuildNumber() or self._tryBuildIdentifierOrKeyword()
        except LexerError as e:
            print(e)
            return None
        if token is not None:
            return token
        return None

    def _tryBuildNumber(self) -> Optional[FloatValueToken | IntValueToken]:
        startPosition = self.source.getPosition()
        isDecimal = False
        decimalPart = 0

        integerLength = 1
        fractionalLength = 0

        if self.currentCharacter.isdigit():
            number = ord(self.currentCharacter) - ord("0")
            startsWithZero = True if number == 0 else False
            while True:
                self._nextCharacter()
                if self.currentCharacter.isdigit() and startsWithZero:
                    self._skipNumbers()
                    raise LexerError("Integer number can't start with zero", startPosition)
                else:
                    startsWithZero = False

                if self.currentCharacter.isdigit():
                    if not isDecimal:
                        number = number * 10 + ord(self.currentCharacter) - ord("0")
                        integerLength += 1
                    else:
                        decimalPart = decimalPart * 10 + ord(self.currentCharacter) - ord("0")
                        fractionalLength += 1

                    if number > MAX_NUMBER:
                        raise LexerError("Number is too big", startPosition)
                elif self.currentCharacter == ".":
                    if isDecimal:
                        raise LexerError("Number can't have more than one decimal point", startPosition)
                    isDecimal = True
                elif self._isWhitespace() or self._isNewLine():
                    break
                elif self._isLetter():
                    invalidCharacter = self.currentCharacter
                    self._skipIdentifierCharacters()
                    raise LexerError(f"Invalid character `{invalidCharacter}` in number", startPosition)
                else:
                    break

            length = integerLength + fractionalLength + int(isDecimal)
            if isDecimal:
                number += decimalPart / 10**fractionalLength
                return FloatValueToken(startPosition, length, number)
            else:
                return IntValueToken(startPosition, length, number)
        return None

    def _tryBuildIdentifierOrKeyword(self) -> Optional[Token]:
        startPosition = self.source.getPosition()

        identifierString = self.currentCharacter
        isFirstValidIdentifier = isValidIdentifier = self._isValidIdentifier(isFirstCharacter=True)
        self._nextCharacter()

        tokenType = self._getTokenType(identifierString)
        if tokenType is not None:
            if self.currentCharacter == "=":
                self._nextCharacter()
                if tokenType == TokenType.T_LESS:
                    return Token(TokenType.T_LESS_OR_EQ, startPosition)
                elif tokenType == TokenType.T_GREATER:
                    return Token(TokenType.T_GREATER_OR_EQ, startPosition)
                elif tokenType == TokenType.T_ASSIGN:
                    return Token(TokenType.T_EQ, startPosition)
            return Token(tokenType, startPosition)

        while not self.source.isEndOfSource() and not self._isWhitespace() and not self._isNewLine():
            isValidIdentifier = isValidIdentifier and self._isValidIdentifier(isFirstCharacter=False)
            if not isValidIdentifier and isFirstValidIdentifier:
                return IdentifierValueToken(startPosition, len(identifierString), identifierString)
                # TODO:  count length of identifier in the loop
            identifierString += self.currentCharacter
            self._nextCharacter()

            tokenType = self._getTokenType(identifierString)
            if tokenType is not None:
                if tokenType == TokenType.VT_PI:
                    return FloatValueToken(startPosition, 2, math.pi)
                elif tokenType == TokenType.T_TRUE:
                    return BooleanValueToken(startPosition, True)
                elif tokenType == TokenType.T_FALSE:
                    return BooleanValueToken(startPosition, False)

                if not self._isLetter() and not self.currentCharacter == "_":
                    return Token(tokenType, startPosition)

        if isValidIdentifier:
            return IdentifierValueToken(startPosition, len(identifierString), identifierString)
        else:
            raise LexerError(f"Invalid identifier ({identifierString})", startPosition)

    def _tryBuildString(self) -> Optional[StringValueToken]:
        startPosition = self.source.position.copy()
        string = ""
        length = 2

        if self.currentCharacter != '"':
            return None

        self._nextCharacter()

        while not self.source.isEndOfSource() and self.currentCharacter != '"':
            string += self.currentCharacter
            length += 1
            self._nextCharacter()

        self._nextCharacter()

        if len(string) > MAX_STRING_LENGTH:
            raise LexerError("String is too long", self.source.position)
        print(string)
        return StringValueToken(startPosition, length, string)

    def _isValidIdentifier(self, isFirstCharacter: bool) -> bool:
        if isFirstCharacter:
            return self._isLetter() or self.currentCharacter == "_"
        else:
            return self._isLetter() or self._idDigit() or self.currentCharacter == "_"

    def _getTokenType(self, value: str) -> Optional[TokenType]:
        for tokenType in TokenType:
            if tokenType.value == value:
                return tokenType
        return None

    def _isLowerCase(self) -> bool:
        return ord(self.currentCharacter) >= ord("a") and ord(self.currentCharacter) <= ord("z")

    def _isUpperCase(self) -> bool:
        return ord(self.currentCharacter) >= ord("A") and ord(self.currentCharacter) <= ord("Z")

    def _isLetter(self) -> bool:
        return self._isLowerCase() or self._isUpperCase()

    def _idDigit(self) -> bool:
        return self.currentCharacter.isdigit()

    def _isWhitespace(self) -> bool:
        return self.currentCharacter in [" ", "\t", "\r"]

    def _isNewLine(self) -> bool:
        return self.currentCharacter == "\n"

    def _skipWhitespace(self) -> None:
        self._skip(lambda: self._isWhitespace() or self._isNewLine())

    def _skipIdentifierCharacters(self) -> None:
        self._skip(lambda: self._isLetter() or self._idDigit() or self.currentCharacter == "_")

    def _skipNumbers(self) -> None:
        self._skip(lambda: self.currentCharacter.isdigit() or self.currentCharacter == ".")

    def _skipLine(self) -> None:
        self._skip(lambda: not self._isNewLine())

    def _skip(self, condition: Callable[[], bool]) -> None:
        while not self.source.isEndOfSource():
            if condition():
                self._nextCharacter()
            else:
                break

    def _nextCharacter(self) -> None:
        self.currentCharacter = self.source.readNextCharacter()
