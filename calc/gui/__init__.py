"""
Module: calc.gui
Description: Provides the default tkinter implementation GUI view for calculator.
"""

from typing import Any
import tkinter as tk
from tkinter import messagebox

from .components.button import Button
from .components.input_box import InputBox
from ..view import AbstractView, resolve_key


keypad = (
    ("CE", "(", ")", "⌫"),
    ("%", "e", "π", "/"),
    ("9", "8", "7", "*"),
    ("6", "5", "4", "-"),
    ("3", "2", "1", "+"),
    (",", "0", ".", "="),
)


class TkView(tk.Tk, AbstractView):
    """Tkinter view for the application."""

    keypad = keypad

    def __init__(self, title: str, control: Any | None = None):
        """
        Creates tkinter window.

        Arguemnts:
        - title: name of the window.
        - control: main application.
        """
        tk.Tk.__init__(self)
        AbstractView.__init__(self, control)

        self.wm_title(title)
        self.resizable(False, False)

        # constructing interface
        self.config(bg="#232323")

        root = tk.Frame(self, bg="#232323", relief="flat")
        root.pack(padx=2, pady=2)

        display = tk.Frame(root, bg="#232323", relief="flat")
        display.pack(expand=1, fill="x")

        self.input_box = InputBox(display)
        self.input_box.pack(fill="x", padx=6, pady=12, ipadx=0, ipady=0)

        buttons = tk.Frame(root, bg="#232323", relief="flat")
        buttons.pack(expand=1, fill="both")

        for i, row in enumerate(self.keypad):
            for j, key in enumerate(row):
                btn = Button(buttons, key, self.callback)
                btn.grid(
                    row=i, column=j, padx=2, pady=2, ipadx=24, ipady=8, sticky="nsew"
                )

        self.bind("<Key-Return>", self.callback)
        self.bind("<Key-Delete>", lambda _: self.callback("cls"))

    @property
    def expression(self) -> str:
        return self.input_box.get_text()

    def show_expression(self, expr: str):
        return self.input_box.set_text(expr)

    def callback(self, event: tk.Event | str = ""):
        """Handles the key input events in the application.

        Arguments:
        - event: tkinter event with keypress info or key as string.
        """
        key = resolve_key(event.char if isinstance(event, tk.Event) else event)
        if key == "backspace":
            self.input_box.backspace()
        elif key == "clear":
            self.input_box.clear()
        elif key == "equal":
            if self.control:
                self.control.evaluate_expression()
        elif key != "":
            self.input_box.push(key)

    def show_error(self, error: Exception):
        title = type(error).__name__
        message = str(error)
        return messagebox.showerror(title, message)

    def mainloop(self):
        self.input_box.focus()
        return super().mainloop()


if __name__ == "__main__":
    view = TkView(title="Test Calculator View", control=None)
    view.mainloop()
