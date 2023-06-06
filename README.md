# TKOM - Interpreter języka opisu brył

>Język do opisu brył i ich właściwości. Podstawowe bryły (prostopadłościan, ostrosłup, stożek, walec, kula itd.) są wbudowanymi typami języka. Każdy typ posiada wbudowane metody służące do wyznaczania charakterystycznych dla niego wielkości, np. pole podstawy, pole powierzchni bocznej, objętość, wysokość, średnica itp. Kolekcja brył tworzy scenę wyświetlaną na ekranie.

***Język dynamicznie i silne typowanie.***

Projekt realizowany w języku Python 3.11

## Sposób uruchomienia
Z pliku:
`python main.py <ścieżka do pliku>`

Oprócz pliku z kodem możliwe jest też podanie kodu w postaci stringa.

## Przykładowy kod
```swift
function add(a, b) {
    return a + b
}

let cube = Cuboid(width=2, height=3, length=4)

if (2 > 3) {
    cube.width = add(a=2, b=3)
}
else {
    cube.width = add(a=3, b=4)
}

let cylinder = Cylinder(radius=2, height=3)

let volume = cube.getVolume() + cylinder.getVolume()
let volumeString = string(value=volume)
print(out="Volume: " + volumeString)

let objects = [cube, cylinder]

foreach (object in objects) {
    object.display()
}

let string = "2"
let number = int(value=string) + 3
print(out=number)
```

Powyższy kod wyświetli na ekranie:
```
Volume: 121.69911184307752
Cuboid: width=7 length=4 height=3
Cylinder: radius=2 height=3
5
```

## Przykładowe wyrażenia

#### Podstawowe

Deklaracja zmiennej

```typescript
let a = 5 # integer
let b = 3.14 # float
let c = "Hello world!" # string
let d = true # boolean
let f = [1, 2, 3, 4, 5] # list
```

Deklaracja funkcji

```typescript
function add(a, b) {
    return a + b
}
```

Instrukcja warunkowa

```typescript
if (a > 0) {
    print("a is positive")
} elif (a < 0) {
    print("a is negative")
} else {
    print("a is zero")
}
```

Pętla

```typescript
while (a > 0) {
    print(a)
    a = a - 1
}
```

```typescript
a = -10
while (true) {
    if (a > 0) {
        break
    }
    if (a < -5) {
        continue
    }
    print('close to zero')
}
```

```typescript
let list = [1, 2, 3, 4, 5]
foreach (number in list) {
    print(number)
}
```

Komentarze

```typescript
# single line comment
let a = 4 # comment after statement
```

Stałe - są zamieniane przez lexer na wartości liczbowe (float)

```typescript
let a = PI
Cone b = (radius=3*PI, height=2)
```

#### Bryły geometryczne

Deklaracje

```
let a = Cuboid(width=4, length=2, height=5)
let b = Tetrahedron(edge=3)
```

Metody

```
a.getBaseArea()
a.getSurfaceArea()
a.getVolume()
```

## Tokeny lexera

 - T_VARIABLE = "let"

Bryły geometryczne:
 - T_CUBOID = "Cuboid"
 - T_PYRAMID = "Pyramid"
 - T_CONE = "Cone"
 - T_CYLINDER = "Cylinder"
 - T_SPHERE = "Sphere"
 - T_TETRAHEDRON = "Tetrahedron"

Punktuacja:
 - T_COMMA = ","
 - T_DOT = "."
 - T_LSQBRACKET = "["
 - T_RSQBRACKET = "]"
 - T_LBRACKET = "{"
 - T_RBRACKET = "}"
 - T_LPARENT = "("
 - T_RPARENT = ")"

Operatory arytmetyczne:
 - T_PLUS = "+"
 - T_MINUS = "-"
 - T_MUL = "*"
 - T_DIV = "/"

Operatory logiczne:
 - T_LESS = "<"
 - T_LESS_OR_EQ = "<="
 - T_GREATER = ">"
 - T_GREATER_OR_EQ = ">="
 - T_EQ = "=="
 - T_NOT_EQ = "!="
 - T_OR = "or"
 - T_AND = "and"
 - T_NOT = "not"

Słowa kluczowe:
 - T_IF = "if"
 - T_ELSE = "else"
 - T_ELSEIF = "elif"
 - T_TRUE = "true"
 - T_FALSE = "false"
 - T_RETURN = "return"
 - T_BREAK = "break"
 - T_CONTINUE = "continue"
 - T_WHILE = "while"
 - T_FOREACH = "foreach"
 - T_IN = "in"
 - T_ASSIGN = "="
 - T_FUNCTION = "function"

