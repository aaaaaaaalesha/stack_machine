# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>
from src.stack_machine import StackMachine, output_source_code

if __name__ == '__main__':
    """Example from the task."""
    with open('../binomial.txt', 'r') as f:
        source_code = f.read()
        output_source_code(source_code)

    sm = StackMachine(source_code)

    sm.launch()
