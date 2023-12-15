"""
This module contains base view objects.
"""

import abc
from typing import Iterable

from .types import _Token, _Node


class AbstractView(abc.ABC):
    """Abstrcat Base class for view"""


class TokenView(AbstractView):
    """Abstract base class for expression's token viewer"""

    @abc.abstractmethod
    def token_view(self, tokens: Iterable[_Token]) -> object:
        raise NotImplementedError


class AstView(AbstractView):
    """Abstract base class for expression's ast viewer"""

    @abc.abstractmethod
    def ast_view(self, root: _Node) -> object:
        raise NotImplementedError


class ErrorView(AbstractView):
    """Error viewer object"""

    @abc.abstractmethod
    def error_view(self, title: str, *args: object) -> object:
        raise NotImplementedError


class View(TokenView, AstView, ErrorView):
    """Abstrcat Base viewer class with collection of views"""

    @abc.abstractmethod
    def expr_view(self, expr: str) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def eval_view(self, expr: str, result: str) -> object:
        raise NotImplementedError
