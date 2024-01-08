"""
This module contains input widget.
"""

from typing import Callable

import tkinter as tk


class InputBox(tk.Entry):
    """Calculator InputBox widget."""
    style = {
        "disabledbackground": "#232323",
        "disabledforeground": "#ff646c",
        "relief": "flat",
        "font": ("Roboto", 20, "bold"),
        "cursor": "",
        "width": 1,
    }

    def __init__(self, parent: tk.Misc, on_input: Callable[[str], None]):
        self._var = tk.StringVar()
        super().__init__(
            parent,
            textvariable=self._var,
            state="disabled",
            justify=tk.RIGHT,
            **self.style
        )
        self.on_input = on_input
        self.bind('<Key>', self.call)

    def get(self) -> str:
        """Returns the text from buffer"""
        return self._var.get()

    def set(self, text: str):
        """Sets the buffer text"""
        self._var.set(text)

    def call(self, e: tk.Event):
        """Informs main running gui program for keyboard input"""
        if callable(self.on_input):
            self.on_input(e.char)