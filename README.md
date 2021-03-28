# Домашнее задание №1. Stack Machine.

<img alt="aaaaaaaalesha" src="https://img.shields.io/badge/aaaaaaaalesha-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/><img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>

## Задание

Разработать стек машину, обратывающую forth-подобный язык.

```
Пример: вычисление квадратичной функции  
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

/usr/local/bin/python3.7 pythonProject/vm.py run.vm
Give me $a 12
Give me $b 32
Give me $c 1
Give me $x 8
1025
<StopIteration>
Data stack (top first):
 - type <class 'int'>, value '1025'

---------------------------------------
Результат компиляции:
['"Give me $a"', 43, 'call', '"a"', 'store', '"Give me $b"', 43, 'call', '"b"', 'store', '"Give me $c"', 43, 'call', '"c"', 'store', '"Give me $x"', 43, 'call', '"x"', 'store', '"a"', 'load', '"x"', 'load', '*', '"b"', 'load', '+', '"x"', 'load', '*', '"c"', 'load', '+', 'dup', 'println', 'stack', '', '', 'exit', 'dup', '*', 'return', 'print', 'read', 'cast_int', 'return']
```

### Внутренние сущности:

-[x] `DS` (data stack) - основной стек для операций;
-[x] `RS` (return stack) - поддерживает работу процедур;
-[x] `IP` (instruction pointer) - указатель на текущую инструкцию в коде;
-[x] `код` - последовательный набор инструкций и операндов к ним;
-[x] `TOS` (top-of-stack) - вершина стека;
-[x] `heap` - пространство для переменных;

### Минимальный набор инструкций:

-[x] `int` - арифметика: `%`, `*`, `+`, `-`, `/`;
-[x] опреаторы сравнения: `>`, `<`, `==`, `and`, `or`;
-[x] `cast_int`, `cast_str` - преобразование в `int`, `str`;
-[x] `drop` - удалить TOS;
-[x] `dup` - дубликация TOS;
-[x] `if` - оператор `if`;
-[x] `jmp` - переход на заданный адрес инструкции;
-[x] `stack` - вывести содержимое DS, IP, RS;
-[x] `swap` - поменять местами TOS, TOS-1;
-[x] `print`/`println` - вывести TOS;
-[x] `read` - прочитать ввод от user и положить в TOS;
-[x] `return` - возврат из процедуры (return_stack.pop);
-[x] `exit` - завершение VM;
-[x] `call` - вызов процедуры (сохранить состояние IP, перейти по адресу первой инструкции процедуры);
-[x] `store` - положить по имени TOS значение TOS-1 в `heap`;
-[x] `load` - загрузить содержимое переменной TOS, положить в TOS;

### Основные идеи:

* при парсинге, можно использовать встроенный питонячий-токенизатор:
  ```python
  stream = io.StringIO(text)
  tokens = tokenize.generate_tokens(stream.readline)

  for toknum, tokval, _, _, _ in tokens:
      if toknum == tokenize.NUMBER:
          yield int(tokval)
      else:
          yield tokval
  ``` 

* не нужно париться про оптимизации (например, предварительное сворачивание констант)
* при "компиляции" нужно сделать следующее:
    * отделить процедуры от остального кода (временный словарь)
    * пройтись по коду внутри процедур, заменить встречающиеся процедуры на <адрес_процедуры> `call`
    * пройтись по `main`-коду, заменить встречающиеся процедуры на <адрес_процедуры> `call`
    * добавить в конец `main`-кода инструкцию `exit`
    * добавить в конец результирующего кода код процедур, сохранить адреса
    * пройтись по результирующему коду, заменить все названия процедур на их адреса

`Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>`
