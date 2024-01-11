"""
Module: calc.lexer.exception
Description: provides the exception classes raised during lexical analysis
"""

from ..exceptions import CalcError


__all__ = (
    "LexicalError",
    "IllegalCharError",
)


class LexicalError(CalcError):
    """Raised for errors during lexical analysis"""


class IllegalCharError(LexicalError):
    """Raised when a character is not matched by any of lexer unit"""

    def __init__(self, expr: str, pos: int, *msg: object):
        """
        Arguments:
        - expr: Expression
        - pos: position in the expression
        - msg: error message
        """
        super().__init__(expr, *msg)
        self.pos = pos

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{'^':>{self.pos+14}}"
        )
