from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Self


class State(Protocol):
    def open(self, conn: Connection) -> Connection: ...  # noqa: E704
    def read(self, conn: Connection) -> Connection: ...  # noqa: E704
    def write(self, conn: Connection, data: str) -> Connection: ...  # noqa: E704
    def close(self, conn: Connection) -> Connection: ...  # noqa: E704


@dataclass(frozen=True)
class OpenState:
    def open(self, conn: Connection) -> Connection:
        raise RuntimeError(f"Connection {conn} is already open")

    def read(self, conn: Connection) -> Connection:
        print(f"Reading connection {conn} ...")
        return conn  # unchanged

    def write(self, conn: Connection, data: str) -> Connection:
        print(f"Writing connection {conn} ...")
        return conn  # unchanged

    def close(self, conn: Connection) -> Connection:
        return Connection(state=ClosedState())


@dataclass(frozen=True)
class ClosedState:
    def open(self, conn: Connection) -> Connection:
        return Connection(state=OpenState())

    def read(self, conn: Connection) -> Connection:
        raise RuntimeError("Cannot read closed connection")

    def write(self, conn: Connection, data: str) -> Connection:
        raise RuntimeError("Cannot write closed connection")

    def close(self, conn: Connection) -> Connection:
        raise RuntimeError("Already closed")


@dataclass(frozen=True)
class Connection:
    state: State

    def open(self) -> Self:
        # Incompatible return value type (got "Connection", expected "Self")
        return self.state.open(self)

    def read(self) -> Self:
        return self.state.read(self)

    def write(self, data: str) -> Self:
        return self.state.write(self, data)

    def close(self) -> Self:
        return self.state.close(self)


def new_connection() -> Connection:
    return Connection(state=ClosedState())
