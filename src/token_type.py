from enum import Enum


class TokenType(Enum):
    def hasValue(self):
        return True if self.name.startswith("V") else False

    def toString(self):
        return self.value

    """ TokenTypes with no value """

    T_IGNORE = 0
    # data types
    T_VARIABLE = "let"

    # geometric solids objects
    T_CUBOID = "Cuboid"
    T_PYRAMID = "Pyramid"
    T_CONE = "Cone"
    T_CYLINDER = "Cylinder"
    T_SPHERE = "Sphere"
    T_TATRAHEDRON = 'Tetrahedron'

    # punctuation
    T_COMMA = ","
    T_DOT = "."
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
