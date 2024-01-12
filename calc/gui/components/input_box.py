"""
Module: calc.gui.components.input_box
Description: Provides the input box widget.
"""

from typing import Callable
import tkinter as tk

from ..utils import get_key


class InputBox(tk.Entry):
    """Calculator InputBox widget."""

    style = {
        "background": "#232323",
        "foreground": "#ff646c",
        "selectforeground": "#232323",
        "selectbackground": "#ff646c",
        "relief": "flat",
        "font": ("Roboto", 20, "bold"),
        "insertbackground": "#fffada",
        "insertwidth": 2,
    }

    def __init__(self, parent: tk.Misc, on_return: Callable[[str], None]):
        """
        Argument:
        - parent: parent widget.
        - on_input: callback function when provided keyboard input.
        """
        self.on_return = on_return
        super().__init__(parent, justify=tk.RIGHT, **self.style)
        self.bind("<Return>", self.callback)
        self.bind("<Key-Delete>", lambda _: self.clear())

    def callback(self, e: tk.Event):
        """Invoke callback when enter key is pressed."""
        if callable(self.on_return):
            self.on_return(e.char)

    def get_text(self) -> str:
        """Returns the text from buffer"""
        return self.get()

    def set_text(self, text: str):
        """Sets the buffer text"""
        self.clear()
        self.insert("0", text)

    def push(self, text: str):
        """Inserts the text at place of cursor."""
        self.insert("end", text)

    def clear(self):
        """Clears the text."""
        self.delete("0", "end")

    def backspace(self):
        """Removes a character from end."""
        self.delete(self.index("end") - 1)