Typy danych i stałe:
 - VT_INT = "value int"
 - VT_FLOAT = "value float"
 - VT_STRING = "value string"
 - VT_BOOLEAN = "value bool"
 - VT_PI = "PI"

Nazwy zmiennych, funkcji:
 - VT_ID = "identifier"


## Wbudowane funkcje

```typescript
print(out=value) # wypisuje wartość na ekran
```

Castowanie typów
```typescript
let a = int(value="5")
a = a + 1
```

## Wbudowane typy

```typescript
Cuboid(width, length, height)
Pyramid(width, length, height)
Cone(radius, height)
Cylinder(radius, height)
Tetrahedron(edge)
```

Wszystkie typy mają metody:
```typescript
getSurfaceArea()
getVolume()
display() - wyświetla bryłę na ekranie
```

Wszystkie typy oprócz Cuboid mają metodę:
```typescript
getBaseArea()
```
Wszystkie typt mają pola takie same jak argumenty konstruktora

## Zmienne
Zmienne są mutowalne, można je nadpisywać. Zmienne muszą być zadeklarowane zanim zostaną użyte.
Zasięg zmiennych jest lokalny, nie można się odwoływać do zmiennych z innych funkcji lub bloków.
Zmienne mogą być typu `int`, `float`, `string`, `boolean`, `list` lub `object`.
Lista może przechowywać wartości typu `int`, `float`, `string`, `boolean` lub `object`.


## Funkcje i metody obiektów
Funkcje i metody obiektów nie są mutowalne, więc nie można ich nadpisywać. Funkcje i metody obiektów muszą być zadeklarowane zanim zostaną użyte.
Argumenty podawane przy wywołaniu funkcji lub metody obiektu mogą być podane w dowolnej kolejności ale muszą być nazwane.
Argumenty przekazywane są do funkcji przez wartość.
Funkcja może zwracać tylko jedną wartość, która może być typu `int`, `float`, `string`, `boolean`, `list` lub `object`.
Podczas wywoływanie funkcji nie można zagnieżdżać wywołań funkcji, np. `a = add(1, add(2, 3))` jest niepoprawne.
Nie jest też możliwe wywoływanie funkcji na innej funkcji, np. `a = firstFunction(1, 2).otherFunction(3)` jest niepoprawne.


## Konwersja typów
Konwersja typów jest możliwa tylko w przypadku konwersji typu `int` na `float`. W tym przypadku konwersja jest automatyczna, niejawna.


## Gramatyka

