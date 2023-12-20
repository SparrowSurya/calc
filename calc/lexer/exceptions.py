"""
This module contains Exception classes raised during lexing.
"""

from ..exceptions import CalcError


class LexicalError(CalcError):
    """Raised for errors during tokenization."""


class IllegalCharError(LexicalError):
    """Character does not matched any atomic lexer"""

    def __init__(self, expr: str, pos: int, *msg: object):
        super().__init__(expr, *msg)
        self.pos = pos

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{'^':>{self.pos+14}}"
        )
