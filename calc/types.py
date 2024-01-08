"""
This module contains the definitions for some objects
"""

from __future__ import annotations
from typing import Protocol, Callable, Iterator, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from .lexer.token import TokenType
    from .parser.node import Node


class _Token(Protocol):
    @property
    def type(self) -> TokenType: ...
    @property
    def value(self) -> str: ...
    @property
    def index(self) -> int: ...
    @property
    def end(self) -> int: ...
    @property
    def length(self) -> int: ...

_Lexer = Callable[[str], Iterator[_Token]]

class _Node(Protocol):
    value: int
    left: _Node
    right: _Node
    op: str
    expr: _Node
    name: str
    args: Iterable[_Node]

    @classmethod
    def from_dict(cls, *args) -> _Node: ...
    def to_dict(self) -> dict: ...

_Parser = Callable[[str, _Lexer], _Node]
_Num = int | float
_Func = dict[str, Callable]
_Const = dict[str, int | float]
