# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from src.stack import Stack
from io import StringIO


class StackMachine:
    """Implementation of virtual stack machine."""

    def __init__(self, text):
        # Data stack (main stack for operations).
        self.__ds = Stack()
        # Return stack (supports procedures work).
        self.__rs = Stack()
        # Instruction pointer.
        self.__iptr = 0
        # The input code text.
        self.__text = text
        # Mapping operations in our language to functions that perform the necessary business logic.
        self.__valid_operations = {
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

    # Instructions implementation.
    def sum(self):
        """Implementation of '+'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs + rhs)

    def sub(self):
        """Implementation of '-'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs - rhs)

    def mult(self):
        """Implementation of '*'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs * rhs)

    def div(self):
        """Implementation of '/'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs / rhs)

    def mod(self):
        """Implementation of '%'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs % rhs)

    def equal(self):
        """Implementation of '=='."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs == rhs)

    def cast_int(self):
        """Cast TOS to int."""
        casted_value = int(self.__ds.pop())
        self.__ds.push(casted_value)

    def cast_str(self):
        """Cast TOS to str."""
        casted_value = str(self.__ds.pop())
        self.__ds.push(casted_value)

    def drop(self):
        """Throw TOS away..."""
        self.__ds.pop()

    def dup(self):
        """Duplication of TOS."""
        tos = self.__ds.top()
        self.__ds.push(tos)

    def cond_check(self):
        """Implementation if-operator."""
        is_false = self.__ds.pop()
        is_true = self.__ds.pop()
        condition = self.__ds.pop()

        if condition:
            self.__ds.push(is_true)
        else:
            self.__ds.push(is_false)

    def jump(self):
        """Jumping to pointer of instruction."""
        ptr = self.__ds.pop()
        if not (0 <= ptr < len(self.__text)):
            raise OverflowError("Instruction jmp cannot be executed with a pointer outside the valid range.")
        self.__iptr = ptr

    def output_stack(self):
        """Output the content of DS, IP and RS."""
        print("Data " + self.__ds.__str__())
        print("Instruction Pointer: " + str(self.__iptr))
        print("Return" + self.__rs.__str__())

    def swap(self):
        """Swap TOS and TOS-1."""
        tos = self.__ds.pop()
        tos1 = self.__ds.pop()
        self.__ds.push(tos)
        self.__ds.push(tos1)

    def print(self):
        """Output the TOS."""
        print(self.__ds.pop())

    def read(self):
        """Read an input of user and put it at the TOS."""
        self.__ds.push(input())

    def exit(self):
        """Terminates the stack machine."""
        quit(0)

    def ret(self):
        """Return from procedure."""
        self.__rs.pop()
