"""
This module contains exception classes raised during evaluation.
"""

from ..exceptions import CalcError
from ..types import _Node


class EvaluationError(CalcError):
    """Raised for errors during expression evaluation."""


class DivideByZeroError(EvaluationError):
    """raised when results in zero division error"""

    def __init__(self, expr: str, pos: int, *msg: object):
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
    """raised when function is not found"""

    def __init__(self, expr: str, fn: str, pos: int, *msg: object):
        super().__init__(expr, *msg)
        self.fn = fn
        self.pos = pos

    def __str__(self) -> str:
        marker = '^' * len(self.fn)
        shift = self.pos + len(self.fn) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"function '{self.fn}' is not defined"
        )

class UnknownConstNameError(EvaluationError):
    """raised when constant is not found"""

    def __init__(self, expr: str, const: str, pos: int, *msg: object):
        super().__init__(expr, *msg)
        self.const = const
        self.pos = pos

    def __str__(self) -> str:
        marker = '^' * len(self.const)
        shift = self.pos + len(self.const) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"constant '{self.const}' is not defined"
        )


class WrongArgCountError(EvaluationError):
    """raised when functions gets wrong number of arguments"""

    def __init__(self, expr: str, fn: str, pos: int, *msg: object):
        super().__init__(expr, *msg)
        self.fn = fn
        self.pos = pos

    def __str__(self) -> str:
        marker = '^' * len(self.fn)
        shift = self.pos + len(self.fn) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"function '{self.fn}' got wrong number of arguments"
        )


class MathDomainError(EvaluationError):
    """raised when the value provided is not in domain"""

    def __init__(self, expr: str, fn: str, pos: int, *msg: object):
        super().__init__(expr, *msg)
        self.fn = fn
        self.pos = pos

    def __str__(self) -> str:
        marker = '^' * len(self.fn)
        shift = self.pos + len(self.fn) + 13
        return (
            f"{self.name}: {self.description} \n"
            f"Expression: '{self.expr}' \n"
            f"{marker:>{shift}} \n"
            f"function '{self.fn}' got a value out of domain"
        )



class MethodNotFoundError(EvaluationError):
    """raise when certain eval method isnot found"""

    def __init__(self, expr: str, method: str, node: _Node, *msg: object):
        super().__init__(expr, *msg)
        self.method = method
        self.node = node

    def __str__(self) -> str:
        node = type(node).__name__
        return (
            f"{self.name}: {self.description} \n"
            f"unable to find method '{self.method}' for node '{node}'"
        )
