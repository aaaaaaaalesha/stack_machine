# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from collections import deque


class Stack(deque):
    """
    Best way for stack implementation based on collections.deque.
    Source: https://www.geeksforgeeks.org/stack-in-python/
    """

    def __str__(self):
        """Overrides the string representation of my stack."""
        repr_version = self.copy()
        repr_version.reverse()

        return "Stack" + list(repr_version).__str__()

    def empty(self):
        return len(self) == 0

    def top(self):
        """Accesses the top element."""
        head = self.pop()
        self.push(head)
        return head

    def push(self, value):
        """Inserts element at the top."""
        return self.append(value)

    pop = deque.pop
