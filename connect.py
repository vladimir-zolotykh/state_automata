#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import singledispatchmethod


class State:
    pass


class OpenState(State):
    pass


class ClosedState(State):
    pass


class Connection:
    def __init__(self):
        self._state = ClosedState()

    @singledispatchmethod
    def open(self, state):
        raise NotImplementedError()

    @open.register
    def _(self, state: OpenState):
        raise RuntimeError("Already open")

    @open.register
    def _open(self, state: ClosedState):
        self._state = OpenState()

    @singledispatchmethod
    def read(self, state):
        raise NotImplementedError("Cannot read")

    @read.register
    def _(self, state: OpenState):
        print("Reading ...")

    @read.register
    def _(self, state: ClosedState):
        raise RuntimeError("Closed")

    @singledispatchmethod
    def write(self, state):
        raise NotImplementedError("Cannot write")

    @write.register
    def _(self, state: OpenState):
        print("Writing ...")

    @write.register
    def _(sefl, state: ClosedState):
        raise RuntimeError("Cannot write")

    @singledispatchmethod
    def close(self, state):
        raise NotImplementedError()

    @close.register
    def _(self, state: OpenState):
        self._state = ClosedState()

    @close.register
    def _(self, state: ClosedState):
        raise RuntimeError("Already closed")


if __name__ == "__main__":
    conn = Connection()
    openstate = OpenState()
    conn.read(openstate)
    conn.write(openstate)
    conn.close(openstate)
