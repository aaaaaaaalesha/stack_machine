# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from src.stack import Stack
import io
import tokenize


class StackMachineException(Exception):
    pass


class InvalidInstructionException(StackMachineException):
    pass


class HeapException(StackMachineException):
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
        # Storage for procedures.
        self._procedures = dict()
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
            'println': self.println,
            'read': self.read,
            'call': self.call,
            'return': self.ret,
            'exit': self.exit,
            'store': self.store,
            'load': self.load,
        }

    def compile(self):
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
        for ptr in range(len(self._code_list)):
            if self._code_list[ptr] == ':':
                # All procedures have the following form:
                # : <procedure_name> <instr_1> <instr_2> ... <instr_N> ;
                procedure_name = self._code_list[ptr + 1]
                ptr += 2
                procedure_code = []
                while self._code_list[ptr] != ';':
                    procedure_code.append(self._code_list[ptr])
                    ptr += 1
                # For the specified procedure_name, we set a list of instructions.
                # Then the address of the procedure will be the hash of the key in the dict.
                self._procedures[procedure_name] = procedure_code

        # Cut the procedures from the course code.
        while self._code_list.count(':') != 0:
            ind = self._code_list.index(':')
            last_ind = self._code_list.index(';')
            self._code_list = self._code_list[:ind] + self._code_list[last_ind + 1:]

        # Step 2. Replace procedures with <procedure_address> 'call' in procedures' code.
        for procedure_name, procedure_code in self._procedures.items():
            # Check that at least one procedure in code.
            if any([p in procedure_code for p in self._procedures.keys()]):
                i = 0
                while i != (len(self._procedures[procedure_name]) - 1):
                    if procedure_code[i] in self._procedures:
                        i += 1
                        # Replace procedure_name to address of procedure (hash in our dict)  and 'call'.
                        code_copy = procedure_code[:i] + ['call'] + procedure_code[i:]
                        self._procedures[procedure_name] = code_copy
                    i += 1

        # Step 3. Replace procedures with <procedure_address> 'call' in main-code.
        if any([p in self._code_list for p in self._procedures.keys()]):
            i = 0
            while i != (len(self._code_list) - 1):
                if self._code_list[i] in self._procedures:
                    i += 1
                    # Replace procedure_name to address of procedure (hash in our dict)  and 'call'.
                    code_copy = self._code_list[:i] + ['call'] + self._code_list[i:]
                    self._code_list = code_copy
                i += 1

        if self._procedures:
            # Step 4. Add an 'exit' instruction.
            self._code_list.append('exit')

            # Step 5. Add the procedures code at the end of 'main'-code.
            for procedure_name, procedure_code in self._procedures.items():
                # Address of future procedure.
                address = len(self._code_list)
                for opcode in procedure_code:
                    self._code_list.append(opcode)
                self._code_list.append('return')
                self._procedures[procedure_name] = address

            # Step 6. Change procedures' names to their addresses.
            for i in range(len(self._code_list)):
                if self._code_list[i] in self._procedures:
                    self._code_list[i] = self._procedures[self._code_list[i]]

    def launch(self):
        """Launching the stack machine."""
        self.compile()
        while self._iptr < len(self._code_list):
            current = self._code_list[self._iptr]
            # Go to next instruction.
            self._iptr += 1
            if isinstance(current, int):
                # Put number on data stack.
                self._ds.push(current)
            elif isinstance(current, str) and (current[0] == current[len(current) - 1] == '"'):
                # Put message on data stack.
                self._ds.push(current[1:len(current) - 1])
            elif current in self._valid_operations:
                # Run the instruction.
                self._valid_operations[current]()
            else:
                raise InvalidInstructionException(f"{current} is invalid instruction or type for stack machine.")

    def parse(self, text: str):
        """Parsing the source code to instructions list for machine."""
        stream = io.StringIO(text)
        tokens = tokenize.generate_tokens(stream.readline)

        for toknum, tokval, _, _, _ in tokens:
            if toknum == tokenize.NUMBER:
                yield int(tokval)
            elif toknum == tokenize.NEWLINE:  # '\n'
                continue
            elif toknum == tokenize.ENDMARKER:  # ''
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
        print(self._ds.pop(), end=' ')

    def println(self):
        """Output the TOS and switching to a new line."""
        print(self._ds.pop())

    def read(self):
        """Read an input of user and put it at the TOS."""
        self._ds.push(input())

    def exit(self):
        """Terminates the stack machine."""
        quit(0)

    def ret(self):
        """Return from procedure."""
        self._iptr = self._rs.pop()

    def call(self):
        """Calling an existing procedure."""
        # Store return pointer in RS.
        self._rs.push(self._iptr)
        # Jump to calling procedure.
        self.jump()

    def store(self):
        """Put the value of TOS-1 by the variable initialized by name of TOS."""
        var_name = self._ds.pop()
        value = self._ds.pop()
        # Store pair var_name-value in heap.
        self._heap[var_name] = value

    def load(self):
        """Loads the value of var from the heap by the name lying on TOS and puts this value on TOS."""
        var_name = self._ds.pop()
        if var_name in self._heap:
            # Load the value.
            self._ds.push(self._heap[var_name])
        else:
            raise HeapException(f"No variable {var_name} in heap.")


if __name__ == "__main__":
    # text1 = "2 3 + 4 * print"

    # text2 = ' '.join([
    #     '"Enter a number: "', "print", "read", "cast_int",
    #     '"Enter another number: "', "print", "read", "cast_int",
    #     '"Their sum is: "', "print", "+", "print",
    # ])

    text = """: power2 dup * ;
: get_arg print read cast_int ;
"Give me $a" get_arg "a" store
"Give me $b" get_arg "b" store
"Give me $c" get_arg "c" store
"Give me $x" get_arg "x" store
"a" load "x" load power2  * "b" load "x" load * + "c" load + dup println stack
"""

    sm = StackMachine(text)

    sm.launch()
