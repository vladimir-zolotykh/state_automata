#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self


class ConnectionState(ABC):
    @abstractmethod
    def open(self, conn: Connection) -> Self:
        pass

    @abstractmethod
    def read(self, conn: Connection) -> Self:
        pass

    @abstractmethod
    def write(self, conn: Connection, data: str) -> Self:
        pass

    @abstractmethod
    def close(self, conn: Connection) -> Self:
        pass


class OpenState(ConnectionState):
    def open(self, conn: Connection):
        raise RuntimeError(f"Connection {conn} is already open")

    def read(self, conn: Connection):
        print(f"Reading connection {conn} ...")
        return self

    def write(self, conn: Connection, data):
        print(f"Writing connection {conn} ...")
        return self

    def close(self, conn: Connection):
        return ClosedState()


class ClosedState(ConnectionState):
    def open(self, conn: Connection):
        return OpenState()

    def read(self, conn: Connection):
        raise RuntimeError("Cannot read closed connection")

    def write(self, conn: Connection, data):
        raise RuntimeError("Cannot write closed connection")

    def close(self, conn: Connection):
        raise RuntimeError("Already closed")


class Connection:
    def __init__(self) -> None:
        self._state: ConnectionState = ClosedState()

    def open(self):
        self._state = self._state.open(self)

    def read(self):
        self._state = self._state.read(self)

    def write(self, data):
        self._state = self._state.write(self, data)

    def close(self):
        self._state = self._state.close(self)


def test_states(capsys):
    conn = Connection()

    try:
        conn.read()
    except RuntimeError as err:
        print(f"*** {err}")

    conn.open()
    conn.read()
    conn.write("asdf")
    conn.close()

    try:
        conn.close()
    except RuntimeError as err:
        print(f"*** {err}")

    out = capsys.readouterr().out

    assert "*** Cannot read closed connection" in out
    assert "Reading connection" in out
    assert "Writing connection" in out
    assert "*** Already closed" in out
