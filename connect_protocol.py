#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations

from typing import Protocol
from dataclasses import dataclass


class State(Protocol):
    def open(self, conn: Connection) -> Connection: ...  # noqa: E704
    def read(self, conn: Connection) -> Connection: ...  # noqa: E704
    def write(self, conn: Connection, data) -> Connection: ...  # noqa: E704
    def close(self, conn: Connection) -> Connection: ...  # noqa: E704


@dataclass(frozen=True)
class OpenState:
    def open(self, conn: Connection):
        raise RuntimeError(f"Connection {conn} is already open")

    def read(self, conn: Connection):
        print(f"Reading connection {conn} ...")
        return conn

    def write(self, conn: Connection, data):
        print(f"Writing connection {conn} ...")
        return conn

    def close(self, conn: Connection):
        return type(conn)(_state=ClosedState())


@dataclass(frozen=True)
class ClosedState:
    def open(self, conn: Connection):
        return type(conn)(_state=OpenState())

    def read(self, conn: Connection):
        raise RuntimeError("Cannot read closed connection")

    def write(self, conn: Connection, data):
        raise RuntimeError("Cannot write closed connection")

    def close(self, conn: Connection):
        raise RuntimeError("Already closed")


@dataclass(frozen=True)
class Connection:
    _state: State

    def open(self):
        return self._state.open(self)

    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def close(self):
        return self._state.close(self)


def new_connection() -> Connection:
    return Connection(_state=ClosedState())


def test_states(capsys):
    conn = new_connection()

    try:
        conn.read()
    except RuntimeError as err:
        print(f"*** {err}")

    conn = conn.open()
    conn = conn.read()
    conn = conn.write("asdf")
    conn = conn.close()

    try:
        conn.close()
    except RuntimeError as err:
        print(f"*** {err}")

    out = capsys.readouterr().out

    assert "*** Cannot read closed connection" in out
    assert "Reading connection" in out
    assert "Writing connection" in out
    assert "*** Already closed" in out
