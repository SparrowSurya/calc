"""
Module: calc.models
Description: Provides the model class to handle expression operations.
"""

import abc

from .evaluator import evaluate


class AbstractModel(abc.ABC):
    """Abstract Model for main application engine."""

    @abc.abstractmethod
    def evaluate(self, expression: str) -> tuple[int | float | Exception, bool]:
        """Calcualte the value from expression.

        Arguments:
        - expression: input expression.

        Returns:
        - result of evaluation.
        - success of evaluation.
        """
        raise NotImplementedError


class CalcModel(AbstractModel):
    _eval = staticmethod(evaluate)
    """function to evaluate the expression."""

    def evaluate(self, expression: str) -> tuple[int | float | Exception, bool]:
        success = True

        try:
            result = self._eval(expression)
        except Exception as error:
            success = False
            result = error

        return result, success
