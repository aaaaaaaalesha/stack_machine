# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from src.stack import Stack
import io
import tokenize


class StackMachineException(Exception):
    pass


class InvalidInstructionException(StackMachineException):
    pass


class StackMachine:
    """Implementation of virtual stack machine."""

    def __init__(self, text: str):
        # Data stack (main stack for operations).
        self._ds = Stack()
        # Return stack (supports procedures work).
        self._rs = Stack()
        # Instruction pointer.
        self._iptr = 0
        # Input text parsed into list of values and instructions.
        self._code_list = list(self.parse(text))
        # Storage for variables. Mapping names of vars to their values.
        self._heap = dict()
        # Mapping operations in our language to functions that perform the necessary business logic.
        self._valid_operations = {
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
            'if': self.operator_if,
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

    def launch(self):
        """Launching the compilation process by stack machine."""
        while self._iptr < len(self._code_list):
            current = self._code_list[self._iptr]
            if isinstance(current, int):
                # Put number on data stack.
                self._ds.push(current)
            elif isinstance(current, str) and (current[0] == current[len(current) - 1] == '"'):
                # Put message on data stack.
                self._ds.push(current[1:len(current) - 2])
            elif current in self._valid_operations:
                # Run the instruction.
                self._valid_operations[current]()
            else:
                raise InvalidInstructionException(f"{current} is invalid instruction or type for stack machine.")
            # Go to next instruction.
            self._iptr += 1

    def parse(self, text: str):
        stream = io.StringIO(text)
        tokens = tokenize.generate_tokens(stream.readline)

        for toknum, tokval, _, _, _ in tokens:
            if toknum == tokenize.NUMBER:
                yield int(tokval)
            elif toknum == tokenize.NEWLINE:
                continue
            elif toknum == tokenize.ENDMARKER:
                break
            else:
                yield tokval

    # Instructions implementation.
    def sum(self):
        """Implementation of '+'."""
        rhs = self._ds.pop()
        lhs = self._ds.pop()
        self._ds.push(lhs + rhs)

    def sub(self):
        """Implementation of '-'."""
        rhs = self._ds.pop()
        lhs = self._ds.pop()
        self._ds.push(lhs - rhs)

    def mult(self):
        """Implementation of '*'."""
        rhs = self._ds.pop()
        lhs = self._ds.pop()
        self._ds.push(lhs * rhs)

    def div(self):
        """Implementation of '/'."""
        rhs = self._ds.pop()
        lhs = self._ds.pop()
        self._ds.push(lhs / rhs)

    def mod(self):
        """Implementation of '%'."""
        rhs = self._ds.pop()
        lhs = self._ds.pop()
        self._ds.push(lhs % rhs)

    def equal(self):
        """Implementation of '=='."""
        rhs = self._ds.pop()
        lhs = self._ds.pop()
        self._ds.push(lhs == rhs)

    def cast_int(self):
        """Cast TOS to int."""
        casted_value = int(self._ds.pop())
        self._ds.push(casted_value)

    def cast_str(self):
        """Cast TOS to str."""
        casted_value = str(self._ds.pop())
        self._ds.push(casted_value)

    def drop(self):
        """Throw TOS away..."""
        self._ds.pop()

    def dup(self):
        """Duplication of TOS."""
        tos = self._ds.top()
        self._ds.push(tos)

    def operator_if(self):
        """Implementation if-operator."""
        is_false = self._ds.pop()
        is_true = self._ds.pop()
        condition = self._ds.pop()

        if condition:
            self._ds.push(is_true)
        else:
            self._ds.push(is_false)

    def jump(self):
        """Jumping to pointer of instruction."""
        ptr = self._ds.pop()
        if not (0 <= ptr < len(self._code_list)):
            raise OverflowError("Instruction jmp cannot be executed with a pointer outside the valid range.")
        self._iptr = ptr

    def output_stack(self):
        """Output the content of DS, IP and RS."""
        print("Data " + self._ds.__str__())
        print("Instruction Pointer: " + str(self._iptr))
        print("Return" + self._rs.__str__())

    def swap(self):
        """Swap TOS and TOS-1."""
        tos = self._ds.pop()
        tos1 = self._ds.pop()
        self._ds.push(tos)
        self._ds.push(tos1)

    def print(self):
        """Output the TOS."""
        print(self._ds.pop())

    def read(self):
        """Read an input of user and put it at the TOS."""
        self._ds.push(input())

    def exit(self):
        """Terminates the stack machine."""
        quit(0)

    def ret(self):
        """Return from procedure."""
        self._rs.pop()

    def call(self):
        # TODO
        pass

    def store(self):
        # TODO
        pass

    def load(self):
        # TODO
        pass


if __name__ == "__main__":
    text = "2 3 + 4 * print"
    sm = StackMachine(text)

    sm.launch()
