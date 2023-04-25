from enum import Enum, auto


class TokenType(Enum):
    def hasValue(self):
        return True if self.name.startswith("V") else False

    def toString(self):
        return self.value

    """ TokenTypes with no value """

    # data types
    T_VARIABLE = "let"

    # geometric solids objects
    T_CUBOID = "Cuboid"
    T_PYRAMID = "Pyramid"
    T_CONE = "Cone"
    T_CYLINDER = "Cylinder"
    T_SPHERE = "Sphere"
    T_TETRAHEDRON = "Tetrahedron"

    # punctuation
    T_COMMA = ","
    T_DOT = "."
    T_LSQBRACKET = "["
    T_RSQBRACKET = "]"
    T_LBRACKET = "{"
    T_RBRACKET = "}"
    T_LPARENT = "("
    T_RPARENT = ")"

    # math operations
    T_PLUS = "+"
    T_MINUS = "-"
    T_MUL = "*"
    T_DIV = "/"

    # math order types
    T_LESS = "<"
    T_LESS_OR_EQ = "<="
    T_GREATER = ">"
    T_GREATER_OR_EQ = ">="
    T_EQ = "=="
    T_NOT_EQ = "!="

    # logical types
    T_OR = "or"
    T_AND = "and"
    T_NOT = "not"

    # other
    T_IF = "if"
    T_ELSE = "else"
    T_ELSEIF = "elif"
    T_TRUE = "true"
    T_FALSE = "false"
    T_RETURN = "return"
    T_BREAK = "break"
    T_CONTINUE = "continue"
    T_WHILE = "while"
    T_FOREACH = "foreach"
    T_IN = "in"
    T_ASSIGN = "="
    T_FUNCTION = "function"

    """ TokenTypes that must have a value """

    # values
    VT_INT = "value int"
    VT_FLOAT = "value float"
    VT_STRING = "value string"
    VT_BOOLEAN = "value bool"

    # constants
    VT_PI = "PI"

    # variable names etc.
    VT_ID = auto()
