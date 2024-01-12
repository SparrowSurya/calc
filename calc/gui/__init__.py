"""
Module: calc.gui
Description: Provides the GUI object.
"""

from typing import Callable, Any, Iterable
import tkinter as tk
from tkinter import messagebox

from .components.button import Button
from .components.input_box import InputBox
from .config import keypad
from .utils import get_key
from ..exceptions import CalcError


class Window(tk.Tk):
    """Graphical User Interface object"""

    keypad = keypad

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self.evaluate: Callable[[str], Any] = None

    def setup(self):
        """creates and puts widgets on window"""
        self.config(bg="#232323")

        root = tk.Frame(self, bg="#232323", relief="flat")
        root.pack(padx=2, pady=2)

        display = tk.Frame(root, bg="#232323", relief="flat")
        display.pack(expand=1, fill="x")

        self.input_box = InputBox(display, self.callback)
        self.input_box.pack(fill="x", padx=6, pady=12)

        buttons = tk.Frame(root, bg="#232323", relief="flat")
        buttons.pack(expand=1, fill="both")

        for i, row in enumerate(self.keypad):
            for j, key in enumerate(row):
                btn = Button(buttons, key, self.callback)
                btn.grid(
                    row=i, column=j, padx=2, pady=2, ipadx=24, ipady=8, sticky="nsew"
                )

        self.input_box.focus()

    def set_expr(self, expr: str):
        """Sets the expression on display."""
        self.input_box.set_text(expr)

    def get_expr(self) -> str:
        """Gets the expression from display."""
        return self.input_box.get_text()

    def callback(self, event: tk.Event | str = ""):
        """Handles the events in the application.

        Arguments:
        - event: can be tkinter event or a string.
        """
        key = get_key(event)
        if key == "backspace":
            self.input_box.backspace()
        elif key == "clear":
            self.input_box.clear()
        elif key == "equal":
            if callable(self.evaluate):
                self.evaluate(self.get_expr())
        elif key != "":
            self.input_box.push(key)

    def show_error(self, error: Exception):
        """Displays the error message.

        Arguments:
        - error: should be the exception class or its child.
        """
        title = type(error).__name__
        message = str(error)
        messagebox.showerror(title, message)


if __name__ == "__main__":
    app = Window()
    app.setup()
