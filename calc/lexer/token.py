"""
This module contains `TokenType` and `Token` class object.
"""

from dataclasses import dataclass
from functools import cached_property
from enum import StrEnum, auto


class TokenType(StrEnum):
    """Identifies each kind of token"""

    NUMBER  = auto()
    PLUS    = auto()
    MINUS   = auto()
    MUL     = auto()
    DIV     = auto()
    MOD     = auto()
    POW     = auto()
    LPAREN  = auto()
    RPAREN  = auto()
    NAME    = auto()
    COMMA   = auto()


@dataclass(frozen=True, repr=False)
class Token:
    """An atomic entity/element in the expression"""

    type: TokenType
    value: str
    index: int

    def __post_init__(self):
        if self.index < 0:
            raise TypeError("Start index cannot be -ve")
        if len(self.value) == 0:
            raise ValueError("No value provided")

    @cached_property
    def length(self) -> int:
        """Length of token value captured"""
        return len(self.value)

    @cached_property
    def end(self) -> int:
        """Last index of token. Similar to `start + length`"""
        return self.index + self.length

    def __repr__(self) -> str:
        return f"Token({self.type.upper()!s}, {self.value}, {self.index}:{self.end})"
