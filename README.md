# TKOM - Interpreter języka opisu brył

## Treść zadania

>Język do opisu brył i ich właściwości. Podstawowe bryły (prostopadłościan, ostrosłup, stożek, walec, kula itd.) są wbudowanymi typami języka. Każdy typ posiada wbudowane metody służące do wyznaczania charakterystycznych dla niego wielkości, np. pole podstawy, pole powierzchni bocznej, objętość, wysokość, średnica itp. Kolekcja brył tworzy scenę wyświetlaną na ekranie.

***Język dynamicznie i silne typowanie.***

Program obsługuje dwa rodzaje źródeł danych wejściowych: pliki tekstowe i ciąg znaków.

## Gramatyka

```ebnf
Program                     = Statement* ;

Statement                   = 
                            | VariableDeclaration
                            | FunctionDefinition
                            | IfStatement
                            | WhileLoop
                            | Expression
                            | ObjectDeclaration
                            | ObjectMethodCall
                            | Comment ;

Identifier                  = Letter (Letter | Digit)* ;

Value                       = Boolean | Integer | Float | String | List ;

Boolean                     = "true" | "false" ;

Integer                     = DigitWithoutZero Digit* ;

Float                       =
                            | "0" "." Digit+
                            | DigitWithoutZero Digit* "." Digit+ ;

String                      = "\"" character* "\"" ;

List                        = "[" value ("," value)* "]" ;

VariableDeclaration         = "let" Identifier "=" Value ;

Block                       = "{" Statement* "}"

Condition                   = "(" Expression ")" ;

FunctionDefinition          = "function" Identifier "(" Parameters ")" Block ;

Parameters                  = (Identifier ("," Identifier)*)? ;

FunctionCall                = Identifier Arguments ;

Arguments                   = "(" (ObjectArgument ("," ObjectArgument)*)? ")" ;

Argument                    = Identifier "=" Value ;

IfStatement                 = "if" Condition Block ( "elif" Condition Block )* ( "else" Block )? ;

WhileLoop                   = "while" Condition Block ;

Expression                  = AdditiveExpression ;

ComparisonExpression        = AdditiveExpression ( ( "<" | ">" | "<=" | ">=" | "==" | "!=" ) AdditiveExpression )? ;

AdditiveExpression          = MultiplicativeExpression ( ( "+" | "-" ) MultiplicativeExpression )* ;

MultiplicativeExpression    = PrimaryExpression ( ( "*" | "/" ) PrimaryExpression )* ;

PrimaryExpression           = 
                            | Identifier 
                            | Value 
                            | "(" Expression ")" ;

ObjectDeclaration           = "let" Identifier "=" ObjectConstructor ;

ObjectConstructor           = ObjectType "(" ObjectArguments ")" ;

ObjectType                  = "Cuboid" | "Pyramid" | "Cone" | "Cylinder" | "Sphere" | "Tetrahedron" ;

ObjectMethodCall            = Identifier "." FunctionCall ;

Comment                     = "#" ( Character - "\n" )* ;

Letter                      = ( "a".."z" | "A".."Z" ) ;

Digit                       = "0".."9" ;

Symbol                      = "+" | "-" | "*" | "/" | "(" | ")" | "[" | "]" | "=" | "." | "," | "\"" | "'" | ";" | ":" | "<" | ">" | "!" | "?" | "&" | "|" ;

Whitespace                  = " " | "\t" | "\r" | "\n" ;

Character                   = ( Letter | Digit | Symbol | Whitespace ) ;
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

Komentarze

```typescript
# single line comment
let a = 4 # comment after statement
```

Stałe

```typescript
let a = PI
Cone b = (radius=3*PI, height=2)
```

#### Bryły geometryczne

Deklaracje

```
let a = Cuboid(width=4, length=2, height=5)
let b = Pyramid(width=4, length=2, height=7)
let c = Cone(radius=3, height=7)
let d = Cylinder(radius=3, height=7)
let e = Sphere(radius=3)
let f = Tetrahedron(edge=3)
```

Metody

```
a.getBaseArea()
a.getSurfaceArea()
a.getVolume()
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

## Błędy

Program będzie obsługiwał następujące błędy z każdego modułu, tj. analizatora leksykalnego, składniowego i interpretera. Jeśli wystąpi błąd, to program nie będzie przerywał swojej pracy, tylko będzie próbował kontynuować. W przypadku wystąpienia błędu, program powinien wyświetlić informację o błędzie na standardowe wyjście.
Przykładowy błąd:

```LexerError: Invalid character in number at [Line 2, Column 2]```