"""
Module: calc.exceptions
Description: Provides the base error class for calaulator.
"""


class CalcError(Exception):
    """Base exception class for errors raised in the application."""

    def __init__(self, expr: str, *msg: object):
        """
        Arguments:
        - expr: input expression.
        - msg: messages or data objects.
        """
        super().__init__(*msg)
        self.expr = expr

    @property
    def name(self) -> str:
        """Name of the error."""
        return type(self).__name__

    @property
    def description(self) -> str:
        """Provides the exception messages provided."""
        return "\n".join(map(str, self.args))

    @staticmethod
    def get_marker(length: int, pad: int, mark: str = "^") -> str:
        """Provides the underline marker highlighting."""
        return " " * pad + mark * length

    def __str__(self) -> str:
        """Representation of the error."""
        return f"{self.name}: {self.description}"
