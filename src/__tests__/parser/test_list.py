from typing import List

from src.token_type import TokenType
from .utils import getObjects
from src.parser.nodes import (
    AdditiveExpression,
    Assignment,
    LemonList,
    LiteralIndentifier,
    LiteralInt,
    LiteralString,
)

from src.tokens import IdentifierValueToken, IntValueToken, Position, StringValueToken, Token


class TestList:
    def testListOfIntegers(self):
        # a = [1, 2, 3]
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            Token(TokenType.T_LSQBRACKET, Position(0, 4)),
            IntValueToken(Position(0, 5), 1, 1),
            Token(TokenType.T_COMMA, Position(0, 6)),
            IntValueToken(Position(0, 8), 1, 2),
            Token(TokenType.T_COMMA, Position(0, 9)),
            IntValueToken(Position(0, 11), 1, 3),
            Token(TokenType.T_RSQBRACKET, Position(0, 12)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a",
            LemonList(
                values=[
                    LiteralInt(Position(0, 5), 1),
                    LiteralInt(Position(0, 8), 2),
                    LiteralInt(Position(0, 11), 3),
                ]
            ),
        )

    def testListOfStrings(self):
        # a = ["hello", "world"]
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            Token(TokenType.T_LSQBRACKET, Position(0, 4)),
            StringValueToken(Position(0, 5), 5, "hello"),
            Token(TokenType.T_COMMA, Position(0, 12)),
            StringValueToken(Position(0, 14), 5, "world"),
            Token(TokenType.T_RSQBRACKET, Position(0, 21)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a",
            LemonList(
                values=[
                    LiteralString(Position(0, 5), "hello"),
                    LiteralString(Position(0, 14), "world"),
                ]
            ),
        )

    def testListOfIdentifiers(self):
        # a = [b, c]
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            Token(TokenType.T_LSQBRACKET, Position(0, 4)),
            IdentifierValueToken(Position(0, 5), 1, "b"),
            Token(TokenType.T_COMMA, Position(0, 6)),
            IdentifierValueToken(Position(0, 8), 1, "c"),
            Token(TokenType.T_RSQBRACKET, Position(0, 9)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a",
            LemonList(
                values=[
                    LiteralIndentifier(Position(0, 5), "b"),
                    LiteralIndentifier(Position(0, 8), "c"),
                ]
            ),
        )

    def testListOfExpressions(self):
        # a = [1 + 2, 3 + 4]
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            Token(TokenType.T_LSQBRACKET, Position(0, 4)),
            IntValueToken(Position(0, 5), 1, 1),
            Token(TokenType.T_PLUS, Position(0, 7)),
            IntValueToken(Position(0, 9), 1, 2),
            Token(TokenType.T_COMMA, Position(0, 10)),
            IntValueToken(Position(0, 12), 1, 3),
            Token(TokenType.T_PLUS, Position(0, 14)),
            IntValueToken(Position(0, 16), 1, 4),
            Token(TokenType.T_RSQBRACKET, Position(0, 17)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            "a",
            LemonList(
                values=[
                    AdditiveExpression(
                        left=LiteralInt(Position(0, 5), 1),
                        operator="+",
                        right=LiteralInt(Position(0, 9), 2),
                    ),
                    AdditiveExpression(
                        left=LiteralInt(Position(0, 12), 3),
                        operator="+",
                        right=LiteralInt(Position(0, 16), 4),
                    ),
                ]
            ),
        )
