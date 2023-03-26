# TKOM - Interpreter języka opisu brył

## Treść zadania

>Język do opisu brył i ich właściwości. Podstawowe bryły (prostopadłościan, ostrosłup, stożek, walec, kula itd.) są wbudowanymi typami języka. Każdy typ posiada wbudowane metody służące do wyznaczania charakterystycznych dla niego wielkości, np. pole podstawy, pole powierzchni bocznej, objętość, wysokość, średnica itp. Kolekcja brył tworzy scenę wyświetlaną na ekranie.

***Język dynamicznie i silne typowanie.***

## Dokumentacja wstępna.
- formalna  specyfikacja i składnia: realizowanego języka (jeśli chodzi np. o interpretery), wszystkich plików/strumieni wejściowych, danych konfiguracyjnychitp.
- zwięzłą analizę wymagań funkcjonalnych i niefunkcjonalnych, obsługa błędów(jakiego rodzaju błędy będą wykrywane, tolerowane?, jak będzie wyglądał przykładowy komunikat o błędzie?).
- sposób uruchomienia, wej./wyj.
- zwięzły opis sposobu testowania–podane  przykłady testowanych konstrukcji językowych, przypadków złożonych, błędnych itp.

Czym jest program? Program może być zdefiniowany w pliku lub jako ciąg znaków. Program składa się z deklaracji zmiennych i funkcji oraz instrukcji sterujących.

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