```ebnf
Program                     = Statement* ;

Statement                   = FunctionDefinition
                            | StatementWithoutFunction ;

StatementWithoutFunction    = VariableDeclaration
                            | VariableAssignment
                            | WhileLoop
                            | Expression
                            | ObjectDeclaration
                            | ObjectMethodCall
                            | Comment
                            | IfStatement
                            | ForEachLoop
                            | ReturnStatement ;

Identifier                  = LetterOrUnderscore (LetterOrUnderscore | Digit)* ;

Value                       = Boolean | Number | String | List ;

Boolean                     = "true" | "false" ;

Integer                     = DigitWithoutZero Digit* ;

Float                       = "0" "." Digit+
                            | DigitWithoutZero Digit* "." Digit+ ;

Number                      = Integer | Float ;

String                      = "\"" AnyCharacters "\"" ;

List                        = LeftBracket ListValue (Comma ListValue)* RightBracket ;

ListValue                   = Number | String | Boolean | Identifier ;

ListIndex                   = LeftBracket Integer RightBracket ;

ListGetValue                = List ListIndex ;

VariableAssignment          = Identifier AssignSymbol (Value | FunctionCall | ObjectMethodCall | ObjectProperty | ListGetValue | Identifier | Expression) ;

VariableDeclaration         = "let" VariableAssignment ;

Block                       = LeftBrace Statement* RightBrace

WhileBlock                  = LeftBrace (Statement | WhileLoopOperations)* RightBrace

WhileLoopOperations         = Break | Continue ;

Condition                   = LeftParenthesis Expression RightParenthesis ;

(* Function *)

BlockWithoutFunction        = LeftBrace StatementWithoutFunction* RightBrace ;

FunctionDefinition          = "function" Identifier LeftParenthesis Parameters RightParenthesis BlockWithoutFunction ;

Parameters                  = (Identifier (Comma Identifier)*)? ;

FunctionCall                = Identifier Arguments ;

Arguments                   = LeftParenthesis (Argument (Comma Argument)*)? RightParenthesis ;

Argument                    = Identifier AssignSymbol Value ;

ReturnStatement             = "return" Expression ;

(* If *)

IfStatement                 = "if" Condition BlockWithoutFunction ( "elif" Condition BlockWithoutFunction )* ( "else" BlockWithoutFunction )? ;

(* Loops *)

WhileLoop                   = "while" Condition WhileBlock ;

ForEachLoop                 = "foreach" Identifier "in" Identifier WhileBlock ;

(* Operators *)

Expression                  = LogicalOrExpression ;

LogicalOrExpression         = LogicalAndExpression ( OrOperator LogicalAndExpression )* ;

LogicalAndExpression        = ComparisonExpression ( AndOperator ComparisonExpression )* ;

ComparisonExpression        = AdditiveExpression ( ( "<" | ">" | "<=" | ">=" | "==" | "!=" ) AdditiveExpression )? ;

AdditiveExpression          = MultiplicativeExpression ( ( "+" | "-" ) MultiplicativeExpression )* ;

MultiplicativeExpression    = PrimaryExpression ( ( "*" | "/" ) PrimaryExpression )* ;

PrimaryExpression           = NotOperator? Literal | ( LeftParenthesis Expression RightParenthesis ) ;

Literal                     = Identifier
                            | Boolean
                            | Number 
                            | Identifier LeftBracket Expression RightBracket ;

(* Object *)

ObjectDeclaration           = "let" Identifier AssignSymbol ObjectConstructor ;

ObjectConstructor           = ObjectType LeftParenthesis Arguments RightParenthesis ;

ObjectType                  = "Cuboid" | "Pyramid" | "Cone" | "Cylinder" | "Sphere" | "Tetrahedron" ;

ObjectMethodCall            = Identifier "." FunctionCall ;

ObjectProperty              = Identifier "." Identifier ;

ObjectPropertyAssignment    = ObjectProperty AssignSymbol Value ;

Comment                     = "#" AnyCharacters ;

Letter                      = #"[a-z]" | #"[A-Z]" ;

LetterOrUnderscore          = Letter | "_" ;

Digit                       = "0" | DigitWithoutZero ;

DigitWithoutZero            = #"[1-9]" ;

(* Logical operators *)

OrOperator                  = "or" ;

AndOperator                 = "and" ;

NotOperator                 = "not" | "-" ;

(* Symbols *)

AssignSymbol                = "=" ;

LeftParenthesis             = "(" ;

RightParenthesis            = ")" ;

LeftBracket                 = "[" ;

RightBracket                = "]" ;

LeftBrace                   = "{" ;

RightBrace                  = "}" ;

Comma                       = "," ;

Break                       = "break" ;

Continue                    = "continue" ;

Whitespace                  = (" " | "\t" | "\r")* ;

AnyCharacters               = #".*" ;
```


## Testowanie

