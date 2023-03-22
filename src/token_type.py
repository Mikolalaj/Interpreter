from enum import Enum
import re


class TokenType(Enum):
    def hasValue(self):
        return True if self.name.startswith("V") else False

    def toString(self):
        return self.value

    """ TokenTypes with no value """

    T_IGNORE = 0
    # data types
    T_INT = "int"
    T_FLOAT = "float"
    T_BOOL = "bool"
    T_STRING = "string"

    # punctuation
    T_COMMA = ","
    # T_DOT = "."
    T_COLON = ":"
    T_SEMICOLON = ";"
    T_LSQBRACKET = "["
    T_RSQBRACKET = "]"
    T_LBRACKET = "{"
    T_RBRACKET = "}"
    T_LPARENT = "("
    T_RPARENT = ")"
    T_VERTICAL_BAR = "|"
    T_AMPERSAND = "&"

    # math operations
    T_PLUS = "+"
    T_MINUS = "-"
    T_MUL = "*"
    T_DIV = "/"

    # math order types
    T_LESS_OR_EQ = "<="
    T_LESS = "<"
    T_GREATER_OR_EQ = ">="
    T_GREATER = ">"
    T_EQ = "=="
    T_NOT_EQ = "!="

    # logical types
    T_OR = "or"
    T_AND = "and"
    T_NOT = "not"

    # other
    T_IF = "if"
    T_ELSE = "else"
    T_ELSEIF = "elseif"
    T_TRUE = "true"
    T_FALSE = "false"
    T_RETURN = "return"
    T_BREAK = "break"
    T_CONTINUE = "continue"
    T_WHILE = "while"
    T_ASSIGN = "="
    T_VOID = "void"
    T_FUNCTION = "function"
    T_EOT = "End Of Text"
    T_ARROW = "->"
    T_COMMENT = "~"

    """ TokenTypes that must have a value """

    # const values
    VT_INT = "const int"
    VT_FLOAT = "const float"
    VT_STRING = "const string"
    VT_BOOLEAN = "const bool"

    # variable names etc.
    VT_ID = "identifier"


def getCompiledRegexTokens():
    return {re.compile(regex): regexTokens[regex] for regex in regexTokens}


regexTokens = {
    r"\n": TokenType.T_IGNORE,
    r"[ \t]+": TokenType.T_IGNORE,
    r"float(?![\w\d])": TokenType.T_FLOAT,
    r"int(?![\w\d])": TokenType.T_INT,
    r"bool(?![\w\d])": TokenType.T_BOOL,
    r"string(?![\w\d])": TokenType.T_STRING,
    r"if(?![\w\d])": TokenType.T_IF,
    r"elseif(?![\w\d])": TokenType.T_ELSEIF,
    r"else(?![\w\d])": TokenType.T_ELSE,
    r"true(?![\w\d])": TokenType.T_TRUE,
    r"false(?![\w\d])": TokenType.T_FALSE,
    r"function(?![\w\d])": TokenType.T_FUNCTION,
    r"void(?![\w\d])": TokenType.T_VOID,
    r"return(?![\w\d])": TokenType.T_RETURN,
    r"break(?![\w\d])": TokenType.T_BREAK,
    r"continue(?![\w\d])": TokenType.T_CONTINUE,
    r"while(?![\w\d])": TokenType.T_WHILE,
    r"or(?![\w\d])": TokenType.T_OR,
    r"and(?![\w\d])": TokenType.T_AND,
    r"not(?![\w\d])": TokenType.T_NOT,
    r"\|": TokenType.T_VERTICAL_BAR,
    r"&": TokenType.T_AMPERSAND,
    r",": TokenType.T_COMMA,
    r"\{": TokenType.T_LBRACKET,
    r"\}": TokenType.T_RBRACKET,
    # r"\.": TokenType.T_DOT,
    r"==": TokenType.T_EQ,
    r"=": TokenType.T_ASSIGN,
    r"\(": TokenType.T_LPARENT,
    r"\)": TokenType.T_RPARENT,
    r";": TokenType.T_SEMICOLON,
    r"\:": TokenType.T_COLON,
    r"\+": TokenType.T_PLUS,
    r"-": TokenType.T_MINUS,
    r"\*": TokenType.T_MUL,
    r"/": TokenType.T_DIV,
    r"<=": TokenType.T_LESS_OR_EQ,
    r">=": TokenType.T_GREATER_OR_EQ,
    r"<": TokenType.T_LESS,
    r">": TokenType.T_GREATER,
    r"!=": TokenType.T_NOT_EQ,
    r"->": TokenType.T_ARROW,
    r"~": TokenType.T_COMMENT,
    r"DONE(?![\w\d])": TokenType.T_EOT,
    r"(0|[1-9]\d*)(?![\w])": TokenType.VT_INT,
    r"\d+\.\d+(?![\w])": TokenType.VT_FLOAT,
    r"\".*?\"(?![\w\d])": TokenType.VT_STRING,
    r"[a-zA-Z_][a-zA-Z0-9_]*": TokenType.VT_ID,
}
