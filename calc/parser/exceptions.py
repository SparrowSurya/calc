"""
Module: calc.parser.exceptions
Description: Provide exception classes raised during parsing.
"""

from ..lexer.token import Token
from ..exceptions import CalcError


__all__ = (
    "ParsingError",
    "UnknownTokenError",
    "SyntaxError",
    "UnexpectedEndOfInputError",
)


class ParsingError(CalcError):
    """Raised for errors during parsing."""


class UnknownTokenError(ParsingError):
    """Raised when there is no suitable method provided to parse the token."""

    def __init__(self, expr: str, token: Token, *args: object):
        """
        Arguments:
        - expr: expression.
        - token: unknown token.
        - args: messages or data objects.
        """
        super().__init__(expr, *args)
        self.token = token

    def __str__(self) -> str:
        marker = "^" * self.token.length
        return (
            f"{self.name}: {self.description} \n",
            f"{self.expr} \n",
            f"{marker:>{self.token.index}}",
        )


class SyntaxError(ParsingError):
    """Raised during wrong syntax"""

    def __init__(self, expr: str, token: Token, *args: object):
        """
        Arguments:
        - expr: expression.
        - token: token where the problem occured.
        - args: messages or data objects.
        """
        super().__init__(expr, *args)
        self.token = token

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: {self.expr} \n"
            f"{'^':>{self.pos+14}}",
        )


class UnexpectedEndOfInputError(ParsingError):
    """Raised when given incomplete expression"""

    def __init__(self, expr: str, expected: str, *args: object):
        """
        Arguments:
        - expr: expression.
        - expected: expected value.
        - args: messages or data objects.
        """
        super().__init__(*args)
        self.expr = expr
        self.expected = expected

    def __str__(self) -> str:
        return "n".join(
            [
                f"Unexpected End of Input: {self.expected}",
                f"{self.expr}",
            ]
        )
