"""
Module: calc.evaluator.exceptions
Description: Provides exception classes raised during evaluation.
"""

from ..exceptions import CalcError
from ..parser.node import Node


__all__ = (
    "EvaluationError",
    "DivideByZeroError",
    "UnknownFuncNameError",
    "UnknownConstNameError",
    "WrongArgCountError",
    "MathDomainError",
    "MethodNotFoundError",
)


class EvaluationError(CalcError):
    """Raised for errors during expression evaluation."""


class DivideByZeroError(EvaluationError):
    """Raised when results in zero division error."""

    def __init__(self, expr: str, pos: int, *msg: object):
        """
        Arguments:
        - expr: expression.
        - pos: position of the division operator in expression.
        - msg: messages or data objects.
        """
        super().__init__(expr, *msg)
        self.pos = pos

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{'^':>{self.pos+14}} \n"
            f"Denominator evaluated to zero"
        )


class UnknownFuncNameError(EvaluationError):
    """Raised when function used in expression is not found."""

    def __init__(self, expr: str, fn: str, pos: int, *msg: object):
        """
        Arguments:
        - expr: expression.
        - fn: name of the function used in expression.
        - pos: position of function in expression.
        - msg: messages or data objects.
        """
        super().__init__(expr, *msg)
        self.fn = fn
        self.pos = pos

    def __str__(self) -> str:
        marker = "^" * len(self.fn)
        shift = self.pos + len(self.fn) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"function '{self.fn}' is not defined"
        )


class UnknownConstNameError(EvaluationError):
    """Raised when constant used in expression is not found."""

    def __init__(self, expr: str, const: str, pos: int, *msg: object):
        """
        Arguments:
        - expr: expression.
        - const: name of the constant used in expression.
        - pos: position of constant in expression.
        - msg: messages or data objects.
        """
        super().__init__(expr, *msg)
        self.const = const
        self.pos = pos

    def __str__(self) -> str:
        marker = "^" * len(self.const)
        shift = self.pos + len(self.const) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"constant '{self.const}' is not defined"
        )


class WrongArgCountError(EvaluationError):
    """Raised when function receives wrong number of arguments."""

    def __init__(self, expr: str, fn: str, pos: int, *msg: object):
        """
        Arguments:
        - expr: expression.
        - fn: name of the function.
        - pos: position of function in expression.
        - msg: messages or data objects.
        """
        super().__init__(expr, *msg)
        self.fn = fn
        self.pos = pos

    def __str__(self) -> str:
        marker = "^" * len(self.fn)
        shift = self.pos + len(self.fn) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"function '{self.fn}' got wrong number of arguments"
        )


class MathDomainError(EvaluationError):
    """Raised when the value provided is not in domain of the function."""

    def __init__(self, expr: str, fn: str, pos: int, *msg: object):
        """
        Arguments:
        - expr: expression.
        - fn: name of the function.
        - pos: position of function in expression.
        - msg: messages or data objects.
        """
        super().__init__(expr, *msg)
        self.fn = fn
        self.pos = pos

    def __str__(self) -> str:
        marker = "^" * len(self.fn)
        shift = self.pos + len(self.fn) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"function '{self.fn}' got a value out of domain"
        )


class MethodNotFoundError(EvaluationError):
    """Raised when certain eval method is not found to evaluate the node."""

    def __init__(self, expr: str, method: str, node: Node, *msg: object):
        """
        Arguments:
        - expr: expression.
        - method: expected method name.
        - node: node which was expected to evaluated by the method.
        - msg: messages or data objects.
        """
        super().__init__(expr, *msg)
        self.method = method
        self.node = node

    def __str__(self) -> str:
        node = type(node).__name__
        return (
            f"{self.name}: {self.description} \n"
            f"unable to find method '{self.method}' for node '{node}'"
        )
