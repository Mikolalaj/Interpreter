### TKOM - Interpreter języka opisu brył

# Treść zadania
Język do opisu brył i ich właściwości. Podstawowe bryły (prostopadłościan, ostrosłup, stożek, walec, kula itd.) są wbudowanymi typami języka. Każdy typ posiada wbudowane metody służące do wyznaczania charakterystycznych dla niego wielkości, np. pole podstawy, pole powierzchni bocznej, objętość, wysokość, średnica itp. Kolekcja brył tworzy scenę wyświetlaną na ekranie.

Język dynamiczne i silne typowanie. // może zmienić na słabe?

Czym jest program? Program może być zdefiniowany w pliku lub jako ciąg znaków. Program składa się z deklaracji zmiennych i funkcji oraz instrukcji sterujących.

Minus nie jest częścią liczby

# Przykładowe wyrażenia
Deklaracja zmiennej
```typescript
int a = 5
float b = 3.14
string c = "Hello world!" # nie `` ani ''
bool d = true
bool e = false
int[] f = [1, 2, 3, 4, 5]
```

Deklaracja funkcji
```typescript
function add(a: int, b: int) -> int {
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
while (true) {
    print("infinite loop")
    if (a > 0) {
        break
    }
    if (a < -5) {
        continue
    }
    print("close to zero")
}
```

Komentarze
```typescript
# single line comment
int a = 4 # comment after statement
```

Typy danych z zadania
```
cuboid cub = (4, 2, 5) # szerokość, długość, wysokość
pyramid pyr = (4, 2, 7) # szerokość, długość, wysokość
cone con = (3, 7) # promień podstawy, wysokość
cylinder cyl = (3, 7) # promień podstawy, wysokość
sphere sph = (3) # promień
```

Stałe
```typescript
float a = PI
cone con = (3, 2*PI)
```
