"""
This module contains Exception classes raised during lexing.
"""


class IllegalCharacterError(Exception):
    """Character does not matched any atomic lexer"""

    def __init__(self, expr: str, pos: int):
        self.expr = expr
        self.pos = pos

    def __str__(self) -> str:
        pos = self.pos+1
        return '\n'.join([
            f"Illegal character '{self.expr[self.pos]}' found at {self.pos}",
            f"{self.expr}",
            f"{'^':>{pos}}",
        ])
