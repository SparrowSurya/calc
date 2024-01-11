"""
Module: calc.lexer.token
Description: provides classes for representing tokens in expression.

Usage:
>>> from calc.lexer.token import TokenType, Token
>>> t = Token(TokenType.NUMBER, '23.6', 6)
"""

from dataclasses import dataclass
from functools import cached_property
from enum import StrEnum, auto


__all__ = (
    "TokenType",
    "Token",
)


class TokenType(StrEnum):
    """Defines the different types of token in the expression."""

    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    LPAREN = auto()
    RPAREN = auto()
    NAME = auto()
    COMMA = auto()


@dataclass(frozen=True, repr=False)
class Token:
    """A class representing single token in the expression.

    Arguments:
    - type: type of the value captured represented by TokenType.
    - value: value cpatured by the lexer.
    - index: start index of the value in expression.

    Raises:
    - TypeError:
        - type is not an instance of TokenType
    - ValueError:
        - index is a negative value
        - value is empty

    Usage:
    >>> from calc.lexer.token import TokenType, Token
    >>> t = Token(TokenType.NUMBER, '23.6', 6)
    """

    type: TokenType
    value: str
    index: int

    def __post_init__(self):
        if not isinstance(self.type, TokenType):
            raise TypeError(
                "Argument 'type' got value of unexpected type: {}, expected {}",
                type(self.type),
                TokenType,
            )
        if self.index < 0:
            raise ValueError("Start index cannot be -ve")
        if len(self.value) == 0:
            raise ValueError("No value provided")

    def __len__(self) -> int:
        """Length of token value"""
        return len(self.value)

    @cached_property
    def end(self) -> int:
        """End of the token. Equals to start + length"""
        return self.index + len(self)

    def __repr__(self) -> str:
        return f"Token({self.type.upper()!s}, {self.value}, {self.index}:{self.end})"
