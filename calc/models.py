"""
Module: calc.models
Description: Provides the model class to handle expression and operations.
"""

from calc.common import KeyKind, KeyData, Response, Result
from .evaluator import evaluate


class ExprModel:
    """A model class to provide operations for the expression."""

    def __init__(self):
        self._expr = ""
        self._eval = evaluate

    def eval(self, expr: str) -> int | float | Exception:
        """Evaluates the expression and returns the result.

        Argument:
        - expr: input expression.

        Returns:
        - evaluated result or error.
        """
        try:
            result = self._eval(expr)
        except Exception as error:
            result = error
        return result

    @property
    def expr(self) -> str:
        """Gets expression."""
        return self._expr

    @expr.setter
    def expr(self, expr: str):
        """Sets expression."""
        self._expr = expr

    def evaluate(self, keydata: KeyData) -> Result:
        """Evaluates keydata and appropriate response is provided.

        Arguments:
        - keydata: data provided from view.

        Returns:
        - result of the data.
        """
        response = Response.EXPR
        data = None

        match keydata.kind:
            case KeyKind.BACKSPACE:
                self._expr = self._expr[:-1]

            case KeyKind.CLEAR:
                self._expr = ""

            case KeyKind.EQUAL:
                data = self.eval(self._expr)
                if isinstance(data, (int, float, str)):
                    response = Response.EVAL
                    self._expr = str(data)
                else:
                    response = Response.ERROR

            case KeyKind.INSERT:
                self._expr += keydata.char

        return Result(
            response=response,
            expr=self.expr,
            data=data,
        )
