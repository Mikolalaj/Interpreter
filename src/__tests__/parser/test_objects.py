from typing import List

from src.token_type import TokenType
from .utils import getObjects
from src.parser.nodes import AdditiveExpression, Assignment, FunctionCall, LiteralInt, ObjectMethodCall, ObjectProperty

from src.tokens import IdentifierValueToken, IntValueToken, Position, Token


class TestObjects:
    def testObjectMethodCall(self):
        # object.method(a=1)
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 6)),
            IdentifierValueToken(Position(0, 7), 1, "method"),
            Token(TokenType.T_LPARENT, Position(0, 13)),
            IdentifierValueToken(Position(0, 14), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 15)),
            IntValueToken(Position(0, 16), 1, 1),
            Token(TokenType.T_RPARENT, Position(0, 17)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == ObjectMethodCall(
            startPosition=Position(0, 0),
            identifier="object",
            functionCall=FunctionCall(
                startPosition=Position(0, 7),
                name="method",
                arguments=[
                    Assignment(
                        name="a",
                        value=LiteralInt(Position(0, 16), 1),
                    )
                ],
            ),
        )

    def testObjectMethodCallAssignment(self):
        # a = object.method(a=1)
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            IdentifierValueToken(Position(0, 4), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 10)),
            IdentifierValueToken(Position(0, 11), 1, "method"),
            Token(TokenType.T_LPARENT, Position(0, 17)),
            IdentifierValueToken(Position(0, 18), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 19)),
            IntValueToken(Position(0, 20), 1, 1),
            Token(TokenType.T_RPARENT, Position(0, 21)),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            name="a",
            value=ObjectMethodCall(
                startPosition=Position(0, 4),
                identifier="object",
                functionCall=FunctionCall(
                    startPosition=Position(0, 11),
                    name="method",
                    arguments=[
                        Assignment(
                            name="a",
                            value=LiteralInt(Position(0, 20), 1),
                        )
                    ],
                ),
            ),
        )

    def testObjectPropertyAssignment(self):
        # a = object.property
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "a"),
            Token(TokenType.T_ASSIGN, Position(0, 2)),
            IdentifierValueToken(Position(0, 4), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 10)),
            IdentifierValueToken(Position(0, 11), 1, "property"),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            name="a",
            value=ObjectProperty(
                startPosition=Position(0, 4),
                identifier="object",
                property="property",
            ),
        )

    def testObjectPropertyAssignment2(self):
        # object.property = otherObject.property
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 6)),
            IdentifierValueToken(Position(0, 7), 1, "property"),
            Token(TokenType.T_ASSIGN, Position(0, 15)),
            IdentifierValueToken(Position(0, 17), 1, "otherObject"),
            Token(TokenType.T_DOT, Position(0, 28)),
            IdentifierValueToken(Position(0, 29), 1, "property"),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            name=ObjectProperty(
                startPosition=Position(0, 0),
                identifier="object",
                property="property",
            ),
            value=ObjectProperty(
                startPosition=Position(0, 17),
                identifier="otherObject",
                property="property",
            ),
        )

    def testObjectPropertyAssignment3(self):
        # object.property = function() + 1
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 6)),
            IdentifierValueToken(Position(0, 7), 1, "property"),
            Token(TokenType.T_ASSIGN, Position(0, 15)),
            IdentifierValueToken(Position(0, 17), 1, "function"),
            Token(TokenType.T_LPARENT, Position(0, 25)),
            Token(TokenType.T_RPARENT, Position(0, 26)),
            Token(TokenType.T_PLUS, Position(0, 28)),
            IntValueToken(Position(0, 30), 1, 1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            name=ObjectProperty(
                startPosition=Position(0, 0),
                identifier="object",
                property="property",
            ),
            value=AdditiveExpression(
                left=FunctionCall(
                    startPosition=Position(0, 17),
                    name="function",
                    arguments=[],
                ),
                right=LiteralInt(Position(0, 30), 1),
                operator="+",
            ),
        )

    def testObjectPropertyAssignment4(self):
        # object.property = object.property + 1
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 6)),
            IdentifierValueToken(Position(0, 7), 1, "property"),
            Token(TokenType.T_ASSIGN, Position(0, 15)),
            IdentifierValueToken(Position(0, 17), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 23)),
            IdentifierValueToken(Position(0, 24), 1, "property"),
            Token(TokenType.T_PLUS, Position(0, 32)),
            IntValueToken(Position(0, 34), 1, 1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            name=ObjectProperty(
                startPosition=Position(0, 0),
                identifier="object",
                property="property",
            ),
            value=AdditiveExpression(
                left=ObjectProperty(
                    startPosition=Position(0, 17),
                    identifier="object",
                    property="property",
                ),
                right=LiteralInt(Position(0, 34), 1),
                operator="+",
            ),
        )

    def testObjectPropertyAssignment5(self):
        # object.property = object.method() + 1
        tokens: List[Token] = [
            IdentifierValueToken(Position(0, 0), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 6)),
            IdentifierValueToken(Position(0, 7), 1, "property"),
            Token(TokenType.T_ASSIGN, Position(0, 15)),
            IdentifierValueToken(Position(0, 17), 1, "object"),
            Token(TokenType.T_DOT, Position(0, 23)),
            IdentifierValueToken(Position(0, 24), 1, "method"),
            Token(TokenType.T_LPARENT, Position(0, 30)),
            Token(TokenType.T_RPARENT, Position(0, 31)),
            Token(TokenType.T_PLUS, Position(0, 33)),
            IntValueToken(Position(0, 35), 1, 1),
        ]
        objects = getObjects(tokens)

        assert len(objects) == 1
        assert objects[0] == Assignment(
            name=ObjectProperty(
                startPosition=Position(0, 0),
                identifier="object",
                property="property",
            ),
            value=AdditiveExpression(
                left=ObjectMethodCall(
                    startPosition=Position(0, 17),
                    identifier="object",
                    functionCall=FunctionCall(
                        startPosition=Position(0, 24),
                        name="method",
                        arguments=[],
                    ),
                ),
                right=LiteralInt(Position(0, 35), 1),
                operator="+",
            ),
        )
