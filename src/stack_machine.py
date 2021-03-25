# Copyright 2021 aaaaaaaalesha <sks2311211@mail.ru>

from src.stack import Stack


class StackMachine:
    """Implementation of virtual stack machine."""

    def __init__(self, text):
        self.__ds = Stack()
        self.__rs = Stack()
        self.__ip = None
        self.__text = text
