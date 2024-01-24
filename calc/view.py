"""
Module: calc.view
Descrption: Provides the abstract view for calculator user interface and common functions/values.
"""

import abc
from typing import Any


class AbstractView(abc.ABC):
    """Abstract View class to implement an interface for the controller."""

    def __init__(self, control: Any | None = None):
        """
        Creates an interface for user to interact with.

        Should update the controller's view attribute for output to be visible.

        Arguemnts:
        - control: main application (if None then should non-interactive)
        """
        self.control = control
        if self.control is not None:
            self.control.view = self

    @abc.abstractproperty
    def expression(self) -> str:
        """Provides the input expression from user."""

    @abc.abstractmethod
    def show_expression(self, expression: str) -> None:
        """Shows the provided expression.

        Arguemnts:
        - expression: an expression or calculated value.
        """

    @abc.abstractmethod
    def show_error(self, error: Exception) -> None:
        """Shows the expression from user.

        Arguemnts:
        - error: kind of error raised during expression evaluation.
        """

    @abc.abstractmethod
    def mainloop(self) -> None:
        """Keeps the view open."""


# required to resolve_key to work properly
KEY_CONFIG = {
    "backspace": ["⌫", "\x08", "backspace"],
    "clear": ["CE", "cls", "clear", "clean", "del", "delete"],
    "equal": ["=", "\r", "\n", "equal", "equals"],
    "pi": ["π", "pi"],
    "_": lambda key: len(key) == 1 and ord(key) in range(32, 127),
}


def resolve_key(keydata: str) -> str:
    """
    Provides the suitable key name from provided keydata.

    Arguments:
    - key: a text string.

    Returns:
    - a suitable name for the keydata else empty string.
    """
    for key, obj in KEY_CONFIG.items():
        if callable(obj):
            if obj(keydata) is True:
                return keydata if key == "_" else key
        else:
            if keydata in obj:
                return key
    return ""
