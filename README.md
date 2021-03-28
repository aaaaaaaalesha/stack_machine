# Домашнее задание №1. Stack Machine.
## Выполнил: Александров Алексей Николаевич, ИУ8-44
<img alt="aaaaaaaalesha" src="https://img.shields.io/badge/aaaaaaaalesha-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/><img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>

## Задание.

Разработать стек машину, обратывающую forth-подобный язык.

### Внутренние сущности:

- [x] `DS` (data stack) - основной стек для операций;
- [x] `RS` (return stack) - поддерживает работу процедур;
- [x] `IP` (instruction pointer) - указатель на текущую инструкцию в коде;
- [x] `код` - последовательный набор инструкций и операндов к ним;
- [x] `TOS` (top-of-stack) - вершина стека;
- [x] `heap` - пространство для переменных;

### Поддерживаемые инструкции:

- [x] `int` - арифметика: `%`, `*`, `+`, `-`, `/`, `!` (факториал);
- [x] опреаторы сравнения: `>`, `<`, `==`, `and`, `or`;
- [x] `cast_int`, `cast_str` - преобразование в `int`, `str`;
- [x] `drop` - удалить TOS;
- [x] `dup` - дубликация TOS;
- [x] `if` - оператор `if`;
- [x] `jmp` - переход на заданный адрес инструкции;
- [x] `stack` - вывести содержимое DS, IP, RS;
- [x] `swap` - поменять местами TOS, TOS-1;
- [x] `over` - копирует TOS-1 на вершину стека;
- [x] `print`/`println` - вывести TOS;
- [x] `read` - прочитать ввод от user и положить в TOS;
- [x] `return` - возврат из процедуры (return_stack.pop);
- [x] `exit` - завершение VM;
- [x] `call` - вызов процедуры (сохранить состояние IP, перейти по адресу первой инструкции процедуры);
- [x] `store` - положить по имени TOS значение TOS-1 в `heap`;
- [x] `load` - загрузить содержимое переменной TOS, положить в TOS;

## Пример вычисления квадратичной функции из ТЗ.
Исполняемый файл программы - `stack_machine.py`

### Source code from example.txt:
```shell
------------------------------
// функция возведения в квадрат
: power2 dup * ;
// функция получения int от пользователя
: get_arg print read cast_int ;
"Give me $a" get_arg "a" store
"Give me $b" get_arg "b" store
"Give me $c" get_arg "c" store
"Give me $x" get_arg "x" store
"a" load "x" load power2  * "b" load "x" load * + "c" load + dup println stack
------------------------------
```
### Исполнение на стек машине:
```shell
/usr/bin/python3.7 /home/aaaaaaaalesha/github/stack_machine/src/stack_machine.py
Compile Result: ['"Give me $a"', 43, 'call', '"a"', 'store', '"Give me $b"', 43, 'call', '"b"', 'store', '"Give me $c"', 43, 'call', '"c"', 'store', '"Give me $x"', 43, 'call', '"x"', 'store', '"a"', 'load', '"x"', 'load', 40, 'call', '*', '"b"', 'load', '"x"', 'load', '*', '+', '"c"', 'load', '+', 'dup', 'println', 'stack', 'exit', 'dup', '*', 'return', 'print', 'read', 'cast_int', 'return']
Give me $a 12
Give me $b 32
Give me $c 1
Give me $x 8
1025
Data Stack[1025]
Instruction Pointer: 39
ReturnStack[]
```

## Пример собственной программы для стек машины.

В качестве собственной программы я решил выбрать вычисление функции факториал, а также простейших комбинаторных выборок 
<img src="https://render.githubusercontent.com/render/math?math=A_{n}^{k}"> и <img src="https://render.githubusercontent.com/render/math?math=C_{n}^{k}">.

Исполняемый файл программы - `main.py`

