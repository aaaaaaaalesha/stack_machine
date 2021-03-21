# Домашнее задание №1. Stack Machine.
  
## Задание
Разработать стек машину, обратывающую forth-подобный язык  
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
"a" load "x" load * "b" load + "x" load * "c" load + dup println stack
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
#### Внутренние сущности:  
* `DS` (data stack) - основной стек для операций
* `RS` (return stack) - поддерживает работу процедур
* `IP` (instruction pointer) - указатель на текущую инструкцию в коде
* `код` - последовательный набор инструкций и операндов к ним
* `TOS` (top-of-stack) - вершина стека
* `heap` - пространство для переменных

#### Минимальный набор инструкций:  
* int-арифметика: `%`, `*`, `+`, `-`, `/`, `==`
* `cast_int`, `cast_str` - преобразование в `int`, `str`: 
* `drop` - удалить TOS
* `dup` - дубликация TOS
* `if` - `true_clause false_clause condition if`
* `jmp` - переход на заданный адрес инструкции
* `stack` - вывести содержимое DS, IP, RS
* `swap` - поменять местами TOS, TOS-1
* `print`/`println` - вывести TOS
* `read` - прочитать ввод от user и положить в TOS
* `call` - вызов процедуры (сохранить состояние IP, перейти по адресу первой инструкции процедуры)
* `return` - возврат из процедуры (return_stack.pop)
* `exit` - завершение VM
* `store` - положить по имени TOS значение TOS-1
* `load` - загрузить содержимое переменной TOS, положить в TOS

#### Основные идеи:  
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

PS - за идею благодарим Christian Stigen Larsen (https://csl.name/post/vm/).
