# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

import unittest

from src.stack_machine import StackMachine


class StackMachineTestCase(unittest.TestCase):
    def test_int_operations(self):
        # "(1 + 5 - 10) * 18 / 9 % 2 == 0" Expected result: True.
        source_code = "1 5 + 10 - 18 * 9 / 2 % 0 =="

        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        self.assertTrue(stack_machine.get_TOS())

    def test_conditions(self):
        source_code = "2 1 >"

        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        self.assertTrue(stack_machine.get_TOS())

        source_code = "1 2 <"

        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        self.assertTrue(stack_machine.get_TOS())

        source_code = "2 1 > 1 2 < and"

        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        self.assertTrue(stack_machine.get_TOS())

        source_code = "2 1 < 1 2 > or"

        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        self.assertFalse(stack_machine.get_TOS())

    def test_example(self):
        source_code = ' '.join([
            '"3"', "cast_int", '"n1"', "store",
            '"2"', "cast_int", '"n2"', "store",
            '"Their sum is:"', "print", '"n1"', "load", '"n2"', "load", "+", "dup", "println", '"sum"', "store",
            '"Their product is:"', "print", '"n1"', "load", '"n2"', "load", "*", "dup", "println", '"prod"', "store",
            '"prod"', "load", '"sum"', "load"
        ])

        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        self.assertEqual(stack_machine.get_TOS(), 3 + 2)
        self.assertEqual(stack_machine.get_TOS(), 3 * 2)

    def test_factorial(self):
        source_code = '5 "n" store 3 "k" store "n" load ! "k" load !'
        stack_machine = StackMachine(source_code)
        stack_machine.launch()

        # k!
        self.assertEqual(stack_machine.get_TOS(), 6)
        # n!
        self.assertEqual(stack_machine.get_TOS(), 120)


if __name__ == '__main__':
    unittest.main()