### Source code from binomial.txt:
```shell
// Print 6 times
: print6 println println println println println println ;
// Placement (A_{n}^{k})
: placement swap dup ! "n_fact" store swap - ! "n_fact" load swap / cast_int ;
// Combinations (C_{n}^{k})
: combination dup ! "k_fact" store placement "k_fact" load / cast_int ;
// Main code
"╚═══╝╚══╝╚╝─╚╝╚══╝╚╝──╚╝╚══╝╚╝╚╝╚══╝"
"║╚═╝║╔╝╚╗║║─║║║╚╝║║║╚╝║║╔╝╚╗║║║║║╚═╗"
"║╔═╗║─║║─║║╚╗║║║║║║╔╗╔╗║─║║─║╔╗║║║"
"║╚╝╚╗─║║─║╔╗─║║║║║║╚╗╔╝║─║║─║╚╝║║║"
"║╔╗║─╚╗╔╝║╚═╝║║╔╗║║║──║║╚╗╔╝║╔╗║║║"
"╔══╗─╔══╗╔╗─╔╗╔══╗╔╗──╔╗╔══╗╔══╗╔╗"
print6
"Enter n: " print read cast_int "n" store
"Enter k: " print read cast_int "k" store
// Factorial
"n" load ! "n! =" print println
"k" load ! "k! =" print println
// Placement
"A_{n}^{k} =" print "n" load "k" load placement println
// Binomial coefficient
"C_{n}^{k} =" print "n" load "k" load combination print
```
### Исполнение на стек машине:
```shell
/usr/bin/python3.6 /home/aaaaaaaalesha/github/stack_machine/src/main.py
Compile Result: ['"╚═══╝╚══╝╚╝─╚╝╚══╝╚╝──╚╝╚══╝╚╝╚╝╚══╝"', '"║╚═╝║╔╝╚╗║║─║║║╚╝║║║╚╝║║╔╝╚╗║║║║║╚═╗"', '"║╔═╗║─║║─║║╚╗║║║║║║╔╗╔╗║─║║─║╔╗║║║"', '"║╚╝╚╗─║║─║╔╗─║║║║║║╚╗╔╝║─║║─║╚╝║║║"', '"║╔╗║─╚╗╔╝║╚═╝║║╔╗║║║──║║╚╗╔╝║╔╗║║║"', '"╔══╗─╔══╗╔╗─╔╗╔══╗╔╗──╔╗╔══╗╔══╗╔╗"', 51, 'call', '"Enter n: "', 'print', 'read', 'cast_int', '"n"', 'store', '"Enter k: "', 'print', 'read', 'cast_int', '"k"', 'store', '"n"', 'load', '!', '"n! ="', 'print', 'println', '"k"', 'load', '!', '"k! ="', 'print', 'println', '"A_{n}^{k} ="', 'print', '"n"', 'load', '"k"', 'load', 58, 'call', 'println', '"C_{n}^{k} ="', 'print', '"n"', 'load', '"k"', 'load', 72, 'call', 'print', 'exit', 'println', 'println', 'println', 'println', 'println', 'println', 'return', 'swap', 'dup', '!', '"n_fact"', 'store', 'swap', '-', '!', '"n_fact"', 'load', 'swap', '/', 'cast_int', 'return', 'dup', '!', '"k_fact"', 'store', 58, 'call', '"k_fact"', 'load', '/', 'cast_int', 'return']
╔══╗─╔══╗╔╗─╔╗╔══╗╔╗──╔╗╔══╗╔══╗╔╗
║╔╗║─╚╗╔╝║╚═╝║║╔╗║║║──║║╚╗╔╝║╔╗║║║
║╚╝╚╗─║║─║╔╗─║║║║║║╚╗╔╝║─║║─║╚╝║║║
║╔═╗║─║║─║║╚╗║║║║║║╔╗╔╗║─║║─║╔╗║║║
║╚═╝║╔╝╚╗║║─║║║╚╝║║║╚╝║║╔╝╚╗║║║║║╚═╗
╚═══╝╚══╝╚╝─╚╝╚══╝╚╝──╚╝╚══╝╚╝╚╝╚══╝
Enter n:  5
Enter k:  3
n! = 120
k! = 6
A_{n}^{k} = 60
C_{n}^{k} = 10 
```
`Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>`
