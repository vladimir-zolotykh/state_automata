#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from abc import ABC, abstractmethod

# import pytest


class ConnectionState(ABC):
    @staticmethod
    @abstractmethod
    def open(conn: Connection):
        pass

    @staticmethod
    @abstractmethod
    def read(conn: Connection):
        pass

    @staticmethod
    @abstractmethod
    def write(conn: Connection, data: str):
        pass

    @staticmethod
    @abstractmethod
    def close(conn: Connection):
        pass


class OpenState(ConnectionState):
    @staticmethod
    def open(conn: Connection):
        raise RuntimeError(f"Connection {conn} is already open")

    @staticmethod
    def read(conn: Connection):
        print(f"Reading connection {conn} ...")

    @staticmethod
    def write(conn: Connection):
        print(f"Writing connection {conn} ...")

    @staticmethod
    def close(conn: Connection):
        conn.new_state(ClosedState)


class ClosedState(ConnectionState):
    @staticmethod
    def open(conn: Connection):
        conn.new_state(OpenState)

    @staticmethod
    def read(conn: Connection):
        raise RuntimeError("Cannot read closed connection")

    @staticmethod
    def write(conn: Connection, data):
        raise RuntimeError("Cannot write closed connection")

    @staticmethod
    def close(conn: Connection):
        raise RuntimeError("Already closed")


class Connection:
    def __init__(self):
        self.new_state(ClosedState)

    def open(self):
        self._state.open(self)

    def read(self):
        self._state.read(self)

    def write(self):
        self._state.write(self)

    def close(self):
        self._state.close()

    def new_state(self, state: ConnectionState):
        self._state: ConnectionState = state


def test_connection_smoke():
    conn = Connection()
    for method in (conn.open, conn.read, conn.write, conn.close):
        method()
