# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

import io
import tokenize
import sys
from functools import reduce

from src.stack import Stack


class StackMachineException(Exception):
    """
    Base StackMachine exception.
    """
    pass


class InvalidInstructionException(StackMachineException):
    """
    StackMachine exception which is thrown when an invalid instruction exists.
    """
    pass


class HeapException(StackMachineException):
    """
    StackMachine exception which is thrown when a variable could not be found in heap.
    """
    pass


class StackMachine:
    """Implementation of virtual stack machine."""

    def __init__(self, text: str):
        # Data stack (main stack for operations).
        self.__ds = Stack()
        # Return stack (supports procedures work).
        self.__rs = Stack()
        # Instruction pointer.
        self.__iptr = 0
        # Input text parsed into list of values and instructions.
        self.__code_list = list(self.parse(text))
        # Storage for variables. Mapping names of vars to their values.
        self.__heap = dict()
        # Storage for procedures.
        self.__procedures = dict()
        # Mapping operations in our language to functions that perform the necessary business logic.
        self.__valid_operations = {
            '+': self.sum,
            '-': self.sub,
            '*': self.mult,
            '/': self.div,
            '%': self.mod,
            '!': self.fact,
            '==': self.equal,
            '>': self.greater,
            '<': self.less,
            'and': self.operator_and,
            'or': self.operator_or,
            'cast_int': self.cast_int,
            'cast_str': self.cast_str,
            'drop': self.drop,
            'over': self.over,
            'dup': self.dup,
            'if': self.operator_if,
            'jmp': self.jump,
            'stack': self.output_stack,
            'swap': self.swap,
            'print': self.print,
            'println': self.println,
            'read': self.read,
            'call': self.call,
            'return': self.ret,
            'exit': self.exit,
            'store': self.store,
            'load': self.load,
        }

    def compile(self) -> None:
        """
        When "compiling", we need to do the following:
            1. separate procedures from the rest of the code (temp dict self._procedures);
            2. go through the code inside the procedures, replace procedures with <procedure_address> 'call';
            3. go through the 'main'-code, replace procedures with <procedure_address_> 'call';
            4. add an 'exit' instruction to the end of the 'main' code;
            5. add the procedure code to the end of the resulting code, save the addresses;
            6. go through the resulting code, replace all procedure names with their addresses;
        """

        # Step 1. Save all procedures in special dict (self._procedures).
        for ptr in range(len(self.__code_list)):
            if self.__code_list[ptr] == ':':
                # All procedures have the following form:
                # : <procedure_name> <instr_1> <instr_2> ... <instr_N> ;
                procedure_name = self.__code_list[ptr + 1]
                ptr += 2
                procedure_code = []
                while self.__code_list[ptr] != ';':
                    procedure_code.append(self.__code_list[ptr])
                    ptr += 1
                # For the specified procedure_name, we set a list of instructions.
                # Then the address of the procedure will be the hash of the key in the dict.
                self.__procedures[procedure_name] = procedure_code

        # Cut the procedures from the course code.
        while self.__code_list.count(':') != 0:
            ind = self.__code_list.index(':')
            last_ind = self.__code_list.index(';')
            self.__code_list = self.__code_list[:ind] + self.__code_list[last_ind + 1:]

        # Step 2. Replace procedures with <procedure_address> 'call' in procedures' code.
        for procedure_name, procedure_code in self.__procedures.items():
            # Check that at least one procedure in code.
            if any([p in procedure_code for p in self.__procedures.keys()]):
                i = 0
                while i != (len(self.__procedures[procedure_name]) - 1):
                    if procedure_code[i] in self.__procedures:
                        i += 1
                        # Replace procedure_name to address of procedure (hash in our dict)  and 'call'.
                        code_copy = procedure_code[:i] + ['call'] + procedure_code[i:]
                        self.__procedures[procedure_name] = code_copy
                    i += 1

        # Step 3. Replace procedures with <procedure_address> 'call' in main-code.
        if any([p in self.__code_list for p in self.__procedures.keys()]):
            i = 0
            while i != (len(self.__code_list) - 1):
                if self.__code_list[i] in self.__procedures:
                    i += 1
                    # Replace procedure_name to address of procedure (hash in our dict)  and 'call'.
                    code_copy = self.__code_list[:i] + ['call'] + self.__code_list[i:]
                    self.__code_list = code_copy
                i += 1

        if self.__procedures:
            # Step 4. Add an 'exit' instruction.
            self.__code_list.append('exit')

            # Step 5. Add the procedures code at the end of 'main'-code.
            for procedure_name, procedure_code in self.__procedures.items():
                # Address of future procedure.
                address = len(self.__code_list)
                for opcode in procedure_code:
                    self.__code_list.append(opcode)
                self.__code_list.append('return')
                self.__procedures[procedure_name] = address

            # Step 6. Change procedures' names to their addresses.
            for i in range(len(self.__code_list)):
                if self.__code_list[i] in self.__procedures:
                    self.__code_list[i] = self.__procedures[self.__code_list[i]]

    def launch(self) -> None:
        """Launching the stack machine."""
        self.compile()
        print("Compile Result: " + str(self.get_compile_result()))
        while self.__iptr < len(self.__code_list):
            current = self.__code_list[self.__iptr]
            # Go to next instruction.
            self.__iptr += 1
            if isinstance(current, int):
                # Put number on data stack.
                self.__ds.push(current)
            elif isinstance(current, str) and ((current[0] == current[len(current) - 1] == '"') or (
                    current[0] == current[len(current) - 1] == "'")):
                # Put message on data stack.
                self.__ds.push(current[1:len(current) - 1])
            elif current in self.__valid_operations:
                # Run the instruction.
                self.__valid_operations[current]()
            else:
                raise InvalidInstructionException(str(current) + " is invalid instruction or type for stack machine.")

    @staticmethod
    def parse(text: str):
        """
        Parsing the source code to instructions list for machine.
        @param text: source code
        """
        stream = io.StringIO(text)
        tokens = tokenize.generate_tokens(stream.readline)

        # For comments deleting.
        comment_flag = False
        for toknum, tokval, _, _, _ in tokens:
            if toknum == tokenize.NUMBER:
                if not comment_flag:
                    yield int(tokval)
            elif toknum == tokenize.NEWLINE or toknum == 58 or tokval == ' ':  # '\n'
                if comment_flag:
                    comment_flag = False
                continue
            elif toknum == tokenize.ENDMARKER:  # ''
                if not comment_flag:
                    break
            elif tokval == '//':  # beginning of the comment
                comment_flag = True
            else:
                if not comment_flag:
                    yield tokval

    def get_TOS(self):
        """
        :return: TOS value
        """
        return self.__ds.pop()

    def get_compile_result(self) -> list:
        """
        :return: self.__code_list
        """
        return self.__code_list

    # Instructions implementation.
    def sum(self) -> None:
        """Implementation of '+'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs + rhs)

    def sub(self) -> None:
        """Implementation of '-'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs - rhs)

    def mult(self) -> None:
        """Implementation of '*'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs * rhs)

    def div(self) -> None:
        """Implementation of '/'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs / rhs)

    def mod(self) -> None:
        """Implementation of '%'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs % rhs)

    def fact(self) -> None:
        """Implementation of '!' (factorial function)."""
        n = self.__ds.pop()
        if not isinstance(n, int) or n < 0:
            raise StackMachineException("Factorial does not defined for " + str(n))
        else:
            if n == 0:
                self.__ds.push(1)
            else:
                self.__ds.push(reduce(lambda x, y: x * y, [i for i in range(1, n + 1)]))

    def equal(self) -> None:
        """Implementation of '=='."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs == rhs)

    def greater(self) -> None:
        """Implementation of '>'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs > rhs)

    def less(self) -> None:
        """Implementation of '<'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs < rhs)

    def operator_and(self) -> None:
        """Implementation of 'and'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs and rhs)

    def operator_or(self) -> None:
        """Implementation of 'or'."""
        rhs = self.__ds.pop()
        lhs = self.__ds.pop()
        self.__ds.push(lhs or rhs)

    def cast_int(self) -> None:
        """Cast TOS to int."""
        casted_value = int(self.__ds.pop())
        self.__ds.push(casted_value)

    def cast_str(self) -> None:
        """Cast TOS to str."""
        casted_value = str(self.__ds.pop())
        self.__ds.push(casted_value)

    def drop(self) -> None:
        """Throw TOS away..."""
        self.__ds.pop()

    def dup(self) -> None:
        """Duplication of TOS."""
        tos = self.__ds.top()
        self.__ds.push(tos)

    def operator_if(self) -> None:
        """Implementation if-operator."""
        is_false = self.__ds.pop()
        is_true = self.__ds.pop()
        condition = self.__ds.pop()

        if condition:
            self.__ds.push(is_true)
        else:
            self.__ds.push(is_false)

    def jump(self) -> None:
        """Jumping to pointer of instruction."""
        ptr = self.__ds.pop()
        if not (0 <= ptr < len(self.__code_list)):
            raise OverflowError("Instruction jmp cannot be executed with a pointer outside the valid range.")
        self.__iptr = ptr

    def output_stack(self) -> None:
        """Output the content of DS, IP and RS."""
        print("Data " + self.__ds.__str__())
        print("Instruction Pointer: " + str(self.__iptr))
        print("Return" + self.__rs.__str__())

    def swap(self) -> None:
        """Swap TOS and TOS-1."""
        tos = self.__ds.pop()
        tos1 = self.__ds.pop()
        self.__ds.push(tos)
        self.__ds.push(tos1)

    def over(self) -> None:
        """
        Puts the value of TOS-1 on TOS without removing it.
        :example: Stack[3, 2] -> Stack[2, 3, 2]
        """
        old_tos = self.__ds.pop()
        old_tos1 = self.__ds.pop()
        self.__ds.push(old_tos)
        self.__ds.push(old_tos1)

    def print(self) -> None:
        """Output the TOS."""
        print(self.__ds.pop(), end=' ')

    def println(self) -> None:
        """Output the TOS and switching to a new line."""
        print(self.__ds.pop())

    def read(self) -> None:
        """Read an input of user and put it at the TOS."""
        self.__ds.push(input())

    def exit(self) -> None:
        """Terminates the stack machine."""
        sys.exit(0)

    def ret(self) -> None:
        """Return from procedure."""
        self.__iptr = self.__rs.pop()

    def call(self) -> None:
        """Calling an existing procedure."""
        # Store return pointer in RS.
        self.__rs.push(self.__iptr)
        # Jump to calling procedure.
        self.jump()

    def store(self) -> None:
        """Put the value of TOS-1 by the variable initialized by name of TOS."""
        var_name = self.__ds.pop()
        value = self.__ds.pop()
        # Store pair var_name-value in heap.
        self.__heap[var_name] = value

    def load(self) -> None:
        """Loads the value of var from the heap by the name lying on TOS and puts this value on TOS."""
        var_name = self.__ds.pop()
        if var_name in self.__heap:
            # Load the value.
            self.__ds.push(self.__heap[var_name])
        else:
            raise HeapException(f"No variable {var_name} in heap.")


if __name__ == '__main__':
    """Example from the task."""
    with open('../example.txt', 'r') as f:
        source_code = f.read()

    sm = StackMachine(source_code)

    sm.launch()
