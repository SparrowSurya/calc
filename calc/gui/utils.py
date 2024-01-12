"""
Module: calc.gui.utils
Description: Provides the functions for window & its components.
"""

import tkinter as tk

from .config import BACKSPACE, CLEAR, EQUAL, PI


__all__ = ("get_key",)


def get_key(key: tk.Event | str) -> str:
    """
    Provides the appropriate key from provided data.

    Arguments:
    - key: tkinter event or text string.

    Return:
    - a string for valid key else empty string.
    """
    char = key.char if isinstance(key, tk.Event) else key
    if char in BACKSPACE:
        return "backspace"
    elif char in CLEAR:
        return "clear"
    elif char in EQUAL:
        return "equal"
    elif char in PI:
        return "pi"
    elif len(char) == 1 and ord(char) in range(32, 127):
        return char
    else:
        return ""