W zdecydowanie większości będą to testy jednostkowe wykonywane za pomocą biblioteki [unittest](https://docs.python.org/3/library/unittest.html). Testowane będą zarówno przypadki poprawne jak i te które powinny zwracać błędy. Przykład testu jednostkowego lexera:

```python
def testIdentifier(capfd):
    code = """
jp2
 2asd
3qq=
d3
"""

    lexer = Lexer(source=StringSource(code[1:-1]))

    out, _ = capfd.readouterr()
    assert out == """LexerError: Invalid character in number at [Line 2, Column 2]
LexerError: Invalid character in number at [Line 3, Column 1]
"""
    print(lexer.allTokens)
    assert len(lexer.allTokens) == 3

    assert lexer.allTokens[0] == IdentifierValueToken(startPosition=Position(line=1, column=1), length=3, value="jp2")
    assert lexer.allTokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=3, column=4), length=1)
    assert lexer.allTokens[3] == IdentifierValueToken(startPosition=Position(line=4, column=1), length=2, value="d3")
```

Kolejny przykład testu jednostkowego parsera:

```python
def testForeach(self):
        code = """
            let arr = [1, 2, 3]
            foreach(i in arr) {
                print(i)
            }
        """

        tokens = getTokens(code)
        assert len(tokens) == 22

        assert tokens[0] == Token(type=TokenType.T_VARIABLE, startPosition=Position(line=1, column=1))
        assert tokens[1] == IdentifierValueToken(value="arr", length=3, startPosition=Position(line=1, column=5))
        assert tokens[2] == Token(type=TokenType.T_ASSIGN, startPosition=Position(line=1, column=9))
        assert tokens[3] == Token(type=TokenType.T_LSQBRACKET, startPosition=Position(line=1, column=11))
        assert tokens[4] == IntValueToken(value=1, length=1, startPosition=Position(line=1, column=12))
        assert tokens[5] == Token(type=TokenType.T_COMMA, startPosition=Position(line=1, column=13))
        assert tokens[6] == IntValueToken(value=2, length=1, startPosition=Position(line=1, column=15))
        assert tokens[7] == Token(type=TokenType.T_COMMA, startPosition=Position(line=1, column=16))
        assert tokens[8] == IntValueToken(value=3, length=1, startPosition=Position(line=1, column=18))
        assert tokens[9] == Token(type=TokenType.T_RSQBRACKET, startPosition=Position(line=1, column=19))
        assert tokens[10] == Token(type=TokenType.T_FOREACH, startPosition=Position(line=2, column=1))
        assert tokens[11] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=2, column=8))
        assert tokens[12] == IdentifierValueToken(value="i", length=1, startPosition=Position(line=2, column=9))
        assert tokens[13] == Token(type=TokenType.T_IN, startPosition=Position(line=2, column=11))
        assert tokens[14] == IdentifierValueToken(value="arr", length=3, startPosition=Position(line=2, column=14))
        assert tokens[15] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=2, column=17))
        assert tokens[16] == Token(type=TokenType.T_LBRACKET, startPosition=Position(line=2, column=19))
        assert tokens[17] == IdentifierValueToken(value="print", length=5, startPosition=Position(line=3, column=5))
        assert tokens[18] == Token(type=TokenType.T_LPARENT, startPosition=Position(line=3, column=10))
        assert tokens[19] == IdentifierValueToken(value="i", length=1, startPosition=Position(line=3, column=11))
        assert tokens[20] == Token(type=TokenType.T_RPARENT, startPosition=Position(line=3, column=12))
        assert tokens[21] == Token(type=TokenType.T_RBRACKET, startPosition=Position(line=4, column=1))
```

Przykładowy test jednostkowy interpretera:
    
```python
def testWhileBreak(self, capfd):
"""
let a = 1
while (a < 5) {
    a = a + 1
    if (a == 3) {
        break
    }
}
"""
interpreter = getInterpreter(
    [
        VariableDeclaration(POSITION, Assignment(POSITION, "a", LiteralInt(POSITION, 1))),
        WhileLoop(
            POSITION,
            ComparisonExpression(
                LiteralIdentifier(POSITION, "a"),
                LiteralInt(POSITION, 5),
                "<",
            ),
            WhileBlock(
                POSITION,
                [
                    Assignment(
                        POSITION,
                        "a",
                        AdditiveExpression(
                            LiteralIdentifier(POSITION, "a"),
                            LiteralInt(POSITION, 1),
                            "+",
                        ),
                    ),
                    IfStatement(
                        POSITION,
                        ConditionWithBlock(
                            ComparisonExpression(
                                LiteralIdentifier(POSITION, "a"),
                                LiteralInt(POSITION, 3),
                                "==",
                            ),
                            BlockWithoutFunciton(POSITION, [Break()]),
                        ),
                        None,
                        None,
                    ),
                ],
            ),
        ),
    ]
)

assert interpreter.context == {"a": (3, POSITION)}
assertNoOutput(capfd)
```

Oprócz testów jednostkowych używam też mypy do sprawdzania poprawności typów. Aby sprawdzić poprawność typów, należy wykonać polecenie:

```bash
mypy ./src/lexer.py
```

Pokrycie testami jednostkowymi można sprawdzić za pomocą:

```bash
python -m pytest .\src\__tests__\ --cov=.\src\
```


## Błędy

Program będzie obsługiwał następujące błędy z każdego modułu, tj. analizatora leksykalnego, składniowego i interpretera. Jeśli wystąpi błąd, to program nie będzie przerywał swojej pracy, tylko będzie próbował kontynuować. W przypadku wystąpienia błędu, program powinien wyświetlić informację o błędzie na standardowe wyjście.
Przykładowy błąd:

```LexerError: Invalid character in number at [Line 2, Column 2]```
```SyntaxError: Unterminated string literal at [Line 2, Column 2]```
```InterpreterError: Variable 'a' is not defined at [Line 2, Column 2]```
