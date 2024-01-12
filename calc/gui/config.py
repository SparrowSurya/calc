"""
Module: calc.gui.config
Description: Provides the configuration for ui.
"""

# 6x4 keypad
keypad = (
    ("CE", "(", ")", "⌫"),
    ("%", "e", "π", "/"),
    ("9", "8", "7", "*"),
    ("6", "5", "4", "-"),
    ("3", "2", "1", "+"),
    (",", "0", ".", "="),
)

BACKSPACE = ("⌫", "\x08", "backspace")
CLEAR = ("CE", "cls", "clear", "clean", "del", "delete")
EQUAL = ("=", "\r", "equal", "equals")
PI = ("π", "pi")
