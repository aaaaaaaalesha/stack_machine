# Copyright 2021 aaaaaaaalesha

import unittest
from src.stack import Stack


class StackTestCase(unittest.TestCase):

    def test_stack_empty(self):
        stack = Stack()
        self.assertTrue(stack.empty())

        stack.push(1)
        self.assertFalse(stack.empty())

        stack.push(2)
        self.assertEqual(stack.__str__(), "Stack[2, 1]")
        self.assertFalse(stack.empty())

        stack.clear()

        self.assertTrue(stack.empty())

    def test_stack_pop_top(self):
        stack = Stack()

        self.assertTrue(stack.empty())

        stack.push(1)
        self.assertFalse(stack.empty())
        self.assertEqual(stack.top(), 1)

        stack.push(2)
        self.assertEqual(stack.top(), 2)

        stack.push(3)
        self.assertEqual(stack.top(), 3)
        self.assertEqual(stack.__str__(), "Stack[3, 2, 1]")

        self.assertEqual(stack.pop(), 3)

        self.assertEqual(stack.pop(), 2)

        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.empty())


if __name__ == '__main__':
    unittest.main()
