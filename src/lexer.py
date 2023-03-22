from typing import List, Optional

from .errors import LexerError
from .source import Source
from .tokens import StringValueToken, Token, FloatValueToken, IntValueToken, IdentifierValueToken
from .token_type import TokenType, getCompiledRegexTokens


MAX_NUMBER = 2**31 - 1
MAX_STRING_LENGTH = 2**31 - 1


class Lexer:
    def __init__(self, source: Source):
        self.source = source
        self.regexTokens = getCompiledRegexTokens()
        self.tokenIterator = 0
        self.currentCharacter: str = self.source.readNextCharacter()
        self.allTokens = self._getAllTokens()

    def getNextToken(self, move_index=True):
        if self.tokenIterator < len(self.allTokens):
            token = self.allTokens[self.tokenIterator]
            if move_index:
                self.tokenIterator += 1
            return token
        return None

    def doesNextTokenExists(self):
        return True if self.tokenIterator < len(self.allTokens) else False

    def _getAllTokens(self) -> List[Token]:
        allTokens = []
        while not self.source.isEndOfSource():
            token = self._getNextToken()
            if token is not None:
                allTokens.append(token)
        return allTokens

    def _getNextToken(self) -> Optional[Token]:
        self._skipWhitespace()
        try:
            token = self._tryBuildString() or self._tryBuildNumber() or self._tryBuildIdentifierOrKeyword()
        except LexerError as e:
            print(e)
            return None
        if token is not None:
            return token

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
                if not self._isWhitespace() and not self._isNewLine() and startsWithZero and self.currentCharacter != ".":
                    self._skipToFirstWhitespace()
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
                else:
                    self._skipToFirstWhitespace()
                    raise LexerError("Invalid character in number", startPosition)

            length = integerLength + fractionalLength + int(isDecimal)
            if isDecimal:
                number += decimalPart / 10**fractionalLength
                return FloatValueToken(startPosition, length, number)
            else:
                return IntValueToken(startPosition, length, number)

    def _tryBuildIdentifierOrKeyword(self) -> Optional[Token]:
        startPosition = self.source.position.copy()
        print(f"LEXER - char: {self.currentCharacter}, pos: {startPosition}")
        isValidIdentifier = True

        identifierString = self.currentCharacter
        isValidIdentifier = self._isValidIdentifier(isFirstCharacter=True)

        self._nextCharacter()

        tokenType = self._getTokenType(identifierString)
        if tokenType is not None:
            return Token(tokenType, startPosition, 1)

        while not self.source.isEndOfSource() and not self._isWhitespace() and not self._isNewLine():
            isValidIdentifier = isValidIdentifier and self._isValidIdentifier(isFirstCharacter=False)
            identifierString += self.currentCharacter
            self._nextCharacter()

            tokenType = self._getTokenType(identifierString)
            if tokenType is not None:
                return Token(tokenType, startPosition, len(identifierString))

        if isValidIdentifier:
            return IdentifierValueToken(startPosition, len(identifierString), identifierString)
        else:
            raise LexerError(f"Invalid identifier ({identifierString})", self.source.position)

    def _tryBuildString(self) -> Optional[StringValueToken]:
        startPosition = self.source.position.copy()
        string = ""

        if self.currentCharacter != '"':
            return None

        self._nextCharacter()

        while not self.source.isEndOfSource() and self.currentCharacter != '"':
            string += self.currentCharacter
            self._nextCharacter()

        self._nextCharacter()

        if len(string) > MAX_STRING_LENGTH:
            raise LexerError("String is too long", self.source.position)

        return StringValueToken(startPosition, len(string), string)

    def _isValidIdentifier(self, isFirstCharacter: bool) -> bool:
        if isFirstCharacter:
            return self._isLetter() or self.currentCharacter == "_"
        else:
            return self._isLetter() or self._idDigit() or self.currentCharacter == "_" or self.currentCharacter == "-"

    def _getTokenType(self, value: str) -> Optional[TokenType]:
        for tokenType in TokenType:
            if tokenType.value == value:
                return tokenType

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
        while not self.source.isEndOfSource():
            if not self._isNewLine() and not self._isWhitespace():
                break
            self.currentCharacter = self.source.readNextCharacter()

    def _skipToFirstWhitespace(self) -> None:
        while not self.source.isEndOfSource():
            if self._isNewLine() or self._isWhitespace():
                break
            self._nextCharacter()

    def _nextCharacter(self) -> None:
        self.currentCharacter = self.source.readNextCharacter()
