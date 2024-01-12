"""
Module: calc.models
Description: Provides the model class to handle expression operations.
"""

from .evaluator import evaluate


class ExprModel:
    """A model class to provide operations for the expression."""

    _eval = staticmethod(evaluate)
    """function to evaluate the expression."""

    def evaluate(self, expr: str) -> tuple[int | float | Exception, bool]:
        """Expression evaluation.

        Arguments:
        - expr: input expression.

        Returns:
        - result: evaluated value or Exception.
        - success: False if result is error otherwise True.
        """
        success = True

        try:
            result = self._eval(expr)
        except Exception as error:
            success = False
            result = error

        return result, success
