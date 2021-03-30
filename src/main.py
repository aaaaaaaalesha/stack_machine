# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>
from src.stack_machine import StackMachine

if __name__ == '__main__':
    """Example from the task."""
    with open('../binomial.txt', 'r') as f:
        source_code = f.read()

    sm = StackMachine(source_code)

    sm.launch()
