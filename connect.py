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
        raise NotImplementedError()

    @read.register
    def _(self, state: OpenState):
        print("Reading ...")

    @read.register
    def _(self, state: ClosedState):
        raise RuntimeError("Closed")

    @singledispatchmethod
    def write(self, state):
        raise NotImplementedError()

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


def test_connection_smoke():
    conn = Connection()
    state = OpenState()
    for method in (conn.read, conn.write, conn.close):
        method(state)
