# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from src.stack import Stack


class StackMachine:
    """Implementation of virtual stack machine."""

    def __init__(self, text):
        self.__ds = Stack()
        self.__rs = Stack()
        self.__iptr = 0
        self.__text = text
        self.__valid_instructions = {
            '+': self.sum,
            '-': self.sub,
            '*': self.mult,
            '/': self.div,
            '%': self.mod,
            '==': self.equal,
            'cast_int': self.cast_int,
            'cast_str': self.cast_str,
            'drop': self.drop,
            'dup': self.dup,
            'if': self.cond_check,
            'jmp': self.jump,
            'stack': self.output_stack,
            'swap': self.swap,
            'print': self.print,
            'read': self.read,
            'call': self.call,
            'return': self.ret,
            'exit': self.exit,
            'store': self.store,
            'load': self.load,
        }

    def sum(self):
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs + rhs)

    def sub(self):
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs - rhs)

    def mult(self):
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs * rhs)

    def div(self):
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs / rhs)

    def mod(self):
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs % rhs)

    def equal(self):
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs == rhs)

    def cast_int(self):
        casted_value = int(self.__ds.pop())
        self.__ds.push(casted_value)

    def cast_str(self):
        casted_value = str(self.__ds.pop())
        self.__ds.push(casted_value)

    def drop(self):
        self.__ds.pop()

    def dup(self):
        tos = self.__ds.top()
        self.__ds.push(tos)

    def cond_check(self):
        is_false = self.__ds.pop()
        is_true = self.__ds.pop()
        condition = self.__ds.pop()

        if condition:
            self.__ds.push(is_true)
        else:
            self.__ds.push(is_false)

    def jump(self):
        ptr = self.__ds.pop()
        if not (0 <= ptr < len(self.__text)):
            raise OverflowError("Instruction jmp cannot be executed with a pointer outside the valid range.")
        self.__iptr = ptr

    def output_stack(self):
        print("Data " + self.__ds.__str__())
        print("Instruction Pointer: " + str(self.__iptr))
        print("Return" + self.__rs.__str__())

    def swap(self):
        tos = self.__ds.pop()
        tos1 = self.__ds.pop()
        self.__ds.push(tos)
        self.__ds.push(tos1)

    def print(self):
        print(self.__ds.pop())

    def read(self):
        self.__ds.push(input())
