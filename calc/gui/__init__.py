"""
This package contains the GUI object.
"""

from typing import Callable
import tkinter as tk
from tkinter import messagebox

from .components.button import Button
from .components.input_box import InputBox
from .config import keypad, BACKSPACE, CLEAR, EQUAL, PI
from ..common import KeyKind, KeyData, Response, Result


class Window(tk.Tk):
    """Graphical User Interface object"""

    keypad = keypad

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.on_input: Callable[[KeyData], None] = None

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

        self.bind("<Key>", lambda e: self.callback(e.char))
        self.bind("<Delete>", lambda _: self.callback("cls"))

    def callback(self, key: str):
        """Provide the key entered or button pressed info to controller"""
        if callable(self.on_input):
            data = self.resolve_keydata(key)
            self.on_input(data)

    def resolve_keydata(self, key: str) -> KeyData:
        """Returns keydata from key input"""
        if key in BACKSPACE:
            return KeyData(KeyKind.BACKSPACE)
        if key in EQUAL:
            return KeyData(KeyKind.EQUAL)
        if key in CLEAR:
            return KeyData(KeyKind.CLEAR)
        if key in PI:
            key = "pi"
        return KeyData(KeyKind.INSERT, key)

    def update_expr(self, result: Result):
        """Sets the expression on display"""
        match result.response:
            case Response.ERROR:
                self.show_error(result.data)
                self.input_box.set(str(result.expr))

            case Response.EVAL:
                self.input_box.set(str(result.data))

            case Response.EXPR:
                self.input_box.set(str(result.expr))

    def show_error(self, error: Exception):
        """Display the error"""
        messagebox.showerror(type(error).__name__, message=str(error))


if __name__ == "__main__":
    app = Window()
    app.setup()
