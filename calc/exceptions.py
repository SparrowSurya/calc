"""
This module contains base exception class.
"""


class CalcError(Exception):
    """Base class for all Calc errors."""

    def __init__(self, expr: str, *msg: object):
        super().__init__(*msg)
        self.expr = expr

    @property
    def description(self) -> str:
        return '\n'.join(map(str, self.args))

    @property
    def name(self) -> str:
        return type(self).__name__

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class LexicalError(CalcError):
    """Raised for errors during tokenization."""


class ParsingError(CalcError):
    """Raised for errors during parsing."""


class EvaluationError(CalcError):
    """Raised for errors during expression evaluation."""


class InternalError(CalcError):
    """Raised for unexpected errors or bugs."""
