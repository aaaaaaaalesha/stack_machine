# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from collections import deque


class Stack(deque):
    """
    Stack implementation based on collections.deque.
    Source: https://www.geeksforgeeks.org/stack-in-python/
    """

    def __str__(self):
        repr_version = self.copy()
        repr_version.reverse()

        return "Stack" + list(repr_version).__str__()

    def __len__(self):
        return len(self)

    def __bool__(self):
        return bool(self)

    def top(self):
        """
        Accesses the top element.
        @return: top element in stack.
        """
        head = self.pop()
        self.push(head)
        return head

    def push(self, value):
        """
        Inserts element at the top.
        @param value: the element that is put on the stack;
        """
        return self.append(value)

    pop = deque.pop
