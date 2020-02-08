# mapleleaf
An interpreted language made purely in Python. It does not use any external libraries such as lex/yacc, and is currently a work in progress.


### Features

###### Variable declaration
```
var a = 0;
var b = 2;
```
###### Basic arithmetic and order of operations
```
print((3+5)*(2)); # 16
```
###### Some neat high-level features
```
var q = "Hello";
var r = 0;

# Overloaded + operator for string-int concatenation
print(q+r) # "Hello0"
var s = "Hello";
var t = "ell";

# Removes the first occurence of t in s
print(s-t); # "Ho"
```
###### Block scoping
```
{
    var a = "Hello, World!";
    print("Printing from inside block: " + a); # OK
}

print("Printing from outside block: " + a); # Runtime error
```
###### For/While loops
```
var i = 0;
from (; i < 10; i = i + 1) {
    print("Hello");
}

until (i < 20) {
    print("World");
}
```
###### Nested for/while loops
```
from (var i = 0; i < 3; i = i + 1) {
    from (var j = 0; j < 3; j = j + 1) {
        print(i+j);
    }
}

# Output
0
1
2
1
3
2
3
4
```

To use the language, run `mapleleaf.py` with `sample.maple` as an argument
