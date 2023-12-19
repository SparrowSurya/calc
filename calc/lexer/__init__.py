"""
This package contains Lexer class for lexing various tokens in expression.
"""

from __future__ import annotations
from typing import Iterator

from .token import Token
from .atomic_lexer import AtomicLexer
from .exceptions import IllegalCharError
from .lexers import lexers



class Lexer:
    """Lexer object to tokenise the expression"""

    def __init__(self, expr: str, ignore_chars: str, atomic_lexers: tuple[AtomicLexer]):
        self.expr = expr
        self.ignore_chars = ignore_chars
        self.lexers = atomic_lexers

        self.pos = 0
        self.char: str | None = None
        self.advance()

    def advance(self):
        """moves to next character of expression"""
        try:
            self.char = self.expr[self.pos]
            self.ignore()
        except IndexError:
            self.char = None

    def ignore(self):
        """skips character to be ignored"""
        while self.char in self.ignore_chars:
            self.pos += 1
            self.char = self.expr[self.pos]

    def illegal_char_error(self) -> IllegalCharError:
        """returns illegal character object"""
        msg = f"illegal character '{self.char}' found at index {self.pos} during lexing"
        return IllegalCharError(self.expr, self.pos, msg)

    def next_token(self) -> Token:
        """tokenises expression one at a time"""
        if self.pos >= len(self.expr):
            raise StopIteration

        while True:
            for cls_lexer in self.lexers:
                if cls_lexer.match(self.char):
                    lexer: AtomicLexer = cls_lexer(self.expr, self.pos)
                    tok = lexer.get_token()
                    self.pos += len(tok.value)
                    self.advance()
                    return tok

            raise self.illegal_char_error()

    def __iter__(self) -> Lexer:
        return self

    __next__ = next_token


def lex(expr: str, ignore_chars: str = ' \t\n\r') -> Iterator[Token]:
    """returns iterator of tokens"""
    return iter(
        Lexer(expr=expr, ignore_chars=ignore_chars, atomic_lexers=lexers)
    )
