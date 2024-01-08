"""
This module contains button widget.
"""

from typing import Callable
from functools import cached_property

import tkinter as tk


class Button(tk.Button):
    """Calculator Button Widget"""
    style = {
        "bg": "#3c3c3c",
        "fg": "#c0c0c0",
        "bd": 0,
        "relief": "flat",
        "font": ("Accuratist", 16, "normal"),
        "height": 16,
        "width": 24,
    }

    def __init__(self, parent: tk.Misc, key: str, callback: Callable[[str], None]):
        self._key = key
        self._callback = callback
        
        super().__init__(
            parent,
            text=self._key,
            image=self.img,
            compound=tk.CENTER,
            command=self.click,
            **self.style,
        )

    @cached_property
    def img(self) -> tk.PhotoImage:
        return tk.PhotoImage()

    def click(self):
        """Invokes callback"""
        if callable(self._callback):
            self._callback(self._key)
