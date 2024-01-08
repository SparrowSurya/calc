"""
This module contains model objects.
"""

from calc.common import KeyKind, KeyData, Response, Result
from .evaluator import evaluate


class ExprModel:
    """Manages the expression and the associated operations"""

    def __init__(self, initial_expr: str = ''):
        self._expr = initial_expr
        self._eval = evaluate

    def eval(self, expr: str) -> int | float | Exception:
        """Evaluates the expression and returns the result."""
        try:
            result = self._eval(expr)
        except Exception as error:
            result = error
        return result

    @property
    def expr(self) -> str:
        """get expr"""
        return self._expr

    @expr.setter
    def expr(self, expr: str):
        """set expr"""
        self._expr = expr

    def eval_key(self, keydata: KeyData):
        """
        Evaluates keydata and appropriate response is provided.
        """
        response = Response.EXPR
        data = None

        match keydata.kind:
            case KeyKind.BACKSPACE:
                self._expr = self._expr[:-1]

            case KeyKind.CLEAR:
                self._expr = ''

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
